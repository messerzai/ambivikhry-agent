"""Bounded Occam's Razor tool.

The tool is a methodological preference, not a truth oracle: among candidates
that meet the same required constraints and explanatory score, prefer the one
with fewer assumptions/greater simplicity. It never overrides PolicyGate.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Hypothesis:
    name: str
    fit: float
    complexity: float
    assumptions: int = 0

    def validate(self) -> None:
        if not self.name:
            raise ValueError("name must be non-empty")
        if not 0.0 <= self.fit <= 1.0:
            raise ValueError("fit must be in [0, 1]")
        if not 0.0 <= self.complexity <= 1.0:
            raise ValueError("complexity must be in [0, 1]")
        if self.assumptions < 0:
            raise ValueError("assumptions must be non-negative")


class OccamsRazor:
    """Prefer simpler hypotheses only after adequacy is established."""

    def rank(self, hypotheses: Iterable[Hypothesis], *, min_fit: float = 0.7) -> list[Hypothesis]:
        items = list(hypotheses)
        for item in items:
            item.validate()
        if not 0.0 <= min_fit <= 1.0:
            raise ValueError("min_fit must be in [0, 1]")

        adequate = [item for item in items if item.fit >= min_fit]
        return sorted(
            adequate,
            key=lambda item: (item.complexity, item.assumptions, -item.fit),
        )

    def select(self, hypotheses: Iterable[Hypothesis], *, min_fit: float = 0.7) -> Hypothesis:
        ranked = self.rank(hypotheses, min_fit=min_fit)
        if not ranked:
            raise ValueError("no hypothesis meets the minimum fit")
        return ranked[0]
