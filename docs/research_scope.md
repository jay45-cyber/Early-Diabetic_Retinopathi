# Research Scope & Clinical Problem Statement

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Academic Context**: M.Tech Research Project in Machine Learning and Artificial Intelligence  

---

## 1. Clinical Context & Healthcare Need in Rural India
In India, an estimated 77 to 100 million individuals live with diabetes, and up to **50% of rural cases remain undiagnosed** until severe complications emerge. In rural and low-resource community health centers (CHCs) and primary healthcare clinics (PHCs):
- Access to centralized biochemical laboratories for HbA1c or fasting venous plasma glucose testing is frequently constrained by logistics, reagent costs, cold-chain transport, and follow-up attrition.
- Conversely, digital non-mydriatic fundus cameras and portable smartphone-based ophthalmoscopes are increasingly deployed for community-level vision screening.
- The microvasculature of the human retina is the only in-vivo window where systemic vascular morphology, vessel caliber, arteriolar narrowing, venular dilation, branching angles, and fractal dimensions can be directly observed non-invasively.

---

## 2. Crucial Scientific Disambiguation
A fundamental flaw in previous computer vision studies is the conflation of diabetic eye disease with systemic diabetes. This project explicitly establishes three distinct clinical problems:

| Problem Domain | Definition | Ground Truth Origin | Role in this Research |
| :--- | :--- | :--- | :--- |
| **1. Diabetic Retinopathy (DR) Detection** | Detecting visible ophthalmological microvascular lesions (microaneurysms, hemorrhages, cotton-wool spots, neovascularization). | Ophthalmic exam / expert fundus grading. | **Auxiliary task only**; used to evaluate feature representations. |
| **2. DR Severity Classification** | Staging retinal damage into categories (0: None, 1: Mild NPDR, 2: Moderate, 3: Severe, 4: PDR). | International Clinical Diabetic Retinopathy (ICDR) scale. | **Subgroup covariate**; never used as a proxy for diabetes. |
| **3. Systemic Type 2 Diabetes Prediction** | Predicting whether the individual has systemic Type 2 diabetes mellitus, regardless of visible DR lesions. | **Independent laboratory biomarker** (HbA1c >= 6.5%, Fasting Glucose >= 126 mg/dL, or OGTT >= 200 mg/dL). | **PRIMARY RESEARCH TARGET**. |

---

## 3. The Core Clinical Research Hypothesis
Can deep convolutional and foundation neural network architectures detect subtle sub-clinical microvascular alterations indicative of systemic glycemic dysfunction in retinal fundus photographs of patients **who exhibit no clinically apparent diabetic retinopathy (DR Grade = 0)**?

### Scientific Guardrails:
1. **Never substitute DR grades for diabetes labels**: A participant with DR grade 0 (normal retina) may have had high HbA1c for years; conversely, retinal lesions can occasionally arise from hypertension or vein occlusions.
2. **Clinical Reference Standard**: The ground truth must stem from laboratory-confirmed biochemistry (HbA1c or fasting glucose) or documented clinical medical records.
3. **Screening-Support Role**: The model provides a calibrated risk assessment to prioritize high-risk rural individuals for definitive diagnostic blood work. It does not issue diagnostic declarations or treatment prescriptions.

