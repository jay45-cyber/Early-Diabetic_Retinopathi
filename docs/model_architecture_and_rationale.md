# Model Architecture & Experimental Hierarchy Rationale

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Auditor**: Senior Machine Learning Architect  

---

## 1. Experimental Hierarchy Overview

To ensure scientific defensibility, model development adheres to a controlled, incremental hierarchy:

```
                  [Level 1: Reproducible Baseline (ResNet50)]
                                      |
                     +----------------+----------------+
                     |                                 |
     [Level 2: Modern CNN (EfficientNetV2)]    [Level 3: Modern ConvNet (ConvNeXt)]
                     |                                 |
                     +----------------+----------------+
                                      |
              [Level 4: Retinal Foundation Model (RETFound ViT)]
                                      |
              [Level 5: Multimodal Fusion (Retina + Metadata)]
```

---

## 2. Architectural Specifications & Clinical Rationale

### Level 1: ResNet50 Baseline (Experiment 1)
- **Architecture**: 50-layer Residual Network (`torchvision.models.resnet50`).
- **Pretrained Weights**: ImageNet-1K (`IMAGENET1K_V2`).
- **Modifications**: Replaces the final 1000-class fully-connected layer with:
  `Linear(2048, 256) -> BatchNorm1d -> ReLU -> Dropout(0.3) -> Linear(256, 1)`.
- **Rationale**: ResNet50 is the gold standard benchmark across medical imaging literature. Establishing a clean, reproducible ResNet50 baseline guarantees that performance gains in advanced models are genuine and measurable.

### Level 2: EfficientNetV2-S / M (Experiment 2)
- **Architecture**: EfficientNetV2 with fused-MBConv and progressive learning.
- **Rationale**: Optimized parameter efficiency and compound scaling. Excels at multi-scale feature representation while consuming significantly fewer FLOPs than standard CNNs, crucial for low-resource environments.

### Level 3: ConvNeXt-Tiny / Small (Experiment 3)
- **Architecture**: Pure convolutional network modernized with Vision Transformer design choices (inverted bottleneck, depthwise $7 \times 7$ convolutions, LayerNorm).
- **Rationale**: Retains the inductive bias of convolutions (translation invariance and data efficiency) while matching Transformer expressiveness without requiring massive compute.

### Level 4: Retinal Foundation Model (RETFound) (Experiment 4)
- **Architecture**: Vision Transformer (ViT-Large/16) pre-trained with Masked Autoencoding (MAE) on 1.6 million retinal images (Zhou et al., *Nature* 2023).
- **Rationale**: Captures fine domain-specific ophthalmic patterns, vessel branching geometries, and optical choroidal textures. Evaluated via linear probing and fine-tuning on GPU nodes.

### Level 5: Multimodal Fusion (Experiment 5)
- **Architecture**: Two-stream architecture combining the retinal image embedding with tabular clinical covariates (age, sex, BMI, systolic blood pressure).
- **Fusion Method**: Late fusion via concatenated feature projection.

---

## 3. Training & Regularization Hyperparameters

| Parameter | Baseline Value | Justification |
| :--- | :--- | :--- |
| **Loss Function** | `BCEWithLogitsLoss(pos_weight=w)` | Handles binary screening with automated weighting for class imbalance. |
| **Optimizer** | AdamW | Decoupled weight decay provides superior regularization over standard Adam. |
| **Learning Rate** | $1 \times 10^{-4}$ (Backbone), $1 \times 10^{-3}$ (Head) | Differential learning rates prevent catastrophic forgetting of pre-trained weights. |
| **LR Scheduler** | Cosine Annealing with Warmup | Smoothly decays learning rate towards zero over training epochs. |
| **Weight Decay** | $1 \times 10^{-4}$ | Prevents weight explosion and over-reliance on single pixel features. |
| **Early Stopping** | Patience: 7 epochs on Validation AUROC | Halts training before overfitting manifests. |

