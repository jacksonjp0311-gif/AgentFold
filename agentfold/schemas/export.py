"""Export JSON Schemas for core AgentFold artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Type

from pydantic import BaseModel

from agentfold.authority.matrix import AuthorityDecision, AuthorityMatrix, AuthorityRequest
from agentfold.evidence.packet import FoldEvidencePacket
from agentfold.fitness.evaluator import FitnessVector
from agentfold.folding.certificate import FoldCertificate
from agentfold.folding.graph_builder import BehavioralFoldGraph
from agentfold.folding.misfold import MisfoldEvent
from agentfold.folding.phenotype import AgentPhenotype
from agentfold.folding.predictor import FoldPrediction
from agentfold.genome.schema import AgentGenome
from agentfold.ledger.writer import LedgerEntry
from agentfold.origin.certificate import OriginCertificate
from agentfold.transcriptome.schema import AgentTranscriptome


CORE_SCHEMA_MODELS: dict[str, Type[BaseModel]] = {
    "agent_genome": AgentGenome,
    "origin_certificate": OriginCertificate,
    "agent_transcriptome": AgentTranscriptome,
    "behavioral_fold_graph": BehavioralFoldGraph,
    "fold_prediction": FoldPrediction,
    "misfold_event": MisfoldEvent,
    "fitness_vector": FitnessVector,
    "agent_phenotype": AgentPhenotype,
    "fold_certificate": FoldCertificate,
    "authority_matrix": AuthorityMatrix,
    "authority_request": AuthorityRequest,
    "authority_decision": AuthorityDecision,
    "fold_evidence_packet": FoldEvidencePacket,
    "ledger_entry": LedgerEntry,
}


def export_core_schemas(output_dir: str | Path) -> list[Path]:
    """Export core Pydantic model schemas to JSON files."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name, model in CORE_SCHEMA_MODELS.items():
        path = out / f"{name}.schema.json"
        path.write_text(
            json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written.append(path)
    return written
