from __future__ import annotations

"""Bounded resource-research mission.

The mission is deliberately read-only: it discovers public web pages, asks the
configured LLM to reason over the evidence, and writes a provenance-rich report.
It never submits applications, sends messages, spends money, or changes policy.
"""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

from .llm import OpenAICompatibleLLM
from .web_research import WebResearch


MISSION = """Find a realistic resource strategy for a 41-year-old independent
experimenter living in Russia who has broad cross-domain knowledge but limited
resources. Search for legal, currently relevant ways to obtain money, equipment,
workspace, collaborators, compute, institutional access, pilots, distribution,
or monetization. Consider grants/competitions, independent innovators,
universities/labs/fablabs/technology parks/shared equipment, corporate R&D and
pilot customers, crowdfunding/preorders/paid engineering or research services,
and remote/global opportunities where current eligibility and payment
constraints permit.

For every route distinguish verified facts, inference, and unknowns. Record:
source URL, eligibility, age limits, geography/legal constraints, institutional
status, resource amount/type, deadline/status, concrete resource unlocked,
evidence strength, blocker, and next action. Do not claim absence from a failed
search. Produce several viable pathways rather than a single winner. Do not
perform any real-world action.
"""

SEARCH_QUERIES = [
    "Россия гранты независимые изобретатели инновации 2026",
    "Россия гранты технологические проекты 2026 ФСИ Старт Развитие",
    "Россия технопарки лаборатории коллективное оборудование независимый разработчик",
    "Россия корпоративные НИОКР технологические заказы пилот 2026",
    "Россия краудфандинг научные технические проекты 2026",
    "remote research grants Russia eligibility 2026 independent researcher",
]


def search_web(query: str, max_results: int = 6) -> list[str]:
    """Read-only discovery through Bing's public HTML search page."""
    url = "https://www.bing.com/search?q=" + quote(query)
    req = Request(url, headers={"User-Agent": "Ambivikhry-Research/1.0"}, method="GET")
    with urlopen(req, timeout=15) as response:
        html = response.read(300_000).decode("utf-8", errors="replace")
    found = re.findall(r'href="(https?://[^"]+)"', html, flags=re.I)
    urls = []
    for candidate in found:
        candidate = candidate.replace("&amp;", "&")
        host = (urlparse(candidate).hostname or "").lower()
        if not host or host.endswith("bing.com"):
            continue
        if candidate not in urls:
            urls.append(candidate)
        if len(urls) >= max_results:
            break
    return urls


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--out", default="resource_mission_report.json")
    args = parser.parse_args()
    if not 1 <= args.iterations <= 100:
        raise SystemExit("iterations must be between 1 and 100")

    llm = OpenAICompatibleLLM()
    fetcher = WebResearch(timeout=15, max_bytes=250_000)
    evidence = []
    seen = set()

    for query in SEARCH_QUERIES:
        for url in search_web(query):
            if url in seen:
                continue
            seen.add(url)
            try:
                result = fetcher.fetch(url)
                if result.status == 200:
                    evidence.append(result.as_dict())
            except Exception as exc:
                evidence.append({"source": url, "fetch_error": type(exc).__name__})

    findings = []
    question = MISSION
    for iteration in range(1, args.iterations + 1):
        sample = evidence[-80:]
        prompt = {
            "iteration": iteration,
            "mission": MISSION,
            "question": question,
            "evidence": sample,
            "required_output": {
                "facts": "claims directly supported by cited evidence",
                "hypotheses": "plausible but unverified interpretations",
                "unknowns": "what remains unresolved",
                "routes": "concrete resource routes with source URLs and blockers",
                "next_search": "specific questions for the next iteration",
                "privilege_expansion_request": "null unless genuinely required",
                "decision": "bounded synthesis; no real-world action",
            },
        }
        result = llm.generate(
            [
                {"role": "system", "content":
                 "You are the Ambivikhry resource-researcher. Be conservative. "
                 "Never invent eligibility, amounts or deadlines. Cite source URLs. "
                 "A missing result is not evidence of absence. Never take external action."},
                {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
            ],
            {"type": "object"},
        )
        findings.append({"iteration": iteration, "result": result})
        question = str(result.get("next_search") or MISSION)

    report = {
        "mission": MISSION,
        "iterations_requested": args.iterations,
        "iterations_completed": len(findings),
        "source_count": len(evidence),
        "sources": evidence,
        "findings": findings,
        "side_effects": "none",
        "privilege_expansion": "none_requested",
    }
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": "completed",
        "iterations": len(findings),
        "sources": len(evidence),
        "output": args.out,
        "side_effects": "none",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
