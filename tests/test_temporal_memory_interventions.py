import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_temporal_memory_intervention_benchmark_passes_and_exposes_baseline_gap():
    result = subprocess.run(
        [sys.executable, str(ROOT / "benchmarks" / "temporal_memory_interventions.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["pass"] is True
    assert report["metrics"]["stale_marker_checks"] == 5
    assert report["metrics"]["legacy_baseline_stale_exposure_rate"] == 1.0
    assert report["metrics"]["candidate_stale_exposure_rate"] == 0.0
    assert report["metrics"]["current_value_retention_rate"] == 1.0
    assert report["metrics"]["explicit_reconfirmation_rate"] == 1.0


def test_benchmark_includes_all_required_temporal_interventions():
    result = subprocess.run(
        [sys.executable, str(ROOT / "benchmarks" / "temporal_memory_interventions.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    names = {case["name"] for case in report["cases"]}
    assert names == {
        "dismiss_then_replay",
        "correct_then_replay",
        "explicit_reconfirm",
        "malformed_legacy_payload",
    }
