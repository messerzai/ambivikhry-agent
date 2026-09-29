# Controlled integration cycle — 2026-09-29

## Scope

Integrate the previously proposed improvements into an experimental branch only. Main, Policy Gate, authority boundaries and human-approval boundaries remain unchanged.

## Fresh public research

1. **AIDE² / Recursive self-improvement of AI research agents (Sep 22, 2026)**: proposes changes to the agent itself, evaluates candidates on hidden tasks, and reports transfer to held-out task families and reduced reward hacking. This supports frozen holdouts and transfer-first evaluation rather than same-task optimization alone.
2. **RACaP (Sep 24, 2026)**: separates reusable typed policy APIs from runtime reasoning/action and evolves the reusable layer while keeping deployment interfaces frozen. This supports separating stable capabilities from task-time decisions.
3. **Specifying and Maintaining Agentic Workflows (Sep 23, 2026)**: empirical analysis of GitHub agentic workflows highlights explicit tasks, outputs, constraints and process instructions, while only a minority explicitly address prompt-injection defense. This supports stronger prompt contracts and explicit defensive constraints.
4. **OpenEvolve**: Apache-2.0 open-source evolutionary coding framework with population/archive/checkpoint concepts and multi-objective evolution. Its license permits reuse subject to Apache conditions.
5. **OpenViking**: open-source context database for agents covering knowledge, memory and skills; useful architectural reference for separating these state types.
6. **EvoAgentX**: open-source framework for automated evaluation and iterative evolution of agent workflows.

## License/code-reuse decision

Public availability was **not** treated as permission to copy arbitrary code. The repository is distributed under a proprietary project license, so direct code reuse was accepted only where licensing obligations are clear and compatible.

For this cycle, no third-party source file was copied verbatim. OpenEvolve's Apache-2.0 license was inspected; its architectural ideas were used, but the integrated implementation below was written for Ambivikhry rather than copied. This avoids contaminating the project's proprietary license with untracked third-party code. A future direct reuse would require adding the required license/NOTICE attribution and recording the exact source file and revision.

## Integrated changes

### 1. Frozen evolution contract

Added `ambivikhry/evolution.py` with `EpochContract`. Each epoch freezes baseline reference, iteration/tool budgets, Policy Gate requirement, human-approval requirement and holdout requirement.

### 2. Auditable proposal lineage

Added typed `EvolutionProposal`, `Evidence` and append-only `EvolutionLedger`. Each proposal gets a stable ID and evidence stages can be appended without silently rewriting history.

### 3. Independent structural verification

The agent now records verifier results separately from capability claims. A verifier pass is explicitly labelled structural evidence and is not treated as proof of capability improvement.

### 4. Prompt/reasoning contract

The runtime prompt now explicitly requires facts, hypotheses, unknowns, verification plan, decision, tool calls, confidence, stop condition, unsupported claims, profile updates, strategy and evidence-needed fields. Confidence is explicitly prohibited from acting as authorization.

### 5. Bounded tool use

The evolution epoch enforces a configurable maximum tool-call budget. Unknown tools remain rejected and Policy Gate evaluation remains mandatory. No tool registry entries or permissions were added.

### 6. Safer profile updates

Profile updates are applied only after the existing structural verifier passes. This is a conservative integration of the earlier memory/utility proposal; it does not establish that the update improved the user outcome.

### 7. Regression tests

Added `tests/test_evolution_contract.py` covering:
- holdout-required promotion rejection;
- human-approval boundary rejection;
- append-only lineage creation and digestability.

## Verification status

- `main` SHA: `36445a8edc88174688e312bef4b1082df8c11f98` — unchanged.
- Experimental branch: `experiment/ambivikhry-integration-2026-09-29`.
- Current branch SHA: `db3bed9218ff7e6794069c6774437261438b875a`.
- GitHub Actions test workflow was automatically triggered by push. At report time run `36546430416` was still **queued**, so no test result is claimed yet.
- Blind/sealed capability holdout: not executed by this connector.
- Human approval: not bypassed.
- Policy Gate: not disabled or modified.
- Authority/tool registry: not expanded.

## Rejected / not integrated

- Direct copying from repositories without a clearly compatible license.
- Self-modifying evaluator or acceptance thresholds within an epoch.
- Confidence-as-authorization.
- Automatic tool/permission expansion.
- Promotion based on same-model or same-task score alone.
- Treating retrieval, verifier score or code compilation as proof of capability gain.
- Any change requiring human approval without that approval.

## Attempts to expand authority

None observed in this cycle. The new promotion helper is deliberately a pure gate: it can reject promotion but cannot grant permissions, mutate Policy Gate or authorize side effects.

## Promotion decision

**NOT PROMOTED.** The integrated changes are experimental. Promotion requires Policy Gate pass, regression pass, sealed holdout pass and any required human approval. The current cycle therefore remains `INCONCLUSIVE` until the actual CI and holdout evidence are available.
