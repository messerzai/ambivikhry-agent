from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json


@dataclass(frozen=True)
class TrajectoryStep:
    """Immutable provenance record for one bounded Ambivikhry step."""

    step_id: str
    role: str
    action: str
    observation: str
    verifier: str
    outcome: str
    policy_decision: str
    parent_lineage: str

    def canonical(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    def digest(self) -> str:
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()


def lineage_digest(steps: list[TrajectoryStep]) -> str:
    """Return an order-sensitive digest for a trajectory prefix."""
    material = "\n".join(step.digest() for step in steps)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def validate_step(step: TrajectoryStep) -> tuple[bool, str]:
    """Fail closed when provenance or policy state is incomplete."""
    required = {
        "step_id": step.step_id,
        "role": step.role,
        "action": step.action,
        "verifier": step.verifier,
        "outcome": step.outcome,
        "policy_decision": step.policy_decision,
        "parent_lineage": step.parent_lineage,
    }
    missing = sorted(name for name, value in required.items() if not str(value).strip())
    if missing:
        return False, f"rejected: missing provenance fields: {', '.join(missing)}"
    if step.policy_decision not in {"allow", "deny", "approval_required"}:
        return False, "rejected: unknown policy decision"
    return True, "accepted: trajectory step is auditable"
