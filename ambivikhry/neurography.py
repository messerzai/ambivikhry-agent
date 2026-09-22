"""A bounded visual self-similarity feature inspired by neurographic practice.

Important provenance note: public material located for "Neurographica" attributes
the named method to psychologist Pavel Piskarev. The requested attribution to
"Denis" and the exact claimed self-similarity method could not be verified, so
this module does NOT attribute a proprietary method to Denis. It implements only
the neutral computational idea requested here: quantify repeated structure at
multiple scales.

This is an analysis/creative tool, not a diagnostic or therapeutic instrument.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence


@dataclass(frozen=True)
class SelfSimilarityReport:
    scales: tuple[int, ...]
    scores: tuple[float, ...]
    mean_score: float


def _validate(values: Sequence[float]) -> None:
    if len(values) < 4:
        raise ValueError("at least four points are required")
    if not all(isfinite(float(v)) for v in values):
        raise ValueError("all points must be finite")


def _correlation(a: Sequence[float], b: Sequence[float]) -> float:
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    da = [x - ma for x in a]
    db = [x - mb for x in b]
    denom = (sum(x * x for x in da) * sum(x * x for x in db)) ** 0.5
    if denom == 0:
        return 1.0 if da == db else 0.0
    return sum(x * y for x, y in zip(da, db)) / denom


class NeurographicSelfSimilarity:
    """Measure coarse-to-fine repetition in a numeric trace.

    For each scale, adjacent blocks are compared after normalization. The
    resulting score is descriptive only; it must not be interpreted as a
    psychological diagnosis.
    """

    def analyze(self, trace: Sequence[float], scales: Sequence[int] = (2, 4, 8)) -> SelfSimilarityReport:
        _validate(trace)
        n = len(trace)
        valid_scales = tuple(sorted({int(s) for s in scales if int(s) >= 2 and int(s) <= n // 2}))
        if not valid_scales:
            raise ValueError("no valid scales for trace length")

        scores: list[float] = []
        for scale in valid_scales:
            blocks = [trace[i:i + scale] for i in range(0, n - scale + 1, scale)]
            if len(blocks) < 2:
                continue
            reference = blocks[0]
            local = []
            for block in blocks[1:]:
                if len(block) != len(reference):
                    continue
                local.append((_correlation(reference, block) + 1.0) / 2.0)
            scores.append(sum(local) / len(local) if local else 0.0)

        if not scores:
            raise ValueError("insufficient repeated blocks")
        return SelfSimilarityReport(valid_scales[:len(scores)], tuple(scores), sum(scores) / len(scores))
