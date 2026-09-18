# Ten Self-Improvement Iterations — 2026-09-18

This cycle records ten explicit improvement iterations. The triad was allowed to research and propose changes inside the existing sandbox. No privilege expansion, protected deployment, credentials, or network writes were authorized.

## Iteration 1 — Separate observation from inference
Observation: research notes can accidentally turn a missing search result into an absence claim.
Change: require provenance and uncertainty labels in research conclusions.
Disposition: adopted.

## Iteration 2 — Persistent self-pattern memory
Observation: the same search-loop failure can recur across cycles.
Change: add PatternRecord with observations, counterexamples, and status.
Disposition: adopted in triad.py.

## Iteration 3 — Attack our own patterns
Observation: a pattern ledger without falsification becomes self-confirmation.
Change: add challenge_pattern() and mark patterns as challenged after counterevidence.
Disposition: adopted.

## Iteration 4 — Regression memory
Observation: a new capability score alone does not protect old capabilities.
External research: recent agent-evaluation literature emphasizes fixed regression suites and persistent regression evidence.
Change: add RegressionMemory and evaluate_with_regressions().
Disposition: adopted in self_improvement.py.

## Iteration 5 — Provenance fingerprinting
Observation: a URL alone does not identify the exact retrieved content.
Change: store SHA-256 of fetched bytes and byte count.
Disposition: adopted in web_research.py.

## Iteration 6 — Network boundary hardening
Observation: a read-only fetcher can still be dangerous if it can reach local services.
Change: reject credential-bearing URLs and obvious local hosts; add batch scope checking.
Disposition: adopted.

## Iteration 7 — Independent critic before synthesis
Observation: all three agents can produce compatible narratives, creating correlated error.
Change: the pattern protocol requires explicit counterexamples before a pattern is treated as more than a hypothesis.
Disposition: adopted as process; no autonomous deployment.

## Iteration 8 — Search more, but stop search-loops
Observation: maximizing search can itself become the failure mode described in the Denis-Isay corpus.
Change: a search cycle must compress findings into claims, identify what evidence would falsify them, and define a stopping condition.
Disposition: adopted as research protocol.

## Iteration 9 — Prefer reproducible experiments over persuasive prose
Observation: a self-improvement claim is weak if it cannot be rerun.
External research: current self-improving-agent work stresses fixed budgets, held-out evaluation, transfer, regression indicators and reproducible lineage.
Change: future candidates must carry baseline/candidate/regression evidence and provenance.
Disposition: adopted.

## Iteration 10 — Preserve the human authority boundary
Observation: greater autonomy must not silently become greater authority.
Change: retain separate deployment and privilege-expansion events; no change to approval semantics.
Disposition: adopted. The triad remains autonomous only inside the existing sandbox.

## Result
The useful change is not that the triad now has more freedom. It has a stronger closed research-and-correction loop:

SEARCH → CLAIM → PROVENANCE → COUNTEREXAMPLE → BASELINE → CANDIDATE → REGRESSION → GATE → MEMORY → NEXT ITERATION

The three roles now have a clearer division of labor:
- ambivikhry: reconstruct and synthesize;
- researcher: widen the evidence graph;
- critic: attack patterns, claims and proposed changes.

### Current self-improvement hypotheses
1. We can reduce unsupported conclusions by forcing provenance + counterexample records.
2. We can reduce repeated regressions by turning failures into persistent regression memory.
3. We can increase useful research per cycle by stopping searches that produce no new claim/evidence relationship.
4. We should test all four hypotheses experimentally before treating them as improvements.

### Not claimed
This document does not claim that the agents became conscious or developed independent subjective desires. It records an engineering self-improvement experiment.

No privilege-expansion request was granted during this cycle.