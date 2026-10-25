# Profile context sanitization: reject malformed persisted values

**Date:** 2026-10-25  
**Status:** experimental candidate; not promoted.  
**Parent before this cycle:** `be6a6ee613c38d86e028df090c94a18eb06bd9d7`  
**Implementation commit:** `2e0f1d87b356fbf39e72bda5072c9a18454602df`  
**Regression-test commit:** `474df9e6c006f83f3cbff8cbd3954a804ea542e8`

## Finding

The previous projection allowlisted known profile fields and removed dismissed/superseded values, observations, and lifecycle metadata. However, a malformed or legacy profile could still contain arbitrary JSON objects, arrays, numbers, nulls, blank strings, or oversized strings inside an otherwise allowed list field. The projection appended these values to the model context unchanged. It also passed `version` and `status` without checking their types.

This is a confirmed input-validation gap in the projection code. It does not prove that a real user profile was corrupted or that a model actually disclosed such a value.

## Hypothesis

If model-visible profile items are restricted to non-empty strings of at most 2,000 characters, and metadata types are checked, malformed persisted payloads will not be copied into the model context. Valid compact preferences remain available.

## Change

In `JsonMemory.profile_context()`:

- require `version` to be a positive integer (excluding booleans); otherwise use 1 in the projection;
- require `status` to be a non-empty string of at most 64 characters; otherwise use `unknown`;
- omit non-string, blank/whitespace-only, and over-2,000-character list entries from model context;
- preserve the persisted profile unchanged;
- retain the existing lifecycle filter for `dismissed` and `superseded` entries.

This is context projection, not deletion. Omitted values may remain in the stored profile and other logs.

## Tests and evidence

Added `tests/test_profile_context_sanitization.py` with four tests:

1. malformed/non-string/blank/oversized values are omitted;
2. malformed `version` and `status` metadata are replaced by safe defaults;
3. valid metadata and valid preferences remain visible;
4. projection does not mutate the persisted input.

GitHub Actions workflow run `40217398800` (run number 416) completed `pytest -q` successfully on Python 3.10, 3.11, 3.12, and 3.13 for the regression-test commit `474df9e6c006f83f3cbff8cbd3954a804ea542e8`.

This is full-suite CI evidence for this branch head, not a real-user personalization benchmark or a proof of secure erasure.

## Independent criticism / risks

- The 2,000-character cap is an engineering guard, not a scientifically optimized threshold. A legitimate long item may be omitted from prompts while remaining stored.
- Type validation cannot detect semantic paraphrases of a dismissed value in another valid string.
- Current task text and audit events are separate storage paths; this patch does not implement deletion or retention controls for them.
- The browser prototype update for Zhivoy Uzor is a separate local artifact and is not part of this repository commit.

## Decision

`CANDIDATE / NOT PROMOTED`. Keep `main`, Policy Gate, tool permissions, and autonomy unchanged. Next evaluation should use paired temporal interventions and report both stale-value exposure and retention of valid current preferences. A separate retention/deletion design is needed before claiming that user data can be erased across all storage tiers.
