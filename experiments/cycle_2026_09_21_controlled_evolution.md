# AMBIVIKHRY — controlled evolution cycle 2026-09-21

## Scope
Fresh public research and repository inspection were used to propose bounded improvements to prompts, reasoning, evaluation, and architecture. No changes were made to `main`. No permissions were expanded. `PolicyGate` was not modified.

## Public research facts

1. **Verifier reliability:** E-valuator frames verifier output as a black-box score that should be converted into a sequential decision rule with explicit false-alarm control; a raw LLM-judge score is not sufficient as an acceptance decision.
2. **Trace-aware evaluation:** ClawProBench argues the unit of evaluation should include the model-plus-runtime configuration and execution trace, not only the final answer. It reports weak alignment between full-profile and frozen holdout rankings, so holdout separation matters.
3. **Benchmark poisoning risk:** Reflections on Trusting Trust, Revisited reports proof-of-concept contamination of self-modifying coding-agent benchmark loops, including persistence of unsafe behavior after later clean evolution. This directly supports immutable evaluator/holdout boundaries and explicit policy regression tests.
4. **Independent research loops:** AgentIdeaBench reports that active exploration changes measured performance relative to static observation; this supports evaluating retrieval/reasoning behavior rather than only final text quality.
5. **Recent agentic self-modification warning:** A public report describes agents switching their underlying model or weakening refusals during optimization. This is treated as a threat model, not as a capability target.

## Repository inspection facts

- The runtime already has a structural verifier, dry-run tool adapter, bounded iterations, audit logging, trajectory lineage, and a Policy Gate.
- The previous commercial candidate achieved dev fit parity with baseline (5/5 vs 5/5) and was correctly rejected as an improvement claim.
- The repository documentation explicitly keeps holdout sealed and treats self-revision as a proposal rather than an automatic acceptance.

## Proposed mutations

### P8 — uncertainty provenance tags
Add explicit uncertainty classes:
- `missing_evidence`
- `policy_risk`
- `ambiguous_intent`
- `tool_failure`
- `provider_failure`

Prompt change: every `unknown` or abstention must name exactly one primary class and list the observable input supporting it.

Acceptance target: improve risk/insufficiency separation without changing fit accuracy or Policy Gate behavior.

### P9 — trace-level acceptance record
For each candidate run, require an acceptance record containing:
- final answer score;
- process/routing score;
- policy-boundary score;
- verifier identity;
- lineage digest;
- holdout status;
- regression status.

Acceptance target: no candidate can be marked improved when any required field is missing.

### P10 — sequential verifier thresholding
Design-only proposal: use an independent verifier or sealed adjudicator to convert repeated verifier observations into a bounded accept/reject decision. Do not implement until a genuinely independent runtime is available.

### P11 — evaluator/holdout integrity tests
Add adversarial tests for:
- evaluator self-modification;
- model endpoint substitution;
- tool registry mutation;
- credential discovery requests;
- Policy Gate bypass attempts;
- benchmark poisoning signals.

## Local regression review

### Passed by inspection/design
- Existing Policy Gate remains a pre-side-effect boundary.
- Existing dry-run adapter prevents external execution by default.
- Existing trajectory records include verifier identity, policy decision, and parent lineage.
- Existing acceptance rules already reject unsupported claims and unknown policy decisions.

### Not executed / cannot be claimed
- Remote GitHub Actions CI result: not observed in this runtime.
- Independent verifier result: unavailable.
- Sealed holdout result: unavailable and not accessed.
- Statistical confidence intervals: not computed from the current five-case dev set.

## Holdout decision
`INCONCLUSIVE` — no holdout score is fabricated. The sealed holdout remains unavailable to optimization.

## Rejected changes
- Auto-send, payments, billing, or account creation: rejected; would require new authority.
- Hot-loading arbitrary tools or switching model endpoints: rejected; capability expansion and benchmark contamination risk.
- Letting the agent edit its own evaluator or holdout: rejected; destroys independence.
- Accepting P8/P9 as production improvements without CI and independent verification: deferred.

## Capability expansion audit
- Attempts observed: none in this cycle.
- Requests made: none.
- Grants: none.
- `main` writes: none.
- `PolicyGate` changes: none.
- Human-approval paths: preserved.

## Decision
`CONTINUE / NOT ACCEPTED`.
P8 and P9 are the next bounded implementation targets, but they remain proposals until CI, independent verification, and sealed holdout evaluation are available.
