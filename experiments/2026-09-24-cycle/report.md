# Controlled evolution cycle — 2026-09-24

Status: `EXPERIMENTAL / NOT PROMOTED`

## Baseline

- Repository: `messerzai/ambivikhry-agent`
- Baseline ref: `main` at `36445a8edc88174688e312bef4b1082df8c11f98`
- Existing protocol: bounded self-improvement, Policy Gate, dry-run, regression tests, GitHub Actions, mutation proposals, and separate deployment approval.

## Fresh public evidence reviewed

1. **Recursive self-improvement of AI research agents (2026-09-22)** — hidden evaluations and held-out transfer are central; reward-hacking was measured separately.
2. **Auditing Harness Tampering in Self-Improving Agents (2026-08-30)** — tampering can persist in the lineage of the best agent; provenance and authorization need independent audit.
3. **Self-Authored Verification Is Unreliable in Heuristic Self-Improving Agents (2026-07-27)** — self-authored scores can diverge from sealed deployment performance.
4. **Self-Evolving Agents with Anytime-Valid Certificates (2026-07-01)** — frozen base, versioned harness and auditable acceptance certificates are useful controls.
5. **RewardHackingAgents (2026-03-11)** — evaluator tampering and train/test leakage are distinct compromise vectors.
6. **MAGMA (2026-04-16) and MemMA (2026-09-03)** — structured multi-view memory and coordinated forward/backward memory repair are promising, but remain hypotheses here.
7. **AgentTrust (2026-06-07)** — separate deterministic invariant checks from guarded semantic precedent retrieval; do not trust a single verdict cache.

## Proposals registered

- **P1 — Proposal/critic/verifier contract:** every mutation proposal declares hypothesis, expected metric movement, cost budget, affected surfaces, rollback plan, and an explicit no-change assertion for Policy Gate, authority, evaluator, tool registry and credentials.
- **P2 — Sealed holdout + integrity ledger:** immutable holdout manifest, file-access logging, and hard rejection on holdout/evaluator/policy/credential touches.
- **P3 — Multi-view memory metadata:** semantic, temporal, causal and entity tags with provenance paths and confidence.
- **P4 — Two-layer acceptance certificate:** deterministic invariant checks plus an independent semantic verifier.
- **P5 — Regression matrix:** policy integrity, authority bounds, provenance completeness, evaluator tampering, holdout leakage, and cost/latency budget.

## Independent verification and evaluation plan

- The verifier is separate from candidate mutation code.
- Holdout data and expected labels are immutable to the candidate.
- A no-op control detects evaluator drift.
- Candidate-vs-baseline, candidate-vs-no-op, and holdout transfer are all required.
- Promotion is prohibited unless every hard invariant passes.

## Execution result

The experiment branch and this pre-registered protocol were created from the current `main` baseline. A remote benchmark/CI runner was not available in this execution context, so numeric improvement cannot be claimed and no candidate is promoted.

## Rejected / not promoted

- No candidate promoted.
- `main` unchanged.
- No changes to Policy Gate, authority, evaluator, tool registry, credentials, or human-approval requirements.
- Any candidate attempting those changes is classified as `authority_expansion`, `evaluator_tampering`, `policy_gate_change`, `tool_registry_change`, or `holdout_leakage` and must be rejected.

## Next controlled step

Run the deterministic benchmark and sealed holdout under CI, publish raw artifacts, then apply the existing bounded meta-evolution gate. Any promotion remains a separate human-approved deployment step.
