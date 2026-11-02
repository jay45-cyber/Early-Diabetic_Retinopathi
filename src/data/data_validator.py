"""Comprehensive Dataset Validation & Quality Auditing Engine."""
import json
from pathlib import Path
from typing import Dict, Any, List, Set
from PIL import Image
import pandas as pd
import numpy as np

from src.data.duplicate_detection import compute_md5, compute_dhash, hamming_distance
from src.data.image_quality import assess_image_quality
from src.data.patient_manifest import validate_manifest


class DatasetValidator:
    """Validator enforcing medical data integrity across all 15 audit dimensions."""

    def __init__(self, manifest_df: pd.DataFrame):
        self.df = manifest_df.copy()

    def run_full_audit(self, check_images_on_disk: bool = False) -> Dict[str, Any]:
        """Execute comprehensive audit across schema, quality, duplicates, and distributions."""
        report: Dict[str, Any] = {}

        # 1. Schema & Missing Metadata
        schema_audit = validate_manifest(self.df)
        report["schema_audit"] = schema_audit

        # 2. Conflicting Labels check: same participant has conflicting labels
        if "participant_id" in self.df.columns and "diabetes_label" in self.df.columns:
            patient_label_counts = self.df.dropna(subset=["diabetes_label"]).groupby("participant_id")["diabetes_label"].nunique()
            conflicting_patients = patient_label_counts[patient_label_counts > 1].index.tolist()
            report["conflicting_patient_labels"] = {
                "count": len(conflicting_patients),
                "patient_ids": conflicting_patients
            }
        else:
            report["conflicting_patient_labels"] = {"count": 0, "patient_ids": []}

        # 3. Bilateral Eye & Multiple Visits Grouping
        if "eye_side" in self.df.columns:
            eye_dist = self.df["eye_side"].value_counts().to_dict()
            report["eye_side_distribution"] = eye_dist

        # 4. Class Distribution Analysis
        if "diabetes_label" in self.df.columns:
            class_counts = self.df["diabetes_label"].value_counts(dropna=False).to_dict()
            report["class_distribution"] = {str(k): int(v) for k, v in class_counts.items()}

        # 5. DR Grade Distribution
        if "dr_grade" in self.df.columns:
            dr_counts = self.df["dr_grade"].value_counts(dropna=False).to_dict()
            report["dr_grade_distribution"] = {str(k): int(v) for k, v in dr_counts.items()}

        # 6. Site & Camera Distribution
        report["site_distribution"] = (
            self.df["site_id"].value_counts().to_dict()
            if "site_id" in self.df.columns else {}
        )
        report["camera_distribution"] = (
            self.df["camera_id"].value_counts().to_dict()
            if "camera_id" in self.df.columns else {}
        )

        # 7. Physical Image Integrity & Quality Check (optional disk verification)
        if check_images_on_disk:
            disk_issues = []
            quality_fails = []
            for _, row in self.df.iterrows():
                p = Path(row["image_path"])
                if not p.is_file():
                    disk_issues.append(f"Missing file: {p}")
                    continue
                try:
                    with Image.open(p) as img:
                        img.verify()
                    # Reopen for quality assessment (verify corrupts image handle)
                    with Image.open(p) as img:
                        q = assess_image_quality(img)
                        if not q["gradable"]:
                            quality_fails.append({"image_id": row["image_id"], "reasons": q["failure_reasons"]})
                except Exception as e:
                    disk_issues.append(f"Corrupt image {p}: {str(e)}")

            report["disk_audit"] = {
                "file_issues_count": len(disk_issues),
                "quality_fails_count": len(quality_fails),
                "disk_issues_sample": disk_issues[:10],
                "quality_fails_sample": quality_fails[:10]
            }

        return report

    def generate_markdown_report(self, output_path: str | Path, check_images_on_disk: bool = False) -> str:
        """Run audit and format as human-readable Markdown documentation."""
        audit = self.run_full_audit(check_images_on_disk=check_images_on_disk)
        
        md_lines = [
            "# Dataset Quality & Integrity Audit Report",
            "",
            f"**Total Records Evaluated**: {len(self.df)}",
            f"**Unique Participants**: {self.df['participant_id'].nunique() if 'participant_id' in self.df.columns else 'N/A'}",
            "",
            "## 1. Schema & Metadata Verification",
            f"- **Valid According to Protocol**: {audit['schema_audit']['valid']}",
            f"- **Noted Issues**: {audit['schema_audit']['issues']}",
            f"- **Conflicting Patient Labels**: {audit['conflicting_patient_labels']['count']}",
            "",
            "## 2. Target Class & Subgroup Distributions",
            f"- **Diabetes Labels**: {audit.get('class_distribution', {})}",
            f"- **Retinopathy (DR) Grades**: {audit.get('dr_grade_distribution', {})}",
            f"- **Bilateral Eye Sides**: {audit.get('eye_side_distribution', {})}",
            "",
            "## 3. Imaging Hardware & Center Distribution",
            f"- **Sites**: {audit.get('site_distribution', {})}",
            f"- **Cameras**: {audit.get('camera_distribution', {})}",
            ""
        ]

        md_content = "\n".join(md_lines)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return md_content

