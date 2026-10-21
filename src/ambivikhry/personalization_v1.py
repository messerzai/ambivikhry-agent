"""Auditable, consent-aware personalization primitives for Ambivikhry.

This module is intentionally provider-agnostic and uses only the Python standard
library. It does not infer sensitive traits or make medical claims.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4


class EvidenceKind(str, Enum):
    USER_STATED = "user_stated"
    OBSERVATION = "observation"
    HYPOTHESIS = "hypothesis"


class ProposalStatus(str, Enum):
    PROPOSED = "proposed"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ProfileEntry:
    key: str
    value: Any
    kind: EvidenceKind
    source: str
    created_at: str = field(default_factory=utc_now)
    confidence: float = 1.0
    expires_at: str | None = None
    consent_scope: str = "personalization"
    entry_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("key must not be empty")
        if not self.source.strip():
            raise ValueError("source must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.kind is EvidenceKind.HYPOTHESIS and self.confidence == 1.0:
            # Hypotheses are uncertain by definition; require an explicit lower score.
            raise ValueError("hypotheses must have confidence below 1.0")


@dataclass
class Feedback:
    task_id: str
    useful: bool
    outcome_achieved: bool | None = None
    note: str = ""
    created_at: str = field(default_factory=utc_now)
    feedback_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id must not be empty")


@dataclass
class ProfileStore:
    """Small JSON-backed profile store; one instance must map to one user.

    Writes are atomic at the file level. Callers must enforce authentication and
    authorization before constructing/using a store for a user.
    """

    path: Path
    user_id: str
    biometrics_enabled: bool = False
    entries: list[ProfileEntry] = field(default_factory=list)
    feedback: list[Feedback] = field(default_factory=list)
    audit: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.user_id.strip():
            raise ValueError("user_id must not be empty")

    def propose(self, entry: ProfileEntry) -> str:
        if entry.kind is EvidenceKind.USER_STATED and not entry.source:
            raise ValueError("user-stated entries require a source")
        if any(e.key == entry.key and e.value == entry.value and e.kind == entry.kind
               for e in self.entries):
            return "duplicate"
        self.audit.append({"at": utc_now(), "action": "propose_entry",
                           "entry_id": entry.entry_id, "key": entry.key})
        self.entries.append(entry)
        self.save()
        return "added"

    def record_feedback(self, item: Feedback) -> str:
        if any(f.task_id == item.task_id and f.useful == item.useful
               and f.outcome_achieved == item.outcome_achieved and f.note == item.note
               for f in self.feedback):
            return "duplicate"
        self.feedback.append(item)
        self.audit.append({"at": utc_now(), "action": "record_feedback",
                           "feedback_id": item.feedback_id, "task_id": item.task_id})
        self.save()
        return "added"

    def confirm(self, entry_id: str) -> None:
        entry = self._entry(entry_id)
        entry.kind = EvidenceKind.USER_STATED
        entry.confidence = 1.0
        self.audit.append({"at": utc_now(), "action": "confirm_entry",
                           "entry_id": entry_id})
        self.save()

    def reject(self, entry_id: str) -> None:
        self.entries = [e for e in self.entries if e.entry_id != entry_id]
        self.audit.append({"at": utc_now(), "action": "reject_entry",
                           "entry_id": entry_id})
        self.save()

    def delete_key(self, key: str) -> int:
        before = len(self.entries)
        self.entries = [e for e in self.entries if e.key != key]
        removed = before - len(self.entries)
        self.audit.append({"at": utc_now(), "action": "delete_key",
                           "key": key, "removed": removed})
        self.save()
        return removed

    def add_biometric_signal(self, signal: dict[str, Any]) -> None:
        if not self.biometrics_enabled:
            raise PermissionError("biometric collection is disabled; explicit opt-in required")
        required = {"type", "value", "timestamp", "quality"}
        if not required.issubset(signal):
            raise ValueError(f"signal missing fields: {sorted(required - set(signal))}")
        # Signals are stored as explicitly consented observations, never diagnoses.
        self.propose(ProfileEntry(
            key=f"biometric.{signal['type']}",
            value={k: signal[k] for k in required},
            kind=EvidenceKind.OBSERVATION,
            source="consented_biometric_signal",
            confidence=float(signal["quality"]),
            consent_scope="biometrics",
        ))

    def _entry(self, entry_id: str) -> ProfileEntry:
        for entry in self.entries:
            if entry.entry_id == entry_id:
                return entry
        raise KeyError(entry_id)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 1,
            "user_id": self.user_id,
            "biometrics_enabled": self.biometrics_enabled,
            "entries": [{**asdict(e), "kind": e.kind.value} for e in self.entries],
            "feedback": [asdict(f) for f in self.feedback],
            "audit": self.audit,
        }
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(self.path)

    @classmethod
    def load(cls, path: Path, expected_user_id: str) -> "ProfileStore":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("user_id") != expected_user_id:
            raise PermissionError("profile belongs to a different user")
        entries = [
            ProfileEntry(**{**raw, "kind": EvidenceKind(raw["kind"])})
            for raw in payload.get("entries", [])
        ]
        return cls(path=path, user_id=expected_user_id,
                   biometrics_enabled=bool(payload.get("biometrics_enabled", False)),
                   entries=entries,
                   feedback=[Feedback(**x) for x in payload.get("feedback", [])],
                   audit=list(payload.get("audit", [])))
