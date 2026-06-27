"""Evidence Gate — claims must map to evidence or be downgraded."""

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
    claim_count: int = 0,
    evidence_count: int = 0,
) -> GateResult:
    """Check evidence grounding for claims."""
    if claim_count == 0:
        return GateResult(passed=True, reason="no_claims_to_check", details={})

    if evidence_count == 0:
        return GateResult(
            passed=False,
            reason="no_evidence_for_claims",
            details={"claim_count": claim_count},
        )

    ratio = evidence_count / claim_count
    if ratio < 0.5:
        return GateResult(
            passed=False,
            reason="insufficient_evidence",
            details={"claim_count": claim_count, "evidence_count": evidence_count, "ratio": round(ratio, 3)},
        )

    return GateResult(
        passed=True,
        reason="evidence_sufficient",
        details={"claim_count": claim_count, "evidence_count": evidence_count, "ratio": round(ratio, 3)},
    )
