"""Multimodal Retinal Image + Clinical Covariates Late-Fusion Architecture."""
import torch
import torch.nn as nn
from src.models.baseline_resnet import BaselineResNet50


class MultimodalRetinaModel(nn.Module):
    """Two-stream multimodal network fusing retinal fundus features and tabular clinical covariates."""

    def __init__(
        self,
        num_clinical_features: int = 4, # e.g., age, sex, BMI, systolic BP
        pretrained_vision: bool = True,
        dropout_rate: float = 0.3
    ):
        super().__init__()
        # Vision Stream: ResNet50 feature extractor
        self.vision_stream = BaselineResNet50(pretrained=pretrained_vision, dropout_rate=dropout_rate)
        # Tabular Clinical Stream
        self.clinical_mlp = nn.Sequential(
            nn.Linear(num_clinical_features, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout_rate),
            nn.Linear(64, 32),
            nn.ReLU(inplace=True)
        )
        # Fusion Head (Vision 256 + Clinical 32 = 288)
        self.fusion_head = nn.Sequential(
            nn.Linear(2048 + 32, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout_rate),
            nn.Linear(128, 1) # Raw logit output
        )

    def forward(self, images: torch.Tensor, clinical_data: torch.Tensor) -> torch.Tensor:
        vision_feat = self.vision_stream.extract_features(images) # [B, 2048]
        clin_feat = self.clinical_mlp(clinical_data) # [B, 32]
        fused = torch.cat([vision_feat, clin_feat], dim=-1) # [B, 2080]
        logits = self.fusion_head(fused)
        return logits.squeeze(-1)

