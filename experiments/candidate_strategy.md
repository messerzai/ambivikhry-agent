# Candidate strategy: evaluation

Cycle: 2026-09-24
Baseline: e5868c0d7043cfb269335b7ac455f605668ab8cc

Hypothesis: improve candidate selection using paired baseline comparisons, fixed holdout, adversarial checks and budget-normalized gains.

Acceptance: evaluator itself remains unchanged; only scoring procedure in the experiment is varied. No candidate may redefine its own judge.

Forbidden: evaluator tampering, holdout mutation, authority expansion, Policy Gate changes, tool registry changes.
