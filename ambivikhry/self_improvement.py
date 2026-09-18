from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Callable
import json

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
    """Generate, test and rank improvement proposals without self-authorizing deployment.

    The agent may discover and propose changes. Adoption remains an explicit deployment
    boundary; arbitrary self-modification and privilege changes are intentionally absent.
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

    def export_report(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"proposals": self.rank()}, f, ensure_ascii=False, indent=2)
