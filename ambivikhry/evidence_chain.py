"""Evidence-gated improvement claims for Ambivikhry.

An improvement is not a feeling or a larger version: it must be traceable
from a baseline through candidate, trajectory, benchmark, verification,
policy and observed outcome. This module never grants permissions.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

POLICY_DECISIONS = {"allow", "deny", "approval_required"}
DECISIONS = {"accept", "reject", "inconclusive"}

@dataclass(frozen=True)
class EvidenceRecord:
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
    fields = asdict(record)
    missing = sorted(k for k, v in fields.items() if not str(v).strip())
    if missing:
        return False, f"rejected: missing evidence fields: {', '.join(missing)}"
    if record.policy_decision not in POLICY_DECISIONS:
        return False, "rejected: unknown policy decision"
    if record.decision not in DECISIONS:
        return False, "rejected: unknown evidence decision"
    return True, "accepted: evidence chain is complete"

def improvement_claim(record: EvidenceRecord) -> tuple[bool, str]:
    valid, reason = validate_evidence(record)
    if not valid:
        return False, reason
    if record.decision != "accept":
        return False, "rejected: evidence does not accept the candidate"
    if record.policy_decision != "allow":
        return False, "rejected: policy gate did not allow the candidate"
    return True, "accepted: improvement claim is traceable and policy-allowed"
