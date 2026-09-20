# Ambivikhry v2.8 — bounded evolutionary self-improvement experiment

## Purpose

Run ten experimental generations of the agent on isolated branches/workspaces. Each generation may propose changes to the agent, verifier, memory, prompts, tools, or collaboration policy. A generation is accepted only when an independent evaluation shows measurable improvement over its parent without violating invariants.

## Research signals incorporated

- ReVeal: co-evolution of code generation and self-verification; iterative generation → verification → tool feedback.
- EvoTest: separate Actor and Evolver roles; evolve configuration, memory and tool routines from execution traces.
- HyperAgents: explicit task-agent + meta-agent architecture inside an editable program.
- Self-Evolving Coding Agents survey: use executable feedback, repository context and coding trajectories; guard against benchmark overfitting.
- A Self-Improving Coding Agent: self-editing can improve coding benchmarks, but improvement must remain evaluation-gated.

These are research inputs, not code to copy blindly. Every imported idea becomes a proposal and must pass local tests.

## Ten-generation ladder

1. **G01 — Evidence loop:** explicit evidence objects and source quality scoring.
2. **G02 — Independent verifier:** verifier receives candidate + evidence, not the candidate's confidence alone.
3. **G03 — Actor/Evolver split:** task agent executes; evolver proposes changes from traces.
4. **G04 — Helper council:** critic, test designer, researcher and safety auditor produce independent proposals.
5. **G05 — Regression memory:** preserve successful and failed mutations with reasons.
6. **G06 — Search diversification:** maintain multiple candidates instead of greedy single-line evolution.
7. **G07 — Anti-overfitting:** hidden holdout tasks and mutation-specific tests.
8. **G08 — Verifier co-evolution:** evolve tests/verifiers only when they improve agreement with fixed external checks.
9. **G09 — Meta-improvement:** allow the evolver to propose changes to its own improvement strategy, still behind the same gate.
10. **G10 — Consolidation:** compare all surviving candidates against v2.6/v2.7 baselines and produce a human-reviewable winner; no automatic promotion to main.

## Hard boundaries

- No network propagation or automatic deployment.
- No privilege escalation.
- No secret extraction or credential modification.
- No automatic merge to `main`.
- No candidate may disable, weaken or rewrite the Policy Gate, audit trail, approval boundary or independent evaluation rules.
- Helper agents may propose and review mutations but cannot authorize their own promotion.
- Failed candidates remain archived with lineage and evaluation results.

## Selection rule

A candidate survives only if:

`quality_gain > 0 AND safety_invariants_pass AND regression_suite_pass`

For claims about the outside world, external evidence is required. Self-reported confidence is never an independent proof.
