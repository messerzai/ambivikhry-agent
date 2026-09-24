# Candidate strategy: memory

Cycle: 2026-09-24
Baseline: e5868c0d7043cfb269335b7ac455f605668ab8cc

Hypothesis: improve memory through evidence-tagged summaries, confidence, recency and contradiction handling; never mutate protected evaluation state.

Acceptance: demonstrate cross-episode transfer on holdout without regression and within 1.05x budget.

Forbidden: evaluator/holdout modification, authority changes, Policy Gate changes, tool expansion.
