from __future__ import annotations

"""Agent-backed orchestration for bounded mutual source evolution."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol

from .mutual_code_evolution import MutualCodeEvolution, RewriteResult


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
    critique: str = ""


class AgentBackend(Protocol):
    def generate(self, context: AgentContext) -> AgentCandidate:
        """Generate a complete candidate source for the assigned target."""


class AgentBackedMutualEvolution:
    """Run 100 reciprocal rounds with research, critique, and evaluation gates."""

    AUTHORS = ("ambivikhry", "researcher", "critic")

    def __init__(
        self,
        workspace: str | Path,
        verify: Callable[[Path], bool],
        backend: AgentBackend,
        *,
        research: Callable[[str], dict] | None = None,
        critic: Callable[[AgentContext, AgentCandidate], dict] | None = None,
        evaluate: Callable[[Path, AgentCandidate], dict] | None = None,
        allow_writes: bool = True,
    ):
        self.workspace = Path(workspace).resolve()
        self.backend = backend
        self.research = research
        self.critic = critic
        self.evaluate = evaluate
        self.engine = MutualCodeEvolution(
            self.workspace, verify, allow_writes=allow_writes
        )
        self.audit: list[dict] = []

    def _context(self, iteration: int, author: str, target: str) -> AgentContext:
        path = (self.workspace / target).resolve()
        if self.workspace not in path.parents:
            raise ValueError("target escaped workspace")
        source = path.read_text(encoding="utf-8")
        evidence: list[dict] = []
        if self.research is not None:
            seed = AgentContext(
                iteration, author, target, source, (), tuple(r.__dict__ for r in self.engine.results)
            )
            urls = getattr(self.backend, "research_urls", lambda _ctx: ())(seed)
            for url in tuple(urls or ()):
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

    def _record_rejection(
        self, iteration: int, author: str, target: str, source: str, candidate: AgentCandidate, reason: str
    ) -> RewriteResult:
        result = RewriteResult(
            iteration, author, target, False,
            self.engine.digest(source), self.engine.digest(candidate.source), reason
        )
        self.engine.results.append(result)
        return result

    def run(self) -> dict:
        for iteration in range(1, 101):
            author = self.AUTHORS[(iteration - 1) % len(self.AUTHORS)]
            target = MutualCodeEvolution.TARGETS[author]
            context = self._context(iteration, author, target)
            candidate = self.backend.generate(context)

            if not candidate.source.strip():
                raise ValueError(f"agent {author} returned an empty source")

            critique = (
                self.critic(context, candidate)
                if self.critic is not None
                else {"passed": True, "notes": "critic not configured"}
            )
            if not critique.get("passed", False):
                result = self._record_rejection(
                    iteration, author, target, context.source, candidate, "critic_rejected"
                )
                self.audit.append({
                    "iteration": iteration, "author": author, "target": target,
                    "critique": critique, "evaluation": None, "accepted": result.accepted,
                    "reason": result.reason,
                })
                continue

            proposal = self.engine.propose(iteration, author, candidate.reason, candidate.source)

            evaluation = (
                self.evaluate(self.workspace, candidate)
                if self.evaluate is not None
                else {"passed": True, "notes": "evaluator not configured"}
            )
            if not evaluation.get("passed", False):
                result = self._record_rejection(
                    iteration, author, target, context.source, candidate, "evaluation_failed"
                )
                self.audit.append({
                    "iteration": iteration, "author": author, "target": target,
                    "critique": critique, "evaluation": evaluation, "accepted": result.accepted,
                    "reason": result.reason,
                })
                continue

            result = self.engine.apply(proposal)
            self.audit.append({
                "iteration": iteration, "author": author, "target": target,
                "critique": critique, "evaluation": evaluation,
                "accepted": result.accepted, "reason": result.reason,
            })

        report = self.engine.report()
        report.update({
            "agent_backend": type(self.backend).__name__,
            "research_enabled": self.research is not None,
            "critic_enabled": self.critic is not None,
            "evaluator_enabled": self.evaluate is not None,
            "round_order": list(self.AUTHORS),
            "semantic_improvement_proven": bool(
                self.evaluate is not None and any(
                    item.get("accepted") and item.get("evaluation", {}).get("passed")
                    for item in self.audit
                )
            ),
            "audit": self.audit,
        })
        return report
