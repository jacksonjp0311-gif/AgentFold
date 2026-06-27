"""Hashchain verification — ensure ledger integrity."""

from __future__ import annotations

from agentfold.ledger.writer import LedgerEntry


def verify_chain(entries: list[LedgerEntry]) -> dict:
    """Verify the hashchain integrity of ledger entries.

    Returns:
        {"valid": bool, "entries_checked": int, "failures": list[str]}
    """
    failures = []
    prev_hash = ""

    for i, entry in enumerate(entries):
        # Check previous hash linkage
        if entry.previous_ledger_hash != prev_hash:
            failures.append(
                f"Entry {i} ({entry.ledger_id}): previous_hash mismatch "
                f"(expected {prev_hash}, got {entry.previous_ledger_hash})"
            )

        # Verify entry hash
        computed = entry.compute_hash()
        if computed != entry.entry_hash:
            failures.append(
                f"Entry {i} ({entry.ledger_id}): hash mismatch "
                f"(computed {computed}, stored {entry.entry_hash})"
            )

        prev_hash = entry.entry_hash

    return {
        "valid": len(failures) == 0,
        "entries_checked": len(entries),
        "failures": failures,
    }


def hash_entry(entry: LedgerEntry) -> str:
    """Compute hash for a single ledger entry."""
    return entry.compute_hash()
