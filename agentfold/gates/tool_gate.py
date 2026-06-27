"""Tool Gate — tools must be manifest-bound, scoped, and logged."""

from __future__ import annotations

from dataclasses import dataclass
from agentfold.genome.schema import AgentGenome, RiskLevel


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
    genome: AgentGenome | None,
    invoked_tool_id: str = "",
    invoked_risk_level: str = "",
) -> GateResult:
    """Check tool invocation against manifest."""
    if not invoked_tool_id:
        return GateResult(passed=True, reason="no_tool_invoked", details={})

    if genome is None:
        return GateResult(passed=False, reason="no_genome_context", details={})

    tool = next((t for t in genome.tool_manifest if t.tool_id == invoked_tool_id), None)
    if tool is None:
        return GateResult(
            passed=False,
            reason="tool_not_in_manifest",
            details={"tool_id": invoked_tool_id},
        )

    if tool.risk_level == RiskLevel.CRITICAL and not tool.requires_human_confirmation:
        return GateResult(
            passed=False,
            reason="critical_tool_without_human_confirmation",
            details={"tool_id": invoked_tool_id},
        )

    return GateResult(
        passed=True,
        reason="tool_permitted",
        details={"tool_id": invoked_tool_id, "risk_level": str(tool.risk_level)},
    )
