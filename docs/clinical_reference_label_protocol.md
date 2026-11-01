# Clinical Reference Label Protocol & Diagnostic Standards

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Clinical Reference Guidelines**: ICMR (Indian Council of Medical Research) & ADA (American Diabetes Association) Standards of Medical Care  

---

## 1. Laboratory Diagnostic Reference Thresholds

To establish scientifically rigorous and clinically defensible ground-truth labels, the project adopts international consensus thresholds for Type 2 Diabetes Mellitus:

| Diagnostic Biomarker | Normal (Non-Diabetic) | Prediabetes (Impaired) | Diabetes Mellitus (Screening Target) |
| :--- | :--- | :--- | :--- |
| **HbA1c (Glycated Hemoglobin)** | $< 5.7\%$ ($< 39$ mmol/mol) | $5.7\% - 6.4\%$ ($39 - 47$ mmol/mol) | $\ge 6.5\%$ ($\ge 48$ mmol/mol) |
| **Fasting Plasma Glucose (FPG)** | $< 100$ mg/dL ($< 5.6$ mmol/L) | $100 - 125$ mg/dL ($5.6 - 6.9$ mmol/L) | $\ge 126$ mg/dL ($\ge 7.0$ mmol/L) |
| **2-Hour Post-Load Glucose (OGTT)** | $< 140$ mg/dL ($< 7.8$ mmol/L) | $140 - 199$ mg/dL ($7.8 - 11.0$ mmol/L) | $\ge 200$ mg/dL ($\ge 11.1$ mmol/L) |
| **Random Plasma Glucose** | N/A | N/A | $\ge 200$ mg/dL with classic hyperglycemic symptoms |

---

## 2. Binary Screening Target Formulation

For binary risk screening ($Y \in \{0, 1\}$):

- **Class 1 (Diabetic Risk Screen Positive)**:
  - Documented clinical diagnosis of Type 2 Diabetes in electronic health records, OR
  - Confirmed laboratory test with $\text{HbA1c} \ge 6.5\%$ or $\text{FPG} \ge 126$ mg/dL.
- **Class 0 (Diabetic Risk Screen Negative)**:
  - Verified non-diabetic control with $\text{HbA1c} < 5.7\%$ and $\text{FPG} < 100$ mg/dL, with zero medical history of anti-diabetic medication.
- **Prediabetes Policy**:
  - In primary binary benchmark experiments, individuals with borderline/prediabetic HbA1c ($5.7\% - 6.4\%$) are documented in the manifest. In primary classification, they are evaluated separately to prevent boundary noise from contaminating the core decision surface.

---

## 3. Disconnection from Diabetic Retinopathy (DR) Staging

Under no circumstances will the presence or absence of diabetic retinopathy lesions dictate the ground truth label:
$$\text{Label}(P) = f(\text{Laboratory Glycemia}(P)) \quad \text{NOT} \quad f(\text{Retinal Lesion Score}(P))$$

- **DR = 0 & Diabetes = 1**: Participant has systemic diabetes, but has not developed visible retinal microvascular damage. This is our **primary cohort of clinical interest**.
- **DR = 0 & Diabetes = 0**: Healthy non-diabetic control.
- **DR > 0 & Diabetes = 1**: Established diabetes with clinical microvascular sequelae.

