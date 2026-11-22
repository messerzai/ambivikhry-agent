import hashlib
import unittest
import urllib.error
from email.message import Message
from unittest.mock import MagicMock, patch

from archive_workflow_artifacts import (
    ARCHIVE_MARKER_PATH,
    DAILY_TRIGGER_PATH,
    download_artifact,
    immutable_path_for_payload,
    select_source_commit,
    should_wait_for_evaluation,
    validate_forecast_schema,
    append_forecast_ledger,
    validate_raw_input_snapshot,
)


class ArchiveArtifactDownloadTests(unittest.TestCase):
    def test_signed_redirect_does_not_forward_github_token(self):
        payload = b"immutable-artifact-zip"
        api_url = "https://api.github.com/repos/example/repo/actions/artifacts/123/zip"
        signed_url = "https://objects.example.test/signed-download?sig=abc"
        headers = Message()
        headers["Location"] = signed_url
        redirect = urllib.error.HTTPError(api_url, 302, "Found", headers, None)
        opener = MagicMock()
        opener.open.side_effect = redirect

        signed_response = MagicMock()
        signed_response.__enter__.return_value.read.return_value = payload
        with (
            patch("archive_workflow_artifacts.urllib.request.build_opener", return_value=opener),
            patch("archive_workflow_artifacts.urllib.request.urlopen", return_value=signed_response) as signed_open,
        ):
            result = download_artifact(
                "example/repo",
                {"id": 123, "name": "forecast", "digest": f"sha256:{hashlib.sha256(payload).hexdigest()}"},
                "test-token",
            )

        api_request = opener.open.call_args.args[0]
        storage_request = signed_open.call_args.args[0]
        self.assertEqual(api_request.get_header("Authorization"), "token test-token")
        self.assertEqual(storage_request.full_url, signed_url)
        self.assertIsNone(storage_request.get_header("Authorization"))
        self.assertIsNone(storage_request.get_header("Accept"))
        self.assertEqual(result, payload)

    def test_conflicting_evaluation_payload_gets_artifact_specific_path(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            existing = root / "evaluation.json"
            existing.write_bytes(b"first immutable evaluation")
            same = immutable_path_for_payload(
                root, "evaluation.json", b"first immutable evaluation", "141"
            )
            different = immutable_path_for_payload(
                root, "evaluation.json", b"repeat with a new evaluated_at", "141"
            )
            self.assertEqual(same, "evaluation.json")
            self.assertEqual(different, "evaluation.artifact-141.json")
            self.assertEqual(existing.read_bytes(), b"first immutable evaluation")


    def test_daily_trigger_ignores_stale_archive_marker_and_waits(self):
        daily_sha = "b" * 40
        stale_archive_sha = "a" * 40
        marker = f"Source head SHA: {stale_archive_sha}\n"
        source_sha, wait_for_runs = select_source_commit(
            daily_sha, marker, {DAILY_TRIGGER_PATH}
        )
        self.assertEqual(source_sha, daily_sha)
        self.assertTrue(wait_for_runs)

    def test_archive_marker_uses_explicit_source_commit(self):
        daily_sha = "b" * 40
        source_sha = "a" * 40
        marker = f"Source head SHA: {source_sha}\n"
        selected, wait_for_runs = select_source_commit(
            daily_sha, marker, {ARCHIVE_MARKER_PATH}
        )
        self.assertEqual(selected, source_sha)
        self.assertFalse(wait_for_runs)

    def test_non_trigger_change_does_not_use_stale_archive_marker(self):
        daily_sha = "b" * 40
        stale_archive_sha = "a" * 40
        marker = f"Source head SHA: {stale_archive_sha}\n"
        selected, wait_for_runs = select_source_commit(
            daily_sha, marker, {"research/living-fractal-market/RESEARCH_LOG.md"}
        )
        self.assertEqual(selected, daily_sha)
        self.assertFalse(wait_for_runs)


    def test_forecast_code_change_waits_for_sibling_forecast_run(self):
        source_sha = "c" * 40
        selected, wait_for_runs = select_source_commit(
            source_sha, "", {"research/living-fractal-market/forecast_btc_5m.py"}
        )
        self.assertEqual(selected, source_sha)
        self.assertTrue(wait_for_runs)


    def test_forecast_code_change_does_not_wait_for_nonexistent_evaluation_run(self):
        self.assertFalse(should_wait_for_evaluation({"research/living-fractal-market/forecast_btc_5m.py"}))

    def test_daily_marker_change_waits_for_evaluation_run(self):
        self.assertTrue(should_wait_for_evaluation({DAILY_TRIGGER_PATH}))

    def test_malformed_archive_marker_is_rejected_when_marker_changed(self):
        with self.assertRaisesRegex(ValueError, "valid"):
            select_source_commit(
                "b" * 40, "Source head SHA: invalid\n", {ARCHIVE_MARKER_PATH}
            )

    def test_artifact_digest_mismatch_is_rejected(self):
        payload = b"artifact"
        headers = Message()
        headers["Location"] = "https://objects.example.test/signed-download"
        redirect = urllib.error.HTTPError(
            "https://api.github.com/repos/example/repo/actions/artifacts/123/zip",
            302,
            "Found",
            headers,
            None,
        )
        opener = MagicMock()
        opener.open.side_effect = redirect
        signed_response = MagicMock()
        signed_response.__enter__.return_value.read.return_value = payload
        with (
            patch("archive_workflow_artifacts.urllib.request.build_opener", return_value=opener),
            patch("archive_workflow_artifacts.urllib.request.urlopen", return_value=signed_response),
        ):
            with self.assertRaisesRegex(ValueError, "artifact digest mismatch"):
                download_artifact(
                    "example/repo",
                    {"id": 123, "name": "forecast", "digest": "sha256:" + "0" * 64},
                    "test-token",
                )


class ForecastSchemaValidationTests(unittest.TestCase):
    def test_accepts_legacy_v1_payload(self):
        validate_forecast_schema({"schema": "lfm.forecast.5m.v1"}, {"id": 1})

    def test_accepts_v2_when_provenance_matches_workflow(self):
        commit = "a" * 40
        forecast = {
            "schema": "lfm.forecast.5m.v2",
            "vintage_id": "lfm5m-test-BTCUSDT-binance-spot-council-0.4",
            "model_commit": commit,
            "training_cutoff_utc": "2026-11-17T07:34:59.999Z",
            "input_interval": "5m",
            "retrieved_at_utc": "2026-11-17T07:35:00.100Z",
            "issued_at_utc": "2026-11-17T07:35:00.200Z",
            "data_cutoff_utc": "2026-11-17T07:34:59.999Z",
        }
        validate_forecast_schema(forecast, {"id": 2, "head_sha": commit})

    def test_rejects_v2_commit_mismatch(self):
        commit = "a" * 40
        forecast = {
            "schema": "lfm.forecast.5m.v2", "vintage_id": "lfm5m-test",
            "model_commit": "b" * 40, "training_cutoff_utc": "2026-11-17T07:34:59Z",
            "input_interval": "5m", "retrieved_at_utc": "2026-11-17T07:35:00Z",
            "issued_at_utc": "2026-11-17T07:35:01Z", "data_cutoff_utc": "2026-11-17T07:34:59Z",
        }
        with self.assertRaisesRegex(ValueError, "does not match workflow source commit"):
            validate_forecast_schema(forecast, {"id": 3, "head_sha": commit})

    def test_rejects_v2_non_monotone_timestamps(self):
        commit = "a" * 40
        forecast = {
            "schema": "lfm.forecast.5m.v2", "vintage_id": "lfm5m-test",
            "model_commit": commit, "training_cutoff_utc": "2026-11-17T07:34:59Z",
            "input_interval": "5m", "retrieved_at_utc": "2026-11-17T07:35:02Z",
            "issued_at_utc": "2026-11-17T07:35:01Z", "data_cutoff_utc": "2026-11-17T07:34:59Z",
        }
        with self.assertRaisesRegex(ValueError, "data cutoff <= retrieval <= issue time"):
            validate_forecast_schema(forecast, {"id": 4, "head_sha": commit})


class ForecastLedgerFormattingTests(unittest.TestCase):
    def test_provenance_metadata_uses_real_line_breaks(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            ledger_path = Path(directory) / "FORECAST_LEDGER.md"
            ledger_path.write_text("# Forecast ledger\n", encoding="utf-8")
            forecast = {
                "issued_at_utc": "2026-11-17T07:38:41.322709Z",
                "asset": "BTC/USDT", "model_version": "LFM-5m-Downside-Aware-Council-0.4",
                "data_cutoff_utc": "2026-11-17T07:34:59.999Z", "schema": "lfm.forecast.5m.v2",
                "vintage_id": "lfm5m-test", "input_interval": "5m",
                "retrieved_at_utc": "2026-11-17T07:38:41.318153Z",
                "model_commit": "a" * 40, "training_cutoff_utc": "2026-11-17T07:34:59.999Z",
                "closed_candles": 999, "venue": "Binance Spot", "quote_currency": "USDT",
            }
            append_forecast_ledger(
                ledger_path,
                {"repository": {"full_name": "example/repo"}, "id": 1, "head_sha": "a" * 40},
                {"id": 2, "name": "forecast"},
                "forecasts/test.artifact.zip", "b" * 64,
                "forecasts/test.json", "c" * 64, forecast,
            )
            text = ledger_path.read_text(encoding="utf-8")
            self.assertNotIn("\\n- Input interval", text)
            self.assertIn("\n- Input interval / retrieved UTC:", text)
            self.assertIn("\n- Model commit / training cutoff UTC:", text)


class RawInputSnapshotTests(unittest.TestCase):
    @staticmethod
    def fixture():
        import json
        import hashlib
        from datetime import datetime, timezone

        open_ms = int(datetime(2026, 11, 17, 7, 30, tzinfo=timezone.utc).timestamp() * 1000)
        close_ms = open_ms + 300_000 - 1
        row = [open_ms, "100", "101", "99", "100", "1", close_ms, "100", 10, "0.5", "50", "0"]
        raw = json.dumps([row], separators=(",", ":")).encode("utf-8")
        forecast = {
            "issued_at_utc": "2026-11-17T07:35:00.200Z",
            "data_cutoff_utc": "2026-11-17T07:34:59.999Z",
            "closed_candles": 1,
            "data_provenance": {
                "request_url": "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1000",
                "raw_response_file": "forecast_5m_raw_klines.json",
                "raw_response_sha256": hashlib.sha256(raw).hexdigest(),
                "raw_response_bytes": len(raw),
                "last_closed_candle_open_ms": open_ms,
                "last_closed_candle_close_ms": close_ms,
            },
        }
        return forecast, raw

    def test_accepts_exact_raw_snapshot_and_cutoff(self):
        forecast, raw = self.fixture()
        result = validate_raw_input_snapshot(forecast, raw)
        self.assertEqual(result["closed_candles"], 1)
        self.assertEqual(result["last_closed_close_ms"], forecast["data_provenance"]["last_closed_candle_close_ms"])

    def test_rejects_raw_snapshot_hash_mismatch(self):
        forecast, raw = self.fixture()
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            validate_raw_input_snapshot(forecast, raw + b" ")

    def test_rejects_cutoff_mismatch(self):
        forecast, raw = self.fixture()
        forecast["data_cutoff_utc"] = "2026-11-17T07:29:59.999Z"
        with self.assertRaisesRegex(ValueError, "does not match data_cutoff_utc"):
            validate_raw_input_snapshot(forecast, raw)


if __name__ == "__main__":
    unittest.main()
