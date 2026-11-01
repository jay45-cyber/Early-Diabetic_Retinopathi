"""Reproducibility and deterministic seed configuration."""
import os
import random
import numpy as np


def seed_everything(seed: int = 42) -> int:
    """Set random seeds across random, numpy, and torch (if installed) for reproducible research."""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)

    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass

    return seed

