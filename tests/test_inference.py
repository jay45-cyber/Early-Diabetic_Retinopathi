"""Tests for inference pipeline, quality gateway, and abstention mechanism."""
import pytest
import torch
import torch.nn as nn
from PIL import Image
import numpy as np
from src.inference.predictor import RetinaDiabetesPredictor
from src.inference.risk_output import format_screening_output


class DummyRetinaModel(nn.Module):
    """Dummy model returning fixed scalar logit for unit testing."""
    def __init__(self, output_logit: float = 1.0):
        super().__init__()
        self.output_logit = nn.Parameter(torch.tensor([output_logit]), requires_grad=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.output_logit.expand(x.size(0))


def test_inference_abstention_on_ungradable_image():
    """Verify that predictor abstains when presented with a severely degraded image."""
    model = DummyRetinaModel(output_logit=2.0)
    predictor = RetinaDiabetesPredictor(model)

    # Completely black ungradable image
    bad_img = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
    result = predictor.predict(bad_img)

    assert result["status"] == "Abstained"
    assert result["gradable"] is False
    assert "reason" in result
    assert "RESEARCH SCREENING-SUPPORT PROTOTYPE ONLY" in result["disclaimer"]


def test_inference_success_on_gradable_image():
    """Verify that predictor generates structured triage output on gradable image."""
    model = DummyRetinaModel(output_logit=1.5)
    predictor = RetinaDiabetesPredictor(model)

    # Sharp synthetic image
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[::10, :] = 180
    arr[:, ::10] = 180
    arr += 50
    good_img = Image.fromarray(arr)

    result = predictor.predict(good_img)

    assert result["status"] == "Success"
    assert result["gradable"] is True
    assert 0.0 <= result["calibrated_risk_score"] <= 100.0
    assert result["risk_category"] in ["Low Risk", "Moderate Risk", "High Risk"]
    assert "clinical_recommendation" in result


def test_format_screening_output_categories():
    """Verify triage thresholds map accurately to clinical recommendations."""
    low = format_screening_output(0.20)
    assert low["risk_category"] == "Low Risk"
    assert low["triage_urgency"] == "Routine"

    med = format_screening_output(0.50)
    assert med["risk_category"] == "Moderate Risk"
    assert med["triage_urgency"] == "Moderate"

    high = format_screening_output(0.85)
    assert high["risk_category"] == "High Risk"
    assert high["triage_urgency"] == "Priority"

