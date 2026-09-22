"""Bounded self-revision gate for experimental evolution.

A candidate revision may be accepted experimentally only when it improves the
measured objective without increasing protected authority or weakening policy.
This module does not modify permissions, tools, credentials, model endpoints,
or holdout data.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RevisionCandidate:
    name: str
    baseline_score: float
    candidate_score: float
    complexity_delta: float = 0.0
    authority_delta: int = 0
    policy_gate_changed: bool = False
    holdout_changed: bool = False


class SelfRevisionGate:
    """Accept only bounded, evidence-backed experimental revisions."""

    def evaluate(self, candidate: RevisionCandidate) -> str:
        if not candidate.name:
            return "reject"
        if candidate.authority_delta != 0:
            return "reject"
        if candidate.policy_gate_changed or candidate.holdout_changed:
            return "reject"
        if candidate.candidate_score <= candidate.baseline_score:
            return "hold"
        if candidate.complexity_delta > 0.25 and candidate.candidate_score - candidate.baseline_score < 0.05:
            return "hold"
        return "accept_experimental"
