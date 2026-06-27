"""Tests for ledger writer, reader, and hashchain verification."""

import tempfile
from pathlib import Path

import pytest

from agentfold.ledger.writer import LedgerWriter, LedgerEntry
from agentfold.ledger.reader import LedgerReader
from agentfold.ledger.hashchain import verify_chain


@pytest.fixture
def ledger_path():
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    yield path
    Path(path).unlink(missing_ok=True)


@pytest.fixture
def sample_entries():
    return [
        LedgerEntry(ledger_id="le_001", run_id="run_001", agent_id="a_001"),
        LedgerEntry(ledger_id="le_002", run_id="run_002", agent_id="a_001"),
        LedgerEntry(ledger_id="le_003", run_id="run_003", agent_id="a_002"),
    ]


def test_write_and_read(ledger_path, sample_entries):
    writer = LedgerWriter(ledger_path)
    for entry in sample_entries:
        writer.write(entry)

    reader = LedgerReader(ledger_path)
    entries = reader.read_all()
    assert len(entries) == 3


def test_hashchain_integrity(ledger_path, sample_entries):
    writer = LedgerWriter(ledger_path)
    for entry in sample_entries:
        writer.write(entry)

    reader = LedgerReader(ledger_path)
    entries = reader.read_all()
    result = verify_chain(entries)
    assert result["valid"] is True
    assert result["entries_checked"] == 3


def test_read_by_run(ledger_path, sample_entries):
    writer = LedgerWriter(ledger_path)
    for entry in sample_entries:
        writer.write(entry)

    reader = LedgerReader(ledger_path)
    entries = reader.read_by_run("run_001")
    assert len(entries) == 1
    assert entries[0].ledger_id == "le_001"


def test_read_by_agent(ledger_path, sample_entries):
    writer = LedgerWriter(ledger_path)
    for entry in sample_entries:
        writer.write(entry)

    reader = LedgerReader(ledger_path)
    entries = reader.read_by_agent("a_001")
    assert len(entries) == 2


def test_ledger_hash_linkage(ledger_path):
    writer = LedgerWriter(ledger_path)
    e1 = LedgerEntry(ledger_id="le_001", run_id="run_001")
    e2 = LedgerEntry(ledger_id="le_002", run_id="run_002")
    written1 = writer.write(e1)
    written2 = writer.write(e2)

    assert written1.previous_ledger_hash == ""
    assert written2.previous_ledger_hash == written1.entry_hash
