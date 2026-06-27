"""AgentFold command-line interface."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from agentfold import __architecture__, __non_claim__, __version__
from agentfold.benchmark.report import BenchmarkReport
from agentfold.benchmark.runner import BenchmarkRunner
from agentfold.ci.policy import load_policy
from agentfold.ci.verify import verify_for_ci, write_ci_summary
from agentfold.evidence.packet import (
    diff_evidence_packets,
    read_evidence_packet,
    verify_evidence_packet,
    write_evidence_packet,
)
from agentfold.genome.hashing import hash_genome
from agentfold.genome.loader import load_genome
from agentfold.genome.validator import validate_genome
from agentfold.instrumentation.session import AgentFoldSession
from agentfold.origin.alignment import check_alignment
from agentfold.origin.certificate import certify_origin
from agentfold.reports.markdown import write_evidence_report
from agentfold.release.validator import validate_release, write_release_validation
from agentfold.runtime.pipeline import run_pipeline
from agentfold.schemas.export import export_core_schemas


console = Console()


def _banner() -> None:
    console.print(f"[bold pink]AgentFold[/] [cyan]{__version__}[/] - [dim]{__architecture__}[/]")
    console.print(f"[dim italic]{__non_claim__}[/]\n")


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """AgentFold - Sequence-to-Behavior Folding Architecture."""


@main.command("validate-genome")
@click.argument("genome_path", type=click.Path(exists=True))
def validate_genome_cmd(genome_path: str) -> None:
    """Validate an AgentGenome file."""
    _banner()
    genome = load_genome(genome_path)
    result = validate_genome(genome)

    console.print("[green]Genome validation PASSED[/]" if result.passed else "[red]Genome validation FAILED[/]")
    for error in result.errors:
        console.print(f"  [red]{error}[/]")
    for warning in result.warnings:
        console.print(f"  [yellow]{warning}[/]")

    console.print(f"\nGenome hash: [cyan]{hash_genome(genome)}[/]")


@main.command("certify-origin")
@click.argument("genome_path", type=click.Path(exists=True))
def certify_origin_cmd(genome_path: str) -> None:
    """Certify origin alignment for a genome."""
    _banner()
    genome = load_genome(genome_path)
    cert = certify_origin(genome)
    alignment = check_alignment(genome, cert)

    status = "[green]ALIGNED[/]" if alignment.aligned else "[red]MISALIGNED[/]"
    console.print(f"Origin status: {status}")
    console.print(f"Certificate ID: [cyan]{cert.certificate_id}[/]")
    console.print(f"Origin ref: {cert.origin_ref}")
    for reason in cert.reasons:
        console.print(f"  [yellow]{reason}[/]")


@main.command("benchmark")
@click.option("--suite", default="basic", help="Benchmark suite to run")
def benchmark_cmd(suite: str) -> None:
    """Run the benchmark suite."""
    _banner()
    runner = BenchmarkRunner(suite=suite)
    report = BenchmarkReport(runner)

    table = Table(title=f"Benchmark Results - {suite}")
    table.add_column("Task ID", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")

    for row in report.to_table():
        status = "[green]PASS[/]" if row["passed"] == "PASS" else "[red]FAIL[/]"
        table.add_row(row["task_id"], status, row["details"])

    console.print(table)
    summary = runner.summary()
    console.print(f"[bold]Summary:[/] {summary['passed']}/{summary['total']} passed ({summary['pass_rate']:.1%})")


@main.command("run")
@click.argument("genome_path", type=click.Path(exists=True))
@click.option("--task", "task_path", default=None, help="Optional task JSON path")
@click.option("--run-id", default="agentfold_cli_run", help="Deterministic run identity")
@click.option("--output-dir", default=None, help="Write evidence/report artifacts to this directory")
def run_cmd(genome_path: str, task_path: str | None, run_id: str, output_dir: str | None) -> None:
    """Run the full local AgentFold pipeline."""
    _banner()
    result = run_pipeline(genome_path=genome_path, task_path=task_path, run_id=run_id)
    console.print(f"Run ID: [cyan]{result.run_id}[/]")
    console.print(f"Genome valid: [cyan]{result.genome_valid}[/]")
    console.print(f"Origin aligned: [cyan]{result.origin_aligned}[/]")
    console.print(f"Compounding decision: [cyan]{result.compounding_decision}[/]")
    console.print(f"Phenotype: [cyan]{result.phenotype.status}[/]")
    console.print(f"Evidence packet: [cyan]{result.evidence_packet.packet_id}[/]")

    if output_dir:
        out = Path(output_dir)
        packet_path = out / "evidence" / f"{result.run_id}.evidence.json"
        report_path = out / "reports" / f"{result.run_id}.report.md"
        write_evidence_packet(result.evidence_packet, packet_path)
        write_evidence_report(result.evidence_packet, report_path)
        console.print(f"Evidence written: [cyan]{packet_path}[/]")
        console.print(f"Report written: [cyan]{report_path}[/]")

    console.print(f"\n[bold pink]AgentFold {__version__} pipeline complete.[/]")
    console.print("[dim]Local evidence only - not production certification.[/]")


@main.command("replay")
@click.argument("evidence_path", type=click.Path(exists=True))
def replay_cmd(evidence_path: str) -> None:
    """Replay-verify a saved evidence packet."""
    _banner()
    packet = read_evidence_packet(evidence_path)
    result = verify_evidence_packet(packet)
    status = "[green]VALID[/]" if result["valid"] else "[red]INVALID[/]"
    console.print(f"Replay status: {status}")
    console.print(f"Packet ID: [cyan]{result['packet_id']}[/]")
    for failure in result["failures"]:
        console.print(f"  [red]{failure}[/]")


@main.command("ci-verify")
@click.argument("evidence_path", type=click.Path(exists=True))
@click.option("--policy", "policy_path", default=None, type=click.Path(exists=True), help="Optional policy JSON path")
@click.option("--output-dir", default=None, type=click.Path(), help="Optional directory for CI summary JSON/MD")
def ci_verify_cmd(evidence_path: str, policy_path: str | None, output_dir: str | None) -> None:
    """Verify an evidence packet against CI policy."""
    _banner()
    packet = read_evidence_packet(evidence_path)
    result = verify_for_ci(packet, load_policy(policy_path))
    status = "[green]PASS[/]" if result.passed else "[red]FAIL[/]"
    console.print(f"CI status: {status}")
    console.print(f"Packet ID: [cyan]{result.packet_id}[/]")
    for failure in result.failures:
        console.print(f"  [red]{failure}[/]")
    for warning in result.warnings:
        console.print(f"  [yellow]{warning}[/]")
    if output_dir:
        paths = write_ci_summary(result, output_dir)
        console.print(f"CI JSON: [cyan]{paths['json']}[/]")
        console.print(f"CI MD: [cyan]{paths['markdown']}[/]")
    if not result.passed:
        raise click.ClickException("AgentFold CI verification failed")


@main.command("diff-runs")
@click.argument("left_evidence", type=click.Path(exists=True))
@click.argument("right_evidence", type=click.Path(exists=True))
def diff_runs_cmd(left_evidence: str, right_evidence: str) -> None:
    """Diff two evidence packets by hash surfaces."""
    _banner()
    diff = diff_evidence_packets(read_evidence_packet(left_evidence), read_evidence_packet(right_evidence))
    console.print(f"Left: [cyan]{diff['left_packet_id']}[/]")
    console.print(f"Right: [cyan]{diff['right_packet_id']}[/]")
    console.print(f"Same run id: [cyan]{diff['same_run_id']}[/]")
    if diff["changed_fields"]:
        console.print("[yellow]Changed fields:[/]")
        for field in diff["changed_fields"]:
            console.print(f"  {field}")
    else:
        console.print("[green]No hash-surface changes detected[/]")


@main.command("report")
@click.argument("evidence_path", type=click.Path(exists=True))
@click.argument("report_path", type=click.Path())
def report_cmd(evidence_path: str, report_path: str) -> None:
    """Render a Markdown report from an evidence packet."""
    _banner()
    path = write_evidence_report(read_evidence_packet(evidence_path), report_path)
    console.print(f"Report written: [cyan]{path}[/]")


@main.command("export-schemas")
@click.argument("output_dir", type=click.Path())
def export_schemas_cmd(output_dir: str) -> None:
    """Export JSON Schemas for core AgentFold artifacts."""
    _banner()
    paths = export_core_schemas(output_dir)
    console.print(f"Exported [cyan]{len(paths)}[/] schemas to [cyan]{output_dir}[/]")


@main.command("start-session")
@click.option("--run-id", required=True, help="Session run identity")
@click.option("--genome-id", required=True, help="Genome identifier")
@click.option("--agent-id", default="", help="Agent identifier")
@click.option("--output", required=True, type=click.Path(), help="Path to write session JSON")
def start_session_cmd(run_id: str, genome_id: str, agent_id: str, output: str) -> None:
    """Create an empty instrumented session file."""
    _banner()
    session = AgentFoldSession(run_id=run_id, genome_id=genome_id, agent_id=agent_id)
    path = session.write_session(output)
    console.print(f"Session written: [cyan]{path}[/]")


@main.command("record-event")
@click.argument("session_path", type=click.Path(exists=True))
@click.option("--type", "event_type", required=True, type=click.Choice(["prompt", "memory", "tool", "claim", "evidence", "gate", "output"]))
@click.option("--id", "item_id", required=True, help="Event item identifier")
@click.option("--text", default="", help="Claim text, action, reason, or source text")
@click.option("--outcome", default="allowed", help="Claim outcome")
@click.option("--passed/--failed", default=True, help="Gate result")
def record_event_cmd(session_path: str, event_type: str, item_id: str, text: str, outcome: str, passed: bool) -> None:
    """Append a simple event to a session file."""
    _banner()
    session = AgentFoldSession.read_session(session_path)
    if event_type == "prompt":
        session.record_prompt(item_id)
    elif event_type == "memory":
        session.record_memory(item_id, reason=text)
    elif event_type == "tool":
        session.record_tool_call(item_id, tool_name=item_id, action=text)
    elif event_type == "claim":
        session.record_claim(item_id, text or item_id, outcome=outcome)
    elif event_type == "evidence":
        session.record_evidence(item_id, source=text)
    elif event_type == "gate":
        session.record_gate(item_id, gate_type=text or "manual", passed=passed)
    elif event_type == "output":
        session.record_output(item_id)
    session.write_session(session_path)
    console.print(f"Recorded event: [cyan]{event_type}:{item_id}[/]")


@main.command("close-session")
@click.argument("session_path", type=click.Path(exists=True))
@click.argument("transcriptome_path", type=click.Path())
def close_session_cmd(session_path: str, transcriptome_path: str) -> None:
    """Build a transcriptome from a session file."""
    _banner()
    session = AgentFoldSession.read_session(session_path)
    transcriptome = session.build_transcriptome()
    path = Path(transcriptome_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(transcriptome.model_dump_json(indent=2) + "\n", encoding="utf-8")
    console.print(f"Transcriptome written: [cyan]{path}[/]")


@main.command("release-validate")
@click.option("--output-dir", default="reports/release", type=click.Path(), help="Directory for release validation artifacts")
@click.option("--run-tests/--skip-tests", default=False, help="Run pytest inside release validation")
def release_validate_cmd(output_dir: str, run_tests: bool) -> None:
    """Run local release validation and write release reports."""
    _banner()
    result = validate_release(".", run_tests=run_tests)
    paths = write_release_validation(result, output_dir)
    status = "[green]PASS[/]" if result.passed else "[red]FAIL[/]"
    console.print(f"Release validation: {status}")
    for failure in result.failures:
        console.print(f"  [red]{failure}[/]")
    console.print(f"Release JSON: [cyan]{paths['json']}[/]")
    console.print(f"Release MD: [cyan]{paths['markdown']}[/]")
    if not result.passed:
        raise click.ClickException("AgentFold release validation failed")


if __name__ == "__main__":
    main()
