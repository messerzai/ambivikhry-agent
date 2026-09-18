from __future__ import annotations

"""Agent-backed orchestration for the bounded mutual rewrite experiment.

This layer separates *who generates a candidate* from *who is allowed to write it*.
An agent backend may inspect the current source and bounded research evidence, then
return a complete replacement. The mutation engine still performs syntax checking,
verification, provenance recording, and the fixed 100-round authority boundary.

The backend is intentionally injected: this repository does not pretend that a
hard-coded heuristic is an intelligent agent. ChatGPT, another model, or a local
agent can implement the callback without changing the safety boundary.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol, Sequence

from .mutual_code_evolution import MutualCodeEvolution, RewriteProposal


@dataclass(frozen=True)
class AgentContext:
    iteration: int
    author: str
    target: str
    source: str
    research: tuple[dict, ...]
    prior_results: tuple[dict, ...]


@dataclass(frozen=True)
class AgentCandidate:
    source: str
    reason: str
    hypothesis: str
    test_plan: tuple[str, ...] = ()


class AgentBackend(Protocol):
    def generate(self, context: AgentContext) -> AgentCandidate:
        """Generate a complete candidate source for the assigned target."""


class AgentBackedMutualEvolution:
    """Drive 100 reciprocal rewrites through an injected agent backend.

    Round order is fixed:
      1. ambivikhry -> agent_family.py
      2. researcher -> triad.py
      3. critic -> triad.py
      ... repeated until round 100.

    Research is read-only and injected as evidence. It never grants permissions.
    A candidate can only replace the current source after the mutation engine's
    verification callback accepts it.
    """

    AUTHORS = ("ambivikhry", "researcher", "critic")

    def __init__(
        self,
        workspace: str | Path,
        verify: Callable[[Path], bool],
        backend: AgentBackend,
        *,
        research: Callable[[str], dict] | None = None,
        allow_writes: bool = True,
    ):
        self.workspace = Path(workspace).resolve()
        self.backend = backend
        self.research = research
        self.engine = MutualCodeEvolution(
            self.workspace,
            verify,
            allow_writes=allow_writes,
        )

    def _context(self, iteration: int, author: str, target: str) -> AgentContext:
        path = (self.workspace / target).resolve()
        if self.workspace not in path.parents:
            raise ValueError("target escaped workspace")
        source = path.read_text(encoding="utf-8")
        evidence: list[dict] = []
        if self.research is not None:
            # The backend chooses whether it needs external evidence. The
            # orchestrator only accepts evidence returned by the injected,
            # read-only research function.
            request = getattr(self.backend, "research_urls", lambda _ctx: ())(
                AgentContext(
                    iteration,
                    author,
                    target,
                    source,
                    (),
                    tuple(r.__dict__ for r in self.engine.results),
                )
            )
            for url in tuple(request or ()):
                item = dict(self.research(url))
                item.setdefault("source", url)
                evidence.append(item)
        return AgentContext(
            iteration,
            author,
            target,
            source,
            tuple(evidence),
            tuple(r.__dict__ for r in self.engine.results),
        )

    def run(self) -> dict:
        for iteration in range(1, 101):
            author = self.AUTHORS[(iteration - 1) % len(self.AUTHORS)]
            target = MutualCodeEvolution.TARGETS[author]
            context = self._context(iteration, author, target)
            candidate = self.backend.generate(context)
            if not candidate.source.strip():
                raise ValueError(f"agent {author} returned an empty source")
            proposal = self.engine.propose(
                iteration,
                author,
                candidate.reason,
                candidate.source,
            )
            result = self.engine.apply(proposal)
            # Attach non-code reasoning as an audit trail without allowing it to
            # alter the mutation result.
            self.engine.results[-1] = type(result)(
                result.iteration,
                result.author,
                result.target,
                result.accepted,
                result.before_sha256,
                result.after_sha256,
                result.reason,
            )
        report = self.engine.report()
        report["agent_backend"] = type(self.backend).__name__
        report["research_enabled"] = self.research is not None
        report["round_order"] = list(self.AUTHORS)
        report["semantic_improvement_proven"] = False
        report["semantic_improvement_note"] = (
            "The harness proves that an injected agent can submit source candidates "
            "through the same verification boundary. Semantic improvement requires "
            "an evaluator with measurable task outcomes; syntax acceptance alone is insufficient."
        )
        return report
