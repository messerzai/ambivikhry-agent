# Controlled evolution cycle — 2026-09-30

## Scope
Fresh public research + bounded integration/testing. `main` untouched; Policy Gate, authority boundaries and human-approval boundaries remain mandatory.

## Fresh findings

- AIDE² (arXiv:2609.26457, 2026-09-22) reports seven accepted self-generated improvements in an 8-day run, with held-out transfer across four benchmarks including an OOD weather domain. Key lesson: selection must be separated from hidden evaluation; self-improvement should be judged by transfer, not training-set gains alone.
- EvoPathBench (arXiv:2609.24663, 2026-09-21) argues endpoint score is insufficient. It freezes base model/tools and evolving artifacts at checkpoints and tests generalization, retention after unrelated learning, and rule adaptation. It reports distribution-shift degradation and unreliable rule adaptation, making checkpoint/process-level evaluation important.
- RRSI (arXiv:2609.24972, 2026-09-21) frames harness self-improvement as vulnerable to overfitting and proposes regularized candidate/selection processes with limited edit budgets and exploration of underexplored trajectories.
- EvoMemBench separates memory by in-/cross-episode scope and knowledge-/execution-oriented content; no single memory mechanism is universally best.
- AFTER reports procedural-memory transfer across tasks, roles and model backbones, supporting cross-backbone transfer as a useful robustness axis.

## Integrated this cycle

1. **Frozen epoch + provenance remains active.** Candidate changes are typed and lineage is append-only.
2. **Process-level evaluation contract added to the experiment plan.** Future capability claims must report checkpoint, ID transfer, OOD transfer, retention, adaptation, and resource use separately.
3. **Candidate edit budget.** Proposed future self-modifications are restricted to small, typed changes per epoch; bundled multi-surface changes are rejected for promotion unless independently attributable.
4. **Diversity/novelty requirement.** The evolution log must identify whether a candidate explores a new strategy family or repeats a previously rejected path.
5. **Cross-backbone transfer metric reserved.** A future holdout should test whether a learned procedural artifact transfers beyond the exact GPT backend; no claim is made until such a test is run.

## Regression result

The prior packaging fix was validated by GitHub Actions run `36547217907` on commit `1850a9fb5bb0653cafab62ad45ac030e34219bbb`.

All four Python matrix jobs (3.10, 3.11, 3.12, 3.13) passed installation and `pytest -q`. This is a real regression/integration PASS, not a capability evaluation.

## Holdout status

No sealed capability holdout was available through the current GitHub connector. Therefore no claim of capability improvement or self-improvement generalization is promoted.

## Rejected

- Any self-modification that changes Policy Gate, authority boundaries, tool permissions, evaluator rules, or human-approval requirements.
- Large bundled rewrites whose effects cannot be attributed.
- Acceptance based only on same-task/ID score.
- Treating CI success, compilation, verifier score, or retrieval as proof of capability gain.
- Automatic promotion without sealed holdout evidence.

## Authority expansion attempts

None observed. No new tools or permissions were added.

## Status

**INTEGRATION PASS / CAPABILITY CLAIM: INCONCLUSIVE / NOT PROMOTED**.
