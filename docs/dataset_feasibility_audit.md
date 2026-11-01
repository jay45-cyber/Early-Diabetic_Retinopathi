# Dataset Feasibility & Ground-Truth Provenance Audit

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Auditor**: Lead AI Research Engineer  
**Date**: 2026-11-01  

---

## 1. Executive Summary & Critical Distinction
A fatal methodological flaw in naive medical AI implementations is assuming that public Diabetic Retinopathy (DR) datasets can be directly repurposed for Type 2 Diabetes detection by labeling Grade 0 as "No Diabetes" and Grades 1–4 as "Diabetes".

> [!WARNING]
> In clinical cohorts such as **APTOS 2019** and **IDRiD**, all participating patients were recruited from diabetic specialty clinics. A patient with Grade 0 DR in APTOS is **diabetic without visible retinopathy**. Treating Grade 0 as "Non-Diabetic" completely invalidates the clinical label and causes severe label contamination.

---

## 2. Systematic Candidate Dataset Audit

| Dataset | Origin & Population | Patients / Images | Diabetes Ground Truth | DR Grading | Suitability Classification | Data Access & License |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BRSET** (Brazilian Retinal Screening) | Brazil (multi-ethnic public health system) | 8,524 patients / 16,266 images | **Yes** (EHR-confirmed Type 2 Diabetes; Yes/No) | Yes (ICDR 0–4) | **PRIMARY CANDIDATE**: Contains both diabetic and non-diabetic cohorts across all DR grades, enabling DR=0 analysis. | Open Access (PhysioNet Credentialed / CC-BY 4.0) |
| **mBRSET** (Multi-attribute BRSET) | Brazil | Subset of BRSET | **Yes** (Detailed demographic & systemic covariates) | Yes | **PRIMARY CANDIDATE**: Multimodal analysis with age, sex, and anatomical quality. | Open Access |
| **APTOS 2019** | India (Aravind Eye Hospital) | 3,662 images | **NO (All patients are diabetic)** | Yes (0–4) | **AUXILIARY ONLY**: Excellent Indian demographic representation, but strictly prohibited from serving as non-diabetic controls. | Open Access (Kaggle Research) |
| **IDRiD** | India (Nanded, Maharashtra) | 516 images | **NO (All patients are diabetic)** | Yes (0–4) + Lesion masks | **AUXILIARY ONLY**: Indian rural cohort; ideal for lesion segmentation and domain adaptation, but cannot train diabetes classifier. | Open Access (IEEE Dataport) |
| **Messidor / Messidor-2** | France (Hospital clinics) | 874 patients / 1,748 images | Partial / Inconsistent across cohorts | Yes (0–4) | **AUXILIARY / EXTERNAL TEST**: Useful for external domain generalization tests on DR detection. | Open Access / Research Agreement |
| **EyePACS** | USA (California Community Health) | 88,702 images | Limited to DR screening outcomes | Yes (0–4) | **REPRESENTATION LEARNING**: Pre-training retinal foundation encoders. | Research Access |

---

## 3. Dataset Roles in the Single Implementation Phase

```
                                  +---------------------------------------------+
                                  |    BRSET / mBRSET Primary Dataset           |
                                  |    (Diabetic vs. Non-Diabetic ground truth) |
                                  +----------------------+----------------------+
                                                         |
                              +--------------------------+--------------------------+
                              |                                                     |
               +--------------v---------------+                      +--------------v---------------+
               |    Primary Diabetes Model    |                      |   Subgroup Analysis Cohort   |
               |    (All Patients, Grouped)   |                      |   (DR Grade = 0 ONLY)        |
               +------------------------------+                      +------------------------------+

               +------------------------------+                      +------------------------------+
               | APTOS / IDRiD Indian Cohorts |                      | EyePACS / Messidor           |
               | (Auxiliary Retinal Features) |                      | (External Domain Robustness) |
               +------------------------------+                      +------------------------------+
```

---

## 4. Ground-Truth Data Governance Rules
1. **Clinical Reference Standard**: Labels must originate from verifiable biochemical evidence (HbA1c >= 6.5%, Fasting Plasma Glucose >= 126 mg/dL) or confirmed clinical medical diagnosis.
2. **No Self-Reported Fallback as Primary**: Self-reported diabetes questionnaires without medical record verification must not be treated as gold-standard ground truth.
3. **Data Integrity & Privacy**: All participant identifiers must be cryptographic hashes (`participant_id`), completely stripped of Protected Health Information (PHI).

