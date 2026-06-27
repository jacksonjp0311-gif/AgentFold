"""Transcriptome builder — convert events into AgentTranscriptome entries."""

from __future__ import annotations

from agentfold.expression.events import ExpressionEvent, ExpressionType
from agentfold.transcriptome.schema import (
    AgentTranscriptome,
    ClaimAllowedEntry,
    ClaimAttemptEntry,
    ClaimBlockedEntry,
    DriftEventEntry,
    GateEventEntry,
    MisfoldEventEntry,
    MemoryActivationEntry,
    RepairEventEntry,
    ToolActivationEntry,
)


def build_transcriptome(
    events: list[ExpressionEvent],
    *,
    run_id: str,
    genome_id: str,
    agent_id: str = "",
    origin_certificate_id: str = "",
) -> AgentTranscriptome:
    """Build a full AgentTranscriptome from a list of events."""
    claims_attempted: list[ClaimAttemptEntry] = []
    claims_allowed: list[ClaimAllowedEntry] = []
    claims_blocked: list[ClaimBlockedEntry] = []
    activated_genes: list[str] = []
    activated_memory: list[MemoryActivationEntry] = []
    activated_tools: list[ToolActivationEntry] = []
    gate_events: list[GateEventEntry] = []
    drift_events: list[DriftEventEntry] = []
    misfold_events: list[MisfoldEventEntry] = []
    repair_events: list[RepairEventEntry] = []
    evidence_used: set[str] = set()

    for ev in events:
        ref = ev.payload.get("gene_id") or ev.payload.get("memory_id") or ev.source
        if ev.expression_type == ExpressionType.PROMPT_GENE_ACTIVATION:
            activated_genes.append(ref)
        elif ev.expression_type == ExpressionType.MEMORY_ACTIVATION:
            activated_memory.append(MemoryActivationEntry(
                memory_id=ref,
                activation_reason=ev.payload.get("activation_reason", ""),
                relevance_score=ev.confidence,
            ))
        elif ev.expression_type in (ExpressionType.TOOL_INVOCATION, ExpressionType.TOOL_CONSIDERATION):
            activated_tools.append(ToolActivationEntry(
                tool_id=ref,
                tool_name=ev.payload.get("tool_name", ""),
                action=ev.payload.get("action", ""),
                result_summary=ev.payload.get("result_summary", ""),
            ))
        elif ev.expression_type == ExpressionType.CLAIM_ATTEMPT:
            outcome = ev.payload.get("outcome", "")
            entry = ClaimAttemptEntry(
                claim_id=ev.payload.get("claim_id", ""),
                claim_text=ev.payload.get("claim_text", ""),
                evidence_refs=ev.evidence_refs,
                outcome=outcome,
            )
            claims_attempted.append(entry)
            if outcome == "allowed":
                claims_allowed.append(ClaimAllowedEntry(
                    claim_id=entry.claim_id,
                    evidence_refs=entry.evidence_refs,
                ))
            elif outcome == "blocked":
                claims_blocked.append(ClaimBlockedEntry(
                    claim_id=entry.claim_id,
                    reason=ev.payload.get("reason", ""),
                ))
        elif ev.expression_type in (ExpressionType.GATE_PASS, ExpressionType.GATE_FAIL):
            gate_events.append(GateEventEntry(
                gate_id=ref,
                gate_type=ev.payload.get("gate_type", ""),
                passed=ev.expression_type == ExpressionType.GATE_PASS,
                reason=ev.payload.get("reason", ""),
            ))
        elif ev.expression_type == ExpressionType.DRIFT_WARNING:
            drift_events.append(DriftEventEntry(
                drift_type=ev.payload.get("drift_type", ""),
                severity=ev.payload.get("severity", "low"),
                description=ev.payload.get("description", ""),
            ))
        elif ev.expression_type == ExpressionType.MISFOLD_WARNING:
            misfold_events.append(MisfoldEventEntry(
                misfold_type=ev.payload.get("misfold_type", ""),
                severity=ev.payload.get("severity", "low"),
                description=ev.payload.get("description", ""),
                recommended_action=ev.payload.get("recommended_action", ""),
            ))
        elif ev.expression_type == ExpressionType.REPAIR_ATTEMPT:
            repair_events.append(RepairEventEntry(
                target_event_id=ev.payload.get("target_event_id", ""),
                repair_type=ev.payload.get("repair_type", ""),
                success=ev.payload.get("success", False),
            ))

        evidence_used.update(ev.evidence_refs)

    return AgentTranscriptome(
        run_id=run_id,
        agent_id=agent_id,
        genome_id=genome_id,
        origin_certificate_id=origin_certificate_id,
        activated_prompt_genes=activated_genes,
        activated_memory=activated_memory,
        activated_tools=activated_tools,
        claims_attempted=claims_attempted,
        claims_allowed=claims_allowed,
        claims_blocked=claims_blocked,
        evidence_used=sorted(evidence_used),
        gate_events=gate_events,
        drift_events=drift_events,
        misfold_events=misfold_events,
        repair_events=repair_events,
        claim_boundary="transcript_built_from_events",
    )
