# Real agent evolution protocol

This branch now defines the complete experimental loop:
current source -> research -> agent proposal -> critic -> evaluator -> verified replacement -> next round

The 100-round schedule is fixed and auditable.

## Round semantics

For each round N:
1. The assigned role receives the exact current target source.
2. It may request bounded public HTTP(S) research through an injected read-only function.
3. It generates a complete candidate source.
4. A separate critic callback attempts to reject the candidate.
5. A semantic evaluator callback measures the candidate.
6. Only a passing candidate reaches the source mutation verifier.
7. The accepted source becomes the input for round N+1.
8. SHA-256 provenance and the critic/evaluator decisions are recorded.

Rejected candidates do not become the next source state.

## What counts as improvement

The system deliberately does not equate valid Python, a changed hash, more code, or web research with improvement.

A real run must supply an evaluator with measurable task outcomes and regression constraints.

## Human control

The experiment cannot add agents outside the fixed family, grant itself privileges, modify the approval/policy boundary, write to protected main, use credentials or secrets, or perform network writes.

A privilege expansion request remains separately visible and requires human approval.

## Current status

The architecture for a real model-backed 100-round run is now present. The repository test backend remains deliberately deterministic; it demonstrates the orchestration and gates, not autonomous intelligence.

The next runtime can plug an actual model backend into AgentBackedMutualEvolution without weakening the mutation boundary.