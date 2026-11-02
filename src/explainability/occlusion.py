"""Occlusion Sensitivity Analysis for Retinal Fundus AI."""
import torch
import numpy as np


class OcclusionSensitivity:
    """Computes attribution by systematically occluding local rectangular/circular patches."""

    def __init__(self, model: torch.nn.Module, patch_size: int = 32, stride: int = 16):
        self.model = model
        self.patch_size = patch_size
        self.stride = stride

    def attribute(self, input_tensor: torch.Tensor) -> np.ndarray:
        """Generate sensitivity heatmaps based on probability drop when patches are occluded."""
        self.model.eval()
        with torch.no_grad():
            baseline_prob = torch.sigmoid(self.model(input_tensor)).item()

        _, _, h, w = input_tensor.shape
        heatmap = np.zeros((h, w), dtype=np.float32)
        counts = np.zeros((h, w), dtype=np.float32)

        for y in range(0, h - self.patch_size + 1, self.stride):
            for x in range(0, w - self.patch_size + 1, self.stride):
                occluded = input_tensor.clone()
                # Occlude with zero (mean background)
                occluded[:, :, y:y + self.patch_size, x:x + self.patch_size] = 0.0

                with torch.no_grad():
                    occ_prob = torch.sigmoid(self.model(occluded)).item()

                diff = max(0.0, baseline_prob - occ_prob)
                heatmap[y:y + self.patch_size, x:x + self.patch_size] += diff
                counts[y:y + self.patch_size, x:x + self.patch_size] += 1.0

        counts[counts == 0] = 1.0
        sensitivity_map = heatmap / counts

        # Normalize
        s_min, s_max = sensitivity_map.min(), sensitivity_map.max()
        if s_max > s_min:
            sensitivity_map = (sensitivity_map - s_min) / (s_max - s_min)

        return sensitivity_map

