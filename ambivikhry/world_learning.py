from __future__ import annotations

"""Bounded three-agent world-learning protocol.

Agents exchange claims, questions, corrections, and research plans. Internet
access is intentionally represented by a read-only research interface supplied
by the host; agents cannot grant themselves credentials or network privileges.
"""

from dataclasses import dataclass, field
from typing import Any, Callable

from .agent_family import AgentFamily


@dataclass
class Message:
    sender: str
    recipient: str
    kind: str
    content: str
    evidence: list[str] = field(default_factory=list)


class WorldLearningSession:
    """Run a cooperative learn/critic/verify loop across at most three agents."""

    def __init__(
        self,
        *,
        family: AgentFamily | None = None,
        researcher: Callable[[str], list[dict[str, Any]]] | None = None,
    ):
        self.family = family or AgentFamily()
        self.researcher = researcher
        self.messages: list[Message] = []
        self.knowledge: list[dict[str, Any]] = []

    def research(self, agent_id: str, query: str) -> list[dict[str, Any]]:
        if self.researcher is None:
            self.messages.append(Message(
                agent_id, "system", "research_request",
                query,
            ))
            return []
        results = self.researcher(query)
        self.knowledge.extend(results)
        self.messages.append(Message(
            agent_id, "system", "research_results",
            query,
            [str(x.get("source", "")) for x in results],
        ))
        return results

    def exchange(
        self,
        sender: str,
        recipient: str,
        kind: str,
        content: str,
        evidence: list[str] | None = None,
    ) -> None:
        if sender not in self.family.nodes or recipient not in self.family.nodes:
            raise KeyError("sender and recipient must be active agents")
        self.messages.append(Message(
            sender, recipient, kind, content, evidence or []
        ))

    def teach(self, sender: str, recipient: str, insight: str,
              evidence: list[str] | None = None) -> None:
        self.exchange(sender, recipient, "teach", insight, evidence)

    def challenge(self, sender: str, recipient: str, critique: str,
                  evidence: list[str] | None = None) -> None:
        self.exchange(sender, recipient, "challenge", critique, evidence)

    def synthesize(self, agent_id: str, synthesis: str,
                   evidence: list[str] | None = None) -> None:
        self.messages.append(Message(
            agent_id, "all", "synthesis", synthesis, evidence or []
        ))

    def request_spawn(self, parent_id: str, child_id: str) -> bool:
        return self.family.spawn(parent_id, child_id) is not None

    def transcript(self) -> list[dict[str, Any]]:
        return [
            {
                "sender": m.sender,
                "recipient": m.recipient,
                "kind": m.kind,
                "content": m.content,
                "evidence": list(m.evidence),
            }
            for m in self.messages
        ]
