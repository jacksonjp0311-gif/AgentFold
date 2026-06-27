"""Genome Gate — AgentGenome must be present, parseable, and hashable."""

from __future__ import annotations

from agentfold.genome.schema import AgentGenome
from agentfold.genome.validator import GenomeValidationResult, validate_genome


def check(genome: AgentGenome | None) -> "GateResult":
    from agentfold.gates.origin_gate import GateResult

    if genome is None:
        return GateResult(passed=False, reason="genome_missing", details={})

    result: GenomeValidationResult = validate_genome(genome)
    if not result.passed:
        return GateResult(
            passed=False,
            reason="genome_validation_failed",
            details={"errors": result.errors, "warnings": result.warnings},
        )

    return GateResult(
        passed=True,
        reason="genome_valid",
        details={"genome_id": genome.genome_id, "warnings": result.warnings},
    )
