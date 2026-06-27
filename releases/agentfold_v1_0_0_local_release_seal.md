# AgentFold v1.0.0 Local Release Seal

## Status

AF-SA v1.0.0 is a local validated checkpoint.

## Required Validation

    python -m pytest -q
    python -m agentfold.cli --help
    python -m agentfold.cli validate-genome examples/genomes/minimal_agent_genome.json

## Release Functional

    A_AF =
    origin * genome * transcript * fold_graph * prediction * misfold
    * fitness * phenotype * authority * gate * replay * ledger
    * tests * docs * nonclaim * (1 - overclaim_pressure)

## Boundary

This release seal does not prove production readiness, safety, security, AGI, consciousness, biological equivalence, autonomous authority, or claim truth.

## v1.1.0 Continuation

AF-SA v1.1.0 adds persisted evidence packet IO, replay verification, run diffing, Markdown reporting, and JSON Schema export while preserving the v1.0.0 non-claim boundary.

## v1.2.0 Continuation

AF-SA v1.2.0 adds adapter instrumentation: session event recording, event-populated transcriptomes, guarded tool execution, an adapter contract, and CLI session lifecycle commands.

## v1.3.0 Continuation

AF-SA v1.3.0 adds CI gate verification, policy thresholds, CI summary artifacts, adversarial misfold fixtures, and a GitHub Actions template.
