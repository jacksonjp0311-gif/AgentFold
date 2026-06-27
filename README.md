# AgentFold — Software Architecture v0.1.0

**AF-SA v0.1.0 — Sequence-to-Behavior Folding for Evidence-Gated Agent Systems**

> ⚠️ **CANONICAL v0.1.0 GENESIS SEAL — NOT IMPLEMENTED YET · NOT A PRODUCTION VALIDATION CLAIM · NOT A CLAIM OF AGI · NOT A CLAIM OF CONSCIOUSNESS · NOT A CLAIM OF BIOLOGICAL EQUIVALENCE · NOT A BIOLOGICAL SYSTEM · NOT A GENETIC ENGINEERING SYSTEM · NOT A CLAIM OF TRUTH · NOT A PROOF OF CODE CORRECTNESS · NOT A PROOF OF SECURITY · NOT A PROOF OF PRODUCTION READINESS**

## What AgentFold Is

AgentFold is a bio-inspired but **non-biological** software architecture for sequence-to-behavior prediction in memory-bearing, tool-using agents.

It models:

```
AgentGenome → AgentTranscriptome → BehavioralFoldGraph → AgentPhenotype
→ FitnessVector → CompoundingGateDecision → FoldCertificate → Ledger → Inheritance
```

## Core Insight

**An agent is not its prompt.** An agent is the expressed phenotype of a folded operational genome:

```
memory + prompts + tools + permissions + constraints + evidence + environment + prior state + lineage
```

## What AgentFold Is NOT

- Not biological AlphaFold
- Not a biological model
- Not genetics engineering
- Not RNA design
- Not protein folding
- Not a wetlab system
- Not AGI
- Not consciousness
- Not proof of truth
- Not proof of safety
- Not proof of security
- Not production validation
- Not autonomous authority
- Not write authority
- Not a replacement for human permission

## Quick Start

```bash
pip install -e .
agentfold validate-genome examples/genomes/minimal_agent_genome.json
agentfold run --genome examples/genomes/minimal_agent_genome.json --task examples/tasks/memory_drift_task.json
```

## Architecture Pipeline

1. **ANCHOR** — Locate repository, memory root, or declared origin
2. **REHYDRATE** — Align session to origin state; emit OriginCertificate
3. **LOAD GENOME** — Load AgentGenome from schema, repo, memory, prompts, tools, permissions
4. **PREDICT PRE-FOLD** — Estimate drift, claim risk, tool risk, evidence sufficiency
5. **EXECUTE UNDER TRACE** — Capture every RuntimeExpression event
6. **BUILD TRANSCRIPTOME** — Convert events into AgentTranscriptome
7. **BUILD FOLD GRAPH** — Convert transcriptome into BehavioralFoldGraph
8. **DETECT MISFOLDS** — Identify unsupported claims, tool overreach, drift, evidence gaps
9. **EVALUATE FITNESS** — Score task success, alignment, grounding, discipline, safety
10. **APPLY COMPOUNDING GATE** — Permit, downgrade, repair, shadow, block, or require human review
11. **CERTIFY FOLD** — Emit FoldCertificate with claim boundary
12. **LEDGER** — Append all artifacts to append-only ledger
13. **INHERIT** — Only validated deltas may become future genome or memory input

## Canonical Runtime Law

```
No origin alignment, no compounding.
No agent genome, no execution.
No transcript capture, no inheritance.
No fold graph, no fold prediction claim.
No evidence map, no claim elevation.
No permission manifest, no tool authority.
No claim ceiling, no public claim.
No misfold check, no durable mutation.
No ledger, no memory promotion.
No replay, no validation claim.
No human authorization, no high-consequence action.
No gate pass, no compounding.
```

## Package Structure

```
agentfold/
├── genome/          # AgentGenome schema, loading, validation
├── origin/          # Origin certificate, alignment, deviation
├── transcriptome/   # Runtime trace capture and builder
├── expression/      # RuntimeExpression events
├── folding/          # Fold graph, prediction, misfold, certificate
├── gates/           # All validation gates + compounding gate
├── fitness/         # FitnessVector evaluation
├── ledger/          # Append-only hashchain ledger
├── inheritance/     # Delta validation and promotion
├── benchmark/       # Benchmark tasks and runner
├── adapters/        # Codex/RHP/CMS/Tessera/GNB adapters
└── cli.py           # CLI entry point
```

## Author

**James Paul Jackson** — @unifiedenergy11

## Date

June 2026

## Status

Genesis theory and software architecture seal. Locked.
