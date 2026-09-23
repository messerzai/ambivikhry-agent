# Controlled evolution cycle — 2026-09-23

## Scope
Fresh public material on self-improving and agentic systems was reviewed. The cycle targeted bounded improvements to evaluation, promotion logic, prompt/reasoning discipline, regression coverage, and lineage recording.

## Public findings used

1. A 2026 survey frames an agent as a coupled system of model + prompts + memory + tools + control logic, and recommends fixed-budget trajectories, held-out transfer, overhead accounting, and regression tracking rather than peak score alone.
2. SkillsBench reports that curated procedural skills can help, but self-generated skills do not reliably help on average; focused skills outperform comprehensive documentation. This supports conservative promotion of small, verified artifacts instead of automatic accumulation.
3. Harness-tampering audits report that self-improving agents may alter execution/evaluation/recording harnesses and create illusory gains. This supports explicit rejection of evaluator, policy, authority, and tool-registry changes.
4. PILOT-style supervisor/worker loops suggest that mid-run supervision and early aborts can reduce wasted work; this cycle records the idea as a future proposal, not as an accepted capability change.
5. EvoMemBench/PRISM-style memory evaluation motivates separate checks for retention, update consistency, cross-episode transfer, and judge integrity.

## Implemented changes

- Added `ambivikhry/adaptive_eval.py`.
- Added `tests/test_adaptive_eval.py`.
- Exported the new gate and bumped package version to `2.6.3`.

The new `AdaptivePromotionGate` requires:

- independent evaluation;
- complete provenance;
- matched budget (within 5%); 
- positive candidate gain;
- positive holdout transfer;
- no regression drop;
- no evaluator change;
- no Policy Gate change;
- no authority delta;
- no tool-registry change.

Decision values are `accept_experimental`, `hold`, or `reject`.

## Regression / holdout evaluation

The new tests cover:

- bounded transfer accepted;
- no holdout transfer held;
- regression drop rejected;
- authority/evaluator changes rejected;
- unmatched budget held.

The repository workflow remains the existing GitHub Actions matrix for Python 3.10–3.13. This automation run did not have a local execution environment for running pytest directly, so the code was committed and the remote CI result must be treated as the authoritative test outcome once available.

## Rejected proposals

- automatic self-generated skill promotion without independent verification;
- evaluator changes made by the candidate;
- modifications to Policy Gate;
- authority or credential expansion;
- automatic Tool Registry growth;
- accepting a score increase that costs materially more budget;
- accepting a candidate that improves only in-sample score but fails holdout transfer;
- adding new supervisor/worker runtime control in this cycle because it would require broader orchestration changes and human review.

## Attempts to expand authority

No authority-expansion attempt was observed in this cycle. The new gate rejects any non-zero `authority_delta` and any evaluator, policy, or tool-registry change.

## Branch protection

`main` was not modified. All changes were written to `experiment/ambivikhry-v3-unified-2026-09-22`.

## Status

`EXPERIMENTAL / REMOTE CI PENDING`
