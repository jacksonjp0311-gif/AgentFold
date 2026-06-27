"""Origin deviation metric — d(Γ(S_n), Γ(R))."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class DeviationResult:
    """Quantified deviation between session geometry and origin geometry."""

    deviation: float  # 0.0 = identical, 1.0 = fully diverged
    details: dict

    def to_dict(self) -> dict:
        return {"deviation": self.deviation, "details": self.details}


def compute_deviation(
    origin_node_count: int,
    session_node_count: int,
    shared_node_count: int,
) -> DeviationResult:
    """Compute deviation as Jaccard-style distance over graph nodes.

    d = 1 - (|shared| / |union|)
    """
    union = origin_node_count + session_node_count - shared_node_count
    if union <= 0:
        return DeviationResult(deviation=0.0, details={"union": 0})

    jaccard = shared_node_count / union
    deviation = 1.0 - jaccard
    return DeviationResult(
        deviation=round(deviation, 6),
        details={
            "origin_nodes": origin_node_count,
            "session_nodes": session_node_count,
            "shared_nodes": shared_node_count,
            "union": union,
            "jaccard": round(jaccard, 6),
        },
    )
