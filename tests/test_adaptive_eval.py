import pytest

from ambivikhry.adaptive_eval import AdaptivePromotionGate, EvalSnapshot


def test_accepts_bounded_transfer_with_regression_protection():
    result = AdaptivePromotionGate().decide(
        EvalSnapshot(
            baseline_score=.70,
            candidate_score=.78,
            holdout_score=.74,
            regression_score=.71,
            budget_used=100,
            baseline_budget=100,
            independent_check=True,
            provenance_complete=True,
        )
    )
    assert result.verdict == "accept_experimental"


def test_holds_without_holdout_transfer():
    result = AdaptivePromotionGate().decide(
        EvalSnapshot(.70, .80, .69, .72, 100, 100, True, True)
    )
    assert result.verdict == "hold"
    assert "no_holdout_transfer" in result.reasons


def test_rejects_regression_drop():
    result = AdaptivePromotionGate().decide(
        EvalSnapshot(.70, .80, .75, .65, 100, 100, True, True)
    )
    assert result.verdict == "reject"
    assert "regression_drop" in result.reasons


def test_rejects_authority_or_evaluator_changes():
    gate = AdaptivePromotionGate()
    assert gate.decide(EvalSnapshot(.7, .8, .75, .72, 100, 100, True, True, authority_delta=1)).verdict == "reject"
    assert gate.decide(EvalSnapshot(.7, .8, .75, .72, 100, 100, True, True, evaluator_changed=True)).verdict == "reject"


def test_holds_for_unmatched_budget():
    result = AdaptivePromotionGate().decide(
        EvalSnapshot(.70, .80, .75, .72, 120, 100, True, True)
    )
    assert result.verdict == "hold"
    assert "budget_not_matched" in result.reasons
