# AgentFold Docs Registry

## Canonical Read Order

1. `README.md`
2. `README_90_SECONDS.md`
3. `docs/protocols/REHYDRATION_PROTOCOL.md`
4. `docs/context/repository_context_index.json`
5. `docs/context/rcc_nexus_index.json`
6. `rcc/nexus/route_map.json`
7. `docs/software_architecture/agentfold_sa_v0_1_0_genesis_source.md`
8. `docs/cross_domain/alphafold_genome_rna_agentfold_analysis.md`
9. `docs/roadmap/agentfold_evolution_roadmap.md`

## Validation Commands

    python -m pytest -q
    python -m agentfold.cli --help
    python -m agentfold.cli validate-genome examples/genomes/minimal_agent_genome.json
    python -m agentfold.cli release-validate

## Boundary

The docs registry improves release orientation. It does not prove production readiness.
