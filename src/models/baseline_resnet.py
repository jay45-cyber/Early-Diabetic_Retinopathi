"""ResNet50 baseline model architecture for diabetes risk screening."""
from typing import Dict, Any
import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights


class BaselineResNet50(nn.Module):
    """ResNet50 backbone initialized with ImageNet weights and adapted for binary screening."""

    def __init__(self, pretrained: bool = True, dropout_rate: float = 0.3):
        super().__init__()
        weights = ResNet50_Weights.IMAGENET1K_V2 if pretrained else None
        self.backbone = resnet50(weights=weights)

        # Retain feature extractor up to average pooling
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Identity()

        # Custom screening classification head
        self.classifier = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout_rate),
            nn.Linear(256, 1) # Raw logit output for BCEWithLogitsLoss
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass returning raw scalar logits."""
        features = self.backbone(x)
        logits = self.classifier(features)
        return logits.squeeze(-1)

    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """Extract 2048-dimensional feature embedding before classification head."""
        return self.backbone(x)

