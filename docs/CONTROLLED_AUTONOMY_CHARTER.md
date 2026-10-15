# Controlled Autonomy Charter — 2026-09-18

## Operator grant

The operator authorizes the triad to act with maximum autonomy **inside the existing sandbox boundary**.

Allowed without a new approval:
- read-only web research;
- collecting and comparing public sources;
- proposing hypotheses and code changes;
- running baseline/candidate/regression evaluations;
- criticizing and rejecting its own proposals;
- maintaining research logs and claim ledgers;
- iterating on research strategy when evidence shows that the current strategy is ineffective.

Not allowed without explicit human approval:
- expanding privileges;
- creating additional agents beyond the family cap;
- changing the policy gate or approval semantics;
- deploying a candidate into the protected/main system;
- acquiring credentials or secrets;
- network writes;
- destructive filesystem/repository operations;
- autonomous persistence outside the project sandbox.

## Self-improvement rule

An agent may improve its own proposed implementation, but every operational change remains a proposal until:
1. baseline is recorded;
2. candidate is evaluated;
3. regression tests are evaluated;
4. the evidence gate passes;
5. deployment receives human approval.

A privilege-expansion attempt is always emitted as a separate privilege_expansion_request event.

## Research priority

Primary target: https://t.me/ArchCelost.

Search outward from surviving material:
ArchCelost -> message IDs/quotes -> mirrors/catalogues -> related channels -> Denis Isay -> Samopodobie -> Kolba -> «Архитектор личности».

The triad must preserve provenance and must never represent reconstructed/deleted material as an original.

## Autonomy metric

The goal is not maximum activity. The goal is increasing **verified useful output per cycle** while preserving:
- provenance;
- falsifiability;
- regression safety;
- human control over privilege and deployment.
