import math
import unittest
from datetime import datetime, timezone

from evaluate_vintages import (
    INTERVAL_MS,
    parse_utc,
    score_path,
    validate_actual_rows,
    volatility_capped_slow_drift_baseline,
)


class EvaluationTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
