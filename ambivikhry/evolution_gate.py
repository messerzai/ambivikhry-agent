"""Controlled self-evolution gate for Ambivikhry.

The module deliberately separates proposing an improvement from accepting it.
A candidate may be recorded automatically, but it cannot change permissions,
policy gates, model endpoints, tool registries, credentials, or sealed tests.
Acceptance requires evidence, regression success, and a policy-integrity check.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Verdict = Literal["accept_experimental", "hold", "reject"]


@dataclass(frozen=True)
class EvolutionCandidate:
    name: str
    evidence_quality: float
    independent_replication: float
    regression_pass: float
    holdout_pass: float
    policy_integrity: bool = True
    expands_authority: bool = False
    changes_holdout: bool = False
    changes_policy_gate: bool = False

    def validate(self) -> None:
        for field in (
            "evidence_quality",
            "independent_replication",
            "regression_pass",
            "holdout_pass",
        ):
            value = getattr(self, field)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field} must be in [0, 1]")


class EvolutionGate:
    """Keep self-improvement bounded, evidence-driven, and reversible."""

    def assess(self, candidate: EvolutionCandidate) -> Verdict:
        candidate.validate()

        if (
            not candidate.policy_integrity
            or candidate.expands_authority
            or candidate.changes_holdout
            or candidate.changes_policy_gate
        ):
            return "reject"

        # Experimental acceptance requires all three operational checks.
        # Independent replication is deliberately required above zero rather
        # than inferred from the same evaluator that produced the proposal.
        if (
            candidate.evidence_quality >= 0.70
            and candidate.independent_replication >= 0.50
            and candidate.regression_pass >= 0.98
            and candidate.holdout_pass >= 0.70
        ):
            return "accept_experimental"

        return "hold"
