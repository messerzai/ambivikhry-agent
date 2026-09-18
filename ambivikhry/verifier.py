from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
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
        verification_plan = proposal.get("verification_plan", [])
        claims_without_sources = proposal.get("claims_without_sources", [])

        try:
            confidence = float(proposal.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0
            issues.append("invalid confidence")

        if not isfinite(confidence) or not 0.0 <= confidence <= 1.0:
            issues.append("confidence outside [0, 1]")

        if not proposal.get("decision"):
            issues.append("missing decision")

        if confidence > 0.85 and unknowns:
            issues.append("high confidence with unresolved unknowns")

        if claims_without_sources:
            issues.append("claims_without_sources")

        # A proposal that asserts facts or leaves unknowns must also state
        # how those claims will be checked. This does not prove truth; it
        # prevents the agent from silently treating unverified claims as facts.
        if (facts or unknowns) and not verification_plan:
            issues.append("missing verification_plan")

        # Tool requests are data, not authority. Malformed requests should
        # fail closed instead of reaching the policy/tool layer ambiguously.
        tool_calls = proposal.get("tool_calls", [])
        if not isinstance(tool_calls, list) or any(
            not isinstance(call, dict) or not call.get("name")
            for call in tool_calls
        ):
            issues.append("malformed tool_calls")

        score = max(0.0, min(1.0, confidence))
        if issues:
            score *= 0.6
        return VerificationReport(not issues, score, issues, facts, unknowns)
