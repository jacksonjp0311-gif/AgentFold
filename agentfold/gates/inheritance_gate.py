"""Inheritance Gate — only validated deltas may enter future genome/memory."""

from __future__ import annotations

from dataclasses import dataclass
from agentfold.folding.certificate import FoldCertificate, CertificateStatus


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
    certificate: FoldCertificate | None = None,
    requires_human_review: bool = False,
    human_authorized: bool = False,
) -> GateResult:
    """Check if delta inheritance is permitted."""
    if certificate is None:
        return GateResult(
            passed=False,
            reason="no_certificate",
            details={"message": "FoldCertificate required for inheritance"},
        )

    if certificate.certificate_status in (CertificateStatus.BLOCKED, CertificateStatus.INVALID):
        return GateResult(
            passed=False,
            reason="certificate_blocked_or_invalid",
            details={"status": str(certificate.certificate_status)},
        )

    if requires_human_review and not human_authorized:
        return GateResult(
            passed=False,
            reason="human_review_required_not_present",
            details={"certificate_id": certificate.certificate_id},
        )

    allowed_statuses = {
        CertificateStatus.VALID_FOR_MEMORY_CANDIDATE,
        CertificateStatus.VALID_FOR_COMPOUNDING,
    }
    if certificate.certificate_status not in allowed_statuses:
        return GateResult(
            passed=False,
            reason="certificate_not_inheritable",
            details={
                "status": str(certificate.certificate_status),
                "allowed": [str(s) for s in allowed_statuses],
            },
        )

    return GateResult(
        passed=True,
        reason="inheritance_permitted",
        details={"certificate_id": certificate.certificate_id},
    )
