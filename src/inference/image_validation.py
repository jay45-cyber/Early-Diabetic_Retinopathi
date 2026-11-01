"""Input image validation gateway for clinical inference."""
from pathlib import Path
from typing import Dict, Any, Tuple
from PIL import Image
from src.data.image_quality import assess_image_quality


def validate_inference_input(image_input: str | Path | Image.Image) -> Dict[str, Any]:
    """Validate format, dimensions, and gradability before running neural inference."""
    try:
        if isinstance(image_input, (str, Path)):
            img = Image.open(image_input)
        else:
            img = image_input

        # Check format
        if img.mode not in ("RGB", "RGBA", "L"):
            return {
                "valid": False,
                "reason": f"Unsupported image color mode: {img.mode}. Expected RGB color fundus."
            }

        # Quality assessment
        quality_res = assess_image_quality(img)
        if not quality_res["gradable"]:
            return {
                "valid": False,
                "reason": f"Image ungradable: {', '.join(quality_res['failure_reasons'])}",
                "quality_details": quality_res
            }

        return {
            "valid": True,
            "image": img.convert("RGB"),
            "quality_details": quality_res
        }

    except Exception as e:
        return {
            "valid": False,
            "reason": f"Failed to decode fundus image: {str(e)}"
        }

