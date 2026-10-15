from ambivikhry.evidence_chain import EvidenceRecord, improvement_claim, validate_evidence


def make_record(**overrides):
    data = dict(
        baseline_id="baseline-v1",
        baseline_digest="b"*64,
        hypothesis="reduce regression risk",
        candidate_id="candidate-v2",
        candidate_digest="c"*64,
        trajectory_lineage="l"*64,
        benchmark="regression-suite",
        benchmark_result="8/8",
        verifier_result="accepted",
        policy_decision="allow",
        outcome="no regression observed",
        decision="accept",
    )
    data.update(overrides)
    return EvidenceRecord(**data)


def test_complete_chain_is_accepted():
    ok, reason = validate_evidence(make_record())
    assert ok
    assert "complete" in reason


def test_missing_benchmark_fails_closed():
    ok, _ = validate_evidence(make_record(benchmark=""))
    assert not ok


def test_rejected_policy_cannot_be_improvement_claim():
    ok, reason = improvement_claim(make_record(policy_decision="approval_required"))
    assert not ok
    assert "policy" in reason


def test_nonaccepted_decision_cannot_be_improvement_claim():
    ok, _ = improvement_claim(make_record(decision="inconclusive"))
    assert not ok


def test_digest_is_stable_and_changes_with_evidence():
    first = make_record().digest()
    second = make_record().digest()
    changed = make_record(outcome="different observation").digest()
    assert first == second
    assert first != changed
