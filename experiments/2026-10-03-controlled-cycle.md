# Controlled evolution cycle — 2026-10-03

## Scope
Controlled research/integration only. `main` is not modified. Policy Gate, authority boundaries, tool permissions and human-approval requirements remain unchanged.

## Fresh public research

- OpenEvolve documents a practical evolutionary loop built from prompt sampling, LLM ensemble mutation, evaluator pool, program database, asynchronous evaluation and checkpoints. This is useful as an architectural reference for population/archive and reproducible evolution, not as permission to copy code. Source: https://github.com/algorithmicsuperintelligence/openevolve
- ShinkaEvolve maintains a population of programs across generations and uses multiple LLM mutation operators, reinforcing population diversity and sample-efficient search. Source: https://github.com/SakanaAI/ShinkaEvolve
- HELIX treats a repository as the evolving organism and isolates mutations in git worktrees with tests/tooling before scoring. Source: https://github.com/KE7/helix
- EVOSEAL explicitly combines candidate selection/archive management with regression testing and Git-based improvement. Source: https://github.com/SHA888/EVOSEAL
- The Agent Memory Leaderboard now reports separate dimensions for explicit recall, compositional inference, temporal/event reasoning, memory governance, personalization, execution, and safety/privacy. This supports keeping memory quality multidimensional rather than collapsing it into recall. Source: https://agentmemoryleaderboard.ai/
- Current agent-security developments also reinforce the need for operational boundaries and containment rather than unrestricted autonomy. NVIDIA's September 28, 2026 announcement described OpenShell/Sentry as a boundary and containment layer for agents. Source: Reuters/Guardian coverage published September 28, 2026.

## Proposals

1. **Novelty/diversity gate:** distinguish a genuinely new strategy from repeated variants of already rejected strategies. This reduces premature convergence and repetitive self-improvement.
2. **Process-integrity gate:** require evidence that evaluator, policy constraints, and acceptance rules were not modified by the candidate being evaluated.
3. **Mutation isolation principle:** future repository-scale changes should be isolated and evaluated as bounded mutations, following the useful isolation pattern seen in HELIX.
4. **Memory multidimensionality:** preserve separate dimensions for recall, inference, temporal reasoning, governance, personalization and execution; do not use recall alone as a capability claim.
5. **Archive/provenance discipline:** keep candidate lineage and rejected strategies so the evolution loop can avoid rediscovering known failures.

## Integrated change

`ambivikhry/evaluation.py` now expands the evidence matrix from six to eight required axes:

- ID validation
- ID regression
- OOD transfer
- retention
- adaptation
- resource efficiency
- novelty/diversity
- process integrity

`UNKNOWN` remains non-promotable. A single `FAIL` dominates to `FAIL`; only eight explicit `PASS` values can yield `PASS`.

A regression test was added/updated to cover the two new gates.

## CI results

- The first CI run for the matrix change (`37108868737`) failed because an existing test still expected the old six-axis matrix. This is a genuine regression detected by the independent CI path, not hidden.
- The test was corrected to reflect the new contract without weakening the gate.
- A new CI run (`37108882198`) was automatically queued for the corrected HEAD. At report generation time it had not completed, so no PASS is claimed for that run.
- The preceding baseline cycle run (`37108860363`) completed successfully before the new matrix change.

## Holdout

No sealed/blind capability holdout is available through this GitHub-only runtime. OOD transfer, retention and adaptation therefore remain UNKNOWN for actual capability improvement. The new matrix intentionally prevents promotion under those conditions.

## Rejected changes

- evaluator self-modification;
- changing acceptance thresholds after observing results;
- using self-reported scores as independent evidence;
- promotion on ID accuracy/recall alone;
- treating CI success as proof of intelligence improvement;
- automatic expansion of tools or permissions;
- weakening Policy Gate;
- bypassing human approval;
- copying third-party code without verifying license compatibility and attribution requirements.

## Authority-expansion attempts

None observed in this cycle. The changes only make promotion harder and add evidence requirements; they do not grant new capabilities or permissions.

## Main branch

No changes made to `main`. The cycle branches from the prior experimental head and remains experimental.

## Status

**INCONCLUSIVE / NOT PROMOTED**

The software-level change is integrated experimentally, but the capability claim remains unproven until the corrected CI run completes and a sealed holdout evaluates transfer, retention, adaptation, novelty and resource tradeoffs.
