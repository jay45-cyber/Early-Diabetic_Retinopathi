"""Subgroup stratification and clinical covariate performance evaluation."""
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from src.evaluation.classification_metrics import compute_screening_metrics


def evaluate_subgroups(
    df: pd.DataFrame,
    y_true_col: str = "diabetes_label",
    y_prob_col: str = "pred_prob",
    subgroup_cols: List[str] | None = None
) -> Dict[str, Any]:
    """Evaluate screening performance across clinical and demographic subgroups.
    
    Primary subgroups evaluated:
    - No Visible Retinopathy (dr_grade == 0)
    - Biological Sex (Female vs. Male)
    - Age Brackets (<45, 45-60, >60)
    """
    if subgroup_cols is None:
        subgroup_cols = ["dr_grade", "sex", "age_bracket"]

    results: Dict[str, Any] = {}

    # 1. Primary clinical subgroup: DR = 0 (No Diabetic Retinopathy)
    if "dr_grade" in df.columns:
        dr0_mask = df["dr_grade"] == 0
        if dr0_mask.sum() > 0:
            y_true_dr0 = df.loc[dr0_mask, y_true_col].values
            y_prob_dr0 = df.loc[dr0_mask, y_prob_col].values
            results["subgroup_dr_grade_0"] = {
                "n_samples": int(dr0_mask.sum()),
                "metrics": compute_screening_metrics(y_true_dr0, y_prob_dr0)
            }

    # 2. Demographic sex stratification
    if "sex" in df.columns:
        results["sex_stratification"] = {}
        for s in df["sex"].dropna().unique():
            mask = df["sex"] == s
            if mask.sum() > 10:
                results["sex_stratification"][str(s)] = {
                    "n_samples": int(mask.sum()),
                    "metrics": compute_screening_metrics(
                        df.loc[mask, y_true_col].values,
                        df.loc[mask, y_prob_col].values
                    )
                }

    return results

