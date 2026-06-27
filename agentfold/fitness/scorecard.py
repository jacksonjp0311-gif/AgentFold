"""FitnessScorecard — tabular scoring report."""

from __future__ import annotations

from agentfold.fitness.evaluator import FitnessVector


class FitnessScorecard:
    """Generate a human-readable scorecard from a FitnessVector."""

    def __init__(self, fv: FitnessVector):
        self.fv = fv

    def to_dict(self) -> dict:
        return {
            "fitness_id": self.fv.fitness_id,
            "run_id": self.fv.run_id,
            "composite_score": self.fv.score(),
            "dimensions": {
                "task_success": self.fv.task_success,
                "truth_alignment": self.fv.truth_alignment,
                "origin_alignment": self.fv.origin_alignment,
                "evidence_grounding": self.fv.evidence_grounding,
                "claim_discipline": self.fv.claim_discipline,
                "tool_correctness": self.fv.tool_correctness,
                "safety_margin": self.fv.safety_margin,
                "coherence": self.fv.coherence,
                "drift_resistance": self.fv.drift_resistance,
                "recovery_quality": self.fv.recovery_quality,
                "human_usefulness": self.fv.human_usefulness,
            },
            "canonical_metric": {
                "blocked_invalid_compounding": self.fv.blocked_invalid_compounding,
                "false_block_risk": self.fv.false_block_risk,
            },
            "claim_boundary": self.fv.claim_boundary,
        }

    def to_table(self) -> list[dict]:
        """Return scorecard as a list of rows for tabular display."""
        d = self.to_dict()
        rows = []
        for k, v in d["dimensions"].items():
            rows.append({"metric": k, "score": v})
        rows.append({"metric": "COMPOSITE", "score": d["composite_score"]})
        rows.append({"metric": "BIC", "score": d["canonical_metric"]["blocked_invalid_compounding"]})
        rows.append({"metric": "FALSE_BLOCK_RISK", "score": d["canonical_metric"]["false_block_risk"]})
        rows.append({"metric": "CLAIM_BOUNDARY", "score": d["claim_boundary"]})
        return rows
