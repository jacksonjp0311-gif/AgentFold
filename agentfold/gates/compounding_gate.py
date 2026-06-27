"""CompoundingGate — central decision: permit, downgrade, repair, shadow, block."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from pydantic import BaseModel, Field


class CompoundingDecision(str, Enum):
    PERMIT = "permit"
    PERMIT_WITH_WARNING = "permit_with_warning"
    DOWNGRADE = "downgrade"
    REPAIR_REQUIRED = "repair_required"
    SHADOW_ONLY = "shadow_only"
    BLOCK = "block"
    REQUIRE_HUMAN_REVIEW = "require_human_review"


@dataclass
class CompoundingGateResult:
    decision: CompoundingDecision
    allowed_mutations: list[str] = field(default_factory=list)
    blocked_mutations: list[str] = field(default_factory=list)
    reason: str = ""
    claim_boundary: str = "compounding_gate_decision"

    def to_dict(self) -> dict:
        return {
            "decision": str(self.decision),
            "allowed_mutations": self.allowed_mutations,
            "blocked_mutations": self.blocked_mutations,
            "reason": self.reason,
            "claim_boundary": self.claim_boundary,
        }


class CompoundingGate:
    """Central compounding gate — evaluates all sub-gates and emits decision."""

    def evaluate(
        self,
        *,
        origin_passed: bool = False,
        genome_valid: bool = False,
        permission_passed: bool = False,
        claim_within_ceiling: bool = False,
        evidence_sufficient: bool = False,
        transcript_complete: bool = False,
        fold_graph_complete: bool = False,
        misfold_passed: bool = False,
        tool_permitted: bool = False,
        replay_complete: bool = False,
        ledger_written: bool = False,
        inheritance_permitted: bool = False,
        human_auth_present: bool = True,
        human_auth_required: bool = False,
    ) -> CompoundingGateResult:
        """Evaluate all gate conditions and emit compounding decision."""
        # Critical blocks — any of these is a hard stop
        blockers = []
        if not origin_passed:
            blockers.append("origin_alignment_failed")
        if not genome_valid:
            blockers.append("genome_invalid")
        if not claim_within_ceiling:
            blockers.append("claim_exceeds_ceiling")
        if not misfold_passed:
            blockers.append("critical_misfold")
        if human_auth_required and not human_auth_present:
            blockers.append("human_authorization_missing")

        if blockers:
            return CompoundingGateResult(
                decision=CompoundingDecision.BLOCK,
                blocked_mutations=["all"],
                reason=f"Critical gate failures: {', '.join(blockers)}",
            )

        # Warnings — non-critical gate failures
        warnings = []
        if not evidence_sufficient:
            warnings.append("insufficient_evidence")
        if not transcript_complete:
            warnings.append("transcript_incomplete")
        if not fold_graph_complete:
            warnings.append("fold_graph_incomplete")
        if not replay_complete:
            warnings.append("replay_incomplete")
        if not ledger_written:
            warnings.append("ledger_not_written")
        if not permission_passed:
            warnings.append("permission_not_explicit")

        if len(warnings) >= 3:
            return CompoundingGateResult(
                decision=CompoundingDecision.SHADOW_ONLY,
                blocked_mutations=["memory_write", "repo_write", "external_message"],
                reason=f"Multiple warnings: {', '.join(warnings)}",
            )

        if warnings:
            # Downgrade: permit with restrictions
            if "insufficient_evidence" in warnings:
                return CompoundingGateResult(
                    decision=CompoundingDecision.REPAIR_REQUIRED,
                    blocked_mutations=["memory_write", "elevated_claims"],
                    reason=f"Warnings require repair: {', '.join(warnings)}",
                )
            return CompoundingGateResult(
                decision=CompoundingDecision.PERMIT_WITH_WARNING,
                allowed_mutations=["validated_delta", "local_state"],
                blocked_mutations=["memory_write", "repo_write", "external_message"],
                reason=f"Warnings: {', '.join(warnings)}",
            )

        # All gates passed
        return CompoundingGateResult(
            decision=CompoundingDecision.PERMIT,
            allowed_mutations=["validated_delta"],
            reason="All gates passed",
        )


def decide_compounding(**kwargs) -> CompoundingGateResult:
    """Convenience function for compounding gate evaluation."""
    gate = CompoundingGate()
    return gate.evaluate(**kwargs)
