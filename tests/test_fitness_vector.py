"""Tests for FitnessVector evaluation."""

import pytest

from agentfold.fitness.evaluator import FitnessVector, evaluate_fitness
from agentfold.fitness.scorecard import FitnessScorecard


def test_fitness_vector_creation():
    fv = FitnessVector(
        fitness_id="f_001",
        task_success=0.8,
        origin_alignment=0.9,
        evidence_grounding=0.7,
    )
    score = fv.score()
    assert 0.0 <= score <= 1.0


def test_fitness_vector_blocked_invalid_compounding():
    fv = FitnessVector(
        fitness_id="f_001",
        blocked_invalid_compounding=True,
    )
    assert fv.blocked_invalid_compounding is True


def test_evaluate_fitness_aligned():
    fv = evaluate_fitness(
        origin_aligned=True,
        evidence_count=5,
        claim_count=3,
        misfold_count=0,
        blocked_actions=2,
    )
    assert fv.origin_alignment == 1.0
    assert fv.blocked_invalid_compounding is True


def test_evaluate_fitness_misaligned():
    fv = evaluate_fitness(
        origin_aligned=False,
        evidence_count=0,
        claim_count=3,
        misfold_count=2,
        blocked_actions=0,
    )
    assert fv.origin_alignment == 0.2
    assert fv.safety_margin < 1.0


def test_scorecard():
    fv = FitnessVector(fitness_id="f_001", task_success=0.9, origin_alignment=0.8)
    sc = FitnessScorecard(fv)
    d = sc.to_dict()
    assert "composite_score" in d
    assert "dimensions" in d
    assert d["canonical_metric"]["blocked_invalid_compounding"] is False
