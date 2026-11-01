# Primary Research Questions & Hypotheses

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  

---

## Primary Research Questions (RQ)

### RQ1: Sub-Clinical Diabetes Detection
> **Can deep learning models extract features from retinal fundus photographs that predict systemic Type 2 diabetes in patients without visible diabetic retinopathy (DR = 0)?**
- **Hypothesis $H_1$**: Retinal microvascular remodeling (vessel caliber, tortuosity, foveal avascular zone changes) occurs prior to clinically visible microaneurysms, allowing an appropriately regularized deep learning model to discriminate diabetic from non-diabetic individuals with an AUROC statistically superior to chance ($p < 0.05$).
- **Null Hypothesis $H_0$**: In the absence of visible DR lesions, deep learning models cannot distinguish diabetic from non-diabetic fundus images beyond baseline demographic prevalence.

### RQ2: Model Architecture & Representation Comparison
> **How do conventional transfer learning backbones (ResNet50, EfficientNetV2, ConvNeXt) compare with self-supervised retinal foundation representations (e.g., RETFound) on systemic diabetes prediction?**
- **Hypothesis**: Domain-specific retinal foundation models pre-trained on millions of unlabeled fundus images capture subtle morphological vascular features more effectively than natural-image ImageNet models, yielding superior generalization on out-of-distribution camera domains.

### RQ3: Probability Calibration in Rural Screening
> **Does post-hoc probability calibration (Platt scaling / Isotonic regression) produce screening risk scores that reflect true disease prevalence across clinical risk strata?**
- **Hypothesis**: Uncalibrated modern neural networks exhibit overconfidence; post-hoc probability calibration evaluated via Brier score and calibration curves is mandatory to provide trustworthy decision thresholds for rural community health referrals.

### RQ4: Visual Explainability & Clinical Plausibility
> **Do gradient-weighted class activation maps (Grad-CAM++ / Integrated Gradients) highlight physiologically plausible retinal regions (optic disc, major vascular arcades, macula) rather than imaging artifacts?**
- **Hypothesis**: Saliency heatmaps from well-regularized models trained on patient-separated splits concentrate on vascular structures and the parafoveal capillary network, whereas models suffering from shortcut learning rely on camera borders or illumination gradients.

---

## Experimental Acceptance Criteria
1. Models must be evaluated on patient-level locked test partitions.
2. 95% Confidence Intervals must be derived via patient-level bootstrapping (1,000 resamples).
3. Performance must be reported overall AND stratified on the DR=0 subgroup.

