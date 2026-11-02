"""BRSET (Brazilian Retinal Screening Dataset) Ingestion Adapter."""
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from src.data.adapters.base_adapter import BaseDatasetAdapter
from src.data.patient_manifest import validate_manifest


class BRSETAdapter(BaseDatasetAdapter):
    """Adapter for BRSET (PhysioNet).
    
    Contains:
    - 16,266 fundus images across 8,524 patients.
    - True EHR-confirmed systemic Type 2 Diabetes label (`diabetes == 1 / 0`).
    - Full ICDR Diabetic Retinopathy grades (0 to 4).
    - Bilateral eye side (OD / OS).
    - Camera type (Canon CR-2, Nikon).
    - Primary candidate for early diabetes screening (DR = 0 analysis).
    """

    def get_dataset_metadata(self) -> Dict[str, Any]:
        return {
            "dataset_id": "BRSET",
            "full_name": "Brazilian Retinal Screening Dataset",
            "citation": "Nature Scientific Data (2024), DOI: 10.1038/s41597-024-03096-9",
            "license": "PhysioNet Open Access / Credentialed CC-BY 4.0",
            "primary_task_suitability": "PRIMARY_DIABETES_PREDICTION",
            "total_images": 16266,
            "total_patients": 8524,
            "has_ehr_diabetes_label": True,
            "has_dr_grades": True,
            "supports_dr0_subgroup": True
        }

    def ingest(self) -> pd.DataFrame:
        """Parse BRSET labels CSV and build standardized manifest."""
        if self.metadata_file is None or not self.metadata_file.is_file():
            raise FileNotFoundError(f"BRSET metadata CSV not found at: {self.metadata_file}")

        df = pd.read_csv(self.metadata_file)
        
        # Standardize column names to manifest schema
        # In BRSET: image_id, patient_id, camera, eye, diabetes, dr_icdr
        manifest_rows = []
        for _, row in df.iterrows():
            img_id = str(row.get("image_id", ""))
            pid = str(row.get("patient_id", row.get("participant_id", img_id)))
            eye = str(row.get("eye", row.get("laterality", "Unknown"))).upper()
            eye_std = "OD" if eye in ("OD", "RIGHT") else ("OS" if eye in ("OS", "LEFT") else "Unknown")
            
            # Clinical diabetes label
            raw_diab = row.get("diabetes", None)
            diabetes_label = int(raw_diab) if pd.notnull(raw_diab) and raw_diab in (0, 1, "0", "1") else None

            # DR grade
            raw_dr = row.get("dr_icdr", row.get("dr", None))
            dr_grade = int(raw_dr) if pd.notnull(raw_dr) and raw_dr in range(5) else 0

            manifest_rows.append({
                "participant_id": pid,
                "image_id": img_id,
                "eye_side": eye_std,
                "image_path": str(self.data_dir / f"{img_id}.jpg"),
                "dataset_id": "BRSET",
                "site_id": str(row.get("site", "Brazil_Public_Network")),
                "camera_id": str(row.get("camera", "Canon_CR2")),
                "image_quality": float(row.get("quality", 1.0)),
                "diabetes_label": diabetes_label,
                "diabetes_label_source": "EHR_Diagnosis",
                "dr_grade": dr_grade,
                "age": int(row["age"]) if "age" in row and pd.notnull(row["age"]) else None,
                "sex": str(row["sex"]) if "sex" in row and pd.notnull(row["sex"]) else None
            })

        manifest_df = pd.DataFrame(manifest_rows)
        return manifest_df

