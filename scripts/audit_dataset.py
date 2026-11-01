"""Dataset audit utility script: checks schema, missingness, duplicates, and quality."""
import sys
from pathlib import Path
import argparse
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.patient_manifest import validate_manifest
from src.utils.logging import get_logger

logger = get_logger("audit_dataset")


def main():
    parser = argparse.ArgumentParser(description="Audit retinal dataset manifest integrity.")
    parser.add_argument("--manifest", type=str, default="data/manifests/patient_manifest.csv", help="Path to manifest CSV.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.is_file():
        logger.error(f"Manifest not found: {manifest_path.resolve()}")
        sys.exit(1)

    logger.info(f"Loading manifest from {manifest_path}...")
    df = pd.read_csv(manifest_path)
    
    summary = validate_manifest(df)
    logger.info("=== DATASET AUDIT SUMMARY ===")
    logger.info(f"Total Records: {summary['total_records']}")
    logger.info(f"Unique Patients: {summary['unique_participants']}")
    logger.info(f"Diabetic Cases: {summary['diabetic_count']}")
    logger.info(f"Non-Diabetic Controls: {summary['non_diabetic_count']}")
    logger.info(f"DR Grade 0 Total: {summary['dr_grade_0_count']}")
    logger.info(f"DR Grade 0 Diabetic (Early Target): {summary['dr0_diabetic_count']}")
    
    if summary["valid"]:
        logger.info("SUCCESS: Manifest is valid according to research standards.")
    else:
        logger.warning(f"Issues identified: {summary['issues']}")


if __name__ == "__main__":
    main()

