# Requirements Traceability Matrix (RTM)

**Project**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Last Updated**: 2026-11-01  

---

| Req ID | Research / Clinical Requirement | Architectural Design | Implementation Component | Verification & Test | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Distinguish systemic diabetes screening from diabetic retinopathy grading. | `docs/research_scope.md` | `config/dataset_config.yaml` | `tests/test_patient_grouping.py` | Verified |
| **REQ-02** | Independent clinical ground truth (HbA1c >= 6.5%, FPG >= 126 mg/dL). | `docs/clinical_reference_label_protocol.md` | `src/data/patient_manifest.py` | Schema validation | Verified |
| **REQ-03** | Grouped patient splitting; both eyes strictly in same split. | `docs/patient_level_splitting_and_leakage_audit.md` | `src/data/grouped_split.py` | `tests/test_split_integrity.py` | In Progress |
| **REQ-04** | Detection of exact & perceptual image duplicates. | `docs/data_quality_audit.md` | `src/data/duplicate_detection.py` | `tests/test_duplicate_detection.py` | In Progress |
| **REQ-05** | Preprocessing pipeline: circular crop, quality check, normalization. | `docs/preprocessing_specification.md` | `src/data/preprocessing.py` | `tests/test_image_preprocessing.py` | In Progress |
| **REQ-06** | Baseline ResNet50 model with reproducible training. | `docs/model_architecture_and_rationale.md` | `src/models/baseline_resnet.py` | Loss & metric convergence | Planned |
| **REQ-07** | Advanced backbones (EfficientNetV2, ConvNeXt, Foundation Models). | `docs/model_architecture_and_rationale.md` | `src/models/efficientnet.py` | Benchmark comparisons | Planned |
| **REQ-08** | Clinically calibrated risk probability (Platt scaling / Isotonic). | `docs/evaluation_and_statistical_analysis.md` | `src/evaluation/calibration.py` | Brier score & calibration curves | Planned |
| **REQ-09** | Subgroup analysis on participants with **no visible DR (DR = 0)**. | `docs/research_questions.md` | `src/evaluation/subgroup_analysis.py` | Subgroup AUROC/Sensitivity | Planned |
| **REQ-10** | Explainability visualizations (Grad-CAM++ / saliency maps). | `docs/explainability_protocol.md` | `src/explainability/gradcam.py` | Heatmap generation tests | Planned |
| **REQ-11** | Interactive screening prototype with quality filter and disclaimer. | `docs/application_and_inference_specification.md` | `app/streamlit_app.py` | `tests/test_inference.py` | Planned |
| **REQ-12** | Privacy, PHI safety, and zero leakage to Git. | `docs/security_privacy_and_safety.md` | `.gitignore`, `tests/` | Git diff & secret audits | Verified |

