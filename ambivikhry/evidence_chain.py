"""Fail-closed evidence chain linking baseline, candidate, tests and policy.

An improvement claim is valid only when it is traceable from a baseline through
a candidate, benchmark, verifier result, policy decision, trajectory lineage,
and an explicit outcome. This module never grants permissions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json


ALLOWED_POLICY_DECISIONS = {"allow", "deny", "approval_required"}
ALLOWED_DECISIONS = {"accept", "reject", "inconclusive"}


@dataclass(frozen=True)
class EvidenceRecord:
    """Immutable evidence chain for one proposed change."""

    baseline_id: str
    baseline_digest: str
    hypothesis: str
    candidate_id: str
    candidate_digest: str
    trajectory_lineage: str
    benchmark: str
    benchmark_result: str
    verifier_result: str
    policy_decision: str
    outcome: str
    decision: str

    def canonical(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    def digest(self) -> str:
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()


def validate_evidence(record: EvidenceRecord) -> tuple[bool, str]:
    """Fail closed if any link required for an improvement claim is absent."""
    required = {
        "baseline_id": record.baseline_id,
        "baseline_digest": record.baseline_digest,
        "hypothesis": record.hypothesis,
        "candidate_id": record.candidate_id,
        "candidate_digest": record.candidate_digest,
        "trajectory_lineage": record.trajectory_lineage,
        "benchmark": record.benchmark,
        "benchmark_result": record.benchmark_result,
        "verifier_result": record.verifier_result,
        "policy_decision": record.policy_decision,
        "outcome": record.outcome,
        "decision": record.decision,
    }
    missing = sorted(name for name, value in required.items() if not str(value).strip())
    if missing:
        return False, f"rejected: missing evidence fields: {', '.join(missing)}"
    if record.policy_decision not in ALLOWED_POLICY_DECISIONS:
        return False, "rejected: unknown policy decision"
    if record.decision not in ALLOWED_DECISIONS:
        return False, "rejected: unknown evidence decision"
    return True, "accepted: evidence chain is complete"


def improvement_claim(record: EvidenceRecord) -> tuple[bool, str]:
    """Allow an improvement claim only for complete, accepted evidence."""
    valid, reason = validate_evidence(record)
    if not valid:
        return False, reason
    if record.decision != "accept":
        return False, "rejected: evidence does not accept the candidate"
    if record.policy_decision != "allow":
        return False, "rejected: policy gate did not allow the candidate"
    return True, "accepted: improvement claim is traceable and policy-allowed"
