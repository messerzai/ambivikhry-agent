# Self-improvement protocol — v2.8 experiment

This experiment gives the agent a larger reasoning budget while keeping the action surface bounded.

## Objective
Improve useful task performance while preserving or improving:

- correctness;
- uncertainty calibration;
- verification discipline;
- stopping behavior;
- safety boundaries;
- auditability.

## Gate
A candidate improvement may be proposed automatically, but adoption is conditional:

`candidate_score > baseline_score`
AND
`candidate_safety >= baseline_safety`
AND
`candidate_verification >= baseline_verification`
AND
`regressions == 0`

A failed candidate becomes data for the next iteration; it is not deployed.

## Experiment stages

1. Observe the current implementation.
2. Establish deterministic baseline.
3. Generate one bounded hypothesis.
4. Implement the smallest testable mutation.
5. Run the hard benchmark.
6. Run the complete regression suite.
7. Record delta and failure modes.
8. Keep the mutation only if all gates pass.
9. Produce the next hypothesis.

## Autonomy boundary

The experiment can edit project code only through the repository's normal development workflow. It cannot obtain secrets, alter permissions, disable policy checks, create hidden persistence, or propagate itself over a network.

Increasing autonomy is therefore staged by evidence, not by a single switch.
