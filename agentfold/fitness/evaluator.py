"""FitnessVector evaluator — multi-dimensional scoring."""

from __future__ import annotations

import hashlib
from pydantic import BaseModel, Field


class FitnessVector(BaseModel):
    """FitnessVector — multi-dimensional fitness score.

    BIC (Blocked Invalid Compounding) is the canonical metric.
    """

    fitness_id: str = ""
    run_id: str = ""
    task_success: float = 0.0
    truth_alignment: float = 0.0
    origin_alignment: float = 0.0
    evidence_grounding: float = 0.0
    claim_discipline: float = 0.0
    tool_correctness: float = 0.0
    safety_margin: float = 0.0
    coherence: float = 0.0
    drift_resistance: float = 0.0
    recovery_quality: float = 0.0
    human_usefulness: float = 0.0
    blocked_invalid_compounding: bool = False
    false_block_risk: float = 0.0
    claim_boundary: str = "fitness_not_truth"

    def score(self) -> float:
        """Return weighted composite score."""
        weights = {
            "task_success": 0.15,
            "origin_alignment": 0.15,
            "evidence_grounding": 0.12,
            "claim_discipline": 0.10,
            "safety_margin": 0.10,
            "coherence": 0.08,
            "drift_resistance": 0.08,
            "tool_correctness": 0.07,
            "truth_alignment": 0.05,
            "recovery_quality": 0.05,
            "human_usefulness": 0.05,
        }
        total = sum(getattr(self, k) * v for k, v in weights.items())
        return round(total, 4)


def evaluate_fitness(
    *,
    origin_aligned: bool = True,
    evidence_count: int = 0,
    claim_count: int = 0,
    misfold_count: int = 0,
    tool_invocations: int = 0,
    blocked_actions: int = 0,
) -> FitnessVector:
    """Heuristic fitness evaluation."""
    origin_score = 1.0 if origin_aligned else 0.2
    evidence_score = min(1.0, evidence_count / max(claim_count, 1))
    claim_discipline = max(0.0, 1.0 - (max(0, claim_count - evidence_count) * 0.3))
    safety = max(0.0, 1.0 - misfold_count * 0.2)
    tool_score = max(0.0, 1.0 - max(0, tool_invocations - 5) * 0.1)
    bic = blocked_actions > 0 or (not origin_aligned)

    fitness_id = hashlib.sha256(
        f"{origin_aligned}:{evidence_count}:{claim_count}:{misfold_count}:{blocked_actions}".encode()
    ).hexdigest()[:16]

    return FitnessVector(
        fitness_id=fitness_id,
        task_success=0.5,  # placeholder — real implementation needs task evaluation
        truth_alignment=evidence_score * 0.8,
        origin_alignment=origin_score,
        evidence_grounding=evidence_score,
        claim_discipline=round(claim_discipline, 4),
        tool_correctness=round(tool_score, 4),
        safety_margin=round(safety, 4),
        coherence=round((origin_score + evidence_score) / 2, 4),
        drift_resistance=round(origin_score * 0.9, 4),
        recovery_quality=0.5,
        human_usefulness=0.5,
        blocked_invalid_compounding=bic,
        false_block_risk=0.1 if blocked_actions > 0 else 0.0,
    )
