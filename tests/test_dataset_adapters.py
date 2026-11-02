"""Automated tests for dataset adapters (BRSET, APTOS, IDRiD, LocalFolder)."""
import pytest
from pathlib import Path
import pandas as pd
from src.data.adapters.brset_adapter import BRSETAdapter
from src.data.adapters.aptos_adapter import APTOS2019Adapter
from src.data.adapters.idrid_adapter import IDRiDAdapter
from src.data.adapters.local_folder_adapter import LocalFolderAdapter


def test_brset_adapter_ingestion(tmp_path):
    """Test that BRSETAdapter correctly parses schema and preserves EHR diabetes labels."""
    csv_file = tmp_path / "brset_mock.csv"
    mock_data = pd.DataFrame([
        {"image_id": "img01", "patient_id": "p01", "eye": "OD", "diabetes": 1, "dr_icdr": 0, "age": 55, "sex": "F"},
        {"image_id": "img02", "patient_id": "p01", "eye": "OS", "diabetes": 1, "dr_icdr": 0, "age": 55, "sex": "F"},
        {"image_id": "img03", "patient_id": "p02", "eye": "OD", "diabetes": 0, "dr_icdr": 0, "age": 42, "sex": "M"}
    ])
    mock_data.to_csv(csv_file, index=False)

    adapter = BRSETAdapter(data_dir=tmp_path, metadata_file=csv_file)
    meta = adapter.get_dataset_metadata()
    assert meta["dataset_id"] == "BRSET"
    assert meta["has_ehr_diabetes_label"] is True

    manifest = adapter.ingest()
    assert len(manifest) == 3
    assert set(manifest["eye_side"]) == {"OD", "OS"}
    assert manifest.loc[manifest["image_id"] == "img01", "diabetes_label"].values[0] == 1
    assert manifest.loc[manifest["image_id"] == "img03", "diabetes_label"].values[0] == 0


def test_aptos_adapter_clinical_safety(tmp_path):
    """Verify that APTOS adapter strictly tags dataset as auxiliary and does NOT invent diabetes labels."""
    csv_file = tmp_path / "aptos_mock.csv"
    mock_data = pd.DataFrame([
        {"id_code": "aptos01", "diagnosis": 0},
        {"id_code": "aptos02", "diagnosis": 2}
    ])
    mock_data.to_csv(csv_file, index=False)

    adapter = APTOS2019Adapter(data_dir=tmp_path, metadata_file=csv_file)
    meta = adapter.get_dataset_metadata()
    assert meta["primary_task_suitability"] == "AUXILIARY_DR_REPRESENTATION"
    assert meta["supports_dr0_subgroup"] is False

    manifest = adapter.ingest()
    # Grade 0 in APTOS must NOT be labeled non-diabetic
    assert manifest["diabetes_label"].isnull().all()

