from dataclasses import dataclass, field
from typing import Any
import math

@dataclass
class CycleState:
    task: str
    hunger: float = 0.5
    lilitemy: float = 0.5
    center: dict[str, Any] = field(default_factory=dict)
    facts: list[str] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    reentry: dict[str, Any] = field(default_factory=dict)

class AmbivikhryCore:
    """Operational form of the Ambivikhry protocol."""
    def intake(self, task: str) -> CycleState:
        # A generic placeholder is not an actual unknown. Keeping it out of
        # unknowns prevents false uncertainty from contaminating stop logic.
        return CycleState(task=task.strip(), center={"known": [], "unknown": [], "change_conditions": []})

    def anti_drift(self, state: CycleState) -> dict[str, Any]:
        return {"facts": list(state.facts), "inferences": list(state.hypotheses), "unknowns": list(state.unknowns), "verified": list(state.verification)}

    def score(self, *, relevance: float, reliability: float, verifiability: float, usefulness: float) -> float:
        return math.prod(max(0.0, min(1.0, x)) for x in (relevance, reliability, verifiability, usefulness))

    def should_stop(self, confidence: float, remaining_unknowns: int, iteration: int, max_iterations: int) -> bool:
        return iteration >= max_iterations or (confidence >= 0.85 and remaining_unknowns <= 1)

    def reenter(self, state: CycleState, result: dict[str, Any]) -> None:
        state.observations.append(str(result.get("observation", "")))
        state.reentry = {"what_changed": result.get("what_changed", ""), "error_found": result.get("error_found", ""), "next_adjustment": result.get("next_adjustment", "")}
