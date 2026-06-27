"""Base adapter contract for AgentFold integrations."""

from __future__ import annotations

from typing import Protocol

from agentfold.expression.events import ExpressionEvent


class AgentFoldAdapter(Protocol):
    """Minimal adapter contract for event-producing integrations."""

    def record(self, event: ExpressionEvent) -> None:
        """Record an AgentFold expression event."""
