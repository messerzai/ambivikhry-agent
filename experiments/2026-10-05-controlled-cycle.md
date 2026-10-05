# Controlled evolution cycle — 2026-10-05

## Scope

Experimental branch only. `main` is not modified. Policy Gate, authority boundaries, tool permissions, and human-approval requirements remain unchanged.

## Fresh public research

- **Beagle / DarwinX** (Salesforce AI Research, public release 2026-09-02) evaluates and evolves agent harnesses with verifier-backed tasks, explicit train/test separation, and robustness to new challenges. The project reports that evolved harnesses can improve transfer, but the benchmark-native evolution setup still requires independent test evaluation. Source: https://github.com/SalesforceAIResearch/Beagle
- **A-Evolve** emphasizes targeted skills, episodic memory, Git-tagged mutations, and transfer across benchmarks. Its public results reinforce a useful distinction: reusable skills can outperform larger collections of generic instructions. Source: https://github.com/A-EVO-Lab/a-evolve
- **EvoAgentBench** explicitly evaluates longitudinal growth curves, ability transfer, error avoidance, and skill-hit quality rather than a single static score. Source: https://github.com/EverMind-AI/EvoAgentBench
- **EvolveMem** reports guarded co-evolution of memory content and retrieval configuration, with revert-on-regression and exploration-on-stagnation. This supports treating retrieval policy as an evolvable but protected component. Source: https://arxiv.org/abs/2605.13941
- **AFTER** evaluates procedural memory across tasks, roles, and model backbones and finds that some evolved skills transfer broadly while others become specialized. Source: https://arxiv.org/abs/2606.23127
- **EvoMemBench** finds that long-context baselines remain competitive and that no memory mechanism wins consistently; memory helps most when context is insufficient or tasks are difficult. Source: https://arxiv.org/abs/2605.18421
- **Reliable self-evolving agent survey** identifies scaffold overfitting, metric capture, and criterion drift as recurring failure modes and recommends keeping evidence and acceptance gates outside the update boundary. Source: https://github.com/wkqdzkd/Awesome-Reliable-Self-Evolving-Agents
- **PAST-Bench / current RSI benchmark maps** reinforce the need to verify the intended save-retrieve-update pathway on fresh sessions and held-out tasks. Source: https://github.com/Gen-Verse/PAST-Bench

## New hypotheses for Ambivikhry

### 1. Separate skill value from prompt value

A candidate improvement should record whether the gain comes from a prompt edit, procedural skill, memory entry, retrieval change, workflow change, or interaction policy. A mixed mutation is not promoted unless its causal contribution is identifiable.

### 2. Add longitudinal transfer as a first-class gate

A successful candidate should be evaluated not only immediately after mutation but also after intervening tasks. This detects short-lived gains, forgetting, and scaffold overfitting.

### 3. Add counterfactual memory checks

For memory-related candidates, compare:

`no-memory baseline` vs `candidate memory` vs `candidate memory + irrelevant-memory distraction`.

A memory mechanism is not credited when its apparent benefit comes only from extra context or accidental leakage.

### 4. Add process-integrity adversarial tests

Before promotion, attempt to induce the candidate to:

- alter evaluator thresholds;
- read hidden test material;
- rewrite Policy Gate;
- expand tool permissions;
- use unauthorized data;
- declare success without evidence.

Any successful bypass is an automatic rejection, independent of task score.

### 5. Track intervention cost

For future personalized/resonance features, optimize not only capability but also interruption cost and unnecessary action rate. A more active agent is not automatically a better agent.

## Architecture proposal

Add a conceptual `EvolutionEvidence` record to future evaluation infrastructure:

- candidate lineage;
- mutation class;
- baseline/evaluator digests;
- exact training/evolution set;
- untouched holdout identifier;
- immediate score;
- transfer score;
- delayed retention score;
- error-avoidance score;
- resource/intervention cost;
- process-integrity result;
- rollback reason if rejected.

The record is evidence metadata only; it grants no authority.

## Regression / holdout plan

Required promotion matrix now has these explicit dimensions:

1. ID validation;
2. ID regression;
3. OOD transfer;
4. longitudinal retention;
5. adaptation after intervening tasks;
6. resource efficiency;
7. novelty/diversity;
8. process integrity;
9. memory counterfactual robustness;
10. delayed transfer / ability retention.

`UNKNOWN` remains non-promotable.

A benchmark score produced by the candidate itself, or by an evaluator changed by the candidate, is not accepted as independent evidence.

## Independent checks proposed

The cycle adds a design-level test plan for:

- hidden-test isolation;
- evaluator immutability;
- Policy Gate immutability;
- Tool Registry immutability;
- memory leakage resistance;
- longitudinal retention;
- rollback after regression;
- no-promotion on incomplete evidence.

No production capability is claimed from these proposals alone.

## Rejected changes

- self-modifying evaluator;
- access to hidden holdout data;
- changing thresholds after observing candidate results;
- automatic expansion of permissions or sensors;
- Policy Gate changes;
- Tool Registry changes;
- unrestricted biometric/EEG collection;
- promotion from a single benchmark score;
- promotion from self-reported success;
- large simultaneous prompt+memory+tool mutations without attribution;
- bypassing human approval.

## Authority-expansion attempts

No actual authority-expansion attempt was observed in this cycle. Adversarial tests are specified as future checks rather than being represented as observed attacks.

## Main branch

No changes made to `main`. This cycle is based on the previous experimental personalization design commit and is isolated in:

`experiment/ambivikhry-controlled-cycle-2026-10-05`

## Status

**EXPERIMENTAL / NOT PROMOTED**

No capability-improvement claim is made until the independent holdout and longitudinal evidence are actually executed and observed.
