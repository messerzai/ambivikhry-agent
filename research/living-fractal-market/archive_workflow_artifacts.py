#!/usr/bin/env python3
"""Archive exact successful LFM GitHub Actions artifacts into the research branch.

The script is branch-scoped, append-only and refuses to replace any existing
path whose bytes differ. It stores original workflow ZIPs plus exact extracted
JSON payloads, and appends provenance/evaluation summaries to FORECAST_LEDGER.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any

API = "https://api.github.com"
FORECAST_WORKFLOW = "lfm-5m.yml"
EVALUATION_WORKFLOW = "lfm-evaluate.yml"
FORECAST_ARTIFACT_NAME = "lfm-5m-btc-forecast"
EVALUATION_ARTIFACT_NAME = "lfm-completed-vintage-evaluation"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def make_vintage_id(forecast: dict[str, Any]) -> str:
    issued = str(forecast["issued_at_utc"])
    asset = str(forecast.get("asset", "BTCUSDT")).replace("/", "")
    venue = slug(str(forecast.get("venue", "binance-spot")))
    version = str(forecast.get("model_version", "unknown")).lower()
    version_tag = "council-" + version.rsplit("council-", 1)[1] if "council-" in version else slug(version)
    return f"lfm5m-{issued}-{asset}-{venue}-{version_tag}"


def request_bytes(url: str, token: str, accept: str = "application/vnd.github+json") -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": accept,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Ambivikhry-LFM-Artifact-Archiver/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def api_json(url: str, token: str) -> dict[str, Any]:
    return json.loads(request_bytes(url, token).decode("utf-8"))


def list_workflow_runs(
    repo: str,
    branch: str,
    workflow_file: str,
    head_sha: str,
    token: str,
) -> list[dict[str, Any]]:
    query = urllib.parse.urlencode({"branch": branch, "per_page": 100})
    url = f"{API}/repos/{repo}/actions/workflows/{workflow_file}/runs?{query}"
    deadline = time.time() + 180
    runs: list[dict[str, Any]] = []
    while True:
        payload = api_json(url, token)
        runs = [
            run for run in payload.get("workflow_runs", [])
            if run.get("head_branch") == branch
        ]
        exact = [run for run in runs if run.get("head_sha") == head_sha]
        if exact or time.time() >= deadline:
            break
        time.sleep(5)

    exact = [run for run in runs if run.get("head_sha") == head_sha]
    if exact:
        deadline = time.time() + 300
        current = exact
        while time.time() < deadline:
            refreshed = []
            for run in current:
                refreshed.append(api_json(
                    f"{API}/repos/{repo}/actions/runs/{run['id']}", token
                ))
            current = refreshed
            if all(run.get("status") == "completed" for run in current):
                break
            time.sleep(5)
        return [
            run for run in current
            if run.get("status") == "completed" and run.get("conclusion") == "success"
        ]

    return [
        run for run in runs
        if run.get("status") == "completed" and run.get("conclusion") == "success"
    ][:20]


def find_artifact(repo: str, run_id: int, artifact_name: str, token: str) -> dict[str, Any] | None:
    payload = api_json(
        f"{API}/repos/{repo}/actions/runs/{run_id}/artifacts?per_page=100",
        token,
    )
    for artifact in payload.get("artifacts", []):
        if artifact.get("name") == artifact_name and not artifact.get("expired", False):
            return artifact
    return None


def download_artifact(repo: str, artifact: dict[str, Any], token: str) -> bytes:
    data = request_bytes(
        f"{API}/repos/{repo}/actions/artifacts/{artifact['id']}/zip",
        token,
        accept="application/vnd.github+json",
    )
    expected = str(artifact.get("digest", "")).removeprefix("sha256:")
    actual = sha256_bytes(data)
    if expected and expected != actual:
        raise ValueError(
            f"artifact digest mismatch for {artifact.get('name')} id={artifact.get('id')}: "
            f"expected {expected}, got {actual}"
        )
    return data


def write_immutable(root: Path, relative_path: str, data: bytes) -> tuple[bool, str]:
    path = root / relative_path
    digest = sha256_bytes(data)
    if path.exists():
        existing = sha256_bytes(path.read_bytes())
        if existing != digest:
            raise RuntimeError(
                f"refusing to overwrite immutable archive {relative_path}: "
                f"existing sha256={existing}, incoming sha256={digest}"
            )
        return False, digest
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return True, digest


def append_forecast_ledger(
    ledger_path: Path,
    run: dict[str, Any],
    artifact: dict[str, Any],
    archive_path: str,
    archive_sha: str,
    json_path: str,
    json_sha: str,
    forecast: dict[str, Any],
) -> bool:
    ledger = ledger_path.read_text(encoding="utf-8")
    if archive_path in ledger:
        return False
    if "## Canonical exact workflow artifact archives" not in ledger:
        ledger += "\n\n## Canonical exact workflow artifact archives (append-only)\n"
    issue = forecast["issued_at_utc"]
    entry = (
        f"\n### {issue} — {forecast.get('asset')} — {forecast.get('model_version')}\n"
        f"- Workflow run: https://github.com/{run['repository']['full_name']}/actions/runs/{run['id']}\n"
        f"- Run checkout commit: {run.get('head_sha')}\n"
        f"- Artifact ID: {artifact['id']} (name: {artifact['name']})\n"
        f"- Exact ZIP archive: {archive_path}\n"
        f"- Exact ZIP SHA-256: {archive_sha}\n"
        f"- Exact extracted JSON: {json_path}\n"
        f"- Exact extracted JSON SHA-256: {json_sha}\n"
        f"- Asset / venue / quote: {forecast.get('asset')} / {forecast.get('venue')} / {forecast.get('quote_currency')}\n"
        f"- Issue / cutoff UTC: {issue} / {forecast.get('data_cutoff_utc')}\n"
        f"- Closed input candles: {forecast.get('closed_candles')} at 5m; hourly targets: 24\n"
    )
    ledger_path.write_text(ledger + entry, encoding="utf-8")
    return True


def archive_forecast_run(
    root: Path,
    repo: str,
    run: dict[str, Any],
    token: str,
    ledger_path: Path,
) -> dict[str, Any]:
    artifact = find_artifact(repo, int(run["id"]), FORECAST_ARTIFACT_NAME, token)
    if artifact is None:
        return {"status": "no_forecast_artifact", "run_id": run["id"]}
    zip_bytes = download_artifact(repo, artifact, token)
    with zipfile.ZipFile(BytesIO(zip_bytes)) as archive:
        names = [name for name in archive.namelist() if name.endswith("forecast_5m.json")]
        if len(names) != 1:
            raise ValueError(f"run {run['id']} artifact must contain one forecast_5m.json")
        forecast_bytes = archive.read(names[0])
    forecast = json.loads(forecast_bytes.decode("utf-8"))
    if forecast.get("schema") != "lfm.forecast.5m.v1":
        raise ValueError(f"unexpected forecast schema in run {run['id']}")
    models = forecast.get("models", [])
    if not models or any(len(model.get("points", [])) != 24 for model in models):
        raise ValueError(f"run {run['id']} forecast does not have 24 points per model")
    if int(forecast.get("closed_candles", 0)) < 300:
        raise ValueError(f"run {run['id']} failed the minimum closed-candle gate")

    issue = str(forecast["issued_at_utc"])
    date = issue[:10]
    stamp = issue.replace(":", "-")
    asset_tag = str(forecast.get("asset", "BTCUSDT")).replace("/", "")
    venue_tag = "".join(ch for ch in str(forecast.get("venue", "BinanceSpot")) if ch.isalnum())
    version = str(forecast.get("model_version", "LFM-unknown"))
    match = re.search(r"(\d+\.\d+)$", version)
    version_tag = f"LFM-5m-{match.group(1)}" if match else slug(version)
    base = f"{stamp}_{asset_tag}_{venue_tag}_{version_tag}"
    archive_rel = f"research/living-fractal-market/forecasts/{date}/{base}.artifact.zip"
    json_rel = f"research/living-fractal-market/forecasts/{date}/{base}.json"

    zip_created, zip_sha = write_immutable(root, archive_rel, zip_bytes)
    json_created, json_sha = write_immutable(root, json_rel, forecast_bytes)
    ledger_changed = append_forecast_ledger(
        ledger_path, run, artifact, archive_rel, zip_sha, json_rel, json_sha, forecast
    )
    return {
        "status": "archived" if zip_created or json_created or ledger_changed else "already_archived",
        "run_id": run["id"],
        "artifact_id": artifact["id"],
        "archive": archive_rel,
        "archive_sha256": zip_sha,
        "forecast_json": json_rel,
        "forecast_json_sha256": json_sha,
    }


def append_evaluation_ledger(
    ledger_path: Path,
    run: dict[str, Any],
    artifact: dict[str, Any],
    artifact_path: str,
    artifact_sha: str,
    evaluation_path: str,
    evaluation_sha: str,
    actual_path: str,
    actual_sha: str,
    evaluation: dict[str, Any],
) -> bool:
    ledger = ledger_path.read_text(encoding="utf-8")
    marker = f"### Evaluation: {evaluation['vintage_id']}"
    if marker in ledger:
        return False
    if "## Evaluation records (append-only)" not in ledger:
        ledger += "\n\n## Evaluation records (append-only)\n"
    baseline = evaluation.get("baseline_results", {})
    random_walk = baseline.get("RandomWalkLastPrice", {}).get("normalized_log_price_mae")
    slow_drift = baseline.get("VolatilityCappedSlowDrift", {}).get("normalized_log_price_mae")
    lines = [
        f"\n{marker}",
        f"- Evaluation workflow: https://github.com/{run['repository']['full_name']}/actions/runs/{run['id']}",
        f"- Evaluation artifact ID: {artifact['id']}",
        f"- Exact evaluation ZIP: {artifact_path}",
        f"- Evaluation ZIP SHA-256: {artifact_sha}",
        f"- Evaluation JSON: {evaluation_path} (SHA-256 {evaluation_sha})",
        f"- Exact actual Binance Spot 1h response: {actual_path} (SHA-256 {actual_sha})",
        f"- Actual data source: {evaluation.get('actual_source')}",
        f"- Evaluated at UTC: {evaluation.get('actual_retrieved_at_utc')}",
        f"- Primary nMAE: normalized by issue-time hourly sigma {evaluation.get('primary_metric', {}).get('denominator_sigma_hour')}.",
        f"- RandomWalkLastPrice nMAE: {random_walk}; VolatilityCappedSlowDrift nMAE: {slow_drift}.",
        f"- P90 intervals calibrated: {evaluation.get('intervals_calibrated')}; virtual points awarded: {evaluation.get('virtual_points_awarded')}.",
    ]
    for model in evaluation.get("model_results_ranked_by_primary_loss", []):
        lines.append(
            f"- {model['model']}: nMAE {model['normalized_log_price_mae']:.6f}; "
            f"direction vs issue {model['directional_accuracy_vs_issue_reference']:.3f}; "
            f"hour-to-hour direction {model['directional_accuracy_hour_to_hour']:.3f}; "
            f"P90 empirical coverage {model['p90_empirical_coverage']}; "
            f"beats RW {model['beats_random_walk_primary_loss']}."
        )
    threshold = evaluation.get("threshold_event_diagnostic")
    if threshold:
        lines.append(
            f"- Terminal threshold diagnostic: {threshold['level_usdt']} USDT; "
            f"uncalibrated heuristic {threshold['heuristic_probability_uncalibrated']}; "
            f"observed terminal-below-level {threshold['observed_terminal_outcome']}; "
            f"diagnostic Brier {threshold['brier_diagnostic_only']} (not a calibrated score)."
        )
    lines.append("- Interpretation: one completed vintage is descriptive only; no champion promotion or research points.")
    ledger_path.write_text(ledger + "\n".join(lines) + "\n", encoding="utf-8")
    return True


def archive_evaluation_run(
    root: Path,
    repo: str,
    run: dict[str, Any],
    token: str,
    ledger_path: Path,
) -> dict[str, Any]:
    artifact = find_artifact(repo, int(run["id"]), EVALUATION_ARTIFACT_NAME, token)
    if artifact is None:
        return {"status": "no_evaluation_artifact", "run_id": run["id"]}
    zip_bytes = download_artifact(repo, artifact, token)
    with zipfile.ZipFile(BytesIO(zip_bytes)) as archive:
        names = archive.namelist()
        manifest_names = [name for name in names if name.endswith("evaluation_manifest.json")]
        if len(manifest_names) != 1:
            raise ValueError(f"evaluation run {run['id']} must contain one evaluation_manifest.json")
        manifest_bytes = archive.read(manifest_names[0])
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        eval_entries = manifest.get("evaluated", [])
        if not eval_entries:
            return {"status": "no_completed_vintages_in_artifact", "run_id": run["id"]}
        archived_records = []
        for item in eval_entries:
            eval_member = item.get("evaluation_file", "").split("/")[-1]
            actual_member = item.get("actual_file", "").split("/")[-1]
            if eval_member not in names or actual_member not in names:
                raise ValueError(f"evaluation artifact missing files for {item.get('vintage_id')}")
            eval_bytes = archive.read(eval_member)
            actual_bytes = archive.read(actual_member)
            evaluation = json.loads(eval_bytes.decode("utf-8"))
            expected_id = make_vintage_id({
                "issued_at_utc": evaluation["issued_at_utc"],
                "asset": evaluation.get("asset"),
                "venue": evaluation.get("venue"),
                "model_version": evaluation.get("model_version"),
            })
            if evaluation.get("vintage_id") != expected_id:
                continue
            if sha256_bytes(actual_bytes) != evaluation.get("actual_data_sha256"):
                raise ValueError(f"actual data hash mismatch for {expected_id}")
            evaluated_at = str(manifest["evaluated_at_utc"])
            date = evaluated_at[:10]
            stamp = evaluated_at.replace(":", "-")
            eval_archive_rel = f"research/living-fractal-market/evaluations/{date}/{stamp}_LFM-completed-vintage-evaluation.artifact.zip"
            eval_json_rel = f"research/living-fractal-market/evaluations/{date}/{expected_id}.json"
            actual_rel = f"research/living-fractal-market/evaluations/{date}/{expected_id}_actual_binance_spot_1h.json"
            manifest_rel = f"research/living-fractal-market/evaluations/{date}/manifest_{stamp}.json"

            _, archive_sha = write_immutable(root, eval_archive_rel, zip_bytes)
            _, eval_sha = write_immutable(root, eval_json_rel, eval_bytes)
            _, actual_sha = write_immutable(root, actual_rel, actual_bytes)
            write_immutable(root, manifest_rel, manifest_bytes)
            ledger_changed = append_evaluation_ledger(
                ledger_path, run, artifact, eval_archive_rel, archive_sha,
                eval_json_rel, eval_sha, actual_rel, actual_sha, evaluation,
            )
            archived_records.append({
                "vintage_id": expected_id,
                "evaluation_archive": eval_archive_rel,
                "evaluation_sha256": eval_sha,
                "actual_data_sha256": actual_sha,
                "ledger_updated": ledger_changed,
            })
    if not archived_records:
        return {"status": "legacy_or_invalid_evaluation_skipped", "run_id": run["id"]}
    return {
        "status": "archived_evaluation",
        "run_id": run["id"],
        "artifact_id": artifact["id"],
        "artifact_sha256": sha256_bytes(zip_bytes),
        "records": archived_records,
    }


def git_commit_and_push(root: Path, branch: str) -> bool:
    def run(*args: str) -> None:
        subprocess.run(args, cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run("git", "add", "research/living-fractal-market/forecasts",
        "research/living-fractal-market/evaluations",
        "research/living-fractal-market/FORECAST_LEDGER.md")
    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if status.returncode == 0:
        return False
    run("git", "commit", "-m", "Archive exact LFM workflow forecasts and evaluations")
    run("git", "fetch", "origin", branch)
    run("git", "rebase", f"origin/{branch}")
    run("git", "push", "origin", f"HEAD:{branch}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--branch", default="research/living-fractal-market")
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required by the branch-scoped archive workflow")

    ledger_path = args.root / "research/living-fractal-market/FORECAST_LEDGER.md"
    if not ledger_path.exists():
        raise FileNotFoundError(ledger_path)

    summary: dict[str, Any] = {
        "archived_forecasts": [],
        "archived_evaluations": [],
        "skipped": [],
        "errors": [],
    }
    forecast_runs = list_workflow_runs(
        args.repo, args.branch, FORECAST_WORKFLOW, args.head_sha, token
    )
    for run in forecast_runs:
        try:
            result = archive_forecast_run(args.root, args.repo, run, token, ledger_path)
            if result["status"] == "archived":
                summary["archived_forecasts"].append(result)
            else:
                summary["skipped"].append(result)
        except Exception as exc:
            summary["errors"].append({
                "workflow": FORECAST_WORKFLOW,
                "run_id": run.get("id"),
                "error_type": type(exc).__name__,
                "error": str(exc),
            })

    evaluation_runs = list_workflow_runs(
        args.repo, args.branch, EVALUATION_WORKFLOW, args.head_sha, token
    )
    for run in evaluation_runs:
        try:
            result = archive_evaluation_run(args.root, args.repo, run, token, ledger_path)
            if result["status"] == "archived_evaluation":
                summary["archived_evaluations"].append(result)
            else:
                summary["skipped"].append(result)
        except Exception as exc:
            summary["errors"].append({
                "workflow": EVALUATION_WORKFLOW,
                "run_id": run.get("id"),
                "error_type": type(exc).__name__,
                "error": str(exc),
            })

    pushed = git_commit_and_push(args.root, args.branch)
    summary["branch_commit_pushed"] = pushed
    summary["finished_at_utc"] = iso_utc_now()
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))
    if summary["errors"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
