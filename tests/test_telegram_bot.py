from __future__ import annotations

import os

import pytest

from ambivikhry.telegram_bot import TelegramAmbivikhry, _chunks


def test_chunks_respect_telegram_limit():
    parts = list(_chunks("x" * 9000, 4096))
    assert [len(x) for x in parts] == [4096, 4096, 808]


def test_allowlist_is_fail_closed(monkeypatch, tmp_path):
    monkeypatch.delenv("TELEGRAM_ALLOWED_USER_IDS", raising=False)
    monkeypatch.setenv("AMBIVIKHRY_WORKDIR", str(tmp_path))
    with pytest.raises(RuntimeError):
        TelegramAmbivikhry()


def test_allowlist_accepts_configured_id(monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_ALLOWED_USER_IDS", "123,456")
    monkeypatch.setenv("AMBIVIKHRY_WORKDIR", str(tmp_path))
    interface = TelegramAmbivikhry()
    assert interface.allowed_users == {123, 456}
