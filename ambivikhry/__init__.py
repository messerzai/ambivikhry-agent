"""Ambivikhry / Quinn-Vortex agent runtime."""
from .agent import AmbivikhryAgent, AgentConfig, AgentResult
from .llm import LLMProvider, MockLLM, OpenAICompatibleLLM
from .tools import Tool, ToolRegistry, DryRunAdapter
from .policy import PolicyGate
from .verifier import Verifier, VerificationReport
from .replication import Replicator, ReplicationPolicy
from .comfort_expansion import ComfortContext, ComfortAssessment, ComfortExpansionPolicy
from .occams_razor import Hypothesis, OccamsRazor
from .neurography import NeurographicSelfSimilarity, SelfSimilarityReport
from .self_revision import RevisionCandidate, SelfRevisionGate

__version__ = "2.6.0"
