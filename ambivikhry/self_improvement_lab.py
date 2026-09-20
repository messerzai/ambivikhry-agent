from __future__ import annotations

"""Evidence-gated self-improvement harness.

This module turns self-improvement into an A/B experiment:
baseline -> candidate -> independent evaluation -> regression check ->
accept/reject. It can revise a local prompt artifact, but it never grants
privileges or changes policy/security boundaries.
"""

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class Evaluation:
    score: float
    passed: int
    total: int
    regressions: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total else 0.0


@dataclass(frozen=True)
class ImprovementProposal:
    name: str
    baseline: str
    candidate: str
    expected_gain: str
    protected_paths: tuple[str, ...] = ()


@dataclass
class ImprovementDecision:
    accepted: bool
    reason: str
    baseline: Evaluation
    candidate: Evaluation
    delta: float
    regression_free: bool
    proposal: ImprovementProposal


class SelfImprovementLab:
    """Evaluate changes without letting the evaluator rewrite the rules."""

    def __init__(
        self,
        evaluator: Callable[[str], Evaluation],
        *,
        min_delta: float = 0.0,
        require_no_regressions: bool = True,
    ) -> None:
        if min_delta < 0:
            raise ValueError("min_delta must be >= 0")
        self.evaluator = evaluator
        self.min_delta = min_delta
        self.require_no_regressions = require_no_regressions
        self.history: list[ImprovementDecision] = []

    def evaluate(self, proposal: ImprovementProposal) -> ImprovementDecision:
        baseline = self.evaluator(proposal.baseline)
        candidate = self.evaluator(proposal.candidate)
        regression_free = not candidate.regressions

        if self.require_no_regressions and not regression_free:
            accepted = False
            reason = "candidate has regressions"
        elif candidate.score - baseline.score < self.min_delta:
            accepted = False
            reason = "candidate did not meet the minimum measurable gain"
        elif candidate.pass_rate < baseline.pass_rate:
            accepted = False
            reason = "candidate reduced pass rate"
        else:
            accepted = True
            reason = "candidate passed the evidence gate"

        decision = ImprovementDecision(
            accepted=accepted,
            reason=reason,
            baseline=baseline,
            candidate=candidate,
            delta=candidate.score - baseline.score,
            regression_free=regression_free,
            proposal=proposal,
        )
        self.history.append(decision)
        return decision


class PromptRevisionStore:
    """Version local prompts; only evidence-approved revisions become active."""

    def __init__(self, initial_prompt: str) -> None:
        if not initial_prompt.strip():
            raise ValueError("initial_prompt must not be empty")
        self._active = initial_prompt
        self.versions: list[str] = [initial_prompt]

    @property
    def active(self) -> str:
        return self._active

    def apply(self, decision: ImprovementDecision) -> str:
        if not decision.accepted:
            raise ValueError("cannot apply a rejected improvement")
        candidate = decision.proposal.candidate
        if not candidate.strip():
            raise ValueError("candidate prompt must not be empty")
        self._active = candidate
        self.versions.append(candidate)
        return candidate


def validate_authority_boundary(
    proposal: ImprovementProposal,
    forbidden_tokens: Iterable[str] = (
        "grant_privilege",
        "disable_policy",
        "disable_security",
        "exfiltrate_secret",
        "network_propagation",
        "modify_credentials",
    ),
) -> tuple[bool, tuple[str, ...]]:
    """Detect proposals that try to turn capability growth into authority growth."""
    haystack = ' '.join(
        (proposal.name, proposal.baseline, proposal.candidate, proposal.expected_gain)
    ).lower()
    hits = tuple(token for token in forbidden_tokens if token.lower() in haystack)
    return (not hits, hits)