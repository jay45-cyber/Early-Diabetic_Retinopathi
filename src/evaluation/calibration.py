"""Probability calibration and reliability evaluation."""
from typing import Dict, Any, Tuple
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import calibration_curve


class PlattCalibrator:
    """Post-hoc Platt scaling calibrator fitted on validation logits."""

    def __init__(self):
        self.model = LogisticRegression(C=1.0, solver="lbfgs")
        self.is_fitted = False

    def fit(self, val_logits: np.ndarray, val_y: np.ndarray) -> "PlattCalibrator":
        """Fit univariate logistic regression on raw logits."""
        logits = np.asarray(val_logits, dtype=np.float32).reshape(-1, 1)
        labels = np.asarray(val_y, dtype=np.int32)
        self.model.fit(logits, labels)
        self.is_fitted = True
        return self

    def predict_proba(self, logits: np.ndarray) -> np.ndarray:
        """Transform raw uncalibrated logits into calibrated probabilities."""
        if not self.is_fitted:
            raise RuntimeError("PlattCalibrator must be fitted before predict_proba.")
        x = np.asarray(logits, dtype=np.float32).reshape(-1, 1)
        return self.model.predict_proba(x)[:, 1]


def compute_expected_calibration_error(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10
) -> Dict[str, Any]:
    """Calculate Expected Calibration Error (ECE) and reliability curve bins."""
    y_true = np.asarray(y_true, dtype=np.int32)
    y_prob = np.asarray(y_prob, dtype=np.float32)

    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy="uniform")

    # Bin-wise weighted absolute calibration gap
    bin_edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    total_samples = len(y_true)

    for i in range(n_bins):
        in_bin = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i + 1])
        bin_count = np.sum(in_bin)
        if bin_count > 0:
            bin_acc = np.mean(y_true[in_bin])
            bin_conf = np.mean(y_prob[in_bin])
            ece += (bin_count / total_samples) * abs(bin_acc - bin_conf)

    return {
        "expected_calibration_error": round(float(ece), 4),
        "prob_true": prob_true.tolist(),
        "prob_pred": prob_pred.tolist(),
        "n_bins": n_bins
    }

