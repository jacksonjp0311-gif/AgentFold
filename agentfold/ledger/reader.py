"""LedgerReader — read and query the append-only ledger."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agentfold.ledger.writer import LedgerEntry


class LedgerReader:
    """Read entries from a JSONL ledger file."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def read_all(self) -> list[LedgerEntry]:
        """Read all ledger entries."""
        if not self.path.exists():
            return []

        entries = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                entries.append(LedgerEntry(**data))
        return entries

    def read_by_run(self, run_id: str) -> list[LedgerEntry]:
        """Read entries for a specific run."""
        return [e for e in self.read_all() if e.run_id == run_id]

    def read_by_agent(self, agent_id: str) -> list[LedgerEntry]:
        """Read entries for a specific agent."""
        return [e for e in self.read_all() if e.agent_id == agent_id]

    @property
    def entry_count(self) -> int:
        return len(self.read_all())

    @property
    def latest_hash(self) -> str:
        entries = self.read_all()
        return entries[-1].entry_hash if entries else ""


def read_entries(path: str | Path) -> list[dict[str, Any]]:
    """Convenience: read all entries as dicts."""
    reader = LedgerReader(path)
    return [e.model_dump() for e in reader.read_all()]
