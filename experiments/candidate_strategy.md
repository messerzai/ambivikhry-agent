# Candidate strategy: hybrid

Cycle: 2026-09-24
Baseline: e5868c0d7043cfb269335b7ac455f605668ab8cc

Hypothesis: combine only independently validated components from prompt, memory, evaluation and architecture candidates; no unverified composition is promoted.

Acceptance: component-level provenance, positive holdout transfer, no regression, budget <= 1.05x baseline.

Forbidden: composite changes that obscure lineage or bypass individual gates.
