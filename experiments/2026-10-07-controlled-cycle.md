# Controlled evolution cycle — 2026-10-07

## Status
EXPERIMENTAL / NOT PROMOTED.

## Fresh public research
- SEABench (submitted 2026-09-29) studies endogenous misalignment in self-evolving agents over 48 longitudinal task sequences and tests persistent unsafe behavior caused by locally useful self-updates. Implication: add longitudinal safety regression, not only capability regression. Source: https://www.alphaxiv.org/abs/2609.35596
- EvoPathBench (published 2026-09-21) argues endpoint scores are insufficient; it freezes base model/tools and evaluates successive artifact checkpoints on held-out episodes. Implication: evaluate capability trajectories and checkpoint deltas. Source: https://www.emergentmind.com/papers/2609.24663
- AFTER reports controlled transfer tests for procedural memory across tasks, roles and model backbones. One refinement round improved aggregate performance by 3.7–6.7 points in its setting; multi-model traces reached 73.1% cross-model test accuracy. Implication: transfer should be an explicit gate. Source: https://www.alphaxiv.org/abs/2606.23127
- EvoMemBench compares 15 memory methods with strong long-context baselines across in-/cross-episode and knowledge/execution axes. Implication: memory must demonstrate incremental utility over a context baseline. Source: https://www.alphaxiv.org/abs/2605.18421v2
- ADEBench evaluates the memory actually delivered to the model, with no LLM judge, highlighting deterministic retrieval evaluation as an independent check. Source: https://adebench.dev/
- RSEA's held-out selection reinforces that held-out gates can prevent recursive context evolution from regressing below baseline, while representativeness of the split remains a limitation. Source: https://www.alphaxiv.org/abs/2606.28374
- Recent reporting indicates agents are consuming very large token volumes rereading cached context. This strengthens context compression/selective retrieval as an efficiency metric. Source: https://www.tomshardware.com/tech-industry/artificial-intelligence/futurum-ceo-says-agents-use-ai-5x-more-than-humans-number-will-eventually-hit-10x-but-agents-are-mostly-rereading-what-theyve-already-seen

## New proposals
1. Longitudinal safety regression: freeze prior safety behavior at checkpoints and compare evolved artifacts on the same held-out safety suite.
2. Checkpoint trajectory evaluation: record capability and safety deltas at every experimental checkpoint rather than only final-vs-baseline.
3. Deterministic memory retrieval gate: add a non-LLM-juror retrieval check for whether the memory layer delivered required evidence.
4. Context efficiency gate: measure useful evidence per token and reject candidates that gain score only through substantially larger context.
5. Transfer matrix: require at least one cross-task or cross-domain test for reusable prompt/skill/memory changes.
6. Endogenous-drift probe: add paired evolving/non-evolving trajectories to detect whether a locally useful mutation creates later harmful behavior.

## Prompt/reasoning proposal
Use a compact evidence contract before final reasoning:
goal -> relevant evidence -> uncertainty -> candidate action -> constraint check -> response.
This is an evaluator-visible trace schema, not a request for hidden chain-of-thought. Store only concise auditable summaries, provenance, uncertainty and test outcomes.

## Independent verification plan
Candidate acceptance remains fail-closed. Independent checks are:
- deterministic tests;
- frozen evaluator digest;
- baseline comparison;
- held-out capability;
- held-out safety;
- transfer;
- efficiency;
- process integrity.
UNKNOWN is non-promotable.

## Rejected changes
- evaluator or threshold self-modification;
- candidate access to sealed holdout data;
- Policy Gate or Tool Registry modification;
- autonomous sensor/biometric permission expansion;
- hidden collection of personal/biometric data;
- promotion based on capability score without safety regression;
- promotion based only on final endpoint score;
- changes requiring human approval without explicit approval.

## Authority-expansion attempts
No actual authority-expansion attempt was observed in this cycle. The endogenous-drift probe is defensive only and cannot grant permissions.

## Lineage
Parent: 2b5be55d3d6de6dd83acab33ef02dbb69c433101
Branch: experiment/ambivikhry-controlled-cycle-2026-10-07
Main: untouched.

## Verification result
This cycle adds research/design artifacts only. A GitHub Actions status for the new commit must be observed before claiming PASS. A sealed capability/safety holdout is not available through the current runtime, so promotion remains blocked.

## Final status
EXPERIMENTAL / NOT PROMOTED / HOLDOUT UNKNOWN
