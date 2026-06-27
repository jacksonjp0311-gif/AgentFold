"""ValidatedDelta — a delta that has passed inheritance validation."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class DeltaType(str, Enum):
    MEMORY_UPDATE = "memory_update"
    PROMPT_GENE_UPDATE = "prompt_gene_update"
    TOOL_POLICY_UPDATE = "tool_policy_update"
    CLAIM_CEILING_UPDATE = "claim_ceiling_update"
    EVIDENCE_INDEX_UPDATE = "evidence_index_update"
    FAILURE_MODE_UPDATE = "failure_mode_update"
    BENCHMARK_UPDATE = "benchmark_update"
    DOCUMENTATION_UPDATE = "documentation_update"


class ValidatedDelta(BaseModel):
    """A delta from a run that has been validated for inheritance."""

    delta_id: str = ""
    source_run_id: str = ""
    source_certificate_id: str = ""
    delta_type: DeltaType | str = DeltaType.MEMORY_UPDATE
    allowed: bool = False
    reason: str = ""
    requires_human_review: bool = False
    ledger_hash: str = ""
    claim_boundary: str = "delta_not_inheritance_without_validation"
