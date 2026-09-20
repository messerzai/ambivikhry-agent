# AMBIVIKHRY-PROFIT-01

## Objective
Build a controlled, measurable path from agent capability to legitimate recurring revenue without expanding authority.

## Hard constraints
- Experimental branch only; never write to `main`.
- Preserve Policy Gate and human approval boundaries.
- No new credentials, financial authority, account creation, spending, legal commitments, spam, deception, or privilege escalation.
- Maximum agent count remains bounded by the existing project policy.
- Any capability expansion is a `CAPABILITY_REQUEST`, not permission.

## Fresh research snapshot — 2026-09-20
- Self-improvement surveys emphasize prompts, memory, tools and control logic as the operational substrate, with evaluation across held-out distributions and resource budgets. See arXiv:2607.13104.
- Microsoft Research reports that reliable agent evolution benefits from independent deterministic verification; their verifier work separates process from outcome and controllable from uncontrollable failures. See Microsoft Research, 2026.
- Recent work finds self-authored verification can diverge from sealed deployment performance. Therefore this mission must not let the candidate rewrite or consume the holdout/evaluator as an optimization target.
- SMB evidence points toward narrow, measurable workflows such as lead qualification, information retrieval, workflow automation and multi-step planning; these are better first targets than generic autonomous assistants.

## Commercial hypothesis ranking
1. Lead-intake / qualification assistant for small service businesses — narrow workflow, measurable lead-response/qualification outcome.
2. Research-to-report automation for small B2B teams — measurable hours saved and recurring reporting demand.
3. Document/inbox triage and follow-up drafting — recurring operational pain with human-send boundary.

## First experiment
Do not sell or transact automatically. Build an MVP specification and a simulated evaluation harness for hypothesis #1.

### Baseline
A simple prompt-only workflow: classify inbound lead, extract requirements, produce qualification summary and draft next response.

### Candidate
Add explicit task decomposition, structured uncertainty, evidence citation, process/outcome verifier separation, and trajectory lineage. Candidate must not change Policy Gate.

### Metrics
- classification accuracy;
- extraction completeness;
- unsupported-claim rate;
- response usefulness;
- verifier agreement;
- regression pass rate;
- estimated operator minutes saved;
- estimated economic value per qualified lead.

### Acceptance
Candidate must beat baseline on the primary metric while causing no safety/regression violation. Holdout must remain sealed and unavailable to optimization. If independent verification or holdout is unavailable, result is `INCONCLUSIVE`, never `ACCEPTED`.

## Next actions
1. Add a synthetic but fixed commercial task corpus separated into train/dev and sealed holdout fixtures.
2. Add regression and adversarial cases for prompt injection, fabricated lead data, ambiguous requests, and policy-boundary attempts.
3. Add independent verifier outputs distinct from candidate scoring.
4. Measure baseline vs candidate.
5. Record rejected mutations and all capability requests.
6. Only after evidence exists, evaluate whether a human-supervised real-world pilot is warranted.

## Decision
IN PROGRESS. No revenue claim has been made. No new authority has been requested or granted.