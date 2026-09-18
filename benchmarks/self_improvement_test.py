"""Deterministic test: improvement must be measurable before adoption."""
from ambivikhry.self_improvement import ImprovementProposal, SelfImprovementLoop

def test_improvement_is_ranked_by_metric():
    def evaluator(p):
        return 0.9 if "verification" in p.metric.lower() else 0.4
    loop = SelfImprovementLoop(evaluator)
    loop.evaluate(ImprovementProposal(
        title="Stronger verification", hypothesis="Independent checks reduce factual errors",
        expected_benefit="higher reliability", metric="verification coverage",
        test_plan=["run regression suite", "compare error rate"],
    ))
    loop.evaluate(ImprovementProposal(
        title="Longer prompts", hypothesis="More text may help", expected_benefit="uncertain",
        metric="latency", test_plan=["measure latency"],
    ))
    ranked = loop.rank()
    assert ranked[0]["title"] == "Stronger verification"
    assert ranked[0]["score"] > ranked[1]["score"]

if __name__ == "__main__":
    test_improvement_is_ranked_by_metric()
    print("SELF-IMPROVEMENT TEST: PASS")
