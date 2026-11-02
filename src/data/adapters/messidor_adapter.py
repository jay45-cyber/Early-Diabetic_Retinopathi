"""Messidor & Messidor-2 Dataset Ingestion Adapter."""
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from src.data.adapters.base_adapter import BaseDatasetAdapter


class Messidor2Adapter(BaseDatasetAdapter):
    """Adapter for Messidor-2 (France).
    
    Contains 1,748 fundus photographs (874 patients, bilateral OD/OS).
    Provides DR grades and macular edema risk. Used primarily for external validation.
    """

    def get_dataset_metadata(self) -> Dict[str, Any]:
        return {
            "dataset_id": "Messidor_2",
            "full_name": "Messidor-2 Retinal Image Dataset",
            "source": "Three French Ophthalmology Departments",
            "license": "Research Permission Required",
            "primary_task_suitability": "EXTERNAL_VALIDATION",
            "total_images": 1748,
            "total_patients": 874,
            "has_ehr_diabetes_label": False,
            "has_dr_grades": True,
            "supports_dr0_subgroup": False
        }

    def ingest(self) -> pd.DataFrame:
        if self.metadata_file is None or not self.metadata_file.is_file():
            raise FileNotFoundError(f"Messidor metadata CSV not found at: {self.metadata_file}")

        df = pd.read_csv(self.metadata_file)
        manifest_rows = []
        for _, row in df.iterrows():
            img_id = str(row.get("image_id", row.get("image", "")))
            pid = str(row.get("patient_id", img_id[:img_id.rfind("_")] if "_" in img_id else img_id))
            dr_grade = int(row.get("adjudicated_dr_grade", row.get("dr_grade", 0)))

            manifest_rows.append({
                "participant_id": pid,
                "image_id": img_id,
                "eye_side": "OD" if "_1" in img_id or "right" in img_id.lower() else ("OS" if "_2" in img_id or "left" in img_id.lower() else "Unknown"),
                "image_path": str(self.data_dir / f"{img_id}.jpg"),
                "dataset_id": "Messidor_2",
                "site_id": "France_Ophthalmology_Network",
                "camera_id": "Topcon_TRC_NW6",
                "image_quality": 1.0,
                "diabetes_label": None,
                "diabetes_label_source": "Unknown",
                "dr_grade": dr_grade
            })

        return pd.DataFrame(manifest_rows)

