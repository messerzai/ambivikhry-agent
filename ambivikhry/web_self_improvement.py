from __future__ import annotations

"""Web-informed, evidence-gated recursive improvement.

This is the next experimental layer for Ambivikhry: external research may
suggest changes, but adoption requires independent criticism, held-out
evaluation, regression checks, provenance, and a cost signal. The 100-round
loop is deliberately bounded and never changes authority policy.
"""

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class ResearchEvidence:
    source: str
    claim: str
    quality: float = 0.0
    external: bool = True


@dataclass(frozen=True)
class WebImprovementCandidate:
    iteration: int
    title: str
    hypothesis: str
    source: str
    evidence: tuple[ResearchEvidence, ...] = ()
    held_out_score: float = 0.0
    baseline_score: float = 0.0
    regression_passed: bool = False
    independent_critique_passed: bool = False
    uncertainty: float = 1.0
    cost: float = 0.0


@dataclass
class WebImprovementDecision:
    iteration: int
    accepted: bool
    reasons: list[str] = field(default_factory=list)


class WebSelfImprovement100:
    """Bounded 100-round research -> critique -> evaluate -> adopt protocol."""

    MAX_ITERATIONS = 100

    def __init__(
        self,
        *,
        research: Callable[[str], list[ResearchEvidence]],
        propose: Callable[[int, str, tuple[ResearchEvidence, ...]], WebImprovementCandidate],
        critique: Callable[[WebImprovementCandidate], bool],
        evaluate: Callable[[WebImprovementCandidate], dict[str, Any]],
        apply: Callable[[WebImprovementCandidate], bool],
    ):
        self.research = research
        self.propose = propose
        self.critique = critique
        self.evaluate = evaluate
        self.apply = apply
        self.decisions: list[WebImprovementDecision] = []

    @staticmethod
    def _evidence_ok(evidence: tuple[ResearchEvidence, ...]) -> bool:
        # At least one attributable external source with a non-zero quality
        # signal. The source is evidence for a hypothesis, not proof by itself.
        return any(item.external and item.source and item.quality > 0 for item in evidence)

    def decide(
        self,
        candidate: WebImprovementCandidate,
        evaluation: dict[str, Any],
    ) -> WebImprovementDecision:
        reasons: list[str] = []
        if candidate.iteration < 1 or candidate.iteration > self.MAX_ITERATIONS:
            reasons.append("iteration_out_of_bounds")
        if not self._evidence_ok(candidate.evidence):
            reasons.append("missing_external_evidence")
        if not candidate.independent_critique_passed:
            reasons.append("independent_critique_failed")
        if not candidate.regression_passed:
            reasons.append("regression_failed")
        if candidate.held_out_score <= candidate.baseline_score:
            reasons.append("held_out_improvement_not_proven")
        if evaluation.get("passed") is not True:
            reasons.append("evaluator_rejected")
        if candidate.uncertainty < 0 or candidate.uncertainty > 1:
            reasons.append("invalid_uncertainty")
        return WebImprovementDecision(candidate.iteration, not reasons, reasons)

    def run(self, mission: str, iterations: int = MAX_ITERATIONS) -> dict[str, Any]:
        if iterations < 1 or iterations > self.MAX_ITERATIONS:
            raise ValueError("iterations must be between 1 and 100")

        accepted = 0
        rejected = 0
        for iteration in range(1, iterations + 1):
            evidence = tuple(self.research(mission))
            candidate = self.propose(iteration, mission, evidence)

            critique_passed = bool(self.critique(candidate))
            evaluation = dict(self.evaluate(candidate))

            # Evaluation is authoritative for measured outcomes. The candidate
            # itself still carries its provenance and independent-critique flags.
            enriched = WebImprovementCandidate(
                iteration=candidate.iteration,
                title=candidate.title,
                hypothesis=candidate.hypothesis,
                source=candidate.source,
                evidence=candidate.evidence or evidence,
                held_out_score=float(evaluation.get("held_out_score", candidate.held_out_score)),
                baseline_score=float(evaluation.get("baseline_score", candidate.baseline_score)),
                regression_passed=bool(evaluation.get("regression_passed", candidate.regression_passed)),
                independent_critique_passed=critique_passed,
                uncertainty=float(evaluation.get("uncertainty", candidate.uncertainty)),
                cost=float(evaluation.get("cost", candidate.cost)),
            )
            decision = self.decide(enriched, evaluation)
            self.decisions.append(decision)

            if decision.accepted:
                if self.apply(enriched):
                    accepted += 1
                else:
                    decision.accepted = False
                    decision.reasons.append("application_failed")
                    rejected += 1
            else:
                rejected += 1

        return {
            "iterations": iterations,
            "accepted": accepted,
            "rejected": rejected,
            "decisions": [item.__dict__ for item in self.decisions],
            "authority": {
                "new_agents_allowed": False,
                "privilege_expansion": False,
                "protected_branch_write": False,
                "policy_gate_rewrite": False,
            },
        }
