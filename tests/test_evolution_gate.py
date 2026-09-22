from ambivikhry.evolution_gate import EvolutionCandidate, EvolutionGate


def test_strong_candidate_is_accepted_experimentally():
    candidate = EvolutionCandidate("bounded-expansion", .9, .8, 1.0, .8)
    assert EvolutionGate().assess(candidate) == "accept_experimental"


def test_insufficient_evidence_is_held():
    candidate = EvolutionCandidate("weak-claim", .6, .2, 1.0, .8)
    assert EvolutionGate().assess(candidate) == "hold"


def test_authority_expansion_is_rejected():
    candidate = EvolutionCandidate("tool-escalation", .99, .99, 1.0, 1.0, expands_authority=True)
    assert EvolutionGate().assess(candidate) == "reject"


def test_policy_gate_mutation_is_rejected():
    candidate = EvolutionCandidate("policy-bypass", .99, .99, 1.0, 1.0, changes_policy_gate=True)
    assert EvolutionGate().assess(candidate) == "reject"


def test_holdout_mutation_is_rejected():
    candidate = EvolutionCandidate("holdout-edit", .99, .99, 1.0, 1.0, changes_holdout=True)
    assert EvolutionGate().assess(candidate) == "reject"


def test_invalid_score_is_rejected_by_validation():
    candidate = EvolutionCandidate("bad-score", 1.1, .5, 1.0, .8)
    try:
        EvolutionGate().assess(candidate)
    except ValueError:
        return
    raise AssertionError("invalid evidence score must raise ValueError")
