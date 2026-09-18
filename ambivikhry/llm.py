from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, messages: list[dict[str, str]], schema: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

class MockLLM(LLMProvider):
    """Deterministic local provider; no network access."""
    def generate(self, messages, schema):
        task = messages[-1]["content"] if messages else ""
        return {
            "hunger_plan": ["identify the task", "list candidate approaches"],
            "conflict": ["separate facts from assumptions"],
            "unknowns": ["external evidence may be required"],
            "verification_plan": ["verify critical claims before acting"],
            "decision": f"Draft a bounded next step for: {task[:300]}",
            "tool_calls": [], "confidence": 0.55, "stop": True,
            "reason": "Mock provider: no external execution configured."
        }
