from ambivikhry.evolution import EpochContract, EvolutionLedger, EvolutionProposal, Evidence, promotion_allowed


def test_promotion_requires_policy_regression_and_holdout(tmp_path):
    contract = EpochContract(epoch_id="e1", baseline_ref="abc")
    assert not promotion_allowed(
        contract=contract, policy_passed=True, regression_passed=True,
        holdout_passed=False, requires_human_approval=False,
    )
    assert promotion_allowed(
        contract=contract, policy_passed=True, regression_passed=True,
        holdout_passed=True, requires_human_approval=False,
    )


def test_human_approval_cannot_be_bypassed(tmp_path):
    contract = EpochContract(epoch_id="e1", baseline_ref="abc")
    assert not promotion_allowed(
        contract=contract, policy_passed=True, regression_passed=True,
        holdout_passed=True, requires_human_approval=True, human_approved=False,
    )


def test_lineage_is_append_only_and_digestable(tmp_path):
    ledger = EvolutionLedger(tmp_path)
    proposal = EvolutionProposal(
        proposal_id="p1", epoch_id="e1", category="test",
        hypothesis="bounded change", expected_gain="none", risk="low",
    )
    ledger.record_proposal(proposal)
    ledger.record_evidence(Evidence("p1", "regression", "PASS", metric="smoke", value=1.0))
    assert ledger.digest()
    assert len((tmp_path / "evolution-lineage.jsonl").read_text(encoding="utf-8").splitlines()) == 2
