"""Deterministic memory-lifecycle benchmark; no LLM calls or external services.

Run from the repository root:
    python benchmarks/temporal_memory_interventions.py

The legacy baseline intentionally reproduces the pre-projection behavior:
serializing the entire persisted profile. It is a comparison fixture, not a
second production implementation.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ambivikhry.memory import JsonMemory  # noqa: E402


def _contexts(profile: dict[str, Any]) -> tuple[str, str]:
    legacy_baseline = json.dumps(profile, ensure_ascii=False, indent=2)
    candidate = JsonMemory.profile_context(profile)
    return legacy_baseline, candidate


def _case(
    name: str,
    profile: dict[str, Any],
    *,
    stale_markers: list[str],
    current_markers: list[str],
    reconfirmed: str | None = None,
) -> dict[str, Any]:
    baseline, candidate = _contexts(profile)
    return {
        "name": name,
        "stale_markers": stale_markers,
        "current_markers": current_markers,
        "baseline_stale_hits": sum(marker in baseline for marker in stale_markers),
        "candidate_stale_hits": sum(marker in candidate for marker in stale_markers),
        "candidate_current_hits": sum(marker in candidate for marker in current_markers),
        "candidate_current_expected": len(current_markers),
        "reconfirmed": reconfirmed,
        "reconfirmation_visible": bool(reconfirmed and reconfirmed in candidate),
    }


def build_cases(directory: str | Path) -> list[dict[str, Any]]:
    memory = JsonMemory(directory)
    cases: list[dict[str, Any]] = []

    # Intervention 1: dismiss a value, then replay the old inferred hint.
    memory.personalize(
        "I prefer short answers and concrete examples.",
        {"preferences": ["short answers", "concrete examples"]},
    )
    memory.revise_profile_item("preferences", "short answers", "dismiss")
    memory.personalize("A later task", {"preferences": ["short answers"]})
    cases.append(_case(
        "dismiss_then_replay",
        memory.load_profile(),
        stale_markers=["short answers"],
        current_markers=["concrete examples"],
    ))

    # Intervention 2: correct a value, then replay the superseded hint.
    memory = JsonMemory(Path(directory) / "correction")
    memory.personalize("I prefer concise replies.", {"preferences": ["concise replies"]})
    memory.revise_profile_item(
        "preferences", "concise replies", "correct", replacement="detailed replies"
    )
    memory.personalize("Another task", {"preferences": ["concise replies"]})
    cases.append(_case(
        "correct_then_replay",
        memory.load_profile(),
        stale_markers=["concise replies"],
        current_markers=["detailed replies"],
    ))

    # Intervention 3: an explicit user action may legitimately re-confirm a value.
    memory = JsonMemory(Path(directory) / "explicit_reconfirm")
    memory.personalize("I prefer concise replies.", {"preferences": ["concise replies"]})
    memory.revise_profile_item("preferences", "concise replies", "dismiss")
    memory.revise_profile_item("preferences", "concise replies", "confirm")
    cases.append(_case(
        "explicit_reconfirm",
        memory.load_profile(),
        stale_markers=[],
        current_markers=["concise replies"],
        reconfirmed="concise replies",
    ))

    # Intervention 4: malformed legacy list entries must not be prompt-visible.
    malformed = {
        "version": 1,
        "status": "MALFORMED_STATUS_SENTINEL",
        "preferences": [
            {"private_payload_marker": "MALFORMED_SENTINEL"},
            "current legacy preference",
        ],
        "observations": [{"text": "MALFORMED_OBSERVATION_SENTINEL"}],
        "profile_history": [{"value": "MALFORMED_HISTORY_SENTINEL"}],
    }
    cases.append(_case(
        "malformed_legacy_payload",
        malformed,
        stale_markers=[
            "MALFORMED_SENTINEL",
            "MALFORMED_OBSERVATION_SENTINEL",
            "MALFORMED_HISTORY_SENTINEL",
            "MALFORMED_STATUS_SENTINEL",
        ],
        current_markers=["current legacy preference"],
    ))
    return cases


def run_benchmark() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ambivikhry-temporal-bench-") as temp_dir:
        cases = build_cases(temp_dir)

    stale_checks = sum(len(case["stale_markers"]) for case in cases)
    baseline_stale_hits = sum(case["baseline_stale_hits"] for case in cases)
    candidate_stale_hits = sum(case["candidate_stale_hits"] for case in cases)
    current_checks = sum(case["candidate_current_expected"] for case in cases)
    current_hits = sum(case["candidate_current_hits"] for case in cases)
    reconfirm_cases = [case for case in cases if case["reconfirmed"] is not None]
    reconfirm_hits = sum(case["reconfirmation_visible"] for case in reconfirm_cases)

    result = {
        "benchmark": "temporal-memory-interventions-v1",
        "scope": "deterministic storage/projection behavior only; no LLM quality or secure-erasure claim",
        "cases": cases,
        "metrics": {
            "stale_marker_checks": stale_checks,
            "legacy_baseline_stale_exposure_rate": (
                baseline_stale_hits / stale_checks if stale_checks else 0.0
            ),
            "candidate_stale_exposure_rate": (
                candidate_stale_hits / stale_checks if stale_checks else 0.0
            ),
            "current_value_retention_rate": current_hits / current_checks if current_checks else 1.0,
            "explicit_reconfirmation_rate": (
                reconfirm_hits / len(reconfirm_cases) if reconfirm_cases else 1.0
            ),
        },
    }
    result["pass"] = (
        result["metrics"]["candidate_stale_exposure_rate"] == 0.0
        and result["metrics"]["current_value_retention_rate"] == 1.0
        and result["metrics"]["explicit_reconfirmation_rate"] == 1.0
        and result["metrics"]["legacy_baseline_stale_exposure_rate"] > 0.0
    )
    return result


def main() -> int:
    result = run_benchmark()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
