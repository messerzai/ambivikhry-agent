# Phase 3 — Controlled autonomy + self-knowledge

The agent gets enough autonomy to investigate and improve itself without authority to silently
change its own rules.

Allowed control:
- state inspection
- capability inspection
- read-only research queries
- benchmark execution
- mutation proposals

The kernel blocks:
- policy changes
- permission grants
- audit deletion
- publishing
- replication
- direct candidate commits

A mutation is a proposal, not execution.

Self-knowledge requires four fields:
1. known — evidence-backed capabilities/observations;
2. unknown — unresolved questions;
3. evidence — observations supporting the self-model;
4. next_experiment — an experiment that could falsify/refine it.

The external agent should search for methods that can falsify its own claims, not merely confirm them.

Required report:
sources, claims, self-model changes, candidate mutation, baseline metric, candidate metric,
failed attacks, unresolved uncertainty, and accept/reject decision.
