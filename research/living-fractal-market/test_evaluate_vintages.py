import gzip
import json
import math
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from archive_workflow_artifacts import source_head_sha_from_marker

from evaluate_vintages import (
    INTERVAL_MS,
    discover_forecast_archives,
    evaluate_vintage,
    parse_utc,
    score_path,
    validate_actual_rows,
    volatility_capped_slow_drift_baseline,
    threshold_event_diagnostic,
    summarize_leaderboard,
)


class EvaluationTests(unittest.TestCase):

    def test_canonical_zip_suppresses_corrupt_gzip_mirror(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            day = root / "2026-11-13"
            day.mkdir()
            gzip_mirror = day / "vintage.json.gz"
            canonical_zip = day / "vintage.artifact.zip"
            gzip_mirror.write_bytes(b"deliberately-corrupt-gzip")
            canonical_zip.write_bytes(b"canonical-workflow-zip")

            selected, duplicates = discover_forecast_archives(root)

            self.assertEqual(selected, [canonical_zip])
            self.assertEqual(len(duplicates), 1)
            self.assertEqual(duplicates[0]["archive"], str(gzip_mirror))
            self.assertEqual(duplicates[0]["canonical_archive"], str(canonical_zip))

    def test_archive_marker_parses_source_head_sha(self):
        source_sha = "a" * 40
        marker = f"# archive marker\nSource head SHA: {source_sha}\n"
        self.assertEqual(source_head_sha_from_marker(marker), source_sha)

    def test_archive_marker_rejects_missing_or_malformed_source_sha(self):
        self.assertIsNone(source_head_sha_from_marker("Source head SHA: not-a-sha\n"))
        self.assertIsNone(source_head_sha_from_marker("no source sha here\n"))

    def test_perfect_path_has_zero_primary_loss_and_full_direction_accuracy(self):
        reference = 100.0
        actual = [101.0 + i for i in range(24)]
        points = []
        previous = reference
        for value in actual:
            points.append({
                "point_usdt": value,
                "p90_low_usdt": value * 0.9,
                "p90_high_usdt": value * 1.1,
            })
            previous = value
        result = score_path(points, actual, reference, 0.01)
        self.assertAlmostEqual(result["normalized_log_price_mae"], 0.0)
        self.assertAlmostEqual(result["directional_accuracy_vs_issue_reference"], 1.0)
        self.assertAlmostEqual(result["directional_accuracy_hour_to_hour"], 1.0)
        self.assertAlmostEqual(result["p90_empirical_coverage"], 1.0)

    def test_normalized_loss_uses_frozen_sigma(self):
        reference = 100.0
        actual = [100.0] * 24
        points = [{"point_usdt": 100.0 * math.exp(0.01)} for _ in range(24)]
        result = score_path(points, actual, reference, 0.02)
        self.assertAlmostEqual(result["log_price_mae"], 0.01)
        self.assertAlmostEqual(result["normalized_log_price_mae"], 0.5)

    def test_volatility_capped_drift_respects_sigma_cap(self):
        points = volatility_capped_slow_drift_baseline(100.0, 0.01, 0.2)
        expected_drift = 0.0025
        self.assertEqual(len(points), 24)
        self.assertAlmostEqual(points[0]["point_usdt"], 100.0 * math.exp(expected_drift))
        self.assertLess(points[0]["p90_low_usdt"], points[0]["point_usdt"])
        self.assertGreater(points[0]["p90_high_usdt"], points[0]["point_usdt"])

    def test_volatility_capped_drift_handles_negative_signal(self):
        points = volatility_capped_slow_drift_baseline(100.0, 0.01, -0.2)
        self.assertAlmostEqual(points[0]["point_usdt"], 100.0 * math.exp(-0.0025))

    def test_actual_validator_rejects_missing_target_bar(self):
        open_ms = int(datetime(2026, 11, 12, 9, tzinfo=timezone.utc).timestamp() * 1000)
        row = [open_ms, "100", "102", "99", "101", "10", open_ms + INTERVAL_MS - 1]
        with self.assertRaisesRegex(ValueError, "missing 1 target"):
            validate_actual_rows([row], [open_ms, open_ms + INTERVAL_MS], open_ms + 2 * INTERVAL_MS)

    def test_actual_validator_rejects_unclosed_bar(self):
        open_ms = int(datetime(2026, 11, 12, 9, tzinfo=timezone.utc).timestamp() * 1000)
        row = [open_ms, "100", "102", "99", "101", "10", open_ms + INTERVAL_MS - 1]
        with self.assertRaisesRegex(ValueError, "not closed"):
            validate_actual_rows([row], [open_ms], open_ms + INTERVAL_MS - 1)

    def test_utc_parser_requires_offset(self):
        self.assertEqual(parse_utc("2026-11-12T09:00:00Z").tzinfo, timezone.utc)
        with self.assertRaisesRegex(ValueError, "lacks UTC offset"):
            parse_utc("2026-11-12T09:00:00")

    def test_threshold_event_is_terminal_not_first_passage(self):
        forecast = {
            "reference_price_usdt": 73660.61,
            "downside_risk": {
                "level_usdt": 70000.0,
                "heuristic_probability_below_level_24h": 0.0,
            },
        }
        result = threshold_event_diagnostic(forecast, [73400.0] * 23 + [68717.47])
        self.assertTrue(result["observed_terminal_outcome"])
        self.assertFalse(result["reference_already_below_level"])
        self.assertFalse(result["is_first_passage_probability"])
        self.assertAlmostEqual(result["brier_diagnostic_only"], 1.0)


    @staticmethod
    def _write_test_forecast_archive(root: Path):
        target_start = datetime(2026, 11, 20, 8, 0, tzinfo=timezone.utc)
        points = []
        for horizon in range(24):
            target = target_start + timedelta(hours=horizon)
            points.append({
                "target_utc": target.isoformat().replace("+00:00", "Z"),
                "point_usdt": 100.0,
                "p90_low_usdt": 90.0,
                "p90_high_usdt": 110.0,
            })
        forecast = {
            "schema": "lfm.forecast.5m.v2",
            "issued_at_utc": "2026-11-20T07:57:36.065378Z",
            "data_cutoff_utc": "2026-11-20T07:54:59.999Z",
            "asset": "BTC/USDT",
            "venue": "Binance Spot",
            "quote_currency": "USDT",
            "model_version": "LFM-5m-Downside-Aware-Council-0.4",
            "reference_price_usdt": 100.0,
            "diagnostics": {"hourly_sigma_estimate": 0.01, "slow_12h_log_return_per_hour": 0.0},
            "interval_calibration": {"calibrated": False},
            "warning": "test fixture; intervals uncalibrated",
            "models": [{"model": "RandomWalk", "points": points}],
        }
        archive_path = root / "forecast.json.gz"
        archive_path.write_bytes(gzip.compress(json.dumps(forecast, separators=(",", ":")).encode("utf-8")))
        final_close = target_start + timedelta(hours=24) - timedelta(milliseconds=1)
        return archive_path, final_close

    def test_evaluation_stays_pending_until_final_target_close(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive_path, final_close = self._write_test_forecast_archive(root)
            now = final_close - timedelta(milliseconds=1)
            with patch("evaluate_vintages.fetch_hourly_rows", side_effect=AssertionError("must not fetch")) as fetch:
                result = evaluate_vintage(archive_path, root, root / "evaluations", root / "output", now)
            self.assertEqual(result["status"], "pending")
            self.assertEqual(result["final_target_close_utc"], "2026-11-21T07:59:59.999Z")
            fetch.assert_not_called()

    def test_evaluation_stays_pending_at_inclusive_final_close_timestamp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive_path, final_close = self._write_test_forecast_archive(root)
            now = final_close
            with patch(
                "evaluate_vintages.fetch_hourly_rows",
                side_effect=AssertionError("must wait until the inclusive close timestamp has passed"),
            ) as fetch:
                result = evaluate_vintage(
                    archive_path, root, root / "evaluations", root / "output", now
                )
            self.assertEqual(result["status"], "pending")
            self.assertEqual(result["final_target_close_utc"], "2026-11-21T07:59:59.999Z")
            fetch.assert_not_called()

    def test_evaluation_fetches_actuals_only_after_final_target_close(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive_path, final_close = self._write_test_forecast_archive(root)
            target_start = datetime(2026, 11, 20, 8, 0, tzinfo=timezone.utc)
            rows = []
            for horizon in range(24):
                open_ms = int((target_start + timedelta(hours=horizon)).timestamp() * 1000)
                rows.append([open_ms, "100", "101", "99", "100", "1", open_ms + INTERVAL_MS - 1])
            now = final_close + timedelta(milliseconds=1)
            with patch("evaluate_vintages.fetch_hourly_rows", return_value=(json.dumps(rows).encode("utf-8"), "https://example.invalid/test")) as fetch:
                result = evaluate_vintage(archive_path, root, root / "evaluations", root / "output", now)
            self.assertEqual(result["status"], "evaluated")
            fetch.assert_called_once()
            self.assertTrue(Path(result["evaluation_file"]).exists())
            self.assertTrue(Path(result["actual_file"]).exists())

    @staticmethod
    def _write_evaluation(
        root: Path,
        vintage_id: str,
        target_start: datetime,
        random_walk: float,
        volatility_slow_drift: float,
        model_losses: dict[str, float],
    ) -> None:
        grid = [target_start + timedelta(hours=hour) for hour in range(24)]
        final_close = grid[-1] + timedelta(hours=1) - timedelta(milliseconds=1)
        record = {
            "schema": "lfm.evaluation.hourly.v1",
            "evaluation_protocol": "LFM-Tournament-1.1",
            "status": "evaluated",
            "vintage_id": vintage_id,
            "issued_at_utc": (target_start - timedelta(minutes=5)).isoformat().replace("+00:00", "Z"),
            "asset": "BTC/USDT",
            "venue": "Binance Spot",
            "quote_currency": "USDT",
            "target_interval": "1h",
            "target_grid_open_utc": [
                value.isoformat(timespec="milliseconds").replace("+00:00", "Z")
                for value in grid
            ],
            "target_grid_final_close_utc": final_close.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "baseline_results": {
                "RandomWalkLastPrice": {"normalized_log_price_mae": random_walk},
                "VolatilityCappedSlowDrift": {"normalized_log_price_mae": volatility_slow_drift},
            },
            "model_results_ranked_by_primary_loss": [
                {"model": name, "normalized_log_price_mae": loss}
                for name, loss in model_losses.items()
            ],
            "intervals_calibrated": False,
            "virtual_points_awarded": 0,
        }
        root.mkdir(parents=True, exist_ok=True)
        (root / f"evaluation_{vintage_id}.json").write_text(
            json.dumps(record), encoding="utf-8"
        )

    def test_leaderboard_excludes_overlapping_vintages_and_bootstrap_is_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "evaluations"
            first_start = datetime(2026, 11, 20, 8, tzinfo=timezone.utc)
            overlapping_start = datetime(2026, 11, 20, 9, tzinfo=timezone.utc)
            next_start = datetime(2026, 11, 21, 8, tzinfo=timezone.utc)
            self._write_evaluation(
                root, "vintage-a", first_start, 1.0, 2.0,
                {"MeanReversion5m": 0.9, "Momentum5m": 1.2},
            )
            self._write_evaluation(
                root, "vintage-b-overlap", overlapping_start, 1.2, 1.1,
                {"MeanReversion5m": 1.3, "Momentum5m": 1.0},
            )
            self._write_evaluation(
                root, "vintage-c", next_start, 1.0, 1.5,
                {"MeanReversion5m": 0.8, "Momentum5m": 1.1},
            )
            now = datetime(2026, 11, 23, 9, tzinfo=timezone.utc)
            first = summarize_leaderboard([root], now, bootstrap_samples=250)
            second = summarize_leaderboard([root], now, bootstrap_samples=250)

            self.assertEqual(first["completed_unique_vintages"], 3)
            self.assertEqual(first["non_overlapping_vintages"], 2)
            self.assertEqual(first["overlapping_vintages_excluded"], 1)
            self.assertEqual(
                [item["vintage_id"] for item in first["selected_vintages"]],
                ["vintage-a", "vintage-c"],
            )
            self.assertEqual(first["strongest_simple_baseline_by_mean"], "RandomWalkLastPrice")
            self.assertAlmostEqual(
                first["baseline_mean_normalized_log_price_mae"]["RandomWalkLastPrice"], 1.0
            )
            self.assertAlmostEqual(
                first["baseline_mean_normalized_log_price_mae"]["VolatilityCappedSlowDrift"], 1.75
            )
            ranked = {item["model"]: item for item in first["models_ranked_by_mean_loss"]}
            self.assertAlmostEqual(ranked["MeanReversion5m"]["mean_normalized_log_price_mae"], 0.85)
            self.assertAlmostEqual(ranked["Momentum5m"]["mean_normalized_log_price_mae"], 1.15)
            interval = ranked["MeanReversion5m"]["paired_bootstrap_95pct_ci_difference_vs_random_walk"]
            self.assertEqual(len(interval), 2)
            self.assertLessEqual(interval[0], interval[1])
            self.assertEqual(first, second)
            self.assertEqual(first["calibrated_selected_vintages"], 0)
            self.assertEqual(first["virtual_points_awarded_selected_vintages"], 0)

    def test_leaderboard_empty_history_is_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "empty"
            summary = summarize_leaderboard(
                [root], datetime(2026, 11, 23, 9, tzinfo=timezone.utc), bootstrap_samples=10
            )
            self.assertEqual(summary["completed_unique_vintages"], 0)
            self.assertEqual(summary["non_overlapping_vintages"], 0)
            self.assertEqual(summary["models_ranked_by_mean_loss"], [])
            self.assertEqual(summary["baseline_mean_normalized_log_price_mae"], {})

    def test_leaderboard_reads_archived_vintage_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "evaluations"
            target_start = datetime(2026, 11, 20, 8, tzinfo=timezone.utc)
            self._write_evaluation(
                root, "archived-vintage", target_start, 1.1, 1.0,
                {"MeanReversion5m": 0.9},
            )
            generated = root / "evaluation_archived-vintage.json"
            archived = root / "lfm5m-archived-vintage.json"
            generated.rename(archived)
            (root / "actual_hourly_archived-vintage.json").write_text("[]", encoding="utf-8")
            (root / "evaluation_manifest.json").write_text(
                json.dumps({"schema": "lfm.evaluation.manifest.v1", "evaluated": []}),
                encoding="utf-8",
            )

            summary = summarize_leaderboard(
                [root], datetime(2026, 11, 22, 9, tzinfo=timezone.utc),
                bootstrap_samples=50,
            )
            self.assertEqual(summary["completed_unique_vintages"], 1)
            self.assertEqual(summary["non_overlapping_vintages"], 1)
            self.assertEqual(
                [item["vintage_id"] for item in summary["selected_vintages"]],
                ["archived-vintage"],
            )
            self.assertEqual(summary["invalid_evaluation_files"], [])


if __name__ == "__main__":
    unittest.main()
