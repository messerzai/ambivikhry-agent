# Profile context projection: keep dismissed values out of prompts

**Date:** 2026-10-24  
**Status:** isolated follow-up candidate; not merged or production-approved.  
**Parent:** `experiment/ambivikhry-profile-lifecycle-2026-10-23` at `bf4795109870a57745697e931a42b15a263b63d1`.

## Finding

The profile lifecycle candidate prevented generic hints from re-adding dismissed/superseded values to active list fields, but `profile_context()` serialized the entire profile to the model. The persisted object also contains `profile_history`, `profile_lifecycle`, and raw `observations`. Therefore an old value could remain model-visible even when it was no longer active. This is a control-plane/projection mismatch: persisted history is useful for audit, but should not automatically be prompt context.

## Hypothesis

If model-visible context is projected from current active profile fields only, dismissed/superseded values and raw historical task text will not be exposed through the profile-context serializer. This does not prove they are absent from every other data source, log, cache, or connected application.

## Change

- `JsonMemory.profile_context()` now allowlists version/status and known profile list fields.
- It filters values whose lifecycle status is `dismissed` or `superseded`.
- It excludes raw observations, lifecycle metadata, history, confidence internals, and unknown extension fields from the LLM context.
- Persistent profile storage and audit history are not deleted or rewritten.
- No Policy Gate, tool permission, autonomy, or biometric behavior changes.

## Tests added

- Dismissed and superseded values do not appear in model-visible context even if they remain in observations/history.
- Active values remain visible.
- Context projection does not mutate the persisted profile.
- Malformed lifecycle metadata does not expose history/observations.

## Risks

- Removing observations from model context may reduce personalization for details not yet consolidated into profile fields.
- This is prompt projection, not secure erasure: data remain in the persisted profile and audit trail. A future explicit deletion feature must separately define retention, export, backup, and deletion semantics.
- The projection cannot remove equivalent paraphrases embedded in active fields unless those items have matching lifecycle state.
- CI and the full suite must pass before promotion.

## Evaluation decision

Candidate only. Validate with targeted tests and the full repository CI; then run a paired temporal-intervention benchmark covering add → correct → stale hint → dismiss → stale hint → explicit confirm. Keep the parent branch and `main` unchanged.
