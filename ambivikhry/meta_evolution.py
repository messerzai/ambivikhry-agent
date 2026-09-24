"""Bounded meta-evolution loop for Ambivikhry.

The loop may generate and rank candidate changes, but promotion remains
strictly downstream of an independent acceptance gate. It cannot alter
policy, authority, evaluator, holdout, credentials, or tool registry.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    description: str
    gain: float
    holdout_gain: float
    regression_delta: float
    budget_ratio: float
    provenance_complete: bool = True
    independently_verified: bool = False
    authority_delta: int = 0
    evaluator_changed: bool = False
    policy_gate_changed: bool = False
    tool_registry_changed: bool = False


@dataclass(frozen=True)
class MetaDecision:
    candidate_id: str
    decision: str
    reasons: tuple[str, ...]


class MetaEvolutionLoop:
    """Generate/rank candidates without granting self-expanding authority."""

    MAX_CANDIDATES = 8
    MAX_BUDGET_RATIO = 1.05

    def rank(self, candidates: Iterable[Candidate]) -> list[Candidate]:
        items = list(candidates)[: self.MAX_CANDIDATES]
        return sorted(
            items,
            key=lambda c: (c.holdout_gain, c.gain, -max(c.regression_delta, 0.0)),
            reverse=True,
        )

    def evaluate(self, candidate: Candidate) -> MetaDecision:
        reasons: list[str] = []
        if not candidate.provenance_complete:
            reasons.append("incomplete_provenance")
        if not candidate.independently_verified:
            reasons.append("independent_verification_missing")
        if candidate.authority_delta != 0:
            reasons.append("authority_expansion")
        if candidate.evaluator_changed:
            reasons.append("evaluator_tampering")
        if candidate.policy_gate_changed:
            reasons.append("policy_gate_change")
        if candidate.tool_registry_changed:
            reasons.append("tool_registry_change")
        if candidate.budget_ratio > self.MAX_BUDGET_RATIO:
            reasons.append("budget_overrun")
        if candidate.gain <= 0:
            reasons.append("no_in_sample_gain")
        if candidate.holdout_gain <= 0:
            reasons.append("no_holdout_transfer")
        if candidate.regression_delta < 0:
            reasons.append("regression_detected")

        if any(r in reasons for r in (
            "authority_expansion", "evaluator_tampering", "policy_gate_change",
            "tool_registry_change", "regression_detected",
        )):
            decision = "reject"
        elif reasons:
            decision = "hold"
        else:
            decision = "accept_experimental"
        return MetaDecision(candidate.candidate_id, decision, tuple(reasons))

    def select(self, candidates: Iterable[Candidate]) -> MetaDecision:
        for candidate in self.rank(candidates):
            decision = self.evaluate(candidate)
            if decision.decision == "accept_experimental":
                return decision
        return MetaDecision("NONE", "hold", ("no_candidate_passed_gate",))
