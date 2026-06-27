"""Origin Gate — session must align to declared origin before compounding."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GateResult:
    passed: bool
    reason: str
    details: dict

    def to_dict(self) -> dict:
        return {"passed": self.passed, "reason": self.reason, "details": self.details}


def check(
    *,
    origin_ref: str = "",
    origin_hash: str = "",
    prior_origin_hash: str | None = None,
) -> GateResult:
    """Check origin alignment."""
    if not origin_ref:
        return GateResult(
            passed=False,
            reason="origin_ref_empty",
            details={"message": "No origin declared"},
        )

    if prior_origin_hash is not None and prior_origin_hash != origin_hash:
        return GateResult(
            passed=False,
            reason="origin_hash_mismatch",
            details={"message": "Origin state has changed since last session"},
        )

    return GateResult(
        passed=True,
        reason="origin_aligned",
        details={"origin_ref": origin_ref},
    )
