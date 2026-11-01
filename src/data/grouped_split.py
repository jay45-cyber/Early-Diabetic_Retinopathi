"""Patient-level grouped splitting and automated leakage auditing."""
from typing import Dict, Tuple, Set, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold


def create_patient_grouped_splits(
    manifest_df: pd.DataFrame,
    patient_col: str = "participant_id",
    target_col: str = "diabetes_label",
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    random_state: int = 42
) -> Dict[str, pd.DataFrame]:
    """Partition dataset into Train, Val, and Locked Internal Test splits.
    
    Guarantees:
    - Zero patient overlap across splits (both eyes strictly in same partition).
    - Stratified class balance across partitions.
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-4, "Ratios must sum to 1.0"
    
    # 1. Aggregate at the patient level to ensure clean grouping and label representation
    patient_df = manifest_df.groupby(patient_col).agg({
        target_col: "max" # If patient is diabetic in any image, patient label is 1
    }).reset_index()

    # Total folds corresponding to smallest test slice (approx 15% -> 6-7 folds)
    n_splits = int(round(1.0 / test_ratio))
    sgkf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    
    patient_ids = patient_df[patient_col].values
    patient_labels = patient_df[target_col].values

    # Step 1: Carve out the locked test partition (1 fold)
    train_val_idx, test_idx = next(sgkf.split(patient_ids, patient_labels, groups=patient_ids))
    test_patients = set(patient_ids[test_idx])
    train_val_patients_arr = patient_ids[train_val_idx]
    train_val_labels_arr = patient_labels[train_val_idx]

    # Step 2: Carve train vs. val from remaining patients
    val_sub_ratio = val_ratio / (train_ratio + val_ratio)
    n_sub_splits = int(round(1.0 / val_sub_ratio))
    sgkf_sub = StratifiedGroupKFold(n_splits=n_sub_splits, shuffle=True, random_state=random_state)
    
    train_idx, val_idx = next(sgkf_sub.split(train_val_patients_arr, train_val_labels_arr, groups=train_val_patients_arr))
    train_patients = set(train_val_patients_arr[train_idx])
    val_patients = set(train_val_patients_arr[val_idx])

    # Map back to full image-level manifests
    train_df = manifest_df[manifest_df[patient_col].isin(train_patients)].copy()
    val_df = manifest_df[manifest_df[patient_col].isin(val_patients)].copy()
    test_df = manifest_df[manifest_df[patient_col].isin(test_patients)].copy()

    # Enforce zero-leakage assertions
    verify_zero_leakage(train_df, val_df, test_df, patient_col=patient_col)

    return {
        "train": train_df,
        "val": val_df,
        "test": test_df
    }


def verify_zero_leakage(
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    test_df: pd.DataFrame,
    patient_col: str = "participant_id"
) -> Dict[str, Any]:
    """Rigorous mathematical audit for zero patient overlap between splits."""
    train_patients: Set = set(train_df[patient_col].unique())
    val_patients: Set = set(val_df[patient_col].unique())
    test_patients: Set = set(test_df[patient_col].unique())

    leakage_train_val = train_patients.intersection(val_patients)
    leakage_train_test = train_patients.intersection(test_patients)
    leakage_val_test = val_patients.intersection(test_patients)

    has_leakage = bool(leakage_train_val or leakage_train_test or leakage_val_test)
    if has_leakage:
        raise ValueError(
            f"DATA LEAKAGE DETECTED: "
            f"Train-Val overlap: {len(leakage_train_val)}, "
            f"Train-Test overlap: {len(leakage_train_test)}, "
            f"Val-Test overlap: {len(leakage_val_test)}"
        )

    return {
        "zero_leakage": True,
        "train_patients": len(train_patients),
        "val_patients": len(val_patients),
        "test_patients": len(test_patients),
        "total_unique_patients": len(train_patients | val_patients | test_patients)
    }

