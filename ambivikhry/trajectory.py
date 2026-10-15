from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib
import json

@dataclass(frozen=True)
class TrajectoryStep:
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
    return hashlib.sha256("\n".join(s.digest() for s in steps).encode("utf-8")).hexdigest()

def validate_step(step: TrajectoryStep) -> tuple[bool, str]:
    fields = asdict(step)
    required = {k: fields[k] for k in fields if k != "observation"}
    missing = sorted(k for k, v in required.items() if not str(v).strip())
    if missing:
        return False, f"rejected: missing provenance fields: {', '.join(missing)}"
    if step.policy_decision not in {"allow", "deny", "approval_required"}:
        return False, "rejected: unknown policy decision"
    return True, "accepted: trajectory step is auditable"
