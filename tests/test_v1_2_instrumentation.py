"""Tests for v1.2 instrumentation and adapter surfaces."""

from click.testing import CliRunner

from agentfold.authority.matrix import AuthorityMatrix, AuthoritySurface
from agentfold.cli import main
from agentfold.instrumentation.session import AgentFoldSession
from agentfold.instrumentation.tool_guard import guard_tool


def test_session_records_real_transcriptome_entries(tmp_path):
    session = AgentFoldSession(run_id="run_inst", genome_id="genome_001", agent_id="agent_001")
    session.record_prompt("gene_role_001")
    session.record_memory("mem_001", reason="task", confidence=0.8)
    session.record_tool_call("tool_read", tool_name="read_file", action="read")
    session.record_claim("claim_001", "bounded claim", evidence_refs=["ev_001"], outcome="allowed")
    session.record_gate("gate_001", gate_type="evidence", passed=True, reason="ok")
    session.record_output("hash_001")

    transcriptome = session.build_transcriptome()
    session_path = session.write_session(tmp_path / "session.json")
    loaded = AgentFoldSession.read_session(session_path)

    assert len(transcriptome.activated_prompt_genes) == 1
    assert len(transcriptome.activated_memory) == 1
    assert len(transcriptome.activated_tools) == 1
    assert len(transcriptome.claims_allowed) == 1
    assert len(transcriptome.gate_events) == 1
    assert len(loaded.events) == 6


def test_guard_tool_blocks_denied_surface_and_executes_allowed_surface():
    blocked = guard_tool(
        surface=AuthoritySurface.REPOSITORY.value,
        action="write",
        fn=lambda: "mutated",
    )
    allowed = guard_tool(
        surface=AuthoritySurface.LOCAL_STATE.value,
        action="read",
        fn=lambda value: f"read:{value}",
        value="ok",
    )

    assert blocked.executed is False
    assert blocked.authority_decision.passed is False
    assert allowed.executed is True
    assert allowed.result == "read:ok"


def test_guard_tool_can_use_custom_matrix():
    matrix = AuthorityMatrix(allowed={AuthoritySurface.REPOSITORY.value: ["write"]}, denied={})
    result = guard_tool(
        surface=AuthoritySurface.REPOSITORY.value,
        action="write",
        matrix=matrix,
        fn=lambda: "custom-ok",
    )

    assert result.executed is True
    assert result.result == "custom-ok"


def test_cli_session_lifecycle(tmp_path):
    runner = CliRunner()
    session_path = tmp_path / "session.json"
    transcriptome_path = tmp_path / "transcriptome.json"

    start = runner.invoke(
        main,
        [
            "start-session",
            "--run-id",
            "cli_session",
            "--genome-id",
            "genome_001",
            "--agent-id",
            "agent_001",
            "--output",
            str(session_path),
        ],
    )
    assert start.exit_code == 0
    assert session_path.exists()

    record = runner.invoke(
        main,
        [
            "record-event",
            str(session_path),
            "--type",
            "claim",
            "--id",
            "claim_001",
            "--text",
            "bounded claim",
            "--outcome",
            "blocked",
        ],
    )
    assert record.exit_code == 0

    close = runner.invoke(main, ["close-session", str(session_path), str(transcriptome_path)])
    assert close.exit_code == 0
    assert transcriptome_path.exists()
    assert "claim_001" in transcriptome_path.read_text(encoding="utf-8")
