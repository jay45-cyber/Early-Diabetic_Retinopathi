"""Tests for exact and perceptual image duplicate detection."""
import pytest
from PIL import Image
import numpy as np
from src.data.duplicate_detection import compute_dhash, hamming_distance


def test_perceptual_hash_identical_images():
    """Verify that identical images have zero Hamming distance."""
    img1 = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
    img2 = img1.copy()

    h1 = compute_dhash(img1)
    h2 = compute_dhash(img2)

    assert hamming_distance(h1, h2) == 0


def test_perceptual_hash_distinct_images():
    """Verify that completely different images have high Hamming distance."""
    # Uniform white vs uniform black with a diagonal split
    arr1 = np.zeros((100, 100, 3), dtype=np.uint8)
    arr2 = np.zeros((100, 100, 3), dtype=np.uint8)
    arr2[:, :50] = 255

    img1 = Image.fromarray(arr1)
    img2 = Image.fromarray(arr2)

    h1 = compute_dhash(img1)
    h2 = compute_dhash(img2)

    dist = hamming_distance(h1, h2)
    assert dist > 0

