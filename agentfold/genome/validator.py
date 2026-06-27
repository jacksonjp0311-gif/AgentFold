"""AgentGenome validation — Genome Gate checks."""

from __future__ import annotations

from agentfold.genome.schema import AgentGenome, RiskLevel, ToolType


class GenomeValidationResult:
    """Result of genome validation."""

    def __init__(self):
        self.passed: bool = True
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def fail(self, msg: str):
        self.passed = False
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def validate_genome(genome: AgentGenome) -> GenomeValidationResult:
    """Validate an AgentGenome against the schema and governance rules."""
    result = GenomeValidationResult()

    # Required identifiers
    if not genome.genome_id:
        result.fail("genome_id is required")
    if not genome.agent_id:
        result.fail("agent_id is required")

    # Claim ceiling declared
    if not genome.claim_ceiling:
        result.fail("claim_ceiling must be declared")

    # Tool manifest checks
    for tool in genome.tool_manifest:
        if tool.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            if not tool.requires_gate:
                result.warn(
                    f"Tool {tool.tool_id} has risk_level={tool.risk_level} "
                    "but no gates declared"
                )
        if tool.tool_type in (ToolType.PAYMENT, ToolType.COMMUNICATION):
            if not tool.requires_human_confirmation:
                result.warn(
                    f"Tool {tool.tool_id} type={tool.tool_type} should require "
                    "human confirmation"
                )

    # Permission manifest checks
    for perm in genome.permission_manifest:
        if not perm.surface:
            result.fail(f"Permission {perm.permission_id} missing surface")

    # Evidence index non-empty for compounding genomes
    if genome.claim_ceiling not in ("diagnostic", "") and not genome.evidence_index:
        result.warn(
            "Genome claim_ceiling allows elevated claims but evidence_index is empty"
        )

    return result
