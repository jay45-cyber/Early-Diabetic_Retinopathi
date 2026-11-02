"""Patient-level bootstrap confidence intervals for medical screening evaluation."""
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss


def compute_patient_bootstrap_ci(
    df: pd.DataFrame,
    patient_col: str = "participant_id",
    y_true_col: str = "diabetes_label",
    y_prob_col: str = "pred_prob",
    n_bootstraps: int = 1000,
    confidence_level: float = 0.95,
    random_seed: int = 42
) -> Dict[str, Tuple[float, float]]:
    """Compute empirical 95% bootstrap confidence intervals by resampling unique patients."""
    rng = np.random.RandomState(random_seed)
    unique_patients = df[patient_col].unique()
    n_patients = len(unique_patients)

    auroc_scores = []
    auprc_scores = []
    brier_scores = []

    alpha_low = (1.0 - confidence_level) / 2.0 * 100.0
    alpha_high = (1.0 - (1.0 - confidence_level) / 2.0) * 100.0

    # Group dataframe by patient for fast multi-eye lookup
    patient_grouped = df.groupby(patient_col)

    for _ in range(n_bootstraps):
        sampled_pids = rng.choice(unique_patients, size=n_patients, replace=True)
        # Concatenate images for sampled patients
        sample_dfs = [patient_grouped.get_group(pid) for pid in sampled_pids if pid in patient_grouped.groups]
        if not sample_dfs:
            continue
        sample_df = pd.concat(sample_dfs, ignore_index=True)

        y_true = sample_df[y_true_col].values
        y_prob = sample_df[y_prob_col].values

        # AUROC requires at least one positive and one negative sample
        if len(np.unique(y_true)) >= 2:
            try:
                auroc_scores.append(roc_auc_score(y_true, y_prob))
                auprc_scores.append(average_precision_score(y_true, y_prob))
                brier_scores.append(brier_score_loss(y_true, y_prob))
            except ValueError:
                pass

    def get_ci(scores):
        if not scores:
            return (float("nan"), float("nan"))
        return (
            round(float(np.percentile(scores, alpha_low)), 4),
            round(float(np.percentile(scores, alpha_high)), 4)
        )

    return {
        "auroc_ci": get_ci(auroc_scores),
        "auprc_ci": get_ci(auprc_scores),
        "brier_ci": get_ci(brier_scores),
        "n_bootstraps_completed": len(auroc_scores),
        "confidence_level": confidence_level
    }

