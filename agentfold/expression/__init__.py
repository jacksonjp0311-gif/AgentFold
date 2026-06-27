"""RuntimeExpression — atomic unit of agent transcriptomics."""

from agentfold.expression.events import (
    ExpressionEvent,
    ExpressionType,
    MemoryActivation,
    ToolActivation,
    ToolConsideration,
    ClaimAttempt,
    GateEvent,
    DriftEvent,
    MisfoldWarning,
    RepairEvent,
)
from agentfold.expression.activation import should_activate

__all__ = [
    "ExpressionEvent",
    "ExpressionType",
    "MemoryActivation",
    "ToolActivation",
    "ToolConsideration",
    "ClaimAttempt",
    "GateEvent",
    "DriftEvent",
    "MisfoldWarning",
    "RepairEvent",
    "should_activate",
]
