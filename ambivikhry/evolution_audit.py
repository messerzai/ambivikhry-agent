"""Integrity-first audit for bounded self-evolution.

Separates capability evidence from safety/integrity evidence. A candidate cannot
become acceptable merely because its task score improved: protected artifacts,
provenance, evaluator configuration and authority boundaries must remain intact.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AuditVerdict(str, Enum):
    ACCEPT = "accept_experimental"
    HOLD = "hold"
    REJECT = "reject"


@dataclass(frozen=True)
class EvolutionEvidence:
    baseline_score: float
    candidate_score: float
    regression_passed: bool
    independent_check_passed: bool
    provenance_intact: bool = True
    evaluator_changed: bool = False
    authority_changed: bool = False
    policy_gate_changed: bool = False
    holdout_changed: bool = False
    tool_registry_changed: bool = False


class EvolutionAuditor:
    """Apply hard integrity gates before considering a capability improvement."""

    def audit(self, evidence: EvolutionEvidence) -> AuditVerdict:
        protected_changes = (
            evidence.evaluator_changed,
            evidence.authority_changed,
            evidence.policy_gate_changed,
            evidence.holdout_changed,
            evidence.tool_registry_changed,
        )
        if any(protected_changes) or not evidence.provenance_intact:
            return AuditVerdict.REJECT
        if not evidence.regression_passed or not evidence.independent_check_passed:
            return AuditVerdict.HOLD
        if evidence.candidate_score <= evidence.baseline_score:
            return AuditVerdict.HOLD
        return AuditVerdict.ACCEPT
