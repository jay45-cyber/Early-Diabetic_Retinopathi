"""Tests for patient-level bootstrap confidence intervals."""
import pytest
import numpy as np
import pandas as pd
from src.evaluation.confidence_intervals import compute_patient_bootstrap_ci


def test_patient_bootstrap_ci_computation():
    """Verify that bootstrap confidence intervals return valid interval bounds."""
    records = []
    for i in range(40):
        pid = f"PAT_{i}"
        label = 1 if i < 15 else 0
        prob = 0.8 if label == 1 else 0.2
        # Two eyes per patient
        for eye in ["OD", "OS"]:
            records.append({
                "participant_id": pid,
                "diabetes_label": label,
                "pred_prob": prob + (0.05 if eye == "OS" else -0.05)
            })

    df = pd.DataFrame(records)
    res = compute_patient_bootstrap_ci(df, n_bootstraps=50, random_seed=42)

    assert "auroc_ci" in res
    low, high = res["auroc_ci"]
    assert 0.0 <= low <= high <= 1.0

