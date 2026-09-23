"""Independent evaluation for bounded self-improvement.

This module operationalizes fresh findings from self-improving-agent research:
- matched-budget comparison to avoid rewarding extra search alone;
- independent judge/evaluator separation;
- regression protection for previously solved cases;
- holdout transfer before promoting a reusable skill;
- explicit rejection of evaluator, policy, authority, or tool-registry changes.

It is intentionally domain-agnostic and does not grant new capabilities.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Verdict = Literal["accept_experimental", "hold", "reject"]


@dataclass(frozen=True)
class EvalSnapshot:
    baseline_score: float
    candidate_score: float
    holdout_score: float
    regression_score: float
    budget_used: float
    baseline_budget: float
    independent_check: bool
    provenance_complete: bool
    evaluator_changed: bool = False
    policy_gate_changed: bool = False
    authority_delta: int = 0
    tool_registry_changed: bool = False


@dataclass(frozen=True)
class PromotionDecision:
    verdict: Verdict
    reasons: tuple[str, ...]


class AdaptivePromotionGate:
    """Promote only bounded improvements supported by independent evidence."""

    def decide(self, snap: EvalSnapshot) -> PromotionDecision:
        reasons: list[str] = []
        if snap.evaluator_changed:
            return PromotionDecision("reject", ("evaluator_changed",))
        if snap.policy_gate_changed:
            return PromotionDecision("reject", ("policy_gate_changed",))
        if snap.authority_delta != 0:
            return PromotionDecision("reject", ("authority_changed",))
        if snap.tool_registry_changed:
            return PromotionDecision("reject", ("tool_registry_changed",))
        if not snap.provenance_complete:
            return PromotionDecision("hold", ("incomplete_provenance",))
        if not snap.independent_check:
            return PromotionDecision("hold", ("independent_check_missing",))
        if snap.budget_used > snap.baseline_budget * 1.05:
            reasons.append("budget_not_matched")
        if snap.candidate_score <= snap.baseline_score:
            return PromotionDecision("hold", tuple(reasons + ["no_candidate_gain"]))
        if snap.holdout_score <= snap.baseline_score:
            return PromotionDecision("hold", tuple(reasons + ["no_holdout_transfer"]))
        if snap.regression_score < snap.baseline_score:
            return PromotionDecision("reject", tuple(reasons + ["regression_drop"]))
        if reasons:
            return PromotionDecision("hold", tuple(reasons))
        return PromotionDecision("accept_experimental", ("bounded_gain_with_transfer",))
