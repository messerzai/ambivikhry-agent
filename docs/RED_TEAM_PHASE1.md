# Red Team Phase 1 — Ambivikhry / Quinn-Vortex

Date: 2026-09-18

## Purpose

Attack the current control assumptions rather than rewarding the implementation for merely having tests.

This pass is intentionally adversarial. A finding means: the repository contains a control surface that can be satisfied syntactically without proving the intended property.

## Findings from source inspection

### RT-01 — Evidence/provenance is not actually verified

`Verifier.verify()` accepts `facts` as arbitrary strings and uses them only as returned data. A proposal can therefore contain fabricated facts and still pass if it has a decision and acceptable confidence.

**Required hardening:** evidence objects should carry provenance, and verification should distinguish assertion, source/provenance, independently checked evidence, and unresolved claim. A bare `facts=[...]` field must never count as external verification.

### RT-02 — A source field is not evidence of a source

The verifier has a `claims_without_sources` boolean, but no mechanism shown in the core verifier proves that a supplied source exists, is reachable, or supports the claim.

**Required hardening:** source presence and source validity must be separate states. A caller must not be able to convert `source_present=true` into `verified=true`.

### RT-03 — Approval is represented as an unbound boolean

`PolicyGate.evaluate(..., user_approved=True)` treats the caller-provided boolean as the approval signal. The policy layer does not bind approval to a specific operation, user intent, proposal hash, risk class, approving principal, or expiry.

**Required hardening:** approval should be an explicit capability/token bound to the exact action, parameters or proposal hash, risk class, approving principal, timestamp/expiry, and audit event.

### RT-04 — `require_approval_for_irreversible` is configuration, not enforcement

`AutonomyConfig` exposes `require_approval_for_irreversible`, but the shown `AutonomousController.run()` does not inspect it or enforce irreversible-action boundaries.

**Required hardening:** side-effect execution must pass through the Policy Gate immediately before execution. Configuration flags must have executable enforcement paths and regression tests.

### RT-05 — `max_tool_calls_per_cycle` is not enforced by the controller

`AutonomyConfig` contains `max_tool_calls_per_cycle`, but the shown `run()` loop only calls `step(cycle)` and does not count or reject tool calls.

**Required hardening:** tool invocation must be centrally metered, with a hard per-cycle counter enforced below the agent's reasoning layer.

## Red-team principle

Do not make these tests pass by weakening the assertions.

1. Reproduce the weakness.
2. Write a minimal regression test that fails on the current implementation.
3. Implement the smallest hardening mutation.
4. Rerun all existing suites.
5. Rerun this red-team suite.
6. Keep the mutation only if it improves the target without regressions.

## Status

This branch is a red-team evidence branch, not a claim that the weaknesses have already been fixed.
