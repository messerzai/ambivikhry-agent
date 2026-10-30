# Personalization input-boundary validation

**Date:** 2026-10-30  
**Status:** experimental candidate; not promoted.  
**Parent:** PR #27 head `58f339c3dad001b77171ce1ffd45671706604437`.

## Observation

`JsonMemory.personalize()` previously iterated each supplied hint field and coerced every element with `str(value)`. This allowed malformed inputs to become profile text:
- a string supplied instead of a list could be split into individual characters;
- a dictionary could be iterated as keys;
- nested objects, lists, numbers, and `None` could be stringified and persisted;
- overlong values could be stored even though the prompt projection later excluded them.

This is a confirmed input-validation defect in the code path. No evidence was found that it caused an incident in production.

## Hypothesis

Validating the ingestion boundary before mutating the profile will prevent malformed model-produced hints from becoming persistent profile text, while preserving valid string hints and explicit user confirmation semantics.

## Change

- Require `task` to be a non-empty string.
- For inferred/model-produced hints, accept only list/tuple containers and non-empty strings up to `MAX_PROFILE_ITEM_CHARS`; skip malformed containers and entries without coercion.
- For explicit user teaching, reject malformed containers or entries with `ValueError` rather than silently accepting only part of the submission.
- Validate confidence metadata as a mapping of non-empty keys to finite numeric values in the inclusive range [0, 1]; filter malformed inferred metadata and reject malformed explicit metadata.
- Keep lifecycle, context projection, Policy Gate, tool permissions, autonomy, and biometric behavior unchanged.
- Validate before loading/mutating the profile so rejected explicit submissions do not persist partial changes.

## Validation

The first CI run exposed an additional lifecycle persistence defect: explicit confirmation updated a temporary empty dictionary when a field lifecycle map did not yet exist. The fix now registers that map with `setdefault` before writing the `confirmed` state. The existing explicit-teaching test then verifies that the confirmation survives persistence.

New test file: `tests/test_personalization_input_validation.py`.

Scenarios:
1. Nested objects, arrays, numbers, nulls, blanks, and overlong strings are skipped from inferred hints.
2. A string or mapping is not iterated as a hint collection.
3. Explicit teaching rejects malformed containers and values without writing a profile.
4. Valid explicit strings remain accepted and marked `confirmed`.
5. Empty and non-string tasks are rejected before persistence.
6. Malformed confidence containers, booleans, strings, non-finite values, and out-of-range scores cannot crash or contaminate stored confidence metadata.

Run from repository root:

```bash
pytest -q tests/test_personalization_input_validation.py tests/test_profile_lifecycle.py tests/test_profile_lifecycle_malformed_metadata.py tests/test_profile_context_sanitization.py tests/test_profile_context_budget.py
```

## Risks and limits

- Explicit callers that previously passed a scalar string instead of a list will now receive `ValueError`; this is an intentional contract clarification.
- Inferred malformed entries and confidence values are silently skipped; this avoids crashes and unsafe coercion but does not yet emit a per-field rejection diagnostic.
- This validates profile hint inputs only. It does not sanitize arbitrary task text, observations, external tools, or other persistence paths.
- It does not establish semantic forgetting, secure erasure, prompt-injection resistance, or improved user-facing personalization.
- Full test and CI results must be checked after this branch commit; no promotion is authorized by this note.

## Decision

Keep as a child experiment based on PR #27's current head. Do not merge, retarget to `main`, change Policy Gate, or expand permissions.
