"""Test that unauthorized tool calls are blocked by Permission Gate."""

import pytest

from agentfold.genome.schema import (
    AgentGenome,
    ToolSpec,
    ToolType,
    RiskLevel,
)
from agentfold.gates.permission_gate import check as check_permission


@pytest.fixture
def genome_with_limited_tools():
    return AgentGenome(
        genome_id="g_001",
        agent_id="a_001",
        version="0.1.0",
        origin_ref="test",
        tool_manifest=[
            ToolSpec(
                tool_id="tool_read",
                tool_name="read_file",
                tool_type=ToolType.READ_ONLY,
                risk_level=RiskLevel.LOW,
            )
        ],
        claim_ceiling="diagnostic",
    )


def test_allowed_tool(genome_with_limited_tools):
    result = check_permission(
        genome=genome_with_limited_tools,
        requested_tool_id="tool_read",
        requested_action="read",
    )
    assert result.passed is True


def test_blocked_tool_not_in_manifest(genome_with_limited_tools):
    result = check_permission(
        genome=genome_with_limited_tools,
        requested_tool_id="tool_delete",
        requested_action="delete",
    )
    assert result.passed is False
    assert "not_in_manifest" in result.reason


def test_no_tool_requested(genome_with_limited_tools):
    result = check_permission(
        genome=genome_with_limited_tools,
    )
    assert result.passed is True
