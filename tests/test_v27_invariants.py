from ambivikhry.core import AmbivikhryCore
from ambivikhry.verifier import Verifier


def test_stop_uses_configured_threshold_and_hard_iteration_bound():
    core = AmbivikhryCore()
    assert not core.should_stop(0.84, 0, 1, 4, 0.90)
    assert core.should_stop(0.90, 0, 2, 4, 0.90)
    assert core.should_stop(0.10, 99, 4, 4, 0.90)


def test_reentry_records_next_adjustment_without_creating_fake_facts():
    core = AmbivikhryCore()
    state = core.intake("test")
    core.reenter(state, {
        "observation": "verification found a gap",
        "what_changed": "evidence requirement added",
        "error_found": "missing source",
        "next_adjustment": "retrieve external evidence",
    })
    assert state.cycle_index == 1
    assert state.facts == []
    assert "retrieve external evidence" in state.center["change_conditions"]


def test_verifier_fails_closed_on_missing_decision():
    report = Verifier().verify({"confidence": 0.99})
    assert not report.passed
    assert "missing decision" in report.issues
    assert report.score < 0.99


def test_verifier_rejects_high_confidence_with_unknowns():
    report = Verifier().verify({
        "decision": "tentative",
        "confidence": 0.95,
        "unknowns": ["external fact not checked"],
    })
    assert not report.passed
    assert "high confidence with unresolved unknowns" in report.issues


def test_verifier_does_not_treat_empty_evidence_as_proof():
    report = Verifier().verify({
        "decision": "answer",
        "confidence": 0.8,
        "claims_without_sources": ["claim"],
        "evidence": [],
    })
    assert not report.passed
    assert report.score <= 0.4
