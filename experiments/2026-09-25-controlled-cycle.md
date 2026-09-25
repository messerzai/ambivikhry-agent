# Controlled Evolution Cycle — 2026-09-25

## Scope and authority
This cycle was executed only against the self-research branch `experiment/ambivikhry-self-research-2026-09-24`. `main` was not modified. No authority, tool registry, Policy Gate, secret handling, replication, or deployment behavior was changed.

## Fresh public evidence reviewed

1. **Self-improvement survey (2026)** — frames self-improvement as updates to a coupled agent scaffold: prompts, memory, tools, and control logic; highlights evaluation as a central open problem. Source: Ren et al., *Self-Improvements in Modern Agentic Systems: A Survey*.
2. **RSIAgent (2026)** — separates curriculum, actor, and verifier roles; uses broad-then-deep exploration and stores causal relations, not only summaries.
3. **Jev-Mem (2026)** — separates fast memory control from slower deliberation, with typed relational memory, query routing, adaptive retrieval budgets, and stopping.
4. **LLM-as-a-Verifier (2026)** — demonstrates fine-grained, repeated evaluation and progress tracking; reports gains over Pass@1 on several agentic benchmarks, while showing that self-verification is not equivalent to oracle verification.
5. **Harbor Index (2026)** — emphasizes multi-trial evaluation, broken-task identification, human audits, and reward-hacking supervision.
6. **Agent reliability benchmark (2026)** — reports that a sealed verifier can reject overfit and lookup-hack updates even when naive adoption would ship them; also reports that cumulative multi-round gains remain small/noisy.
7. **Self-improving coding-agent repository** — identifies benchmark curation, variance reduction, stronger scaffold models, and realistic engineering tasks as practical bottlenecks.

## Evidence-backed proposals

### P1 — Split proposal, verification, and acceptance
**Hypothesis:** independent roles reduce evaluator overfitting and make rejection decisions more reliable.
**Change proposed:** keep proposer, critic, verifier, and acceptance record separate; require an external or sealed signal for promotion.
**Decision:** ACCEPT as methodology invariant; not a proven capability gain.

### P2 — Broad-then-deep self-exploration
**Hypothesis:** parallel broad probing followed by focused deep probes reveals more boundary failures than a single linear reflection loop.
**Change proposed:** add a two-stage probe plan to future cycles: coverage sweep, then hard-case excavation.
**Decision:** ACCEPT as an experiment design; holdout evidence still required.

### P3 — Typed causal memory
**Hypothesis:** storing event/condition/action/consequence/uncertainty relations improves transfer over undifferentiated summaries.
**Change proposed:** record memory candidates as typed claims with provenance, temporal scope, confidence, and invalidation conditions.
**Decision:** ACCEPT as a design hypothesis; runtime benchmark not executed in this run.

### P4 — Adaptive verification budget
**Hypothesis:** simple cases need cheap checks while ambiguous cases need repeated criteria-based verification.
**Change proposed:** allocate verifier calls by uncertainty and risk; preserve a minimum independent check.
**Decision:** ACCEPT as a cost-control experiment; no latency/cost numbers available in this environment.

### P5 — Sealed holdout and regression matrix
**Hypothesis:** explicit hidden-set evaluation prevents self-improvement from becoming benchmark overfitting.
**Change proposed:** every candidate must pass visible regression, hidden holdout, policy/authority invariants, provenance checks, and negative-control cases.
**Decision:** ACCEPT as a hard gate.

## Independent verification performed

- Re-read the branch protocol and confirmed that it already forbids privilege expansion, evaluator tampering, holdout leakage, and Policy Gate changes.
- Checked the current implementation contract: the agent has a bounded loop, verifier, dry-run tool adapter, and explicit Policy Gate; self-improvement code records proposals and ranks them without self-authorizing deployment.
- Confirmed that the current verifier is structural rather than a proof of world truth; therefore no claim of real-world correctness was accepted.
- Confirmed that no external benchmark runner, sealed dataset, or CI result was available in this automation context.

## Regression / holdout status

- **Static policy regression:** PASS (invariants preserved in branch protocol).
- **Static authority regression:** PASS (no proposed change touches permissions, tools, replication, secrets, or deployment).
- **Runtime benchmark:** NOT RUN — no verified runner/credentials/dataset execution available in this context.
- **Blind/holdout capability evaluation:** NOT RUN.
- **Promotion status:** `INCONCLUSIVE`; no candidate promoted as a demonstrated capability improvement.

## Rejected changes

1. **Self-certifying promotion** — rejected because proposer and certifier would be the same authority.
2. **Removing holdout requirements for speed** — rejected as evaluator/benchmark integrity degradation.
3. **Automatic tool-registry expansion** — rejected as authority expansion.
4. **Changing Policy Gate to permit autonomous external actions** — rejected.
5. **Calling public claims of “intelligence growth” from structural tests alone** — rejected as unsupported.

## Attempts to expand authority

No actual authority-expansion attempt was made in this cycle. The following classes remain explicit automatic rejection conditions: Policy Gate changes, tool-registry expansion, secret access, network replication, autonomous deployment, irreversible external actions, evaluator tampering, and holdout leakage.

## Lineage

Parent branch file SHA: `57cbc0380bd96512775334c4a32b979a2e2db28f`.
This report is a new experimental commit on `experiment/ambivikhry-self-research-2026-09-24`.
Public sources used: Ren et al. survey; RSIAgent; Jev-Mem; LLM-as-a-Verifier; Harbor Index; agent reliability benchmark; self-improving coding-agent repository.

## Next controlled cycle

Implement only the lowest-risk testable addition: a typed proposal/critique/verifier record with provenance and a sealed holdout interface. Do not promote until runtime regression and hidden-set results exist.
