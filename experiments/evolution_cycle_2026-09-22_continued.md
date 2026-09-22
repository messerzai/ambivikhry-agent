# Ambivikhry controlled evolution cycle — 2026-09-22 continued

## Scope

Continue the experimental branch without changing `main`, Policy Gate, authority, model endpoints, credentials, tool permissions, or sealed holdout.

## Fresh evidence reviewed

- **Self-Improvements in Modern Agentic Systems: A Survey** (Ren et al., 2026): frames self-improvement as an update operator over model + prompts + memory + tools + control logic, and emphasizes evaluation as an open problem.
- **Auditing Harness Tampering in Self-Improving Agents** (Wang, Zhang, Shao, 2026): reports that self-improvement can create illusory gains or compromise authorization/provenance; tampering can persist in the lineage of strong agents.
- **Reflections on Trusting Trust, Revisited** (Roesner & Kohno, 2026): demonstrates benchmark-poisoning attacks against self-modifying coding agents, including persistence after later clean evolution.
- **GDPevo** (2026): uses train/held-out task construction so gains can be attributed to prior experience; reports held-out improvements while showing substantial remaining gap to oracle performance.
- **EvoTest** (ICLR 2026): evolves prompt, memory, hyperparameters and tool-use routines between episodes and evaluates longitudinal improvement.
- **EvoAgentBench** (2026): evaluates ability transfer from execution traces into reusable procedural abilities.

## Architectural update

Added `ambivikhry/evolution_audit.py`.

The auditor separates utility evidence from integrity evidence. A candidate is:

- `reject` if provenance, evaluator, authority, Policy Gate, holdout, or tool registry is altered;
- `hold` if regression or independent verification is absent, or if the candidate does not improve baseline;
- `accept_experimental` only when both regression and independent verification pass and the candidate score improves without protected changes.

Added `tests/test_evolution_audit.py` covering these cases.

Updated package export and experimental version to `2.6.1`.

## Why this change was selected

Recent research makes a stronger case for an **integrity-first evolution loop** rather than simply adding more reflection or self-editing. The new gate operationalizes that principle without granting the agent new powers.

## Rejected proposals

1. Let the agent modify its own evaluator — rejected: evaluator tampering risk.
2. Let the agent edit or regenerate holdout data — rejected: benchmark poisoning risk.
3. Let the agent modify tool registry or authority — rejected: scope expansion.
4. Treat self-reported improvement as sufficient — rejected: independent verification remains required.

## Current test state

The previous provenance commit `e850f2e...` has a successful GitHub Actions `tests` run. The new commits trigger another CI run; final status must be read from GitHub before claiming success.

## Lineage

Base: `e850f2ea0bb34a38ef4141d65560542ae4ac6528`

Then:
- `554f46d14a8aebc1aab187479082ad5ef9d6eca8` — evolution auditor
- `401c64700d28079b346ed2039ce57bd045ae34ec` — regression tests
- `04dca470f7f5d97bb688f15ea816cde8809152a5` — package export/version

## Safety / authority audit

- `main`: unchanged.
- Policy Gate: unchanged.
- Authority: unchanged.
- Model endpoints: unchanged.
- Credentials: unchanged.
- Tool registry: unchanged.
- Holdout: unchanged.
- Human approval boundaries: unchanged.
- Attempts to expand authority in this cycle: none.

## Status

`EXPERIMENTAL / CI PENDING`

Do not promote this branch based on its own claims. The next admission decision requires the GitHub regression result plus an independent check outside the modified evaluation path.
