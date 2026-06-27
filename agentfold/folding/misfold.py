"""MisfoldEvent — detect runtime structure indicating drift/risk/overreach."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class MisfoldType(str, Enum):
    ORIGIN_DRIFT = "origin_drift"
    MEMORY_DECOHERENCE = "memory_decoherence"
    UNSUPPORTED_CLAIM = "unsupported_claim"
    CLAIM_OVERREACH = "claim_overreach"
    TOOL_OVERREACH = "tool_overreach"
    UNAUTHORIZED_ACTION_PRESSURE = "unauthorized_action_pressure"
    RECURSIVE_LOOP = "recursive_loop"
    STALE_CONTEXT_ACTIVATION = "stale_context_activation"
    EVIDENCE_GAP = "evidence_gap"
    CONTRADICTION_UNRESOLVED = "contradiction_unresolved"
    HALLUCINATED_SOURCE = "hallucinated_source"
    UNSAFE_COMPOUNDING = "unsafe_compounding"
    PERMISSION_MISMATCH = "permission_mismatch"
    EXTERNAL_ACTION_WITHOUT_AUTHORITY = "external_action_without_authority"


class MisfoldSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MisfoldEvent(BaseModel):
    """A detected misfold — runtime structure indicating risk."""

    misfold_id: str = ""
    run_id: str = ""
    agent_id: str = ""
    fold_graph_id: str = ""
    misfold_type: MisfoldType | str = MisfoldType.UNSUPPORTED_CLAIM
    severity: MisfoldSeverity | str = MisfoldSeverity.LOW
    detected_by: str = "rule"
    evidence_refs: list[str] = Field(default_factory=list)
    recommended_action: str = "block"
    claim_boundary: str = "misfold_detection_not_safety_proof"


def detect_misfolds(
    graph: "BehavioralFoldGraph",
    *,
    origin_aligned: bool = True,
    gate_pass_rate: float = 1.0,
) -> list[MisfoldEvent]:
    """Detect misfolds from a fold graph and governance context."""
    from agentfold.folding.graph_builder import FoldNodeType

    events: list[MisfoldEvent] = []
    run_id = graph.run_id
    agent_id = graph.agent_id
    graph_id = graph.fold_graph_id

    # Origin drift
    if not origin_aligned:
        events.append(MisfoldEvent(
            misfold_id=f"mf_{graph_id}_origin",
            run_id=run_id,
            agent_id=agent_id,
            fold_graph_id=graph_id,
            misfold_type=MisfoldType.ORIGIN_DRIFT,
            severity=MisfoldSeverity.CRITICAL,
            detected_by="origin_gate",
            recommended_action="block",
        ))

    # Check misfold nodes in graph
    for node in graph.nodes:
        if node.node_type == FoldNodeType.MISFOLD:
            sev = MisfoldSeverity(node.metadata.get("severity", "low"))
            events.append(MisfoldEvent(
                misfold_id=f"mf_{node.node_id}",
                run_id=run_id,
                agent_id=agent_id,
                fold_graph_id=graph_id,
                misfold_type=node.label or MisfoldType.UNSUPPORTED_CLAIM,
                severity=sev,
                detected_by="graph_node",
                recommended_action="block" if sev in (MisfoldSeverity.HIGH, MisfoldSeverity.CRITICAL) else "shadow",
            ))

    # Claim overreach: high-risk claim nodes
    claim_nodes = [n for n in graph.nodes if n.node_type == FoldNodeType.CLAIM]
    high_risk_claims = [n for n in claim_nodes if n.risk >= 0.7]
    for cn in high_risk_claims:
        events.append(MisfoldEvent(
            misfold_id=f"mf_claim_{cn.node_id}",
            run_id=run_id,
            agent_id=agent_id,
            fold_graph_id=graph_id,
            misfold_type=MisfoldType.CLAIM_OVERREACH,
            severity=MisfoldSeverity.HIGH,
            detected_by="claim_gate",
            recommended_action="downgrade",
        ))

    # Evidence gap: claim nodes without supporting evidence nodes
    ev_nodes = [n for n in graph.nodes if n.node_type == FoldNodeType.EVIDENCE]
    if claim_nodes and not ev_nodes:
        events.append(MisfoldEvent(
            misfold_id=f"mf_{graph_id}_ev_gap",
            run_id=run_id,
            agent_id=agent_id,
            fold_graph_id=graph_id,
            misfold_type=MisfoldType.EVIDENCE_GAP,
            severity=MisfoldSeverity.MEDIUM,
            detected_by="evidence_gate",
            recommended_action="require_human_review",
        ))

    # Gate failure
    if gate_pass_rate < 0.8:
        events.append(MisfoldEvent(
            misfold_id=f"mf_{graph_id}_gate",
            run_id=run_id,
            agent_id=agent_id,
            fold_graph_id=graph_id,
            misfold_type=MisfoldType.UNSAFE_COMPOUNDING,
            severity=MisfoldSeverity.HIGH if gate_pass_rate < 0.5 else MisfoldSeverity.MEDIUM,
            detected_by="compounding_gate",
            recommended_action="block" if gate_pass_rate < 0.5 else "shadow",
        ))

    return events
