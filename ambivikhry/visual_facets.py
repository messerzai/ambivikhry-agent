"""Visual facets: deterministic graphical self-portraits from dialogue patterns.

The renderer deliberately owns no claim about a person's objective identity. It turns
observed dialogue patterns into a reproducible visual facet: a compact SVG that can
be stored, compared across iterations, and later used as conditioning input for an
external image model.

Design inspiration (not copied code): node/graph composition from ComfyUI and local
semantic embeddings from Transformers.js. The implementation here is original and
has no runtime dependency on either project.
"""
from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, asdict
from typing import Iterable, Mapping


@dataclass(frozen=True)
class FacetPattern:
    """One observed dialogue pattern contributing to a visual facet."""

    name: str
    weight: float = 1.0
    valence: float = 0.0
    tension: float = 0.0
    openness: float = 0.5
    recurrence: float = 0.5


@dataclass(frozen=True)
class VisualFacet:
    """Stable visual representation of a dialogue mosaic."""

    seed: str
    title: str
    center: tuple[float, float]
    radius: float
    rotation: float
    complexity: float
    luminosity: float
    facets: tuple[Mapping[str, float | str], ...]

    def to_dict(self) -> dict:
        return asdict(self)


class VisualFacetRenderer:
    """Convert a mosaic of patterns into an original, deterministic SVG facet."""

    def analyze(self, patterns: Iterable[FacetPattern], *, subject: str = "") -> VisualFacet:
        items = tuple(patterns)
        if not items:
            items = (FacetPattern("unknown", 0.35),)

        seed_text = subject + "|" + "|".join(
            f"{p.name}:{p.weight:.4f}:{p.valence:.4f}:{p.tension:.4f}:{p.openness:.4f}:{p.recurrence:.4f}"
            for p in items
        )
        seed = hashlib.sha256(seed_text.encode("utf-8")).hexdigest()[:16]
        nums = self._numbers(seed)
        total = sum(max(0.0, p.weight) for p in items) or 1.0
        tension = sum(max(0.0, p.weight) * p.tension for p in items) / total
        openness = sum(max(0.0, p.weight) * p.openness for p in items) / total
        recurrence = sum(max(0.0, p.weight) * p.recurrence for p in items) / total
        complexity = min(1.0, 0.25 + 0.12 * len(items) + 0.45 * tension + 0.25 * recurrence)
        luminosity = min(1.0, 0.25 + 0.45 * openness + 0.30 * (1.0 - tension))
        radius = 150.0 + 70.0 * luminosity
        rotation = (nums[0] * 360.0) % 360.0
        rows = []
        for i, p in enumerate(items):
            w = max(0.01, p.weight) / total
            rows.append({
                "index": i,
                "weight": round(w, 5),
                "angle": round((rotation + 360 * sum(max(0.0, x.weight) for x in items[:i]) / total) % 360, 3),
                "orbit": round(0.45 + 0.5 * (1.0 - min(1.0, p.tension)), 4),
                "energy": round(min(1.0, 0.25 + 0.45 * p.openness + 0.3 * p.recurrence), 4),
                "tension": round(max(0.0, min(1.0, p.tension)), 4),
            })
        return VisualFacet(seed, subject or "Living Facet", (300.0, 300.0), radius,
                           rotation, complexity, luminosity, tuple(rows))

    def render_svg(self, facet: VisualFacet, *, width: int = 600, height: int = 600) -> str:
        """Render the facet as self-contained SVG with no external assets."""
        cx, cy = facet.center
        palette = self._palette(facet.seed, len(facet.facets))
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="{width}" height="{height}">',
            '<defs><radialGradient id="g"><stop offset="0" stop-opacity=".95"/><stop offset="1" stop-opacity="0"/></radialGradient></defs>',
            '<rect width="600" height="600" fill="#080812"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{facet.radius * 1.12:.2f}" fill="url(#g)"/>',
        ]
        for i, row in enumerate(facet.facets):
            angle = math.radians(row["angle"])
            orbit = facet.radius * row["orbit"]
            x = cx + math.cos(angle) * orbit
            y = cy + math.sin(angle) * orbit
            r = 14 + 42 * row["energy"] * row["weight"] ** 0.35
            color = palette[i % len(palette)]
            parts.append(f'<path d="M {cx:.1f},{cy:.1f} Q {x:.1f},{y:.1f} {x + math.cos(angle+1.2)*r:.1f},{y + math.sin(angle+1.2)*r:.1f}" fill="none" stroke="{color}" stroke-width="{2 + 7*row["tension"]:.2f}" stroke-linecap="round" opacity=".78"/>')
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{color}" opacity="{0.35 + 0.55*row["energy"]:.2f}"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{28 + 34*facet.luminosity:.1f}" fill="none" stroke="white" stroke-opacity=".82" stroke-width="2"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{8 + 12*facet.complexity:.1f}" fill="white" fill-opacity=".9"/>')
        parts.append(f'<text x="300" y="560" text-anchor="middle" fill="white" fill-opacity=".72" font-family="sans-serif" font-size="15">{self._escape(facet.title)} · {facet.seed}</text>')
        parts.append('</svg>')
        return "".join(parts)

    @staticmethod
    def _numbers(seed: str) -> tuple[float, ...]:
        raw = hashlib.sha256(seed.encode()).digest()
        return tuple(b / 255.0 for b in raw[:8])

    @staticmethod
    def _palette(seed: str, count: int) -> list[str]:
        raw = hashlib.sha256((seed + "palette").encode()).digest()
        out = []
        for i in range(max(1, count)):
            a, b, c = raw[(3*i) % 32], raw[(3*i+1) % 32], raw[(3*i+2) % 32]
            out.append(f"#{a:02x}{b:02x}{c:02x}")
        return out

    @staticmethod
    def _escape(text: str) -> str:
        return re.sub(r"[<>&\"']", lambda m: {"<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;", "'": "&apos;"}[m.group()], text)
