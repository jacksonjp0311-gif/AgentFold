"""Fold Graph Gate — behavior graph must exist for fold prediction claims."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GateResult:
    passed: bool
    reason: str
    details: dict

    def to_dict(self) -> dict:
        return {"passed": self.passed, "reason": self.reason, "details": self.details}

    def __init__(self, passed: bool, reason: str, details: dict | None = None):
        self.passed = passed
        self.reason = reason
        self.details = details or {}


def check(
    *,
    node_count: int = 0,
    edge_count: int = 0,
) -> GateResult:
    """Check fold graph existence and minimum structure."""
    if node_count == 0:
        return GateResult(passed=False, reason="fold_graph_empty", details={})

    if edge_count == 0:
        return GateResult(
            passed=False,
            reason="fold_graph_no_edges",
            details={"node_count": node_count},
        )

    return GateResult(
        passed=True,
        reason="fold_graph_present",
        details={"node_count": node_count, "edge_count": edge_count},
    )
