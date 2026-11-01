"""Partition manifest into train, val, and locked test splits with zero patient leakage."""
import sys
from pathlib import Path
import argparse
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.grouped_split import create_patient_grouped_splits, verify_zero_leakage
from src.utils.logging import get_logger

logger = get_logger("build_splits")


def main():
    parser = argparse.ArgumentParser(description="Create patient-level grouped splits.")
    parser.add_argument("--manifest", type=str, default="data/manifests/patient_manifest.csv")
    parser.add_argument("--output_dir", type=str, default="data/manifests")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.is_file():
        logger.error(f"Manifest not found: {manifest_path.resolve()}")
        sys.exit(1)

    df = pd.read_csv(manifest_path)
    logger.info(f"Creating patient-level grouped splits for {len(df)} images...")

    splits = create_patient_grouped_splits(df, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15)
    
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    splits["train"].to_csv(out_dir / "train_manifest.csv", index=False)
    splits["val"].to_csv(out_dir / "val_manifest.csv", index=False)
    splits["test"].to_csv(out_dir / "locked_test_manifest.csv", index=False)

    audit = verify_zero_leakage(splits["train"], splits["val"], splits["test"])
    logger.info("=== SPLIT VERIFICATION AUDIT ===")
    logger.info(f"Train Patients: {audit['train_patients']} ({len(splits['train'])} images)")
    logger.info(f"Val Patients:   {audit['val_patients']} ({len(splits['val'])} images)")
    logger.info(f"Test Patients:  {audit['test_patients']} ({len(splits['test'])} images)")
    logger.info("CONFIRMED: Zero patient overlap across partitions.")


if __name__ == "__main__":
    main()

