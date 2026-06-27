"""Transcriptome parser — load from JSON / JSONL."""

from __future__ import annotations

import json
from pathlib import Path

from agentfold.transcriptome.schema import AgentTranscriptome


def parse_transcriptome_from_file(path: str | Path) -> AgentTranscriptome:
    """Load an AgentTranscriptome from a JSON file."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return AgentTranscriptome(**data)
