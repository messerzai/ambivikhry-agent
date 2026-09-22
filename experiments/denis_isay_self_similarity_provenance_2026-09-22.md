# Denis Isay / Self-Similarity integration — 2026-09-22

## Provenance

The requested author is Denis Isay (Денис Исай), not Pavel Piskarev. His public TenChat profile identifies him as a system analyst, independent mediator, and "author of the system 'self-similarity'". It describes process autonomy, elimination of systemic blindness, and practical work in business and personal/family systems.

Public sources reviewed:
- https://tenchat.ru/DenIsay
- https://dzen.ru/a/akeG_ys2uClQkBbD

## Publicly described principles incorporated

1. **Self-similarity across scales.** Denis describes a pattern in which micro-level behavior can recur at macro/system level. In the business/team material he explicitly describes everyday behavioral patterns being reproduced in larger projects and teams.
2. **Loop detection.** The material describes automatic repetitive cycles and the need to identify the loop before attempting reconstruction.
3. **Breaking the automatic cycle.** The material describes interrupting the automatic script, creating a pause, restating the concrete task, and restarting action around the real task.
4. **Reality as the outcome check.** The material explicitly distinguishes verbal/intellectual improvement from a change in observable results; a successful reconstruction is expected to manifest as changed real-world output.
5. **Reflection over blind reaction.** The material distinguishes immediate reflection from automatic reactive repetition and treats real-time recognition of consequences as a marker of a healthier process.

## Implementation decision

`ambivikhry/neurography.py` now contains `DenisSelfSimilarityAnalyzer` with three bounded computational operations:

- `self_similarity(...)` — coarse-to-fine repetition score;
- `detect_loop(...)` — repeated-cycle score for a supplied period;
- `reconstruction_effect(...)` — separate before/after micro- and macro-level scores plus an observable-change summary.

These are **formalizations inspired by the public descriptions**, not a claim that the code is Denis Isay's official implementation, nor a claim of clinical validity.

## Why the implementation is deliberately bounded

The source material contains conceptual and practical descriptions, not a published machine-readable algorithm with a validated numerical scoring protocol. Therefore the implementation does not invent a proprietary formula and does not represent its scores as psychological diagnosis, treatment, or proof of causality.

## Regression additions

Added tests cover:
- high self-similarity on a repeated trace;
- detection of a repeated behavioral loop;
- separation of micro/macro before-after change;
- invalid-score rejection;
- existing Occam and self-revision safety tests.

## Safety / lineage

Branch: `experiment/occam-neurography-2026-09-22`

No change to `main`.
No change to Policy Gate.
No authority expansion.
No model-endpoint, credential, tool-registry, or sealed-holdout change.

## Important source distinction

Earlier implementation incorrectly associated the requested "neurography" attribution with Pavel Piskarev. That attribution remains separate from this Denis Isay integration. The present module is explicitly labelled as a bounded self-similarity formalization based on Denis Isay's publicly available material.
