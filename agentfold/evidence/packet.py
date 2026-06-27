"""Replayable fold evidence packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class FoldEvidencePacket(BaseModel):
    """Hash-addressed evidence packet for one AgentFold run."""

    schema_version: str = "1.0.0"
    packet_id: str = ""
    run_id: str = ""
    agent_id: str = ""
    genome_id: str = ""
    genome_hash: str = ""
    origin_certificate_hash: str = ""
    transcriptome_hash: str = ""
    fold_graph_hash: str = ""
    prediction_hash: str = ""
    misfold_hashes: list[str] = Field(default_factory=list)
    fitness_hash: str = ""
    phenotype_hash: str = ""
    certificate_hash: str = ""
    authority_hash: str = ""
    ledger_hash: str = ""
    artifacts: dict[str, Any] = Field(default_factory=dict)
    claim_boundary: str = "evidence_packet_replay_not_truth_proof"

    def canonical_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude={"packet_id"})

    def compute_packet_id(self) -> str:
        data = json.dumps(self.canonical_dict(), sort_keys=True, default=str)
        return f"fep_{hashlib.sha256(data.encode()).hexdigest()[:16]}"


def _hash_artifact(artifact: Any) -> str:
    if hasattr(artifact, "model_dump"):
        data = artifact.model_dump()
    elif hasattr(artifact, "to_dict"):
        data = artifact.to_dict()
    else:
        data = artifact
    canonical = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()[:32]


def create_evidence_packet(
    *,
    run_id: str,
    agent_id: str,
    genome_id: str,
    genome: Any,
    origin_certificate: Any,
    transcriptome: Any,
    fold_graph: Any,
    prediction: Any,
    misfolds: list[Any],
    fitness: Any,
    phenotype: Any,
    certificate: Any,
    authority_decisions: list[Any] | None = None,
    ledger_hash: str = "",
) -> FoldEvidencePacket:
    """Create a replayable evidence packet from run artifacts."""
    authority_decisions = authority_decisions or []
    packet = FoldEvidencePacket(
        run_id=run_id,
        agent_id=agent_id,
        genome_id=genome_id,
        genome_hash=_hash_artifact(genome),
        origin_certificate_hash=_hash_artifact(origin_certificate),
        transcriptome_hash=_hash_artifact(transcriptome),
        fold_graph_hash=_hash_artifact(fold_graph),
        prediction_hash=_hash_artifact(prediction),
        misfold_hashes=[_hash_artifact(m) for m in misfolds],
        fitness_hash=_hash_artifact(fitness),
        phenotype_hash=_hash_artifact(phenotype),
        certificate_hash=_hash_artifact(certificate),
        authority_hash=_hash_artifact([a.model_dump() if hasattr(a, "model_dump") else a for a in authority_decisions]),
        ledger_hash=ledger_hash,
        artifacts={
            "genome": genome.model_dump() if hasattr(genome, "model_dump") else genome,
            "origin_certificate": origin_certificate.model_dump() if hasattr(origin_certificate, "model_dump") else origin_certificate,
            "transcriptome": transcriptome.model_dump() if hasattr(transcriptome, "model_dump") else transcriptome,
            "fold_graph": fold_graph.model_dump() if hasattr(fold_graph, "model_dump") else fold_graph,
            "prediction": prediction.model_dump() if hasattr(prediction, "model_dump") else prediction,
            "misfolds": [m.model_dump() if hasattr(m, "model_dump") else m for m in misfolds],
            "fitness": fitness.model_dump() if hasattr(fitness, "model_dump") else fitness,
            "phenotype": phenotype.model_dump() if hasattr(phenotype, "model_dump") else phenotype,
            "certificate": certificate.model_dump() if hasattr(certificate, "model_dump") else certificate,
            "authority_decisions": [a.model_dump() if hasattr(a, "model_dump") else a for a in authority_decisions],
        },
    )
    packet.packet_id = packet.compute_packet_id()
    return packet


def verify_evidence_packet(packet: FoldEvidencePacket) -> dict[str, Any]:
    """Verify packet self-hash and required artifact hashes."""
    failures: list[str] = []
    expected_id = packet.compute_packet_id()
    if packet.packet_id != expected_id:
        failures.append(f"packet_id mismatch: expected {expected_id}, got {packet.packet_id}")

    required_hashes = [
        "genome_hash",
        "origin_certificate_hash",
        "transcriptome_hash",
        "fold_graph_hash",
        "prediction_hash",
        "fitness_hash",
        "phenotype_hash",
        "certificate_hash",
        "authority_hash",
    ]
    for field in required_hashes:
        if not getattr(packet, field):
            failures.append(f"missing {field}")

    return {
        "valid": not failures,
        "packet_id": packet.packet_id,
        "failures": failures,
        "claim_boundary": packet.claim_boundary,
    }


def write_evidence_packet(packet: FoldEvidencePacket, path: str | Path) -> Path:
    """Write an evidence packet to disk as canonical JSON."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(packet.model_dump(), indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return output_path


def read_evidence_packet(path: str | Path) -> FoldEvidencePacket:
    """Read an evidence packet from disk."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return FoldEvidencePacket(**data)


def diff_evidence_packets(left: FoldEvidencePacket, right: FoldEvidencePacket) -> dict[str, Any]:
    """Compare two evidence packets by stable hash surfaces."""
    fields = [
        "genome_hash",
        "origin_certificate_hash",
        "transcriptome_hash",
        "fold_graph_hash",
        "prediction_hash",
        "fitness_hash",
        "phenotype_hash",
        "certificate_hash",
        "authority_hash",
        "ledger_hash",
    ]
    changed = [
        field for field in fields
        if getattr(left, field) != getattr(right, field)
    ]
    return {
        "left_packet_id": left.packet_id,
        "right_packet_id": right.packet_id,
        "changed_fields": changed,
        "same_run_id": left.run_id == right.run_id,
        "claim_boundary": "evidence_diff_not_behavioral_truth",
    }
