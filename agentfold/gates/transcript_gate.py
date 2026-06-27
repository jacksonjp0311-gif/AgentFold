"""Transcript Gate — runtime expression must be captured for inheritance."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GateResult:
    passed: bool
    reason: str
    details: dict

    def to_dict(self) -> dict:
        return {"passed": self.passed, "reason": self.reason, "details": self.details}

    def __init__(self, passed: bool, reason: str, details: dict | None = None):
        self.passed = passed
        self.reason = reason
        self.details = details or {}


def check(
    *,
    event_count: int = 0,
    has_transcript: bool = False,
) -> GateResult:
    """Check transcript completeness."""
    if has_transcript:
        return GateResult(passed=True, reason="transcript_present", details={})

    if event_count > 0:
        return GateResult(passed=False, reason="transcript_not_built", details={"event_count": event_count})

    return GateResult(passed=True, reason="no_events_to_transcribe", details={})
