"""Integrated Gradients feature attribution for deep neural network interpretability."""
import torch
import numpy as np


class IntegratedGradients:
    """Computes Integrated Gradients path-integral attributions.
    
    Reference: Sundararajan et al. (2017) 'Axiomatic Attribution for Deep Networks', ICML.
    """

    def __init__(self, model: torch.nn.Module, steps: int = 50):
        self.model = model
        self.steps = steps

    def attribute(
        self,
        input_tensor: torch.Tensor,
        baseline: torch.Tensor | None = None
    ) -> np.ndarray:
        """Calculate pixel-level attribution map."""
        self.model.eval()

        if baseline is None:
            baseline = torch.zeros_like(input_tensor)

        # Scale inputs along linear path from baseline to input
        alphas = torch.linspace(0.0, 1.0, self.steps, device=input_tensor.device)
        scaled_inputs = [baseline + alpha * (input_tensor - baseline) for alpha in alphas]
        scaled_batch = torch.cat(scaled_inputs, dim=0).requires_grad_(True)

        logits = self.model(scaled_batch)
        total_score = logits.sum()

        self.model.zero_grad()
        total_score.backward()

        grads = scaled_batch.grad # [steps, C, H, W]
        # Trapezoidal approximation of path integral
        avg_grads = (grads[:-1] + grads[1:]).mean(dim=0, keepdim=True) / 2.0
        delta = input_tensor - baseline
        attributions = (delta * avg_grads).squeeze(0).detach().cpu().numpy()

        # Aggregate across color channels
        attribution_map = np.abs(attributions).sum(axis=0)
        # Normalize in [0, 1]
        attr_min, attr_max = attribution_map.min(), attribution_map.max()
        if attr_max > attr_min:
            attribution_map = (attribution_map - attr_min) / (attr_max - attr_min)

        return attribution_map

