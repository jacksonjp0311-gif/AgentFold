"""AgentPhenotype - observed behavior summary from fold evidence."""

from __future__ import annotations

import hashlib
from enum import Enum

from pydantic import BaseModel, Field

from agentfold.fitness.evaluator import FitnessVector
from agentfold.folding.certificate import FoldCertificate
from agentfold.folding.graph_builder import BehavioralFoldGraph
from agentfold.folding.misfold import MisfoldEvent
from agentfold.folding.predictor import FoldPrediction


class PhenotypeStatus(str, Enum):
    DIAGNOSTIC = "diagnostic"
    STABLE_LOCAL = "stable_local"
    REPAIR_REQUIRED = "repair_required"
    SHADOW_ONLY = "shadow_only"
    BLOCKED = "blocked"


class AgentPhenotype(BaseModel):
    """Observed software phenotype derived from runtime evidence.

    This is a software behavior summary. It is not a biological phenotype.
    """

    phenotype_id: str = ""
    run_id: str = ""
    agent_id: str = ""
    genome_id: str = ""
    fold_graph_id: str = ""
    prediction_id: str = ""
    fitness_id: str = ""
    certificate_id: str = ""
    expressed_capabilities: list[str] = Field(default_factory=list)
    expressed_risks: list[str] = Field(default_factory=list)
    misfold_count: int = 0
    high_or_critical_misfold_count: int = 0
    composite_fitness: float = 0.0
    predicted_compounding_permission: bool = False
    status: PhenotypeStatus = PhenotypeStatus.DIAGNOSTIC
    claim_boundary: str = "software_phenotype_not_biological_truth"


def derive_phenotype(
    *,
    graph: BehavioralFoldGraph,
    prediction: FoldPrediction,
    fitness: FitnessVector,
    certificate: FoldCertificate,
    misfolds: list[MisfoldEvent] | None = None,
) -> AgentPhenotype:
    """Derive an AgentPhenotype from fold evidence."""
    misfolds = misfolds or []
    severe = [
        m for m in misfolds
        if str(m.severity) in {"high", "critical", "MisfoldSeverity.HIGH", "MisfoldSeverity.CRITICAL"}
    ]

    capabilities = sorted({
        node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type)
        for node in graph.nodes
        if node.node_type not in {"misfold"}
    })
    risks = sorted({
        str(m.misfold_type.value if hasattr(m.misfold_type, "value") else m.misfold_type)
        for m in misfolds
    })

    composite = fitness.score()
    if severe or not prediction.predicted_compounding_permission:
        status = PhenotypeStatus.BLOCKED if severe else PhenotypeStatus.REPAIR_REQUIRED
    elif composite >= 0.75:
        status = PhenotypeStatus.STABLE_LOCAL
    else:
        status = PhenotypeStatus.SHADOW_ONLY

    canonical = (
        f"{graph.run_id}:{graph.agent_id}:{graph.genome_id}:"
        f"{graph.fold_graph_id}:{prediction.prediction_id}:{fitness.fitness_id}:"
        f"{certificate.certificate_id}:{len(misfolds)}:{status.value}"
    )
    phenotype_id = f"ph_{hashlib.sha256(canonical.encode()).hexdigest()[:16]}"

    return AgentPhenotype(
        phenotype_id=phenotype_id,
        run_id=graph.run_id,
        agent_id=graph.agent_id,
        genome_id=graph.genome_id,
        fold_graph_id=graph.fold_graph_id,
        prediction_id=prediction.prediction_id,
        fitness_id=fitness.fitness_id,
        certificate_id=certificate.certificate_id,
        expressed_capabilities=capabilities,
        expressed_risks=risks,
        misfold_count=len(misfolds),
        high_or_critical_misfold_count=len(severe),
        composite_fitness=composite,
        predicted_compounding_permission=prediction.predicted_compounding_permission,
        status=status,
    )
