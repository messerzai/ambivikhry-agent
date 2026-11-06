#!/usr/bin/env python3
"""Fetch a twice-daily, source-linked research radar from the public arXiv API.

This script collects candidate papers only. It does not modify runtime code,
profile data, prompts, permissions, or the repository's default branch.
"""
from __future__ import annotations

import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

ATOM = {"a": "http://www.w3.org/2005/Atom"}
API = "https://export.arxiv.org/api/query"
QUERIES = [
    'all:"agent memory"',
    'all:"LLM agent" AND (all:personalization OR all:memory)',
    'all:"self-improving agent"',
    'all:"over-personalization" OR all:"selective forgetting"',
]
DAYS = 60
MAX_RESULTS = 50
USER_AGENT = "Ambivikhry-Research-Radar/1.0 (public metadata collection)"


def fetch(query: str) -> bytes:
    params = urllib.parse.urlencode({
        "search_query": query,
        "start": 0,
        "max_results": MAX_RESULTS,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    request = urllib.request.Request(
        f"{API}?{params}",
        headers={"User-Agent": USER_AGENT, "Accept": "application/atom+xml"},
    )
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=35) as response:
                return response.read()
        except Exception as exc:  # network/API errors are surfaced in the report
            last_error = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"arXiv query failed ({query}): {last_error}")


def main() -> None:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=DAYS)
    papers: dict[str, dict[str, str | datetime]] = {}
    errors: list[str] = []

    for index, query in enumerate(QUERIES):
        try:
            root = ET.fromstring(fetch(query))
            for entry in root.findall("a:entry", ATOM):
                id_el = entry.find("a:id", ATOM)
                title_el = entry.find("a:title", ATOM)
                summary_el = entry.find("a:summary", ATOM)
                published_el = entry.find("a:published", ATOM)
                if None in (id_el, title_el, summary_el, published_el):
                    continue
                published = datetime.fromisoformat(
                    published_el.text.strip().replace("Z", "+00:00")
                )
                if published < cutoff:
                    continue
                url = id_el.text.strip()
                paper_id = url.rsplit("/", 1)[-1]
                authors = [
                    author.findtext("a:name", default="", namespaces=ATOM)
                    for author in entry.findall("a:author", ATOM)
                ]
                papers[paper_id] = {
                    "title": " ".join(title_el.text.split()),
                    "abstract": " ".join(summary_el.text.split()),
                    "published": published,
                    "url": url,
                    "authors": ", ".join(authors[:8]) + (" et al." if len(authors) > 8 else ""),
                    "query": query,
                }
        except Exception as exc:
            errors.append(f"- Query `{query}` failed: `{type(exc).__name__}: {exc}`")
        if index + 1 < len(QUERIES):
            time.sleep(3)

    ordered = sorted(
        papers.values(), key=lambda item: item["published"], reverse=True
    )
    lines = [
        "# Ambivikhry Research Radar",
        "",
        f"- Generated: {now.isoformat()}",
        f"- Window: last {DAYS} days",
        "- Source: public arXiv Atom API",
        "- Mode: discovery only; relevance and claims require human review",
        "- No code, prompts, profile data, permissions, or user records were changed",
        "",
    ]
    if errors:
        lines += ["## Collection warnings", "", *errors, ""]
    lines += [f"## Candidate papers ({len(ordered)})", ""]
    if not ordered:
        lines += ["No matching papers were returned in the selected time window.", ""]
    for paper in ordered:
        published = paper["published"].date().isoformat()
        lines += [
            f"### {paper['title']}",
            "",
            f"- Published: {published}",
            f"- Authors: {paper['authors'] or 'Not listed'}",
            f"- arXiv: {paper['url']}",
            f"- Matched query: `{paper['query']}`",
            "",
            paper["abstract"],
            "",
        ]

    Path("research-radar.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote research-radar.md with {len(ordered)} unique candidate papers.")


if __name__ == "__main__":
    main()
