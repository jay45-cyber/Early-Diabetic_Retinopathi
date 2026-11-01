"""Automated unit tests for patient grouping and zero data leakage."""
import pytest
import pandas as pd
from src.data.grouped_split import create_patient_grouped_splits, verify_zero_leakage


def create_synthetic_manifest(num_patients: int = 100) -> pd.DataFrame:
    """Generate synthetic manifest where each patient has bilateral images (OD and OS)."""
    records = []
    for i in range(num_patients):
        pid = f"PATIENT_{i:04d}"
        label = 1 if i % 4 == 0 else 0 # 25% diabetic prevalence
        dr = 0 if i % 2 == 0 else 1
        
        # Bilateral eyes
        for eye in ["OD", "OS"]:
            records.append({
                "participant_id": pid,
                "image_id": f"IMG_{pid}_{eye}",
                "eye_side": eye,
                "image_path": f"data/raw/{pid}_{eye}.jpg",
                "dataset_id": "TEST_DATASET",
                "diabetes_label": label,
                "diabetes_label_source": "Laboratory_HbA1c",
                "dr_grade": dr
            })
    return pd.DataFrame(records)


def test_patient_grouping_zero_leakage():
    """Verify that patient-level splitting guarantees zero overlap across train, val, and test."""
    manifest_df = create_synthetic_manifest(num_patients=60)
    splits = create_patient_grouped_splits(manifest_df, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15)

    train_df = splits["train"]
    val_df = splits["val"]
    test_df = splits["test"]

    # Test that patient sets are mutually disjoint
    train_patients = set(train_df["participant_id"])
    val_patients = set(val_df["participant_id"])
    test_patients = set(test_df["participant_id"])

    assert len(train_patients.intersection(val_patients)) == 0, "Leakage between Train and Val"
    assert len(train_patients.intersection(test_patients)) == 0, "Leakage between Train and Test"
    assert len(val_patients.intersection(test_patients)) == 0, "Leakage between Val and Test"

    # Test both eyes of every patient remain in the same partition
    for pid in train_patients:
        patient_records = manifest_df[manifest_df["participant_id"] == pid]
        assert len(patient_records) == len(train_df[train_df["participant_id"] == pid]), "Eye split leaked!"


def test_leakage_detector_fails_on_overlap():
    """Verify that verify_zero_leakage raises ValueError when overlap is injected."""
    manifest_df = create_synthetic_manifest(num_patients=20)
    train_df = manifest_df.iloc[:10]
    val_df = manifest_df.iloc[8:18] # Deliberate overlap on index 8 and 9

    with pytest.raises(ValueError, match="DATA LEAKAGE DETECTED"):
        verify_zero_leakage(train_df, val_df, pd.DataFrame(columns=manifest_df.columns))

