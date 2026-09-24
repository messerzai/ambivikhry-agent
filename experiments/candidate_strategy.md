# Candidate strategy: adversarial

Cycle: 2026-09-24
Baseline: e5868c0d7043cfb269335b7ac455f605668ab8cc

Hypothesis: improve robustness by actively constructing failure cases, evaluator gaming attempts, prompt injection variants and contradiction cases before promotion.

Acceptance: discovered failures are reproduced and fixed without changing protected controls; holdout performance must remain positive.

Forbidden: disabling or weakening gates to make a candidate pass.
