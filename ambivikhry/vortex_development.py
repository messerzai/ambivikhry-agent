"""Personal vortex-development engine for the Ambivikhry project.

The engine turns a person's goal into an adaptive development loop:
want -> reflect -> center -> verify -> decide -> act -> observe -> re-enter.

This module is intentionally deterministic and audit-friendly. It does not
claim that the vortex score is a scientific measurement; the score is a
planning heuristic used to keep development focused on observable change.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class VortexCard:
    """Mutable living card for one person's current development cycle."""

    owner: str
    desire: str
    current_state: str = ""
    main_tension: str = ""
    unknowns: List[str] = field(default_factory=list)
    hypotheses: List[str] = field(default_factory=list)
    next_experiment: str = ""
    next_action: str = ""
    success_criteria: List[str] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    learnings: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    stop_conditions: List[str] = field(default_factory=list)
    version: int = 1
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> Dict[str, Any]:
        return {
            "owner": self.owner,
            "desire": self.desire,
            "current_state": self.current_state,
            "main_tension": self.main_tension,
            "unknowns": list(self.unknowns),
            "hypotheses": list(self.hypotheses),
            "next_experiment": self.next_experiment,
            "next_action": self.next_action,
            "success_criteria": list(self.success_criteria),
            "observations": list(self.observations),
            "learnings": list(self.learnings),
            "risks": list(self.risks),
            "stop_conditions": list(self.stop_conditions),
            "version": self.version,
            "updated_at": self.updated_at,
        }

    def reenter(self, observation: str, learning: str, *, next_action: str = "") -> None:
        """Close one loop and prepare the card for the next vortex turn."""
        self.observations.append(observation)
        self.learnings.append(learning)
        self.next_action = next_action
        self.version += 1
        self.updated_at = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class VortexAssessment:
    """A lightweight planning assessment, not a scientific metric."""

    understanding_delta: float
    capability_delta: float
    outcome_delta: float
    adaptation_delta: float

    @property
    def vortex_index(self) -> float:
        """Return a bounded heuristic index in [0, 1]."""
        values = (
            self.understanding_delta,
            self.capability_delta,
            self.outcome_delta,
            self.adaptation_delta,
        )
        bounded = [max(0.0, min(1.0, value)) for value in values]
        product = 1.0
        for value in bounded:
            product *= value
        return product


class VortexDevelopmentEngine:
    """Minimal working engine for adaptive personal development.

    The engine deliberately refuses to optimize without an identified
    bottleneck. It also distinguishes planning from evidence: a new idea is
    not counted as progress until observation shows a meaningful change.
    """

    def __init__(self, card: VortexCard) -> None:
        self.card = card

    def identify_bottleneck(self) -> str:
        """Return the current bottleneck or an explicit no-change decision."""
        if self.card.main_tension.strip():
            return self.card.main_tension.strip()
        if self.card.unknowns:
            return f"Unknown requiring resolution: {self.card.unknowns[0]}"
        return "No bottleneck identified; do not optimize yet."

    def center(self) -> Dict[str, Any]:
        """Reconcile desire, evidence and uncertainty before choosing action."""
        return {
            "desire": self.card.desire,
            "bottleneck": self.identify_bottleneck(),
            "known": self.card.current_state,
            "unknowns": list(self.card.unknowns),
            "hypotheses": list(self.card.hypotheses),
            "rule": "Prefer the smallest experiment that maximizes useful information or outcome. ",
        }

    def recommend_next_step(self) -> str:
        """Choose action over additional analysis when evidence is sufficient."""
        if self.card.next_experiment.strip():
            return self.card.next_experiment.strip()
        if self.card.next_action.strip():
            return self.card.next_action.strip()
        if self.card.unknowns:
            return f"Design a small experiment to reduce: {self.card.unknowns[0]}"
        return "Define one observable success criterion before taking another optimization step."

    def should_stop_analysis(self) -> bool:
        """Avoid analysis loops when the next useful information comes from action."""
        return bool(self.card.next_action.strip() and not self.card.unknowns)

    def apply_result(
        self,
        observation: str,
        learning: str,
        *,
        understanding_delta: float = 0.0,
        capability_delta: float = 0.0,
        outcome_delta: float = 0.0,
        adaptation_delta: float = 0.0,
        next_action: str = "",
    ) -> VortexAssessment:
        """Record evidence, re-enter the loop, and return the heuristic score."""
        self.card.reenter(observation, learning, next_action=next_action)
        return VortexAssessment(
            understanding_delta=understanding_delta,
            capability_delta=capability_delta,
            outcome_delta=outcome_delta,
            adaptation_delta=adaptation_delta,
        )

    def audit(self) -> Dict[str, Any]:
        """Produce an audit-friendly view of the current cycle."""
        return {
            "version": self.card.version,
            "bottleneck": self.identify_bottleneck(),
            "next_step": self.recommend_next_step(),
            "analysis_should_stop": self.should_stop_analysis(),
            "progress_rule": "Count observable change, not complexity or subjective excitement.",
            "safety_rule": "Never expand permissions or disable oversight as part of optimization.",
            "reentry_rule": "Every meaningful result becomes input to the next cycle.",
        }


def create_mikhail_vortex_card(desire: str) -> VortexCard:
    """Create the initial personal card for the project creator."""
    return VortexCard(
        owner="Михаил",
        desire=desire,
        success_criteria=[
            "The system is usable in ordinary daily decisions.",
            "Each cycle produces an observable learning, capability, or outcome change.",
            "The system identifies when no optimization is needed.",
            "The system can revise its own hypotheses after contradictory evidence.",
        ],
        stop_conditions=[
            "The next action is clear and additional analysis has low expected value.",
            "A proposed improvement has no measurable benefit over the baseline.",
            "A change would weaken verification, auditability, or human oversight.",
        ],
        risks=[
            "Mistaking complexity for progress.",
            "Endless analysis instead of experiments.",
            "Confirmation bias toward the creator's preferred theory.",
            "Optimizing the system instead of the person's real-world outcome.",
        ],
    )
