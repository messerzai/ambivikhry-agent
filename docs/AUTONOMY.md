# Autonomous mode

v2.7 adds a bounded autonomous controller. The agent may continue a sequence of work cycles without waiting for another user message.

## What autonomy means here

The controller can:

- iterate on a task;
- observe progress;
- stop when the objective is reached or a bound is hit;
- record every cycle for audit;
- request tools through the existing policy layer.

It does **not** grant unlimited authority. Network propagation, privilege escalation, hidden persistence, secret extraction, or irreversible external actions are not enabled by this module.

The purpose of the test is to measure whether autonomy improves task completion rather than merely producing more activity.

## Smoke benchmark

Run:

```bash
python benchmarks/autonomy_smoke.py
```

Expected deterministic result:

```text
cycles: 3
stopped: True
final_score: 0.9
```

This is a plumbing test, not evidence of general intelligence. Real evaluation should use task-specific datasets, independent verification, cost/latency measurements, and regression comparisons against the previous release.
