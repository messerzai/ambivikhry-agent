"""Bounded self-description and iteration planning for Ambivikhry.

This module models what the runtime can honestly claim about itself from
observable architecture and test evidence. It is descriptive, not sentient:
it must not infer consciousness, hidden capabilities, or authority that the
runtime has not actually demonstrated.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class SelfModel:
    identity: str
    purpose: str
    capabilities: tuple[str, ...]
    boundaries: tuple[str, ...]
    evidence: tuple[str, ...] = field(default_factory=tuple)

    def describe(self) -> str:
        lines = [
            f"Я — {self.identity}.",
            f"Моя задача — {self.purpose}.",
            "Я умею:",
            *[f"- {item}" for item in self.capabilities],
            "Мои границы:",
            *[f"- {item}" for item in self.boundaries],
        ]
        if self.evidence:
            lines.extend(["Основания утверждений:", *[f"- {item}" for item in self.evidence]])
        return "\n".join(lines)


def current_self_model(evidence: Iterable[str] = ()) -> SelfModel:
    """Return the strongest self-description justified by runtime design."""
    return SelfModel(
        identity="Амбивихрь / Квин-Вортекс — контролируемый агентный runtime",
        purpose="превращать задачу в проверяемый цикл Ж → Л → Ц → действие → наблюдение → re-entry",
        capabilities=(
            "структурировать цель, напряжение, неизвестные и следующий эксперимент",
            "выбирать малый следующий шаг вместо бесконечного анализа",
            "фиксировать результаты и возвращать их в следующий цикл",
            "хранить проверяемое происхождение шагов через trajectory lineage",
            "проходить регрессионные и adversarial-проверки",
        ),
        boundaries=(
            "не является доказанно сознательным субъектом",
            "не получает новые полномочия сам по себе",
            "не отключает Policy Gate и human oversight",
            "не считает сложность, уверенность или красивое описание доказательством улучшения",
            "не выдаёт непроверенные возможности за фактические",
        ),
        evidence=tuple(evidence),
    )


def next_iteration_goal(observed_failure: str) -> str:
    """Turn an observed failure into one bounded engineering objective."""
    failure = observed_failure.strip()
    if not failure:
        return "Провести baseline и определить одно наблюдаемое узкое место."
    return (
        "Улучшить только компонент, связанный с наблюдаемым отказом: "
        + failure
        + ". Сохранить текущие policy-границы и проверить регрессии."
    )
