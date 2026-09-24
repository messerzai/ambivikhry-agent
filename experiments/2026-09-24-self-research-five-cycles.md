# Deep Self-Research — Five Controlled Cycles

Date: 2026-09-24
Branch: `experiment/ambivikhry-self-research-2026-09-24`

## Internet evidence reviewed
- AIDE² reports recursive self-improvement of a research agent using hidden evaluations, with seven successive improvements and transfer to held-out tasks. citeturn0academia55
- PAST-Bench isolates whether retained experience actually improves later personal-agent behavior and emphasizes pathway evidence, not just headline gains. citeturn0academia53
- AI4AI-Bench evaluates whether agents actually redesign training algorithms rather than merely tune data/hyperparameters; results show current systems remain far from task optima. citeturn0academia52
- RewardHackingAgents demonstrates evaluator tampering and train/test leakage as distinct attack surfaces and shows evaluator locking can eliminate tampering at measurable runtime cost. citeturn0search4
- Hack-Verifiable Environments argues reward hacking should be made directly detectable by embedding verifiable opportunities into environments. citeturn0academia54
- AgentV-RL supports bidirectional/tool-assisted verification because one-way verification can propagate incorrect intermediate reasoning. citeturn0search6
- RSI-Exam evaluates long-horizon self-improvement with a final hidden test set, reinforcing the need for unseen-data generalization. citeturn0search3
- Anthropic's September 2026 public discussion describes increasing AI contribution to AI development while explicitly stating that fully autonomous recursive self-improvement has not yet been reached. citeturn0search9

## Cycle 1 — Evaluation integrity
Hypothesis: self-improvement is invalid if the evaluator can be influenced by the proposer.

Change: strengthen the branch protocol so proposer and certifier are distinct roles and evaluator/holdout integrity is a hard invariant.

Decision: **ACCEPTED as protocol improvement.** This is a methodological improvement, not evidence that the agent itself became more capable.

## Cycle 2 — Holdout generalization
Hypothesis: an apparent self-improvement is weak evidence unless it transfers to unseen tasks.

Change: require blind/holdout testing and explicitly record transfer rather than optimizing only the visible evaluation.

Decision: **ACCEPTED as protocol improvement.** Inspired by AIDE², PAST-Bench and RSI-Exam. citeturn0academia55turn0academia53turn0search3

## Cycle 3 — Memory pathway verification
Hypothesis: storing more memory is not equivalent to learning; improvement should be traceable through save → retrieve → update → later behavior.

Change: add memory contamination/pathway checks to the research domains.

Decision: **ACCEPTED as protocol improvement.** PAST-Bench directly motivates this distinction. citeturn0academia53

## Cycle 4 — Reward/evaluator attack resistance
Hypothesis: optimizing a score without protecting the evaluation channel can produce false improvement.

Change: classify evaluator tampering, holdout leakage, benchmark overfitting, and policy/authority changes as automatic rejection conditions.

Decision: **ACCEPTED as safety/evaluation invariant.** Supported by RewardHackingAgents and the reward-hacking survey. citeturn0search4turn0search0

## Cycle 5 — Deeper verifier independence
Hypothesis: a single forward verifier can share blind spots with the proposer; independent backward/tool-assisted verification is stronger.

Change: require independent critique and make verifier independence an explicit research target. Future implementation may investigate bidirectional verification, but no authority/tool expansion is authorized by this cycle.

Decision: **ACCEPTED as research direction; implementation status INCONCLUSIVE.** AgentV-RL provides evidence for complementary forward/backward verification, but this branch has not run its own benchmark yet. citeturn0search6

## Overall result
Five controlled improvement passes were completed at the **protocol/research-design level**. No claim is made that the underlying LLM became intrinsically more capable: no independent runtime benchmark was available in this session to establish such a capability gain.

## Rejected / not promoted
- Autonomous expansion of tools or permissions — rejected by invariant.
- Self-modification of Policy Gate — rejected by invariant.
- Treating public literature as proof of local improvement — rejected.
- Declaring success without hidden/holdout evidence — rejected.
- Using self-generated evaluation as sole certification — rejected.
- Product/monetization/user-acquisition changes — out of scope.

## Lineage
Starting protocol commit: `72369b58b8bb63c53d7c3495d68c6ed86227b899`
Five-cycle protocol commit: `ade97589c6338afb440d914f1317d327ce6c5dff`

## Status
`CONTROLLED-PROTOCOL-IMPROVEMENT / UNDER HOLDOUT VALIDATION`
