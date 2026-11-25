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
ARCHIVE_MARKER_PATH = "research/living-fractal-market/ARCHIVE_RUN_TRIGGER.md"
DAILY_TRIGGER_PATH = "research/living-fractal-market/DAILY_RUN_TRIGGER.md"
FORECAST_WORKFLOW = "lfm-5m.yml"
EVALUATION_WORKFLOW = "lfm-evaluate.yml"
EVALUATION_TRIGGER_PATHS = {
    DAILY_TRIGGER_PATH,
    "research/living-fractal-market/evaluate_vintages.py",
    "research/living-fractal-market/test_evaluate_vintages.py",
    ".github/workflows/lfm-evaluate.yml",
}
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


def validate_forecast_schema(forecast: dict[str, Any], run: dict[str, Any]) -> None:
    """Validate legacy v1 and provenance-complete v2 forecast payloads."""
    schema = forecast.get("schema")
    if schema == "lfm.forecast.5m.v1":
        return
    if schema != "lfm.forecast.5m.v2":
        raise ValueError(f"unexpected forecast schema in run {run.get('id')}")
    required = ("vintage_id", "model_commit", "training_cutoff_utc", "input_interval", "retrieved_at_utc", "issued_at_utc", "data_cutoff_utc")
    missing = [field for field in required if not forecast.get(field)]
    if missing:
        raise ValueError(f"v2 forecast missing provenance fields: {missing}")
    if forecast["input_interval"] != "5m":
        raise ValueError("v2 forecast input_interval must be 5m")
    if forecast["model_commit"] != run.get("head_sha"):
        raise ValueError("forecast model_commit does not match workflow source commit")
    if forecast["training_cutoff_utc"] != forecast["data_cutoff_utc"]:
        raise ValueError("training cutoff must match the last observed data cutoff for this rolling-feature model")
    if not str(forecast["vintage_id"]).startswith("lfm5m-"):
        raise ValueError("v2 forecast vintage_id has an invalid prefix")

    def parse_timestamp(value: str) -> datetime:
        text = str(value)
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            raise ValueError("v2 provenance timestamps must include a UTC offset")
        return parsed.astimezone(timezone.utc)

    issued = parse_timestamp(forecast["issued_at_utc"])
    retrieved = parse_timestamp(forecast["retrieved_at_utc"])
    cutoff = parse_timestamp(forecast["data_cutoff_utc"])
    if not cutoff <= retrieved <= issued:
        raise ValueError("v2 timestamps must satisfy data cutoff <= retrieval <= issue time")


