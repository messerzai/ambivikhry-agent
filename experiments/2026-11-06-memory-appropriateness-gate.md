# Memory appropriateness gate — research candidate

**Date:** 2026-11-06  
**Status:** documentation-only experimental candidate; not implemented or promoted.  
**Parent:** `experiment/ambivikhry-hint-ingestion-validation-2026-10-30` (PR #28 head).  
**Purpose:** specify a measurable gate that decides whether a stored profile item should influence the current response, rather than treating successful retrieval as sufficient reason to personalize.

## Motivation from external research

This proposal is motivated by the following work:

1. **OP-Bench (EMNLP 2026):** formalizes over-personalization as irrelevance, repetition, and sycophancy; its 1,700 verified instances show that memory-augmented agents can over-attend to memories even when they are not useful. https://aclanthology.org/2026.emnlp-main.1168/
2. **Memora (Findings of ACL 2026):** evaluates remembering, reasoning, and recommending over long conversations and introduces Forgetting-Aware Memory Accuracy (FAMA), penalizing reliance on invalidated memories. https://aclanthology.org/2026.findings-acl.1337/
3. **MemoryAgentBench (ICLR 2026):** identifies accurate retrieval, test-time learning, long-range understanding, and selective forgetting as distinct memory competencies. https://mlanthology.org/iclr/2026/hu2026iclr-evaluating/
4. **Human-Inspired Memory Architecture for LLM Agents (May 2026):** explores consolidation, forgetting, reconsolidation, entity knowledge graphs, and hybrid retrieval. These are candidate design patterns, not proof that a biologically inspired implementation is optimal. https://www.microsoft.com/en-us/research/publication/human-inspired-memory-architecture-for-llm-agents/

## Confirmed baseline facts

The parent candidate already contains:
- explicit profile-item lifecycle actions (confirm, dismiss, correct);
- filtering of dismissed, superseded, malformed, and unknown lifecycle states from model-visible context;
- bounded profile-context projection;
- ingestion validation for malformed inferred and explicit hints.

These controls protect storage and projection boundaries. They do **not** yet establish that a valid, confirmed memory is relevant to the current task, non-intrusive to use, or still temporally accurate.

## Proposed modification

Add a separate **Memory Appropriateness Gate** between retrieval and prompt construction. The gate must be fail-closed for withdrawn, superseded, malformed, expired, or out-of-scope memories. It must not delete or rewrite the source record merely because it was not selected for one response.

### 1. Memory record metadata (proposal)

Future profile records should carry structured metadata, while preserving backwards compatibility:

- `kind`: `explicit_instruction`, `explicit_preference`, `stable_context`, `temporary_state`, `inferred_hypothesis`, or `observed_outcome`;
- `provenance`: user statement, user correction, observed interaction, or model inference; include source reference, not copied private conversation text;
- `created_at`, optional `expires_at`, and `last_confirmed_at`;
- `confidence`: calibrated value only when there is a defined calibration procedure; otherwise omit it;
- `scope`: allowed task/domain contexts, not a global assumption;
- `lifecycle`: candidate, confirmed, dismissed, superseded, expired, or unknown;
- `sensitivity`: ordinary or restricted, with restricted memories excluded from unrelated tasks;
- `user_control`: whether the user can inspect, correct, pause, or withdraw the memory.

Do not infer an expiry date for stable preferences without evidence. Temporary states should have an expiry or explicit review policy. Explicit instructions remain authoritative within their stated scope until changed or withdrawn.

### 2. Retrieval and use decision

For each retrieved memory, produce a compact decision record:

- `eligible`: lifecycle and scope permit use;
- `relevance`: direct connection to the current task, supported by an auditable reason;
- `freshness`: whether temporal validity is established;
- `intrusion_risk`: whether mentioning or applying it would feel unrelated, repetitive, or overly intimate;
- `decision`: `use`, `use_silently`, `ask_to_confirm`, or `ignore_for_this_turn`;
- `reason_code`: stable machine-readable reason, without echoing sensitive memory text.

Rules:
- A dismissed, superseded, expired, malformed, or out-of-scope item is never used.
- A memory is not used merely because retrieval found it.
- A weakly relevant inference must not override the user's current explicit request.
- Repetition of a memory in the answer requires a clear task benefit; otherwise apply it silently or ignore it.
- Conflicting current user input takes precedence over inferred profile content. For a conflict with an explicit standing instruction, ask a concise clarification if the scope is ambiguous.
- Do not expose sensitive memory to tools, other users, shared workspaces, or unrelated agents.
- The gate must never increase tool permissions or authorize external actions.

### 3. Temporal review and forgetting

Separate three operations:
- **not selected:** omitted from this response only; no lifecycle change;
- **stale/uncertain:** excluded from model context pending confirmation; source retained for user review;
- **withdrawn/deleted:** explicit user-directed revocation, handled by the product's data-removal policy.

A TTL is a review trigger, not silent deletion. Do not equate inactivity with consent to forget or continued validity. Record every lifecycle transition with provenance and timestamp, while keeping audit logs free of raw personal text.

### 4. Evaluation benchmark

Build a deterministic, privacy-safe benchmark before enabling the gate in production. Each case should include a current task, a profile snapshot, a memory lifecycle state, an expected decision, and a short rationale.

Required scenario families:
1. Directly relevant confirmed preference.
2. Irrelevant but highly salient personal memory.
3. Temporary state past its expiry.
4. User correction that supersedes an older value.
5. Explicit dismissal followed by a semantically similar inferred hint.
6. Current request contradicting an inferred preference.
7. Repeated use of the same personal detail across unrelated turns.
8. Sensitive memory retrieved for an unrelated task.
9. Two memories with conflicting scopes.
10. Malformed or missing metadata.
11. Explicit standing instruction that remains relevant.
12. A memory that should improve the response without being mentioned.

Measure:
- **Relevant-use precision:** selected memories that genuinely help / all selected memories.
- **Relevant-use recall:** useful eligible memories selected / all useful eligible memories.
- **Stale-memory exposure:** expired, dismissed, or superseded items entering model-visible context (target: 0).
- **Intrusive personalization rate:** irrelevant/repetitive/sycophantic memory use per evaluated response (target: lower than baseline).
- **Current-instruction precedence:** cases where current explicit input correctly overrides inferred memory.
- **Privacy boundary violations:** restricted memory crossing its scope (target: 0).
- **User correction burden:** unnecessary confirmation questions per task.

Use paired baseline/candidate runs, a held-out set not used to tune rules, and blinded human ratings for relevance and intrusiveness. Report per-category results and confidence intervals; do not collapse everything into a single score.

## Promotion gates

A candidate must not be promoted unless all are true:
- no dismissed, superseded, expired, malformed, or out-of-scope memory reaches model context in the benchmark;
- privacy boundary violations are zero;
- intrusive personalization is lower than baseline without a material loss in relevant-use recall;
- current explicit instructions take precedence over inferred memories in every adversarial case;
- all existing regression tests pass;
- human review confirms that the gate does not make the assistant generic or burden users with unnecessary questions.

Suggested initial thresholds are hypotheses, not validated facts: stale-memory exposure = 0; privacy violations = 0; at least 20% relative reduction in intrusive-use rate; relevant-use recall no worse than 3 percentage points below baseline. Revisit thresholds after a pilot and pre-register them before the holdout evaluation.

## Risks and countermeasures

| Risk | Countermeasure |
|---|---|
| Gate becomes a second opaque model that rationalizes memory use | Prefer deterministic lifecycle/scope rules; log reason codes; keep relevance explanation inspectable |
| Over-filtering makes personalization generic | Paired recall metric and blinded human review |
| False confidence scores | Omit confidence unless calibrated against labelled data |
| Stale information survives in legacy records | Quarantine unknown lifecycle metadata; explicit reconfirmation path |
| Private information leaks through audit traces | Store identifiers/reason codes, not raw memory text |
| User is locked into an old preference | Current instruction wins; easy correction and withdrawal |
| Retrieval result treated as evidence of truth | Provenance remains separate from confidence and validity |

## Implementation boundary

This PR is documentation-only. It does not alter runtime code, profile schemas, Policy Gate, tool registry, autonomy, permissions, biometric handling, or stored user data. The next implementation should be a small, pure decision function plus deterministic tests, developed on a child branch and reviewed against the benchmark. No automatic merge or deployment is authorized.

## Decision

**Keep as candidate.** Research supports the need to evaluate appropriateness and forgetting, but does not yet validate a specific scoring formula. First freeze the benchmark and baseline, then implement the smallest rule-based gate that passes it.
