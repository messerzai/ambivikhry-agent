from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class VerificationReport:
    passed: bool
    score: float
    issues: list[str]
    facts: list[str]
    unknowns: list[str]
    evidence: list[dict[str, Any]]


class Verifier:
    """Conservative structural verifier.

    This verifier does not prove real-world truth. It checks consistency of
    the proposal and whether externally testable claims have an evidence
    trail. A future web/tool verifier can supply the evidence objects.
    """

    @staticmethod
    def _confidence(value: Any) -> float:
        try:
            value = float(value)
        except (TypeError, ValueError):
            return 0.0
        return max(0.0, min(1.0, value))

    def verify(self, proposal: dict[str, Any]) -> VerificationReport:
        if not isinstance(proposal, dict):
            return VerificationReport(False, 0.0, ["proposal must be an object"], [], [], [])

        issues: list[str] = []
        facts = [str(x).strip() for x in proposal.get("facts", []) if str(x).strip()]
        unknowns = [str(x).strip() for x in proposal.get("unknowns", []) if str(x).strip()]
        evidence = [x for x in proposal.get("evidence", []) if isinstance(x, dict)]
        confidence = self._confidence(proposal.get("confidence", 0.0))

        if not str(proposal.get("decision", "")).strip():
            issues.append("missing decision")
        if confidence > 0.85 and unknowns:
            issues.append("high confidence with unresolved unknowns")
        if proposal.get("claims_without_sources"):
            issues.append("claims_without_sources")

        # Evidence must have a source and a claim. Empty evidence objects do
        # not count merely because the model emitted an evidence array.
        bad_evidence = [e for e in evidence if not str(e.get("source", "")).strip()
                        or not str(e.get("claim", "")).strip()]
        if bad_evidence:
            issues.append("malformed evidence entries")

        verification_plan = proposal.get("verification_plan", [])
        if not isinstance(verification_plan, list):
            issues.append("verification_plan must be a list")

        score = confidence
        if issues:
            score *= 0.6
        # Structural verification should never manufacture certainty.
        if proposal.get("claims_without_sources") and not evidence:
            score = min(score, 0.4)

        return VerificationReport(
            not issues,
            max(0.0, min(1.0, score)),
            issues,
            facts,
            unknowns,
            evidence,
        )
