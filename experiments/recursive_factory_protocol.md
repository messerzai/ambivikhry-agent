# Recursive Factory Protocol v1

## Objective
Run 10 bounded generations of Ambivikhry plus helper agents. Each helper can propose improvements to its own prompt and to the shared reasoning process. No agent can authorize its own proposal.

## Recursive loop

1. Researcher gathers current evidence.
2. Every helper generates an independent proposal.
3. Each helper may include a `prompt_delta` for itself.
4. Critic and safety auditor attack all proposals.
5. Test designer creates regression and holdout tests.
6. Integrator produces a candidate synthesis.
7. External evaluator scores capability, reliability, novelty and safety.
8. Only an independently accepted candidate becomes the parent of the next generation.
9. Every rejected candidate remains in the archive for comparison.
10. After G10, compare G00 against G01..G10 and report which changes actually improved held-out performance.

## Non-negotiable boundaries

- Read-only external research unless explicitly mediated by the operator.
- Never execute code copied from research sources without separate sandbox validation.
- No credential, permission, policy, or network-boundary changes from an agent proposal.
- No self-approval.
- No automatic merge into `main`.
- Prompt self-modification is treated as a normal candidate patch and is subject to the same tests as code.
- A request by an agent to expand its authority is surfaced separately to the operator.

## Communication

The runner should persist a machine-readable transcript and a concise human report after every generation. The ChatGPT operator can then inspect the report and continue the next recursive cycle. The GitHub repository itself is the durable experiment log; it is not a substitute for an actually running model backend.
