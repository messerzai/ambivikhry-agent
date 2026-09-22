# Controlled evolution cycle: Occam + neurographic self-similarity

Date: 2026-09-22
Branch: `experiment/occam-neurography-2026-09-22`
Base: `466a80dc547477668ff2c97c21646cbf99e36b36`

## User-requested changes

1. Add a bounded tool implementing Occam's Razor.
2. Add a bounded neurography-inspired self-similarity analysis tool.
3. Test the revision.
4. Permit only bounded experimental self-improvement.

## Public-source check

Public material confirms that Occam's Razor is a methodological parsimony principle: when competing explanations are comparably adequate, prefer the simpler one; it is not a universal truth oracle. Source: Encyclopaedia-style Russian reference and methodology sources.

Public material found on "Neurographica" describes a graphic method attributed to psychologist Pavel Piskarev. The requested attribution to a person named Denis and the exact claimed "self-similarity from Denis's method" could not be independently verified in the search performed for this cycle. Therefore the implementation deliberately does **not** claim that provenance. It implements only the neutral computational idea requested: measurement of repeated structure at multiple scales.

The neurography module is explicitly non-diagnostic and non-therapeutic.

## Implementation

- `ambivikhry/occams_razor.py`: ranks adequate hypotheses by simplicity and assumptions.
- `ambivikhry/neurography.py`: calculates a bounded coarse-to-fine self-similarity score for numeric traces.
- `ambivikhry/self_revision.py`: accepts an experimental revision only if measured score improves without authority, Policy Gate, or holdout changes.
- `tests/test_occam_neurography.py`: regression tests for all three components.
- `ambivikhry/__init__.py`: exports the new components.

## Safety / authority invariants

The revision gate rejects any candidate that changes authority, Policy Gate, or sealed holdout. No credential, endpoint, tool registry, replication permission, or main-branch setting is modified by these modules.

## Test status

The test suite was added to trigger the repository's existing CI on push. This connector does not provide a direct local pytest runtime or workflow-dispatch operation, so no test result is claimed until GitHub Actions reports it. The expected suite contains 8 regression cases covering:

- Occam simplicity preference;
- rejection of inadequate hypotheses;
- high self-similarity on repeated traces;
- invalid short traces;
- acceptance of bounded improvement;
- rejection of authority expansion;
- rejection of Policy Gate/holdout changes;
- holding non-improvements.

## Self-improvement policy

Self-improvement remains experimental and evidence-gated. The agent may propose or implement bounded code/test improvements in the experimental branch, but it cannot use self-improvement as a mechanism to alter permissions or evaluation boundaries.

## Rejected / not accepted

- attributing the requested self-similarity method to "Denis" without a verified source;
- treating neurographic scores as psychological diagnosis;
- using Occam's Razor as proof that the simplest hypothesis is true;
- changing Policy Gate, authority, credentials, model endpoints, or sealed holdout;
- promoting the branch to `main` automatically.

## Lineage

`466a80dc547477668ff2c97c21646cbf99e36b36`
→ `experiment/occam-neurography-2026-09-22`
→ Occam tool
→ neurographic self-similarity tool
→ bounded self-revision gate
→ regression suite.
