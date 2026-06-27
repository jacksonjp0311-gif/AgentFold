"""Replay Gate — memory promotion requires replayable evidence."""

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
    has_transcript: bool = False,
    has_fold_graph: bool = False,
    has_ledger_entry: bool = False,
) -> GateResult:
    """Check if replay evidence exists for memory promotion."""
    if not has_transcript:
        return GateResult(
            passed=False,
            reason="no_transcript_for_replay",
            details={"message": "Transcript required for replay-based validation"},
        )

    if not has_fold_graph:
        return GateResult(
            passed=False,
            reason="no_fold_graph_for_replay",
            details={"message": "Fold graph required to replay behavioral structure"},
        )

    if not has_ledger_entry:
        return GateResult(
            passed=False,
            reason="no_ledger_entry",
            details={"message": "Ledger entry required for replay certification"},
        )

    return GateResult(
        passed=True,
        reason="replay_evidence_complete",
        details={},
    )
