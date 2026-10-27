# Bounded profile-context projection

**Date:** 2026-10-27  
**Status:** experimental candidate; not promoted.  
**Parent:** `experiment/ambivikhry-bounded-profile-context-2026-10-27`.

## Hypothesis

A deterministic upper bound on the serialized profile context can limit prompt growth and reduce the amount of stale or malformed material that reaches the model, while retaining the newest useful values across all profile fields.

## Change

- Maximum 20 eligible values per field.
- Maximum 2,000 characters per individual value.
- Maximum 20,000 characters for the serialized profile projection.
- Newest values are considered first in round-robin order across the nine profile fields. Once an older value for a field does not fit, older values from that field are not admitted ahead of it.
- The persisted profile is not mutated and no data is deleted by projection.

These thresholds are engineering heuristics selected for a bounded experiment. They are not scientifically established optimal values and must be tuned against real task utility and context-tokenization behavior.

## Research grounding

- AMV-L argues that persistent memory needs a bounded request-path working set rather than relying only on age-based retention: https://arxiv.org/abs/2603.04443
- LongMemEval evaluates temporal reasoning, knowledge updates, and abstention in long-running interactions: https://arxiv.org/abs/2410.10813

These sources motivate bounded retrieval and temporal tests; they do not validate this implementation's thresholds.

## Validation protocol

Run:

```bash
pytest -q tests/test_profile_context_budget.py tests/test_profile_context_sanitization.py tests/test_profile_lifecycle.py tests/test_temporal_memory_interventions.py
python benchmarks/temporal_memory_interventions.py
```

Acceptance:
1. Serialized projection never exceeds 20,000 characters.
2. With nine fields containing 20 strings of 1,800 plain characters each, the newest item from every field remains visible.
3. No field exposes more than 20 items.
4. Existing lifecycle, sanitization, and temporal-intervention tests remain green.
5. Source profile is not mutated.

## Risks and regression concerns

- Valid older preferences may be omitted when the budget is exhausted.
- Character count is only a proxy for token count and may differ by model tokenizer.
- Selection prioritizes recency by list order; imported legacy lists may not be chronologically ordered.
- This limits only the model-visible projection. It does not erase source text from profile files, audit logs, backups, or other stores.
- It does not mitigate semantic prompt injection in an otherwise valid string.

## Decision

Keep isolated. Do not merge, alter `main`, change Policy Gate, or expand agent permissions. Require a utility-retention benchmark and a separate audit of raw task-text retention before any promotion.
