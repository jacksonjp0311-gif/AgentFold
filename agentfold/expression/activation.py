"""Activation logic — should a prompt gene or memory activate?"""

from __future__ import annotations

from agentfold.genome.schema import PromptGene, PromptGeneType


def should_activate(
    gene: PromptGene,
    *,
    current_context: str = "",
) -> bool:
    """Decide whether a prompt gene should activate for the given context."""
    # Check denied contexts first
    if current_context in gene.denied_contexts:
        return False

    # Check allowed contexts
    if gene.allowed_contexts and current_context not in gene.allowed_contexts:
        return False

    # Check activation condition
    if gene.activation_condition:
        # Simple substring check — can be extended to full expression eval
        return gene.activation_condition.lower() in current_context.lower()

    # No restrictions — default activate
    return True
