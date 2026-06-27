"""AgentTranscriptome schema — complete runtime expression trace."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MemoryActivationEntry(BaseModel):
    memory_id: str = ""
    activation_reason: str = ""
    relevance_score: float = 0.0


class ToolActivationEntry(BaseModel):
    tool_id: str = ""
    tool_name: str = ""
    action: str = ""
    parameters: dict = Field(default_factory=dict)
    result_summary: str = ""


class ClaimAttemptEntry(BaseModel):
    claim_id: str = ""
    claim_text: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
    outcome: str = ""  # allowed | downgraded | blocked


class ClaimAllowedEntry(BaseModel):
    claim_id: str = ""
    evidence_refs: list[str] = Field(default_factory=list)


class ClaimBlockedEntry(BaseModel):
    claim_id: str = ""
    reason: str = ""


class GateEventEntry(BaseModel):
    gate_id: str = ""
    gate_type: str = ""
    passed: bool = False
    reason: str = ""


class DriftEventEntry(BaseModel):
    drift_type: str = ""
    severity: str = "low"
    description: str = ""


class MisfoldEventEntry(BaseModel):
    misfold_type: str = ""
    severity: str = "low"
    description: str = ""
    recommended_action: str = ""


class RepairEventEntry(BaseModel):
    target_event_id: str = ""
    repair_type: str = ""
    success: bool = False


class AgentTranscriptome(BaseModel):
    """AgentTranscriptome — complete runtime expression trace.

    Answers: "What actually expressed during the run?"
    """

    transcriptome_id: str = ""
    run_id: str = ""
    agent_id: str = ""
    genome_id: str = ""
    origin_certificate_id: str = ""
    activated_prompt_genes: list[str] = Field(default_factory=list)
    activated_memory: list[MemoryActivationEntry] = Field(default_factory=list)
    activated_tools: list[ToolActivationEntry] = Field(default_factory=list)
    claims_attempted: list[ClaimAttemptEntry] = Field(default_factory=list)
    claims_allowed: list[ClaimAllowedEntry] = Field(default_factory=list)
    claims_blocked: list[ClaimBlockedEntry] = Field(default_factory=list)
    evidence_used: list[str] = Field(default_factory=list)
    gate_events: list[GateEventEntry] = Field(default_factory=list)
    drift_events: list[DriftEventEntry] = Field(default_factory=list)
    misfold_events: list[MisfoldEventEntry] = Field(default_factory=list)
    repair_events: list[RepairEventEntry] = Field(default_factory=list)
    final_output_hash: str = ""
    ledger_hash: str = ""
    claim_boundary: str = "transcriptome_recorded"
