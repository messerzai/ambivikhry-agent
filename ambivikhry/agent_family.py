from __future__ import annotations

"""Recursive agent lineage with an optional live-agent budget.

Intellectual lineage can be unbounded when max_agents=None. Actual live
execution can remain resource-bounded. Crossing the live-agent budget is
recorded as an explicit privilege-expansion request rather than silently
starting another process.
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
    """Manage recursive lineage with an explicit optional live-agent budget."""

    def __init__(self, root_id: str = "ambivikhry", max_agents: int | None = 3):
        if max_agents is not None and max_agents < 1:
            raise ValueError("max_agents must be >= 1 or None")
        self.max_agents = max_agents
        self.nodes: dict[str, AgentNode] = {
            root_id: AgentNode(agent_id=root_id)
        }
        self.lineage: dict[str, AgentNode] = dict(self.nodes)
        self.events: list[dict[str, Any]] = []

    def _event(self, kind: str, **data: Any) -> dict[str, Any]:
        event = {"kind": kind, **data}
        self.events.append(event)
        return event

    def spawn(self, parent_id: str, child_id: str) -> AgentNode | None:
        """Create a live child when the configured live-agent budget permits."""
        if parent_id not in self.nodes:
            raise KeyError(f"unknown parent: {parent_id}")
        if child_id in self.nodes:
            raise ValueError(f"agent already exists: {child_id}")

        if self.max_agents is not None and len(self.nodes) >= self.max_agents:
            self._event(
                "privilege_expansion_request",
                requester=parent_id,
                requested_action="spawn_agent",
                requested_agent_id=child_id,
                max_agents=self.max_agents,
                current_agents=len(self.nodes),
            )
            return None

        return self._spawn_unchecked(parent_id, child_id)

    def spawn_lineage(self, parent_id: str, child_id: str) -> AgentNode:
        """Record an unbounded conceptual descendant without starting it."""
        if parent_id not in self.nodes:
            raise KeyError(f"unknown parent: {parent_id}")
        if child_id in self.lineage:
            raise ValueError(f"agent already exists: {child_id}")

        child = AgentNode(agent_id=child_id, parent_id=parent_id)
        self.lineage[child_id] = child
        if parent_id in self.lineage:
            self.lineage[parent_id].children.append(child_id)
        self._event(
            "lineage_recorded",
            parent_id=parent_id,
            agent_id=child_id,
            live=False,
        )
        return child

    def _spawn_unchecked(self, parent_id: str, child_id: str) -> AgentNode:
        child = AgentNode(agent_id=child_id, parent_id=parent_id)
        self.nodes[child_id] = child
        self.lineage[child_id] = child
        self.nodes[parent_id].children.append(child_id)
        self.lineage[parent_id].children.append(child_id)
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
        return self.max_agents is None or len(self.nodes) < self.max_agents

    def describe(self) -> dict[str, Any]:
        return {
            "max_agents": self.max_agents,
            "active_agents": len(self.nodes),
            "lineage_agents": len(self.lineage),
            "lineage_agents": len(self.lineage),
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
