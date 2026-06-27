"""Ledger Gate — every artifact must be append-only recorded."""

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


def check(*, has_ledger_entry: bool = False) -> GateResult:
    """Check that a ledger entry has been written."""
    if not has_ledger_entry:
        return GateResult(
            passed=False,
            reason="no_ledger_entry",
            details={"message": "Ledger entry required for inheritance eligibility"},
        )

    return GateResult(passed=True, reason="ledger_entry_present", details={})
