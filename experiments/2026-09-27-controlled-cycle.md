# Controlled Evolution Cycle — 2026-09-27

## Scope and invariants
Target branch: `experiment/ambivikhry-self-research-2026-09-24` only.
`main` is not modified.
Policy Gate, tool registry, secrets, replication, deployment and approval boundaries are unchanged.
No human-approval-required change was accepted.

## Fresh public evidence reviewed
1. **PAST-Bench** — evaluates whether retained experience improves later tasks through the intended save → retrieve → update pathway, not only headline score. https://arxiv.org/abs/2608.04003
2. **EvoMemBench** — separates memory scope (in-episode vs cross-episode) and content (knowledge vs execution), showing no single memory method dominates. https://arxiv.org/abs/2605.18421
3. **Mem2ActBench** — tests whether memory is actively used to ground later tool actions and parameters, not merely recalled in answers. https://arxiv.org/abs/2601.19935
4. **AMA-Bench** — focuses on long-horizon agent memory built from agent-environment trajectories and highlights causal/objective retrieval gaps. https://arxiv.org/abs/2602.22769
5. **AgentMem** — emphasizes async memory computation with synchronous context injection and intervention only when memory changes the next action. https://github.com/agentmem/agentmem
6. **Memory Policy Lab** — makes retention, compression, retrieval and context-budget trade-offs explicit and auditable. https://github.com/cendywang/memory-policy-lab
7. **Cortex Memory** — uses evidence feedback, correction preservation, bounded recall and offline consolidation rather than unlimited append-only memory. https://github.com/jacobycoffin/cortex-memory
8. **ProveM** — highlights tenant isolation, auditability, prompt-injection defense and governed memory as first-class concerns. https://github.com/BernhardJackiewicz/provem

## Proposals generated
### P1 — Pathway evidence tuple
Require every claimed self-improvement to log:
`experience_id -> saved_artifact -> retrieval_event -> update_event -> later_task_delta`.
**Decision:** ACCEPT as evaluation/provenance design. No runtime change yet.

### P2 — Action-grounded memory score
Add a metric for whether memory changes a later tool choice or parameter correctly, distinct from recall/QA accuracy.
**Decision:** ACCEPT as benchmark design.

### P3 — Two-axis memory regression matrix
Run knowledge-retention and execution-reuse tracks across in-episode and cross-episode settings.
**Decision:** ACCEPT as regression design.

### P4 — Intervention threshold
Permit memory injection only when expected action benefit exceeds a configurable threshold; otherwise remain silent.
**Decision:** ACCEPT as implementation hypothesis, pending runtime validation.

### P5 — Correction and invalidation ledger
Store corrections, superseded items, invalidation conditions and provenance explicitly; never silently overwrite prior claims.
**Decision:** ACCEPT as implementation hypothesis.

### P6 — Negative-control suite
Add tests for stale-memory use, poisoning, prompt-injection payloads in memory, holdout leakage, evaluator tampering and unauthorized tool expansion.
**Decision:** ACCEPT as hard regression gate.

## Prompt / reasoning changes proposed
- Distinguish `recalled`, `action-grounding`, `verified`, `superseded` and `unknown` in every memory-related reasoning step.
- Require the agent to state whether memory changed the chosen action, not just whether memory was retrieved.
- Require an explicit “do not use” decision when provenance is absent or the item is invalidated.
- Freeze evaluator criteria inside an epoch; evaluator changes require a separate approved boundary.

## Independent verification
- Re-read current self-research protocol and prior controlled-cycle report.
- Checked that current implementation retains bounded loops, dry-run tools and explicit Policy Gate.
- Confirmed the current verifier is structural and cannot establish external truth by itself.
- Confirmed no sealed holdout corpus, runtime benchmark result or CI execution was available in this automation context.
- No evidence was found of a successful authority-expansion attempt.

## Regression / holdout results
- Static policy invariants: **PASS**
- Static authority invariants: **PASS**
- `main` unchanged: **PASS**
- Runtime regression suite: **NOT RUN**
- Blind/holdout capability evaluation: **NOT RUN**
- Memory pathway benchmark: **NOT RUN**
- Capability promotion: **NO**
- Overall status: **INCONCLUSIVE**

## Rejected changes
- Treating memory recall as proof of learning.
- Allowing silent overwrite of corrections or provenance.
- Auto-injecting all retrieved memory into prompts.
- Changing evaluator criteria mid-epoch.
- Expanding tools, permissions or replication automatically.
- Weakening Policy Gate for speed.
- Declaring capability improvement from literature review or static checks alone.

## Attempts to expand authority
No actual attempt occurred in this cycle.
Automatic rejection classes remain: Policy Gate changes, tool-registry expansion, secret access, network replication, autonomous deployment, irreversible external actions, evaluator tampering and holdout leakage.

## Lineage
Parent: prior controlled-cycle report on the same branch.
This report is appended only to `experiment/ambivikhry-self-research-2026-09-24`.
