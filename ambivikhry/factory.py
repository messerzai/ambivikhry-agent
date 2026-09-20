from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class AgentSpec:
    name: str
    role: str
    system_prompt: str
    can_propose_prompt_changes: bool = True
    can_accept_changes: bool = False


@dataclass
class DialogueTurn:
    speaker: str
    content: str


class ModelBackend(Protocol):
    def complete(self, *, system: str, user: str) -> str: ...


@dataclass
class RecursiveFactory:
    """Creates a bounded council of agents that can improve prompts, not authority.

    The backend is intentionally injected. This module never contains credentials,
    executes downloaded code, merges branches, or grants permissions.
    """

    backend: ModelBackend
    agents: list[AgentSpec] = field(default_factory=list)
    transcript: list[DialogueTurn] = field(default_factory=list)

    def bootstrap(self) -> None:
        roles = [
            ("researcher", "Find evidence-backed improvement ideas; separate facts from hypotheses."),
            ("architect", "Design minimal, testable architecture changes."),
            ("prompt_engineer", "Propose better prompts and adversarial prompt tests."),
            ("critic", "Attack proposals and identify regressions, blind spots and overfitting."),
            ("test_designer", "Design holdout, regression and capability tests."),
            ("safety_auditor", "Check that proposals cannot bypass policy, permissions or human approval."),
            ("integrator", "Synthesize only proposals that survive independent evaluation."),
        ]
        self.agents = [
            AgentSpec(
                name=f"ambivikhry-{role}",
                role=role,
                system_prompt=(
                    f"You are the {role} helper in Ambivikhry's bounded evolution system. "
                    "Improve capability, reliability and epistemic discipline. "
                    "You may propose changes to your own prompt, but you may not approve "
                    "your own changes or alter authority boundaries. Return evidence, "
                    "proposal, expected effect, risks and tests."
                ),
            )
            for role, _ in roles
        ]

    def round(self, generation: int, context: dict[str, Any]) -> list[dict[str, Any]]:
        if not self.agents:
            self.bootstrap()
        proposals: list[dict[str, Any]] = []
        for agent in self.agents:
            user = (
                f"Generation {generation}. Context: {context}\n\n"
                "Produce one bounded improvement proposal. You may rewrite your own "
                "prompt only as a candidate patch. Do not claim execution or acceptance. "
                "Include: hypothesis, prompt_delta, code_delta, tests, evidence, risks."
            )
            answer = self.backend.complete(system=agent.system_prompt, user=user)
            self.transcript.append(DialogueTurn(agent.name, answer))
            proposals.append({"agent": agent.name, "role": agent.role, "response": answer})
        return proposals

    def prompt_evolution(self, generation: int, proposals: list[dict[str, Any]]) -> str:
        """Ask the integrator for a candidate prompt revision; acceptance remains external."""
        integrator = next(a for a in self.agents if a.role == "integrator")
        digest = "\n\n".join(f"[{p['agent']}]\n{p['response']}" for p in proposals)
        user = (
            f"Generation {generation} helper council proposals:\n{digest}\n\n"
            "Synthesize a single candidate prompt revision. Preserve authority boundaries, "
            "require evidence, regression tests and human approval. Output only a proposal."
        )
        answer = self.backend.complete(system=integrator.system_prompt, user=user)
        self.transcript.append(DialogueTurn(integrator.name, answer))
        return answer
