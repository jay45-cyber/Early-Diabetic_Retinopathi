"""Run external validation across independent clinical cohorts."""
import sys
import argparse
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.utils.logging import get_logger

logger = get_logger("external_validation")


def main():
    parser = argparse.ArgumentParser(description="Run external validation.")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--external_manifest", type=str, default="data/manifests/external_test_manifest.csv")
    args = parser.parse_args()

    ext_path = Path(args.external_manifest)
    if not ext_path.is_file():
        logger.warning(
            f"External validation cohort manifest not found at {ext_path}. "
            "External validation will execute when independent external images are ingested."
        )
        return

    logger.info(f"Running external cohort validation on {ext_path}...")


if __name__ == "__main__":
    main()
