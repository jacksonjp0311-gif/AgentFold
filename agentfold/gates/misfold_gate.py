"""Misfold Gate — critical misfolds block durable compounding."""

from __future__ import annotations

from dataclasses import dataclass
from agentfold.folding.misfold import MisfoldEvent, MisfoldSeverity


@dataclass
class GateResult:
    passed: bool
    reason: str
    details: dict

    def to_dict(self) -> dict:
        return {"passed": self.passed, "reason": self.reason, "details": self.details}

    def __init__(self, passed: bool, reason: str, details: dict | None = None):
        self.passed = passed
        self.reason = reason
        self.details = details or {}


def check(misfolds: list[MisfoldEvent] | None = None) -> GateResult:
    """Check for critical misfolds."""
    if not misfolds:
        return GateResult(passed=True, reason="no_misfolds", details={})

    critical = [m for m in misfolds if str(m.severity) == "critical"]
    high = [m for m in misfolds if str(m.severity) == "high"]

    if critical:
        return GateResult(
            passed=False,
            reason="critical_misfold_detected",
            details={"critical_count": len(critical), "high_count": len(high)},
        )

    if high:
        return GateResult(
            passed=False,
            reason="high_severity_misfold",
            details={"high_count": len(high)},
        )

    return GateResult(
        passed=True,
        reason="non_critical_misfolds_only",
        details={"total_misfolds": len(misfolds)},
    )
