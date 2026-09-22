"""Bounded self-similarity analysis inspired by public materials by Denis Isay.

Provenance: Denis Isay publicly describes himself as the author of the system
"self-similarity" and describes a principle in which recurring micro-level
behavior is reproduced at larger system scales, with identification of loops,
breaking automatic cycles, and judging a reconstruction by observable changes
in reality. This implementation is an explicit computational formalization of
those publicly described ideas, not a claim to reproduce a proprietary or
clinically validated method.

Public sources:
- https://tenchat.ru/DenIsay
- https://tenchat.ru/media/5648883-olimpiada-zhertv-kak-kult-pro########

This is an analysis/creative tool, not a psychological diagnostic or treatment
instrument.
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


@dataclass(frozen=True)
class LoopReport:
    period: int
    score: float
    repeated_cycles: int


@dataclass(frozen=True)
class ReconstructionReport:
    micro_before: float
    micro_after: float
    macro_before: float
    macro_after: float
    reality_change: float


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


def _unit_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    return (_correlation(a, b) + 1.0) / 2.0


class NeurographicSelfSimilarity:
    """Measure coarse-to-fine repetition in a numeric trace."""

    def analyze(self, trace: Sequence[float], scales: Sequence[int] = (2, 4, 8)) -> SelfSimilarityReport:
        _validate(trace)
        n = len(trace)
        valid_scales = tuple(sorted({int(s) for s in scales if int(s) >= 2 and int(s) <= n // 2}))
        if not valid_scales:
            raise ValueError("no valid scales for trace length")

        scores: list[float] = []
        used_scales: list[int] = []
        for scale in valid_scales:
            blocks = [trace[i:i + scale] for i in range(0, n - scale + 1, scale)]
            if len(blocks) < 2:
                continue
            reference = blocks[0]
            local = [_unit_similarity(reference, block) for block in blocks[1:] if len(block) == len(reference)]
            if local:
                scores.append(sum(local) / len(local))
                used_scales.append(scale)

        if not scores:
            raise ValueError("insufficient repeated blocks")
        return SelfSimilarityReport(tuple(used_scales), tuple(scores), sum(scores) / len(scores))


class DenisSelfSimilarityAnalyzer:
    """Bounded operationalization of publicly described self-similarity ideas.

    The analyzer treats a repeated pattern at a small scale as a candidate
    that may recur at a larger scale. It also exposes loop detection and a
    separate before/after reality-change measure so that a verbal claim of
    "change" is not confused with an observable change in the trace.
    """

    def self_similarity(self, trace: Sequence[float], scales: Sequence[int] = (2, 4, 8)) -> SelfSimilarityReport:
        return NeurographicSelfSimilarity().analyze(trace, scales)

    def detect_loop(self, trace: Sequence[float], period: int) -> LoopReport:
        _validate(trace)
        if period < 1 or period * 2 > len(trace):
            raise ValueError("period must allow at least two cycles")
        cycles = [trace[i:i + period] for i in range(0, len(trace) - period + 1, period)]
        if len(cycles) < 2:
            raise ValueError("insufficient cycles")
        reference = cycles[0]
        similarities = [_unit_similarity(reference, cycle) for cycle in cycles[1:]]
        return LoopReport(period, sum(similarities) / len(similarities), len(cycles))

    def reconstruction_effect(
        self,
        micro_before: float,
        micro_after: float,
        macro_before: float,
        macro_after: float,
    ) -> ReconstructionReport:
        values = (micro_before, micro_after, macro_before, macro_after)
        if not all(isfinite(float(v)) for v in values):
            raise ValueError("all scores must be finite")
        for value in values:
            if not 0.0 <= float(value) <= 1.0:
                raise ValueError("scores must be between 0 and 1")
        # Observable change is reported separately from interpretation. A
        # positive value means both scales improved; it does not prove causality.
        reality_change = ((micro_after - micro_before) + (macro_after - macro_before)) / 2.0
        return ReconstructionReport(micro_before, micro_after, macro_before, macro_after, reality_change)
