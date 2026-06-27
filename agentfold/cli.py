"""AgentFold CLI — command-line interface for the folding architecture."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from agentfold import __version__, __architecture__, __non_claim__
from agentfold.genome.loader import load_genome
from agentfold.genome.validator import validate_genome
from agentfold.genome.hashing import hash_genome
from agentfold.origin.certificate import certify_origin
from agentfold.origin.alignment import check_alignment
from agentfold.benchmark.runner import BenchmarkRunner
from agentfold.benchmark.report import BenchmarkReport

console = Console()


def _banner():
    console.print(f"[bold pink]AgentFold[/] [cyan]{__version__}[/] — [dim]{__architecture__}[/]")
    console.print(f"[dim italic]{__non_claim__}[/]\n")


@click.group()
@click.version_option(version=__version__)
def main():
    """AgentFold — Sequence-to-Behavior Folding Architecture."""
    pass


@main.command("validate-genome")
@click.argument("genome_path", type=click.Path(exists=True))
def validate_genome_cmd(genome_path: str):
    """Validate an AgentGenome file."""
    _banner()
    genome = load_genome(genome_path)
    result = validate_genome(genome)

    if result.passed:
        console.print("[green]Genome validation PASSED[/]")
    else:
        console.print("[red]Genome validation FAILED[/]")

    if result.errors:
        console.print("\n[red]Errors:[/]")
        for e in result.errors:
            console.print(f"  {e}")

    if result.warnings:
        console.print("\n[yellow]Warnings:[/]")
        for w in result.warnings:
            console.print(f"  {w}")

    console.print(f"\nGenome hash: [cyan]{hash_genome(genome)}[/]")


@main.command("certify-origin")
@click.argument("genome_path", type=click.Path(exists=True))
def certify_origin_cmd(genome_path: str):
    """Certify origin alignment for a genome."""
    _banner()
    genome = load_genome(genome_path)
    cert = certify_origin(genome)
    alignment = check_alignment(genome, cert)

    status = "[green]ALIGNED[/]" if alignment.aligned else "[red]MISALIGNED[/]"
    console.print(f"Origin status: {status}")
    console.print(f"Certificate ID: [cyan]{cert.certificate_id}[/]")
    console.print(f"Origin ref: {cert.origin_ref}")

    if cert.reasons:
        console.print(f"\n[yellow]Reasons:[/]")
        for r in cert.reasons:
            console.print(f"  {r}")


@main.command("benchmark")
@click.option("--suite", default="basic", help="Benchmark suite to run")
def benchmark_cmd(suite: str):
    """Run the benchmark suite."""
    _banner()
    runner = BenchmarkRunner(suite=suite)
    report = BenchmarkReport(runner)

    table = Table(title=f"Benchmark Results — {suite}")
    table.add_column("Task ID", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")

    for row in report.to_table():
        status = "[green]PASS[/]" if row["passed"] == "PASS" else "[red]FAIL[/]"
        table.add_row(row["task_id"], status, row["details"])

    console.print(table)
    console.print()

    summary = runner.summary()
    console.print(f"[bold]Summary:[/] {summary['passed']}/{summary['total']} passed "
                  f"({summary['pass_rate']:.1%})")


@main.command("run")
@click.argument("genome_path", type=click.Path(exists=True))
@click.option("--task", "task_path", default=None, help="Optional task JSON path")
def run_cmd(genome_path: str, task_path: str | None):
    """Run the full AgentFold pipeline."""
    _banner()
    console.print("[bold]Loading genome...[/]")
    genome = load_genome(genome_path)
    console.print(f"  Genome ID: [cyan]{genome.genome_id}[/]")
    console.print(f"  Agent ID: [cyan]{genome.agent_id}[/]")
    console.print(f"  Version: [cyan]{genome.version}[/]")

    console.print("\n[bold]Validating genome...[/]")
    validation = validate_genome(genome)
    if not validation.passed:
        console.print("[red]Genome validation failed — aborting.[/]")
        for e in validation.errors:
            console.print(f"  {e}")
        sys.exit(1)
    console.print("[green]Genome valid[/]")

    console.print("\n[bold]Certifying origin...[/]")
    cert = certify_origin(genome)
    if not cert.passed:
        console.print("[red]Origin certification failed — no compounding allowed.[/]")
        for r in cert.reasons:
            console.print(f"  {r}")
        sys.exit(1)
    console.print(f"[green]Origin certified[/] — {cert.certificate_id}")

    console.print("\n[bold]Running benchmark suite...[/]")
    runner = BenchmarkRunner()
    results = runner.run_all()
    summary = runner.summary()
    console.print(f"  {summary['passed']}/{summary['total']} benchmarks passed")

    console.print("\n[bold pink]AgentFold v0.1.0 pipeline complete.[/]")
    console.print("[dim]No durable mutation performed — dry run only.[/]")


def main():
    """CLI entry point."""
    pass


if __name__ == "__main__":
    main()
