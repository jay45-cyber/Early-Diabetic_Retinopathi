"""Reproducible training and validation loop."""
from typing import Dict, Any, List
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from src.evaluation.classification_metrics import compute_screening_metrics


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device
) -> float:
    """Train model for a single epoch and return average loss."""
    model.train()
    total_loss = 0.0
    for images, targets in loader:
        images = images.to(device)
        targets = targets.to(device).float()

        optimizer.zero_grad()
        logits = model(images)
        loss = criterion(logits, targets)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)

    return total_loss / len(loader.dataset)


def evaluate_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device
) -> Dict[str, Any]:
    """Evaluate model on validation/test loader and compute full metric suite."""
    model.eval()
    total_loss = 0.0
    all_targets = []
    all_probs = []

    with torch.no_grad():
        for images, targets in loader:
            images = images.to(device)
            targets = targets.to(device).float()

            logits = model(images)
            loss = criterion(logits, targets)
            total_loss += loss.item() * images.size(0)

            probs = torch.sigmoid(logits)
            all_targets.extend(targets.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())

    y_true = np.array(all_targets)
    y_prob = np.array(all_probs)
    metrics = compute_screening_metrics(y_true, y_prob)
    metrics["loss"] = round(total_loss / len(loader.dataset), 4)

    return metrics

