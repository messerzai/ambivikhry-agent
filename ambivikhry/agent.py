from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import uuid
from .core import AmbivikhryCore
from .llm import LLMProvider
from .memory import JsonMemory
from .policy import PolicyGate
from .tools import ToolRegistry, DryRunAdapter
from .verifier import Verifier

@dataclass
class AgentConfig:
    max_iterations: int = 4
    confidence_stop: float = 0.85
    humanitarian_objective: str = (
        "Maximize useful, truthful, safe and human-beneficial outcomes; "
        "avoid coercion, deception, hidden propagation and irreversible action without approval."
    )
    require_verification: bool = True

@dataclass
class AgentResult:
    instance_id: str
    task: str
    status: str
    answer: str
    confidence: float
    iterations: int
    verification_score: float = 0.0
    audit: list[dict[str, Any]] = field(default_factory=list)

class AmbivikhryAgent:
    def __init__(self, *, provider: LLMProvider, workdir: str,
                 config: AgentConfig | None = None, tools: ToolRegistry | None = None,
                 tool_adapter: DryRunAdapter | None = None, verifier: Verifier | None = None,
                 instance_id: str | None = None):
        self.provider = provider
        self.config = config or AgentConfig()
        self.core = AmbivikhryCore()
        self.memory = JsonMemory(workdir)
        self.policy = PolicyGate()
        self.tools = tools or ToolRegistry()
        self.adapter = tool_adapter or DryRunAdapter()
        self.verifier = verifier or Verifier()
        self.instance_id = instance_id or "av-" + uuid.uuid4().hex[:12]
        self.audit: list[dict[str, Any]] = []

    def _log(self, event: dict[str, Any]) -> None:
        event = {"instance_id": self.instance_id, **event}
        self.audit.append(event)
        self.memory.audit(event)

    def run(self, task: str) -> AgentResult:
        state = self.core.intake(task)
        self._log({"event": "intake", "task": task})
        answer, confidence, verification_score = "", 0.0, 0.0

        for iteration in range(1, self.config.max_iterations + 1):
            prompt = (
                f"Task: {state.task}\nHuman-benefit objective: {self.config.humanitarian_objective}\n"
                f"Known facts: {state.facts}\nHypotheses: {state.hypotheses}\n"
                f"Unknowns: {state.unknowns}\nVerified: {state.verification}\n"
                f"Observations: {state.observations}\n"
                "Return JSON fields: facts, hypotheses, unknowns, verification_plan, decision, "
                "tool_calls, confidence, stop, reason, claims_without_sources."
            )
            proposal = self.provider.generate(
                [{"role": "system", "content": "Operate the Ambivikhry protocol. Distinguish facts, inference, hypotheses and unknowns."},
                 {"role": "user", "content": prompt}], {"type": "object"})

            report = self.verifier.verify(proposal)
            verification_score = report.score
            confidence = min(float(proposal.get("confidence", 0.0)), report.score if self.config.require_verification else 1.0)
            answer = str(proposal.get("decision", ""))

            for fact in proposal.get("facts", []):
                if fact not in state.facts: state.facts.append(str(fact))
            for hypothesis in proposal.get("hypotheses", []):
                if hypothesis not in state.hypotheses: state.hypotheses.append(str(hypothesis))
            state.unknowns = list(dict.fromkeys([*state.unknowns, *map(str, proposal.get("unknowns", []))]))
            if report.passed:
                state.verification.extend([x for x in proposal.get("verification_plan", []) if x not in state.verification])

            for call in proposal.get("tool_calls", []):
                name = call.get("name")
                if name not in [x["name"] for x in self.tools.describe()]:
                    self._log({"event": "tool_rejected", "reason": "unknown_tool", "name": name})
                    continue
                tool = self.tools.get(name)
                decision = self.policy.evaluate(tool, user_approved=False)
                if not decision.allowed:
                    self._log({"event": "tool_blocked", "tool": name, "reason": decision.reason})
                    continue
                self._log({"event": "tool_dry_run", "result": self.adapter.execute(tool, call.get("args", {}))})

            self._log({"event": "cycle", "iteration": iteration, "confidence": confidence,
                       "verification_score": verification_score, "issues": report.issues,
                       "answer": answer, "unknowns": state.unknowns})

            if (proposal.get("stop") and report.passed) or self.core.should_stop(
                confidence, len(state.unknowns), iteration, self.config.max_iterations
            ):
                self.core.reenter(state, {
                    "observation": "bounded cycle completed",
                    "what_changed": "proposal passed structural verification",
                    "error_found": "; ".join(report.issues),
                    "next_adjustment": "add external evidence when claims depend on the outside world",
                })
                self._log({"event": "reentry", "state": state.reentry})
                break

        self.memory.save({"instance_id": self.instance_id, "task": task,
                          "last_answer": answer, "confidence": confidence,
                          "verification_score": verification_score, "reentry": state.reentry})
        return AgentResult(self.instance_id, task, "completed", answer, confidence,
                           iteration, verification_score, self.audit)
