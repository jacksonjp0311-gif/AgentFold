"""AgentGenome — encoded operational substrate."""

from agentfold.genome.schema import (
    AgentGenome,
    PromptGene,
    ToolSpec,
    PermissionSpec,
    ConstraintSpec,
    EvidenceRef,
    FailureMode,
    LineageRef,
)
from agentfold.genome.loader import load_genome, load_genome_from_dict
from agentfold.genome.validator import validate_genome
from agentfold.genome.hashing import hash_genome

__all__ = [
    "AgentGenome",
    "PromptGene",
    "ToolSpec",
    "PermissionSpec",
    "ConstraintSpec",
    "EvidenceRef",
    "FailureMode",
    "LineageRef",
    "load_genome",
    "load_genome_from_dict",
    "validate_genome",
    "hash_genome",
]
