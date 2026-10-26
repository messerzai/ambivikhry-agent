# Temporal memory intervention benchmark v1

**Date:** 2026-10-26  
**Status:** experimental evaluation harness; not a promotion decision.  
**Parent:** `experiment/ambivikhry-profile-context-projection-2026-10-24`.

## Question

Does the profile-context projection suppress values that have been dismissed or superseded while preserving current values and allowing explicit user re-confirmation?

## Reproducible command

```bash
python benchmarks/temporal_memory_interventions.py
pytest -q tests/test_temporal_memory_interventions.py
```

The harness is deterministic and makes no LLM calls. It reports JSON for four interventions, including an unrecognized free-form status string that must not be treated as control metadata:

1. dismiss a value, then replay an inferred hint;
2. correct a value, then replay the superseded hint;
3. explicitly re-confirm a previously dismissed value;
4. provide malformed legacy profile content.

## Metrics

- `legacy_baseline_stale_exposure_rate`: proportion of stale markers visible when the entire persisted profile is serialized, reproducing the pre-projection baseline.
- `candidate_stale_exposure_rate`: proportion of stale markers visible in the current `profile_context()` projection.
- `current_value_retention_rate`: proportion of expected current values retained in candidate context.
- `explicit_reconfirmation_rate`: proportion of explicit re-confirmations visible after the user action.

The current candidate includes an allowlist for model-visible status metadata (`bootstrap`, `active`, `unknown`); unrecognized strings map to `unknown`. The pass condition is zero candidate stale-marker exposure, 100% retention of expected current values, 100% explicit re-confirmation, and a non-zero stale exposure rate in the legacy baseline.

## Limits

This benchmark measures storage and context-projection behavior only. It does **not** test semantic paraphrases, model behavior, real-user utility, privacy across other logs/backups, or secure erasure. The markers are exact strings; passing cannot establish that a model will never infer or repeat a semantically similar value. The baseline is a local comparator, not a benchmark against a running production deployment.

## Decision rule

Keep the candidate isolated. A pass is evidence for these four deterministic cases only. Do not merge, change `main`, alter Policy Gate, or increase agent permissions based on this result alone. Follow with adversarial paraphrase cases and a separate audit of retention/deletion paths.
