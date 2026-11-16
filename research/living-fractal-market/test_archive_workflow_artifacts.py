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
        marker = f"Source head SHA: {stale_archive_sha}\\n"
        source_sha, wait_for_runs = select_source_commit(
            daily_sha, marker, {DAILY_TRIGGER_PATH}
        )
        self.assertEqual(source_sha, daily_sha)
        self.assertTrue(wait_for_runs)

    def test_archive_marker_uses_explicit_source_commit(self):
        daily_sha = "b" * 40
        source_sha = "a" * 40
        marker = f"Source head SHA: {source_sha}\\n"
        selected, wait_for_runs = select_source_commit(
            daily_sha, marker, {ARCHIVE_MARKER_PATH}
        )
        self.assertEqual(selected, source_sha)
        self.assertFalse(wait_for_runs)

    def test_non_trigger_change_does_not_use_stale_archive_marker(self):
        daily_sha = "b" * 40
        stale_archive_sha = "a" * 40
        marker = f"Source head SHA: {stale_archive_sha}\\n"
        selected, wait_for_runs = select_source_commit(
            daily_sha, marker, {"research/living-fractal-market/RESEARCH_LOG.md"}
        )
        self.assertEqual(selected, daily_sha)
        self.assertFalse(wait_for_runs)

    def test_malformed_archive_marker_is_rejected_when_marker_changed(self):
        with self.assertRaisesRegex(ValueError, "valid"):
            select_source_commit(
                "b" * 40, "Source head SHA: invalid\\n", {ARCHIVE_MARKER_PATH}
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


if __name__ == "__main__":
    unittest.main()
