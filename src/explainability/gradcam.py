"""Grad-CAM++ implementation for convolutional retinal backbones."""
from typing import Tuple, Optional
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image


class GradCAMPlusPlus:
    """Grad-CAM++ generates saliency heatmaps highlighting predictive retinal microvasculature."""

    def __init__(self, model: torch.nn.Module, target_layer: torch.nn.Module):
        self.model = model
        self.target_layer = target_layer
        self.gradients: Optional[torch.Tensor] = None
        self.activations: Optional[torch.Tensor] = None

        # Register forward and backward hooks
        self.forward_handle = self.target_layer.register_forward_hook(self._save_activations)
        self.backward_handle = self.target_layer.register_full_backward_hook(self._save_gradients)

    def _save_activations(self, module, input, output):
        self.activations = output.detach()

    def _save_gradients(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate_cam(self, input_tensor: torch.Tensor) -> np.ndarray:
        """Compute 2D Grad-CAM++ heatmap normalized in [0, 1]."""
        self.model.eval()
        logits = self.model(input_tensor)
        score = logits.squeeze()

        self.model.zero_grad()
        score.backward(retain_graph=False)

        grads = self.gradients # [B, C, H, W]
        acts = self.activations # [B, C, H, W]

        # Grad-CAM++ weighting coefficients
        grads_power_2 = grads.pow(2)
        grads_power_3 = grads.pow(3)
        sum_acts = acts.sum(dim=(2, 3), keepdim=True)
        eps = 1e-7

        aij = grads_power_2 / (2 * grads_power_2 + sum_acts * grads_power_3 + eps)
        weights = (aij * F.relu(grads)).sum(dim=(2, 3), keepdim=True)

        cam = (weights * acts).sum(dim=1, keepdim=True)
        cam = F.relu(cam)
        cam = F.interpolate(cam, size=input_tensor.shape[2:], mode="bilinear", align_corners=False)
        cam = cam.squeeze().cpu().numpy()

        cam_min, cam_max = cam.min(), cam.max()
        if cam_max > cam_min:
            cam = (cam - cam_min) / (cam_max - cam_min)
        else:
            cam = np.zeros_like(cam)

        return cam

    def overlay_on_image(self, original_image: Image.Image, cam: np.ndarray, alpha: float = 0.4) -> Image.Image:
        """Overlay normalized CAM heatmap onto original fundus photograph."""
        import matplotlib.cm as cm

        colormap = cm.get_cmap("jet")
        heatmap = colormap(cam)[:, :, :3] # Discard alpha
        heatmap = (heatmap * 255).astype(np.uint8)
        heatmap_img = Image.fromarray(heatmap).resize(original_image.size, Image.Resampling.LANCZOS)

        return Image.blend(original_image.convert("RGB"), heatmap_img, alpha=alpha)

    def remove_hooks(self):
        self.forward_handle.remove()
        self.backward_handle.remove()

