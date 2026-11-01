"""Exact and perceptual duplicate image detection for retinal fundus datasets."""
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple
from PIL import Image
import numpy as np


def compute_md5(image_path: str | Path) -> str:
    """Compute the MD5 hash of a raw image file for exact duplicate identification."""
    hasher = hashlib.md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_dhash(image: Image.Image, hash_size: int = 8) -> int:
    """Compute difference hash (dHash) for perceptual duplicate identification.
    
    Resizes image to (hash_size + 1, hash_size), converts to grayscale,
    and compares adjacent horizontal pixel values.
    """
    resized = image.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = np.array(resized, dtype=np.int32)
    diff = pixels[:, 1:] > pixels[:, :-1]
    
    # Pack boolean array into an integer hash
    decimal_val = 0
    for bit in diff.flatten():
        decimal_val = (decimal_val << 1) | int(bit)
    return decimal_val


def hamming_distance(hash1: int, hash2: int) -> int:
    """Calculate the Hamming distance between two perceptual hashes."""
    x = hash1 ^ hash2
    return bin(x).count("1")


def detect_exact_duplicates(image_paths: List[str | Path]) -> Dict[str, List[str]]:
    """Scan list of image paths and return mapping of MD5 -> list of duplicate paths."""
    seen_hashes: Dict[str, List[str]] = {}
    for p in image_paths:
        path = Path(p)
        if not path.is_file():
            continue
        h = compute_md5(path)
        seen_hashes.setdefault(h, []).append(str(path))
    
    # Return only collisions
    return {h: paths for h, paths in seen_hashes.items() if len(paths) > 1}

