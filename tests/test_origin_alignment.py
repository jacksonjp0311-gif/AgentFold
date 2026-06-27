"""Tests for origin certificate, alignment, and deviation."""

import pytest

from agentfold.genome.schema import AgentGenome
from agentfold.origin.certificate import certify_origin, OriginCertificate
from agentfold.origin.alignment import check_alignment
from agentfold.origin.deviation import compute_deviation


@pytest.fixture
def genome():
    return AgentGenome(
        genome_id="g_001",
        agent_id="a_001",
        version="0.1.0",
        origin_ref="test_origin_path",
        origin_hash="abc123",
        claim_ceiling="diagnostic",
    )


def test_certify_origin_passes(genome):
    cert = certify_origin(genome)
    assert cert.passed is True
    assert cert.genome_id == genome.genome_id


def test_certify_origin_no_origin_ref():
    genome = AgentGenome(
        genome_id="g_001",
        agent_id="a_001",
        version="0.1.0",
        claim_ceiling="diagnostic",
    )
    cert = certify_origin(genome)
    assert cert.passed is False
    assert "origin_ref" in cert.reasons[0].lower() or "empty" in cert.reasons[0].lower()


def test_certify_origin_hash_mismatch(genome):
    cert = certify_origin(genome, prior_origin_hash="different_hash")
    assert cert.passed is False
    assert "mismatch" in cert.reasons[0].lower() or "drifted" in cert.reasons[0].lower()


def test_alignment_passes(genome):
    cert = certify_origin(genome)
    result = check_alignment(genome, cert)
    assert result.aligned is True


def test_alignment_fails_on_bad_certificate(genome):
    cert = certify_origin(genome)
    bad_cert = OriginCertificate(
        certificate_id="bad",
        genome_id="wrong_genome",
        agent_id=genome.agent_id,
        origin_ref=genome.origin_ref,
        genome_hash="hash",
        passed=False,
    )
    result = check_alignment(genome, bad_cert)
    assert result.aligned is False


def test_deviation_identical():
    result = compute_deviation(10, 10, 10)
    assert result.deviation == 0.0


def test_deviation_complete_divergence():
    result = compute_deviation(10, 10, 0)
    assert result.deviation == 1.0


def test_deviation_partial():
    result = compute_deviation(10, 10, 5)
    assert 0.0 < result.deviation < 1.0
