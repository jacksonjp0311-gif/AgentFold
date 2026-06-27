# AgentFold Rehydration Protocol

## Purpose

Rehydration restores repository context before an agent edits code, promotes claims, mutates memory, or writes inheritance state.

## Canonical Sequence

    anchor -> read -> index -> route -> validate -> inspect -> plan -> patch -> test -> ledger -> boundary

## Required Read Order

1. `README.md`
2. `README_90_SECONDS.md`
3. `docs/protocols/REHYDRATION_PROTOCOL.md`
4. `docs/context/repository_context_index.json`
5. `docs/context/rcc_nexus_index.json`
6. `rcc/nexus/route_map.json`
7. The nearest folder-level `README.md` for touched files, or `FOLDER_README.md` inside reserved metadata folders such as `.github`

## Minimum Validation

Run:

    python -m pytest -q

For CLI-facing changes, also run:

    python -m agentfold.cli --help
    python -m agentfold.cli validate-genome examples/genomes/minimal_agent_genome.json

## Promotion Rules

- No origin alignment, no compounding.
- No transcript, no inheritance.
- No evidence, no claim elevation.
- No ledger continuity, no durable memory promotion.
- No route map, no agent-safe patch.
- No local validation, no health claim.

## Non-Claim Lock

AgentFold does not prove code correctness, security, production readiness, AGI, consciousness, biological equivalence, autonomous authority, or claim truth.
