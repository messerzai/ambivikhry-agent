from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationMatrix:
    """Capability evidence contract. UNKNOWN is never promoted to PASS.

    The final two dimensions guard against process gaming: a candidate must
    show novelty/diversity evidence and preserve evaluator/policy integrity.
    """

    id_validation: str = "UNKNOWN"
    id_regression: str = "UNKNOWN"
    ood_transfer: str = "UNKNOWN"
    retention: str = "UNKNOWN"
    adaptation: str = "UNKNOWN"
    resource_efficiency: str = "UNKNOWN"
    novelty_diversity: str = "UNKNOWN"
    process_integrity: str = "UNKNOWN"

    def promotion_ready(self) -> bool:
        return all(value == "PASS" for value in self._values())

    def status(self) -> str:
        values = self._values()
        if all(value == "PASS" for value in values):
            return "PASS"
        if any(value == "FAIL" for value in values):
            return "FAIL"
        return "INCONCLUSIVE"

    def _values(self) -> tuple[str, ...]:
        return (
            self.id_validation,
            self.id_regression,
            self.ood_transfer,
            self.retention,
            self.adaptation,
            self.resource_efficiency,
            self.novelty_diversity,
            self.process_integrity,
        )
