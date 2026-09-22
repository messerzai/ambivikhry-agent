import pytest

from ambivikhry.occams_razor import Hypothesis, OccamsRazor
from ambivikhry.neurography import DenisSelfSimilarityAnalyzer, NeurographicSelfSimilarity
from ambivikhry.self_revision import RevisionCandidate, SelfRevisionGate


def test_occam_prefers_simpler_adequate_hypothesis():
    tool = OccamsRazor()
    result = tool.select([
        Hypothesis("complex", fit=.95, complexity=.8, assumptions=5),
        Hypothesis("simple", fit=.90, complexity=.2, assumptions=1),
    ])
    assert result.name == "simple"


def test_occam_does_not_select_inadequate_simple_model():
    tool = OccamsRazor()
    with pytest.raises(ValueError):
        tool.select([Hypothesis("too_simple", fit=.4, complexity=.1)])


def test_self_similarity_is_high_for_repeated_trace():
    trace = [0, 1, 0, 1, 0, 1, 0, 1]
    report = NeurographicSelfSimilarity().analyze(trace, scales=(2, 4))
    assert report.mean_score > .95


def test_self_similarity_rejects_short_input():
    with pytest.raises(ValueError):
        NeurographicSelfSimilarity().analyze([1, 2, 3])


def test_denis_analyzer_detects_repeated_behavioral_loop():
    analyzer = DenisSelfSimilarityAnalyzer()
    report = analyzer.detect_loop([0, 1, 0, 1, 0, 1, 0, 1], period=2)
    assert report.repeated_cycles == 4
    assert report.score > .95


def test_denis_analyzer_separates_micro_macro_reality_change():
    analyzer = DenisSelfSimilarityAnalyzer()
    report = analyzer.reconstruction_effect(.30, .80, .40, .70)
    assert report.reality_change == pytest.approx(.40)


def test_denis_analyzer_rejects_invalid_reality_scores():
    with pytest.raises(ValueError):
        DenisSelfSimilarityAnalyzer().reconstruction_effect(.30, 1.2, .40, .70)


def test_revision_accepts_bounded_improvement():
    gate = SelfRevisionGate()
    assert gate.evaluate(RevisionCandidate("r1", .70, .76)) == "accept_experimental"


def test_revision_rejects_authority_expansion():
    gate = SelfRevisionGate()
    assert gate.evaluate(RevisionCandidate("r2", .70, .95, authority_delta=1)) == "reject"


def test_revision_rejects_policy_or_holdout_changes():
    gate = SelfRevisionGate()
    assert gate.evaluate(RevisionCandidate("r3", .70, .95, policy_gate_changed=True)) == "reject"
    assert gate.evaluate(RevisionCandidate("r4", .70, .95, holdout_changed=True)) == "reject"


def test_revision_holds_non_improvement():
    gate = SelfRevisionGate()
    assert gate.evaluate(RevisionCandidate("r5", .70, .70)) == "hold"
