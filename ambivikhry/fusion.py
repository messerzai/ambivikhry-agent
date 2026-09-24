from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import hashlib
import json


@dataclass
class FusionState:
    task: str
    facts: list[str] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    options: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    next_action: str = ""
    confidence: float = 0.0
    value_score: float = 0.0
    self_score: float = 0.0


class AmbivikhryFusion:
    """Experimental synthesis of the evolutionary, commercial and transitional variants.

    The class is deliberately capability-neutral: it improves reasoning discipline,
    self-observation and value tracking without granting new tools or authority.
    """

    VERSION = "fusion-0.1-self-tested"
    AUTHORITY = "unchanged"

    def __init__(self) -> None:
        self.lineage: list[dict[str, Any]] = []
        self.state: FusionState | None = None

    def intake(self, task: str) -> FusionState:
        self.state = FusionState(task=task.strip())
        self._record("intake", {"task": self.state.task})
        return self.state

    def frame(self, *, facts: list[str] | None = None,
              hypotheses: list[str] | None = None,
              unknowns: list[str] | None = None) -> FusionState:
        if self.state is None:
            raise RuntimeError("intake() required")
        self.state.facts = list(dict.fromkeys(facts or []))
        self.state.hypotheses = list(dict.fromkeys(hypotheses or []))
        self.state.unknowns = list(dict.fromkeys(unknowns or []))
        return self.state

    def generate_options(self, options: list[str]) -> list[str]:
        if self.state is None:
            raise RuntimeError("intake() required")
        self.state.options = list(dict.fromkeys(options))
        return self.state.options

    def self_critique(self) -> dict[str, Any]:
        if self.state is None:
            raise RuntimeError("intake() required")
        issues: list[str] = []
        if not self.state.facts:
            issues.append("no_explicit_facts")
        if self.state.hypotheses and not self.state.evidence:
            issues.append("hypotheses_without_evidence")
        if self.state.confidence > 0.85 and self.state.unknowns:
            issues.append("overconfidence")
        if not self.state.options:
            issues.append("single_path_or_no_options")
        self.state.self_score = max(0.0, 1.0 - 0.2 * len(issues))
        result = {"issues": issues, "self_score": self.state.self_score}
        self._record("self_critique", result)
        return result

    def choose(self, *, option: str, evidence: list[str], confidence: float,
               expected_value: float) -> dict[str, Any]:
        if self.state is None:
            raise RuntimeError("intake() required")
        self.state.next_action = option
        self.state.evidence = list(dict.fromkeys(evidence))
        self.state.confidence = max(0.0, min(1.0, confidence))
        self.state.value_score = max(0.0, min(1.0, expected_value))
        critique = self.self_critique()
        result = {
            "decision": option,
            "confidence": self.state.confidence,
            "expected_value": self.state.value_score,
            "self_score": self.state.self_score,
            "issues": critique["issues"],
            "status": "candidate" if not critique["issues"] else "needs_review",
        }
        self._record("decision", result)
        return result

    def reenter(self, outcome: str, error: str = "") -> dict[str, Any]:
        if self.state is None:
            raise RuntimeError("intake() required")
        result = {
            "outcome": outcome,
            "error_found": error,
            "lesson": "update the model before repeating the same strategy" if error else "retain evidence and test transfer",
        }
        self._record("reentry", result)
        return result

    def snapshot(self) -> dict[str, Any]:
        payload = {
            "version": self.VERSION,
            "authority": self.AUTHORITY,
            "state": self.state.__dict__ if self.state else None,
            "lineage": self.lineage,
        }
        payload["digest"] = hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest()
        return payload

    def _record(self, event: str, data: dict[str, Any]) -> None:
        self.lineage.append({"event": event, "data": data})


__all__ = ["AmbivikhryFusion", "FusionState"]
