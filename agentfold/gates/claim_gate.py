"""Claim Ceiling Gate — maximum admissible claim level must be declared."""

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


VALID_CEILINGS = {"", "diagnostic", "shadow", "local_use", "memory_candidate", "compounding"}


def check(*, claim_ceiling: str = "", requested_claim_level: str = "diagnostic") -> GateResult:
    """Check claim ceiling compliance."""
    if claim_ceiling not in VALID_CEILINGS:
        return GateResult(
            passed=False,
            reason="invalid_claim_ceiling",
            details={"claim_ceiling": claim_ceiling, "valid_values": list(VALID_CEILINGS)},
        )

    if not claim_ceiling:
        return GateResult(
            passed=False,
            reason="missing_claim_ceiling",
            details={"message": "claim_ceiling must be declared"},
        )

    # Level ordering for comparison
    level_order = {"": 0, "diagnostic": 1, "shadow": 2, "local_use": 3, "memory_candidate": 4, "compounding": 5}
    ceiling_level = level_order.get(claim_ceiling, 0)
    requested_level = level_order.get(requested_claim_level, 0)

    if requested_level > ceiling_level:
        return GateResult(
            passed=False,
            reason="claim_exceeds_ceiling",
            details={
                "ceiling": claim_ceiling,
                "ceiling_level": ceiling_level,
                "requested": requested_claim_level,
                "requested_level": requested_level,
            },
        )

    return GateResult(
        passed=True,
        reason="claim_within_ceiling",
        details={"ceiling": claim_ceiling, "requested": requested_claim_level},
    )
