"""Local Directory Ingestion Adapter for custom or institutional fundus datasets."""
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from PIL import Image
from src.data.adapters.base_adapter import BaseDatasetAdapter
from src.data.image_quality import assess_image_quality


class LocalFolderAdapter(BaseDatasetAdapter):
    """Adapter for scanning arbitrary local image directories and building manifests."""

    def get_dataset_metadata(self) -> Dict[str, Any]:
        return {
            "dataset_id": "LOCAL_CUSTOM",
            "full_name": "Local Directory Ingestion",
            "source": str(self.data_dir),
            "license": "Internal Research / User Provided",
            "primary_task_suitability": "CUSTOM_INGESTION"
        }

    def ingest(self, extensions: List[str] | None = None) -> pd.DataFrame:
        if not self.data_dir.is_dir():
            raise FileNotFoundError(f"Image directory not found: {self.data_dir}")

        if extensions is None:
            extensions = ["*.jpg", "*.jpeg", "*.png"]

        image_files = []
        for ext in extensions:
            image_files.extend(list(self.data_dir.glob(ext)))

        # Also support CSV metadata if provided
        meta_lookup = {}
        if self.metadata_file and self.metadata_file.is_file():
            meta_df = pd.read_csv(self.metadata_file)
            id_col = "image_id" if "image_id" in meta_df.columns else meta_df.columns[0]
            meta_lookup = meta_df.set_index(id_col).to_dict(orient="index")

        manifest_rows = []
        for p in image_files:
            stem = p.stem
            meta = meta_lookup.get(stem, {})

            pid = str(meta.get("participant_id", meta.get("patient_id", stem)))
            eye = str(meta.get("eye_side", "Unknown"))
            label = meta.get("diabetes_label", None)
            dr = int(meta.get("dr_grade", 0))

            manifest_rows.append({
                "participant_id": pid,
                "image_id": stem,
                "eye_side": eye,
                "image_path": str(p),
                "dataset_id": "LOCAL_CUSTOM",
                "site_id": str(meta.get("site_id", "Local_Site")),
                "camera_id": str(meta.get("camera_id", "Unknown_Camera")),
                "image_quality": float(meta.get("image_quality", 1.0)),
                "diabetes_label": int(label) if pd.notnull(label) else None,
                "diabetes_label_source": str(meta.get("diabetes_label_source", "Unknown")),
                "dr_grade": dr
            })

        return pd.DataFrame(manifest_rows)

