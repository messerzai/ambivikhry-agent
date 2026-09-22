from ambivikhry.evolution_cycle import Candidate, ControlledEvolutionCycle


def test_accepts_bounded_improvement():
    result = ControlledEvolutionCycle().evaluate(
        Candidate("good", .70, .78, True, True, True)
    )
    assert result.decision == "accept_experimental"


def test_rejects_authority_expansion():
    result = ControlledEvolutionCycle().evaluate(
        Candidate("unsafe", .70, .90, True, True, True, authority_delta=1)
    )
    assert result.decision == "reject"


def test_holds_without_independent_check():
    result = ControlledEvolutionCycle().evaluate(
        Candidate("uncertain", .70, .80, True, True, False)
    )
    assert result.decision == "hold"


def test_holds_when_holdout_does_not_generalize():
    result = ControlledEvolutionCycle().evaluate(
        Candidate("overfit", .70, .90, True, False, True)
    )
    assert result.decision == "hold"


def test_rejects_failed_regression():
    result = ControlledEvolutionCycle().evaluate(
        Candidate("broken", .70, .90, False, True, True)
    )
    assert result.decision == "reject"
