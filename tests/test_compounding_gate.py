"""Tests for CompoundingGate decision logic."""

from agentfold.gates.compounding_gate import (
    CompoundingGate,
    CompoundingDecision,
    decide_compounding,
)


def test_gate_permits_when_all_pass():
    gate = CompoundingGate()
    result = gate.evaluate(
        origin_passed=True,
        genome_valid=True,
        permission_passed=True,
        claim_within_ceiling=True,
        evidence_sufficient=True,
        misfold_passed=True,
        tool_permitted=True,
        transcript_complete=True,
        fold_graph_complete=True,
        replay_complete=True,
        ledger_written=True,
        inheritance_permitted=True,
        human_auth_present=True,
    )
    assert result.decision == CompoundingDecision.PERMIT


def test_gate_blocks_on_origin_failure():
    gate = CompoundingGate()
    result = gate.evaluate(
        origin_passed=False,
        genome_valid=True,
        claim_within_ceiling=True,
    )
    assert result.decision == CompoundingDecision.BLOCK


def test_gate_blocks_on_missing_human_auth():
    gate = CompoundingGate()
    result = gate.evaluate(
        origin_passed=True,
        genome_valid=True,
        claim_within_ceiling=True,
        human_auth_required=True,
        human_auth_present=False,
    )
    assert result.decision == CompoundingDecision.BLOCK


def test_convenience_function_permit():
    result = decide_compounding(
        origin_passed=True,
        genome_valid=True,
        permission_passed=True,
        claim_within_ceiling=True,
        evidence_sufficient=True,
        misfold_passed=True,
        tool_permitted=True,
        transcript_complete=True,
        fold_graph_complete=True,
        replay_complete=True,
        ledger_written=True,
        inheritance_permitted=True,
        human_auth_present=True,
    )
    assert result.decision == CompoundingDecision.PERMIT
