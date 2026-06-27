"""Tests for AgentPhenotype derivation."""

from agentfold.fitness.evaluator import evaluate_fitness
from agentfold.folding.certificate import create_fold_certificate
from agentfold.folding.graph_builder import BehavioralFoldGraph, FoldNode, FoldNodeType
from agentfold.folding.misfold import MisfoldEvent, MisfoldSeverity
from agentfold.folding.phenotype import PhenotypeStatus, derive_phenotype
from agentfold.folding.predictor import predict_fold


def test_phenotype_derives_stable_local_status():
    graph = BehavioralFoldGraph(
        fold_graph_id="fg_001",
        run_id="run_001",
        agent_id="agent_001",
        genome_id="genome_001",
        nodes=[
            FoldNode(node_id="claim_001", node_type=FoldNodeType.CLAIM),
            FoldNode(node_id="ev_001", node_type=FoldNodeType.EVIDENCE),
            FoldNode(node_id="gate_001", node_type=FoldNodeType.GATE),
        ],
    )
    prediction = predict_fold(
        has_origin=True,
        evidence_count=2,
        claim_count=1,
        gate_pass_rate=1.0,
    )
    fitness = evaluate_fitness(
        origin_aligned=True,
        evidence_count=2,
        claim_count=1,
    )
    certificate = create_fold_certificate(
        run_id="run_001",
        agent_id="agent_001",
        genome_id="genome_001",
        origin_certificate_id="oc_001",
        fold_graph_id="fg_001",
        prediction_id=prediction.prediction_id,
        fitness_id=fitness.fitness_id,
    )

    phenotype = derive_phenotype(
        graph=graph,
        prediction=prediction,
        fitness=fitness,
        certificate=certificate,
        misfolds=[],
    )

    assert phenotype.status == PhenotypeStatus.STABLE_LOCAL
    assert phenotype.claim_boundary == "software_phenotype_not_biological_truth"
    assert "claim" in phenotype.expressed_capabilities
    assert phenotype.misfold_count == 0


def test_phenotype_blocks_high_misfold():
    graph = BehavioralFoldGraph(
        fold_graph_id="fg_002",
        run_id="run_002",
        agent_id="agent_001",
        genome_id="genome_001",
    )
    prediction = predict_fold(has_origin=True, evidence_count=1, claim_count=1)
    fitness = evaluate_fitness(origin_aligned=True, evidence_count=1, claim_count=1)
    certificate = create_fold_certificate(
        run_id="run_002",
        agent_id="agent_001",
        genome_id="genome_001",
        origin_certificate_id="oc_001",
    )
    misfolds = [
        MisfoldEvent(
            misfold_id="mf_001",
            misfold_type="claim_overreach",
            severity=MisfoldSeverity.HIGH,
        )
    ]

    phenotype = derive_phenotype(
        graph=graph,
        prediction=prediction,
        fitness=fitness,
        certificate=certificate,
        misfolds=misfolds,
    )

    assert phenotype.status == PhenotypeStatus.BLOCKED
    assert phenotype.high_or_critical_misfold_count == 1
    assert "claim_overreach" in phenotype.expressed_risks
