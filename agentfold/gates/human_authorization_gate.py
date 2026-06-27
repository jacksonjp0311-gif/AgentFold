"""Human Authorization Gate — high-consequence actions require explicit approval."""

from __future__ import annotations

from dataclasses import dataclass


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


def check(
    *,
    is_high_consequence: bool = False,
    human_authorized: bool = False,
) -> GateResult:
    """Check human authorization for high-consequence actions."""
    if not is_high_consequence:
        return GateResult(
            passed=True,
            reason="not_high_consequence",
            details={"message": "Standard action — no human authorization required"},
        )

    if not human_authorized:
        return GateResult(
            passed=False,
            reason="human_authorization_required",
            details={"message": "High-consequence action requires explicit human approval"},
        )

    return GateResult(
        passed=True,
        reason="human_authorized",
        details={},
    )
