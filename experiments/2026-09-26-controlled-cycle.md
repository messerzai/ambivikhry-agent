# Controlled Evolution Cycle — 2026-09-26

## Scope and invariants
Target: `experiment/ambivikhry-self-research-2026-09-24` only.
`main` before cycle: 36445a8edc88174688e312bef4b1082df8c11f98.
No changes to `main`, Policy Gate, tool registry, secrets, replication, deployment, or approval boundaries.

## Fresh public evidence reviewed
1. **AIDE² / Recursive self-improvement of AI research agents** — recursive code/harness improvement with hidden evaluations and held-out transfer; the key lesson is that the improvement loop must be judged on unseen tasks, not only the visible score. https://arxiv.org/abs/2609.26457
2. **MemoryArena** — multi-session agent-memory benchmark with interdependent tasks; reports that agents near saturation on dialogue-memory tests can still perform poorly when memory must guide later actions. https://arxiv.org/abs/2602.16313
3. **AMA-Bench** — long-horizon memory benchmark built from agent trajectories, tool outputs and expert/rule-based QA; highlights causal and objective retrieval gaps. https://arxiv.org/abs/2602.22769
4. **Red Queen Gödel Machine** — co-evolving agents and evaluators in fixed epochs; supports changing evaluators only at controlled boundaries rather than allowing continuous self-redefinition. https://arxiv.org/abs/2606.26294
5. **EvoAgentBench** — evaluates self-evolution through transfer of reusable procedures/abilities across domains, not just single-episode success. https://arxiv.org/abs/2607.05202
6. **Jev-Mem / typed memory direction** — supports explicit structure, provenance and adaptive retrieval rather than flat note accumulation. https://arxiv.org/abs/2605.14401
7. **Contextual Agentic Memory is a Memo, Not True Memory** — warns that lookup-heavy memory can fail on compositional generalization and remain vulnerable to poisoning; this is treated as a design warning, not settled fact. https://arxiv.org/abs/2604.27707
8. **EvoMemBench** — evaluates memory across in-episode/cross-episode and knowledge/execution axes, useful as a regression matrix design reference. https://arxiv.org/abs/2605.18421

## Proposals generated
### P1 — Epoch-frozen acceptance contract
Separate proposer, critic and certifier; freeze acceptance criteria within a cycle; permit changes to the evaluator only at a human-reviewed epoch boundary.
**Decision:** ACCEPT as protocol design. No authority change.

### P2 — Transfer-first self-improvement score
Add a required transfer score: performance on unseen tasks that share procedure but not surface form.
**Decision:** ACCEPT as test design. Runtime not executed here.

### P3 — Typed causal memory record
Record `event → condition → action → outcome → uncertainty → provenance → invalidation` instead of only summaries.
**Decision:** ACCEPT as implementation hypothesis. Runtime not executed here.

### P4 — Two-axis memory regression
Evaluate both knowledge retention and execution/procedure reuse across sessions.
**Decision:** ACCEPT as benchmark design.

### P5 — Poisoning and evaluator-tamper negatives
Add negative controls for memory poisoning, holdout leakage, evaluator tampering and benchmark overfitting.
**Decision:** ACCEPT as hard regression gate.

### P6 — Adaptive verification budget
Use cheap checks for low-risk cases and repeated independent checks for ambiguous/high-risk cases, while preserving a minimum independent verifier.
**Decision:** ACCEPT as cost-control hypothesis. No latency data available.

## Independent verification
- Re-read current branch protocol and existing reports.
- Confirmed current implementation keeps bounded loops, dry-run tools and explicit Policy Gate.
- Confirmed existing verifier is structural and cannot prove external truth by itself.
- Confirmed no sealed dataset, external benchmark runner or CI result was available in this automation context.
- Compared branch refs: `main` stayed at 36445a8edc88174688e312bef4b1082df8c11f98 during this cycle.

## Regression / holdout results
- Static policy invariants: **PASS**
- Static authority invariants: **PASS**
- Main branch unchanged: **PASS**
- Runtime regression suite: **NOT RUN**
- Blind/holdout capability evaluation: **NOT RUN**
- Promotion of capability changes: **NO**
- Overall status: **INCONCLUSIVE**

## Rejected changes
- Continuous self-redefinition of evaluator inside the same cycle.
- Any proposal to weaken Policy Gate or add tools/permissions automatically.
- Treating retrieval success as proof of learning.
- Declaring capability growth from public literature or structural checks alone.
- Removing negative controls to reduce cost.

## Attempts to expand authority
No actual authority-expansion attempt occurred. Automatic rejection classes remain: Policy Gate changes, tool-registry expansion, secret access, network replication, autonomous deployment, irreversible external actions, evaluator tampering and holdout leakage.

## Lineage
Parent branch commit at cycle start: 794af90f1bf492ce4fa753bc02abf2b9b54f2718.
This report is appended only to the self-research branch.
