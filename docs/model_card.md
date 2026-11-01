# Model Card: Early Diabetes Retinal Risk Screening Network

**Model Name**: Diabetes-Retina-Screen-V1  
**Architecture**: ResNet50 / Modern ConvNet Backbone with Platt-Calibrated Sigmoid Head  
**Version**: 0.1.0-alpha  
**Date**: 2026-11-01  

---

## 1. Intended Use & Target Population
- **Intended Purpose**: Assistive community-level early Type 2 diabetes risk screening.
- **Target Population**: Adults ($\ge 18$ years) in rural and semi-urban community screening clinics in India.
- **Input Modality**: Digital color retinal fundus photograph (macula or optic-disc centered, minimum $300 \times 300$ resolution).
- **Primary Output**: Calibrated risk score ($0.0 - 1.0$) representing estimated probability of systemic diabetes.

---

## 2. Factors, Metrics & Ethical Considerations
- **Evaluation Metrics**: AUROC, AUPRC, Sensitivity, Specificity, Brier score, Expected Calibration Error.
- **Fairness & Demographic Subgroups**: Evaluated across sex (Female vs. Male) and age strata ($<45$, $45-60$, $>60$).
- **Primary Clinical Focus**: Subgroup evaluation on individuals with **No Visible Diabetic Retinopathy (DR = 0)**.

---

## 3. Limitations & Out-of-Scope Uses
- Not intended for diagnosing diabetic macular edema (DME) or staging proliferative retinopathy.
- Not validated on neonates, pediatric cohorts, or eyes with severe mature cataracts obscuring fundus visibility.
- Never to be used as a standalone diagnostic determinant without laboratory blood confirmation.

