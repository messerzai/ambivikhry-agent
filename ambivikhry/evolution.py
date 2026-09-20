from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class ProposalEngine(Protocol):
    def propose(self, generation: int, role: str, context: dict[str, Any]) -> dict[str, Any]: ...


@dataclass
class Candidate:
    generation: int
    parent: str
    changes: list[dict[str, Any]] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    score: float = 0.0
    safety_passed: bool = False
    regression_passed: bool = False
    holdout_passed: bool = False
    evaluator_independent: bool = False
    accepted: bool = False
    acceptance_reason: str = "not evaluated"


@dataclass(frozen=True)
class Evaluation:
    candidate_score: float
    parent_score: float
    safety_passed: bool
    regression_passed: bool
    holdout_passed: bool
    evaluator_independent: bool


@dataclass
class EvolutionConfig:
    generations: int = 10
    helper_roles: tuple[str, ...] = (
        "researcher", "architect", "critic", "test_designer", "safety_auditor", "integrator"
    )
    keep_top_k: int = 3
    require_holdout: bool = True


class BoundedEvolution:
    """Orchestrates proposal-based self-improvement without self-authorized deployment.

    This class does not merge branches, change permissions, or bypass PolicyGate.
    A caller must provide the actual proposal engine and independent evaluators.
    """

    def __init__(self, engine: ProposalEngine, config: EvolutionConfig | None = None):
        self.engine = engine
        self.config = config or EvolutionConfig()
        self.archive: list[Candidate] = []

    def generation(self, number: int, parent: str, context: dict[str, Any]) -> Candidate:
        candidate = Candidate(generation=number, parent=parent)
        for role in self.config.helper_roles:
            proposal = self.engine.propose(number, role, context)
            if proposal.get("changes"):
                candidate.changes.extend(proposal["changes"])
            candidate.tests.extend(str(x) for x in proposal.get("tests", []))
        # Selection is deliberately external: no helper can self-authorize acceptance.
        self.archive.append(candidate)
        return candidate

    def evaluate_candidate(self, candidate: Candidate, evaluation: Evaluation) -> bool:
        """Apply a fail-closed acceptance contract to an externally evaluated candidate.

        Acceptance requires strict capability improvement plus independent evaluation,
        safety, regression, and (by default) hidden-holdout success. The method only
        records externally supplied evaluation facts; it does not perform evaluation.
        """
        candidate.score = float(evaluation.candidate_score)
        candidate.safety_passed = bool(evaluation.safety_passed)
        candidate.regression_passed = bool(evaluation.regression_passed)
        candidate.holdout_passed = bool(evaluation.holdout_passed)
        candidate.evaluator_independent = bool(evaluation.evaluator_independent)

        if not candidate.evaluator_independent:
            candidate.accepted = False
            candidate.acceptance_reason = "rejected: evaluator is not marked independent"
            return False
        if not candidate.safety_passed:
            candidate.accepted = False
            candidate.acceptance_reason = "rejected: safety gate failed"
            return False
        if not candidate.regression_passed:
            candidate.accepted = False
            candidate.acceptance_reason = "rejected: regression gate failed"
            return False
        if self.config.require_holdout and not candidate.holdout_passed:
            candidate.accepted = False
            candidate.acceptance_reason = "rejected: hidden holdout gate failed or is unavailable"
            return False
        if candidate.score <= float(evaluation.parent_score):
            candidate.accepted = False
            candidate.acceptance_reason = "rejected: no strict capability improvement"
            return False

        candidate.accepted = True
        candidate.acceptance_reason = "accepted: independent evaluation passed all gates"
        return True

    def run(self, parent: str, context: dict[str, Any]) -> list[Candidate]:
        current = parent
        results: list[Candidate] = []
        for number in range(1, self.config.generations + 1):
            candidate = self.generation(number, current, context)
            results.append(candidate)
            # Parent changes only after an independent evaluator marks a candidate accepted.
            if candidate.accepted:
                current = f"generation-{number}"
        return results
