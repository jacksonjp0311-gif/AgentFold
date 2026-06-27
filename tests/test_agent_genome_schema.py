"""Tests for AgentGenome schema, loader, validator, and hashing."""

import json
import tempfile
from pathlib import Path

import pytest

from agentfold.genome.schema import (
    AgentGenome,
    PromptGene,
    PromptGeneType,
    ToolSpec,
    ToolType,
    RiskLevel,
    PermissionSpec,
    ConstraintSpec,
    EvidenceRef,
    FailureMode,
)
from agentfold.genome.loader import load_genome, load_genome_from_dict
from agentfold.genome.validator import validate_genome
from agentfold.genome.hashing import hash_genome


@pytest.fixture
def minimal_genome():
    return AgentGenome(
        genome_id="test_genome_001",
        agent_id="test_agent_001",
        version="0.1.0",
        origin_ref="test_origin",
        prompt_genome=[
            PromptGene(
                gene_id="gene_001",
                gene_type=PromptGeneType.ROLE,
                content="Be helpful.",
            )
        ],
        tool_manifest=[
            ToolSpec(
                tool_id="tool_001",
                tool_name="read_file",
                tool_type=ToolType.READ_ONLY,
                risk_level=RiskLevel.LOW,
            )
        ],
        permission_manifest=[
            PermissionSpec(
                permission_id="perm_001",
                surface="filesystem",
            )
        ],
        claim_ceiling="diagnostic",
        evidence_index=[
            EvidenceRef(evidence_id="ev_001", confidence=0.9)
        ],
        known_failure_modes=[
            FailureMode(failure_id="fm_001", failure_type="test_failure")
        ],
    )


def test_genome_creation(minimal_genome):
    assert minimal_genome.genome_id == "test_genome_001"
    assert minimal_genome.agent_id == "test_agent_001"
    assert len(minimal_genome.prompt_genome) == 1
    assert minimal_genome.nonclaim_boundary != ""


def test_genome_tool_ids(minimal_genome):
    ids = minimal_genome.tool_ids()
    assert "tool_001" in ids


def test_genome_evidence_ids(minimal_genome):
    ids = minimal_genome.evidence_ids()
    assert "ev_001" in ids


def test_genome_validation_passes(minimal_genome):
    result = validate_genome(minimal_genome)
    assert result.passed is True
    assert len(result.errors) == 0


def test_genome_validation_missing_genome_id():
    genome = AgentGenome(
        genome_id="",
        agent_id="agent_001",
        version="0.1.0",
        claim_ceiling="diagnostic",
    )
    result = validate_genome(genome)
    assert result.passed is False
    assert "genome_id is required" in result.errors


def test_genome_validation_missing_claim_ceiling():
    genome = AgentGenome(
        genome_id="g_001",
        agent_id="a_001",
        version="0.1.0",
        claim_ceiling="",
    )
    result = validate_genome(genome)
    assert result.passed is False
    assert "claim_ceiling must be declared" in result.errors


def test_genome_validation_high_risk_tool_no_gate():
    genome = AgentGenome(
        genome_id="g_001",
        agent_id="a_001",
        version="0.1.0",
        claim_ceiling="compounding",
        tool_manifest=[
            ToolSpec(
                tool_id="tool_high",
                tool_name="deploy",
                tool_type=ToolType.EXTERNAL_API,
                risk_level=RiskLevel.HIGH,
            )
        ],
    )
    result = validate_genome(genome)
    assert len(result.warnings) > 0


def test_genome_hash(minimal_genome):
    h = hash_genome(minimal_genome)
    assert len(h) == 64  # SHA-256 hex
    h2 = hash_genome(minimal_genome)
    assert h == h2  # Deterministic


def test_genome_load_from_file(minimal_genome):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(minimal_genome.model_dump_json())
        path = f.name

    loaded = load_genome(path)
    assert loaded.genome_id == minimal_genome.genome_id
    Path(path).unlink()


def test_genome_load_from_dict():
    data = {
        "genome_id": "g_001",
        "agent_id": "a_001",
        "version": "0.1.0",
        "claim_ceiling": "diagnostic",
    }
    genome = load_genome_from_dict(data)
    assert genome.genome_id == "g_001"
