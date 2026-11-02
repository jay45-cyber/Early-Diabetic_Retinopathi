"""Build and validate a standardized research manifest from raw dataset directories."""
import sys
import argparse
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.patient_manifest import validate_manifest, REQUIRED_COLUMNS
from src.utils.logging import get_logger

logger = get_logger("generate_manifest")


def main():
    parser = argparse.ArgumentParser(description="Generate standardized patient manifest.")
    parser.add_argument("--raw_dir", type=str, required=True, help="Path to raw image directory.")
    parser.add_argument("--labels_csv", type=str, required=True, help="Path to raw metadata CSV.")
    parser.add_argument("--output_path", type=str, default="data/manifests/patient_manifest.csv")
    args = parser.parse_args()

    labels_path = Path(args.labels_csv)
    raw_dir = Path(args.raw_dir)

    if not labels_path.is_file():
        logger.error(f"Labels file not found: {labels_path}")
        sys.exit(1)

    logger.info(f"Ingesting metadata from {labels_path}...")
    raw_df = pd.read_csv(labels_path)

    # Standardize column mappings if present
    # Users can map custom column names to standardized schema
    manifest_df = pd.DataFrame()
    for col in REQUIRED_COLUMNS:
        if col in raw_df.columns:
            manifest_df[col] = raw_df[col]
        else:
            manifest_df[col] = None

    # Audit manifest
    validation_res = validate_manifest(manifest_df)
    out_file = Path(args.output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    manifest_df.to_csv(out_file, index=False)

    logger.info(f"Manifest written to {out_file} ({len(manifest_df)} records).")
    logger.info(f"Validation status: {validation_res['valid']}")
    if validation_res["issues"]:
        logger.warning(f"Validation notices: {validation_res['issues']}")


if __name__ == "__main__":
    main()

