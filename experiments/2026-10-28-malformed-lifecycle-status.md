# Controlled cycle — malformed profile lifecycle metadata
Date: 2026-10-28

## Baseline and hypothesis
Baseline: `experiment/ambivikhry-bounded-profile-context-2026-10-27`, commit
`c14438e7bde1ca1810a2535c108ed4ad6a6501e4`.

Hypothesis: malformed lifecycle status values must not crash prompt projection or
silently reactivate a value. A lifecycle entry is considered eligible for model
use only when it is an explicit `confirmed` record. Legacy items with no
lifecycle entry remain eligible for backward compatibility.

## Change
- Centralized lifecycle eligibility in `JsonMemory._lifecycle_state_blocks`.
- Non-dictionary item records, non-string status values, and unknown status
  strings fail closed for that item.
- A malformed lifecycle map for a particular field excludes that field from
  model-visible context.
- Inferred hints are skipped when their field lifecycle map is malformed.
- Explicit user teaching can replace a malformed field map and write a new
  confirmed record.

No Policy Gate, tool permissions, autonomy, biometric behavior, or main-branch
files were changed. The persisted profile is not deleted or rewritten by
`profile_context`; ordinary `personalize` still records the current task as
an observation.

## Regression coverage
`tests/test_profile_lifecycle_malformed_metadata.py` covers:
1. list/object/unknown status values;
2. malformed per-field lifecycle map;
3. prevention of inferred reintroduction;
4. explicit-user recovery of a malformed per-field map.

## Independent criticism and limits
- A malformed *root* `profile_lifecycle` object is now handled by
  quarantining pre-existing string values as `unknown`; they remain persisted
  but are excluded from model context until explicitly reconfirmed. This
  recovery path still needs review against real legacy profiles.
- Exact status allowlisting may exclude data written by an external extension
  using a status other than `confirmed`, `dismissed`, or `superseded`.
- This is structural validation, not semantic forgetting, secure erasure,
  prompt-injection prevention, or proof of better user-facing personalization.

## Acceptance
- Full repository CI must pass on supported Python versions.
- Verify this PR targets the existing experimental branch, not `main`.
- Keep the PR draft until a separate review of root-level corruption and
  temporal benchmark coverage is complete.
