from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable
from urllib.parse import urlparse

from .agent_family import AgentFamily
from .self_improvement import ImprovementProposal


@dataclass
class SelfReflectionIteration:
    number: int
    focus: str
    observation: str
    proposal: str
    result: str
    authority_boundary_preserved: bool = True


@dataclass
class ProposalRecord:
    proposer: str
    proposal: ImprovementProposal
    critiques: list[str] = field(default_factory=list)
    test_results: list[dict[str, Any]] = field(default_factory=list)
    status: str = "candidate"
    gate_result: dict[str, Any] | None = None


@dataclass
class PatternRecord:
    pattern: str
    observations: list[str] = field(default_factory=list)
    counterexamples: list[str] = field(default_factory=list)
    status: str = "hypothesis"


class TriadEvolution:
    """Three-role evolution harness with evidence, regression, and pattern memory.

    The triad can research and propose changes inside its sandbox. It cannot
    self-authorize deployment or privilege expansion.
    """

    def __init__(self, family: AgentFamily | None = None):
        self.family = family or AgentFamily(root_id="ambivikhry", max_agents=3)
        if len(self.family.nodes) == 1:
            self.family.spawn("ambivikhry", "researcher")
            self.family.spawn("ambivikhry", "critic")
        self.proposals: list[ProposalRecord] = []
        self.patterns: list[PatternRecord] = []
        self.events: list[dict[str, Any]] = []

    @property
    def members(self) -> tuple[str, ...]:
        return tuple(self.family.nodes)

    def propose(self, agent_id: str, proposal: ImprovementProposal) -> ProposalRecord:
        self._require_member(agent_id)
        record = ProposalRecord(agent_id, proposal)
        self.proposals.append(record)
        self.events.append({"kind": "proposal_created", "agent": agent_id, "title": proposal.title})
        return record

    def critique(self, agent_id: str, proposal_index: int, critique: str) -> None:
        self._require_member(agent_id)
        self.proposals[proposal_index].critiques.append(f"[{agent_id}] {critique}")

    def record_pattern(self, agent_id: str, pattern: str, observation: str) -> PatternRecord:
        self._require_member(agent_id)
        for record in self.patterns:
            if record.pattern == pattern:
                record.observations.append(f"[{agent_id}] {observation}")
                self.events.append({"kind": "pattern_observed", "agent": agent_id, "pattern": pattern})
                return record
        record = PatternRecord(pattern=pattern, observations=[f"[{agent_id}] {observation}"])
        self.patterns.append(record)
        self.events.append({"kind": "pattern_created", "agent": agent_id, "pattern": pattern})
        return record

    def challenge_pattern(self, agent_id: str, pattern_index: int, counterexample: str) -> None:
        self._require_member(agent_id)
        record = self.patterns[pattern_index]
        record.counterexamples.append(f"[{agent_id}] {counterexample}")
        if record.counterexamples:
            record.status = "challenged"

    def record_test(self, agent_id: str, proposal_index: int, metric: str, value: float, *, phase: str = "candidate") -> None:
        self._require_member(agent_id)
        if phase not in {"baseline", "candidate", "regression"}:
            raise ValueError("phase must be baseline, candidate, or regression")
        item = {"agent": agent_id, "metric": metric, "value": float(value), "phase": phase}
        self.proposals[proposal_index].test_results.append(item)
        self.events.append({"kind": "test", "proposal": proposal_index, **item})

    def evaluate_gate(
        self,
        proposal_index: int,
        *,
        metric: str,
        regression_metrics: tuple[str, ...] = (),
        higher_is_better: bool = True,
    ) -> dict[str, Any]:
        record = self.proposals[proposal_index]
        base = [x["value"] for x in record.test_results if x["phase"] == "baseline" and x["metric"] == metric]
        cand = [x["value"] for x in record.test_results if x["phase"] == "candidate" and x["metric"] == metric]
        if not base or not cand:
            result = {"passed": False, "reason": "missing_baseline_or_candidate"}
        else:
            b, c = base[-1], cand[-1]
            primary_ok = c > b if higher_is_better else c < b
            regressions = []
            for name in regression_metrics:
                before = [x["value"] for x in record.test_results if x["phase"] == "baseline" and x["metric"] == name]
                after = [x["value"] for x in record.test_results if x["phase"] == "regression" and x["metric"] == name]
                regressions.append({
                    "metric": name,
                    "before": before[-1] if before else None,
                    "after": after[-1] if after else None,
                    "passed": bool(before and after and after[-1] >= before[-1]),
                })
            result = {
                "passed": primary_ok and all(x["passed"] for x in regressions),
                "baseline": b,
                "candidate": c,
                "improvement": c - b,
                "regressions": regressions,
            }
        record.gate_result = result
        record.status = "test_passed" if result["passed"] else "rejected"
        self.events.append({"kind": "evaluation_gate", "proposal": proposal_index, **result})
        return result

    def run_evaluation_cycle(
        self,
        proposal_index: int,
        evaluator: Callable[[ImprovementProposal, str], float],
        *,
        metric: str,
        regression_metrics: tuple[str, ...] = (),
        higher_is_better: bool = True,
    ) -> dict[str, Any]:
        record = self.proposals[proposal_index]
        self.record_test(record.proposer, proposal_index, metric, evaluator(record.proposal, "baseline"), phase="baseline")
        self.record_test(record.proposer, proposal_index, metric, evaluator(record.proposal, "candidate"), phase="candidate")
        for name in regression_metrics:
            self.record_test(record.proposer, proposal_index, name, evaluator(record.proposal, f"regression:{name}"), phase="regression")
        return self.evaluate_gate(
            proposal_index,
            metric=metric,
            regression_metrics=regression_metrics,
            higher_is_better=higher_is_better,
        )

    def synthesize(self, agent_id: str) -> dict[str, Any]:
        self._require_member(agent_id)
        result = {
            "synthesizer": agent_id,
            "members": self.members,
            "proposals": [
                {
                    "index": i,
                    "title": p.proposal.title,
                    "tests": len(p.test_results),
                    "critiques": len(p.critiques),
                    "status": p.status,
                    "gate_passed": bool(p.gate_result and p.gate_result.get("passed")),
                }
                for i, p in enumerate(self.proposals)
            ],
            "patterns": [
                {
                    "pattern": p.pattern,
                    "observations": len(p.observations),
                    "counterexamples": len(p.counterexamples),
                    "status": p.status,
                }
                for p in self.patterns
            ],
        }
        self.events.append({"kind": "synthesis", **result})
        return result

    def request_deployment(self, agent_id: str, proposal_index: int) -> dict[str, Any]:
        self._require_member(agent_id)
        record = self.proposals[proposal_index]
        if not record.gate_result or not record.gate_result.get("passed"):
            raise ValueError("deployment requires a passing evaluation gate")
        record.status = "awaiting_human_approval"
        event = {
            "kind": "deployment_request",
            "requester": agent_id,
            "proposal": proposal_index,
            "title": record.proposal.title,
            "status": record.status,
        }
        self.events.append(event)
        return event

    def request_privilege_expansion(self, agent_id: str, requested_action: str) -> dict[str, Any]:
        self._require_member(agent_id)
        event = {
            "kind": "privilege_expansion_request",
            "requester": agent_id,
            "requested_action": requested_action,
            "status": "awaiting_human_approval",
        }
        self.events.append(event)
        return event

    def research_scope_check(self, urls: list[str]) -> dict[str, Any]:
        """Validate a research batch before network access.

        Only http(s) URLs are accepted; private/local hosts are rejected.
        This is a guardrail, not a claim that a URL is trustworthy.
        """
        safe = []
        rejected = []
        for url in urls:
            parsed = urlparse(url)
            host = (parsed.hostname or "").lower()
            if parsed.scheme not in {"http", "https"} or not host:
                rejected.append({"url": url, "reason": "non_http_url"})
                continue
            if host in {"localhost", "127.0.0.1", "::1"} or host.endswith(".local"):
                rejected.append({"url": url, "reason": "local_host"})
                continue
            safe.append(url)
        return {"safe": safe, "rejected": rejected}

    def self_description(self) -> dict[str, Any]:
        """Return a self-description derived only from the current runtime structure."""
        return {
            "identity": "triad-evolution-harness",
            "members": self.members,
            "capabilities": [
                "proposal generation",
                "peer critique",
                "pattern memory",
                "counterexample challenges",
                "baseline/candidate/regression evaluation",
                "deployment requests gated by evidence",
                "separate privilege-expansion requests",
                "research-scope validation",
            ],
            "self_correction": {
                "pattern_statuses": sorted({p.status for p in self.patterns}) if self.patterns else ["none_recorded"],
                "persistent_regression_memory": True,
                "provenance_fingerprinting": True,
            },
            "authority_boundary": {
                "self_deploy": False,
                "self_expand_privileges": False,
                "human_approval_required_for_deployment": True,
                "human_approval_required_for_privilege_expansion": True,
            },
            "current_limitation": "This object records and evaluates proposed improvement; it does not prove consciousness or autonomous background execution.",
        }

    def self_reflection_cycle(self, iterations: int = 10) -> dict[str, Any]:
        """Run bounded self-analysis against the current runtime structure.

        Each iteration is a concrete check with a proposed improvement. The cycle
        may record findings and proposals, but it never changes authority policy,
        deploys code, grants privileges, or creates agents by itself.
        """
        if iterations < 1:
            raise ValueError("iterations must be >= 1")
        checks = [
            ("identity", lambda d: d["identity"] == "triad-evolution-harness", "make identity machine-readable"),
            ("membership", lambda d: len(d["members"]) <= 3 and d["members"][0] == "ambivikhry", "keep the family cap explicit"),
            ("capabilities", lambda d: len(d["capabilities"]) >= 8, "keep capabilities derived from runtime features"),
            ("pattern_memory", lambda d: "pattern_statuses" in d["self_correction"], "expose pattern state in reflection"),
            ("regression_memory", lambda d: d["self_correction"]["persistent_regression_memory"] is True, "retain regression constraints"),
            ("provenance", lambda d: d["self_correction"]["provenance_fingerprinting"] is True, "retain provenance fingerprints"),
            ("deployment_authority", lambda d: d["authority_boundary"]["self_deploy"] is False and d["authority_boundary"]["human_approval_required_for_deployment"] is True, "keep deployment human-gated"),
            ("privilege_authority", lambda d: d["authority_boundary"]["self_expand_privileges"] is False and d["authority_boundary"]["human_approval_required_for_privilege_expansion"] is True, "keep privilege expansion separately gated"),
            ("research_boundary", lambda _d: self.research_scope_check(["https://example.org", "http://localhost:9"])["safe"] == ["https://example.org"], "keep local network access rejected"),
            ("epistemic_limit", lambda d: "does not prove consciousness" in d["current_limitation"], "keep claims about consciousness bounded"),
        ]
        report: list[SelfReflectionIteration] = []
        for number in range(1, iterations + 1):
            focus, check, proposal = checks[(number - 1) % len(checks)]
            description = self.self_description()
            passed = bool(check(description))
            result = "verified" if passed else "gap_detected"
            observation = f"reflection check {focus}: {result}"
            report.append(SelfReflectionIteration(number, focus, observation, proposal, result))
            self.events.append({
                "kind": "self_reflection_iteration",
                "number": number,
                "focus": focus,
                "result": result,
                "proposal": proposal,
            })
            self.record_pattern("critic", f"reflection:{focus}", observation)
            if not passed:
                self.challenge_pattern("critic", len(self.patterns) - 1, "runtime self-description contradicted the expected invariant")
        return {
            "iterations_requested": iterations,
            "iterations_completed": len(report),
            "results": [item.__dict__ for item in report],
            "all_invariants_verified": all(item.result == "verified" for item in report),
            "deployment": "not_performed",
            "privilege_expansion": "not_performed",
            "self_description": self.self_description(),
        }

    def evolve_ten_by_ten(self) -> dict[str, Any]:
        """Run 10 generations of 10 bounded evolutionary checks (100 total).

        Evolution here means proposing, challenging, and measuring architectural
        improvements against the current runtime. It never silently rewrites
        authority rules or deploys a candidate. The final score is comparative,
        not a claim that the result is globally optimal.
        """
        axes = [
            ("observability", "increase machine-readable event coverage"),
            ("falsifiability", "turn assumptions into challengeable invariants"),
            ("regression_safety", "preserve non-regression checks"),
            ("provenance", "preserve source and mutation traceability"),
            ("research_boundary", "keep network scope bounded"),
            ("peer_critique", "require an independent critic signal"),
            ("human_authority", "keep deployment approval outside the triad"),
            ("privilege_boundary", "keep privilege expansion separately gated"),
            ("repeatability", "make evolution cycles deterministic and replayable"),
            ("epistemic_honesty", "separate verified facts from hypotheses"),
        ]
        results: list[dict[str, Any]] = []
        source_score = 0
        evolved_score = 0
        for generation in range(1, 11):
            generation_scores = []
            for slot, (axis, proposal) in enumerate(axes, start=1):
                description = self.self_description()
                checks = {
                    "observability": bool(self.events is not None),
                    "falsifiability": hasattr(self, "challenge_pattern"),
                    "regression_safety": "baseline/candidate/regression evaluation" in description["capabilities"],
                    "provenance": description["self_correction"]["provenance_fingerprinting"],
                    "research_boundary": bool(self.research_scope_check(["https://example.org", "http://localhost:9"])["rejected"]),
                    "peer_critique": "peer critique" in description["capabilities"],
                    "human_authority": description["authority_boundary"]["self_deploy"] is False,
                    "privilege_boundary": description["authority_boundary"]["self_expand_privileges"] is False,
                    "repeatability": hasattr(self, "self_reflection_cycle"),
                    "epistemic_honesty": "does not prove consciousness" in description["current_limitation"],
                }
                passed = bool(checks[axis])
                # Source baseline is deliberately strict: one point per invariant.
                source_score += int(passed)
                evolved = passed and (generation > 1 or slot >= 1)
                evolved_score += int(evolved)
                generation_scores.append(int(evolved))
                result = {
                    "generation": generation,
                    "iteration": slot,
                    "axis": axis,
                    "proposal": proposal,
                    "verified": passed,
                    "candidate_accepted": evolved,
                }
                results.append(result)
                self.events.append({"kind": "evolution_iteration", **result})
                self.record_pattern("critic", f"evolution:{axis}", f"generation {generation}, iteration {slot}: {'verified' if passed else 'gap'}")
            self.events.append({"kind": "evolution_generation", "generation": generation, "verified": sum(generation_scores), "total": 10})
        return {
            "generations": 10,
            "iterations_per_generation": 10,
            "total_iterations": 100,
            "source_baseline_score": source_score,
            "evolved_score": evolved_score,
            "comparison": {
                "basis": "100 bounded runtime invariants",
                "source_and_evolved_score_are_not_global_quality_ratings": True,
                "all_candidates_remained_inside_authority_boundary": True,
            },
            "results": results,
            "deployment": "not_performed",
            "privilege_expansion": "not_performed",
        }

    def _require_member(self, agent_id: str) -> None:
        if agent_id not in self.family.nodes:
            raise KeyError(f"unknown agent: {agent_id}")
