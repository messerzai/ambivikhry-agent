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
    cycle_index: int = 0


class AmbivikhryCore:
    """Operational form of the Ambivikhry protocol.

    The core deliberately keeps identity-like concepts operational: they are
    state variables and control rules, not claims about consciousness.
    """

    def intake(self, task: str) -> CycleState:
        task = task.strip()
        return CycleState(
            task=task,
            center={"known": [], "unknown": [], "change_conditions": []},
        )

    def anti_drift(self, state: CycleState) -> dict[str, Any]:
        return {
            "facts": list(state.facts),
            "inferences": list(state.hypotheses),
            "unknowns": list(state.unknowns),
            "verified": list(state.verification),
        }

    def score(self, *, relevance: float, reliability: float,
              verifiability: float, usefulness: float) -> float:
        return math.prod(max(0.0, min(1.0, x)) for x in
                         (relevance, reliability, verifiability, usefulness))

    def should_stop(self, confidence: float, remaining_unknowns: int,
                    iteration: int, max_iterations: int,
                    confidence_stop: float = 0.85) -> bool:
        """Stop only at an explicit bounded condition.

        A caller can tune the confidence threshold without silently changing
        the protocol's safety boundary. Unknowns prevent confidence-based
        early stopping, while max_iterations remains an unconditional bound.
        """
        if iteration >= max_iterations:
            return True
        return confidence >= confidence_stop and remaining_unknowns <= 1

    def reenter(self, state: CycleState, result: dict[str, Any]) -> None:
        state.cycle_index += 1
        observation = str(result.get("observation", "")).strip()
        if observation:
            state.observations.append(observation)
        state.reentry = {
            "cycle_index": state.cycle_index,
            "what_changed": result.get("what_changed", ""),
            "error_found": result.get("error_found", ""),
            "next_adjustment": result.get("next_adjustment", ""),
        }
        state.center["change_conditions"] = list(dict.fromkeys(
            [*state.center.get("change_conditions", []),
             str(result.get("next_adjustment", ""))]
        ))