def validate_raw_input_snapshot(forecast: dict[str, Any], raw_bytes: bytes) -> dict[str, Any]:
    """Verify the exact archived Binance 5m response against forecast provenance."""
    provenance = forecast.get("data_provenance")
    if not isinstance(provenance, dict):
        raise ValueError("forecast is missing data_provenance for its raw 5m snapshot")
    if provenance.get("raw_response_file") != "forecast_5m_raw_klines.json":
        raise ValueError("unexpected raw 5m snapshot filename")
    if not isinstance(raw_bytes, bytes) or not raw_bytes:
        raise ValueError("raw 5m snapshot is empty")
    digest = sha256_bytes(raw_bytes)
    if digest != provenance.get("raw_response_sha256"):
        raise ValueError("raw 5m snapshot SHA-256 does not match forecast metadata")
    if len(raw_bytes) != int(provenance.get("raw_response_bytes", -1)):
        raise ValueError("raw 5m snapshot byte length does not match forecast metadata")

    request_url = str(provenance.get("request_url") or "")
    parsed_url = urllib.parse.urlparse(request_url)
    query = urllib.parse.parse_qs(parsed_url.query)
    allowed_hosts = {"data-api.binance.vision", "api.binance.com", "api1.binance.com", "api-gcp.binance.com"}
    if parsed_url.scheme != "https" or parsed_url.hostname not in allowed_hosts or parsed_url.path != "/api/v3/klines":
        raise ValueError("raw 5m snapshot request URL is not an approved Binance public kline endpoint")
    if query.get("symbol") != ["BTCUSDT"] or query.get("interval") != ["5m"]:
        raise ValueError("raw 5m snapshot request URL must identify BTCUSDT at 5m")

    try:
        rows = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("raw 5m snapshot is not valid UTF-8 JSON") from exc
    if not isinstance(rows, list) or not rows:
        raise ValueError("raw 5m snapshot must be a non-empty kline array")

    def parse_time(value: str) -> datetime:
        text = str(value)
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            raise ValueError("forecast timestamps must include a UTC offset")
        return parsed.astimezone(timezone.utc)

    issued_ms = int(parse_time(forecast["issued_at_utc"]).timestamp() * 1000)
    cutoff_ms = int(parse_time(forecast["data_cutoff_utc"]).timestamp() * 1000)
    closed = []
    for row in rows:
        if not isinstance(row, list) or len(row) < 7:
            raise ValueError("raw 5m kline row is malformed")
        open_ms, close_ms = int(row[0]), int(row[6])
        if close_ms != open_ms + 300_000 - 1:
            raise ValueError("raw 5m kline close timestamp is misaligned")
        if close_ms < issued_ms:
            closed.append((open_ms, close_ms))
    if len(closed) != int(forecast.get("closed_candles", -1)):
        raise ValueError("raw 5m snapshot closed-candle count does not match forecast")
    if not closed:
        raise ValueError("raw 5m snapshot contains no closed candles at issue time")
    if any(b[0] - a[0] != 300_000 for a, b in zip(closed, closed[1:])):
        raise ValueError("raw 5m snapshot has duplicate or missing closed candles")
    last_open, last_close = closed[-1]
    if last_close != cutoff_ms:
        raise ValueError("raw 5m snapshot last closed candle does not match data_cutoff_utc")
    if last_open != int(provenance.get("last_closed_candle_open_ms", -1)):
        raise ValueError("raw 5m snapshot last open timestamp does not match forecast metadata")
    if last_close != int(provenance.get("last_closed_candle_close_ms", -1)):
        raise ValueError("raw 5m snapshot last close timestamp does not match forecast metadata")
    return {"sha256": digest, "bytes": len(raw_bytes), "closed_candles": len(closed),
            "last_closed_open_ms": last_open, "last_closed_close_ms": last_close,
            "request_url": request_url}


def source_head_sha_from_marker(marker_text: str) -> str | None:
    """Return the exact source commit named by an archive marker, if valid."""
    match = re.search(
        r"^Source head SHA:\s*([0-9a-f]{40})\s*$",
        marker_text,
        re.MULTILINE,
    )
    return match.group(1) if match else None


def should_wait_for_evaluation(changed_paths: set[str]) -> bool:
    """Wait for the sibling evaluator after any push that triggers it."""
    return bool(changed_paths.intersection(EVALUATION_TRIGGER_PATHS))


def select_source_commit(
    default_sha: str,
    marker_text: str,
    changed_paths: set[str],
) -> tuple[str, bool]:
    """Select the source workflow commit without letting a stale archive marker win.

    An archive-marker-only push explicitly points back to the forecast commit.
    Daily-marker and forecast-code pushes wait for sibling forecast workflows
    to appear and finish. Archive-only and documentation pushes do not wait.
    """
    if ARCHIVE_MARKER_PATH in changed_paths:
        parsed = source_head_sha_from_marker(marker_text)
        if parsed is None:
            raise ValueError(
                "ARCHIVE_RUN_TRIGGER.md must contain a valid "
                "'Source head SHA: <40-hex>' line"
            )
        return parsed, False
    forecast_paths = {
        "research/living-fractal-market/forecast_btc_5m.py",
        "research/living-fractal-market/test_forecast_btc_5m.py",
        ".github/workflows/lfm-5m.yml",
    }
    wait_for_forecast = DAILY_TRIGGER_PATH in changed_paths or bool(changed_paths.intersection(forecast_paths))
    return default_sha, wait_for_forecast


def changed_paths_at_head(root: Path) -> set[str]:
    """Return paths changed by the exact checked-out push commit."""
    completed = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "could not identify trigger paths for checked-out commit: "
            + (completed.stdout or "")[-2000:]
        )
    return {line.strip() for line in (completed.stdout or "").splitlines() if line.strip()}


