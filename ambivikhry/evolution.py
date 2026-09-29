from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EpochContract:
    """Frozen acceptance contract for one controlled evolution epoch."""

    epoch_id: str
    baseline_ref: str
    policy_gate_required: bool = True
    human_approval_required_for_side_effects: bool = True
    holdout_required_for_promotion: bool = True
    max_tool_calls: int = 8
    max_iterations: int = 4


@dataclass(frozen=True)
class EvolutionProposal:
    """Auditable proposal; it is never an authorization by itself."""

    proposal_id: str
    epoch_id: str
    category: str
    hypothesis: str
    expected_gain: str
    risk: str
    changed_surfaces: tuple[str, ...] = ()
    requires_human_approval: bool = False


@dataclass(frozen=True)
class Evidence:
    proposal_id: str
    stage: str
    status: str
    metric: str | None = None
    value: float | None = None
    note: str = ""
    source: str = ""


class EvolutionLedger:
    """Append-only lineage for proposals, verification and holdout evidence."""

    def __init__(self, directory: str | Path):
        self.path = Path(directory)
        self.path.mkdir(parents=True, exist_ok=True)
        self.file = self.path / "evolution-lineage.jsonl"

    def append(self, record: dict[str, Any]) -> None:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **record,
        }
        with self.file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    def record_proposal(self, proposal: EvolutionProposal) -> None:
        self.append({"type": "proposal", **asdict(proposal)})

    def record_evidence(self, evidence: Evidence) -> None:
        self.append({"type": "evidence", **asdict(evidence)})

    def digest(self) -> str:
        if not self.file.exists():
            return hashlib.sha256(b"").hexdigest()
        return hashlib.sha256(self.file.read_bytes()).hexdigest()


def promotion_allowed(
    *,
    contract: EpochContract,
    policy_passed: bool,
    regression_passed: bool,
    holdout_passed: bool,
    requires_human_approval: bool,
    human_approved: bool = False,
) -> bool:
    """Pure promotion gate; it cannot grant permissions or bypass Policy Gate."""
    if contract.policy_gate_required and not policy_passed:
        return False
    if not regression_passed:
        return False
    if contract.holdout_required_for_promotion and not holdout_passed:
        return False
    if requires_human_approval and not human_approved:
        return False
    return True
