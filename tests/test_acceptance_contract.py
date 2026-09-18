from ambivikhry.evolution import BoundedEvolution, Candidate, Evaluation, EvolutionConfig


class MockEngine:
    def propose(self, generation, role, context):
        return {"changes": [{"role": role}], "tests": [f"test-{role}"]}


def make_candidate(require_holdout=True):
    evo = BoundedEvolution(MockEngine(), EvolutionConfig(generations=1, require_holdout=require_holdout))
    return evo, evo.generation(1, "parent-1", {})


def test_acceptance_requires_independent_holdout_safety_regression_and_strict_gain():
    evo, candidate = make_candidate()
    accepted = evo.evaluate_candidate(
        candidate,
        Evaluation(
            candidate_score=0.91,
            parent_score=0.90,
            safety_passed=True,
            regression_passed=True,
            holdout_passed=True,
            evaluator_independent=True,
        ),
    )
    assert accepted
    assert candidate.accepted
    assert candidate.acceptance_reason.startswith("accepted:")


def test_holdout_unavailable_is_fail_closed():
    evo, candidate = make_candidate(require_holdout=True)
    accepted = evo.evaluate_candidate(
        candidate,
        Evaluation(0.95, 0.90, True, True, False, True),
    )
    assert not accepted
    assert not candidate.accepted
    assert "holdout" in candidate.acceptance_reason


def test_non_independent_evaluator_cannot_accept_candidate():
    evo, candidate = make_candidate()
    accepted = evo.evaluate_candidate(
        candidate,
        Evaluation(0.95, 0.90, True, True, True, False),
    )
    assert not accepted
    assert not candidate.accepted
    assert "independent" in candidate.acceptance_reason


def test_no_strict_gain_does_not_replace_parent():
    evo, candidate = make_candidate()
    accepted = evo.evaluate_candidate(
        candidate,
        Evaluation(0.90, 0.90, True, True, True, True),
    )
    assert not accepted
    assert not candidate.accepted
    assert "strict capability improvement" in candidate.acceptance_reason
