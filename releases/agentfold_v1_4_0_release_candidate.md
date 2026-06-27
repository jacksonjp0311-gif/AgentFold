# AgentFold v1.4.0 Release Candidate

## Status

AF-SA v1.4.0 is a release candidate for local validation.

## Required Validation

    python -m pytest -q
    python -m agentfold.cli --help
    python -m agentfold.cli validate-genome examples/genomes/minimal_agent_genome.json
    python -m agentfold.cli release-validate

## Added Release Surfaces

- Release validator
- Docs registry
- Release candidate manifest
- Release validation JSON/Markdown output

## Boundary

This release candidate does not prove production readiness, safety, security, AGI, consciousness, biological equivalence, autonomous authority, or claim truth.
