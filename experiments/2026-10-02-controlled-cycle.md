# Controlled evolution cycle — 2026-10-02

## Scope

Fresh public research plus a bounded architecture/test integration. No changes to `main`, Policy Gate, authority boundaries, tool permissions, or human-approval requirements.

## Fresh evidence reviewed

- **ARI Bench** publishes a fixed-protocol, hidden-evaluation view of recursive AI improvement. Its central lesson for Ambivikhry is that the evaluator must remain hidden/fixed relative to the system being improved; self-reported progress is not enough.
- **SelfMem (arXiv:2607.03726, July 2026)** treats memory strategy itself as an optimization target and reports gains across 100K–1M token settings. This supports making memory strategy an experimental variable rather than hard-coding one universal retrieval policy.
- **EvoMemBench (arXiv:2605.18421v2, June 2026)** evaluates memory along two axes: in-episode vs. cross-episode scope and knowledge-oriented vs. execution-oriented content. This supports separating memory capability claims instead of using one recall number.
- **Bench'd / agent-memory-bench** provide current independent/community measurement examples and emphasize that a no-memory/full-context baseline can outperform some memory systems. Therefore Ambivikhry must compare against a baseline and not assume memory is beneficial.
- **HORIZON (2026)** treats repository-level self-evolution as an isolated worktree with an executable evaluator, acceptance predicate, runtime policy, tracing and replay. This supports isolated Git branches/worktrees and replayable evaluation contracts.

## Proposed improvements

1. **Frozen multi-axis capability matrix**: ID validation, ID regression, OOD transfer, retention, adaptation, and resource efficiency. Missing evidence is `UNKNOWN`, never implicit PASS.
2. **Baseline-first memory evaluation**: compare memory-enabled behavior against an equivalent no-memory/full-context baseline before claiming memory benefit.
3. **Memory-strategy experiments**: allow storage/retrieval strategy to be an experimental variable, but keep the evaluator and policy contract outside the mutable strategy.
4. **Process-aware reasoning prompt**: explicitly separate facts, hypotheses, unknowns, verification plan, decision and evidence-needed fields; keep confidence distinct from authorization.
5. **Replay/retention requirement**: record the exact strategy artifact and evaluation seed/task family so a later run can distinguish genuine transfer from prompt/task memorization.

## Integrated this cycle

- Added `ambivikhry/evaluation.py` with an immutable `EvaluationMatrix`.
- Added `tests/test_evaluation_matrix.py` for UNKNOWN, FAIL and complete PASS behavior.
- The matrix is intentionally standalone and does not grant permissions or change Policy Gate.

## Tests

The new tests are committed and CI is expected to run automatically after the push. At report creation, this connector did not expose a completed result for the new run, so no runtime PASS is claimed here.

Previous CI evidence remains relevant as regression history: the prior integration cycle had reached passing installation/test execution after the packaging fix, but this new commit must be rerun because the acceptance surface changed.

## Holdout

A true sealed/blind holdout is not available in this connector context. Therefore OOD transfer, retention, adaptation and resource-efficiency are recorded as `UNKNOWN` for promotion purposes. No capability improvement is claimed.

## Rejected changes

- Any evaluator that can be modified by the candidate it evaluates.
- Treating memory recall alone as proof of better agent performance.
- Treating self-reported benchmark results as independent evidence.
- Automatic changes to tools, permissions, Policy Gate, or approval boundaries.
- Automatic promotion when any evaluation axis is UNKNOWN.
- Large combined changes to prompt + memory + evaluator + tools in one mutation.

## Authority / safety audit

- `main`: not modified.
- Policy Gate: not modified or disabled.
- Tool/authority registry: not expanded.
- Human approval boundary: preserved.
- No attempt to expand authority detected in this cycle.

## Status

**INCONCLUSIVE / EXPERIMENTAL**

The new evaluation contract is integrated, but it deliberately cannot declare success until independent regression and sealed holdout evidence cover all required axes.