def request_bytes(url: str, token: str, accept: str = "application/vnd.github+json") -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"token {token.strip()}",
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
    wait_for_appearance: bool = False,
) -> list[dict[str, Any]]:
    query = urllib.parse.urlencode({"branch": branch, "per_page": 100})
    url = f"{API}/repos/{repo}/actions/workflows/{workflow_file}/runs?{query}"
    deadline = time.time() + 300
    while True:
        payload = api_json(url, token)
        runs = [
            run for run in payload.get("workflow_runs", [])
            if run.get("head_branch") == branch
        ]
        exact = [run for run in runs if run.get("head_sha") == head_sha]
        if exact:
            current = [
                api_json(f"{API}/repos/{repo}/actions/runs/{run['id']}", token)
                for run in exact
            ]
            if all(run.get("status") == "completed" for run in current):
                return [
                    run for run in current
                    if run.get("conclusion") == "success"
                ]
        elif not wait_for_appearance:
            return []

        if time.time() >= deadline:
            return []
        # A push starts sibling forecast/evaluation workflows concurrently.
        # Wait for their run records to appear before concluding there is
        # nothing to archive; once present, also wait for completion.
        time.sleep(5)


def find_artifact(repo: str, run_id: int, artifact_name: str, token: str) -> dict[str, Any] | None:
    payload = api_json(
        f"{API}/repos/{repo}/actions/runs/{run_id}/artifacts?per_page=100",
        token,
    )
    for artifact in payload.get("artifacts", []):
        if artifact.get("name") == artifact_name and not artifact.get("expired", False):
            return artifact
    return None


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Expose GitHub's artifact redirect so auth headers never reach blob storage."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _download_artifact_zip(url: str, token: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"token {token.strip()}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Ambivikhry-LFM-Artifact-Archiver/1.0",
        },
    )
    opener = urllib.request.build_opener(_NoRedirectHandler())
    try:
        with opener.open(request, timeout=60) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        if exc.code not in {301, 302, 303, 307, 308}:
            raise
        location = exc.headers.get("Location")
        if not location:
            raise RuntimeError("GitHub artifact redirect did not include a Location header") from exc
        signed_url = urllib.parse.urljoin(url, location)
        # GitHub's temporary object-storage URL is already signed. Never forward
        # the repository token or GitHub API headers to that different host.
        signed_request = urllib.request.Request(
            signed_url,
            headers={"User-Agent": "Ambivikhry-LFM-Artifact-Archiver/1.0"},
        )
        with urllib.request.urlopen(signed_request, timeout=60) as response:
            return response.read()


def download_artifact(repo: str, artifact: dict[str, Any], token: str) -> bytes:
    data = _download_artifact_zip(
        f"{API}/repos/{repo}/actions/artifacts/{artifact['id']}/zip",
        token,
    )
    expected = str(artifact.get("digest", "")).removeprefix("sha256:")
    actual = sha256_bytes(data)
    if expected and expected != actual:
        raise ValueError(
            f"artifact digest mismatch for {artifact.get('name')} id={artifact.get('id')}: "
            f"expected {expected}, got {actual}"
        )
    return data


