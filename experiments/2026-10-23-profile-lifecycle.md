# Profile lifecycle: explicit correction, dismissal, and confirmation

**Date:** 2026-10-23  
**Status:** isolated candidate; not production-approved.  
**Base:** `experiment/ambivikhry-controlled-cycle-2026-10-09`.

## Research basis

- Uddin et al., *From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents*, Findings of ACL 2026. The paper introduces FAMA, which penalizes use of obsolete or invalidated memory, and reports that memory systems often reuse invalid memories. https://aclanthology.org/2026.findings-acl.1337/
- Qian et al., *Toward User-Conditioned Evaluation of Personal LLM Agents under Temporal Interventions*, arXiv:2607.21635 (2026). The paper argues for replaying temporal changes across persistent user states and checking downstream effects, not evaluating memory in isolation. https://arxiv.org/abs/2607.21635

These works motivate the risk model; they do not validate this implementation or establish that the current agent exhibits the same measured error rates.

## Hypothesis

If a user explicitly corrects or dismisses a profile item, later generic hints should not silently reintroduce the obsolete value. A later explicit confirmation may reactivate it.

## Change in this candidate

- Adds backward-compatible `profile_lifecycle` state and a bounded `profile_history` trail to the JSON profile.
- Adds `JsonMemory.revise_profile_item(field, value, action, replacement=None)` with explicit `confirm`, `dismiss`, and `correct` operations.
- Prevents later `personalize(..., hints=...)` calls from re-adding values whose latest lifecycle status is `dismissed` or `superseded`.
- Keeps lifecycle history separate from audit metadata; audit events record field/action only and do not duplicate profile text.
- Leaves agent prompts, Policy Gate, tool permissions, and autonomous write authority unchanged. The method is an explicit application/API hook; this commit does not connect it to a UI or let the model invoke it automatically.

## Acceptance checks

1. Correcting an active item replaces it and records both old and new state.
2. Dismissed/superseded values are not reintroduced by later hints.
3. Explicit confirmation can reactivate a previously dismissed value.
4. Legacy profiles without lifecycle keys remain readable and can be updated.
5. Audit metadata contains no profile value.
6. Invalid fields/actions and correction of a non-active value fail closed.
7. Event history is bounded to 500 records while current lifecycle status remains available.
8. Existing test suite and four-version GitHub Actions matrix pass before considering promotion.

## Risks and limitations

- This is not temporal reasoning by the LLM; it is a deterministic memory lifecycle guard.
- Existing values that have no lifecycle status remain active for backward compatibility.
- Explicit confirmation can reactivate a value by design.
- The status map can grow with unique profile values; a future retention policy needs user-visible export/delete semantics.
- Atomic profile-file replacement and audit-file append are not a single transaction. If audit writing fails after profile persistence, callers must inspect the saved profile before retrying.
- No automatic profile updates, biometric inputs, new tool permissions, or Policy Gate changes are introduced.

## Evaluation plan

Run the existing tests plus `pytest -q tests/test_profile_lifecycle.py tests/test_personalization.py` on Python 3.10–3.13. Compare a fixed sequence baseline/candidate: add item → correct → repeat stale hint → dismiss → repeat stale hint → explicitly confirm. Report reintroduction rate, correction retention, profile write errors, and existing-suite regressions. Do not claim user-level quality gains until a separate consented pilot compares outputs on fixed tasks.
