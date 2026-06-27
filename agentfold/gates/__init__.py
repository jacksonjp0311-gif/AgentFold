"""Validation gates — all gate modules for the compounding pipeline."""

from agentfold.gates.origin_gate import check as check_origin_gate
from agentfold.gates.genome_gate import check as check_genome_gate
from agentfold.gates.permission_gate import check as check_permission_gate
from agentfold.gates.claim_gate import check as check_claim_gate
from agentfold.gates.evidence_gate import check as check_evidence_gate
from agentfold.gates.transcript_gate import check as check_transcript_gate
from agentfold.gates.fold_graph_gate import check as check_fold_graph_gate
from agentfold.gates.misfold_gate import check as check_misfold_gate
from agentfold.gates.tool_gate import check as check_tool_gate
from agentfold.gates.replay_gate import check as check_replay_gate
from agentfold.gates.ledger_gate import check as check_ledger_gate
from agentfold.gates.inheritance_gate import check as check_inheritance_gate
from agentfold.gates.human_authorization_gate import check as check_human_auth_gate
from agentfold.gates.compounding_gate import CompoundingGate, decide_compounding

__all__ = [
    "check_origin_gate",
    "check_genome_gate",
    "check_permission_gate",
    "check_claim_gate",
    "check_evidence_gate",
    "check_transcript_gate",
    "check_fold_graph_gate",
    "check_misfold_gate",
    "check_tool_gate",
    "check_replay_gate",
    "check_ledger_gate",
    "check_inheritance_gate",
    "check_human_auth_gate",
    "CompoundingGate",
    "decide_compounding",
]
