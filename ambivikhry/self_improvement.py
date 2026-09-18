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


@dataclass
class RegressionMemory:
    """A fixed failure/constraint that future candidates must not break."""

    name: str
    metric: str
    baseline: float
    tolerance: float = 0.0
    notes: str = ""

    def passes(self, value: float) -> bool:
        return float(value) >= self.baseline - self.tolerance


class SelfImprovementLoop:
    """Generate, test and rank proposals without self-authorizing deployment.

    The evaluator is treated as an external authority. Proposals may be improved
    repeatedly, but adoption remains outside this class.
    """

    def __init__(self, evaluator: Callable[[ImprovementProposal], float]):
        self.evaluator = evaluator
        self.history: list[dict[str, Any]] = []
        self.regression_memory: list[RegressionMemory] = []

    def remember_regression(self, name: str, metric: str, baseline: float, *, tolerance: float = 0.0, notes: str = "") -> RegressionMemory:
        memory = RegressionMemory(name, metric, float(baseline), float(tolerance), notes)
        self.regression_memory.append(memory)
        return memory

    def evaluate(self, proposal: ImprovementProposal) -> dict[str, Any]:
        score = float(self.evaluator(proposal))
        record = {**asdict(proposal), "score": score}
        self.history.append(record)
        return record

    def evaluate_with_regressions(
        self,
        proposal: ImprovementProposal,
        regression_values: dict[str, float],
    ) -> dict[str, Any]:
        result = self.evaluate(proposal)
        checks = []
        for memory in self.regression_memory:
            value = regression_values.get(memory.metric)
            checks.append({
                "name": memory.name,
                "metric": memory.metric,
                "baseline": memory.baseline,
                "value": value,
                "passed": value is not None and memory.passes(value),
            })
        result["regressions"] = checks
        result["gate_passed"] = all(item["passed"] for item in checks)
        return result

    def rank(self) -> list[dict[str, Any]]:
        return sorted(self.history, key=lambda x: x["score"], reverse=True)

    def export_report(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "proposals": self.rank(),
                    "regression_memory": [asdict(x) for x in self.regression_memory],
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
