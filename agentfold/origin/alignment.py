"""Origin alignment check — verify session geometry against origin."""

from __future__ import annotations

from dataclasses import dataclass
from agentfold.genome.schema import AgentGenome
from agentfold.origin.certificate import OriginCertificate


@dataclass
class AlignmentResult:
    aligned: bool
    reason: str
    details: dict

    def to_dict(self) -> dict:
        return {
            "aligned": self.aligned,
            "reason": self.reason,
            "details": self.details,
        }


def check_alignment(
    genome: AgentGenome,
    certificate: OriginCertificate,
) -> AlignmentResult:
    """Verify session aligns to declared origin."""
    if not certificate.passed:
        return AlignmentResult(
            aligned=False,
            reason="origin_certificate_failed",
            details={"reasons": certificate.reasons},
        )

    if certificate.genome_id != genome.genome_id:
        return AlignmentResult(
            aligned=False,
            reason="genome_id_mismatch",
            details={
                "certificate_genome_id": certificate.genome_id,
                "genome_id": genome.genome_id,
            },
        )

    return AlignmentResult(
        aligned=True,
        reason="origin_aligned",
        details={"certificate_id": certificate.certificate_id},
    )
