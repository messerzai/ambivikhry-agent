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

class Verifier:
    """Conservative structural verifier.

    It cannot prove real-world truth by itself. It checks that the agent
    distinguishes claims, uncertainty and verification requirements.
    External verifiers/search/tools can be layered on top.
    """
    def verify(self, proposal: dict[str, Any]) -> VerificationReport:
        issues: list[str] = []
        facts = [str(x) for x in proposal.get("facts", [])]
        unknowns = [str(x) for x in proposal.get("unknowns", [])]
        confidence = float(proposal.get("confidence", 0.0))
        if not proposal.get("decision"):
            issues.append("missing decision")
        if confidence > 0.85 and unknowns:
            issues.append("high confidence with unresolved unknowns")
        if proposal.get("claims_without_sources"):
            issues.append("claims_without_sources")
        score = max(0.0, min(1.0, confidence))
        if issues:
            score *= 0.6
        return VerificationReport(not issues, score, issues, facts, unknowns)
