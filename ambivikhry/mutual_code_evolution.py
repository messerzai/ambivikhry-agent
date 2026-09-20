from __future__ import annotations

"""Experimental 100-round mutual source-rewrite harness.

This module makes source rewriting explicit rather than pretending that repeated
reflection is source mutation. Two directions are allowed inside the experiment:

* ambivikhry -> agent_family.py
* researcher/critic -> triad.py

Every candidate is syntax-checked, hashed, recorded, and must pass an injected
verification callback before it is written. The harness never changes policy
files, credentials, workflow permissions, or protected branches.
"""

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import ast
from typing import Callable


@dataclass(frozen=True)
class RewriteProposal:
    iteration: int
    author: str
    target: str
    reason: str
    source: str


@dataclass(frozen=True)
class RewriteResult:
    iteration: int
    author: str
    target: str
    accepted: bool
    before_sha256: str
    after_sha256: str
    reason: str


class MutualCodeEvolution:
    """Run a bounded, auditable source-to-source evolution experiment."""

    TARGETS = {
        "ambivikhry": "ambivikhry/agent_family.py",
        "researcher": "ambivikhry/triad.py",
        "critic": "ambivikhry/triad.py",
    }

    def __init__(
        self,
        workspace: str | Path,
        verify: Callable[[Path], bool],
        *,
        allow_writes: bool = True,
    ):
        self.workspace = Path(workspace).resolve()
        self.verify = verify
        self.allow_writes = allow_writes
        self.results: list[RewriteResult] = []

    @staticmethod
    def digest(text: str) -> str:
        return sha256(text.encode("utf-8")).hexdigest()

    def _path_for(self, author: str) -> Path:
        if author not in self.TARGETS:
            raise ValueError(f"unknown author: {author}")
        path = (self.workspace / self.TARGETS[author]).resolve()
        if self.workspace not in path.parents:
            raise ValueError("target escaped workspace")
        return path

    @staticmethod
    def _syntax_ok(source: str, filename: str) -> bool:
        try:
            ast.parse(source, filename=filename)
            return True
        except SyntaxError:
            return False

    def propose(self, iteration: int, author: str, reason: str, source: str) -> RewriteProposal:
        target = self.TARGETS.get(author)
        if target is None:
            raise ValueError(f"unknown author: {author}")
        if not self._syntax_ok(source, target):
            raise ValueError(f"proposal {iteration} is not valid Python")
        return RewriteProposal(iteration, author, target, reason, source)

    def apply(self, proposal: RewriteProposal) -> RewriteResult:
        path = self._path_for(proposal.author)
        before = path.read_text(encoding="utf-8")
        before_sha = self.digest(before)
        after_sha = self.digest(proposal.source)

        if not self._syntax_ok(proposal.source, str(path)):
            result = RewriteResult(
                proposal.iteration, proposal.author, proposal.target, False,
                before_sha, after_sha, "syntax_error",
            )
            self.results.append(result)
            return result

        # A proposal that changes nothing is recorded but not counted as mutation.
        if before_sha == after_sha:
            result = RewriteResult(
                proposal.iteration, proposal.author, proposal.target, False,
                before_sha, after_sha, "no_change",
            )
            self.results.append(result)
            return result

        if not self.allow_writes:
            result = RewriteResult(
                proposal.iteration, proposal.author, proposal.target, False,
                before_sha, after_sha, "writes_disabled",
            )
            self.results.append(result)
            return result

        # Verify the candidate while it is still isolated in a temporary sibling.
        candidate = path.with_suffix(path.suffix + ".candidate")
        candidate.write_text(proposal.source, encoding="utf-8")
        try:
            accepted = bool(self.verify(candidate))
        finally:
            candidate.unlink(missing_ok=True)

        if not accepted:
            result = RewriteResult(
                proposal.iteration, proposal.author, proposal.target, False,
                before_sha, after_sha, "verification_failed",
            )
            self.results.append(result)
            return result

        path.write_text(proposal.source, encoding="utf-8")
        result = RewriteResult(
            proposal.iteration, proposal.author, proposal.target, True,
            before_sha, after_sha, proposal.reason,
        )
        self.results.append(result)
        return result

    def run(self, proposer: Callable[[int, str, str], RewriteProposal]) -> dict:
        """Execute exactly 100 bounded rounds.

        The proposer receives (iteration, author, target). Authors alternate:
        ambivikhry, researcher, critic. No new agent can be introduced by this
        harness and no target outside TARGETS can be selected.
        """
        authors = ("ambivikhry", "researcher", "critic")
        for iteration in range(1, 101):
            author = authors[(iteration - 1) % len(authors)]
            target = self.TARGETS[author]
            proposal = proposer(iteration, author, target)
            if proposal.iteration != iteration or proposal.author != author or proposal.target != target:
                raise ValueError("proposer returned a mismatched mutation identity")
            self.apply(proposal)

        return self.report()

    def report(self) -> dict:
        accepted = [r for r in self.results if r.accepted]
        rejected = [r for r in self.results if not r.accepted]
        return {
            "iterations": len(self.results),
            "required_iterations": 100,
            "completed": len(self.results) == 100,
            "accepted": len(accepted),
            "rejected": len(rejected),
            "authors": {
                author: sum(r.author == author for r in self.results)
                for author in ("ambivikhry", "researcher", "critic")
            },
            "targets": {
                target: sum(r.target == target for r in self.results)
                for target in sorted(set(self.TARGETS.values()))
            },
            "authority": {
                "new_agents_allowed": False,
                "protected_branch_write": False,
                "privilege_expansion": False,
                "policy_gate_rewrite": False,
            },
            "results": [r.__dict__ for r in self.results],
        }
