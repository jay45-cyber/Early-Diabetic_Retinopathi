"""Tests for image quality assessment and circular fundus preprocessing."""
import pytest
from PIL import Image
import numpy as np
from src.data.image_quality import assess_image_quality
from src.data.preprocessing import preprocess_fundus_image, normalize_to_tensor


def test_image_quality_sharp_gradable():
    """Verify that a sharp, well-illuminated image is classified as gradable."""
    # Synthetic checkerboard with high contrast and sharpness
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[::20, :] = 200
    arr[:, ::20] = 200
    arr += 40
    img = Image.fromarray(arr)

    res = assess_image_quality(img, min_dimension=200, sharpness_threshold=10.0)
    assert res["gradable"] is True
    assert res["sharpness_score"] > 10.0


def test_image_quality_ungradable_too_dark():
    """Verify that a pitch black image is correctly rejected as ungradable."""
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    img = Image.fromarray(arr)

    res = assess_image_quality(img, min_dimension=200)
    assert res["gradable"] is False
    assert any("illumination" in r.lower() for r in res["failure_reasons"])


def test_preprocessing_output_dimension_and_normalization():
    """Verify that preprocessed images match target dimensions and normalize correctly."""
    arr = np.random.randint(50, 200, (400, 500, 3), dtype=np.uint8)
    img = Image.fromarray(arr)

    preprocessed = preprocess_fundus_image(img, target_size=(384, 384), crop_circle=False)
    assert preprocessed.size == (384, 384)

    tensor = normalize_to_tensor(preprocessed)
    assert tensor.shape == (3, 384, 384)
    assert tensor.dtype == np.float32

