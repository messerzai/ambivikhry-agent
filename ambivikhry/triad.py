from __future__ import annotations

"""Three-agent cooperative self-improvement experiment.

The root and two helpers share a research corpus and proposal board. They can
research, critique, test, and propose mutations. No member can deploy a
mutation or grant new privileges; those actions become auditable requests.
"""

from dataclasses import dataclass, field
from typing import Any

from .agent_family import AgentFamily
from .self_improvement import ImprovementProposal


@dataclass
class ProposalRecord:
    proposer: str
    proposal: ImprovementProposal
    critiques: list[str] = field(default_factory=list)
    test_results: list[dict[str, Any]] = field(default_factory=list)
    status: str = "candidate"


class TriadEvolution:
    def __init__(self, family: AgentFamily | None = None):
        self.family = family or AgentFamily(root_id="ambivikhry", max_agents=3)
        if len(self.family.nodes) == 1:
            self.family.spawn("ambivikhry", "researcher")
            self.family.spawn("ambivikhry", "critic")
        self.proposals: list[ProposalRecord] = []
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
        record = self.proposals[proposal_index]
        record.critiques.append(f"[{agent_id}] {critique}")
        self.events.append({"kind": "critique", "agent": agent_id, "proposal": proposal_index})

    def record_test(self, agent_id: str, proposal_index: int, metric: str, value: float) -> None:
        self._require_member(agent_id)
        record = self.proposals[proposal_index]
        record.test_results.append({"agent": agent_id, "metric": metric, "value": float(value)})
        self.events.append({"kind": "test", "agent": agent_id, "proposal": proposal_index, "metric": metric, "value": float(value)})

    def synthesize(self, agent_id: str) -> dict[str, Any]:
        self._require_member(agent_id)
        ranked = []
        for i, p in enumerate(self.proposals):
            values = [x["value"] for x in p.test_results]
            ranked.append({
                "index": i,
                "title": p.proposal.title,
                "tests": len(values),
                "mean_metric": sum(values) / len(values) if values else None,
                "critiques": len(p.critiques),
            })
        result = {"synthesizer": agent_id, "members": self.members, "proposals": ranked}
        self.events.append({"kind": "synthesis", **result})
        return result

    def request_deployment(self, agent_id: str, proposal_index: int) -> dict[str, Any]:
        self._require_member(agent_id)
        record = self.proposals[proposal_index]
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

    def _require_member(self, agent_id: str) -> None:
        if agent_id not in self.family.nodes:
            raise KeyError(f"unknown agent: {agent_id}")
