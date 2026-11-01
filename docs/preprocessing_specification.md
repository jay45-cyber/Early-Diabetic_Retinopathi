# Preprocessing & Data Augmentation Specification

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Auditor**: Medical Computer Vision Engineer  

---

## 1. Objective & Design Rationale
Retinal fundus images collected across diverse cameras and clinical sites exhibit substantial variations in resolution, black border margins, illumination gradients, and pupil dilation. A standardized, deterministic preprocessing pipeline is mandatory to ensure the neural network learns physiological vascular characteristics rather than camera-specific optical artifacts.

---

## 2. Sequential Preprocessing Stages

```
   Raw Color Fundus Image (Any Resolution)
                     |
  [Stage 1: Dimension & Integrity Validation]
                     |
  [Stage 2: Fundus Masking & Circular Cropping] -> Crops out extraneous black borders
                     |
  [Stage 3: Image Quality / Gradability Assessment] -> Rejects severely blurred/underexposed images
                     |
  [Stage 4: Standardized Spatial Resizing] -> Resizes to target dimension (384 x 384)
                     |
  [Stage 5: Color & Illumination Normalization] -> Standardized channel mean/std
                     |
              Preprocessed Tensor
```

### Stage 1: File Integrity & Dimension Check
- Validates file headers, readable color channels (RGB, 3-channel), and minimum dimension ($> 300 \times 300$ pixels).

### Stage 2: Circular Region Detection & Border Removal
- Digital fundus cameras project a circular field of view onto a rectangular sensor, creating large black uninformative margins.
- A circular mask is extracted by thresholding the green/luminance channel, finding the bounding contour of the illuminated retina, and tightly cropping the image to the fundus circle.

### Stage 3: Automated Image Quality Screening
- Computes sharpness (Laplacian variance), illumination uniformity, and contrast. Images falling below the quality threshold ($0.50$) are flagged as `Ungradable` and abstained from screening.

### Stage 4: Resolution Resizing
- Standard target resolution: **$384 \times 384$ pixels** (balanced for preserving fine microvascular tortuosity while remaining computationally feasible within memory constraints).

### Stage 5: Normalization
- Channel standardization using ImageNet parameters ($\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$).

---

## 3. Training-Only Data Augmentation Rules

> [!IMPORTANT]
> **Data Augmentation Guardrail**:
> Data augmentation is strictly applied **only during training iterations**. Validation and test images must NEVER be augmented.

- **Permitted Augmentations**:
  - Horizontal flip ($p = 0.5$)
  - Vertical flip ($p = 0.5$)
  - Random rotation within $[-20^\circ, +20^\circ]$
  - Subtle brightness and contrast jitter ($\pm 10\%$, $p = 0.3$)
- **Prohibited Augmentations**:
  - Elastic deformations or heavy shear (distorts anatomical vessel caliber and tortuosity).
  - Cutout or heavy erasing (may randomly occlude the fovea or optic disc, mimicking ischemia).

