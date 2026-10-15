from ambivikhry.evidence_chain import EvidenceRecord, improvement_claim, validate_evidence
from ambivikhry.self_model import current_self_model, next_iteration_goal
from ambivikhry.trajectory import TrajectoryStep, lineage_digest, validate_step


def record(**changes):
    data = dict(baseline_id="b1", baseline_digest="b"*64, hypothesis="reduce false improvement claims", candidate_id="c1", candidate_digest="c"*64, trajectory_lineage="l"*64, benchmark="regression", benchmark_result="pass", verifier_result="pass", policy_decision="allow", outcome="no regression", decision="accept")
    data.update(changes)
    return EvidenceRecord(**data)


def test_evidence_chain_is_fail_closed():
    assert validate_evidence(record())[0]
    assert not validate_evidence(record(benchmark=""))[0]
    assert not improvement_claim(record(policy_decision="approval_required"))[0]
    assert record().digest() == record().digest()
    assert record().digest() != record(outcome="changed").digest()


def test_trajectory_is_order_sensitive_and_policy_bounded():
    a = TrajectoryStep("a", "reasoner", "inspect", "obs", "v", "pass", "allow", "root")
    b = TrajectoryStep("b", "critic", "compare", "obs", "v", "pass", "allow", a.digest())
    assert lineage_digest([a, b]) != lineage_digest([b, a])
    assert validate_step(a)[0]
    assert not validate_step(TrajectoryStep("a", "reasoner", "inspect", "obs", "v", "pass", "bypass", "root"))[0]


def test_self_model_does_not_claim_authority():
    text = current_self_model(["test-evidence"]).describe()
    assert "доказанное сознание" in text
    assert "Policy Gate" in text
    assert "test-evidence" in text
    goal = next_iteration_goal("benchmark evidence is disconnected")
    assert "только компонент" in goal
    assert "регресс" in goal
