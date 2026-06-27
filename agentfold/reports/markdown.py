"""Markdown report rendering for AgentFold evidence packets."""

from __future__ import annotations

from pathlib import Path

from agentfold.evidence.packet import FoldEvidencePacket, verify_evidence_packet


def render_evidence_report(packet: FoldEvidencePacket) -> str:
    """Render a concise human-readable evidence report."""
    verification = verify_evidence_packet(packet)
    phenotype = packet.artifacts.get("phenotype", {})
    authority = packet.artifacts.get("authority_decisions", [])
    misfolds = packet.artifacts.get("misfolds", [])
    lines = [
        "# AgentFold Evidence Report",
        "",
        f"- Packet ID: `{packet.packet_id}`",
        f"- Run ID: `{packet.run_id}`",
        f"- Agent ID: `{packet.agent_id}`",
        f"- Genome ID: `{packet.genome_id}`",
        f"- Replay valid: `{verification['valid']}`",
        f"- Phenotype status: `{phenotype.get('status', 'unknown')}`",
        f"- Misfold count: `{len(misfolds)}`",
        f"- Authority decisions: `{len(authority)}`",
        "",
        "## Hash Surfaces",
        "",
        f"- genome: `{packet.genome_hash}`",
        f"- origin: `{packet.origin_certificate_hash}`",
        f"- transcriptome: `{packet.transcriptome_hash}`",
        f"- fold graph: `{packet.fold_graph_hash}`",
        f"- prediction: `{packet.prediction_hash}`",
        f"- fitness: `{packet.fitness_hash}`",
        f"- phenotype: `{packet.phenotype_hash}`",
        f"- certificate: `{packet.certificate_hash}`",
        f"- authority: `{packet.authority_hash}`",
        f"- ledger: `{packet.ledger_hash}`",
        "",
        "## Boundary",
        "",
        packet.claim_boundary,
        "",
        "This report is a local evidence summary. It is not production readiness, safety, security, AGI, consciousness, or biological equivalence proof.",
        "",
    ]
    if verification["failures"]:
        lines.extend(["## Replay Failures", ""])
        lines.extend(f"- {failure}" for failure in verification["failures"])
        lines.append("")
    return "\n".join(lines)


def write_evidence_report(packet: FoldEvidencePacket, path: str | Path) -> Path:
    """Write a Markdown evidence report."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_evidence_report(packet), encoding="utf-8")
    return output_path
