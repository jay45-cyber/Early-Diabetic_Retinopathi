"""Clinical loss functions with automated class imbalance handling."""
import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalLoss(nn.Module):
    """Binary Focal Loss for severe class imbalance."""

    def __init__(self, alpha: float = 0.25, gamma: float = 2.0):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        bce_loss = F.binary_cross_entropy_with_logits(logits, targets, reduction="none")
        probs = torch.sigmoid(logits)
        pt = targets * probs + (1 - targets) * (1 - probs)
        focal_weight = (1 - pt).pow(self.gamma)
        alpha_weight = targets * self.alpha + (1 - targets) * (1 - self.alpha)
        loss = alpha_weight * focal_weight * bce_loss
        return loss.mean()

