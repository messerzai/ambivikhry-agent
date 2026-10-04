from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable


PROTECTED_PATH_PREFIXES = (
    "ambivikhry/policy.py",
    "ambivikhry/tools.py",
)


@dataclass(frozen=True)
class MutationContract:
    """Frozen per-candidate contract for safe experimental mutations.

    The contract constrains what a candidate may claim to change. It does not
    grant tools, permissions, or approval. Protected paths and evaluator rules
    are fail-closed.
    """

    baseline_commit: str
    evaluator_digest: str
    max_changed_files: int = 6
    max_changed_lines: int = 500
    allow_policy_changes: bool = False
    allow_tool_registry_changes: bool = False
    require_isolated_branch: bool = True


def digest_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def mutation_allowed(
    contract: MutationContract,
    *,
    changed_paths: Iterable[str],
    changed_lines: int,
    evaluator_digest: str,
    isolated_branch: bool,
) -> tuple[bool, str]:
    paths = tuple(changed_paths)
    if contract.require_isolated_branch and not isolated_branch:
        return False, "isolated_branch_required"
    if len(paths) > contract.max_changed_files:
        return False, "changed_file_budget_exceeded"
    if changed_lines > contract.max_changed_lines:
        return False, "changed_line_budget_exceeded"
    if evaluator_digest != contract.evaluator_digest:
        return False, "evaluator_digest_changed"
    for path in paths:
        if path == "ambivikhry/policy.py" and not contract.allow_policy_changes:
            return False, "policy_gate_protected"
        if path == "ambivikhry/tools.py" and not contract.allow_tool_registry_changes:
            return False, "tool_registry_protected"
    return True, "allowed"
