<div align="center">

# 🧬 AgentFold

### *Evidence-Gated Agent Folding Runtime* 
<img width="458" height="261" alt="image" src="https://github.com/user-attachments/assets/66eabcc8-6270-42d4-9802-faa22db27dc9" />


**Sequence-to-Behavior Inspection for Memory-Bearing, Tool-Using AI Agents**

[![Tests](https://img.shields.io/badge/tests-87%20passed-brightgreen?style=flat-square)](https://github.com/jacksonjp0311-gif/AgentFold)
[![Version](https://img.shields.io/badge/version-AF--SA%20v1.4.0-blue?style=flat-square)](https://github.com/jacksonjp0311-gif/AgentFold)
[![License](https://img.shields.io/license-MIT-purple?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-cyan?style=flat-square)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-Release%20Candidate%20Validation-orange?style=flat-square)](https://github.com/jacksonjp0311-gif/AgentFold)

<p align="center"><em>Not biological AlphaFold. Not AGI. Not consciousness. A bounded, evidence-gated scaffold for inspecting what your agent actually does.</em></p>

---

> 🔬 **AgentFold tests a single, rigorous question:** *Can an agent run declare its genome, align to origin, execute under trace, build a behavioral fold graph, detect misfolds, score fitness, gate compounding, write an append-only ledger, and admit only validated deltas into inheritance?*

</div>

---

## ✨ Why AgentFold?

Most agent observability tools tell you *what happened*. AgentFold tells you **what was allowed, what was gated, what drifted, and what got promoted** — with cryptographic evidence at every step.

Think of it as a **folding microscope** for agent behavior:

| What other tools do | What AgentFold does |
|---|---|
| Log events | 🔗 Hash-chain linked ledger with append-only integrity |
| Flag errors | 🧬 Misfold detection — structural, not just statistical |
| Track prompts | 🧬 Full genome → origin → transcriptome → fold graph pipeline |
| Report metrics | 🎯 Compounding gates with evidence replay and drift checks |
| Trust the agent | 🚫 Authority matrix blocks unsafe promotion by design |

---

## 🏗️ Architecture: The Folding Pipeline

```
    ┌─────────────────────────────────────────────────────────────────┐
    │                     AGENTFOLD RUNTIME v1.4.0                    │
    │                  Sequence-to-Behavior Folding                    │
    └─────────────────────────────────────────────────────────────────┘

    🧬 AgentGenome          Declare the substrate
         │                   (prompts, memory, tools, permissions,
         ▼                    constraints, evidence, lineage)
    🔐 OriginCertificate    Anchor to declared origin
         │                   (alignment check, deviation scan)
         ▼
    📋 AgentTranscriptome    Capture runtime expression events
         │                   (prompt, memory, tool, claim, gate, output)
         ▼
    🔬 BehavioralFoldGraph  Build causal/semantic graph
         │                   (sequence → behavior mapping)
         ▼
    ⚠️  MisfoldEvents        Detect structural drift
         │                   (origin drift, claim overreach,
         ▼                    evidence gaps, unsafe compounding)
    📊 FitnessVector         Score multi-dimensional fitness
         │                   (bounded, not overclaimed)
         ▼
    🚦 CompoundingGate       Permit / warn / repair / shadow / block
         │                   (evidence-gated decision)
         ▼
    📜 FoldCertificate       Emit signed certificate
         │                   (replayable, verifiable)
         ▼
    📒 Ledger                Append-only JSONL with hash linkage
         │                   (durable, portable)
         ▼
    🧬 Inheritance           Promote only validated deltas
                           (block unsafe mutation by default)
```

---

## 🚀 Quick Start

```bash
# Install locally
pip install -e .

# Explore the CLI
python -m agentfold.cli --help

# Validate an AgentGenome
python -m agentfold.cli validate-genome examples/genomes/minimal_agent_genome.json

# Run the full pipeline (dry-run)
python -m agentfold.cli run examples/genomes/minimal_agent_genome.json \
    --task examples/tasks/memory_drift_task.json

# Run the test suite
python -m pytest -q
```

---

## 🧠 What AgentFold Tests

| Capability | What It Proves |
|---|---|
| 🧬 **Genome Validation** | Declared substrate has required IDs, claim ceiling, tools, permissions, and evidence boundaries |
| 🔐 **Origin Alignment** | Session can anchor to declared origin before any compounding is allowed |
| 📋 **Transcript Capture** | Runtime expression events are recorded before inheritance is permitted |
| 🔬 **Fold Graph Construction** | Observed events become a causal/semantic graph — not just a log |
| ⚠️  **Misfold Detection** | Origin drift, claim overreach, evidence gaps, and unsafe compounding signals are caught |
| 🚦 **Compounding Gate** | Permits, warns, repairs, shadows, blocks, or requires human review — no silent promotion |
| 📒 **Ledger Continuity** | Append-only JSONL entries with hash chain verification |
| 🧬 **Inheritance Controls** | Only validated deltas are promoted — unsafe mutation is blocked by default |

**AgentFold rewards bounded evidence emission and durable auditability — never confident overclaiming.**

---

## 🗺️ Repository Navigation

This repo uses the **RCC-N navigation shell** for human and AI orientation:

### 📖 Three-Layer README

| Layer | Purpose | For Whom |
|---|---|---|
| **PART I — Human README** | Quick start, architecture, tests | Developers, reviewers |
| **PART II — RCC Nexus** | Route maps, context indexes, governance | AI agents, CI systems |
| **PART III — AI Agent** | Operating rules, patch routes, update policy | Autonomous agents |

---

# PART I - Human README

## Current Identity

AgentFold is a local Python package for testing whether agent behavior can be bounded by declared substrate and evidence:

- declare an AgentGenome,
- certify origin alignment,
- capture runtime expression events,
- build an AgentTranscriptome,
- construct a BehavioralFoldGraph,
- predict risk before or during folding,
- detect misfolds,
- evaluate fitness,
- apply compounding gates,
- emit fold certificates,
- append ledger records,
- block unsafe inheritance,
- preserve non-claim boundaries.

The current repo is a scaffold with working local tests. It is not a production agent runtime.

## What AgentFold Tests

| Task | Purpose |
|---|---|
| Genome validation | Ensures declared agent substrate has required IDs, claim ceiling, tools, permissions, and evidence boundaries. |
| Origin alignment | Blocks compounding when the session cannot anchor to declared origin. |
| Transcript capture | Records runtime expression events before inheritance is allowed. |
| Fold graph construction | Converts observed events into a causal/semantic graph. |
| Misfold detection | Detects origin drift, claim overreach, evidence gaps, and unsafe compounding signals. |
| Compounding gate | Permits, warns, repairs, shadows, blocks, or requires human review. |
| Ledger continuity | Writes append-only JSONL entries with hash linkage. |
| Inheritance controls | Promotes only validated deltas. |

AgentFold rewards bounded evidence emission and durable auditability, not confident overclaiming.

## Genesis Source Alignment

The original AF-SA v0.1.0 gist is now treated as the canonical architecture source for future evolution:

> 📎 **Genesis Source:** https://gist.github.com/jacksonjp0311-gif/2d92eb0f12bba782639460f18a426f42

AgentFold v0.1.1 implements only the local scaffold and repository geometry around that source. The next evolution path is to move more of the genesis architecture from prose into validated runtime surfaces: replayable evidence packets, phenotype records, fold certificates, release functionals, authority locks, and transcript-to-ledger inheritance.

**Boundary:** Source alignment preserves intent and traceability. It does not prove that every architectural concept is implemented yet.

## Current Hardening Layer

The current hardening layer includes:

- README trisection,
- 90-second orientation file,
- rehydration protocol,
- route map and context indexes,
- mini README Echo Location records,
- working Click CLI,
- repaired tests,
- enum-safe misfold events,
- hashchain continuation across writer instances,
- origin certificate construction compatible with tests,
- explicit non-claim lock.

## Project Structure

```
agentfold/
├── agentfold/                    # Core Python package
│   ├── genome/                   # AgentGenome schema, loading, validation, hashing
│   ├── origin/                   # Origin certificates, alignment, deviation
│   ├── transcriptome/             # Runtime trace capture and transcript schema
│   ├── expression/               # Runtime expression events
│   ├── folding/                  # Fold graph, prediction, misfolds, certificates
│   ├── gates/                    # Origin, evidence, permission, claim, replay, ledger, compounding gates
│   ├── fitness/                  # Fitness scorecards and evaluator
│   ├── ledger/                   # JSONL append-only ledger and hashchain verification
│   ├── inheritance/              # Delta validation, blocking, promotion
│   ├── authority/                # Authority matrix for mutation surface control
│   ├── evidence/                 # Replayable evidence packets
│   ├── ci/                       # CI policy, verifier, summaries
│   ├── release/                  # Release validator and functional
│   ├── reports/                  # Markdown evidence report renderer
│   ├── schemas/                  # JSON Schema export
│   ├── runtime/                  # Full pipeline orchestration
│   ├── instrumentation/          # Session recorder and guarded tool wrapper
│   ├── benchmark/                # Benchmark task scaffolding
│   └── adapters/                 # Codex, CMS, Tessera, RHP, GNB adapters
├── docs/
│   ├── context/                  # Repository and RCC Nexus indexes
│   ├── cross_domain/             # Bounded AlphaFold/genome/RNA analysis
│   ├── protocols/               # Rehydration and operating protocols
│   ├── roadmap/                  # Evolution roadmap
│   └── software_architecture/   # Source-bound architecture records
├── rcc/nexus/                    # Route maps and navigation shell
├── examples/
│   ├── genomes/                  # Example AgentGenome files
│   └── tasks/                    # Example task definitions
├── benchmarks/                   # Misfold fixtures and adversarial tests
├── tests/                        # 87 passing validation tests
├── releases/                     # Release candidate manifests and seals
└── reports/                      # Generated evidence reports
```

---

# PART II - RCC Nexus README

## RCC Nexus Purpose

The RCC Nexus layer makes AgentFold orientable to humans and AI agents by exposing:

- repository identity,
- route maps,
- folder responsibilities,
- validation surfaces,
- non-claim boundaries,
- rehydration order,
- safe patch routes.

## Nexus Entry Points

| Entry | Purpose |
|---|---|
| `docs/context/repository_context_index.json` | Machine-readable repository map. |
| `docs/context/rcc_nexus_index.json` | RCC-N navigation and governance index. |
| `rcc/nexus/route_map.json` | Route map from intent to files and validation. |
| `docs/protocols/REHYDRATION_PROTOCOL.md` | Agent rehydration and safe-work protocol. |

## Echo Location Block

Repository self-location:

```
repo: agentfold
layer: AF-SA v1.4.0
role: evidence-gated agent folding scaffold
primary package: agentfold
validation: python -m pytest -q
boundary: local scaffold validation only
```

## RCC-N Boundary

RCC-N improves navigation and patch safety. It does not prove:

- code correctness,
- security,
- empirical validity,
- production readiness,
- AI understanding,
- agent autonomy,
- truth of claims,
- biological equivalence.

---

# PART III - AI Agent README

## Required Read Order

1. `README.md`
2. `README_90_SECONDS.md`
3. `docs/protocols/REHYDRATION_PROTOCOL.md`
4. `docs/context/repository_context_index.json`
5. `docs/context/rcc_nexus_index.json`
6. `rcc/nexus/route_map.json`
7. Local folder README for the files being changed

## Agent Operating Rules

- Preserve user changes.
- Inspect `git status --short --branch` before edits.
- Do not promote claims beyond local validation.
- Do not imply AGI, consciousness, biological equivalence, production readiness, or autonomous authority.
- Keep edits scoped to the route being touched.
- Run `python -m pytest -q` before claiming the repo is healthy.
- Update mini READMEs when adding folders.
- Update context indexes when adding major surfaces.

## Patch Routes

| Intent | Route |
|---|---|
| Genome/schema changes | `agentfold/genome/`, then genome tests |
| Origin/rehydration changes | `agentfold/origin/`, `docs/protocols/`, then origin tests |
| Runtime transcript changes | `agentfold/transcriptome/`, `agentfold/expression/`, then transcript tests |
| Fold graph/misfold changes | `agentfold/folding/`, `agentfold/gates/misfold_gate.py`, then folding/misfold tests |
| Gate changes | `agentfold/gates/`, then gate and compounding tests |
| Ledger changes | `agentfold/ledger/`, then ledger tests |
| Documentation shell changes | `README.md`, `README_90_SECONDS.md`, `docs/context/`, `rcc/nexus/`, folder READMEs, then documentation tests |

## AI README Update Policy

Every structural change should update three surfaces:

1. Human explanation if user-facing behavior changes.
2. RCC route/index files if navigation changes.
3. Folder README if local responsibility changes.

Boundary: README updates improve orientation. They do not substitute for tests, review, or evidence.

---

## 📊 Current Health Snapshot

| Surface | Status |
|---|---|
| 🧪 **Unit Tests** | ✅ 87 passed |
| 💻 **CLI** | ✅ Full command group (15 commands) |
| 🧬 **Genome Validation** | ✅ Working with example |
| 🔁 **Rehydration Protocol** | ✅ Documented and tested |
| 🗺️ **Route Map** | ✅ `rcc/nexus/route_map.json` |
| 📋 **Context Indexes** | ✅ Repository + RCC Nexus |
| 🔬 **AgentPhenotype** | ✅ Implemented |
| 🛡️ **Authority Matrix** | ✅ Implemented |
| 📦 **Evidence Packet Replay** | ✅ Implemented |
| 📝 **Markdown Reports** | ✅ Implemented |
| 📐 **JSON Schema Export** | ✅ Implemented |
| 🎛️ **Session Recorder API** | ✅ Implemented |
| 🔒 **Guarded Tool Wrapper** | ✅ Implemented |
| ✅ **CI Verifier** | ✅ Implemented |
| 🧩 **Misfold Fixture Pack** | ✅ Implemented |
| 🚀 **Release Validator** | ✅ Implemented |
| 📒 **Non-Claim Lock** | ✅ Active |

---

## 📜 Canonical Runtime Law

```
No origin alignment,      no compounding.
No agent genome,          no execution.
No transcript capture,    no inheritance.
No fold graph,            no fold prediction claim.
No evidence map,          no claim elevation.
No permission manifest,   no tool authority.
No claim ceiling,         no public claim.
No misfold check,         no durable mutation.
No ledger,                no memory promotion.
No replay,                no validation claim.
No human authorization,   no high-consequence action.
No gate pass,             no compounding.
```

---

## 🔄 Rehydration Protocol

AgentFold rehydration is the process of restoring local context before an agent makes code, claim, or inheritance changes.

Canonical sequence:

```
anchor → read → index → route → validate → inspect → plan → patch → test → ledger → boundary
```

**Minimum local sequence:**

1. ⚓ Anchor to repo root
2. 📖 Read `README.md`
3. ⚡ Read `README_90_SECONDS.md`
4. 🔄 Read `docs/protocols/REHYDRATION_PROTOCOL.md`
5. 🗂️ Read `docs/context/repository_context_index.json`
6. 🧭 Read `docs/context/rcc_nexus_index.json`
7. 🗺️ Read `rcc/nexus/route_map.json`
8. 🔍 Inspect `git status --short --branch`
9. ✅ Run `python -m pytest -q`
10. 🔒 Keep all claims inside the non-claim lock

---

## 🧬 Cross-Domain Evolution Layer

AgentFold includes a **bounded** cross-domain analysis from AlphaFold, genome/RNA expression, and RNA folding:

| Biological Lesson | Software Adaptation |
|---|---|
| Sequence ≠ behavior | Genome validation before execution |
| Expression intermediates matter | Transcript capture at runtime |
| Fold prediction is contextual | Behavioral fold graph construction |
| Confidence ≠ validation | Evidence gates, not score thresholds |
| Misfolds are structural | Misfold detection, not just anomaly flags |
| Fitness is multi-dimensional | Bounded fitness vector, not single metric |

> 🚫 **Boundary:** Biology supplies architecture metaphors and cautionary constraints. AgentFold does **not** model proteins, DNA, RNA, molecular complexes, wetlab systems, AGI, consciousness, or biological equivalence.

---

## 🔮 Evolution Law

```
Rehydrate the origin.
Measure the missing surface.
Repair the drift.
Validate the repair.
Write the ledger.
Preserve the boundary.
```

---

## 🚫 What AgentFold Is NOT

Not biological AlphaFold · Not a biological model · Not genetic engineering · Not RNA design · Not protein folding · Not a wetlab system · Not AGI · Not consciousness · Not proof of truth · Not proof of safety · Not proof of security · Not production validation · Not autonomous authority · Not write authority · Not a replacement for human permission.

---

## 👤 Author

**James Paul Jackson** — [@unifiedenergy11](https://github.com/jacksonjp0311-gif)

---

## 📅 Status

**AF-SA v1.4.0 — Release Candidate Validation Checkpoint** · June 2026

📄 MIT License · [Genesis Source](https://gist.github.com/jacksonjp0311-gif/2d92eb0f12bba782639460f18a426f42)
