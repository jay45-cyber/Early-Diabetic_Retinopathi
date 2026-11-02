"""APTOS 2019 Blindness Detection Dataset Ingestion Adapter."""
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from src.data.adapters.base_adapter import BaseDatasetAdapter


class APTOS2019Adapter(BaseDatasetAdapter):
    """Adapter for APTOS 2019 (Aravind Eye Hospital, India).
    
    CRITICAL MEDICAL AUDIT NOTICE:
    All participants in APTOS 2019 were recruited from diabetic specialty clinics.
    Patients with DR grade 0 in APTOS are DIABETIC individuals without retinopathy.
    Therefore, APTOS must NEVER be used to train a standard diabetic vs. non-diabetic
    classifier, as it completely lacks true non-diabetic controls.
    Suitability: AUXILIARY_DR_REPRESENTATION ONLY.
    """

    def get_dataset_metadata(self) -> Dict[str, Any]:
        return {
            "dataset_id": "APTOS_2019",
            "full_name": "APTOS 2019 Blindness Detection",
            "source": "Aravind Eye Hospital, India / Kaggle",
            "citation": "Kaggle Blindness Detection Challenge (2019)",
            "license": "Research Use Only",
            "primary_task_suitability": "AUXILIARY_DR_REPRESENTATION",
            "total_images": 3662,
            "has_ehr_diabetes_label": False,
            "has_dr_grades": True,
            "supports_dr0_subgroup": False, # Cannot use as non-diabetic control!
            "clinical_warning": "All subjects are diabetic. Grade 0 != Non-diabetic."
        }

    def ingest(self) -> pd.DataFrame:
        if self.metadata_file is None or not self.metadata_file.is_file():
            raise FileNotFoundError(f"APTOS metadata CSV not found at: {self.metadata_file}")

        df = pd.read_csv(self.metadata_file)
        manifest_rows = []
        for _, row in df.iterrows():
            img_id = str(row.get("id_code", ""))
            dr_grade = int(row.get("diagnosis", 0))

            manifest_rows.append({
                "participant_id": img_id, # Patient IDs not released in APTOS
                "image_id": img_id,
                "eye_side": "Unknown",
                "image_path": str(self.data_dir / f"{img_id}.png"),
                "dataset_id": "APTOS_2019",
                "site_id": "Aravind_Eye_Hospital_India",
                "camera_id": "Topcon_Handheld",
                "image_quality": 1.0,
                # Crucial safety rule: Diabetes label is NOT inferred
                "diabetes_label": None,
                "diabetes_label_source": "Unknown",
                "dr_grade": dr_grade
            })

        return pd.DataFrame(manifest_rows)

