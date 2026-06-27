"""Inheritance — validated deltas may become future genome/memory input."""

from agentfold.inheritance.delta import ValidatedDelta, DeltaType
from agentfold.inheritance.promoter import promote_delta
from agentfold.inheritance.blocker import block_delta

__all__ = [
    "ValidatedDelta",
    "DeltaType",
    "promote_delta",
    "block_delta",
]
