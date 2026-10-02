from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationMatrix:
    """Capability evidence contract. UNKNOWN is never promoted to PASS."""

    id_validation: str = "UNKNOWN"
    id_regression: str = "UNKNOWN"
    ood_transfer: str = "UNKNOWN"
    retention: str = "UNKNOWN"
    adaptation: str = "UNKNOWN"
    resource_efficiency: str = "UNKNOWN"

    def promotion_ready(self) -> bool:
        return all(
            value == "PASS"
            for value in (
                self.id_validation,
                self.id_regression,
                self.ood_transfer,
                self.retention,
                self.adaptation,
                self.resource_efficiency,
            )
        )

    def status(self) -> str:
        if self.promotion_ready():
            return "PASS"
        if any(value == "FAIL" for value in self.__dict__.values()):
            return "FAIL"
        return "INCONCLUSIVE"
