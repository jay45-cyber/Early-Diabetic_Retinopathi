"""ConvNeXt architecture adapted for binary diabetes risk screening."""
import torch
import torch.nn as nn
from torchvision.models import convnext_tiny, ConvNeXt_Tiny_Weights


class RetinalConvNeXt(nn.Module):
    """ConvNeXt-Tiny backbone with modernized vision design and custom classification head."""

    def __init__(self, pretrained: bool = True, dropout_rate: float = 0.3):
        super().__init__()
        weights = ConvNeXt_Tiny_Weights.DEFAULT if pretrained else None
        self.backbone = convnext_tiny(weights=weights)

        # In ConvNeXt, classifier is Sequential(LayerNorm2d, Flatten, Linear)
        in_features = self.backbone.classifier[2].in_features
        self.backbone.classifier[2] = nn.Sequential(
            nn.Dropout(p=dropout_rate),
            nn.Linear(in_features, 256),
            nn.LayerNorm(256),
            nn.GELU(),
            nn.Dropout(p=dropout_rate),
            nn.Linear(256, 1) # Raw logit output
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        logits = self.backbone(x)
        return logits.squeeze(-1)

    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """Extract spatial features before final linear projection."""
        x = self.backbone.features(x)
        x = self.backbone.avgpool(x)
        return torch.flatten(x, 1)

