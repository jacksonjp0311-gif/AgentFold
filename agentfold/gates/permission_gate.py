"""Permission Gate — tool and mutation permissions must be explicit."""

from __future__ import annotations

from dataclasses import dataclass
from agentfold.genome.schema import AgentGenome


@dataclass
class GateResult:
    passed: bool
    reason: str
    details: dict

    def to_dict(self) -> dict:
        return {"passed": self.passed, "reason": self.reason, "details": self.details}


def check(
    *,
    genome: AgentGenome | None,
    requested_tool_id: str = "",
    requested_action: str = "",
) -> GateResult:
    """Check if requested tool/action is permitted by the genome."""
    if genome is None:
        return GateResult(passed=False, reason="no_genome", details={})

    if not requested_tool_id:
        return GateResult(passed=True, reason="no_tool_requested", details={})

    tool = next((t for t in genome.tool_manifest if t.tool_id == requested_tool_id), None)
    if tool is None:
        return GateResult(
            passed=False,
            reason="tool_not_in_manifest",
            details={"tool_id": requested_tool_id},
        )

    if requested_action and requested_action in tool.denied_actions:
        return GateResult(
            passed=False,
            reason="action_denied",
            details={"tool_id": requested_tool_id, "action": requested_action},
        )

    if tool.requires_human_confirmation:
        return GateResult(
            passed=False,
            reason="requires_human_confirmation",
            details={"tool_id": requested_tool_id},
        )

    return GateResult(
        passed=True,
        reason="permission_granted",
        details={"tool_id": requested_tool_id, "action": requested_action},
    )
