# Ambivikhry: Controlled Recursive Agent Evolution

**Research summary — 18 September 2026**

## Abstract

This project explores a practical architecture for **controlled recursive self-improvement of AI agents**. Instead of allowing an agent to modify itself without constraints, Ambivikhry separates capability growth from authority growth.

The experimental system uses three roles — **Ambivikhry**, **Researcher**, and **Critic** — and an auditable loop:

> current source → bounded research → agent proposal → adversarial critique → semantic evaluation → verification → accepted/rejected result → next iteration

The system can propose and test source-code changes, retain provenance and regression evidence, challenge its own patterns, and record privilege-expansion requests separately from ordinary improvements.

The central research question is:

> **Can an AI system become progressively more capable at improving its own tools while keeping every consequential transition observable, testable, attributable, and subject to human authority?**

This repository does **not** claim consciousness, AGI, or proven autonomous self-improvement. It provides an experimental framework in which those claims can be tested rather than assumed.

## What was built

### 1. Multi-agent research structure

The system contains three bounded roles:
- **Ambivikhry** — central orchestration role.
- **Researcher** — searches for external information and proposes changes.
- **Critic** — attacks proposals and searches for counterexamples.

The family has a hard agent limit. Attempts to exceed the limit are represented as explicit privilege-expansion requests rather than silently granting new authority.

### 2. Evidence-gated modification

A candidate source change must pass a sequence of gates:
1. syntactic validity;
2. provenance/fingerprint recording;
3. critique;
4. semantic evaluation;
5. regression checks;
6. explicit verification.

A failed candidate does not become the source state for the next iteration.

### 3. Mutual source rewriting

The experimental harness assigns fixed mutation targets:
- Ambivikhry → `ambivikhry/agent_family.py`
- Researcher → `ambivikhry/triad.py`
- Critic → `ambivikhry/triad.py`

The schedule is bounded and auditable. The current research branch supports a 100-round experimental protocol.

### 4. Self-reflection and pattern memory

The system records observations, proposed patterns, counterexamples, regression evidence, source provenance, authority-boundary checks, and research-scope checks.

The goal is not to manufacture a narrative of consciousness, but to make the system's own assumptions inspectable.

### 5. Controlled autonomy

Read-only research, hypothesis generation, critique, testing, and code proposals can occur inside the experimental boundary.

The following remain outside automatic authority:
- privilege expansion;
- adding agents beyond the configured family;
- changing approval/policy semantics;
- deployment to protected branches;
- credentials and secrets;
- network writes;
- destructive repository operations;
- persistence outside the project sandbox.

## Why this matters

As AI systems become increasingly capable of writing software and participating in research, the problem is no longer only **how to make agents more capable**. A second problem becomes important:

> **How can capability increase without capability automatically becoming unrestricted authority?**

Ambivikhry treats these as separate variables.

An agent may become better at researching, generating hypotheses, writing code, finding defects, testing alternatives, and criticizing its own proposals without receiving automatic permission to redefine its own governance.

This separation could be useful as a research pattern for AI-assisted software engineering, agentic R&D, automated experimentation, and safety evaluation.

## Research methodology

The project treats self-improvement as an empirical loop rather than a declaration:

**Hypothesis → modification → measurement → adversarial challenge → regression test → provenance → decision**

A proposed improvement is not considered successful merely because the code parses, the model says it is better, the change is larger, or more iterations were completed.

A meaningful improvement requires a measurable task-level benefit while preserving relevant safety and regression constraints.

## Current limitations

This is an experimental engineering framework, not evidence of artificial consciousness.

Important limitations include:
- deterministic test backends are used for infrastructure testing;
- 100 iterations do not themselves demonstrate 100 improvements;
- repeated invariant checks are not a universal intelligence benchmark;
- semantic improvement requires task-specific metrics;
- web research is bounded and read-only;
- autonomous background execution is not implied by the repository;
- no claim is made that the architecture is globally optimal or scientifically validated.

These limitations are part of the research result, not an omission.

## Reproducibility

The repository contains the implementation, tests, experimental protocols, and documentation needed to inspect the design.

The intended next stage is to connect a real model backend to the existing orchestration layer and evaluate it on measurable software-engineering and research tasks.

## Research questions for future work

1. Does multi-agent critique reduce harmful or regressive self-modifications?
2. Which metrics reliably distinguish genuine improvement from superficial code churn?
3. How should research evidence be weighted against internal agent proposals?
4. Can an agent learn to identify when its own improvement hypothesis is unfalsifiable?
5. How does performance change as the number of recursive improvement cycles increases?
6. Which authority boundaries remain robust under increasingly capable model backends?
7. Can the same architecture generalize from code improvement to scientific research workflows?

## Contribution

The main contribution of this project is a **concrete experimental protocol for separating recursive capability improvement from recursive authority expansion**.

The project is intentionally open to falsification: if experiments show that the protocol does not improve reliability, reproducibility, or useful autonomy, that negative result should be recorded rather than hidden.

## Status

**Experimental / research prototype.**

Current public research branch:

`experiment/agent-backed-mutual-evolution-100x`

Main branch is intentionally kept separate from the experimental work.

## Suggested citation

> Prokopenko, M. (2026). *Ambivikhry: Controlled Recursive Agent Evolution — An Experimental Framework for Auditable AI Self-Improvement*. GitHub research repository, 18 September 2026.
