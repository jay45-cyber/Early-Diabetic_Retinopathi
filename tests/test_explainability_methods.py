"""Tests for Integrated Gradients and Occlusion Sensitivity."""
import pytest
import torch
import torch.nn as nn
import numpy as np
from src.explainability.integrated_gradients import IntegratedGradients
from src.explainability.occlusion import OcclusionSensitivity


class SimpleCNN(nn.Module):
    """Small CNN for fast interpretability unit tests."""
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(3, 8, kernel_size=3, padding=1)
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(8, 1)

    def forward(self, x):
        h = torch.relu(self.conv(x))
        h = self.pool(h).flatten(1)
        return self.fc(h).squeeze(-1)


def test_integrated_gradients():
    """Verify that IntegratedGradients computes 2D attribution map."""
    model = SimpleCNN()
    ig = IntegratedGradients(model, steps=10)
    dummy_input = torch.randn(1, 3, 64, 64)

    attr = ig.attribute(dummy_input)
    assert attr.shape == (64, 64)
    assert 0.0 <= attr.min() and attr.max() <= 1.0


def test_occlusion_sensitivity():
    """Verify that OcclusionSensitivity outputs a 2D sensitivity map."""
    model = SimpleCNN()
    occ = OcclusionSensitivity(model, patch_size=16, stride=16)
    dummy_input = torch.randn(1, 3, 64, 64)

    attr = occ.attribute(dummy_input)
    assert attr.shape == (64, 64)
    assert 0.0 <= attr.min() and attr.max() <= 1.0

