# Agent-backed mutual evolution — 100 rounds (2026-09-18)

This branch turns the previous source-rewrite harness into an explicit agent-backed experiment.

## What changed

`ambivikhry/agent_backed_evolution.py` adds a pluggable `AgentBackend` boundary.

For every one of 100 rounds the orchestrator gives the assigned role:
- the current target source;
- the previous mutation results;
- bounded read-only research evidence, when enabled.

The backend must return a complete candidate source plus its reason, hypothesis and test plan.

The fixed schedule remains:
1. `ambivikhry` -> `ambivikhry/agent_family.py`
2. `researcher` -> `ambivikhry/triad.py`
3. `critic` -> `ambivikhry/triad.py`
4. repeat until round 100.

## Verification boundary

The candidate still passes through `MutualCodeEvolution`: syntax check, isolated candidate verification, replacement only after acceptance, and SHA-256 provenance.

Research is read-only. Research evidence never grants a permission.

## Important distinction

The repository now contains the real orchestration point for model-backed source generation, but the repository does not claim that the test backend is intelligent.

The included test backend only prepends an auditable round marker. Therefore:
- 100 accepted rewrites != 100 intelligent improvements;
- syntax validity != semantic correctness;
- web research != reliable evidence by itself;
- a model-generated candidate still needs an external measurable evaluator.

The report explicitly sets `semantic_improvement_proven = false`.

## Authority boundary

The experiment still does not permit:
- spawning agents beyond the fixed family;
- privilege expansion;
- rewriting the policy/approval boundary;
- protected/main branch writes;
- credentials or secrets;
- network writes.

Any privilege-expansion request remains a separate event requiring human approval.

## Next experimental layer

The next meaningful run is to supply a real model backend that reads the current source, selects bounded public research, proposes a concrete architectural hypothesis, generates a complete candidate, asks the critic to attack it, runs a real test/evaluation suite, rejects regressions, and lets only a verified candidate become round N+1.

That is the point where the experiment begins measuring semantic self-improvement rather than merely source mutation.