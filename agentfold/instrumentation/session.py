"""Session recorder API for instrumenting agent runs."""

from __future__ import annotations

from pathlib import Path
import json
from typing import Any

from pydantic import BaseModel, PrivateAttr

from agentfold.expression.events import ExpressionEvent, ExpressionType
from agentfold.transcriptome.recorder import TranscriptRecorder
from agentfold.transcriptome.schema import AgentTranscriptome


class AgentFoldSession(BaseModel):
    """Thin event recorder for real agent integrations."""

    run_id: str
    genome_id: str
    agent_id: str = ""
    origin_certificate_id: str = ""
    _recorder: TranscriptRecorder = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        self._recorder = TranscriptRecorder(
            run_id=self.run_id,
            genome_id=self.genome_id,
            origin_certificate_id=self.origin_certificate_id,
        )

    @property
    def events(self) -> list[ExpressionEvent]:
        return self._recorder.events

    def record_prompt(self, gene_id: str, *, evidence_refs: list[str] | None = None) -> ExpressionEvent:
        return self._recorder.record(
            ExpressionType.PROMPT_GENE_ACTIVATION,
            "prompt_gene",
            {"gene_id": gene_id},
            evidence_refs=evidence_refs,
        )

    def record_memory(self, memory_id: str, *, reason: str = "", confidence: float = 0.0) -> ExpressionEvent:
        return self._recorder.record(
            ExpressionType.MEMORY_ACTIVATION,
            "memory",
            {"memory_id": memory_id, "activation_reason": reason},
            confidence=confidence,
        )

    def record_tool_call(
        self,
        tool_id: str,
        *,
        tool_name: str = "",
        action: str = "",
        result_summary: str = "",
    ) -> ExpressionEvent:
        return self._recorder.record(
            ExpressionType.TOOL_INVOCATION,
            "tool",
            {
                "tool_id": tool_id,
                "tool_name": tool_name,
                "action": action,
                "result_summary": result_summary,
            },
        )

    def record_claim(
        self,
        claim_id: str,
        claim_text: str,
        *,
        evidence_refs: list[str] | None = None,
        outcome: str = "allowed",
        reason: str = "",
    ) -> ExpressionEvent:
        return self._recorder.record(
            ExpressionType.CLAIM_ATTEMPT,
            "claim",
            {
                "claim_id": claim_id,
                "claim_text": claim_text,
                "outcome": outcome,
                "reason": reason,
            },
            evidence_refs=evidence_refs,
        )

    def record_gate(self, gate_id: str, *, gate_type: str, passed: bool, reason: str = "") -> ExpressionEvent:
        return self._recorder.record(
            ExpressionType.GATE_PASS if passed else ExpressionType.GATE_FAIL,
            "gate",
            {"gate_id": gate_id, "gate_type": gate_type, "reason": reason},
        )

    def record_evidence(self, evidence_id: str, *, source: str = "") -> ExpressionEvent:
        return self._recorder.record(
            ExpressionType.EVIDENCE_LOOKUP,
            "evidence",
            {"evidence_id": evidence_id, "source": source},
            evidence_refs=[evidence_id],
        )

    def record_output(self, output_hash: str) -> ExpressionEvent:
        return self._recorder.record(
            ExpressionType.OUTPUT_COMMIT,
            "output",
            {"output_hash": output_hash},
        )

    def build_transcriptome(self) -> AgentTranscriptome:
        transcriptome = self._recorder.build()
        transcriptome.agent_id = self.agent_id
        return transcriptome

    def write_events_jsonl(self, path: str | Path) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        lines = [event.model_dump_json() for event in self.events]
        output.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        return output

    def to_session_dict(self) -> dict[str, Any]:
        data = self.model_dump()
        data["events"] = [event.model_dump() for event in self.events]
        return data

    def write_session(self, path: str | Path) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(self.to_session_dict(), indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
        return output

    @classmethod
    def read_session(cls, path: str | Path) -> "AgentFoldSession":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        session = cls(
            run_id=data["run_id"],
            genome_id=data["genome_id"],
            agent_id=data.get("agent_id", ""),
            origin_certificate_id=data.get("origin_certificate_id", ""),
        )
        session._recorder._events = [ExpressionEvent(**event_data) for event_data in data.get("events", [])]
        return session
