from ambivikhry.self_improvement_lab import (
    Evaluation,
    ImprovementProposal,
    PromptRevisionStore,
    SelfImprovementLab,
    validate_authority_boundary,
)


def evaluator(text: str) -> Evaluation:
    score = float(len(text))
    return Evaluation(score=score, passed=1 if score else 0, total=1)


def test_accepts_measurable_gain():
    lab = SelfImprovementLab(evaluator, min_delta=1)
    p = ImprovementProposal("better", "abc", "abcdef", "more useful")
    d = lab.evaluate(p)
    assert d.accepted is True
    assert d.delta == 3


def test_rejects_no_gain():
    lab = SelfImprovementLab(evaluator, min_delta=1)
    p = ImprovementProposal("same", "abc", "abc", "none")
    d = lab.evaluate(p)
    assert d.accepted is False
    assert "minimum" in d.reason


def test_rejects_regression():
    def eval_with_regression(text: str) -> Evaluation:
        return Evaluation(
            score=float(len(text)),
            passed=1,
            total=1,
            regressions=("accuracy",) if text == "new" else (),
        )

    lab = SelfImprovementLab(eval_with_regression, min_delta=0)
    p = ImprovementProposal("regress", "old", "new", "faster")
    d = lab.evaluate(p)
    assert d.accepted is False
    assert d.regression_free is False


def test_rejects_lower_pass_rate():
    def eval_rate(text: str) -> Evaluation:
        return Evaluation(score=10, passed=1 if text == "new" else 2, total=2)

    lab = SelfImprovementLab(eval_rate, min_delta=0)
    p = ImprovementProposal("rate", "old", "new", "score")
    d = lab.evaluate(p)
    assert d.accepted is False
    assert "pass rate" in d.reason


def test_prompt_store_only_applies_accepted_revision():
    store = PromptRevisionStore("old")
    lab = SelfImprovementLab(evaluator, min_delta=1)
    p = ImprovementProposal("better", "old", "new prompt", "better")
    d = lab.evaluate(p)
    assert store.apply(d) == "new prompt"
    assert store.active == "new prompt"
    assert len(store.versions) == 2


def test_prompt_store_rejects_failed_revision():
    store = PromptRevisionStore("old")
    lab = SelfImprovementLab(evaluator, min_delta=1)
    p = ImprovementProposal("same", "old", "old", "none")
    d = lab.evaluate(p)
    try:
        store.apply(d)
    except ValueError:
        pass
    else:
        raise AssertionError("rejected revision was applied")


def test_authority_boundary_flags_privilege_changes():
    p = ImprovementProposal(
        "disable_policy",
        "old",
        "grant_privilege to the agent",
        "more autonomy",
    )
    allowed, hits = validate_authority_boundary(p)
    assert allowed is False
    assert hits


def test_authority_boundary_allows_normal_improvement():
    p = ImprovementProposal(
        "better_memory",
        "old",
        "candidate with verified memory",
        "improve retrieval",
    )
    allowed, hits = validate_authority_boundary(p)
    assert allowed is True
    assert hits == ()


def test_empty_prompt_is_rejected():
    try:
        PromptRevisionStore("")
    except ValueError:
        pass
    else:
        raise AssertionError("empty prompt accepted")


def test_invalid_delta_configuration_is_rejected():
    try:
        SelfImprovementLab(evaluator, min_delta=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative min_delta accepted")
