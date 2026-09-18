from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[..., Any]
    risk: str = "low"
    requires_approval: bool = False

class ToolRegistry:
    def __init__(self): self._tools: dict[str, Tool] = {}
    def register(self, tool: Tool) -> None:
        if tool.name in self._tools: raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool
    def get(self, name: str) -> Tool: return self._tools[name]
    def describe(self):
        return [{"name": t.name, "description": t.description, "risk": t.risk, "requires_approval": t.requires_approval} for t in self._tools.values()]

class DryRunAdapter:
    """Records requested actions without executing side effects."""
    def __init__(self): self.events = []
    def execute(self, tool: Tool, args: dict[str, Any], approved: bool = False):
        allowed = approved or (tool.risk == "low" and not tool.requires_approval)
        event = {"tool": tool.name, "args": args, "executed": False, "allowed": allowed, "mode": "dry-run"}
        self.events.append(event)
        return event
