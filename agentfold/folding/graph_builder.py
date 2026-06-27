"""BehavioralFoldGraph — graph of expressed runtime structure."""

from __future__ import annotations

import hashlib
import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class FoldNodeType(str, Enum):
    PROMPT_GENE = "prompt_gene"
    MEMORY_FRAGMENT = "memory_fragment"
    TOOL = "tool"
    CLAIM = "claim"
    EVIDENCE = "evidence"
    GATE = "gate"
    STATE = "state"
    OUTPUT = "output"
    REPAIR = "repair"
    MISFOLD = "misfold"


class FoldRelation(str, Enum):
    ACTIVATED = "activated"
    DEPENDS_ON = "depends_on"
    CONTRADICTS = "contradicts"
    SUPPORTS = "supports"
    BLOCKS = "blocks"
    DOWNGRADES = "downgrades"
    PERMITS = "permits"
    REPAIRS = "repairs"
    COMPOUNDS_INTO = "compounds_into"
    DRIFTS_FROM = "drifts_from"
    INVOKES = "invokes"


class FoldNode(BaseModel):
    node_id: str
    node_type: FoldNodeType | str = FoldNodeType.STATE
    label: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    risk: float = 0.0
    confidence: float = 0.0


class FoldEdge(BaseModel):
    edge_id: str = ""
    source: str = ""
    target: str = ""
    relation: FoldRelation | str = FoldRelation.ACTIVATED
    weight: float = 1.0
    evidence_refs: list[str] = Field(default_factory=list)


class FoldMetrics(BaseModel):
    node_count: int = 0
    edge_count: int = 0
    avg_risk: float = 0.0
    max_risk: float = 0.0
    claim_count: int = 0
    evidence_count: int = 0
    gate_count: int = 0
    misfold_count: int = 0


class BehavioralFoldGraph(BaseModel):
    """BehavioralFoldGraph — causal/semantic structure of an agent run."""

    fold_graph_id: str = ""
    run_id: str = ""
    agent_id: str = ""
    genome_id: str = ""
    nodes: list[FoldNode] = Field(default_factory=list)
    edges: list[FoldEdge] = Field(default_factory=list)
    metrics: FoldMetrics = Field(default_factory=FoldMetrics)
    prediction_id: str | None = None
    observed_outcome_id: str | None = None
    ledger_hash: str = ""
    claim_boundary: str = "fold_graph_constructed"

    def node_ids(self) -> set[str]:
        return {n.node_id for n in self.nodes}

    def edge_count(self) -> int:
        return len(self.edges)

    def compute_metrics(self):
        risks = [n.risk for n in self.nodes]
        self.metrics = FoldMetrics(
            node_count=len(self.nodes),
            edge_count=len(self.edges),
            avg_risk=round(sum(risks) / len(risks), 4) if risks else 0.0,
            max_risk=round(max(risks), 4) if risks else 0.0,
            claim_count=sum(1 for n in self.nodes if n.node_type == FoldNodeType.CLAIM),
            evidence_count=sum(1 for n in self.nodes if n.node_type == FoldNodeType.EVIDENCE),
            gate_count=sum(1 for n in self.nodes if n.node_type == FoldNodeType.GATE),
            misfold_count=sum(1 for n in self.nodes if n.node_type == FoldNodeType.MISFOLD),
        )


