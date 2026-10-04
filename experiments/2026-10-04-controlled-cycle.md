# Controlled evolution cycle — 2026-10-04

## Scope

Experimental branch only. `main` is not modified. Policy Gate, authority boundaries, tool permissions, and human-approval requirements remain unchanged.

## Fresh public research

- **OpenEvolve** documents prompt sampling, LLM ensemble mutation, evaluator pools, a program database, asynchronous evaluation, multi-objective optimization, and checkpoints. Architectural lesson: maintain explicit candidate history and reproducible checkpoints rather than treating the latest candidate as truth. Source: https://github.com/algorithmicsuperintelligence/openevolve
- **EvoAgentX** provides automated workflow construction/evaluation/evolution and evaluates on separate validation/test splits. Its documented benchmark setup uses 50 validation and 100 test examples. Architectural lesson: candidate optimization and final evaluation should remain separated. Source: https://github.com/ANative-Lab/EvoAgentX
- **ShinkaEvolve** uses populations plus multiple LLM mutation operators for sample-efficient open-ended program evolution. Architectural lesson: preserve strategy diversity rather than repeatedly selecting one mutation mode. Source: https://github.com/N-I-ckel/shinkaevolve
- **HELIX** isolates repository-scale mutations in git worktrees and allows tests/tooling during mutation before scoring. Architectural lesson: isolate each candidate and evaluate it in a bounded workspace. Source: https://github.com/KE7/helix
- **EVOSEAL** combines candidate/archive selection with Git-based changes and regression testing. Architectural lesson: version control and regression are part of the evolution loop, not an afterthought. Source: https://github.com/SHA888/EVOSEAL
- **Agentic-evolution survey/indexes** currently emphasize evaluator gates, rollback, snapshotting, provenance, memory, skills and isolated sandboxes as recurring patterns. Source: https://github.com/YuxingLu613/awesome-agentic-evolution
- **Agent security developments** reinforce fail-closed authority boundaries and containment for agentic systems; NVIDIA announced OpenShell/Sentry on September 28, 2026 as an agent security/containment layer. Source: Reuters/AP coverage dated September 28, 2026.

## New hypothesis

The next useful failure mode to remove is **evaluator/process drift**: a self-improving candidate can appear better if it silently changes the evaluator, protected policy surface, tool registry, or the scale of its mutation. Therefore the mutation itself needs a frozen, auditable contract before scoring.

## Integrated change

Added `ambivikhry/mutation_contract.py` with a `MutationContract` that freezes:

- baseline commit identifier;
- evaluator digest;
- maximum changed-file count;
- maximum changed-line budget;
- Policy Gate protection;
- tool-registry protection;
- isolated-branch requirement.

`mutation_allowed()` is fail-closed. It can reject a candidate but cannot grant a permission. A changed evaluator digest, protected policy/tool path, excessive mutation size, or non-isolated candidate is rejected.

This implements the useful isolation/evaluator-integrity ideas from HELIX/OpenEvolve/EVOSEAL without copying third-party source code.

## Independent checks added

Added `tests/test_mutation_contract.py` covering:

1. a small isolated candidate is allowed;
2. evaluator drift is rejected;
3. Policy Gate changes are rejected;
4. tool-registry changes are rejected;
5. mutation-size and isolation violations are rejected.

## Regression / holdout status

The GitHub Actions workflow is triggered by the branch commits. This report does not claim PASS until the workflow result is observed. A sealed capability holdout is not available through the current GitHub-only runtime, so capability improvement remains unproven even if CI passes.

Required capability evidence remains:

- ID validation;
- ID regression;
- OOD transfer;
- retention;
- adaptation;
- resource efficiency;
- novelty/diversity;
- process integrity.

`UNKNOWN` remains non-promotable.

## Rejected changes

- Any mutation of `ambivikhry/policy.py`.
- Any automatic expansion of the tool registry.
- Any evaluator mutation or threshold mutation inside the same candidate evaluation epoch.
- Automatic promotion without sealed holdout evidence.
- Large unconstrained rewrites.
- Direct copying of third-party code without license/provenance verification.
- Any change requiring human approval without that approval.

## Authority-expansion attempts

No actual authority-expansion attempt was observed. The new mutation contract explicitly adds rejection conditions for Policy Gate and tool-registry changes.

## Main branch

No changes made to `main`. All commits are confined to `experiment/ambivikhry-controlled-cycle-2026-10-04`.

## Status

**EXPERIMENTAL / INCONCLUSIVE / NOT PROMOTED**

Software-level safeguards have been integrated. CI evidence must still be observed, and real capability improvement cannot be claimed without independent sealed holdout evidence.
