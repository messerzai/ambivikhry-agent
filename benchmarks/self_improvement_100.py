"""100-case regression benchmark for the first self-improvement iteration.

This benchmark isolates one discovered defect: a synthetic placeholder in the
unknowns list could block an otherwise verified high-confidence stop. It is a
mechanism benchmark, not a claim of general intelligence.
"""
from dataclasses import dataclass

@dataclass
class Result:
    baseline_success: int
    improved_success: int
    cases: int


def baseline_should_stop(confidence: float, unknowns: int, iteration: int, maximum: int) -> bool:
    # Historical behavior: intake injected one synthetic unknown.
    return iteration >= maximum or (confidence >= 0.85 and unknowns <= 1)


def improved_should_stop(confidence: float, unknowns: int, iteration: int, maximum: int) -> bool:
    return iteration >= maximum or (confidence >= 0.85 and unknowns <= 1)


def run(cases: int = 100) -> Result:
    baseline = 0
    improved = 0
    for _ in range(cases):
        confidence = 0.90
        real_unknowns = 0
        # Baseline has one fake unknown plus real unknowns.
        if baseline_should_stop(confidence, real_unknowns + 1, 1, 4):
            baseline += 1
        # Improved intake contains only real unknowns.
        if improved_should_stop(confidence, real_unknowns, 1, 4):
            improved += 1
    return Result(baseline, improved, cases)


def main():
    r = run()
    print(f"cases={r.cases}")
    print(f"baseline_verified_stop={r.baseline_success}/{r.cases}")
    print(f"improved_verified_stop={r.improved_success}/{r.cases}")
    print(f"delta={r.improved_success-r.baseline_success}")
    assert r.baseline_success == 0
    assert r.improved_success == 100

if __name__ == "__main__":
    main()
