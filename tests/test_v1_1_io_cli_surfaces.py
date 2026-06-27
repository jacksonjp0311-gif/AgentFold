"""Tests for v1.1 persisted evidence, reports, schemas, and CLI surfaces."""

from click.testing import CliRunner

from agentfold.cli import main
from agentfold.evidence.packet import (
    diff_evidence_packets,
    read_evidence_packet,
    verify_evidence_packet,
    write_evidence_packet,
)
from agentfold.reports.markdown import render_evidence_report, write_evidence_report
from agentfold.runtime.pipeline import run_pipeline
from agentfold.schemas.export import CORE_SCHEMA_MODELS, export_core_schemas


def test_evidence_packet_roundtrip_and_diff(tmp_path):
    result = run_pipeline(
        genome_path="examples/genomes/minimal_agent_genome.json",
        task_path="examples/tasks/memory_drift_task.json",
        run_id="test_v1_1_roundtrip",
    )
    path = tmp_path / "evidence.json"
    write_evidence_packet(result.evidence_packet, path)
    loaded = read_evidence_packet(path)
    replay = verify_evidence_packet(loaded)
    diff = diff_evidence_packets(result.evidence_packet, loaded)

    assert loaded.packet_id == result.evidence_packet.packet_id
    assert replay["valid"] is True
    assert diff["changed_fields"] == []


def test_markdown_report_contains_boundary(tmp_path):
    result = run_pipeline(
        genome_path="examples/genomes/minimal_agent_genome.json",
        task_path="examples/tasks/memory_drift_task.json",
        run_id="test_v1_1_report",
    )
    report = render_evidence_report(result.evidence_packet)
    path = write_evidence_report(result.evidence_packet, tmp_path / "report.md")

    assert "AgentFold Evidence Report" in report
    assert "not production readiness" in report
    assert path.exists()


def test_schema_export_writes_core_schemas(tmp_path):
    written = export_core_schemas(tmp_path)
    names = {path.name for path in written}

    assert len(written) == len(CORE_SCHEMA_MODELS)
    assert "fold_evidence_packet.schema.json" in names
    assert "agent_phenotype.schema.json" in names
    assert "authority_matrix.schema.json" in names


def test_cli_run_replay_report_and_schema_export(tmp_path):
    runner = CliRunner()
    output_dir = tmp_path / "out"
    run = runner.invoke(
        main,
        [
            "run",
            "examples/genomes/minimal_agent_genome.json",
            "--task",
            "examples/tasks/memory_drift_task.json",
            "--run-id",
            "cli_v1_1",
            "--output-dir",
            str(output_dir),
        ],
    )
    evidence_path = output_dir / "evidence" / "cli_v1_1.evidence.json"
    report_path = output_dir / "reports" / "cli_v1_1.report.md"

    assert run.exit_code == 0
    assert evidence_path.exists()
    assert report_path.exists()

    replay = runner.invoke(main, ["replay", str(evidence_path)])
    assert replay.exit_code == 0
    assert "Replay status" in replay.output
    assert "VALID" in replay.output

    rendered = tmp_path / "rendered.md"
    report = runner.invoke(main, ["report", str(evidence_path), str(rendered)])
    assert report.exit_code == 0
    assert rendered.exists()

    schemas = tmp_path / "schemas"
    export = runner.invoke(main, ["export-schemas", str(schemas)])
    assert export.exit_code == 0
    assert (schemas / "fold_evidence_packet.schema.json").exists()
