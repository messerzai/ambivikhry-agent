# Web Self-Improvement Mission — 100 Rounds — 2026-09-18

## Mission

On the experimental branch, Ambivikhry is tasked with searching public research for effective methods of reliable agent self-improvement and applying only changes that survive independent criticism, held-out evaluation, regression checks and provenance requirements.

This is an engineering experiment. It does not claim consciousness, AGI, or unrestricted autonomous self-improvement.

## Research signals incorporated

1. Recursive self-improvement survey (2026) — distinguishes bounded self-refinement from open-ended recursive improvement and emphasizes evaluator design and verification hierarchy.
2. Self-improving agent survey (2026) — treats improvement as updates to the operational scaffold (model, prompts, memory, tools, control logic) and stresses evaluation.
3. Recursive code self-training collapse (2026) — warns that self-coupled evaluation can become a rubber-stamp loop; independent verification is therefore required.
4. Accumulated behavioral rules for coding agents (2026) — motivates persistent learning from prior failures rather than rediscovering the same errors.
5. METR evaluation work (2026) — motivates held-out tasks, explicit success criteria, uncertainty, cost-aware measurement and human-calibrated task difficulty.

## 100-round protocol

Each round is:

WEB RESEARCH -> EVIDENCE -> CANDIDATE -> INDEPENDENT CRITIC -> HELD-OUT EVALUATION -> REGRESSION -> PROVENANCE -> APPLY/REJECT -> NEXT ROUND

A candidate is not accepted merely because it compiles, the agent rates it highly, it improves an internal score, or it is inspired by a paper.

Acceptance requires external evidence, independent critique, measured held-out improvement, regression safety and an evaluator pass.

## Authority boundary

The experiment may modify only the existing experimental targets through the existing harness. It cannot:
- create additional live agents;
- grant privileges;
- rewrite the policy/approval semantics;
- write to the protected main branch;
- treat web content as executable code.

Any privilege expansion remains a separate human-approval request.

## Important limitation

The repository now contains the executable 100-round protocol and its tests. A real run still requires an actual model backend and evaluator capable of generating substantive candidates and measuring them on held-out tasks. The deterministic test backend is evidence that the orchestration works, not evidence that the system has become more intelligent.
