"""Tests for BehavioralFoldGraph builder."""

import pytest

from agentfold.transcriptome.schema import (
    AgentTranscriptome,
    ClaimAttemptEntry,
    GateEventEntry,
)
from agentfold.folding.graph_builder import build_fold_graph, BehavioralFoldGraph


@pytest.fixture
def sample_transcriptome():
    return AgentTranscriptome(
        run_id="run_001",
        agent_id="a_001",
        genome_id="g_001",
        activated_prompt_genes=["gene_001", "gene_002"],
        claims_attempted=[
            ClaimAttemptEntry(claim_id="c_001", claim_text="test", outcome="blocked"),
        ],
        evidence_used=["ev_001"],
        gate_events=[
            GateEventEntry(gate_id="gate_origin", gate_type="origin", passed=True),
        ],
    )


def test_build_fold_graph(sample_transcriptome):
    graph = build_fold_graph(sample_transcriptome)
    assert isinstance(graph, BehavioralFoldGraph)
    assert graph.run_id == "run_001"
    assert len(graph.nodes) > 0
    assert graph.metrics.node_count > 0


def test_fold_graph_metrics(sample_transcriptome):
    graph = build_fold_graph(sample_transcriptome)
    assert graph.metrics.claim_count >= 1
    assert graph.metrics.evidence_count >= 1
