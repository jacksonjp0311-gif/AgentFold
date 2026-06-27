"""AgentGenome loader — from JSON file or dict."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agentfold.genome.schema import AgentGenome


def load_genome(path: str | Path) -> AgentGenome:
    """Load an AgentGenome from a JSON file."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return AgentGenome(**data)


def load_genome_from_dict(data: dict[str, Any]) -> AgentGenome:
    """Load an AgentGenome from a dict."""
    return AgentGenome(**data)
