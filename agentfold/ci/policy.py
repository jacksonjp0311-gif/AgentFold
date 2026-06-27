"""AgentFold CI policy."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel


class AgentFoldPolicy(BaseModel):
    require_replay_valid: bool = True
    max_high_or_critical_misfolds: int = 0
    require_phenotype_not_blocked: bool = True
    require_ledger_hash: bool = True
    require_schema_version: str = "1.0.0"
    fail_on_authority_denial: bool = True
    claim_boundary: str = "ci_policy_local_gate_only"


def load_policy(path: str | Path | None = None) -> AgentFoldPolicy:
    """Load policy from JSON or return defaults."""
    if path is None:
        default_path = Path("agentfold.policy.json")
        if not default_path.exists():
            return AgentFoldPolicy()
        path = default_path
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    return AgentFoldPolicy(**data)
