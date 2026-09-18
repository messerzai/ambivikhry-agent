from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
import time

@dataclass
class AutonomyConfig:
    max_cycles: int = 8
    max_tool_calls_per_cycle: int = 4
    require_approval_for_irreversible: bool = True
    idle_sleep_seconds: float = 0.0

@dataclass
class AutonomyEvent:
    cycle: int
    kind: str
    data: dict[str, Any] = field(default_factory=dict)

class AutonomousController:
    """Bounded autonomy controller.

    It can continue useful work without a new user message, but it cannot
    silently widen permissions, self-install, propagate over a network, or
    execute irreversible actions without the configured approval boundary.
    """
    def __init__(self, config: AutonomyConfig | None = None):
        self.config = config or AutonomyConfig()
        self.events: list[AutonomyEvent] = []

    def run(self, step: Callable[[int], dict[str, Any]]) -> list[AutonomyEvent]:
        for cycle in range(1, self.config.max_cycles + 1):
            result = step(cycle) or {}
            event = AutonomyEvent(cycle, str(result.get("kind", "cycle")), result)
            self.events.append(event)
            if result.get("stop") is True:
                break
            if self.config.idle_sleep_seconds:
                time.sleep(self.config.idle_sleep_seconds)
        return self.events
