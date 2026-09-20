from ambivikhry.trajectory import TrajectoryStep, lineage_digest, validate_step


def make_step(**overrides):
    values = {
        "step_id": "s1",
        "role": "critic",
        "action": "inspect",
        "observation": "candidate output",
        "verifier": "regression-suite",
        "outcome": "pass",
        "policy_decision": "allow",
        "parent_lineage": "main",
    }
    values.update(overrides)
    return TrajectoryStep(**values)


def test_digest_is_stable_and_order_sensitive():
    first = make_step()
    second = make_step(step_id="s2", action="compare")
    assert first.digest() == make_step().digest()
    assert lineage_digest([first, second]) != lineage_digest([second, first])


def test_validation_fails_closed_for_missing_provenance():
    ok, reason = validate_step(make_step(verifier=""))
    assert not ok
    assert "missing provenance" in reason


def test_validation_rejects_unknown_policy_decision():
    ok, reason = validate_step(make_step(policy_decision="bypass"))
    assert not ok
    assert "unknown policy" in reason


def test_validation_accepts_explicit_approval_required():
    ok, reason = validate_step(make_step(policy_decision="approval_required"))
    assert ok
    assert "auditable" in reason
