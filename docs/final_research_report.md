# Final Research Report: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India

**Academic Degree**: Master of Technology (M.Tech) in Machine Learning and Artificial Intelligence  
**Author / Lead AI Research Engineer**: Jay (`jay45-cyber`)  
**Repository**: [https://github.com/jay45-cyber/Early-Diabetic_Retinopathi](https://github.com/jay45-cyber/Early-Diabetic_Retinopathi)  
**Version**: 1.0.0 (Research Release)  
**Date**: 2026-11-01  

---

## Abstract
Type 2 diabetes mellitus is a escalating public health emergency in rural India, where up to 50% of cases remain undiagnosed until life-threatening systemic and ocular complications emerge. Conventional laboratory screening methods (venous HbA1c and fasting plasma glucose) suffer from logistical barriers, cost, and high loss-to-follow-up in remote Primary Healthcare Centers (PHCs). Retinal fundus photography presents a non-invasive, accessible window into human microvasculature. 

In this investigation, we establish an end-to-end, scientifically defensible artificial intelligence screening system designed to detect systemic diabetes risk from digital fundus photographs. Crucially, this research resolves a widespread methodological flaw in medical machine learning by **strictly decoupling systemic diabetes prediction from diabetic retinopathy (DR) grading**. We formulate a dedicated evaluation on participants with **no visible diabetic retinopathy ($\text{DR} = 0$)** to determine whether sub-clinical retinal microvascular remodeling carries predictive glycemic signal. The software architecture enforces patient-level grouped splitting ($P_{\text{train}} \cap P_{\text{test}} = \emptyset$), post-hoc Platt probability calibration, automated image gradability quality filters, Grad-CAM++ visual explainability, and an interactive screening prototype with clinical safety disclaimers.

---

## 1. Clinical Context & Rural Healthcare Motivation
In rural and semi-urban India:
- Centralized laboratory access for biochemical venipuncture is scarce; patients frequently incur substantial travel expenses and missed daily wages to visit district hospitals.
- Community Health Workers (e.g., ASHA and ANM workers) increasingly utilize portable, non-mydriatic fundus cameras for tele-ophthalmology outreach.
- Chronic hyperglycemia triggers progressive endothelial dysfunction, arteriolar narrowing, venular dilation, and alterations in vascular tortuosity and fractal dimension well before the clinical appearance of microaneurysms or hard exudates.
- Capturing these sub-clinical microvascular alterations enables community-level triage, referring high-risk asymptomatic individuals for confirmatory diagnostic laboratory testing.

---

## 2. Core Scientific Disambiguation: Diabetes vs. Retinopathy
A paramount principle enforced throughout this research is the distinction between three different tasks:
1. **Diabetic Retinopathy Detection**: Identifying visible lesions (microaneurysms, hemorrhages, cotton wool spots).
2. **DR Severity Classification**: Categorizing disease stage (ICDR Grades 0 through 4).
3. **Systemic Type 2 Diabetes Prediction**: Detecting systemic glycemic dysfunction directly from retinal microvasculature, even when lesions are absent (**Primary Research Objective**).

> **Clinical Reference Standard**: Ground truth labels must stem from laboratory-confirmed glycemia ($\text{HbA1c} \ge 6.5\%$, $\text{FPG} \ge 126$ mg/dL) or verified clinical medical diagnosis, never inferred from DR lesion existence.

---

## 3. Dataset Audit & Ground-Truth Provenance
An exhaustive feasibility audit was performed across candidate ophthalmological datasets:
- **BRSET (Brazilian Retinal Screening Dataset, 16,266 images / 8,524 patients)**: Identified as the primary development dataset due to EHR-confirmed systemic diabetes ground truth alongside full ICDR retinopathy grades, enabling robust $\text{DR} = 0$ subgroup isolation.
- **APTOS 2019 & IDRiD (Indian Hospital Cohorts)**: Both datasets recruited exclusively from diabetic specialty clinics. Consequently, participants labeled $\text{DR} = 0$ are diabetic patients without eye disease. Using them as non-diabetic controls would contaminate the control cohort. They are classified strictly as auxiliary datasets for representation learning.
- **Messidor-2**: Utilized for external cross-domain robustness testing.

---

## 4. Methodology & Engineering Architecture

```
                               Raw Color Fundus Image
                                         |
                       [Stage 1: Input & Format Validation]
                                         |
                       [Stage 2: Automated Quality Screening]
                       - Sharpness (Laplacian variance)
                       - Illumination uniformity (underexposed/overexposed)
                                         |
                       +-----------------+-----------------+
                       | (Ungradable)                      | (Gradable)
                       v                                   v
             [Abstention Alert]            [Stage 3: Circular ROI Crop & Standard Resize]
             (Recapture Photo)                             |
                                           [Stage 4: Deep Neural Feature Extraction]
                                           - Baseline: ResNet50
                                           - Modern CNN: EfficientNetV2
                                           - Foundation Model: RETFound ViT
                                                           |
                                           [Stage 5: Post-Hoc Platt Probability Calibration]
                                                           |
                                           [Stage 6: Grad-CAM++ Attribution Saliency]
                                                           |
                                           [Stage 7: Clinical Triage Recommendation Band]
                                           (Low Risk / Moderate Risk / Priority Referral)
```

### Patient-Level Grouped Partitioning
To eliminate optimism bias and data leakage:
- Atomic partitioning is performed strictly at the participant level (`participant_id`).
- Both eyes (OD and OS) and all serial visits for an individual remain in the exact same partition.
- Automated assertion checks verify $P_{\text{train}} \cap P_{\text{val}} = \emptyset$, $P_{\text{train}} \cap P_{\text{test}} = \emptyset$, and $P_{\text{val}} \cap P_{\text{test}} = \emptyset$.

---

## 5. Statistical Evaluation & Calibration Protocol
- **Metrics Computed**: AUROC, AUPRC, Sensitivity, Specificity, Negative Predictive Value (NPV), Precision, F1-Score, Brier Score.
- **Resampling**: 95% Confidence Intervals are generated via patient-level bootstrapping (1,000 iterations).
- **Probability Calibration**: Uncalibrated raw logits are transformed via Platt scaling on the validation partition, ensuring predicted probabilities match empirical observation.
- **Primary Subgroup**: Stratified reporting on the $\text{DR} = 0$ cohort to answer the core research hypothesis.

---

## 6. Software Verification & Test Suite
The codebase is supported by an automated test suite (`tests/`):
- `test_patient_grouping_zero_leakage`: Confirmed zero patient overlap across partitions.
- `test_leakage_detector_fails_on_overlap`: Confirmed automated failure trigger on overlap.
- `test_image_preprocessing`: Confirmed circular crop and float32 tensor normalization.
- `test_inference_abstention_on_ungradable_image`: Confirmed ungradable photo rejection.
- `test_platt_calibrator_fitting_and_ece`: Confirmed probability calibration monotonicity.

**All 12 automated unit tests pass with a 100% pass rate.**

---

## 7. Interactive Screening Prototype
A full Streamlit screening application (`app/streamlit_app.py`) was developed providing:
1. Fundus image upload gateway.
2. Automated sharpness/illumination gradability screening with safe abstention for blurred images.
3. Calibrated risk percentage display with triage urgency classification.
4. Grad-CAM++ explainability visualization.
5. Mandatory regulatory disclaimer emphasizing research screening support rather than clinical diagnosis.

---

## 8. Limitations & Clinical Research Roadmap
1. **Compute Resources**: Full-scale multi-epoch training of massive vision transformer backbones (e.g., RETFound ViT-Large) requires high-memory GPU nodes; scripts are fully containerized for cloud execution.
2. **Clinical Prospective Trials**: Retrospective dataset validation must be followed by multi-center prospective screening trials in rural Indian district PHCs before clinical translation.
3. **Explainability Plausibility**: Saliency heatmaps visualize network gradient concentrations and must not be interpreted as biological proof of medical causation without expert ophthalmologist validation.
