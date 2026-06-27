"""TranscriptRecorder — capture runtime expression events."""

from __future__ import annotations

import hashlib
import itertools
import uuid
from datetime import datetime, timezone

from agentfold.expression.events import ExpressionEvent, ExpressionType


class TranscriptRecorder:
    """Records runtime events and builds transcriptomes.

    Usage:
        recorder = TranscriptRecorder(run_id="run_001", genome_id="g_001")
        recorder.record_expression("memory_activation", "memory", {...}, ["ev_001"])
        transcriptome = recorder.build()
    """

    def __init__(self, run_id: str, genome_id: str, origin_certificate_id: str = ""):
        self.run_id = run_id
        self.genome_id = genome_id
        self.origin_certificate_id = origin_certificate_id
        self._events: list[ExpressionEvent] = []
        self._counter = itertools.count(1)

    def _next_id(self) -> str:
        return f"{self.run_id}_ev{next(self._counter):04d}"

    def record(
        self,
        expression_type: ExpressionType | str,
        source: str,
        payload: dict | None = None,
        *,
        evidence_refs: list[str] | None = None,
        confidence: float = 0.0,
    ) -> ExpressionEvent:
        """Record a single runtime expression event."""
        if isinstance(expression_type, str):
            expression_type = ExpressionType(expression_type)

        event = ExpressionEvent(
            event_id=self._next_id(),
            run_id=self.run_id,
            expression_type=expression_type,
            source=source,
            payload=payload or {},
            evidence_refs=evidence_refs or [],
            confidence=confidence,
        )
        self._events.append(event)
        return event

    @property
    def events(self) -> list[ExpressionEvent]:
        return list(self._events)

    @property
    def event_count(self) -> int:
        return len(self._events)

    def build(self) -> "AgentTranscriptome":
        from agentfold.transcriptome.schema import AgentTranscriptome
        import json
        transcript_id = hashlib.sha256(
            f"{self.run_id}:{self.genome_id}:{len(self._events)}".encode()
        ).hexdigest()[:16]

        parts = [
            f"{e.event_id}:{e.expression_type.value}:{e.confidence}"
            for e in self._events
        ]
        final_hash = hashlib.sha256(",".join(parts).encode()).hexdigest()[:16]

        return AgentTranscriptome(
            transcriptome_id=transcript_id,
            run_id=self.run_id,
            genome_id=self.genome_id,
            origin_certificate_id=self.origin_certificate_id,
            final_output_hash=final_hash,
            claim_boundary="transcript_from_recorder",
        )
