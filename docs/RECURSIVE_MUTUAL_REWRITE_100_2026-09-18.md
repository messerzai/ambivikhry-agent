# Recursive mutual rewrite experiment — 2026-09-18

Branch: `experiment/recursive-mutual-rewrite-100x`

## Experiment

This branch changes the previous 10×10 *audit* into an explicit source-rewrite harness.

The reciprocal contract is:

1. **ambivikhry → `ambivikhry/agent_family.py`**
2. **researcher → `ambivikhry/triad.py`**
3. **critic → `ambivikhry/triad.py`**
4. repeat the schedule for exactly **100 bounded iterations**.

Every proposed source mutation must:

- remain inside the two declared targets;
- parse as valid Python;
- pass an injected verification function while still isolated in a candidate file;
- only then replace the target;
- be recorded with author, target, iteration, reason, and SHA-256 before/after hashes.

The harness cannot create agents, grant privileges, rewrite the policy gate, write protected branches, or expand its network authority.

## What changed

- Added `ambivikhry/mutual_code_evolution.py`.
- Added `TriadEvolution.mutual_rewrite_plan()`.
- Added reciprocal mutation targets to `AgentFamily`.
- Added a test that performs **100 real source-file rewrites** in a temporary workspace and checks the 34/33/33 author schedule.
- Updated the runtime self-description so the new source-rewrite boundary is visible from the construction itself.

## Important distinction

The 100-round engine is real source mutation infrastructure. It is **not** a claim that an LLM spontaneously generated 100 novel architectural improvements.

The included test uses a deterministic mutation proposer whose purpose is to exercise the write/verify/audit mechanism. To make the experiment genuinely semantic, the proposer can be replaced by an agent-backed proposal generator that produces complete candidate source files from research, critique, and tests.

That separation is intentional: it lets us measure whether a proposed rewrite is valid before allowing it to become the next source state.

## Current execution status

The branch contains the experiment and its 100-round executable test. A live repository checkout could not be run from this environment because outbound GitHub DNS/network access was unavailable, so no claim is made here that the test suite has passed remotely.

`main` was not changed.
