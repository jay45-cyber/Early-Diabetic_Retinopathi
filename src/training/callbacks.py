"""Training callbacks: Early Stopping and Model Checkpointing."""
from pathlib import Path
from typing import Dict, Any, Optional
import torch


class EarlyStopping:
    """Early stops the training if validation metric doesn't improve after a given patience."""

    def __init__(self, patience: int = 7, min_delta: float = 0.001, mode: str = "max"):
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.counter = 0
        self.best_score: Optional[float] = None
        self.early_stop = False

    def __call__(self, current_score: float) -> bool:
        if self.best_score is None:
            self.best_score = current_score
            return True

        improved = (
            (current_score > self.best_score + self.min_delta)
            if self.mode == "max"
            else (current_score < self.best_score - self.min_delta)
        )

        if improved:
            self.best_score = current_score
            self.counter = 0
            return True
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
            return False


class ModelCheckpoint:
    """Save model checkpoint when validation metric achieves a new optimum."""

    def __init__(self, filepath: str | Path, mode: str = "max"):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.mode = mode
        self.best_score: Optional[float] = None

    def save(self, model: torch.nn.Module, score: float, metadata: Dict[str, Any] | None = None) -> bool:
        improved = (
            self.best_score is None or
            (score > self.best_score if self.mode == "max" else score < self.best_score)
        )
        if improved:
            self.best_score = score
            payload = {
                "model_state_dict": model.state_dict(),
                "best_score": score,
                "metadata": metadata or {}
            }
            torch.save(payload, self.filepath)
            return True
        return False