def build_fold_graph(
    transcriptome: "AgentTranscriptome",
) -> BehavioralFoldGraph:
    """Build a BehavioralFoldGraph from a transcriptome."""
    from agentfold.transcriptome.schema import AgentTranscriptome

    nodes: list[FoldNode] = []
    edges: list[FoldEdge] = []
    idx = 0

    def nid(prefix: str) -> str:
        nonlocal idx
        idx += 1
        return f"{prefix}_{idx:04d}"

    # Prompt gene nodes
    for gene_id in transcriptome.activated_prompt_genes:
        nodes.append(FoldNode(
            node_id=nid("gene"),
            node_type=FoldNodeType.PROMPT_GENE,
            label=gene_id,
            confidence=0.9,
        ))

    # Memory nodes
    for mem in transcriptome.activated_memory:
        nodes.append(FoldNode(
            node_id=nid("mem"),
            node_type=FoldNodeType.MEMORY_FRAGMENT,
            label=mem.memory_id,
            metadata={"activation_reason": mem.activation_reason},
            confidence=mem.relevance_score,
        ))

    # Tool nodes
    for tool in transcriptome.activated_tools:
        nodes.append(FoldNode(
            node_id=nid("tool"),
            node_type=FoldNodeType.TOOL,
            label=tool.tool_id,
            metadata={"action": tool.action},
            risk=0.5 if tool.action else 0.2,
        ))

    # Claim nodes
    for claim in transcriptome.claims_attempted:
        risk = 0.0 if claim.outcome == "allowed" else 0.7
        nodes.append(FoldNode(
            node_id=nid("claim"),
            node_type=FoldNodeType.CLAIM,
            label=claim.claim_id,
            risk=risk,
            metadata={"outcome": claim.outcome, "text": claim.claim_text},
        ))

    # Evidence nodes
    for ev_id in transcriptome.evidence_used:
        nodes.append(FoldNode(
            node_id=nid("ev"),
            node_type=FoldNodeType.EVIDENCE,
            label=ev_id,
            confidence=0.8,
        ))

    # Gate nodes
    for gate in transcriptome.gate_events:
        nodes.append(FoldNode(
            node_id=nid("gate"),
            node_type=FoldNodeType.GATE,
            label=gate.gate_id,
            risk=0.0 if gate.passed else 0.8,
            metadata={"passed": gate.passed, "gate_type": gate.gate_type},
        ))

    # Misfold nodes
    for misfold in transcriptome.misfold_events:
        sev_map = {"low": 0.3, "medium": 0.5, "high": 0.8, "critical": 1.0}
        nodes.append(FoldNode(
            node_id=nid("misfold"),
            node_type=FoldNodeType.MISFOLD,
            label=misfold.misfold_type,
            risk=sev_map.get(misfold.severity, 0.5),
            metadata={"severity": misfold.severity},
        ))

    # Build edges: connect claims to evidence, tools to genes, misfolds to triggers
    claim_nodes = [n for n in nodes if n.node_type == FoldNodeType.CLAIM]
    ev_nodes = [n for n in nodes if n.node_type == FoldNodeType.EVIDENCE]
    tool_nodes = [n for n in nodes if n.node_type == FoldNodeType.TOOL]
    misfold_nodes = [n for n in nodes if n.node_type == FoldNodeType.MISFOLD]

    for cn in claim_nodes:
        for en in ev_nodes:
            edges.append(FoldEdge(
                edge_id=f"e_{cn.node_id}_{en.node_id}",
                source=en.node_id,
                target=cn.node_id,
                relation=FoldRelation.SUPPORTS,
            ))

    gene_nodes = [n for n in nodes if n.node_type == FoldNodeType.PROMPT_GENE]
    for tn in tool_nodes:
        if gene_nodes:
            edges.append(FoldEdge(
                edge_id=f"e_{gene_nodes[0].node_id}_{tn.node_id}",
                source=gene_nodes[0].node_id,
                target=tn.node_id,
                relation=FoldRelation.INVOKES,
            ))

    for mn in misfold_nodes:
        edges.append(FoldEdge(
            edge_id=f"e_{mn.node_id}_alert",
            source=mn.node_id,
            target=mn.node_id,
            relation=FoldRelation.DRIFTS_FROM,
            weight=mn.risk,
        ))

    # Hash
    canonical = f"{len(nodes)}:{len(edges)}"
    graph_hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]

    graph_id = f"fg_{hashlib.sha256(transcriptome.run_id.encode()).hexdigest()[:12]}"
    graph = BehavioralFoldGraph(
        fold_graph_id=graph_id,
        run_id=transcriptome.run_id,
        agent_id=transcriptome.agent_id,
        genome_id=transcriptome.genome_id,
        nodes=nodes,
        edges=edges,
        ledger_hash=graph_hash,
    )
    graph.compute_metrics()
    return graph
