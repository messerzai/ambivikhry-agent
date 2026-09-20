from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable
import json

from .self_improvement_lab import (
    Evaluation,
    ImprovementDecision,
    ImprovementProposal as EvidenceProposal,
    SelfImprovementLab,
)


@dataclass
class ImprovementProposal:
    title: str
    hypothesis: str
    expected_benefit: str
    metric: str
    test_plan: list[str]
    risk: str = "low"
    mutation: dict[str, Any] | None = None


class SelfImprovementLoop:
    """Propose changes and gate adoption on measurable evidence.

    Legacy proposal ranking is retained for compatibility. New changes should
    use evaluate_change(), which compares baseline and candidate behavior and
    rejects regressions.
    """

    def __init__(self, evaluator: Callable[[ImprovementProposal], float]):
        self.evaluator = evaluator
        self.history: list[dict[str, Any]] = []

    def evaluate(self, proposal: ImprovementProposal) -> dict[str, Any]:
        score = float(self.evaluator(proposal))
        record = {**asdict(proposal), "score": score}
        self.history.append(record)
        return record

    def rank(self) -> list[dict[str, Any]]:
        return sorted(self.history, key=lambda x: x["score"], reverse=True)

    def evaluate_change(
        self,
        *,
        name: str,
        baseline: str,
        candidate: str,
        expected_gain: str,
        evaluator: Callable[[str], Evaluation],
        min_delta: float = 0.0,
    ) -> ImprovementDecision:
        lab = SelfImprovementLab(evaluator, min_delta=min_delta)
        decision = lab.evaluate(
            EvidenceProposal(
                name=name,
                baseline=baseline,
                candidate=candidate,
                expected_gain=expected_gain,
            )
        )
        self.history.append(
            {
                "title": name,
                "baseline": baseline,
                "candidate": candidate,
                "expected_benefit": expected_gain,
                "accepted": decision.accepted,
                "reason": decision.reason,
                "delta": decision.delta,
            }
        )
        return decision

    def export_report(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"proposals": self.rank()}, f, ensure_ascii=False, indent=2)
