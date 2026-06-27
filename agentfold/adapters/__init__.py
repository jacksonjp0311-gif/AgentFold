"""Adapters - Codex/RHP/CMS/Tessera/GNB integration stubs."""

from agentfold.adapters.base import AgentFoldAdapter
from agentfold.adapters.cms_adapter import CMSAdapter
from agentfold.adapters.codex_adapter import CodexAdapter
from agentfold.adapters.gnb_adapter import GNBAdapter
from agentfold.adapters.rhp_adapter import RHPAdapter
from agentfold.adapters.tessera_adapter import TesseraAdapter

__all__ = [
    "AgentFoldAdapter",
    "CMSAdapter",
    "CodexAdapter",
    "GNBAdapter",
    "RHPAdapter",
    "TesseraAdapter",
]
