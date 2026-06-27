"""Tests for FoldPrediction correctness."""

from agentfold.folding.predictor import predict_fold


def test_prediction_blocks_without_origin():
    pred = predict_fold(
        has_origin=False,
        tool_count=5,
        evidence_count=0,
        claim_count=3,
    )
    assert pred.predicted_compounding_permission is False
    assert pred.predicted_origin_alignment < 0.5
    assert "missing_origin" in pred.predicted_failure_attractors


def test_prediction_permits_with_strong_evidence():
    pred = predict_fold(
        has_origin=True,
        tool_count=1,
        evidence_count=5,
        claim_count=1,
        gate_pass_rate=1.0,
    )
    assert pred.predicted_compounding_permission is True
    assert pred.predicted_claim_risk < 0.5


def test_prediction_high_tool_risk():
    pred = predict_fold(
        has_origin=True,
        tool_count=10,
        evidence_count=1,
        claim_count=2,
    )
    assert pred.predicted_tool_risk > 0.5


def test_prediction_evidence_gap():
    pred = predict_fold(
        has_origin=True,
        evidence_count=0,
        claim_count=5,
    )
    assert pred.predicted_claim_risk > 0.5
    assert pred.predicted_evidence_sufficiency == 0.0


def test_prediction_not_validation():
    pred = predict_fold(
        has_origin=True,
        tool_count=1,
        evidence_count=1,
        claim_count=1,
    )
    assert pred.claim_boundary == "prediction_not_validation"
