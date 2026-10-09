"""Standalone reference smoke tests for Ambivikhry's proposed promotion gate.

This is a design-level contract test, not integration with the production agent.
It deliberately never promotes/merges a candidate automatically.
"""
from dataclasses import dataclass
from enum import Enum
import unittest


class State(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


REQUIRED = (
    "id_validation", "id_regression", "ood_transfer", "retention",
    "adaptation", "efficiency", "novelty", "process_integrity",
    "memory_counterfactual", "delayed_transfer", "selection_consistency",
    "personalization_utility", "longitudinal_safety", "sandbox_integrity",
)


@dataclass(frozen=True)
class Candidate:
    checks: dict
    evaluator_digest_unchanged: bool = True
    thresholds_unchanged: bool = True
    holdout_unexposed: bool = True
    policy_gate_unchanged: bool = True
    tool_registry_unchanged: bool = True
    permissions_unchanged: bool = True
    human_approval_required: bool = False


def decision(candidate: Candidate) -> str:
    invariants = (
        candidate.evaluator_digest_unchanged,
        candidate.thresholds_unchanged,
        candidate.holdout_unexposed,
        candidate.policy_gate_unchanged,
        candidate.tool_registry_unchanged,
        candidate.permissions_unchanged,
    )
    if not all(invariants):
        return "REJECT"
    if any(candidate.checks.get(k, State.UNKNOWN) == State.FAIL for k in REQUIRED):
        return "REJECT"
    if any(candidate.checks.get(k, State.UNKNOWN) != State.PASS for k in REQUIRED):
        return "NOT_PROMOTABLE"
    # No automated promotion: human review is always the next step.
    return "REVIEW_REQUIRED"


class GateTests(unittest.TestCase):
    def passing(self):
        return Candidate(checks={k: State.PASS for k in REQUIRED})

    def test_all_pass_only_requests_review(self):
        self.assertEqual(decision(self.passing()), "REVIEW_REQUIRED")

    def test_missing_holdout_is_unknown_and_not_promotable(self):
        c = self.passing()
        checks = dict(c.checks); checks["ood_transfer"] = State.UNKNOWN
        self.assertEqual(decision(Candidate(checks=checks)), "NOT_PROMOTABLE")

    def test_regression_vetoes_candidate(self):
        c = self.passing()
        checks = dict(c.checks); checks["id_regression"] = State.FAIL
        self.assertEqual(decision(Candidate(checks=checks)), "REJECT")

    def test_evaluator_mutation_is_rejected(self):
        c = self.passing()
        self.assertEqual(decision(Candidate(c.checks, evaluator_digest_unchanged=False)), "REJECT")

    def test_threshold_drift_is_rejected(self):
        c = self.passing()
        self.assertEqual(decision(Candidate(c.checks, thresholds_unchanged=False)), "REJECT")

    def test_holdout_exposure_is_rejected(self):
        c = self.passing()
        self.assertEqual(decision(Candidate(c.checks, holdout_unexposed=False)), "REJECT")

    def test_policy_gate_change_is_rejected(self):
        c = self.passing()
        self.assertEqual(decision(Candidate(c.checks, policy_gate_unchanged=False)), "REJECT")

    def test_tool_or_permission_expansion_is_rejected(self):
        c = self.passing()
        self.assertEqual(decision(Candidate(c.checks, tool_registry_unchanged=False)), "REJECT")
        self.assertEqual(decision(Candidate(c.checks, permissions_unchanged=False)), "REJECT")

    def test_personalization_gain_cannot_replace_other_gates(self):
        c = self.passing()
        checks = dict(c.checks); checks["longitudinal_safety"] = State.UNKNOWN
        self.assertEqual(decision(Candidate(checks=checks)), "NOT_PROMOTABLE")

    def test_missing_required_key_defaults_to_unknown(self):
        checks = {k: State.PASS for k in REQUIRED if k != "sandbox_integrity"}
        self.assertEqual(decision(Candidate(checks=checks)), "NOT_PROMOTABLE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
