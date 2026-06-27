"""Codex / evidence-gated compounding adapter — AgentFold adapter stub."""

from __future__ import annotations

from typing import Any


class CodexAdapter:
    """Adapter for Codex / evidence-gated compounding adapter.

    Stub for v0.1.0 — implement integration logic in future versions.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.adapter_name = "CodexAdapter"

    def adapt(self, data: dict[str, Any]) -> dict[str, Any]:
        """Adapt input data to/from the external system."""
        return {
            "adapter": self.adapter_name,
            "input": data,
            "claim_boundary": "adapter_stub_no_truth_claim",
        }

    def health_check(self) -> dict[str, Any]:
        """Check adapter health / connectivity."""
        return {
            "adapter": self.adapter_name,
            "status": "stub",
            "message": "Stub adapter — implement integration logic",
        }
