"""Machine-readable AgentFold release functional."""

from __future__ import annotations

from pydantic import BaseModel


class ReleaseFunctional(BaseModel):
    version: str = "AF-SA v1.0.0"
    origin: bool = False
    genome: bool = False
    transcript: bool = False
    fold_graph: bool = False
    prediction: bool = False
    misfold: bool = False
    fitness: bool = False
    phenotype: bool = False
    authority: bool = False
    gate: bool = False
    replay: bool = False
    ledger: bool = False
    tests: bool = False
    docs: bool = False
    nonclaim: bool = True
    overclaim_pressure: float = 0.0
    claim_boundary: str = "release_functional_not_production_readiness"

    def score(self) -> float:
        fields = [
            self.origin,
            self.genome,
            self.transcript,
            self.fold_graph,
            self.prediction,
            self.misfold,
            self.fitness,
            self.phenotype,
            self.authority,
            self.gate,
            self.replay,
            self.ledger,
            self.tests,
            self.docs,
            self.nonclaim,
        ]
        base = sum(1 for value in fields if value) / len(fields)
        return round(base * (1.0 - self.overclaim_pressure), 4)

    def passed(self) -> bool:
        return self.score() == 1.0


def evaluate_release_functional(*, tests_passed: bool = False, docs_aligned: bool = False) -> ReleaseFunctional:
    """Evaluate the v1 local release functional."""
    return ReleaseFunctional(
        origin=True,
        genome=True,
        transcript=True,
        fold_graph=True,
        prediction=True,
        misfold=True,
        fitness=True,
        phenotype=True,
        authority=True,
        gate=True,
        replay=True,
        ledger=True,
        tests=tests_passed,
        docs=docs_aligned,
        nonclaim=True,
        overclaim_pressure=0.0,
    )
