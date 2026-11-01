"""Patient manifest schema validation and inventory builder."""
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd

REQUIRED_COLUMNS = [
    "participant_id",
    "image_id",
    "eye_side",
    "image_path",
    "dataset_id",
    "diabetes_label",
    "diabetes_label_source",
    "dr_grade"
]

VALID_EYE_SIDES = {"OD", "OS", "Unknown"}
VALID_LABEL_SOURCES = {
    "Laboratory_HbA1c",
    "Laboratory_FPG",
    "EHR_Diagnosis",
    "Self_Report",
    "Unknown"
}


def validate_manifest(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate manifest against medical research standards.
    
    Checks:
    - Required schema columns.
    - Missing participant IDs or image paths.
    - Bilateral eye side validity.
    - Ground truth label integrity (0 or 1, no invalid types).
    - DR grade ranges (0-4).
    """
    issues: List[str] = []

    # 1. Column existence
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        issues.append(f"Missing mandatory columns: {missing_cols}")
        return {"valid": False, "issues": issues}

    # 2. Null participant IDs or image paths
    if df["participant_id"].isnull().any():
        issues.append(f"Found {df['participant_id'].isnull().sum()} null participant IDs.")
    if df["image_path"].isnull().any():
        issues.append(f"Found {df['image_path'].isnull().sum()} null image paths.")

    # 3. Duplicate image_ids
    dup_images = df["image_id"].duplicated().sum()
    if dup_images > 0:
        issues.append(f"Found {dup_images} duplicate image_id entries.")

    # 4. Eye side validation
    invalid_eyes = ~df["eye_side"].astype(str).isin(VALID_EYE_SIDES)
    if invalid_eyes.any():
        issues.append(f"Found {invalid_eyes.sum()} records with invalid eye_side values.")

    # 5. Diabetes label validity
    valid_labels = df["diabetes_label"].dropna().isin([0, 1])
    if not valid_labels.all():
        issues.append(f"Found non-binary values in diabetes_label.")

    # 6. DR grade range
    valid_dr = df["dr_grade"].dropna().isin([0, 1, 2, 3, 4])
    if not valid_dr.all():
        issues.append(f"Found out-of-range values in dr_grade (expected 0-4).")

    # 7. Summary metrics
    summary = {
        "valid": len(issues) == 0,
        "total_records": len(df),
        "unique_participants": int(df["participant_id"].nunique()),
        "diabetic_count": int((df["diabetes_label"] == 1).sum()),
        "non_diabetic_count": int((df["diabetes_label"] == 0).sum()),
        "dr_grade_0_count": int((df["dr_grade"] == 0).sum()),
        "dr0_diabetic_count": int(((df["dr_grade"] == 0) & (df["diabetes_label"] == 1)).sum()),
        "issues": issues
    }

    return summary

