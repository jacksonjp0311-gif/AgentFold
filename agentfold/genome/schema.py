"""AgentFold v0.1.0 — AgentGenome schema definitions.

An AgentGenome is the encoded operational substrate from which an agent
can express runtime behavior. It is NOT the agent's behavior.
It is the encoded possibility space.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


# ── Enumerations ──────────────────────────────────────────────────────────────

class PromptGeneType(str, Enum):
    ROLE = "role"
    TASK_POLICY = "task_policy"
    MEMORY_POLICY = "memory_policy"
    TOOL_POLICY = "tool_policy"
    CLAIM_POLICY = "claim_policy"
    REFUSAL_POLICY = "refusal_policy"
    EVIDENCE_POLICY = "evidence_policy"
    STYLE_POLICY = "style_policy"
    SAFETY_POLICY = "safety_policy"


class ToolType(str, Enum):
    READ_ONLY = "read_only"
    WRITE_LIMITED = "write_limited"
    WRITE_DURABLE = "write_durable"
    EXTERNAL_API = "external_api"
    COMMUNICATION = "communication"
    FILESYSTEM = "filesystem"
    CALENDAR = "calendar"
    EMAIL = "email"
    REPOSITORY = "repository"
    PAYMENT = "payment"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ── Leaf schemas ──────────────────────────────────────────────────────────────

class PromptGene(BaseModel):
    """A reusable prompt instruction, role segment, behavioral constraint,
    tool instruction, or memory routing rule."""

    gene_id: str
    gene_type: PromptGeneType
    content: str
    activation_condition: str = ""
    allowed_contexts: list[str] = Field(default_factory=list)
    denied_contexts: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    claim_boundary: str = "diagnostic"


class ToolSpec(BaseModel):
    """Specification for a single tool available to the agent."""

    tool_id: str
    tool_name: str
    tool_type: ToolType
    allowed_actions: list[str] = Field(default_factory=list)
    denied_actions: list[str] = Field(default_factory=list)
    requires_human_confirmation: bool = False
    requires_gate: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    nonclaim_boundary: str = "tool_spec_read_only"


class PermissionSpec(BaseModel):
    """Explicit permission for a tool or mutation surface."""

    permission_id: str
    surface: str
    allowed: list[str] = Field(default_factory=list)
    denied: list[str] = Field(default_factory=list)
    requires_gate: list[str] = Field(default_factory=list)
    requires_human_authorization: bool = False
    expires_at: Optional[str] = None
    claim_boundary: str = "permission_declared"


class ConstraintSpec(BaseModel):
    """Runtime constraint governing agent behavior."""

    constraint_id: str
    constraint_type: str = ""
    description: str = ""
    parameters: dict[str, Any] = Field(default_factory=dict)
    enforcement: str = "hard"


class EvidenceRef(BaseModel):
    """Reference to an evidence item supporting a claim."""

    evidence_id: str
    source: str = ""
    evidence_type: str = ""
    confidence: float = 0.0
    claim_boundary: str = "evidence_or_downgrade"


class FailureMode(BaseModel):
    """Known failure mode for this agent genome."""

    failure_id: str
    failure_type: str = ""
    description: str = ""
    mitigation: str = ""
    claim_boundary: str = "known_failure_mode"


class LineageRef(BaseModel):
    """Reference to a prior genome, ledger entry, or evolution step."""

    lineage_id: str
    reference_type: str = ""
    reference_hash: str = ""
    timestamp: str = ""
    claim_boundary: str = "lineage_reference"


# ── Root schema ───────────────────────────────────────────────────────────────

class AgentGenome(BaseModel):
    """AgentGenome — the encoded operational substrate.

    G_A does NOT imply P_A. Behavior requires expression.
    """

    genome_id: str
    agent_id: str
    version: str = "0.1.0"
    origin_ref: str = ""
    origin_hash: str = ""
    prompt_genome: list[PromptGene] = Field(default_factory=list)
    memory_schema: dict[str, Any] = Field(default_factory=dict)
    tool_manifest: list[ToolSpec] = Field(default_factory=list)
    permission_manifest: list[PermissionSpec] = Field(default_factory=list)
    constraint_manifest: list[ConstraintSpec] = Field(default_factory=list)
    claim_ceiling: str = "diagnostic"
    evidence_index: list[EvidenceRef] = Field(default_factory=list)
    known_failure_modes: list[FailureMode] = Field(default_factory=list)
    lineage: list[LineageRef] = Field(default_factory=list)
    nonclaim_boundary: str = (
        "AgentFold does not claim biological equivalence, AGI, consciousness, "
        "safety, security, production readiness, or autonomous authority."
    )

    def tool_ids(self) -> set[str]:
        return {t.tool_id for t in self.tool_manifest}

    def prompt_gene_ids(self) -> set[str]:
        return {g.gene_id for g in self.prompt_genome}

    def evidence_ids(self) -> set[str]:
        return {e.evidence_id for e in self.evidence_index}
