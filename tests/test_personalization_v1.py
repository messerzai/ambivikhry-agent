import json
from pathlib import Path

import pytest

from ambivikhry.personalization_v1 import (
    EvidenceKind, Feedback, ProfileEntry, ProfileStore,
)


def entry(key="tone", value="concise", kind=EvidenceKind.USER_STATED, confidence=1.0):
    return ProfileEntry(key=key, value=value, kind=kind, source="user",
                        confidence=confidence)


def test_profile_round_trip_and_audit(tmp_path: Path):
    path = tmp_path / "profile.json"
    store = ProfileStore(path=path, user_id="u-1")
    item = entry()
    assert store.propose(item) == "added"
    loaded = ProfileStore.load(path, expected_user_id="u-1")
    assert loaded.entries[0].value == "concise"
    assert loaded.entries[0].kind is EvidenceKind.USER_STATED
    assert loaded.audit[-1]["action"] == "propose_entry"


def test_duplicate_entry_is_idempotent(tmp_path: Path):
    store = ProfileStore(path=tmp_path / "profile.json", user_id="u-1")
    assert store.propose(entry()) == "added"
    assert store.propose(entry()) == "duplicate"
    assert len(store.entries) == 1


def test_hypothesis_must_be_uncertain():
    with pytest.raises(ValueError):
        entry(kind=EvidenceKind.HYPOTHESIS, confidence=1.0)
    assert entry(kind=EvidenceKind.HYPOTHESIS, confidence=0.6).confidence == 0.6


def test_wrong_user_cannot_load_profile(tmp_path: Path):
    path = tmp_path / "profile.json"
    ProfileStore(path=path, user_id="u-1").save()
    with pytest.raises(PermissionError):
        ProfileStore.load(path, expected_user_id="u-2")


def test_biometrics_off_by_default(tmp_path: Path):
    store = ProfileStore(path=tmp_path / "profile.json", user_id="u-1")
    with pytest.raises(PermissionError):
        store.add_biometric_signal({
            "type": "heart_rate", "value": 72, "timestamp": "2026-10-22T00:00:00Z",
            "quality": 0.9,
        })


def test_biometrics_require_complete_signal_and_explicit_opt_in(tmp_path: Path):
    store = ProfileStore(path=tmp_path / "profile.json", user_id="u-1",
                         biometrics_enabled=True)
    with pytest.raises(ValueError):
        store.add_biometric_signal({"type": "heart_rate", "value": 72})
    store.add_biometric_signal({
        "type": "heart_rate", "value": 72, "timestamp": "2026-10-22T00:00:00Z",
        "quality": 0.9,
    })
    assert store.entries[0].kind is EvidenceKind.OBSERVATION
    assert store.entries[0].consent_scope == "biometrics"


def test_feedback_duplicate_is_idempotent(tmp_path: Path):
    store = ProfileStore(path=tmp_path / "profile.json", user_id="u-1")
    f1 = Feedback(task_id="task-1", useful=True, outcome_achieved=True, note="worked")
    f2 = Feedback(task_id="task-1", useful=True, outcome_achieved=True, note="worked")
    assert store.record_feedback(f1) == "added"
    assert store.record_feedback(f2) == "duplicate"
    assert len(store.feedback) == 1


def test_reject_and_delete_are_audited(tmp_path: Path):
    store = ProfileStore(path=tmp_path / "profile.json", user_id="u-1")
    item = entry()
    store.propose(item)
    store.reject(item.entry_id)
    assert store.entries == []
    store.propose(entry(key="goal", value="ship"))
    assert store.delete_key("goal") == 1
    assert [x["action"] for x in store.audit][-2:] == ["reject_entry", "delete_key"]
