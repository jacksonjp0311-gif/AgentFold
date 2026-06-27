# AgentFold in 90 Seconds

AgentFold is a local-first evidence-gated agent folding runtime.

It preserves the agent-behavior spine:

    AgentGenome
    -> OriginCertificate
    -> AgentTranscriptome
    -> BehavioralFoldGraph
    -> MisfoldEvents
    -> FitnessVector
    -> CompoundingGateDecision
    -> Ledger
    -> Inheritance

Current layer:

    AF-SA v1.4.0
    release candidate validation checkpoint

It adds Codex/RCC governance:

    rehydration
    -> route map
    -> mini READMEs
    -> evidence gates
    -> non-claim lock
    -> local validation

It now uses the OMN/AERMA README shell:

    PART I - Human README
    PART II - RCC Nexus README
    PART III - AI Agent README

Run:

    pip install -e .
    python -m agentfold.cli --help
    python -m agentfold.cli validate-genome examples/genomes/minimal_agent_genome.json
    python -m pytest -q

Core rule:

    No origin alignment, no compounding.
    No transcript, no inheritance.
    No fold graph, no fold prediction claim.
    No evidence, no claim elevation.
    No route map, no agent-safe patch.

Canonical docs:

- `README.md`
- `docs/protocols/REHYDRATION_PROTOCOL.md`
- `docs/software_architecture/agentfold_sa_v0_1_0_genesis_source.md`
- `docs/cross_domain/alphafold_genome_rna_agentfold_analysis.md`
- `docs/cross_domain/cross_domain_mapping.json`
- `docs/roadmap/agentfold_evolution_roadmap.md`
- `releases/agentfold_v1_0_0_local_release_seal.json`
- `docs/context/repository_context_index.json`
- `docs/context/rcc_nexus_index.json`
- `rcc/nexus/route_map.json`

Original architecture source:

    https://gist.github.com/jacksonjp0311-gif/2d92eb0f12bba782639460f18a426f42

Boundary:

AgentFold improves local traceability, route discipline, and evidence-gated development. It does not prove code correctness, security, production readiness, AGI, consciousness, biological equivalence, autonomous authority, or claim truth.
