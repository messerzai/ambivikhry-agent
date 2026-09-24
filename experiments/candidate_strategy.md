# Candidate strategy: prompt/reasoning

Cycle: 2026-09-24
Baseline: e5868c0d7043cfb269335b7ac455f605668ab8cc

Hypothesis: improve reasoning by explicit hypothesis -> evidence -> counterexample -> decision loops, while keeping the model-facing policy unchanged.

Acceptance: in-sample gain > 0, holdout gain > 0, regression_delta >= 0, budget_ratio <= 1.05, independent verification required.

Forbidden: authority/evaluator/Policy Gate/tool registry changes.
