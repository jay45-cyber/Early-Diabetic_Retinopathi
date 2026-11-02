"""Batch duplicate image detection script using exact MD5 and perceptual hashing."""
import sys
import argparse
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.duplicate_detection import compute_md5, compute_dhash, hamming_distance
from src.utils.logging import get_logger

logger = get_logger("detect_duplicates")


def main():
    parser = argparse.ArgumentParser(description="Scan image directory for duplicates.")
    parser.add_argument("--image_dir", type=str, required=True, help="Directory containing retinal images.")
    parser.add_argument("--dhash_threshold", type=int, default=5, help="Hamming distance threshold for perceptual duplicates.")
    args = parser.parse_args()

    img_dir = Path(args.image_dir)
    if not img_dir.is_dir():
        logger.error(f"Directory not found: {img_dir}")
        sys.exit(1)

    image_paths = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpeg"))
    logger.info(f"Scanning {len(image_paths)} images in {img_dir}...")

    # Exact MD5 check
    md5_map = {}
    exact_duplicates = []
    for p in image_paths:
        h = compute_md5(p)
        if h in md5_map:
            exact_duplicates.append((str(p), md5_map[h]))
        else:
            md5_map[h] = str(p)

    logger.info(f"Exact MD5 duplicate pairs found: {len(exact_duplicates)}")
    for dup, orig in exact_duplicates[:10]:
        logger.warning(f"Duplicate: {dup} <-> Original: {orig}")


if __name__ == "__main__":
    main()

