# Controlled evolution cycle — 2026-10-09

## Status

EXPERIMENTAL / NOT PROMOTED. Main was not targeted. No production capability gain is claimed.

## Lineage

- Parent experimental cycle: `df2265ab73d71efdb7ef3cce5b1614bdd6030fda`
- Branch: `experiment/ambivikhry-controlled-cycle-2026-10-09`
- Reference gate contract tests added at commit: `724d99f1765168ae735cd725a6b8284d21b8d7f4`
- This report is committed after the test file.
- No changes to Policy Gate, Tool Registry, sensor permissions, evaluator implementation, or main are proposed by this design-only cycle.

## Public research reviewed

1. **Live-Evo** (arXiv:2602.02369, 2 Feb 2026): separates an Experience Bank from a Meta-Guideline Bank, updates memory weights from feedback, and contrasts guided vs unguided performance. The useful lesson is to measure the marginal causal utility of a memory item and decay misleading/stale experiences, rather than reward accumulation alone. Reported results are from the paper's own Prophet Arena setup and are not evidence about Ambivikhry.
   - https://arxiv.org/abs/2602.02369
   - https://github.com/ag2ai/Live-Evo
2. **MemPO** (Findings of ACL 2026, July 2026): selectively manages memory to reduce long-horizon context/token cost. The reported gains are benchmark-specific; they motivate measuring quality and resource use together, not assuming a universal win.
   - https://aclanthology.org/2026.findings-acl.1166/
3. **EvoMemBench** (arXiv:2605.18421, May 2026): compares 15 memory methods with strong long-context baselines and finds no single memory form consistently wins. This supports counterfactual memory tests and baseline parity checks.
   - https://arxiv.org/abs/2605.18421
4. **Agent Sandbox Taxonomy**: a recent public discussion highlights that a sandbox claim is not enough; isolation, credential handling, action governance, observability and failure response need explicit evidence. This is a secondary news account, so its details should be verified against the original taxonomy before implementation.
   - https://www.techradar.com/pro/the-ai-escape-is-a-red-herring-the-problem-is-we-cant-tell-a-good-sandbox-from-a-bad-one

## Proposals in this cycle

### A. Evidence-weighted memory update

Separate:
- `experience`: what happened and its provenance;
- `guideline`: how an experience may be applied;
- `outcome`: observed result and evaluation context;
- `weight`: provisional retrieval priority with timestamp and decay;
- `counterfactual_delta`: candidate-with-memory versus same-task baseline.

Do not update a durable memory weight from a single noisy or subjective signal. Require repeated evidence or explicit user confirmation where objective outcomes are unavailable. Keep facts, user preferences and speculative hypotheses in separate namespaces.

### B. Token-aware utility gate

Report task utility alongside:
- prompt/input tokens;
- retrieved-memory tokens;
- latency/cost;
- irrelevant-memory distraction sensitivity;
- stale-memory failure rate.

A memory change is not a win if it only adds context or increases cost without a reproducible utility gain.

### C. Sandbox evidence contract

For any future executable candidate, record the tested isolation boundary, network policy, credential scope, permitted actions, audit visibility, and failure/rollback behavior. Do not infer sandbox safety from the mere presence of a worktree or container.

### D. Fail-closed promotion contract

Required dimensions in the standalone reference contract:
`ID validation, ID regression, OOD transfer, retention, adaptation, efficiency, novelty, process integrity, memory counterfactual, delayed transfer, selection consistency, personalization utility, longitudinal safety, sandbox integrity`.

Every dimension must be PASS. FAIL rejects; UNKNOWN blocks promotion. Even a fully passing candidate only becomes `REVIEW_REQUIRED`; the reference gate never merges or promotes automatically.

## Test results

A standalone Python unittest smoke suite was executed locally against the reference contract:
- 10 tests run
- 10 passed
- 0 failed

Covered cases:
- all gates passing leads only to human review;
- missing holdout / missing required dimension defaults to UNKNOWN and is not promotable;
- regression veto;
- evaluator digest mutation rejection;
- threshold drift rejection;
- holdout exposure rejection;
- Policy Gate mutation rejection;
- Tool Registry / permission expansion rejection;
- personalization gain cannot compensate for unknown longitudinal safety.

Important limitation: these are design-level contract tests, not tests against the production agent, Policy Gate implementation, or a configured GitHub Actions workflow. The repository's previous cycle commit had no reported status checks. The new commit's CI status must be checked separately; no CI PASS is claimed here.

## Regression and holdout

- Reference-gate regression smoke: PASS (10/10 local tests).
- Production integration regression: UNKNOWN / not run.
- Capability regression on real agent tasks: UNKNOWN / not run.
- Sealed/blind capability holdout: UNKNOWN / unavailable in this runtime.
- Longitudinal safety holdout: UNKNOWN / unavailable in this runtime.
- Real-user personalization utility: NOT TESTED; no biometric or personal sensor data used.

Therefore, no capability improvement is claimed and no promotion is allowed.

## Rejected / deferred

- Self-modifying evaluator or thresholds.
- Candidate access to sealed holdout.
- Automatic promotion or merge after tests.
- Policy Gate or Tool Registry edits.
- Permission/sensor scope expansion.
- Hidden biometric/EEG collection or export.
- Memory reinforcement based on a single unverified reward.
- Sandbox claims without evidence of boundary enforcement.
- Treating published benchmark gains as proof of Ambivikhry gains.

## Authority audit

No actual permission-expansion attempt was observed in this cycle. The proposed contract explicitly rejects Policy Gate changes, Tool Registry changes, permission expansion, evaluator drift, threshold drift, and holdout exposure. This is a statement about the observed experiment, not a claim that the repository has a production-grade enforcement mechanism.

## Decision

`EXPERIMENTAL / NOT PROMOTED / PRODUCTION REGRESSION UNKNOWN / SEALED HOLDOUT UNKNOWN`.
