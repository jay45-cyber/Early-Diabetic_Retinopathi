"""Retinal Foundation Model (RETFound) Adapter Interface."""
from pathlib import Path
from typing import Optional
import torch
import torch.nn as nn
from torchvision.models import vit_b_16, ViT_B_16_Weights


class RetinalFoundationModel(nn.Module):
    """Retinal Foundation Model adapter supporting RETFound ViT feature extraction.
    
    References:
    - Zhou et al. (2023) 'A foundation model for generalizable disease detection from retinal images', Nature.
    """

    def __init__(
        self,
        checkpoint_path: Optional[str | Path] = None,
        pretrained_backbone: bool = True,
        dropout_rate: float = 0.2
    ):
        super().__init__()
        weights = ViT_B_16_Weights.DEFAULT if pretrained_backbone else None
        self.vit = vit_b_16(weights=weights)

        in_features = self.vit.heads.head.in_features
        self.vit.heads.head = nn.Sequential(
            nn.Dropout(p=dropout_rate),
            nn.Linear(in_features, 256),
            nn.LayerNorm(256),
            nn.GELU(),
            nn.Dropout(p=dropout_rate),
            nn.Linear(256, 1)
        )

        if checkpoint_path and Path(checkpoint_path).is_file():
            self.load_foundation_weights(checkpoint_path)

    def load_foundation_weights(self, checkpoint_path: str | Path):
        """Load fine-tuned or domain-pre-trained RETFound checkpoint weights."""
        state = torch.load(checkpoint_path, map_location="cpu")
        weights = state.get("model", state.get("model_state_dict", state))
        # Filter matching keys
        self.load_state_dict(weights, strict=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        logits = self.vit(x)
        return logits.squeeze(-1)

