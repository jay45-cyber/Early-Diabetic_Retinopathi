"""Standardized fundus preprocessing and circular ROI extraction."""
from pathlib import Path
from typing import Tuple
from PIL import Image
import numpy as np


def crop_fundus_circle(
    image: Image.Image,
    luminance_threshold: int = 15,
    margin_ratio: float = 0.02
) -> Image.Image:
    """Detect circular retinal illumination area and crop out excess black borders."""
    gray = image.convert("L")
    arr = np.array(gray)
    
    # Threshold to identify non-black retinal pixels
    mask = arr > luminance_threshold
    if not np.any(mask):
        return image # Return original if entirely black

    # Find bounding box of foreground
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]

    # Expand margin slightly if possible
    h, w = arr.shape
    margin_y = int((ymax - ymin) * margin_ratio)
    margin_x = int((xmax - xmin) * margin_ratio)
    
    ymin = max(0, ymin - margin_y)
    ymax = min(h, ymax + margin_y)
    xmin = max(0, xmin - margin_x)
    xmax = min(w, xmax + margin_x)

    return image.crop((xmin, ymin, xmax, ymax))


def preprocess_fundus_image(
    image: Image.Image,
    target_size: Tuple[int, int] = (384, 384),
    crop_circle: bool = True
) -> Image.Image:
    """End-to-end preprocessing pipeline for raw fundus photographs.
    
    1. Converts to RGB.
    2. Crops extraneous black camera borders.
    3. Resizes with anti-aliasing to target dimension.
    """
    img = image.convert("RGB")
    if crop_circle:
        img = crop_fundus_circle(img)
    
    return img.resize(target_size, Image.Resampling.LANCZOS)


def normalize_to_tensor(
    image: Image.Image,
    mean: Tuple[float, float, float] = (0.485, 0.456, 0.406),
    std: Tuple[float, float, float] = (0.229, 0.224, 0.225)
) -> np.ndarray:
    """Convert PIL image to standard normalized float32 tensor array [C, H, W]."""
    arr = np.array(image, dtype=np.float32) / 255.0
    arr = (arr - mean) / std
    return np.transpose(arr, (2, 0, 1)).astype(np.float32)

