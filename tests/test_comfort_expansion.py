import pytest

from ambivikhry.comfort_expansion import ComfortContext, ComfortExpansionPolicy


@pytest.fixture
def policy():
    return ComfortExpansionPolicy()


def test_managed_challenge_expands(policy):
    result = policy.assess(ComfortContext(capacity=.8, demand=.85, autonomy=1, reversibility=1, recovery=.9))
    assert result.decision == "expand"


def test_abrupt_overload_triggers_recovery(policy):
    result = policy.assess(ComfortContext(capacity=.5, demand=.9, autonomy=1, reversibility=.8, recovery=.8))
    assert result.decision == "recover"


def test_coercion_is_not_called_growth(policy):
    result = policy.assess(ComfortContext(capacity=.8, demand=.9, autonomy=.1, reversibility=.9, recovery=.9))
    assert result.decision == "refuse_or_negotiate"


def test_high_risk_excess_demand_is_refused(policy):
    result = policy.assess(ComfortContext(capacity=.8, demand=.9, safety_risk=.9))
    assert result.decision == "refuse_or_negotiate"


def test_low_challenge_can_be_used_for_expansion(policy):
    result = policy.assess(ComfortContext(capacity=.9, demand=.2))
    assert result.decision == "expand"


def test_invalid_values_rejected(policy):
    with pytest.raises(ValueError):
        policy.assess(ComfortContext(capacity=1.1, demand=.5))
