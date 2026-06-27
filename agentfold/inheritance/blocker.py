"""Delta blocker — block deltas from inheritance."""

from __future__ import annotations

from agentfold.inheritance.delta import ValidatedDelta


def block_delta(
    delta: ValidatedDelta,
    *,
    reason: str = "blocked_by_gate",
) -> ValidatedDelta:
    """Block a delta from inheritance."""
    delta.allowed = False
    delta.reason = reason
    return delta
