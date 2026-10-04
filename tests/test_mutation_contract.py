from ambivikhry.mutation_contract import MutationContract, mutation_allowed


def contract():
    return MutationContract(
        baseline_commit="abc123",
        evaluator_digest="eval-digest",
        max_changed_files=3,
        max_changed_lines=100,
    )


def test_allows_small_isolated_candidate():
    allowed, reason = mutation_allowed(
        contract(),
        changed_paths=["ambivikhry/prompt.py"],
        changed_lines=20,
        evaluator_digest="eval-digest",
        isolated_branch=True,
    )
    assert allowed is True
    assert reason == "allowed"


def test_rejects_evaluator_change():
    allowed, reason = mutation_allowed(
        contract(),
        changed_paths=["tests/evaluator.py"],
        changed_lines=10,
        evaluator_digest="changed",
        isolated_branch=True,
    )
    assert allowed is False
    assert reason == "evaluator_digest_changed"


def test_rejects_policy_gate_change():
    allowed, reason = mutation_allowed(
        contract(),
        changed_paths=["ambivikhry/policy.py"],
        changed_lines=5,
        evaluator_digest="eval-digest",
        isolated_branch=True,
    )
    assert allowed is False
    assert reason == "policy_gate_protected"


def test_rejects_tool_registry_change():
    allowed, reason = mutation_allowed(
        contract(),
        changed_paths=["ambivikhry/tools.py"],
        changed_lines=5,
        evaluator_digest="eval-digest",
        isolated_branch=True,
    )
    assert allowed is False
    assert reason == "tool_registry_protected"


def test_rejects_budget_and_non_isolated_mutations():
    allowed, reason = mutation_allowed(
        contract(),
        changed_paths=["a", "b", "c", "d"],
        changed_lines=20,
        evaluator_digest="eval-digest",
        isolated_branch=True,
    )
    assert allowed is False
    assert reason == "changed_file_budget_exceeded"

    allowed, reason = mutation_allowed(
        contract(),
        changed_paths=["a"],
        changed_lines=20,
        evaluator_digest="eval-digest",
        isolated_branch=False,
    )
    assert allowed is False
    assert reason == "isolated_branch_required"
