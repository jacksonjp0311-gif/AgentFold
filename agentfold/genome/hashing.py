"""AgentGenome hashing — SHA-256 of canonical JSON."""

from __future__ import annotations

import hashlib
import json

from agentfold.genome.schema import AgentGenome


def hash_genome(genome: AgentGenome) -> str:
    """Return SHA-256 hash of the genome's canonical JSON representation."""
    canonical = json.dumps(genome.model_dump(), sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
