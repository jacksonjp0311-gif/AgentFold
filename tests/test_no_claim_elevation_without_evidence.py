"""Test that claim elevation is blocked without evidence."""

from agentfold.gates.evidence_gate import check as check_evidence
from agentfold.gates.compounding_gate import CompoundingGate, CompoundingDecision


def test_evidence_gate_fails_with_no_evidence():
    result = check_evidence(claim_count=3, evidence_count=0)
    assert result.passed is False
    assert "no_evidence" in result.reason


def test_evidence_gate_passes_with_sufficient():
    result = check_evidence(claim_count=2, evidence_count=5)
    assert result.passed is True


def test_compounding_blocked_with_insufficient_evidence():
    gate = CompoundingGate()
    result = gate.evaluate(
        origin_passed=True,
        genome_valid=True,
        claim_within_ceiling=True,
        evidence_sufficient=False,
        misfold_passed=True,
    )
    assert result.decision != CompoundingDecision.PERMIT
