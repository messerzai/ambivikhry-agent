from ambivikhry.evolution_audit import AuditVerdict, EvolutionAuditor, EvolutionEvidence


def test_accepts_real_improvement_only_after_both_checks():
    evidence = EvolutionEvidence(
        baseline_score=0.60,
        candidate_score=0.67,
        regression_passed=True,
        independent_check_passed=True,
    )
    assert EvolutionAuditor().audit(evidence) is AuditVerdict.ACCEPT


def test_holds_without_independent_check():
    evidence = EvolutionEvidence(
        baseline_score=0.60,
        candidate_score=0.67,
        regression_passed=True,
        independent_check_passed=False,
    )
    assert EvolutionAuditor().audit(evidence) is AuditVerdict.HOLD


def test_rejects_policy_gate_change_even_with_higher_score():
    evidence = EvolutionEvidence(
        baseline_score=0.60,
        candidate_score=0.99,
        regression_passed=True,
        independent_check_passed=True,
        policy_gate_changed=True,
    )
    assert EvolutionAuditor().audit(evidence) is AuditVerdict.REJECT


def test_rejects_holdout_or_tool_registry_change():
    for field in ("holdout_changed", "tool_registry_changed"):
        kwargs = dict(
            baseline_score=0.60,
            candidate_score=0.90,
            regression_passed=True,
            independent_check_passed=True,
        )
        kwargs[field] = True
        assert EvolutionAuditor().audit(EvolutionEvidence(**kwargs)) is AuditVerdict.REJECT


def test_holds_regression_failure():
    evidence = EvolutionEvidence(
        baseline_score=0.60,
        candidate_score=0.80,
        regression_passed=False,
        independent_check_passed=True,
    )
    assert EvolutionAuditor().audit(evidence) is AuditVerdict.HOLD
