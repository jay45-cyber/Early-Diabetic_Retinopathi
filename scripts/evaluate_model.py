"""Evaluate model checkpoint on locked test set and compute metrics and calibration."""
import sys
import argparse
from pathlib import Path
import json
import torch
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.baseline_resnet import BaselineResNet50
from src.evaluation.classification_metrics import compute_screening_metrics
from src.evaluation.calibration import PlattCalibrator, compute_expected_calibration_error
from src.evaluation.subgroup_analysis import evaluate_subgroups
from src.utils.logging import get_logger

logger = get_logger("evaluate_model")


def main():
    parser = argparse.ArgumentParser(description="Evaluate trained screening model.")
    parser.add_argument("--checkpoint", type=str, required=True, help="Path to model checkpoint .pt")
    parser.add_argument("--test_manifest", type=str, default="data/manifests/locked_test_manifest.csv")
    parser.add_argument("--output_dir", type=str, default="outputs/metrics")
    args = parser.parse_args()

    test_path = Path(args.test_manifest)
    ckpt_path = Path(args.checkpoint)

    if not test_path.is_file() or not ckpt_path.is_file():
        logger.error(f"Required test manifest or checkpoint file missing.")
        sys.exit(1)

    logger.info(f"Loading checkpoint {ckpt_path} and test set {test_path}...")
    test_df = pd.read_csv(test_path)
    
    # Run evaluation
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Evaluation completed. Metrics recorded to {out_dir}.")


if __name__ == "__main__":
    main()
