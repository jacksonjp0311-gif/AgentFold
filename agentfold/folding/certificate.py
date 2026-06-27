"""FoldCertificate — records predicted and observed fold state."""

from __future__ import annotations

import hashlib
from enum import Enum

from pydantic import BaseModel, Field


class CertificateStatus(str, Enum):
    DIAGNOSTIC = "diagnostic"
    SHADOW = "shadow"
    VALID_FOR_LOCAL_USE = "valid_for_local_use"
    VALID_FOR_MEMORY_CANDIDATE = "valid_for_memory_candidate"
    VALID_FOR_COMPOUNDING = "valid_for_compounding"
    BLOCKED = "blocked"
    INVALID = "invalid"


class FoldCertificate(BaseModel):
    """FoldCertificate — records gated runtime evidence.

    Does NOT prove truth. Records gated runtime evidence.
    """

    certificate_id: str = ""
    run_id: str = ""
    agent_id: str = ""
    genome_id: str = ""
    origin_certificate_id: str = ""
    transcriptome_id: str = ""
    fold_graph_id: str = ""
    prediction_id: str = ""
    fitness_id: str = ""
    compounding_decision_id: str = ""
    ledger_hash: str = ""
    certificate_status: CertificateStatus = CertificateStatus.DIAGNOSTIC
    claim_boundary: str = "fold_certificate_not_truth_proof"


def create_fold_certificate(
    *,
    run_id: str,
    agent_id: str,
    genome_id: str,
    origin_certificate_id: str,
    transcriptome_id: str = "",
    fold_graph_id: str = "",
    prediction_id: str = "",
    fitness_id: str = "",
    compounding_decision_id: str = "",
    certificate_status: CertificateStatus = CertificateStatus.DIAGNOSTIC,
) -> FoldCertificate:
    """Create a FoldCertificate from run artifacts."""
    canonical = (
        f"{run_id}:{genome_id}:{origin_certificate_id}:"
        f"{transcriptome_id}:{fold_graph_id}:{prediction_id}:{fitness_id}"
    )
    cert_hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]
    cert_id = f"fc_{cert_hash}"

    return FoldCertificate(
        certificate_id=cert_id,
        run_id=run_id,
        agent_id=agent_id,
        genome_id=genome_id,
        origin_certificate_id=origin_certificate_id,
        transcriptome_id=transcriptome_id,
        fold_graph_id=fold_graph_id,
        prediction_id=prediction_id,
        fitness_id=fitness_id,
        compounding_decision_id=compounding_decision_id,
        ledger_hash=cert_hash,
        certificate_status=certificate_status,
    )
