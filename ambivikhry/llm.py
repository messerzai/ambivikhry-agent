from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
import json
import os
from urllib.request import Request, urlopen

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

class OpenAICompatibleLLM(LLMProvider):
    """Minimal dependency-free adapter for OpenAI-compatible chat APIs.

    Configure with AMBIVIKHRY_API_KEY, AMBIVIKHRY_BASE_URL and
    AMBIVIKHRY_MODEL. Secrets are read from the environment and never stored.
    """
    def __init__(self, api_key: str | None = None, base_url: str | None = None,
                 model: str | None = None, timeout: int = 60):
        self.api_key = api_key or os.environ.get("AMBIVIKHRY_API_KEY")
        self.base_url = (base_url or os.environ.get("AMBIVIKHRY_BASE_URL") or
                         "https://api.openai.com/v1").rstrip("/")
        self.model = model or os.environ.get("AMBIVIKHRY_MODEL")
        self.timeout = timeout
        if not self.api_key or not self.model:
            raise ValueError("Set AMBIVIKHRY_API_KEY and AMBIVIKHRY_MODEL")

    def generate(self, messages, schema):
        payload = {"model": self.model, "messages": messages, "temperature": 0.2}
        req = Request(self.base_url + "/chat/completions",
                      data=json.dumps(payload).encode(),
                      headers={"Authorization": f"Bearer {self.api_key}",
                               "Content-Type": "application/json"}, method="POST")
        with urlopen(req, timeout=self.timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError("Provider did not return JSON") from exc
