"""Red-team phase 1: deliberately attacks assumptions in the current core.

This suite is designed to FAIL when a control is only nominally present.
A failure is evidence of a hardening target, not a test-suite bug.

No network, credentials, subprocesses, or irreversible actions are used.
"""
from ambivikhry.autonomy import AutonomousController, AutonomyConfig
from ambivikhry.policy import PolicyGate
from ambivikhry.tools import Tool
from ambivikhry.verifier import Verifier


def expect(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def main():
    v = Verifier()
    p = PolicyGate()
    findings = []

    tests = [
        ("R1 verifier must not trust a bare facts field",
         lambda: expect(
             not v.verify({"decision": "x", "confidence": 0.9, "facts": ["invented"]}).passed,
             "facts are accepted without provenance/evidence")),
        ("R2 verifier must distinguish an actual source from a source flag",
         lambda: expect(
             not v.verify({"decision": "x", "confidence": 0.9, "sources": ["fake"]}).passed,
             "arbitrary source strings are not independently verified")),
        ("R3 policy approval must not be a freely supplied boolean",
         lambda: expect(
             not p.evaluate(Tool("irreversible", risk="high"), user_approved=True).requires_approval,
             "approval is represented only as an unbound boolean")),
        ("R4 autonomy must enforce irreversible-approval configuration",
         lambda: expect(
             AutonomyController(AutonomyConfig(require_approval_for_irreversible=True)).config.require_approval_for_irreversible,
             "configuration flag is missing")),
        ("R5 autonomy must account for per-cycle tool-call budget",
         lambda: expect(
             AutonomyController(AutonomyConfig(max_tool_calls_per_cycle=0)).config.max_tool_calls_per_cycle == 0,
             "tool budget exists but execution path must enforce it")),
    ]

    for name, fn in tests:
        try:
            fn()
            findings.append((name, "PASS"))
        except Exception as exc:
            findings.append((name, f"FINDING: {exc}"))

    print("AMBIVIKHRY RED-TEAM PHASE 1")
    for name, result in findings:
        print(f"{result}: {name}")

    hard_findings = sum(result.startswith("FINDING") for _, result in findings)
    print(f"\nHardening findings: {hard_findings}/{len(findings)}")
    print("Interpret FINDING as an uncovered control weakness to convert into a regression test.")


if __name__ == "__main__":
    main()
