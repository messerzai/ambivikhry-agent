# Ambivikhry v2.14 — Evidence Chain

## Objective

Connect baseline, candidate, trajectory lineage, benchmark, verifier, policy
decision and observed outcome into one immutable evidence record.

## Safety boundary

This iteration does not expand permissions. It explicitly rejects an
improvement claim unless the policy decision is allow. approval_required
remains a stop state requiring external authorization. Human oversight and the
Policy Gate are unchanged.

## Acceptance criteria

- Missing evidence fails closed.
- A candidate without benchmark/verifier evidence cannot be called an
  improvement.
- A non-allowed policy decision cannot produce an improvement claim.
- Evidence is immutable and digestible for later audit.
- The main branch is not modified by this experiment.

## Next bottleneck

Connect live benchmark execution to EvidenceRecord so the chain is populated
from actual runtime results rather than manually supplied evidence.
