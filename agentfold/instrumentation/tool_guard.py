"""Guard tool execution with the AgentFold authority matrix."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

from agentfold.authority.matrix import AuthorityDecision, AuthorityMatrix, check_authority


class GuardedToolResult(BaseModel):
    executed: bool
    authority_decision: AuthorityDecision
    result: Any = None
    claim_boundary: str = "guarded_tool_result_local_policy_only"


def guard_tool(
    *,
    surface: str,
    action: str,
    fn: Callable[..., Any],
    matrix: AuthorityMatrix | None = None,
    human_authorized: bool = False,
    **kwargs: Any,
) -> GuardedToolResult:
    """Run a callable only if the authority matrix permits it."""
    decision = check_authority(
        surface=surface,
        action=action,
        matrix=matrix,
        human_authorized=human_authorized,
    )
    if not decision.passed:
        return GuardedToolResult(executed=False, authority_decision=decision)
    return GuardedToolResult(
        executed=True,
        authority_decision=decision,
        result=fn(**kwargs),
    )
