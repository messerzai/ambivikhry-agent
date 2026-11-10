"""Unit tests for forecast_btc_v2.py; run: python -m unittest research.living-fractal-market.test_forecast_btc_v2"""
import datetime as dt
import math
import unittest

from forecast_btc_v2 import forecast

class ForecastV2Tests(unittest.TestCase):
    def synthetic_rows(self, n=240):
        start = dt.datetime(2026, 10, 1, tzinfo=dt.timezone.utc)
        rows = []
        price = 70000.0
        for i in range(n):
            # Deterministic mixed trend and oscillation; no random fixture.
            price *= math.exp(0.00012 + 0.0008*math.sin(i/9.0))
            t = start + dt.timedelta(hours=i)
            rows.append({
                "open_ms": int(t.timestamp()*1000),
                "close_ms": int((t+dt.timedelta(hours=1)).timestamp()*1000)-1,
                "open": price*0.999, "high": price*1.002,
                "low": price*0.998, "close": price, "volume": 100.0
            })
        return rows

    def test_returns_24_ordered_points_and_distinct_timestamps(self):
        issued = dt.datetime(2026, 11, 1, 12, 34, tzinfo=dt.timezone.utc)
        result = forecast(self.synthetic_rows(), issued)
        self.assertEqual(len(result["forecast"]), 24)
        self.assertEqual([x["horizon_h"] for x in result["forecast"]], list(range(1, 25)))
        times = [x["target_utc"] for x in result["forecast"]]
        self.assertEqual(len(set(times)), 24)

    def test_intervals_are_ordered_and_contain_point(self):
        result = forecast(self.synthetic_rows())
        for row in result["forecast"]:
            self.assertLessEqual(row["p90_low_usd"], row["p50_low_usd"])
            self.assertLessEqual(row["p50_low_usd"], row["point_usd"])
            self.assertLessEqual(row["point_usd"], row["p50_high_usd"])
            self.assertLessEqual(row["p50_high_usd"], row["p90_high_usd"])

    def test_forecast_values_are_finite_positive(self):
        result = forecast(self.synthetic_rows())
        for row in result["forecast"]:
            self.assertTrue(math.isfinite(row["point_usd"]))
            self.assertGreater(row["point_usd"], 0)

if __name__ == "__main__":
    unittest.main()
