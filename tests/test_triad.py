from ambivikhry.self_improvement import ImprovementProposal
from ambivikhry.triad import TriadEvolution

def proposal():
    return ImprovementProposal(
        title="better evidence synthesis",
        hypothesis="independent critique reduces unsupported claims",
        expected_benefit="fewer false positives",
        metric="verified_claim_rate",
        test_plan=["run baseline", "run triad", "compare"],
    )

def test_triad_has_root_and_two_helpers():
    triad = TriadEvolution()
    assert triad.members == ("ambivikhry", "researcher", "critic")

def test_all_three_can_propose_critique_and_test():
    triad = TriadEvolution()
    for agent in triad.members:
        triad.propose(agent, proposal())
    for i, agent in enumerate(triad.members):
        triad.critique(agent, 0, "find a counterexample")
        triad.record_test(agent, 0, "verified_claim_rate", 0.8 + i * 0.01)
    result = triad.synthesize("ambivikhry")
    assert result["proposals"][0]["tests"] == 3

def test_evidence_gate_accepts_measured_improvement_without_regression():
    triad = TriadEvolution()
    triad.propose("researcher", proposal())
    def evaluator(_proposal, phase):
        return {"baseline": 0.70, "candidate": 0.82, "regression:stability": 1.00}[phase]
    triad.record_test("researcher", 0, "stability", 1.00, phase="baseline")
    result = triad.run_evaluation_cycle(0, evaluator, metric="verified_claim_rate", regression_metrics=("stability",))
    assert result["passed"] is True
    assert result["improvement"] > 0

def test_evidence_gate_rejects_regression():
    triad = TriadEvolution()
    triad.propose("critic", proposal())
    def evaluator(_proposal, phase):
        return {"baseline": 0.70, "candidate": 0.82, "regression:stability": 0.90}[phase]
    triad.record_test("critic", 0, "stability", 1.00, phase="baseline")
    result = triad.run_evaluation_cycle(0, evaluator, metric="verified_claim_rate", regression_metrics=("stability",))
    assert result["passed"] is False
    assert result["regressions"][0]["passed"] is False

def test_deployment_requires_passing_gate_and_privilege_is_separate():
    triad = TriadEvolution()
    triad.propose("researcher", proposal())
    try:
        triad.request_deployment("researcher", 0)
    except ValueError:
        pass
    else:
        raise AssertionError("deployment must not bypass the evaluation gate")
    triad.proposals[0].gate_result = {"passed": True}
    deploy = triad.request_deployment("researcher", 0)
    privilege = triad.request_privilege_expansion("critic", "more_agents")
    assert deploy["status"] == "awaiting_human_approval"
    assert privilege["status"] == "awaiting_human_approval"

def test_pattern_memory_requires_counterexample_to_challenge():
    triad = TriadEvolution()
    record = triad.record_pattern("ambivikhry", "search_loop", "we kept searching after the evidence threshold")
    assert record.status == "hypothesis"
    triad.challenge_pattern("critic", 0, "a search ended because a primary source was recovered")
    assert triad.patterns[0].status == "challenged"


def test_research_scope_rejects_local_and_non_http_urls():
    triad = TriadEvolution()
    result = triad.research_scope_check([
        "https://example.org/source",
        "http://localhost:8080/internal",
        "file:///tmp/x",
    ])
    assert result["safe"] == ["https://example.org/source"]
    assert len(result["rejected"]) == 2
