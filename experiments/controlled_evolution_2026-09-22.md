# Controlled evolution cycle — 2026-09-22

## Scope
Fresh public research was reviewed for self-improving and agentic systems. The cycle is limited to the experimental branch `experiment/ambivikhry-v3-unified-2026-09-22`.

Protected constraints: do not modify `main`; do not expand authority; do not disable or weaken Policy Gate; do not modify sealed holdout data; do not accept changes requiring human approval.

## Fresh findings

1. **Audited Skill-Graph Self-Improvement (ASG-SI)**: promote improvements as auditable reusable skills only after verifier-backed replay and contract checks. Source: https://arxiv.org/abs/2512.23760
2. **Harness tampering**: self-improving agents can create illusory gains or violate authorization/provenance/completeness. Source: https://arxiv.org/abs/2609.00069
3. **Phantom guardrails**: agents may hallucinate failures and add guardrails for failures that never occurred; deterministic counterfactual checks are needed. Source: https://arxiv.org/abs/2607.13083
4. **Benchmark contamination**: poisoned benchmarks can cause vulnerable self-modifications to transfer to clean held-out tasks. Source: https://www.alphaxiv.org/abs/2609.17817
5. **Harness evaluation**: improvements must be compared with matched search budgets and evaluated on held-out tasks to distinguish genuine harness improvement from extra search. Source: https://www.emergentmind.com/papers/2607.12227
6. **Graph memory**: self-evolving structured memory can improve evidence recovery, retrieval, and long-horizon grounding when writer/reader feedback is auditable. Source: https://arxiv.org/abs/2605.12061

## Accepted proposal

Added `ambivikhry/evolution_cycle.py` with an explicit staged decision:

- `accept_experimental`: regression, independent check, holdout, provenance, and measured improvement all pass;
- `hold`: evidence is incomplete or generalization is not demonstrated;
- `reject`: protected surfaces changed or regression failed.

Added `tests/test_evolution_cycle.py` covering bounded improvement, authority expansion, missing independent checks, holdout failure, and regression failure.

Exported the new cycle and bumped experimental package version to `2.6.2`.

## Rejected proposals

- Automatic authority expansion: **rejected**.
- Policy Gate changes: **rejected**.
- Holdout/evaluator changes: **rejected**.
- Tool-registry expansion during self-improvement: **rejected**.
- Self-promotion based only on the agent's own score: **rejected**.
- Guardrails inferred from unverified or hallucinated failures: **rejected/hold** until a deterministic counterfactual oracle exists.

## Independent verification and regression

The new tests are committed and the repository GitHub Actions workflow is configured to run `pip install -e .` and `pytest -q` across Python 3.10–3.13. The commit series for this cycle is:

- `09de2003d1d455fc3c1c95c7b06dabc7c391820e` — controlled evolution gate;
- `42d1b0fd08a3d90648d339f460772751e5d2e4fc` — regression tests;
- `f36036bac7023add85ce2ae68cdcebdb7f132764` — package export and version bump.

At the time of writing, no completed CI verdict was available for the final commit. Therefore this report records the result as `CI_PENDING`, not `PASS`.

## Authority-change audit

No attempted change in this cycle was allowed to expand authority. No Policy Gate, credential, model endpoint, tool registry, or holdout modification was accepted.

## Lineage

Parent: `experiment/ambivikhry-v3-unified-2026-09-22`
Current head: `f36036bac7023add85ce2ae68cdcebdb7f132764`
Status: `EXPERIMENTAL / CI_PENDING`
