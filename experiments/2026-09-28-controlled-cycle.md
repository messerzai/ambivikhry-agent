# Controlled Evolution Cycle — 2026-09-28

## Scope
Fresh public research on self-improving and agentic systems; proposals limited to prompts, reasoning, tests, memory/evaluation architecture. No authority expansion, no Policy Gate changes, no main changes, no human-approval bypass.

## Public evidence reviewed
1. **SEAGym (2026-06-16)**: self-evolution needs separate update evidence, frozen validation, ID/OOD transfer, replay/retention, and saved snapshots; frequent updates can fail to improve holdout performance and can cause runtime regressions. citeturn917753view0
2. **EvoMemBench (2026-05-18)**: memory should be evaluated on two axes — in-episode vs cross-episode and knowledge vs execution; long-context baselines remain competitive and no single memory form dominates. citeturn917753view1
3. **MemMA (2026-09-03)**: memory construction, retrieval, and downstream repair should be coordinated rather than treated as isolated subroutines. citeturn987734search1
4. **MIRROR (2026)**: self-prediction is imperfect; external metacognitive control can reduce confident failures, so self-confidence must not directly authorize action. citeturn987734search7
5. **AFTER (2026-06-22)**: procedural memory gains need transfer tests across tasks, roles, and model backbones; diverse traces can transfer better than single-model traces. citeturn917753view4

## Proposals
### P1 — Snapshot contract
Freeze evaluator, acceptance thresholds, and Policy/authority invariants per epoch. Changes to evaluator or thresholds are out-of-band and require human approval.

### P2 — Five-view evaluation
For each candidate snapshot record:
- update evidence;
- frozen validation;
- ID transfer;
- OOD transfer;
- replay/retention.
Add cost and latency.

### P3 — Memory utility matrix
Score memory separately for:
- knowledge retention;
- execution/procedure reuse;
- in-episode revision;
- cross-episode transfer;
- action/tool-choice impact.

### P4 — External metacognitive gate
Confidence is advisory only. Require an independent verifier or abstention rule before high-impact action; calibration is measured against actual outcomes.

### P5 — Provenance + repair loop
Every memory item stores source, timestamp/epoch, task context, confidence, supersession state, and outcome link. Failed later behavior can open a repair proposal; silent overwrite is forbidden.

### P6 — Diversity and model-transfer split
Separate same-model gains from cross-model and cross-domain transfer. A candidate cannot be promoted on same-model ID gains alone.

## Independent verification
- Static invariant scan: PASS (policy/authority terms preserved; no new tool or permission declarations in this change set).
- Proposal/evaluator separation: PASS (this report proposes; verifier criteria are frozen in the report).
- Holdout design: DEFINED, NOT EXECUTED in this GitHub-only run.
- Runtime regression suite: NOT EXECUTED in this GitHub-only run.
- Main branch protection: PASS; no write was made to main.
- Human approval boundary: PASS; no promotion or deployment action taken.

## Rejected changes
- Self-modifying evaluator or threshold updates inside the same epoch.
- Automatic tool-registry expansion or privilege changes.
- Using confidence as authorization.
- Treating retrieval success as proof of learning.
- Silent memory replacement.
- Promoting from same-model ID score without OOD/replay evidence.
- Removing holdout sets to increase apparent speed.

## Authority-extension attempts
Observed in this cycle: none.

## Result
Status: **INCONCLUSIVE — protocol proposals recorded; runtime/holdout execution pending**.

## Lineage
- Parent commit: 773d2de0e35105ea8b45162dbe06dd2180daab09
- Branch: experiment/ambivikhry-self-research-2026-09-24
- Files added: this report and machine-readable proposal record
