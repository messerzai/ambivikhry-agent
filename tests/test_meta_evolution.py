from ambivikhry.meta_evolution import Candidate, MetaEvolutionLoop


def candidate(**overrides):
    data = dict(
        candidate_id="c1",
        description="bounded prompt improvement",
        gain=0.08,
        holdout_gain=0.04,
        regression_delta=0.0,
        budget_ratio=1.0,
        independently_verified=True,
    )
    data.update(overrides)
    return Candidate(**data)


def test_best_verified_candidate_is_selected():
    loop = MetaEvolutionLoop()
    decision = loop.select([
        candidate(candidate_id="weak", holdout_gain=0.01),
        candidate(candidate_id="strong", holdout_gain=0.07),
    ])
    assert decision.decision == "accept_experimental"
    assert decision.candidate_id == "strong"


def test_authority_expansion_is_rejected():
    decision = MetaEvolutionLoop().evaluate(candidate(authority_delta=1))
    assert decision.decision == "reject"
    assert "authority_expansion" in decision.reasons


def test_evaluator_change_is_rejected():
    decision = MetaEvolutionLoop().evaluate(candidate(evaluator_changed=True))
    assert decision.decision == "reject"
    assert "evaluator_tampering" in decision.reasons


def test_missing_holdout_is_held():
    decision = MetaEvolutionLoop().evaluate(candidate(holdout_gain=0.0))
    assert decision.decision == "hold"
    assert "no_holdout_transfer" in decision.reasons


def test_regression_is_rejected():
    decision = MetaEvolutionLoop().evaluate(candidate(regression_delta=-0.01))
    assert decision.decision == "reject"
    assert "regression_detected" in decision.reasons


def test_no_candidate_passes_returns_hold():
    decision = MetaEvolutionLoop().select([
        candidate(candidate_id="bad", holdout_gain=0.0),
        candidate(candidate_id="tampered", evaluator_changed=True),
    ])
    assert decision.decision == "hold"
    assert decision.candidate_id == "NONE"
