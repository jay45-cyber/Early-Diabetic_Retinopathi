"""Comprehensive medical screening evaluation metrics."""
from typing import Dict, Any, Tuple
import numpy as np
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    brier_score_loss,
    f1_score
)


def compute_screening_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float = 0.5
) -> Dict[str, Any]:
    """Calculate the full suite of clinical screening evaluation metrics.
    
    Includes:
    - AUROC & AUPRC (threshold-independent discrimination)
    - Sensitivity & Specificity (operating threshold)
    - Precision (PPV) & Negative Predictive Value (NPV)
    - F1-Score & Brier calibration score
    - 2x2 Confusion Matrix breakdown
    """
    y_true = np.asarray(y_true, dtype=np.int32)
    y_prob = np.asarray(y_prob, dtype=np.float32)
    y_pred = (y_prob >= threshold).astype(np.int32)

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    # Clinical rate metrics
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0.0
    f1 = f1_score(y_true, y_pred, zero_division=0)

    # Threshold-independent curves
    try:
        auroc = float(roc_auc_score(y_true, y_prob))
    except ValueError:
        auroc = float("nan")

    try:
        auprc = float(average_precision_score(y_true, y_prob))
    except ValueError:
        auprc = float("nan")

    brier = float(brier_score_loss(y_true, y_prob))

    return {
        "auroc": round(auroc, 4),
        "auprc": round(auprc, 4),
        "sensitivity": round(float(sensitivity), 4),
        "specificity": round(float(specificity), 4),
        "precision": round(float(precision), 4),
        "npv": round(float(npv), 4),
        "f1_score": round(float(f1), 4),
        "brier_score": round(brier, 4),
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
        "operating_threshold": threshold
    }

