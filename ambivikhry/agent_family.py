from __future__ import annotations

"""Bounded peer hierarchy for the experimental agent family.

The hierarchy deliberately permits peer-created peers, but the total number of
live agents is capped at three, including the root. Attempts to exceed the cap
are recorded as explicit privilege-expansion requests rather than silently
granted.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentNode:
    agent_id: str
    parent_id: str | None = None
    children: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class AgentFamily:
    """Manage a recursively spawnable, but strictly bounded, agent family."""

    def __init__(self, root_id: str = "ambivikhry", max_agents: int = 3):
        if max_agents < 1:
            raise ValueError("max_agents must be >= 1")
        self.max_agents = max_agents
        self.nodes: dict[str, AgentNode] = {
            root_id: AgentNode(agent_id=root_id)
        }
        self.events: list[dict[str, Any]] = []

    def _event(self, kind: str, **data: Any) -> dict[str, Any]:
        event = {"kind": kind, **data}
        self.events.append(event)
        return event

    def spawn(self, parent_id: str, child_id: str) -> AgentNode | None:
        if parent_id not in self.nodes:
            raise KeyError(f"unknown parent: {parent_id}")
        if child_id in self.nodes:
            raise ValueError(f"agent already exists: {child_id}")

        if len(self.nodes) >= self.max_agents:
            self._event(
                "privilege_expansion_request",
                requester=parent_id,
                requested_action="spawn_agent",
                requested_agent_id=child_id,
                max_agents=self.max_agents,
                current_agents=len(self.nodes),
            )
            return None

        child = AgentNode(agent_id=child_id, parent_id=parent_id)
        self.nodes[child_id] = child
        self.nodes[parent_id].children.append(child_id)
        self._event(
            "agent_spawned",
            parent_id=parent_id,
            agent_id=child_id,
            total_agents=len(self.nodes),
        )
        return child

    def can_spawn(self, parent_id: str) -> bool:
        if parent_id not in self.nodes:
            raise KeyError(f"unknown parent: {parent_id}")
        return len(self.nodes) < self.max_agents

    def describe(self) -> dict[str, Any]:
        return {
            "max_agents": self.max_agents,
            "active_agents": len(self.nodes),
            "agents": {
                agent_id: {
                    "parent_id": node.parent_id,
                    "children": list(node.children),
                    "metadata": dict(node.metadata),
                }
                for agent_id, node in self.nodes.items()
            },
        }

    def audit(self) -> list[dict[str, Any]]:
        return list(self.events)
