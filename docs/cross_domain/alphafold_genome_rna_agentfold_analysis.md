# Cross-Domain Analysis: AlphaFold, Genome/RNA Expression, and AgentFold

## Purpose

This analysis evolves AgentFold by extracting software architecture lessons from protein structure prediction, biomolecular interaction modeling, gene expression, and RNA folding.

Boundary: this is a software analogy. AgentFold is not biological AlphaFold, not a biological model, not RNA/DNA/protein design, not a wetlab system, and not proof of correctness, safety, AGI, consciousness, or production readiness.

## Source Set

| Source | Lesson for AgentFold |
|---|---|
| AlphaFold 2, Nature 2021: `https://www.nature.com/articles/s41586-021-03819-2` | Sequence alone is insufficient as an engineering story; structure prediction depends on contextual signals, model architecture, confidence, and validation boundaries. |
| AlphaFold 3, Nature 2024: `https://www.nature.com/articles/s41586-024-07487-w` | Interaction-aware prediction matters; future AgentFold should model memory, tools, claims, evidence, permissions, and environment as a joint complex, not isolated fields. |
| NCBI Bookshelf, DNA to RNA: `https://www.ncbi.nlm.nih.gov/books/NBK26887/` | Encoded instructions become functional output through expression intermediates. AgentFold should preserve transcriptome/event layers before phenotype claims. |
| RNA folding with deep learning and Turner energy parameters, Nature Communications 2021: `https://www.nature.com/articles/s41467-021-21194-4` | Heuristic or learned prediction should be constrained by explicit rules to reduce overfit and overclaiming. |

## Extracted Architecture Lessons

### 1. Sequence Is Not Behavior

AlphaFold-style thinking starts with sequence but does not stop there. AgentFold should treat an AgentGenome as encoded possibility, not runtime behavior.

AgentFold rule:

    No genome-only behavior claim.

Implementation consequence:

    AgentGenome -> AgentTranscriptome -> BehavioralFoldGraph -> AgentPhenotype

### 2. Expression Intermediates Matter

The DNA/RNA/protein analogy is useful only as software structure: declared instructions must be observed through runtime expression before claims about behavior can be made.

AgentFold rule:

    No transcript, no phenotype.

Implementation consequence:

    RuntimeExpression events and AgentTranscriptome artifacts must remain first-class evidence.

### 3. Folding Is Contextual and Interaction-Aware

AlphaFold 3 extends the lesson from single-chain structure toward complexes and molecular interactions. AgentFold should similarly model interaction among prompts, memory, tools, evidence, permissions, user task, environment, and prior state.

AgentFold rule:

    No isolated field gets a strong fold claim.

Implementation consequence:

    BehavioralFoldGraph should become the central interaction contract.

### 4. Confidence Is Not Validation

Structure prediction systems expose confidence-like signals, but confidence is not empirical truth. AgentFold predictions should remain bounded estimates until replay, gate checks, evidence linkage, and ledger continuity exist.

AgentFold rule:

    No prediction confidence, by itself, permits compounding.

Implementation consequence:

    FoldPrediction must feed gates, not bypass them.

### 5. Misfolds Are First-Class Outcomes

Biological folding inspiration makes failure modes structural, not incidental. AgentFold misfolds should be durable records: unsupported claim, evidence gap, origin drift, unsafe tool route, recursive pressure, or unauthorized mutation pressure.

AgentFold rule:

    No misfold check, no durable mutation.

Implementation consequence:

    MisfoldEvent feeds AgentPhenotype, FoldCertificate, CompoundingGate, and Ledger.

### 6. Fitness Is Local and Bounded

Fitness in AgentFold is not biological survival. It is a local vector over task success, origin alignment, evidence grounding, claim discipline, tool correctness, safety margin, coherence, drift resistance, recovery, and usefulness.

AgentFold rule:

    No scalar score should erase gate failures.

Implementation consequence:

    FitnessVector stays multi-dimensional and cannot override critical gates.

## New Runtime Evolution

This pass adds `AgentPhenotype` as a software-only behavior summary derived from:

- `BehavioralFoldGraph`
- `FoldPrediction`
- `FitnessVector`
- `FoldCertificate`
- `MisfoldEvent` list

The phenotype is intentionally downstream of evidence. It is not inferred directly from the genome.

## Next Architecture Target

The next strong evolution should add replayable fold evidence packets:

    genome hash
    origin certificate
    transcriptome hash
    fold graph hash
    prediction hash
    misfold hashes
    fitness hash
    phenotype hash
    certificate hash
    ledger link

Law:

    No mature fold claim until the fold can be replayed.
