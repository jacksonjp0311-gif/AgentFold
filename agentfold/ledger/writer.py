"""LedgerWriter — append-only JSONL ledger."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class LedgerEntry(BaseModel):
    """AgentFoldLedgerEntry — single append-only artifact record."""

    ledger_id: str = ""
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    run_id: str = ""
    agent_id: str = ""
    genome_hash: str = ""
    origin_certificate_hash: str = ""
    transcriptome_hash: str = ""
    fold_graph_hash: str = ""
    prediction_hash: str = ""
    misfold_hashes: list[str] = Field(default_factory=list)
    fitness_hash: str = ""
    compounding_decision_hash: str = ""
    fold_certificate_hash: str = ""
    previous_ledger_hash: str = ""
    entry_hash: str = ""
    claim_boundary: str = "ledger_entry_recorded"

    def compute_hash(self) -> str:
        """Compute hash from all fields except entry_hash itself."""
        import hashlib
        data = self.model_dump_json(
            sort_keys=True,
            exclude={"entry_hash"},
        )
        return hashlib.sha256(data.encode("utf-8")).hexdigest()[:32]


class LedgerWriter:
    """Append-only ledger writer."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._last_hash = ""

    def write(self, entry: LedgerEntry) -> LedgerEntry:
        """Append a ledger entry with hashchain linkage."""
        entry.previous_ledger_hash = self._last_hash
        entry.entry_hash = entry.compute_hash()

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")

        self._last_hash = entry.entry_hash
        return entry


def append_entry(
    path: str | Path,
    data: dict[str, Any],
    *,
    run_id: str = "",
    agent_id: str = "",
) -> LedgerEntry:
    """Convenience: append a ledger entry from a dict."""
    writer = LedgerWriter(path)
    entry = LedgerEntry(
        ledger_id=f"le_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        run_id=run_id,
        agent_id=agent_id,
        **data,
    )
    return writer.write(entry)
