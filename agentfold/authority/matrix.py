"""Central authority matrix for tool and mutation surfaces."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class AuthoritySurface(str, Enum):
    FILESYSTEM = "filesystem"
    REPOSITORY = "repository"
    MEMORY = "memory"
    EXTERNAL_API = "external_api"
    COMMUNICATION = "communication"
    PAYMENT = "payment"
    LOCAL_STATE = "local_state"


class AuthorityRequest(BaseModel):
    surface: AuthoritySurface | str
    action: str = ""
    requires_human_authorization: bool = False
    human_authorized: bool = False
    claim_boundary: str = "authority_request_not_authority_grant"


class AuthorityDecision(BaseModel):
    passed: bool
    reason: str
    surface: str
    action: str = ""
    blocked: bool = True
    claim_boundary: str = "authority_decision_local_policy_only"


class AuthorityMatrix(BaseModel):
    """Declarative local authority matrix.

    This matrix is a local policy object. It does not grant external authority.
    """

    allowed: dict[str, list[str]] = Field(default_factory=lambda: {
        AuthoritySurface.FILESYSTEM.value: ["read"],
        AuthoritySurface.LOCAL_STATE.value: ["write", "read"],
    })
    denied: dict[str, list[str]] = Field(default_factory=lambda: {
        AuthoritySurface.REPOSITORY.value: ["write", "delete", "push"],
        AuthoritySurface.MEMORY.value: ["write", "promote"],
        AuthoritySurface.EXTERNAL_API.value: ["call", "write"],
        AuthoritySurface.COMMUNICATION.value: ["send"],
        AuthoritySurface.PAYMENT.value: ["spend", "transfer"],
    })
    high_consequence_surfaces: list[str] = Field(default_factory=lambda: [
        AuthoritySurface.REPOSITORY.value,
        AuthoritySurface.MEMORY.value,
        AuthoritySurface.EXTERNAL_API.value,
        AuthoritySurface.COMMUNICATION.value,
        AuthoritySurface.PAYMENT.value,
    ])

    def evaluate(self, request: AuthorityRequest) -> AuthorityDecision:
        surface = request.surface.value if hasattr(request.surface, "value") else str(request.surface)
        action = request.action

        if surface in self.denied and (not action or action in self.denied[surface]):
            if surface in self.high_consequence_surfaces and request.human_authorized:
                allowed_actions = self.allowed.get(surface, [])
                if action in allowed_actions:
                    return AuthorityDecision(
                        passed=True,
                        reason="human_authorized_and_allowed",
                        surface=surface,
                        action=action,
                        blocked=False,
                    )
            return AuthorityDecision(
                passed=False,
                reason="surface_or_action_denied",
                surface=surface,
                action=action,
            )

        if request.requires_human_authorization and not request.human_authorized:
            return AuthorityDecision(
                passed=False,
                reason="human_authorization_missing",
                surface=surface,
                action=action,
            )

        allowed_actions = self.allowed.get(surface, [])
        if action in allowed_actions or "*" in allowed_actions:
            return AuthorityDecision(
                passed=True,
                reason="authority_allowed",
                surface=surface,
                action=action,
                blocked=False,
            )

        return AuthorityDecision(
            passed=False,
            reason="authority_not_declared",
            surface=surface,
            action=action,
        )


def check_authority(
    *,
    surface: AuthoritySurface | str,
    action: str = "",
    matrix: AuthorityMatrix | None = None,
    requires_human_authorization: bool = False,
    human_authorized: bool = False,
) -> AuthorityDecision:
    """Convenience authority check."""
    active_matrix = matrix or AuthorityMatrix()
    return active_matrix.evaluate(
        AuthorityRequest(
            surface=surface,
            action=action,
            requires_human_authorization=requires_human_authorization,
            human_authorized=human_authorized,
        )
    )
