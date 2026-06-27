"""Test that compounding is blocked without origin alignment."""

from agentfold.gates.origin_gate import check as check_origin_gate
from agentfold.gates.compounding_gate import CompoundingGate, CompoundingDecision


def test_origin_gate_fails_without_ref():
    result = check_origin_gate(origin_ref="")
    assert result.passed is False


def test_compounding_blocked_without_origin():
    gate = CompoundingGate()
    result = gate.evaluate(
        origin_passed=False,
        genome_valid=True,
        claim_within_ceiling=True,
    )
    assert result.decision == CompoundingDecision.BLOCK


def test_compounding_permitted_with_origin():
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
    )
    assert result.decision == CompoundingDecision.PERMIT
