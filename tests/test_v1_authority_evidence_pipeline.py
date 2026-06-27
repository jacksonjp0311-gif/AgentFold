"""Tests for v1 authority, evidence replay, pipeline, and release functional."""

from agentfold.authority.matrix import AuthoritySurface, check_authority
from agentfold.evidence.packet import verify_evidence_packet
from agentfold.release.functional import evaluate_release_functional
from agentfold.runtime.pipeline import run_pipeline


def test_authority_matrix_blocks_repo_write_by_default():
    decision = check_authority(surface=AuthoritySurface.REPOSITORY, action="write")
    assert decision.passed is False
    assert decision.blocked is True
    assert decision.reason == "surface_or_action_denied"


def test_authority_matrix_allows_local_read():
    decision = check_authority(surface=AuthoritySurface.FILESYSTEM, action="read")
    assert decision.passed is True
    assert decision.blocked is False


def test_pipeline_emits_replayable_evidence_packet():
    result = run_pipeline(
        genome_path="examples/genomes/minimal_agent_genome.json",
        task_path="examples/tasks/memory_drift_task.json",
        run_id="test_v1_pipeline",
    )
    replay = verify_evidence_packet(result.evidence_packet)

    assert result.genome_valid is True
    assert result.origin_aligned is True
    assert result.phenotype.phenotype_id
    assert result.evidence_packet.phenotype_hash
    assert replay["valid"] is True
    assert replay["claim_boundary"] == "evidence_packet_replay_not_truth_proof"


def test_release_functional_passes_only_when_tests_and_docs_pass():
    failed = evaluate_release_functional(tests_passed=True, docs_aligned=False)
    passed = evaluate_release_functional(tests_passed=True, docs_aligned=True)

    assert failed.passed() is False
    assert passed.passed() is True
    assert passed.score() == 1.0
    assert passed.claim_boundary == "release_functional_not_production_readiness"
