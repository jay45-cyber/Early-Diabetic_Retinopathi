# Research Gap Analysis

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Auditor**: Lead AI Research Engineer  

---

## 1. Executive Summary
Extensive literature exists on automated detection of **Diabetic Retinopathy (DR)** from retinal fundus photographs. However, a significant research gap persists at the intersection of **early systemic Type 2 diabetes risk screening** and **low-resource rural healthcare settings**.

---

## 2. Identified Research Gaps

### Gap 1: Conflation of Retinopathy with Diabetes
- **Current State**: Over 90% of published medical computer vision studies evaluate models on datasets such as APTOS 2019, IDRiD, or Messidor, treating the problem as DR lesion detection.
- **The Blind Spot**: DR typically manifests only after 5 to 10 years of sustained hyperglycemia. Relying on DR lesions misses the window for early diabetes risk screening and lifestyle intervention.
- **Project Contribution**: We isolate and evaluate participants with **Grade 0 Diabetic Retinopathy (normal-appearing retina)** to determine whether sub-clinical retinal remodeling contains predictive signal for systemic diabetes.

### Gap 2: Demographic & Domain Generalization in Rural India
- **Current State**: Systemic prediction models (e.g., Poplin et al. 2018) were predominantly trained and validated on UK Biobank (predominantly European ancestry) and US cohorts.
- **The Blind Spot**: Indian populations exhibit distinct ocular pigmentation, higher diabetes risk at lower body mass index (the "Asian Indian Phenotype"), and earlier age of onset. Furthermore, rural Indian healthcare centers utilize portable handheld fundus cameras with variable illumination and artifact patterns rather than high-end benchtop hospital cameras.
- **Project Contribution**: Integration of image quality validation, robust preprocessing, and cross-domain evaluation suitable for handheld camera deployment.

### Gap 3: Absence of Probability Calibration in Triage
- **Current State**: Academic research papers frequently report uncalibrated AUROC or raw accuracy at an arbitrary 0.5 threshold.
- **The Blind Spot**: Community healthcare workers (e.g., ASHA workers in India) require well-calibrated screening probabilities to balance false-positive laboratory referral costs against the clinical risk of missing undiagnosed diabetes.
- **Project Contribution**: Mandatory post-hoc probability calibration (Platt scaling / Isotonic regression) and Brier score evaluation on locked validation splits.

### Gap 4: Clinically Plausible Explainability
- **Current State**: Saliency heatmaps (Grad-CAM) are often presented uncritically as "proof" of biomarkers, even when models focus on image borders or vignetting.
- **Project Contribution**: Rigorous explainability evaluation distinguishing vascular focus from imaging artifacts, accompanied by explicit clinical disclaimers.

