import datetime as dt
import math
import unittest

from forecast_btc_5m import build_forecast, parse_rows


def make_raw(n=1000, now=None):
    now = now or dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc)
    end = int(now.timestamp() * 1000)
    # Most recent candle closes exactly 5 minutes before now.
    last_open = end - 10 * 60_000
    rows = []
    price = 70000.0
    for i in range(n):
        t = last_open - (n-1-i) * 300_000
        o = price
        c = o * math.exp(0.00003 * math.sin(i/7) + 0.00001)
        h, l = max(o,c)*1.0002, min(o,c)*0.9998
        v = 1.0 + (i % 9) * 0.1
        rows.append([t, str(o), str(h), str(l), str(c), str(v),
                     t+299999, str(v*c), 100, str(v*0.52), str(v*c*0.52), "0"])
        price = c
    return rows


class Forecast5mTests(unittest.TestCase):
    def test_filters_open_candle_and_emits_seven_models_24_points(self):
        now = dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc)
        raw = make_raw(now=now)
        raw.append([int(now.timestamp()*1000), "1", "1", "1", "1", "1",
                    int(now.timestamp()*1000)+299999, "1", 1, "0.5", "0.5", "0"])
        rows = parse_rows(raw, now=now)
        result = build_forecast(rows, issued_at=now)
        self.assertEqual(len(rows), 1000)
        self.assertEqual(len(result["models"]), 7)
        self.assertIn("DownsideStress5m", [m["model"] for m in result["models"]])
        self.assertIn("heuristic_probability_below_level_24h", result["downside_risk"])
        self.assertGreaterEqual(result["downside_risk"]["heuristic_probability_below_level_24h"], 0.0)
        self.assertLessEqual(result["downside_risk"]["heuristic_probability_below_level_24h"], 1.0)
        for model in result["models"]:
            self.assertEqual(len(model["points"]), 24)
            prices = [p["point_usdt"] for p in model["points"]]
            self.assertTrue(all(math.isfinite(x) and x > 0 for x in prices))
            for p in model["points"]:
                self.assertLess(p["p90_low_usdt"], p["point_usdt"])
                self.assertGreater(p["p90_high_usdt"], p["point_usdt"])

    def test_rejects_gap(self):
        raw = make_raw()
        del raw[500]
        with self.assertRaisesRegex(ValueError, "gap"):
            parse_rows(raw, now=dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc))

    def test_rejects_stale_data(self):
        raw = make_raw()
        with self.assertRaisesRegex(ValueError, "stale"):
            parse_rows(raw, now=dt.datetime(2026, 11, 10, 13, 0, tzinfo=dt.timezone.utc))

    def test_rejects_bad_ohlc(self):
        raw = make_raw()
        raw[100][2] = "1"
        with self.assertRaisesRegex(ValueError, "inconsistent"):
            parse_rows(raw, now=dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc))


if __name__ == "__main__":
    unittest.main()
