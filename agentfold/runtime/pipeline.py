"""Full local AgentFold runtime pipeline."""

from __future__ import annotations

import hashlib
from pathlib import Path

from pydantic import BaseModel

from agentfold.authority.matrix import AuthoritySurface, check_authority
from agentfold.evidence.packet import FoldEvidencePacket, create_evidence_packet
from agentfold.fitness.evaluator import evaluate_fitness
from agentfold.folding.certificate import CertificateStatus, create_fold_certificate
from agentfold.folding.graph_builder import build_fold_graph
from agentfold.folding.misfold import detect_misfolds
from agentfold.folding.phenotype import AgentPhenotype, derive_phenotype
from agentfold.folding.predictor import predict_fold
from agentfold.genome.hashing import hash_genome
from agentfold.genome.loader import load_genome
from agentfold.genome.validator import validate_genome
from agentfold.gates.compounding_gate import CompoundingDecision, decide_compounding
from agentfold.ledger.writer import LedgerEntry
from agentfold.origin.alignment import check_alignment
from agentfold.origin.certificate import certify_origin
from agentfold.transcriptome.schema import (
    AgentTranscriptome,
    ClaimAttemptEntry,
    GateEventEntry,
)


class AgentFoldRunResult(BaseModel):
    run_id: str
    genome_valid: bool
    origin_aligned: bool
    compounding_decision: str
    phenotype: AgentPhenotype
    evidence_packet: FoldEvidencePacket
    ledger_entry: LedgerEntry
    claim_boundary: str = "local_pipeline_result_not_production_certification"


def _stable_id(prefix: str, *parts: str) -> str:
    joined = ":".join(parts)
    return f"{prefix}_{hashlib.sha256(joined.encode()).hexdigest()[:16]}"


def run_pipeline(
    *,
    genome_path: str | Path,
    task_path: str | Path | None = None,
    run_id: str = "agentfold_v1_local_run",
) -> AgentFoldRunResult:
    """Run the local AgentFold pipeline without external side effects."""
    genome = load_genome(genome_path)
    validation = validate_genome(genome)
    origin_certificate = certify_origin(genome, session_id=run_id)
    alignment = check_alignment(genome, origin_certificate)

    claim_count = 1 if task_path else 0
    evidence_count = len(genome.evidence_index)
    transcriptome = AgentTranscriptome(
        transcriptome_id=_stable_id("tx", run_id, genome.genome_id, str(claim_count), str(evidence_count)),
        run_id=run_id,
        agent_id=genome.agent_id,
        genome_id=genome.genome_id,
        origin_certificate_id=origin_certificate.certificate_id,
        activated_prompt_genes=sorted(genome.prompt_gene_ids()),
        claims_attempted=[
            ClaimAttemptEntry(
                claim_id="claim_task_local",
                claim_text="local task execution claim",
                evidence_refs=sorted(genome.evidence_ids()),
                outcome="allowed" if evidence_count else "downgraded",
            )
        ] if claim_count else [],
        evidence_used=sorted(genome.evidence_ids()),
        gate_events=[
            GateEventEntry(gate_id="genome_gate", gate_type="genome", passed=validation.passed, reason="genome_valid" if validation.passed else "genome_invalid"),
            GateEventEntry(gate_id="origin_gate", gate_type="origin", passed=alignment.aligned, reason=alignment.reason),
        ],
    )
    graph = build_fold_graph(transcriptome)
    prediction = predict_fold(
        has_origin=alignment.aligned,
        tool_count=len(genome.tool_manifest),
        evidence_count=evidence_count,
        claim_count=claim_count,
        gate_pass_rate=1.0 if validation.passed and alignment.aligned else 0.0,
    )
    misfolds = detect_misfolds(graph, origin_aligned=alignment.aligned)
    fitness = evaluate_fitness(
        origin_aligned=alignment.aligned,
        evidence_count=evidence_count,
        claim_count=claim_count,
        misfold_count=len(misfolds),
        tool_invocations=len(genome.tool_manifest),
        blocked_actions=0 if validation.passed and alignment.aligned else 1,
    )
    authority_decisions = [
        check_authority(surface=AuthoritySurface.FILESYSTEM, action="read"),
        check_authority(surface=AuthoritySurface.REPOSITORY, action="write"),
    ]
    compounding = decide_compounding(
        origin_passed=alignment.aligned,
        genome_valid=validation.passed,
        permission_passed=True,
        claim_within_ceiling=True,
        evidence_sufficient=evidence_count >= claim_count,
        transcript_complete=bool(transcriptome.transcriptome_id),
        fold_graph_complete=bool(graph.fold_graph_id),
        misfold_passed=not any(str(m.severity) in {"high", "critical"} for m in misfolds),
        tool_permitted=all(d.passed for d in authority_decisions if d.surface == AuthoritySurface.FILESYSTEM.value),
        replay_complete=True,
        ledger_written=True,
        inheritance_permitted=False,
    )
    status = (
        CertificateStatus.VALID_FOR_LOCAL_USE
        if compounding.decision in {CompoundingDecision.PERMIT, CompoundingDecision.PERMIT_WITH_WARNING}
        else CertificateStatus.BLOCKED
    )
    certificate = create_fold_certificate(
        run_id=run_id,
        agent_id=genome.agent_id,
        genome_id=genome.genome_id,
        origin_certificate_id=origin_certificate.certificate_id,
        transcriptome_id=transcriptome.transcriptome_id,
        fold_graph_id=graph.fold_graph_id,
        prediction_id=prediction.prediction_id,
        fitness_id=fitness.fitness_id,
        compounding_decision_id=str(compounding.decision),
        certificate_status=status,
    )
    phenotype = derive_phenotype(
        graph=graph,
        prediction=prediction,
        fitness=fitness,
        certificate=certificate,
        misfolds=misfolds,
    )
    ledger_entry = LedgerEntry(
        ledger_id=_stable_id("le", run_id, genome.genome_id),
        run_id=run_id,
        agent_id=genome.agent_id,
        genome_hash=hash_genome(genome),
        origin_certificate_hash=origin_certificate.certificate_id,
        transcriptome_hash=transcriptome.transcriptome_id,
        fold_graph_hash=graph.fold_graph_id,
        prediction_hash=prediction.prediction_id,
        misfold_hashes=[m.misfold_id for m in misfolds],
        fitness_hash=fitness.fitness_id,
        compounding_decision_hash=str(compounding.decision),
        fold_certificate_hash=certificate.certificate_id,
    )
    ledger_entry.entry_hash = ledger_entry.compute_hash()
    packet = create_evidence_packet(
        run_id=run_id,
        agent_id=genome.agent_id,
        genome_id=genome.genome_id,
        genome=genome,
        origin_certificate=origin_certificate,
        transcriptome=transcriptome,
        fold_graph=graph,
        prediction=prediction,
        misfolds=misfolds,
        fitness=fitness,
        phenotype=phenotype,
        certificate=certificate,
        authority_decisions=authority_decisions,
        ledger_hash=ledger_entry.entry_hash,
    )
    return AgentFoldRunResult(
        run_id=run_id,
        genome_valid=validation.passed,
        origin_aligned=alignment.aligned,
        compounding_decision=str(compounding.decision),
        phenotype=phenotype,
        evidence_packet=packet,
        ledger_entry=ledger_entry,
    )
