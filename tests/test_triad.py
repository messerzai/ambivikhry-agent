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


def test_deployment_and_privilege_changes_are_requests():
    triad = TriadEvolution()
    triad.propose("researcher", proposal())
    deploy = triad.request_deployment("researcher", 0)
    privilege = triad.request_privilege_expansion("critic", "more_agents")
    assert deploy["status"] == "awaiting_human_approval"
    assert privilege["status"] == "awaiting_human_approval"
