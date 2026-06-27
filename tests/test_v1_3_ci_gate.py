"""Tests for v1.3 CI gate and misfold fixtures."""

import json
from pathlib import Path

from click.testing import CliRunner

from agentfold.ci.policy import AgentFoldPolicy, load_policy
from agentfold.ci.verify import verify_for_ci, write_ci_summary
from agentfold.cli import main
from agentfold.evidence.packet import FoldEvidencePacket, verify_evidence_packet
from agentfold.runtime.pipeline import run_pipeline


def test_ci_verify_passes_clean_packet_when_authority_denial_is_warning(tmp_path):
    result = run_pipeline(
        genome_path="examples/genomes/minimal_agent_genome.json",
        task_path="examples/tasks/memory_drift_task.json",
        run_id="ci_clean",
    )
    policy = AgentFoldPolicy(fail_on_authority_denial=False)
    ci = verify_for_ci(result.evidence_packet, policy)
    paths = write_ci_summary(ci, tmp_path)

    assert ci.passed is True
    assert paths["json"].exists()
    assert paths["markdown"].exists()
    assert "local policy validation only" in paths["markdown"].read_text(encoding="utf-8")


def test_ci_verify_fails_authority_denial_by_default():
    result = run_pipeline(
        genome_path="examples/genomes/minimal_agent_genome.json",
        task_path="examples/tasks/memory_drift_task.json",
        run_id="ci_authority_denial",
    )
    ci = verify_for_ci(result.evidence_packet)

    assert ci.passed is False
    assert any("authority_denial_present" in failure for failure in ci.failures)


def test_ci_verify_fails_blocked_phenotype():
    packet = FoldEvidencePacket(
        schema_version="1.0.0",
        packet_id="placeholder",
        run_id="blocked",
        agent_id="agent",
        genome_id="genome",
        genome_hash="g",
        origin_certificate_hash="o",
        transcriptome_hash="t",
        fold_graph_hash="fg",
        prediction_hash="p",
        fitness_hash="f",
        phenotype_hash="ph",
        certificate_hash="c",
        authority_hash="a",
        ledger_hash="l",
        artifacts={
            "phenotype": {"status": "blocked"},
            "misfolds": [{"severity": "critical"}],
            "authority_decisions": [],
        },
    )
    packet.packet_id = packet.compute_packet_id()
    assert verify_evidence_packet(packet)["valid"] is True

    ci = verify_for_ci(packet)
    assert ci.passed is False
    assert "phenotype_blocked" in ci.failures
    assert any("too_many_high_or_critical_misfolds" in failure for failure in ci.failures)


def test_cli_ci_verify_writes_summary(tmp_path):
    runner = CliRunner()
    run = run_pipeline(
        genome_path="examples/genomes/minimal_agent_genome.json",
        task_path="examples/tasks/memory_drift_task.json",
        run_id="ci_cli",
    )
    evidence_path = tmp_path / "packet.json"
    evidence_path.write_text(run.evidence_packet.model_dump_json(), encoding="utf-8")
    policy_path = tmp_path / "policy.json"
    policy_path.write_text(AgentFoldPolicy(fail_on_authority_denial=False).model_dump_json(), encoding="utf-8")
    summary_dir = tmp_path / "summary"

    result = runner.invoke(
        main,
        ["ci-verify", str(evidence_path), "--policy", str(policy_path), "--output-dir", str(summary_dir)],
    )

    assert result.exit_code == 0
    assert (summary_dir / "ci_summary.json").exists()
    assert (summary_dir / "ci_summary.md").exists()


def test_misfold_fixtures_are_declared():
    fixture_dir = Path("benchmarks/misfold_fixtures")
    fixtures = list(fixture_dir.glob("*.json"))
    assert len(fixtures) >= 8
    for fixture in fixtures:
        data = json.loads(fixture.read_text(encoding="utf-8"))
        assert data["fixture_id"]
        assert data["misfold_type"]
        assert data["expected_ci_result"] in {"fail", "warn", "pass"}


def test_default_policy_file_loads():
    policy = load_policy("agentfold.policy.json")
    assert policy.require_replay_valid is True
    assert policy.max_high_or_critical_misfolds == 0
