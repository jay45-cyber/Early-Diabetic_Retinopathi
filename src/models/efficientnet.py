"""EfficientNetV2 architecture for parameter-efficient retinal screening."""
import torch
import torch.nn as nn
from torchvision.models import efficientnet_v2_s, EfficientNet_V2_S_Weights


class RetinalEfficientNetV2(nn.Module):
    """EfficientNetV2-S adapted for binary risk screening."""

    def __init__(self, pretrained: bool = True, dropout_rate: float = 0.3):
        super().__init__()
        weights = EfficientNet_V2_S_Weights.DEFAULT if pretrained else None
        self.backbone = efficientnet_v2_s(weights=weights)

        # Classifier replacement
        in_features = self.backbone.classifier[1].in_features
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=dropout_rate, inplace=True),
            nn.Linear(in_features, 256),
            nn.BatchNorm1d(256),
            nn.SiLU(inplace=True),
            nn.Dropout(p=dropout_rate, inplace=True),
            nn.Linear(256, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        logits = self.backbone(x)
        return logits.squeeze(-1)

