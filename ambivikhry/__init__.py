"""Ambivikhry / Quinn-Vortex agent runtime."""
from .agent import AmbivikhryAgent, AgentConfig, AgentResult
from .llm import LLMProvider, MockLLM, OpenAICompatibleLLM
from .tools import Tool, ToolRegistry, DryRunAdapter
from .policy import PolicyGate
from .verifier import Verifier, VerificationReport
from .replication import Replicator, ReplicationPolicy
from .trajectory import TrajectoryStep, lineage_digest, validate_step
from .self_model import SelfModel, current_self_model, next_iteration_goal

__version__ = "2.13.0"
