"""Tests for evaluation metrics and probability calibration."""
import pytest
import numpy as np
from src.evaluation.classification_metrics import compute_screening_metrics
from src.evaluation.calibration import PlattCalibrator, compute_expected_calibration_error


def test_compute_screening_metrics():
    """Verify standard metric calculations on predictable synthetic outputs."""
    y_true = np.array([1, 1, 0, 0, 1, 0, 0, 1])
    y_prob = np.array([0.9, 0.8, 0.1, 0.2, 0.7, 0.3, 0.4, 0.85])

    metrics = compute_screening_metrics(y_true, y_prob, threshold=0.5)

    assert metrics["auroc"] == 1.0
    assert metrics["sensitivity"] == 1.0
    assert metrics["specificity"] == 1.0
    assert metrics["brier_score"] < 0.1


def test_platt_calibrator_fitting_and_ece():
    """Verify that PlattCalibrator transforms logits and ECE calculates error."""
    val_logits = np.array([-2.0, -1.5, -0.5, 0.5, 1.5, 2.0, 2.5, 3.0])
    val_y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

    calibrator = PlattCalibrator().fit(val_logits, val_y)
    probs = calibrator.predict_proba(val_logits)

    assert len(probs) == len(val_logits)
    assert np.all(probs >= 0.0) and np.all(probs <= 1.0)
    # Calibrated probabilities should be monotonically increasing with logits
    assert np.all(np.diff(probs) >= 0)

    ece_res = compute_expected_calibration_error(val_y, probs, n_bins=4)
    assert 0.0 <= ece_res["expected_calibration_error"] <= 1.0

