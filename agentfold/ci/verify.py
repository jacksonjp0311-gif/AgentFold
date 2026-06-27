"""CI verification for AgentFold evidence packets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from agentfold.ci.policy import AgentFoldPolicy
from agentfold.evidence.packet import FoldEvidencePacket, verify_evidence_packet


class CIVerificationResult(BaseModel):
    passed: bool
    packet_id: str
    failures: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    claim_boundary: str = "ci_verification_not_production_safety_proof"

    def to_markdown(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [
            "# AgentFold CI Summary",
            "",
            f"- Status: `{status}`",
            f"- Packet ID: `{self.packet_id}`",
            f"- Boundary: `{self.claim_boundary}`",
            "",
        ]
        if self.failures:
            lines.extend(["## Failures", ""])
            lines.extend(f"- {failure}" for failure in self.failures)
            lines.append("")
        if self.warnings:
            lines.extend(["## Warnings", ""])
            lines.extend(f"- {warning}" for warning in self.warnings)
            lines.append("")
        lines.extend([
            "## Non-Claim Lock",
            "",
            "This CI result is local policy validation only. It is not production readiness, safety, security, AGI, consciousness, biological equivalence, or autonomous authority proof.",
            "",
        ])
        return "\n".join(lines)


def _severity_value(misfold: dict[str, Any]) -> str:
    severity = misfold.get("severity", "")
    if isinstance(severity, str):
        return severity.split(".")[-1].lower()
    return str(severity).lower()


def verify_for_ci(packet: FoldEvidencePacket, policy: AgentFoldPolicy | None = None) -> CIVerificationResult:
    """Verify an evidence packet against CI policy."""
    policy = policy or AgentFoldPolicy()
    failures: list[str] = []
    warnings: list[str] = []
    replay = verify_evidence_packet(packet)

    if policy.require_replay_valid and not replay["valid"]:
        failures.extend([f"replay_invalid: {failure}" for failure in replay["failures"]])

    if policy.require_schema_version and packet.schema_version != policy.require_schema_version:
        failures.append(f"schema_version_mismatch: expected {policy.require_schema_version}, got {packet.schema_version}")

    if policy.require_ledger_hash and not packet.ledger_hash:
        failures.append("missing_ledger_hash")

    phenotype = packet.artifacts.get("phenotype", {})
    if policy.require_phenotype_not_blocked and str(phenotype.get("status", "")).endswith("blocked"):
        failures.append("phenotype_blocked")

    misfolds = packet.artifacts.get("misfolds", [])
    severe_count = sum(1 for misfold in misfolds if _severity_value(misfold) in {"high", "critical"})
    if severe_count > policy.max_high_or_critical_misfolds:
        failures.append(f"too_many_high_or_critical_misfolds: {severe_count}")

    authority = packet.artifacts.get("authority_decisions", [])
    denied = [decision for decision in authority if decision.get("blocked") is True or decision.get("passed") is False]
    if denied and policy.fail_on_authority_denial:
        failures.append(f"authority_denial_present: {len(denied)}")
    elif denied:
        warnings.append(f"authority_denial_present: {len(denied)}")

    return CIVerificationResult(
        passed=not failures,
        packet_id=packet.packet_id,
        failures=failures,
        warnings=warnings,
    )


def write_ci_summary(result: CIVerificationResult, output_dir: str | Path) -> dict[str, Path]:
    """Write CI summary JSON and Markdown."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "ci_summary.json"
    md_path = out / "ci_summary.md"
    json_path.write_text(json.dumps(result.model_dump(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(result.to_markdown(), encoding="utf-8")
    return {"json": json_path, "markdown": md_path}
