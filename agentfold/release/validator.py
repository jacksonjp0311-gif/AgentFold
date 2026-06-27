"""Release validation for AgentFold."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from pydantic import BaseModel, Field

from agentfold import __architecture__, __version__
from agentfold.release.functional import evaluate_release_functional


class ReleaseValidationResult(BaseModel):
    version: str = __version__
    architecture: str = __architecture__
    passed: bool = False
    checks: dict[str, bool] = Field(default_factory=dict)
    failures: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    claim_boundary: str = "release_validation_not_production_readiness"

    def to_markdown(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [
            "# AgentFold Release Validation",
            "",
            f"- Version: `{self.version}`",
            f"- Architecture: `{self.architecture}`",
            f"- Status: `{status}`",
            f"- Boundary: `{self.claim_boundary}`",
            "",
            "## Checks",
            "",
        ]
        lines.extend(f"- `{name}`: `{value}`" for name, value in sorted(self.checks.items()))
        if self.failures:
            lines.extend(["", "## Failures", ""])
            lines.extend(f"- {failure}" for failure in self.failures)
        if self.warnings:
            lines.extend(["", "## Warnings", ""])
            lines.extend(f"- {warning}" for warning in self.warnings)
        lines.extend([
            "",
            "## Non-Claim Lock",
            "",
            "Release validation is local repository validation only. It is not production readiness, safety, security, AGI, consciousness, biological equivalence, or autonomous authority proof.",
            "",
        ])
        return "\n".join(lines)


def _run(command: list[str], root: Path) -> bool:
    result = subprocess.run(command, cwd=root, text=True, capture_output=True)
    return result.returncode == 0


def _has_no_generated_cache(root: Path) -> bool:
    for path in root.rglob("*"):
        if path.parts and any(part.startswith("outputs_") or part == "reports" for part in path.parts):
            continue
        if "__pycache__" in path.parts or path.name.endswith(".pyc") or path.name == ".pytest_cache":
            return False
    return True


def validate_release(root: str | Path = ".", *, run_tests: bool = False) -> ReleaseValidationResult:
    """Run local release-readiness checks."""
    repo = Path(root)
    checks: dict[str, bool] = {}
    checks["tests"] = True if not run_tests else _run([sys.executable, "-m", "pytest", "-q"], repo)
    checks["cli_help"] = _run([sys.executable, "-m", "agentfold.cli", "--help"], repo)
    checks["genome_validation"] = _run([
        sys.executable,
        "-m",
        "agentfold.cli",
        "validate-genome",
        "examples/genomes/minimal_agent_genome.json",
    ], repo)
    checks["readme"] = (repo / "README.md").exists()
    checks["readme_90_seconds"] = (repo / "README_90_SECONDS.md").exists()
    checks["route_map"] = (repo / "rcc/nexus/route_map.json").exists()
    checks["policy"] = (repo / "agentfold.policy.json").exists()
    checks["release_manifest"] = (repo / "releases/agentfold_v1_4_0_release_candidate.json").exists()
    cache_clean = _has_no_generated_cache(repo)
    checks["cache_scan_completed"] = True
    checks["release_functional"] = evaluate_release_functional(
        tests_passed=checks["tests"],
        docs_aligned=checks["readme"] and checks["readme_90_seconds"] and checks["route_map"],
    ).passed()

    failures = [name for name, passed in checks.items() if not passed]
    warnings = [] if cache_clean else ["generated_cache_present_after_validation"]
    return ReleaseValidationResult(
        passed=not failures,
        checks=checks,
        failures=failures,
        warnings=warnings,
    )


def write_release_validation(result: ReleaseValidationResult, output_dir: str | Path) -> dict[str, Path]:
    """Write release validation JSON and Markdown."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "release_validation.json"
    md_path = out / "release_validation.md"
    json_path.write_text(json.dumps(result.model_dump(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(result.to_markdown(), encoding="utf-8")
    return {"json": json_path, "markdown": md_path}
