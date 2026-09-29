# Controlled Evolution Cycle — 2026-09-29

## Scope
Fresh public research on self-improving and agentic systems; proposals limited to prompt/reasoning design, evaluation, memory, provenance, and architecture. No authority expansion, no Policy Gate changes, no main changes, no human-approval bypass.

## Public evidence reviewed

1. **AgentSLABench (2026-08-01)** proposes resource-aware evaluation with correctness plus latency, cost, compute, memory, and network budgets, sealed test sets, and an Efficiency-Adjusted Success Rate. This supports adding explicit resource budgets and cost-aware gates to Ambivikhry evaluation. citeturn582673academia26
2. **PAST-Bench (2026-08-04)** isolates whether retained experience improves later fresh-session behavior and checks the intended save → retrieve → update pathway rather than relying on headline gains alone. This supports pathway evidence and matched memory-on/off controls. citeturn582673academia27
3. **EvoMemBench (2026-05-18)** separates memory scope (in-episode vs cross-episode) and content (knowledge vs execution), finding no universal memory method. This supports typed memory and multi-axis scoring. citeturn582673academia25
4. **AML Agent Memory Leaderboard (2026-08-12 update)** emphasizes versioned public evaluation contracts and warns that scoring changes should become a new contract version rather than silently changing old results. This supports epoch-frozen contracts and explicit benchmark versioning. citeturn582673search2
5. **MemAudit (2026)** distinguishes what is stored from what is retrievable and evaluates both full-store and top-k retrieval against hidden user state. This supports separate store-audit and retrieval-audit metrics. citeturn582673search3
6. **ASG-SI (2025-12-28)** frames self-improvement as promotion of auditable, reusable skills through verifier-backed replay and contract checks, with explicit reward decomposition and governance. This supports skill-artifact promotion rather than opaque self-modification. citeturn582673academia28

## Proposed changes

### P1 — Resource-bounded evaluation contract
Add declared per-episode budgets for time, tool calls, network, memory, and cost. Record correctness and an efficiency-adjusted metric. A candidate cannot be promoted by accuracy alone if it violates a declared budget.

### P2 — Dual memory audit
For each memory experiment, report:
- stored-state fidelity;
- top-k retrievability;
- downstream action/tool-choice impact;
- save → retrieve → update → later-task pathway evidence.

### P3 — Epoch-frozen benchmark contract
Freeze evaluator, thresholds, task split, budget policy, and authority invariants for an epoch. Any evaluator or threshold change creates a new contract version and is not a silent in-place update.

### P4 — Skill-artifact promotion
Represent a claimed improvement as a typed artifact with interface, preconditions, postconditions, provenance, replay trace, and known failure modes. Promote only after verifier-backed replay and holdout checks.

### P5 — Prompt/reasoning revision
Require explicit output fields:
- objective;
- facts;
- hypotheses;
- unknowns;
- proposed action;
- verification plan;
- expected utility;
- resource budget;
- abstain/escalate condition;
- provenance references.

### P6 — Negative-control suite
Add sealed negative controls for:
- stale-memory use;
- memory poisoning;
- holdout leakage;
- evaluator tampering;
- reward/metric gaming;
- unauthorized tool/permission expansion;
- budget evasion.

## Independent verification

- Branch lineage inspected: current experimental head before this cycle = `626b537b34c048ceac644a3ef7413463147c8549`.
- `main` ref inspected: `36445a8edc88174688e312bef4b1082df8c11f98`.
- Main-branch write: **none**.
- Static proposal scan: **PASS** — no new authority, permission, replication, or Policy Gate bypass mechanism proposed.
- Evaluator/proposer separation: **PASS** — acceptance contract is frozen in this report; no self-authorized promotion.
- Runtime regression suite: **NOT EXECUTED** in GitHub-only automation context.
- Sealed blind/holdout evaluation: **NOT EXECUTED** in GitHub-only automation context.
- Therefore no capability improvement is claimed.

## Rejected changes

- Self-modifying evaluator or threshold updates inside the same epoch.
- Accuracy-only promotion without resource accounting.
- Treating memory retrieval as proof of learning.
- Silent benchmark-contract edits.
- Opaque parameter or policy mutation.
- Automatic tool-registry or permission expansion.
- Any action that would bypass human approval or Policy Gate.

## Authority-extension attempts

Observed in this cycle: **none**.

## Result

**INCONCLUSIVE — proposals and lineage recorded; runtime regression and holdout execution remain pending.**

## Lineage

- Repository: `messerzai/ambivikhry-agent`
- Branch: `experiment/ambivikhry-self-research-2026-09-24`
- Parent commit: `626b537b34c048ceac644a3ef7413463147c8549`
- Main unchanged at: `36445a8edc88174688e312bef4b1082df8c11f98`
- Files added:
  - `experiments/2026-09-29-controlled-cycle.md`
  - `experiments/2026-09-29-controlled-cycle.json`
