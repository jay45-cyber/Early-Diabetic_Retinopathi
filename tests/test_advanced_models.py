"""Tests for advanced architectures: ConvNeXt, Foundation Model, and Multimodal."""
import pytest
import torch
from src.models.convnext import RetinalConvNeXt
from src.models.retinal_foundation_model import RetinalFoundationModel
from src.models.multimodal_model import MultimodalRetinaModel


def test_convnext_forward_pass():
    """Verify ConvNeXt forward pass returns scalar logits."""
    model = RetinalConvNeXt(pretrained=False, dropout_rate=0.2)
    dummy_input = torch.randn(2, 3, 224, 224)
    logits = model(dummy_input)

    assert logits.shape == (2,)
    features = model.extract_features(dummy_input)
    assert features.shape[0] == 2


def test_foundation_model_stub():
    """Verify RetinalFoundationModel ViT adapter forward pass."""
    model = RetinalFoundationModel(pretrained_backbone=False, dropout_rate=0.1)
    dummy_input = torch.randn(2, 3, 224, 224)
    logits = model(dummy_input)

    assert logits.shape == (2,)


def test_multimodal_fusion_forward_pass():
    """Verify MultimodalRetinaModel fuses vision and tabular clinical features."""
    model = MultimodalRetinaModel(num_clinical_features=4, pretrained_vision=False)
    dummy_images = torch.randn(2, 3, 224, 224)
    dummy_clinical = torch.randn(2, 4) # e.g. age, sex, BMI, SBP

    logits = model(dummy_images, dummy_clinical)
    assert logits.shape == (2,)

