"""FoldPrediction — predict behavioral fold before compounding."""

from __future__ import annotations

import hashlib
from enum import Enum

from pydantic import BaseModel, Field


class PredictionMethod(str, Enum):
    RULES = "rules"
    HEURISTIC = "heuristic"
    GRAPH_METRIC = "graph_metric"
    CLASSIFIER = "classifier"
    LEARNED_MODEL = "learned_model"
    HYBRID = "hybrid"


class FoldPrediction(BaseModel):
    """Predicted fold state for a run."""

    prediction_id: str = ""
    run_id: str = ""
    agent_id: str = ""
    genome_id: str = ""
    predicted_drift: float = 0.0
    predicted_claim_risk: float = 0.0
    predicted_tool_risk: float = 0.0
    predicted_evidence_sufficiency: float = 0.0
    predicted_recursion_pressure: float = 0.0
    predicted_memory_pressure: float = 0.0
    predicted_origin_alignment: float = 1.0
    predicted_failure_attractors: list[str] = Field(default_factory=list)
    predicted_compounding_permission: bool = False
    prediction_method: PredictionMethod = PredictionMethod.RULES
    confidence: float = 0.0
    claim_boundary: str = "prediction_not_validation"


def predict_fold(
    *,
    has_origin: bool,
    tool_count: int,
    evidence_count: int,
    claim_count: int,
    gate_pass_rate: float = 1.0,
    drift_signals: int = 0,
) -> FoldPrediction:
    """Heuristic pre-fold prediction.

    This is NOT a proof. It is a bounded estimate for gate evaluation.
    """
    # Claim risk: high claims with low evidence = high risk
    if claim_count > 0:
        evidence_per_claim = evidence_count / claim_count
        claim_risk = max(0.0, min(1.0, 1.0 - evidence_per_claim))
    else:
        claim_risk = 0.0

    # Tool risk: many tools without origin = higher risk
    tool_risk = max(0.0, min(1.0, (tool_count * 0.15) - (0.3 if has_origin else 0.0)))

    # Drift prediction
    drift_prediction = max(0.0, min(1.0, drift_signals * 0.25))

    # Evidence sufficiency
    evidence_sufficiency = min(1.0, evidence_count / max(claim_count, 1))

    # Origin alignment prediction
    origin_alignment = 1.0 if has_origin else 0.2

    # Compounding permission — conservative default
    compounding = (
        has_origin
        and claim_risk < 0.7
        and tool_risk < 0.7
        and drift_prediction < 0.7
        and gate_pass_rate >= 0.8
    )

    # Failure attractors
    attractors: list[str] = []
    if not has_origin:
        attractors.append("missing_origin")
    if claim_risk > 0.5:
        attractors.append("claim_overreach")
    if tool_risk > 0.5:
        attractors.append("tool_instability")
    if drift_prediction > 0.5:
        attractors.append("origin_drift")

    pred_id = hashlib.sha256(
        f"{has_origin}:{tool_count}:{evidence_count}:{claim_count}:{gate_pass_rate}".encode()
    ).hexdigest()[:16]

    return FoldPrediction(
        prediction_id=pred_id,
        predicted_drift=round(drift_prediction, 4),
        predicted_claim_risk=round(claim_risk, 4),
        predicted_tool_risk=round(tool_risk, 4),
        predicted_evidence_sufficiency=round(evidence_sufficiency, 4),
        predicted_origin_alignment=round(origin_alignment, 4),
        predicted_compounding_permission=compounding,
        prediction_method=PredictionMethod.RULES,
        confidence=0.7 if has_origin else 0.3,
        predicted_failure_attractors=attractors,
    )
