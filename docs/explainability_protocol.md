# Explainable AI (XAI) Protocol & Plausibility Review

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Auditor**: Lead AI Research Engineer  

---

## 1. Objectives & Clinical Grounding
In high-stakes clinical screening, deep learning models must not operate as impenetrable black boxes. Explainability visualizations serve two critical functions:
1. **Safety & Shortcut Detection**: Verify whether the model relies on anatomical retinal vasculature rather than spurious imaging artifacts (e.g., camera dust halos, border vignetting, or patient IDs).
2. **Biomarker Hypothesis Generation**: Enable clinical collaborators to examine subtle structural features correlated with systemic hyperglycemia.

> [!WARNING]
> **Saliency Map Safety Rule**:
> Saliency maps (heatmaps) are visual representations of mathematical network gradients. They do **NOT** constitute medical proof of biological causality or independent biomarker discovery.

---

## 2. Implemented Explainability Techniques

```
                                Trained Deep Neural Network
                                             |
                   +-------------------------+-------------------------+
                   |                                                   |
      +------------v------------+                         +------------v------------+
      |        Grad-CAM++       |                         |   Integrated Gradients  |
      | (Convolutional Layers)  |                         | (Pixel Attribution)     |
      +------------+------------+                         +------------+------------+
                   |                                                   |
                   +-------------------------+-------------------------+
                                             |
                           +-----------------v-----------------+
                           |   Clinical Plausibility Audit     |
                           |   - Optic Disc & Vascular Arcades |
                           |   - Macular Capillary Network     |
                           |   - Artifact Sensitivity Check    |
                           +-----------------------------------+
```

1. **Grad-CAM++ (Gradient-Weighted Class Activation Mapping Plus-Plus)**:
   - Uses higher-order gradients to compute feature map importance, providing superior localization for multiple fine vascular structures compared to standard Grad-CAM.
2. **Integrated Gradients (Sundararajan et al., 2017)**:
   - Evaluates pixel-level path integrals from a black baseline image, satisfying completeness and implementation invariance.
3. **Occlusion Sensitivity Analysis**:
   - Systematically occludes circular patches across the fundus to measure degradation in predicted risk, validating whether central vascular regions drive decision-making.

---

## 3. Visual Reporting & Four-Quadrant Error Analysis
Explainability heatmaps will be generated and reviewed across all four clinical error quadrants:
- **True Positives (TP)**: Correctly identified diabetic patients; inspect vascular focus.
- **True Negatives (TN)**: Correctly classified non-diabetic controls; verify baseline uniformity.
- **False Positives (FP)**: Non-diabetic patients flagged as high risk; check for hypertensive changes, vessel tortuosity, or camera glare artifacts.
- **False Negatives (FN)**: Missed diabetic patients; evaluate whether low contrast or absence of early microvascular remodeling caused model under-prediction.

