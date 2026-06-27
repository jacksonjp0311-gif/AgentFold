"""Tests for v1.4 release validation surfaces."""

import json

from click.testing import CliRunner

from agentfold.cli import main
from agentfold.release.validator import validate_release, write_release_validation


def test_release_validation_passes_local_surfaces(tmp_path):
    result = validate_release(".", run_tests=False)
    paths = write_release_validation(result, tmp_path)

    assert result.passed is True
    assert result.checks["release_manifest"] is True
    assert result.checks["release_functional"] is True
    assert paths["json"].exists()
    assert paths["markdown"].exists()
    assert "not production readiness" in paths["markdown"].read_text(encoding="utf-8")


def test_cli_release_validate_writes_reports(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["release-validate", "--output-dir", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / "release_validation.json").exists()
    assert (tmp_path / "release_validation.md").exists()


def test_release_candidate_manifest_has_non_claim_boundary():
    manifest = json.loads(open("releases/agentfold_v1_4_0_release_candidate.json", encoding="utf-8").read())

    assert manifest["version"] == "AF-SA v1.4.0"
    assert "agentfold/release/validator.py" in manifest["release_surfaces"]
    assert "not production readiness" in manifest["non_claim_boundary"]
