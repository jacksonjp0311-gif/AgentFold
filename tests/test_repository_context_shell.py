"""Tests for the AgentFold repository context shell."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", ".pytest_cache", "__pycache__"}
IGNORED_PREFIXES = ("outputs_", "reports")
README_EXCEPTIONS = {
    ".github": "FOLDER_README.md",
}


def iter_relevant_dirs() -> list[Path]:
    dirs = []
    for path in ROOT.rglob("*"):
        if not path.is_dir():
            continue
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0].startswith(IGNORED_PREFIXES):
            continue
        parts = set(rel.parts)
        if parts & IGNORED_DIRS:
            continue
        dirs.append(path)
    return dirs


def test_every_subfolder_has_readme():
    missing = [
        str(path.relative_to(ROOT))
        for path in iter_relevant_dirs()
        if not (path / README_EXCEPTIONS.get(str(path.relative_to(ROOT)), "README.md")).exists()
    ]
    assert missing == []


def test_context_indexes_and_route_map_are_valid_json():
    required = [
        ROOT / "docs/context/repository_context_index.json",
        ROOT / "docs/context/rcc_nexus_index.json",
        ROOT / "docs/cross_domain/cross_domain_mapping.json",
        ROOT / "rcc/nexus/route_map.json",
    ]
    for path in required:
        assert path.exists()
        json.loads(path.read_text(encoding="utf-8"))


def test_readme_declares_rehydration_and_non_claim_lock():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "PART I - Human README" in readme
    assert "PART II - RCC Nexus README" in readme
    assert "PART III - AI Agent README" in readme
    assert "Rehydration Protocol" in readme
    assert "Genesis Source Alignment" in readme
    assert "production readiness" in readme.lower()
    assert "not prove" in readme.lower()


def test_genesis_source_is_linked_from_navigation_surfaces():
    gist_url = "https://gist.github.com/jacksonjp0311-gif/2d92eb0f12bba782639460f18a426f42"
    paths = [
        ROOT / "README.md",
        ROOT / "README_90_SECONDS.md",
        ROOT / "docs/software_architecture/agentfold_sa_v0_1_0_genesis_source.md",
        ROOT / "docs/context/repository_context_index.json",
        ROOT / "docs/context/rcc_nexus_index.json",
    ]
    for path in paths:
        assert gist_url in path.read_text(encoding="utf-8")


def test_cross_domain_mapping_preserves_non_biological_boundary():
    mapping = json.loads((ROOT / "docs/cross_domain/cross_domain_mapping.json").read_text(encoding="utf-8"))
    assert "software analogy only" in mapping["boundary"]
    assert any(item["agentfold_surface"] == "AgentPhenotype" for item in mapping["mappings"])
    prohibited = " ".join(mapping["prohibited_claims"]).lower()
    assert "biological alphafold" in prohibited
    assert "autonomous write authority" in prohibited


def test_version_surfaces_are_aligned_to_v1_4_0():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    package_init = (ROOT / "agentfold/__init__.py").read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    repo_index = json.loads((ROOT / "docs/context/repository_context_index.json").read_text(encoding="utf-8"))

    assert "AF-SA v1.4.0" in readme
    assert '__version__ = "1.4.0"' in package_init
    assert 'version = "1.4.0"' in pyproject
    assert repo_index["software_layer"] == "AF-SA v1.4.0"
    assert "release candidate" in readme.lower()