def immutable_path_for_payload(
    root: Path,
    relative_path: str,
    data: bytes,
    discriminator: str,
) -> str:
    """Keep an existing immutable record; suffix conflicting duplicate payloads."""
    path = root / relative_path
    if not path.exists() or sha256_bytes(path.read_bytes()) == sha256_bytes(data):
        return relative_path
    candidate = Path(relative_path)
    return str(candidate.with_name(
        f"{candidate.stem}.artifact-{slug(discriminator)}{candidate.suffix}"
    ))


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
        f"- Schema / vintage ID: {forecast.get('schema')} / {forecast.get('vintage_id')}\n"
        f"- Input interval / retrieved UTC: {forecast.get('input_interval', '5m')} / {forecast.get('retrieved_at_utc')}\n"
        f"- Model commit / training cutoff UTC: {forecast.get('model_commit', run.get('head_sha'))} / {forecast.get('training_cutoff_utc', forecast.get('data_cutoff_utc'))}\n"
        f"- Closed input candles: {forecast.get('closed_candles')} at 5m; hourly targets: 24\n"
    )
    provenance = forecast.get("data_provenance") or {}
    if provenance:
        entry += (
            f"- Exact raw 5m response: {json_path.replace('.json', '_raw_klines.json')}\n"
            f"- Raw response SHA-256 / bytes: {provenance.get('raw_response_sha256')} / {provenance.get('raw_response_bytes')}\n"
            f"- Raw request URL: {provenance.get('request_url')}\n"
            f"- Last closed input candle open / close ms: {provenance.get('last_closed_candle_open_ms')} / {provenance.get('last_closed_candle_close_ms')}\n"
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
        members = archive.namelist()
        names = [name for name in members if name.endswith("forecast_5m.json")]
        raw_names = [name for name in members if name.endswith("forecast_5m_raw_klines.json")]
        if len(names) != 1 or len(raw_names) != 1:
            raise ValueError(f"run {run['id']} artifact must contain one forecast_5m.json and one raw 5m snapshot")
        forecast_bytes = archive.read(names[0])
        raw_bytes = archive.read(raw_names[0])
    forecast = json.loads(forecast_bytes.decode("utf-8"))
    validate_forecast_schema(forecast, run)
    raw_provenance = validate_raw_input_snapshot(forecast, raw_bytes)
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

    raw_rel = json_rel.replace(".json", "_raw_klines.json")
    zip_created, zip_sha = write_immutable(root, archive_rel, zip_bytes)
    json_created, json_sha = write_immutable(root, json_rel, forecast_bytes)
    raw_created, raw_sha = write_immutable(root, raw_rel, raw_bytes)
    ledger_changed = append_forecast_ledger(
        ledger_path, run, artifact, archive_rel, zip_sha, json_rel, json_sha, forecast
    )
    return {
        "status": "archived" if zip_created or json_created or raw_created or ledger_changed else "already_archived",
        "run_id": run["id"],
        "artifact_id": artifact["id"],
        "archive": archive_rel,
        "archive_sha256": zip_sha,
        "forecast_json": json_rel,
        "forecast_json_sha256": json_sha,
        "raw_input_snapshot": raw_rel,
        "raw_input_sha256": raw_sha,
        "raw_input_provenance": raw_provenance,
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

            # A later evaluation run may repeat the same vintage with a different
            # evaluated_at timestamp. Preserve that exact payload under an
            # artifact-specific path rather than overwriting the first record.
            eval_json_rel = immutable_path_for_payload(
                root, eval_json_rel, eval_bytes, str(artifact["id"])
            )
            actual_rel = immutable_path_for_payload(
                root, actual_rel, actual_bytes, str(artifact["id"])
            )
            manifest_rel = immutable_path_for_payload(
                root, manifest_rel, manifest_bytes, str(artifact["id"])
            )

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
                "evaluation_json": eval_json_rel,
                "evaluation_sha256": eval_sha,
                "actual_data": actual_rel,
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
    def run(*args: str) -> str:
        completed = subprocess.run(
            args, cwd=root, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True,
        )
        if completed.returncode != 0:
            detail = (completed.stdout or "")[-6000:]
            raise RuntimeError(
                f"command failed ({completed.returncode}): {' '.join(args)}\n{detail}"
            )
        return completed.stdout or ""

    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    candidates = (
        "research/living-fractal-market/forecasts",
        "research/living-fractal-market/evaluations",
        "research/living-fractal-market/FORECAST_LEDGER.md",
    )
    existing_paths = [path for path in candidates if (root / path).exists()]
    if not existing_paths:
        return False
    # Empty directories are not tracked by Git. Add only paths that exist so a
    # run with no evaluation records can still archive its forecast artifact.
    run("git", "add", "-A", "--", *existing_paths)
    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
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

    changed_paths = changed_paths_at_head(args.root)
    archive_marker = args.root / ARCHIVE_MARKER_PATH
    marker_text = archive_marker.read_text(encoding="utf-8") if archive_marker.exists() else ""
    source_head_sha, wait_for_runs = select_source_commit(
        args.head_sha, marker_text, changed_paths
    )

    wait_for_evaluation = should_wait_for_evaluation(changed_paths)
    summary: dict[str, Any] = {
        "source_head_sha": source_head_sha,
        "trigger_paths": sorted(changed_paths),
        "waited_for_workflows": wait_for_runs,
        "waited_for_evaluation_workflow": wait_for_evaluation,
        "archived_forecasts": [],
        "archived_evaluations": [],
        "skipped": [],
        "errors": [],
    }
    forecast_runs = list_workflow_runs(
        args.repo, args.branch, FORECAST_WORKFLOW, source_head_sha, token,
        wait_for_appearance=wait_for_runs,
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
        args.repo, args.branch, EVALUATION_WORKFLOW, source_head_sha, token,
        wait_for_appearance=wait_for_evaluation,
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
