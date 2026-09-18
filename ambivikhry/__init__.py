"""Ambivikhry / Quinn-Vortex agent."""
from .agent import AmbivikhryAgent, AgentConfig, AgentResult
from .core import AmbivikhryCore
from .llm import MockLLM, LLMProvider
from .tools import Tool, ToolRegistry, DryRunAdapter
from .replication import Replicator, ReplicationPolicy
__version__ = "2.5.0"
