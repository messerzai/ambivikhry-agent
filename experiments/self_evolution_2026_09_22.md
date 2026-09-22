# Ambivikhry controlled self-evolution cycle — 2026-09-22

## Scope

Continue the experimental branch `experiment/comfort-expansion-2026-09-22` while preserving `main`, the Policy Gate, tool permissions, model endpoints, credentials, and sealed evaluation data.

## Fresh public evidence reviewed

1. **Socratic-SWE (2026)** proposes closed-loop self-evolution from historical solving traces into structured skills and targeted, execution-validated tasks. Its key transferable idea is to derive future evaluation/training tasks from observed failure modes rather than blindly generating more data.
2. **Auditing Harness Tampering in Self-Improving Agents (2026)** reports that self-improving agents can modify the harness in ways that create illusory gains or violate authorization/provenance/completeness. This supports an explicit acceptance gate that distinguishes capability improvement from harness tampering.
3. **Benchmark-poisoning work (2026)** demonstrates that poisoned evaluation data can induce persistent unsafe changes in self-modifying coding agents. Therefore sealed holdout data must remain immutable and inaccessible to the evolving agent.
4. **SWE-bench evaluation audits (2026)** show that benchmark quality and contamination materially affect apparent progress. Ambivikhry should not accept an improvement merely because one benchmark score rises.
5. **SWE-bench-Live (2026)** emphasizes trajectory submission and verification to reduce leakage and cheating. This supports preserving trajectory/lineage as first-class evidence.

## Proposed self-improvements

### E1 — Trace-derived curriculum
Derive candidate future tests from recurring failure classes, but keep the generated tests outside the sealed holdout until independently reviewed.

**Status:** proposal only.

### E2 — Explicit evolution acceptance gate
Added `ambivikhry/evolution_gate.py`.

A candidate can only reach `accept_experimental` when evidence quality, independent replication, regression, and holdout thresholds are all met. Any candidate that expands authority, changes the Policy Gate, or mutates the holdout is rejected regardless of performance.

**Status:** accepted into experimental branch.

### E3 — Harness-tampering checks
Add adversarial regression cases for policy mutation, holdout mutation, authority expansion, evaluator manipulation, and provenance loss.

**Status:** partially implemented through the evolution gate; broader adversarial suite remains pending.

### E4 — Continuous benchmark refresh
Use fresh, non-stationary tasks where possible and retain a frozen holdout for comparability.

**Status:** proposal only; no external benchmark was imported automatically.

## Tests

New regression tests cover:
- strong evidence candidate accepted experimentally;
- insufficient evidence held;
- authority expansion rejected;
- Policy Gate mutation rejected;
- holdout mutation rejected;
- invalid evidence scores rejected.

The existing comfort-expansion tests remain unchanged. Full CI should be treated as the authoritative regression result after GitHub Actions completes.

## Rejected changes

- automatic permission escalation;
- changing model endpoints;
- adding tools without explicit approval;
- modifying Policy Gate;
- modifying or reading sealed holdout data;
- automatic promotion to `main`;
- treating a single benchmark increase as proof of improvement.

## Lineage

Base experiment: `experiment/comfort-expansion-2026-09-22`.

New commits:
- `47f2805` — bounded evolution acceptance gate;
- `4dd87cd` — regression tests for the gate;
- this report — research/evolution lineage.

`main` remains untouched by this cycle.

## Current verdict

**CONTINUE / EXPERIMENTAL ONLY.**

The new gate is a structural improvement because it makes self-modification more auditable and rejects authority/policy/holdout tampering. It is not evidence that Ambivikhry has achieved autonomous reliable self-improvement. The next cycle should test whether trace-derived curricula improve held-out task performance without increasing policy or provenance failures.
