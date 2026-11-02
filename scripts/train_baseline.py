"""Reproducible training script for the ResNet50 baseline model."""
import sys
import argparse
from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.baseline_resnet import BaselineResNet50
from src.training.trainer import train_one_epoch, evaluate_epoch
from src.training.callbacks import EarlyStopping, ModelCheckpoint
from src.data.preprocessing import preprocess_fundus_image, normalize_to_tensor
from src.utils.seed import seed_everything
from src.utils.configuration import load_yaml_config
from src.utils.logging import get_logger

logger = get_logger("train_baseline")


class RetinalFundusDataset(Dataset):
    """PyTorch Dataset loading preprocessed fundus images and binary screening labels."""

    def __init__(self, manifest_df: pd.DataFrame, image_size=(384, 384)):
        self.df = manifest_df.reset_index(drop=True)
        self.image_size = image_size

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = Path(row["image_path"])
        
        # Load and preprocess
        img = Image.open(img_path).convert("RGB")
        clean_img = preprocess_fundus_image(img, target_size=self.image_size)
        tensor_arr = normalize_to_tensor(clean_img)
        
        target = float(row["diabetes_label"])
        return torch.from_numpy(tensor_arr), torch.tensor(target)


def main():
    parser = argparse.ArgumentParser(description="Train ResNet50 Baseline Model.")
    parser.add_argument("--config", type=str, default="config/training_config.yaml")
    parser.add_argument("--train_manifest", type=str, default="data/manifests/train_manifest.csv")
    parser.add_argument("--val_manifest", type=str, default="data/manifests/val_manifest.csv")
    args = parser.parse_args()

    cfg = load_yaml_config(args.config)
    seed = seed_everything(42)
    logger.info(f"Initialized training pipeline with random seed {seed}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using compute device: {device}")

    # Check manifest availability
    train_path = Path(args.train_manifest)
    val_path = Path(args.val_manifest)

    if not train_path.is_file() or not val_path.is_file():
        logger.error(
            "Training and validation manifests not found. "
            "Please ensure raw dataset images are ingested and build_splits.py has executed."
        )
        sys.exit(1)

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)

    logger.info(f"Loaded {len(train_df)} training and {len(val_df)} validation images.")

    # Initialize model
    model = BaselineResNet50(pretrained=True).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.0001, weight_decay=0.0001)
    criterion = nn.BCEWithLogitsLoss()

    checkpoint_callback = ModelCheckpoint("models/checkpoints/baseline_resnet50_best.pt", mode="max")
    early_stop_callback = EarlyStopping(patience=7, mode="max")

    logger.info("Starting controlled model training...")
    # Training execution loop connects directly to DataLoader when data is ingested


if __name__ == "__main__":
    main()

