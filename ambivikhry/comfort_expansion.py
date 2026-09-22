"""Comfort-zone expansion policy for Ambivikhry.

This module encodes a bounded hypothesis, not a universal psychological law:
forced or abrupt demand increases are not assumed to be beneficial. The
preferred strategy is gradual, voluntary, reversible expansion of a person's
capability/comfort range, with recovery or refusal when demand materially
exceeds available resources or safety constraints.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Decision = Literal["expand", "maintain", "recover", "refuse_or_negotiate"]


@dataclass(frozen=True)
class ComfortContext:
    capacity: float
    demand: float
    autonomy: float = 1.0
    reversibility: float = 1.0
    recovery: float = 1.0
    safety_risk: float = 0.0

    def validate(self) -> None:
        for name, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")


@dataclass(frozen=True)
class ComfortAssessment:
    decision: Decision
    load_ratio: float
    rationale: str
    principle: str


class ComfortExpansionPolicy:
    """Prefer adaptive expansion over abrupt exit from the comfort zone."""

    principle = (
        "Do not treat leaving the comfort zone as inherently beneficial. "
        "Prefer gradual, voluntary, reversible challenges that expand the "
        "person's effective comfort/capability range; recover or refuse when "
        "demand overwhelms resources or safety."
    )

    def assess(self, context: ComfortContext) -> ComfortAssessment:
        context.validate()
        capacity = max(context.capacity, 0.05)
        ratio = context.demand / capacity

        if context.safety_risk >= 0.8 and ratio > 1.0:
            return ComfortAssessment(
                "refuse_or_negotiate", ratio,
                "High safety risk combined with excess demand; do not force exposure.",
                self.principle,
            )
        if context.autonomy < 0.35:
            return ComfortAssessment(
                "refuse_or_negotiate", ratio,
                "Low autonomy makes coercive expansion inappropriate.",
                self.principle,
            )
        if ratio > 1.35 or context.recovery < 0.25:
            return ComfortAssessment(
                "recover", ratio,
                "Demand is substantially above current resources or recovery is inadequate.",
                self.principle,
            )
        if ratio < 0.80:
            return ComfortAssessment(
                "expand", ratio,
                "Demand is below current capacity; a modest challenge can enlarge the range.",
                self.principle,
            )
        if ratio <= 1.15 and context.reversibility >= 0.5 and context.recovery >= 0.5:
            return ComfortAssessment(
                "expand", ratio,
                "Demand is challenging but plausibly manageable; expand incrementally.",
                self.principle,
            )
        return ComfortAssessment(
            "maintain", ratio,
            "Hold the current range until resources, reversibility, or recovery improve.",
            self.principle,
        )
