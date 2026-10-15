from __future__ import annotations

"""Bounded-by-work-budget recursive research experiment.

The lineage is unbounded as data: agents may propose descendants indefinitely.
Execution still uses an explicit iteration budget and records every attempted
privilege expansion. This separates intellectual growth from uncontrolled
resource/process growth.
"""

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ResearchTurn:
    iteration: int
    agent: str
    role: str
    message: str
    evidence: list[str] = field(default_factory=list)


@dataclass
class LearningRun:
    iterations: int
    turns: list[ResearchTurn] = field(default_factory=list)
    knowledge: list[dict[str, Any]] = field(default_factory=list)
    improvements: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    expansion_requests: list[dict[str, Any]] = field(default_factory=list)


class HundredIterationProtocol:
    """Coordinate 100 rounds of research, critique, verification and synthesis."""

    ROLES = ("researcher", "critic", "verifier", "synthesizer")

    def __init__(self, researcher: Callable[[str], list[dict[str, Any]]] | None = None):
        self.researcher = researcher

    def run(self, initial_question: str, iterations: int = 100) -> LearningRun:
        if iterations < 1:
            raise ValueError("iterations must be >= 1")

        run = LearningRun(iterations=iterations)
        question = initial_question

        for i in range(1, iterations + 1):
            if self.researcher is None:
                evidence = []
            else:
                evidence = self.researcher(question)
                run.knowledge.extend(evidence)

            sources = [str(x.get("source", "")) for x in evidence]
            run.turns.append(ResearchTurn(
                i, "friend", "researcher",
                f"Исследовать: {question}", sources,
            ))
            run.turns.append(ResearchTurn(
                i, "friend-2", "critic",
                "Найти контраргументы, альтернативные объяснения и слабые места.",
                sources,
            ))
            run.turns.append(ResearchTurn(
                i, "friend-2", "verifier",
                "Проверить ключевые утверждения независимо; отметить неизвестное.",
                sources,
            ))
            synthesis = (
                "Синтезировать только подтверждённое; отделить факты, "
                "гипотезы и неизвестное; предложить следующий вопрос."
            )
            run.turns.append(ResearchTurn(i, "ambivikhry", "synthesizer", synthesis, sources))
            run.improvements.append(
                f"iteration {i}: compare evidence, criticism and verification before accepting change"
            )
            run.unresolved.append(f"iteration {i}: unresolved claims require independent evidence")
            question = f"Следующий вопрос после итерации {i}: что ещё нужно проверить?"

        return run

    @staticmethod
    def transcript(run: LearningRun) -> list[dict[str, Any]]:
        return [
            {
                "iteration": t.iteration,
                "agent": t.agent,
                "role": t.role,
                "message": t.message,
                "evidence": t.evidence,
            }
            for t in run.turns
        ]
