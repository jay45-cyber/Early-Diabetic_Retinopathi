"""Automated image quality and gradability assessment for retinal photographs."""
from pathlib import Path
from typing import Dict, Any
from PIL import Image, ImageStat
import numpy as np


def assess_image_quality(
    image_input: str | Path | Image.Image,
    min_dimension: int = 256,
    sharpness_threshold: float = 20.0,
    min_mean_intensity: float = 15.0,
    max_mean_intensity: float = 240.0
) -> Dict[str, Any]:
    """Assess fundus photograph quality and gradability.
    
    Metrics evaluated:
    - Dimension validity
    - Illumination / mean luminance (overexposed vs. severely underexposed)
    - Sharpness via Laplacian variance approximation
    """
    if isinstance(image_input, (str, Path)):
        img = Image.open(image_input).convert("RGB")
    else:
        img = image_input.convert("RGB")

    width, height = img.size
    dimension_ok = width >= min_dimension and height >= min_dimension

    # Intensity metrics
    gray = img.convert("L")
    stat = ImageStat.Stat(gray)
    mean_intensity = stat.mean[0]
    illumination_ok = min_mean_intensity <= mean_intensity <= max_mean_intensity

    # Sharpness via discrete Laplacian approximation on grayscale numpy array
    arr = np.array(gray, dtype=np.float32)
    # 2D Laplacian kernel convolution via slice indexing
    laplacian = (
        arr[:-2, 1:-1] + arr[2:, 1:-1] +
        arr[1:-1, :-2] + arr[1:-1, 2:] -
        4.0 * arr[1:-1, 1:-1]
    )
    sharpness = float(np.var(laplacian))
    sharpness_ok = sharpness >= sharpness_threshold

    gradable = dimension_ok and illumination_ok and sharpness_ok

    return {
        "gradable": gradable,
        "width": width,
        "height": height,
        "mean_intensity": round(mean_intensity, 2),
        "sharpness_score": round(sharpness, 2),
        "failure_reasons": [
            *(["Insufficient dimensions"] if not dimension_ok else []),
            *(["Improper illumination (too dark or washed out)"] if not illumination_ok else []),
            *(["Severe blur / low sharpness"] if not sharpness_ok else [])
        ]
    }

