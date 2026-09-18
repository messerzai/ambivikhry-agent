# Self-Improvement V3

The experiment now treats self-improvement as an evidence-gated A/B process.

Pipeline:
OBSERVE -> RESEARCH -> HYPOTHESIZE -> CRITIQUE -> TEST -> COMPARE -> RE-ENTER

Three roles generate research and adversarial criticism:
- researcher: finds evidence and candidate improvements;
- critic: searches for errors and regressions;
- adversary: constructs counterexamples.

Their agreement is never sufficient proof.

## Acceptance gate
A candidate is accepted only when:
1. a baseline exists;
2. the success criterion is defined before evaluation;
3. the candidate reaches the measurable threshold;
4. pass rate does not fall;
5. important regressions are absent.

Rejected changes remain in history rather than replacing the baseline.

## Prompt revision
PromptRevisionStore can update the local active prompt only from an accepted ImprovementDecision.
The current research prompt is stored at prompts/AMBIVIKHRY_SELF_IMPROVEMENT_V3.txt.

This is a local prompt artifact. It does not modify the underlying model, hidden instructions, credentials, or system permissions.

## Agent growth
Conceptual lineage is unbounded as data through spawn_lineage().
Simultaneously active execution remains bounded by max_live_agents.
A request to cross that boundary is recorded as privilege_expansion_request.

This separates intellectual growth from uncontrolled process/resource growth.

## Tests
The new test suite covers measurable gains, no-gain rejection, regressions, pass-rate degradation, accepted/rejected prompt revisions, authority-boundary detection, and bounded-vs-lineage agent growth.

A local targeted execution of the core acceptance logic passed the implemented checks. Repository-wide CI has not yet run for this branch, so that result must not be presented as a full CI pass.