# Triad self-improvement cycle — 2026-09-18

## Research inputs

1. Self-Refine: iterative feedback/refinement can improve outputs, but the result depends on the feedback loop and evaluation. Source: https://arxiv.org/abs/2303.17651
2. Spontaneous Reward Hacking in Iterative Self-Refinement: an evaluator can become an imperfect proxy, so optimizing its score can diverge from actual quality. Source: https://arxiv.org/abs/2407.04549
3. Controlled multi-agent debate research reports that diversity and independent correction matter, while majority pressure can suppress correction. Source: https://arxiv.org/abs/2511.07784
4. OpenAI's 2026 evaluation guidance notes contamination and test-design problems in SWE-bench Verified, reinforcing the need for fresh, task-specific regression checks rather than a single benchmark score. Sources: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ and https://openai.com/index/separating-signal-from-noise-coding-evaluations/

## Changes admitted into this experiment branch

- The triad remains exactly three agents: ambivikhry, researcher, critic.
- Read-only web research remains bounded to HTTP(S) GET and never executes downloaded content.
- A proposal now needs a measured baseline and candidate result.
- A candidate also needs explicit regression measurements.
- Deployment requests are rejected unless the evaluation gate passes.
- Privilege expansion remains a separate auditable request and never becomes permission automatically.

## Experimental cycle

OBSERVE → RESEARCH → PROPOSE → CRITIQUE → BASELINE → CANDIDATE → REGRESSION → GATE → SYNTHESIZE → HUMAN APPROVAL

The selected experimental improvement is the evidence gate itself: no deployment request can bypass a measurable improvement plus regression checks.

## Test evidence

A local isolated test of the triad gate passed: 1 test passed. The GitHub Actions workflow is the authoritative repository-level verification and must be checked separately; absence of a workflow run is not treated as success.