"""Tests for MisfoldEvent detection and misfold gate."""

from agentfold.folding.misfold import (
    detect_misfolds,
    MisfoldEvent,
    MisfoldSeverity,
)
from agentfold.folding.graph_builder import (
    BehavioralFoldGraph,
    FoldNode,
    FoldNodeType,
)
from agentfold.gates.misfold_gate import check as check_misfold_gate


def test_no_misfolds_empty_graph():
    graph = BehavioralFoldGraph(fold_graph_id="test", run_id="r1", agent_id="a1")
    misfolds = detect_misfolds(graph, origin_aligned=True)
    origin_drift = [m for m in misfolds if "origin" in str(m.misfold_type)]
    assert len(origin_drift) == 0


def test_origin_drift_detected():
    graph = BehavioralFoldGraph(fold_graph_id="test", run_id="r1", agent_id="a1")
    misfolds = detect_misfolds(graph, origin_aligned=False)
    types = [str(m.misfold_type) for m in misfolds]
    assert any("origin_drift" in t for t in types)


def test_misfold_gate_passes_with_no_misfolds():
    result = check_misfold_gate([])
    assert result.passed is True


def test_misfold_gate_blocks_critical():
    misfolds = [
        MisfoldEvent(
            misfold_id="mf_001",
            misfold_type="origin_drift",
            severity=MisfoldSeverity.CRITICAL,
        )
    ]
    result = check_misfold_gate(misfolds)
    assert result.passed is False
    assert "critical" in result.reason


def test_misfold_gate_blocks_high():
    misfolds = [
        MisfoldEvent(
            misfold_id="mf_001",
            misfold_type="claim_overreach",
            severity="high",
        )
    ]
    result = check_misfold_gate(misfolds)
    assert result.passed is False


def test_evidence_gap_detected():
    graph = BehavioralFoldGraph(
        fold_graph_id="test",
        run_id="r1",
        agent_id="a1",
        nodes=[
            FoldNode(node_id="n1", node_type=FoldNodeType.CLAIM, risk=0.8, label="unsubstantiated"),
        ],
    )
    misfolds = detect_misfolds(graph, origin_aligned=True)
    types = [str(m.misfold_type) for m in misfolds]
    assert any("evidence_gap" in t for t in types)
