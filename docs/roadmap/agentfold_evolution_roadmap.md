# AgentFold Evolution Roadmap

## Current Checkpoint

AF-SA v1.4.0 is a release candidate validation checkpoint. It has repository geometry, rehydration protocol, route maps, mini READMEs, bounded AlphaFold/genome/RNA analysis, AgentPhenotype, authority matrix, replayable evidence packets, persisted packet IO, replay/diff/report/schema CLI commands, a session recorder API, guarded tool wrapper, adapter contract, session CLI lifecycle, CI policy, CI verifier, misfold fixtures, GitHub Actions template, release validator, docs registry, release candidate manifest, a local pipeline, release seal, working CLI commands, and a passing local test suite.

## Next Evolution Targets

### v0.1.2 - Genesis Source Preservation

- Track the original AF-SA v0.1.0 gist as canonical architecture source.
- Add source-bound implementation map.
- Add tests that ensure source surfaces are linked from README and context indexes.
- Add bounded cross-domain AlphaFold/genome/RNA analysis.
- Implement software-only `AgentPhenotype` as the next runtime layer.

### v0.2.0 - Rehydration Evidence Packets

- Emit a rehydration packet containing origin certificate, repo route snapshot, read order, git state, validation command, and non-claim boundary.
- Add JSON schema for rehydration packets.
- Add replay validator for rehydration packets.

Law:

    No rehydration claim without a replayable rehydration packet.

### v0.3.0 - AgentPhenotype Contract

- Add explicit `AgentPhenotype` schema.
- Derive phenotype from fold graph, gate outcomes, fitness vector, and misfold events.
- Add phenotype certificate tests.

Law:

    No phenotype claim without transcript and fold graph evidence.

### v0.4.0 - Authority Matrix

- Add one authority matrix consumed by tool, permission, human authorization, and compounding gates.
- Cover memory write, repo write, external message, API, payment, and filesystem surfaces.
- Add denial reason consistency tests.

Law:

    No declared authority, no mutation surface.

### v0.5.0 - Replayable Fold Evidence

- Emit fold evidence packets.
- Add replay validator for transcript, graph, prediction, misfolds, fitness, certificate, and ledger links.
- Add drift comparator across fold evidence packets.

Law:

    No fold maturity claim until the fold can be replayed.

### v0.6.0 - Release Functional and Public Metrics

- Encode the AgentFold admissible release functional as machine-readable JSON.
- Add current public metrics page.
- Add version-surface checker.

Law:

    No release checkpoint without a machine-readable release functional.

### v1.0.0 - Local Release Functional Checkpoint

- Add central authority matrix.
- Add replayable fold evidence packet.
- Add full local runtime pipeline.
- Add machine-readable release functional.
- Add local release seal.

Law:

    No v1.0 checkpoint without origin, genome, transcript, fold graph, prediction, misfolds, fitness, phenotype, authority, gate, replay, ledger, tests, docs, and non-claim lock.

### v1.1.0 - Persisted Evidence and Replay Checkpoint

- Add evidence packet read/write.
- Add replay verification CLI.
- Add evidence diff CLI.
- Add Markdown report generation.
- Add JSON Schema export.

Law:

    No portable replay without persisted evidence, schemas, and human-readable reports.

### v1.2.0 - Adapter Instrumentation Checkpoint

- Add `AgentFoldSession` recorder API.
- Populate transcriptomes from recorded runtime events.
- Add guarded tool wrapper.
- Add adapter contract.
- Add session CLI lifecycle.

Law:

    No integration claim without instrumented events and authority-guarded tools.

### v1.3.0 - CI Gate and Misfold Benchmark Checkpoint

- Add CI policy file.
- Add `ci-verify` command.
- Add CI summary JSON/Markdown.
- Add deterministic misfold fixtures.
- Add GitHub Actions template.

Law:

    No automated gate claim without replay verification, authority checks, phenotype checks, and misfold fixtures.

### v1.4.0 - Release Candidate Validation Checkpoint

- Add release validator.
- Add docs registry.
- Add release candidate manifest.
- Add release validation JSON/Markdown output.

Law:

    No release candidate claim without tests, CLI validation, docs registry, route map, policy, manifest, and non-claim lock.

## Boundary

This roadmap improves implementation discipline. It does not prove code correctness, safety, security, production readiness, AGI, consciousness, or biological equivalence.
