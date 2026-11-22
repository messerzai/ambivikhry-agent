import datetime as dt
import math
import unittest

from forecast_btc_5m import build_forecast, parse_rows, write_raw_snapshot


def make_raw(n=1000, now=None):
    now = now or dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc)
    end = int(now.timestamp() * 1000)
    # The latest fully closed candle is the interval immediately before now.
    last_open = end - 5 * 60_000
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
        result = build_forecast(rows, issued_at=now, retrieved_at=now-dt.timedelta(seconds=1), model_commit="a"*40)
        self.assertEqual(len(rows), 1000)
        self.assertEqual(result["schema"], "lfm.forecast.5m.v2")
        self.assertEqual(result["model_version"], "LFM-5m-Downside-Aware-Council-0.4")
        self.assertEqual(result["input_interval"], "5m")
        self.assertEqual(result["model_commit"], "a"*40)
        self.assertEqual(result["retrieved_at_utc"], "2026-11-10T11:59:59Z")
        self.assertEqual(result["training_cutoff_utc"], result["data_cutoff_utc"])
        self.assertEqual(result["training_mode"], "deterministic rolling features; no fitted weights; all signals use observations through data_cutoff_utc")
        self.assertTrue(result["vintage_id"].startswith("lfm5m-2026-11-10T12:00:00Z-BTCUSDT-binance-spot-council-0.4"))
        self.assertEqual(len(result["models"]), 7)
        self.assertIn("DownsideStress5m", [m["model"] for m in result["models"]])
        self.assertIn("heuristic_probability_below_level_24h", result["downside_risk"])
        self.assertGreaterEqual(result["downside_risk"]["heuristic_probability_below_level_24h"], 0.0)
        self.assertLessEqual(result["downside_risk"]["heuristic_probability_below_level_24h"], 1.0)
        tail = result["downside_risk"]["severe_tail_scenario"]
        self.assertEqual(tail["shock_pct"], -6.0)
        self.assertEqual(tail["scenario_price_usdt"], round(result["reference_price_usdt"] * 0.94, 2))
        self.assertIsInstance(tail["crosses_level"], bool)
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

    def test_rejects_missing_latest_closed_candle(self):
        raw = make_raw()
        raw.pop()
        with self.assertRaisesRegex(ValueError, "latest expected closed"):
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


    def test_rejects_misaligned_close_timestamp(self):
        raw = make_raw()
        raw[100][6] = raw[100][0] + 299998
        with self.assertRaisesRegex(ValueError, "close timestamp"):
            parse_rows(raw, now=dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc))

    def test_rejects_negative_trade_count(self):
        raw = make_raw()
        raw[100][8] = -1
        with self.assertRaisesRegex(ValueError, "negative trade count"):
            parse_rows(raw, now=dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc))

    def test_rejects_taker_buy_quote_above_total_quote(self):
        raw = make_raw()
        raw[100][10] = str(float(raw[100][7]) * 1.01)
        with self.assertRaisesRegex(ValueError, "total quote volume"):
            parse_rows(raw, now=dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc))

    def test_below_level_is_terminal_state_not_a_new_crossing(self):
        now = dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc)
        rows = parse_rows(make_raw(now=now), now=now)
        for row in rows:
            for key in ("open", "high", "low", "close"):
                row[key] *= 0.95
        result = build_forecast(rows, issued_at=now)
        risk = result["downside_risk"]
        self.assertTrue(risk["reference_below_level"])
        self.assertLess(risk["reference_vs_level_pct"], 0.0)
        self.assertEqual(risk["probability_event"], "terminal_price_below_level_not_first_passage")
        self.assertFalse(risk["severe_tail_scenario"]["crosses_level"])
        self.assertTrue(risk["severe_tail_scenario"]["ends_below_level"])

    def test_scenario_crosses_level_only_when_starting_above(self):
        now = dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc)
        rows = parse_rows(make_raw(now=now), now=now)
        for row in rows:
            for key in ("open", "high", "low", "close"):
                row[key] *= 1.04
        result = build_forecast(rows, issued_at=now)
        risk = result["downside_risk"]
        self.assertFalse(risk["reference_below_level"])
        self.assertTrue(risk["severe_tail_scenario"]["crosses_level"])
        self.assertTrue(risk["severe_tail_scenario"]["ends_below_level"])

    def test_target_grid_is_next_full_hour_and_shared(self):
        now = dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc)
        rows = parse_rows(make_raw(now=now), now=now)
        result = build_forecast(rows, issued_at=now)
        expected = dt.datetime(2026, 11, 10, 13, 0, tzinfo=dt.timezone.utc)
        for model in result["models"]:
            targets = [dt.datetime.fromisoformat(p["target_utc"].replace("Z", "+00:00")) for p in model["points"]]
            self.assertEqual(len(targets), 24)
            self.assertEqual(targets[0], expected)
            self.assertTrue(all((b-a).total_seconds() == 3600 for a, b in zip(targets, targets[1:])))
        common = [p["target_utc"] for p in result["models"][0]["points"]]
        for model in result["models"][1:]:
            self.assertEqual([p["target_utc"] for p in model["points"]], common)


class RawSnapshotTests(unittest.TestCase):
    def test_writes_exact_response_bytes_and_hash(self):
        import hashlib
        import tempfile
        from pathlib import Path

        payload = b'[ [1, "1", "1", "1", "1", "1", 2, "1", 1, "0.5", "0.5", "0"] ]\n'
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "raw.json"
            digest, size = write_raw_snapshot(payload, target)
            self.assertEqual(target.read_bytes(), payload)
            self.assertEqual(digest, hashlib.sha256(payload).hexdigest())
            self.assertEqual(size, len(payload))

    def test_rejects_non_json_raw_response(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "valid UTF-8 JSON"):
                write_raw_snapshot(b"not-json", directory + "/raw.json")


class ForecastMetadataTests(unittest.TestCase):
    def test_rejects_naive_retrieval_timestamp(self):
        now = dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc)
        rows = parse_rows(make_raw(now=now), now=now)
        with self.assertRaisesRegex(ValueError, "retrieved_at must be timezone-aware"):
            build_forecast(rows, issued_at=now, retrieved_at=now.replace(tzinfo=None))

    def test_rejects_invalid_model_commit(self):
        now = dt.datetime(2026, 11, 10, 12, 0, tzinfo=dt.timezone.utc)
        rows = parse_rows(make_raw(now=now), now=now)
        with self.assertRaisesRegex(ValueError, "40-character Git SHA"):
            build_forecast(rows, issued_at=now, model_commit="not-a-sha")


if __name__ == "__main__":
    unittest.main()
