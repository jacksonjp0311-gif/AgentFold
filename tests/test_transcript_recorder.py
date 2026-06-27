"""Tests for TranscriptRecorder and transcriptome builder."""

import pytest

from agentfold.expression.events import (
    ExpressionEvent,
    ExpressionType,
    MemoryActivation,
    ToolActivation,
    GateEvent,
)
from agentfold.transcriptome.recorder import TranscriptRecorder
from agentfold.transcriptome.schema import AgentTranscriptome
from agentfold.transcriptome.builder import build_transcriptome


def test_recorder_creation():
    recorder = TranscriptRecorder(run_id="run_001", genome_id="g_001")
    assert recorder.event_count == 0


def test_recorder_record_event():
    recorder = TranscriptRecorder(run_id="run_001", genome_id="g_001")
    ev = recorder.record(
        ExpressionType.MEMORY_ACTIVATION,
        "memory",
        {"memory_id": "m_001"},
        evidence_refs=["ev_001"],
        confidence=0.8,
    )
    assert recorder.event_count == 1
    assert ev.expression_type == ExpressionType.MEMORY_ACTIVATION
    assert ev.payload["memory_id"] == "m_001"


def test_recorder_build_transcriptome():
    recorder = TranscriptRecorder(run_id="run_001", genome_id="g_001")
    recorder.record(
        ExpressionType.PROMPT_GENE_ACTIVATION,
        "prompt_gene",
        {"gene_id": "gene_001"},
    )
    recorder.record(
        ExpressionType.MEMORY_ACTIVATION,
        "memory",
        {"memory_id": "m_001", "activation_reason": "task_relevant"},
        confidence=0.9,
    )
    recorder.record(
        ExpressionType.TOOL_INVOCATION,
        "tool",
        {"tool_id": "tool_001", "tool_name": "read_file", "action": "read"},
    )

    transcriptome = recorder.build()
    assert isinstance(transcriptome, AgentTranscriptome)
    assert transcriptome.run_id == "run_001"
    assert len(recorder.events) == 3


def test_build_transcriptome_from_events():
    events = [
        ExpressionEvent(
            event_id="ev_001",
            run_id="run_001",
            expression_type=ExpressionType.PROMPT_GENE_ACTIVATION,
            source="gene_role_001",
            payload={"gene_id": "gene_role_001"},
        ),
        ExpressionEvent(
            event_id="ev_002",
            run_id="run_001",
            expression_type=ExpressionType.MEMORY_ACTIVATION,
            source="memory",
            payload={"memory_id": "m_001", "activation_reason": "task"},
            confidence=0.85,
        ),
        ExpressionEvent(
            event_id="ev_003",
            run_id="run_001",
            expression_type=ExpressionType.CLAIM_ATTEMPT,
            source="claim",
            payload={"claim_id": "c_001", "claim_text": "test claim", "outcome": "blocked"},
        ),
    ]

    transcriptome = build_transcriptome(
        events,
        run_id="run_001",
        genome_id="g_001",
        agent_id="a_001",
    )

    assert len(transcriptome.activated_prompt_genes) == 1
    assert len(transcriptome.activated_memory) == 1
    assert len(transcriptome.claims_attempted) == 1
    assert len(transcriptome.claims_blocked) == 1
