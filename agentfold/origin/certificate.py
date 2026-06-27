"""OriginCertificate — proof of origin alignment."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from agentfold.genome.hashing import hash_genome
from agentfold.genome.schema import AgentGenome


class OriginCertificate(BaseModel):
    """Records that a session has aligned to a declared origin."""

    certificate_id: str
    genome_id: str
    agent_id: str
    origin_ref: str
    origin_hash: str = ""
    genome_hash: str
    session_id: str = ""
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    passed: bool = True
    reasons: list[str] = Field(default_factory=list)
    claim_boundary: str = "origin_alignment_declared"


def certify_origin(
    genome: AgentGenome,
    *,
    session_id: str = "",
    prior_origin_hash: str | None = None,
) -> OriginCertificate:
    """Check origin alignment and emit an OriginCertificate.

    Origin alignment passes when:
    - genome has an origin_ref
    - genome hash is computable
    - if prior_origin_hash provided, it matches current origin state
    """
    genome_hash = hash_genome(genome)
    reasons: list[str] = []
    passed = True

    if not genome.origin_ref:
        passed = False
        reasons.append("genome.origin_ref is empty")

    if prior_origin_hash is not None and prior_origin_hash != genome_hash:
        passed = False
        reasons.append("prior_origin_hash mismatch — genome has drifted")

    certificate_id = hashlib.sha256(
        f"{genome.genome_id}:{genome_hash}:{session_id}".encode()
    ).hexdigest()[:16]

    return OriginCertificate(
        certificate_id=certificate_id,
        genome_id=genome.genome_id,
        agent_id=genome.agent_id,
        origin_ref=genome.origin_ref,
        origin_hash=genome.origin_hash,
        genome_hash=genome_hash,
        session_id=session_id,
        passed=passed,
        reasons=reasons,
    )
