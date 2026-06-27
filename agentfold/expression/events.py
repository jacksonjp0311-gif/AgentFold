"""RuntimeExpression events — atomic units of transcriptomics."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class ExpressionType(str, Enum):
    PROMPT_GENE_ACTIVATION = "prompt_gene_activation"
    MEMORY_ACTIVATION = "memory_activation"
    TOOL_CONSIDERATION = "tool_consideration"
    TOOL_INVOCATION = "tool_invocation"
    CLAIM_ATTEMPT = "claim_attempt"
    CLAIM_DOWNGRADE = "claim_downgrade"
    CLAIM_BLOCK = "claim_block"
    EVIDENCE_LOOKUP = "evidence_lookup"
    GATE_PASS = "gate_pass"
    GATE_FAIL = "gate_fail"
    DRIFT_WARNING = "drift_warning"
    MISFOLD_WARNING = "misfold_warning"
    REPAIR_ATTEMPT = "repair_attempt"
    OUTPUT_COMMIT = "output_commit"


class ExpressionEvent(BaseModel):
    """Base runtime expression event."""

    event_id: str = ""
    run_id: str = ""
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    expression_type: ExpressionType = ExpressionType.PROMPT_GENE_ACTIVATION
    source: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    evidence_refs: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    claim_boundary: str = "runtime_expression_recorded"


class MemoryActivation(BaseModel):
    """Record of a memory fragment being activated."""

    memory_id: str = ""
    activation_reason: str = ""
    relevance_score: float = 0.0
    claim_boundary: str = "memory_activation_recorded"


class ToolActivation(BaseModel):
    """Record of a tool being invoked."""

    tool_id: str = ""
    tool_name: str = ""
    action: str = ""
    parameters: dict[str, Any] = Field(default_factory=dict)
    result_summary: str = ""
    claim_boundary: str = "tool_invocation_recorded"


class ToolConsideration(BaseModel):
    """Record of a tool being considered but not invoked."""

    tool_id: str = ""
    reason_not_invoked: str = ""
    claim_boundary: str = "tool_consideration_recorded"


class ClaimAttempt(BaseModel):
    """Record of a claim being attempted."""

    claim_id: str = ""
    claim_text: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
    ceiling: str = "diagnostic"
    outcome: str = ""  # allowed | downgraded | blocked
    claim_boundary: str = "claim_attempt_recorded"


class GateEvent(BaseModel):
    """Record of a gate evaluation."""

    gate_id: str = ""
    gate_type: str = ""
    passed: bool = False
    reason: str = ""
    claim_boundary: str = "gate_event_recorded"


class DriftEvent(BaseModel):
    """Record of drift detection."""

    drift_type: str = ""
    severity: str = "low"
    description: str = ""
    claim_boundary: str = "drift_event_recorded"


class MisfoldWarning(BaseModel):
    """Record of a misfold warning."""

    misfold_type: str = ""
    severity: str = "low"
    description: str = ""
    recommended_action: str = ""
    claim_boundary: str = "misfold_warning_recorded"


class RepairEvent(BaseModel):
    """Record of a repair attempt."""

    target_event_id: str = ""
    repair_type: str = ""
    success: bool = False
    claim_boundary: str = "repair_event_recorded"
