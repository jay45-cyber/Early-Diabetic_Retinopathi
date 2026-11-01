# Data Dictionary: Unified Patient & Image Manifest Schema

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Schema Version**: 1.0.0  

---

## 1. Primary Manifest Schema (`manifests/patient_manifest.csv`)

| Field Name | Data Type | Constraint / Valid Values | Description | Clinical / Engineering Significance |
| :--- | :--- | :--- | :--- | :--- |
| `participant_id` | String | Non-null, Unique Hash | Anonymized unique participant identifier. | **Primary grouping key**; ensures all eyes and visits stay in one partition. |
| `image_id` | String | Non-null, Unique | Unique identifier for the retinal image file. | Primary key for image loading and artifact mapping. |
| `eye_side` | String | `["OD", "OS", "Unknown"]` | Anatomical eye (`OD`: Right eye, `OS`: Left eye). | Audits bilateral consistency and ocular symmetry. |
| `image_path` | String | Non-null, Valid relative path | Relative path from project root to image file. | Direct pointer for image loading pipelines. |
| `dataset_id` | String | `["BRSET", "mBRSET", "APTOS", "IDRiD", "Messidor"]` | Provenance dataset source identifier. | Tracks site origin and domain generalization splits. |
| `site_id` | String | Nullable | Healthcare facility, clinic, or screening center ID. | Enables site-held-out evaluation. |
| `camera_id` | String | Nullable | Fundus camera make/model (e.g., `Canon_CR2`, `Nikon`). | Enables camera-held-out domain generalization. |
| `capture_date` | Date | Nullable (YYYY-MM-DD) | Date of photograph capture. | Enables temporal drift and longitudinal analysis. |
| `image_quality` | Float | Range `[0.0, 1.0]` or `["Gradable", "Ungradable"]` | Automated or expert-assessed image quality score. | Filters ungradable images to prevent false predictions. |
| `diabetes_label` | Integer | `[0, 1]` or Nullable | Binary screening target (`0`: Non-Diabetic, `1`: Diabetic). | **Primary supervised learning target**. |
| `diabetes_label_source` | String | `["Laboratory_HbA1c", "Laboratory_FPG", "EHR_Diagnosis", "Self_Report", "Unknown"]` | Origin of the diabetes diagnostic confirmation. | Enforces data governance: only valid sources are trained. |
| `hba1c` | Float | Nullable (percentage, e.g., `6.8`) | Measured glycated hemoglobin value. | Gold standard laboratory reference biomarker. |
| `fasting_glucose` | Float | Nullable (mg/dL, e.g., `135.0`) | Measured fasting plasma glucose value. | Secondary laboratory reference biomarker. |
| `dr_grade` | Integer | Range `[0, 4]` or Nullable | International Clinical DR severity score (`0`: None, `1`: Mild, `2`: Moderate, `3`: Severe, `4`: PDR). | Crucial covariate for the **DR = 0 subgroup analysis**. |
| `previous_diabetes_diagnosis` | Boolean | `[True, False]` or Nullable | Prior clinical history of diabetes diagnosis. | Distinguishes known from undiagnosed cases. |
| `age` | Integer | Nullable, Range `[18, 100]` | Patient age in years. | Demographic covariate for fairness and subgroup analysis. |
| `sex` | String | `["Female", "Male", "Other", "Unknown"]` | Biological sex of participant. | Demographic covariate for subgroup analysis. |

