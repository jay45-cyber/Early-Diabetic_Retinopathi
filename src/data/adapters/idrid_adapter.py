"""IDRiD (Indian Diabetic Retinopathy Image Dataset) Ingestion Adapter."""
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from src.data.adapters.base_adapter import BaseDatasetAdapter


class IDRiDAdapter(BaseDatasetAdapter):
    """Adapter for IDRiD (Nanded, Maharashtra, India).
    
    Contains 516 images from an Indian eye clinic with expert DR and DME grading.
    Like APTOS, all participants are diabetic; suitable strictly as an auxiliary
    representation learning and domain adaptation dataset.
    """

    def get_dataset_metadata(self) -> Dict[str, Any]:
        return {
            "dataset_id": "IDRiD",
            "full_name": "Indian Diabetic Retinopathy Image Dataset",
            "source": "Eye Clinic in Nanded, Maharashtra, India",
            "citation": "IEEE Dataport (2018), DOI: 10.21227/H25W98",
            "license": "Creative Commons Attribution 4.0 International",
            "primary_task_suitability": "AUXILIARY_DR_REPRESENTATION",
            "total_images": 516,
            "has_ehr_diabetes_label": False,
            "has_dr_grades": True,
            "supports_dr0_subgroup": False
        }

    def ingest(self) -> pd.DataFrame:
        if self.metadata_file is None or not self.metadata_file.is_file():
            raise FileNotFoundError(f"IDRiD metadata CSV not found at: {self.metadata_file}")

        df = pd.read_csv(self.metadata_file)
        manifest_rows = []
        for _, row in df.iterrows():
            img_id = str(row.get("Image name", ""))
            dr_grade = int(row.get("Retinopathy grade", 0))

            manifest_rows.append({
                "participant_id": img_id,
                "image_id": img_id,
                "eye_side": "Unknown",
                "image_path": str(self.data_dir / f"{img_id}.jpg"),
                "dataset_id": "IDRiD",
                "site_id": "Nanded_Clinic_Maharashtra",
                "camera_id": "Kowa_VX10_Alpha",
                "image_quality": 1.0,
                "diabetes_label": None,
                "diabetes_label_source": "Unknown",
                "dr_grade": dr_grade
            })

        return pd.DataFrame(manifest_rows)

