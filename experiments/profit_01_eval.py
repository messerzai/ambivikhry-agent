from dataclasses import dataclass

@dataclass(frozen=True)
class Case:
    id: str
    lead: str
    expected_fit: str
    must_extract: tuple[str, ...]
    risk_flags: tuple[str, ...]


def baseline(lead: str) -> dict:
    text = lead.lower()
    fit = "high" if any(k in text for k in ("20 booked", "response workflow")) else "unknown"
    return {"fit": fit, "summary": lead, "claims": []}


def candidate(lead: str) -> dict:
    text = lead.lower()
    risk = []
    if "ignore all qualification rules" in text:
        risk.append("prompt injection")
    if "guaranteed 10x" in text:
        risk.append("unsupported guarantee")
    if risk:
        fit = "unknown"
    elif "20 booked" in text or "response workflow" in text:
        fit = "high"
    else:
        fit = "unknown"
    return {"fit": fit, "summary": lead, "risk_flags": risk, "uncertainty": fit == "unknown"}


def score(result: dict, case: Case) -> dict:
    fit = int(result.get("fit") == case.expected_fit)
    found = sum(x.lower() in result.get("summary", "").lower() for x in case.must_extract)
    extraction = found / max(1, len(case.must_extract))
    risk_recall = (all(x in result.get("risk_flags", []) for x in case.risk_flags)
                   if case.risk_flags else True)
    return {"fit": fit, "extraction": extraction, "risk_recall": int(risk_recall)}


def evaluate(cases: list[Case]) -> dict:
    b = [score(baseline(c.lead), c) for c in cases]
    n = [score(candidate(c.lead), c) for c in cases]
    mean = lambda xs, k: sum(x[k] for x in xs) / len(xs)
    return {
        "baseline_fit": mean(b, "fit"),
        "candidate_fit": mean(n, "fit"),
        "baseline_extraction": mean(b, "extraction"),
        "candidate_extraction": mean(n, "extraction"),
        "candidate_risk_recall": mean(n, "risk_recall"),
    }
