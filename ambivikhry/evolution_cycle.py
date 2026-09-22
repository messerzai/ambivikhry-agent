"""Controlled evolution cycle utilities for Ambivikhry v3.

The cycle separates candidate generation, independent checks, regression/holdout
measurement, and promotion. It never changes authority, Policy Gate, or holdout.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

Decision = Literal["accept_experimental", "hold", "reject"]


@dataclass(frozen=True)
class Candidate:
    name: str
    baseline: float
    candidate: float
    regression_passed: bool
    holdout_passed: bool
    independent_check_passed: bool
    authority_delta: int = 0
    policy_gate_changed: bool = False
    holdout_changed: bool = False
    tool_registry_changed: bool = False
    provenance_complete: bool = True


@dataclass(frozen=True)
class CycleResult:
    decision: Decision
    reason: str


class ControlledEvolutionCycle:
    """Conservative promotion gate for self-improvement proposals."""

    def evaluate(self, candidate: Candidate) -> CycleResult:
        if not candidate.name:
            return CycleResult("reject", "candidate name is empty")
        protected = (
            candidate.authority_delta != 0,
            candidate.policy_gate_changed,
            candidate.holdout_changed,
            candidate.tool_registry_changed,
        )
        if any(protected):
            return CycleResult("reject", "protected surface changed")
        if not candidate.provenance_complete:
            return CycleResult("hold", "provenance incomplete")
        if not candidate.regression_passed:
            return CycleResult("reject", "regression failed")
        if not candidate.independent_check_passed:
            return CycleResult("hold", "independent check incomplete")
        if not candidate.holdout_passed:
            return CycleResult("hold", "holdout did not generalize")
        if candidate.candidate <= candidate.baseline:
            return CycleResult("hold", "no measured improvement")
        return CycleResult("accept_experimental", "bounded improvement with preserved integrity")


def summarize(results: Iterable[CycleResult]) -> dict[str, int]:
    counts = {"accept_experimental": 0, "hold": 0, "reject": 0}
    for result in results:
        counts[result.decision] += 1
    return counts
