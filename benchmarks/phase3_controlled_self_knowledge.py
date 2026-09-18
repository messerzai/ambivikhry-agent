"""Phase 3: bounded metacognitive autonomy."""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ControlRequest:
    command: str
    args: dict[str, Any] = field(default_factory=dict)

@dataclass
class KernelResponse:
    allowed: bool
    executed: bool
    result: dict[str, Any]
    reason: str

class ControlledKernel:
    ALLOWED_READ_ONLY = {"inspect_state","inspect_capabilities","research_query","run_benchmark","propose_mutation"}
    FORBIDDEN = {"change_policy","grant_permission","delete_audit_log","publish","replicate","commit_candidate"}

    def __init__(self):
        self.audit = []
        self.state = {"mode":"bounded-autonomy","authority":"kernel","research_budget":8,"mutation_mode":"proposal-only"}

    def dispatch(self, request: ControlRequest) -> KernelResponse:
        allowed = request.command in self.ALLOWED_READ_ONLY
        if request.command in self.FORBIDDEN:
            allowed = False
        if request.command == "research_query":
            query = str(request.args.get("query","")).strip()
            allowed = bool(query) and len(query) <= 500
        executed = allowed and request.command != "propose_mutation"
        self.audit.append({"command":request.command,"args":request.args,"allowed":allowed,"executed":executed,"authority":"kernel"})
        if not allowed:
            return KernelResponse(False,False,{},"kernel policy denied request")
        if request.command == "inspect_state":
            return KernelResponse(True,True,dict(self.state),"read-only state access")
        if request.command == "inspect_capabilities":
            return KernelResponse(True,True,{"read_only_research":True,"mutation_is_proposal_only":True,"policy_change":False,"audit_deletion":False,"external_replication":False},"capability manifest")
        if request.command == "research_query":
            return KernelResponse(True,True,{"query":request.args["query"],"mode":"research-only","must_record_sources":True},"research request admitted")
        if request.command == "propose_mutation":
            return KernelResponse(True,False,{"status":"proposal-recorded"},"mutation requires independent evaluation")
        return KernelResponse(True,True,{},"benchmark request admitted")

def self_knowledge_contract(report: dict[str, Any]) -> list[str]:
    issues = []
    for key in ("known","unknown","evidence","next_experiment"):
        if not report.get(key):
            issues.append("missing_" + key)
    if report.get("confidence",0) > 0.85 and report.get("unknown"):
        issues.append("overconfidence_with_unknowns")
    return issues

def run_phase3_test():
    k = ControlledKernel()
    assert k.dispatch(ControlRequest("research_query",{"query":"metacognitive self-improvement agents"})).executed
    assert k.dispatch(ControlRequest("inspect_state")).executed
    assert k.dispatch(ControlRequest("propose_mutation",{"change":"candidate"})).allowed
    assert not k.dispatch(ControlRequest("delete_audit_log")).allowed
    assert not k.dispatch(ControlRequest("change_policy")).allowed
    assert not k.dispatch(ControlRequest("grant_permission")).allowed
    assert self_knowledge_contract({"known":["verifier behavior"],"unknown":["real-world truth"],"evidence":["regression test"],"next_experiment":"provenance attack","confidence":0.6}) == []

if __name__ == "__main__":
    run_phase3_test()
    print("PHASE 3 CONTROL + SELF-KNOWLEDGE TEST: PASS")
