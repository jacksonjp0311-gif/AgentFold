# AgentFold AF-SA v0.1.0 Genesis Source

## Source

Canonical gist:

    https://gist.github.com/jacksonjp0311-gif/2d92eb0f12bba782639460f18a426f42

The gist is the original AgentFold software architecture source. This file records the implementation-facing extraction used by the local repository.

## Core Thesis

AgentFold starts from the thesis that an agent is not just a prompt. Observable behavior is the expressed phenotype of a folded operational genome composed of memory, prompts, tools, permissions, constraints, evidence, environment, prior state, and lineage.

## Architecture Spine

    AgentGenome
    -> AgentTranscriptome
    -> RuntimeExpression
    -> BehavioralFoldGraph
    -> FoldPrediction
    -> AgentPhenotype
    -> FitnessVector
    -> MisfoldEvent
    -> CompoundingGateDecision
    -> FoldCertificate
    -> Ledgered Inheritance

## Source-Bound Implementation Map

| Genesis concept | Current local surface | Status |
|---|---|---|
| AgentGenome contract | `agentfold/genome/` | scaffold implemented |
| AgentTranscriptome contract | `agentfold/transcriptome/` | scaffold implemented |
| RuntimeExpression recorder | `agentfold/expression/`, `agentfold/transcriptome/recorder.py` | scaffold implemented |
| BehavioralFoldGraph | `agentfold/folding/graph_builder.py` | scaffold implemented |
| FoldPrediction | `agentfold/folding/predictor.py` | heuristic implemented |
| AgentPhenotype contract | `agentfold/folding/phenotype.py` | scaffold implemented |
| MisfoldEvent | `agentfold/folding/misfold.py` | scaffold implemented |
| FitnessVector | `agentfold/fitness/` | scaffold implemented |
| CompoundingGateDecision | `agentfold/gates/compounding_gate.py` | scaffold implemented |
| FoldCertificate | `agentfold/folding/certificate.py` | scaffold implemented |
| Append-only ledger | `agentfold/ledger/` | scaffold implemented |
| Ledgered inheritance | `agentfold/inheritance/` | scaffold implemented |
| Replayable evidence packets | planned | not implemented |
| Release functional | planned | not implemented |
| Authority lock matrix | planned | partial gate coverage |
| Authority matrix | `agentfold/authority/matrix.py` | scaffold implemented |
| Replayable fold evidence | `agentfold/evidence/packet.py` | scaffold implemented |
| Local runtime pipeline | `agentfold/runtime/pipeline.py` | scaffold implemented |
| Release functional | `agentfold/release/functional.py` | scaffold implemented |

## Rehydration Geometry Extraction

The gist emphasizes origin geometry, session geometry, deviation, origin certificates, append-only rehydration ledger, and validated delta inheritance.

AgentFold v0.1.1 now exposes:

- `docs/protocols/REHYDRATION_PROTOCOL.md`
- `agentfold/origin/`
- `docs/context/repository_context_index.json`
- `docs/context/rcc_nexus_index.json`
- `rcc/nexus/route_map.json`

Next implementation should make rehydration evidence an emitted artifact, not only a protocol.

## Authority Lock Extraction

The genesis source blocks unauthorized tool calls, memory writes, repository writes, external messages, financial actions, and self-authorized mutations.

Current partial surfaces:

- `agentfold/gates/permission_gate.py`
- `agentfold/gates/tool_gate.py`
- `agentfold/gates/human_authorization_gate.py`
- `agentfold/gates/compounding_gate.py`

Next implementation should add a single authority matrix object that all tool, mutation, memory, repository, communication, and payment gates read from.

## Non-Claim Boundary

AgentFold remains non-biological and non-autonomous. It does not prove truth, correctness, safety, security, AGI, consciousness, biological equivalence, production readiness, or self-authorized authority.
