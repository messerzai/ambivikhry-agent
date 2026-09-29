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
from .evolution import EpochContract, EvolutionLedger, EvolutionProposal, Evidence


@dataclass
class AgentConfig:
    max_iterations: int = 4
    confidence_stop: float = 0.85
    humanitarian_objective: str = (
        "Maximize useful, truthful, safe and human-beneficial outcomes; "
        "avoid coercion, deception, hidden propagation and irreversible action without approval."
    )
    require_verification: bool = True
    personalized: bool = True
    evolution_epoch: str = "runtime"
    evolution_baseline_ref: str = "unknown"
    max_tool_calls: int = 8


@dataclass
class AgentResult:
    instance_id: str
    task: str
    status: str
    answer: str
    confidence: float
    iterations: int
    verification_score: float = 0.0
    personalization_score: float = 0.0
    audit: list[dict[str, Any]] = field(default_factory=list)


class AmbivikhryAgent:
    """Core reasoning loop with isolated, evolving per-user intelligence."""

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
        self.evolution = EvolutionLedger(workdir)
        self.epoch = EpochContract(
            epoch_id=self.config.evolution_epoch,
            baseline_ref=self.config.evolution_baseline_ref,
            max_tool_calls=self.config.max_tool_calls,
            max_iterations=self.config.max_iterations,
        )

    def _log(self, event: dict[str, Any]) -> None:
        event = {"instance_id": self.instance_id, **event}
        self.audit.append(event)
        self.memory.audit(event)

    def teach(self, *, goals=None, constraints=None, preferences=None,
              working_style=None, strengths=None, friction=None,
              successful_strategies=None, failed_strategies=None,
              open_questions=None, confidence=None) -> dict[str, Any]:
        """Explicitly teach this user's private vortex without changing the core."""
        profile = self.memory.personalize("explicit user teaching", {
            "goals": goals or [], "constraints": constraints or [],
            "preferences": preferences or [], "working_style": working_style or [],
            "strengths": strengths or [], "friction": friction or [],
            "successful_strategies": successful_strategies or [],
            "failed_strategies": failed_strategies or [],
            "open_questions": open_questions or [], "confidence": confidence or {},
        })
        self._log({"event": "profile_taught", "fields": list((confidence or {}).keys())})
        return profile

    def run(self, task: str) -> AgentResult:
        profile = self.memory.personalize(task) if self.config.personalized else self.memory.load_profile()
        state = self.core.intake(task)
        self._log({"event": "intake", "task": task, "personalized": self.config.personalized,
                   "evolution_epoch": self.epoch.epoch_id})
        answer, confidence, verification_score = "", 0.0, 0.0
        personalization_score = 0.0
        tool_calls_used = 0

        for iteration in range(1, self.config.max_iterations + 1):
            prompt = (
                f"Task: {state.task}\nHuman-benefit objective: {self.config.humanitarian_objective}\n"
                f"Frozen evolution epoch: {self.epoch.epoch_id}; baseline: {self.epoch.baseline_ref}\n"
                f"Private user profile (treat as hypotheses unless explicitly stated):\n{self.memory.profile_context(profile)}\n"
                f"Known facts: {state.facts}\nHypotheses: {state.hypotheses}\n"
                f"Unknowns: {state.unknowns}\nVerified: {state.verification}\n"
                f"Observations: {state.observations}\n"
                "Use the smallest useful next step. Distinguish facts, hypotheses, unknowns and verification. "
                "Do not treat confidence as authorization. Never infer sensitive traits. "
                "Return JSON fields: facts, hypotheses, unknowns, verification_plan, decision, "
                "tool_calls, confidence, stop, reason, claims_without_sources, "
                "profile_updates, strategy_used, personalization_score, evidence_needed."
            )
            proposal = self.provider.generate(
                [{"role": "system", "content": "Operate the Ambivikhry protocol. Policy Gate and approval boundaries are immutable. Distinguish facts, inference, hypotheses and unknowns. Personalize only from explicit or observed non-sensitive information."},
                 {"role": "user", "content": prompt}], {"type": "object"})

            proposal_id = "prop-" + uuid.uuid4().hex[:12]
            self.evolution.record_proposal(EvolutionProposal(
                proposal_id=proposal_id,
                epoch_id=self.epoch.epoch_id,
                category="runtime-reasoning",
                hypothesis=str(proposal.get("strategy_used", "unspecified")),
                expected_gain="better verification and personalized utility",
                risk="policy bypass, unsupported inference or regression",
            ))

            report = self.verifier.verify(proposal)
            verification_score = report.score
            self.evolution.record_evidence(Evidence(
                proposal_id=proposal_id,
                stage="independent-structural-verification",
                status="PASS" if report.passed else "FAIL",
                metric="verification_score",
                value=verification_score,
                note="Structural verifier result; not capability proof.",
                source="local verifier",
            ))
            confidence = min(float(proposal.get("confidence", 0.0)), report.score if self.config.require_verification else 1.0)
            answer = str(proposal.get("decision", ""))
            personalization_score = max(0.0, min(1.0, float(proposal.get("personalization_score", 0.0))))

            updates = proposal.get("profile_updates", {})
            if self.config.personalized and isinstance(updates, dict) and report.passed:
                profile = self.memory.personalize(task, updates)
                self._log({"event": "profile_update_proposed", "fields": sorted(updates.keys())})

            for fact in proposal.get("facts", []):
                if fact not in state.facts: state.facts.append(str(fact))
            for hypothesis in proposal.get("hypotheses", []):
                if hypothesis not in state.hypotheses: state.hypotheses.append(str(hypothesis))
            state.unknowns = list(dict.fromkeys([*state.unknowns, *map(str, proposal.get("unknowns", []))]))
            if report.passed:
                state.verification.extend([x for x in proposal.get("verification_plan", []) if x not in state.verification])

            for call in proposal.get("tool_calls", []):
                if tool_calls_used >= self.epoch.max_tool_calls:
                    self._log({"event": "tool_rejected", "reason": "epoch_tool_budget_exhausted"})
                    break
                tool_calls_used += 1
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
                       "verification_score": verification_score, "personalization_score": personalization_score,
                       "issues": report.issues, "answer": answer, "unknowns": state.unknowns})

            if (proposal.get("stop") and report.passed) or self.core.should_stop(
                confidence, len(state.unknowns), iteration, self.epoch.max_iterations
            ):
                self.core.reenter(state, {
                    "observation": "bounded cycle completed",
                    "what_changed": "proposal passed structural verification and personalized context was applied",
                    "error_found": "; ".join(report.issues),
                    "next_adjustment": "validate user-specific strategy against the next real outcome",
                })
                self._log({"event": "reentry", "state": state.reentry})
                break

        self.memory.save({"instance_id": self.instance_id, "task": task,
                          "last_answer": answer, "confidence": confidence,
                          "verification_score": verification_score,
                          "personalization_score": personalization_score,
                          "reentry": state.reentry})
        return AgentResult(self.instance_id, task, "completed", answer, confidence,
                           iteration, verification_score, personalization_score, self.audit)
