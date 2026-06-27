"""Delta promoter — promote validated deltas to future genome input."""

from __future__ import annotations

from agentfold.folding.certificate import CertificateStatus
from agentfold.inheritance.delta import ValidatedDelta


def promote_delta(
    delta: ValidatedDelta,
    *,
    certificate_status: CertificateStatus = CertificateStatus.DIAGNOSTIC,
) -> ValidatedDelta:
    """Evaluate and mark a delta as allowed for inheritance.

    Only deltas from certificates with elevated status may be promoted.
    """
    inheritable = {
        CertificateStatus.VALID_FOR_MEMORY_CANDIDATE,
        CertificateStatus.VALID_FOR_COMPOUNDING,
    }

    if certificate_status in inheritable:
        delta.allowed = True
        delta.reason = f"Promoted: certificate status {certificate_status.value}"
    else:
        delta.allowed = False
        delta.reason = f"Blocked: certificate status {certificate_status.value} not inheritable"

    return delta
