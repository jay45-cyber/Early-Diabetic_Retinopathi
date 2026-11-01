# Single End-to-End Implementation Plan (Phase 1: WP1–WP12)

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Architecture Principle**: One unified implementation phase consisting of sequential, gated work packages.

---

## Work Package Breakdown & Acceptance Gates

### WP1 — Research Integration & Scientific Scope
- **Objective**: Synthesize research objectives, hypotheses, clinical definitions, and terminology.
- **Dependencies**: None.
- **Files Modified/Created**: `docs/research_scope.md`, `docs/research_questions.md`, `docs/literature_matrix.csv`, `docs/research_gap_analysis.md`, `docs/scientific_assumptions_and_decisions.md`.
- **Gate Criteria**:
  1. Clear distinction established between: (a) diabetic retinopathy detection, (b) DR severity grading, and (c) Type 2 diabetes prediction.
  2. Research question formulated for participants with **no visible diabetic retinopathy**.
  3. No unsupported novelty claims; primary outcome explicitly defined.

### WP2 — Dataset Feasibility & Data Governance
- **Objective**: Audit candidate retinal datasets (BRSET, mBRSET, EyePACS, Messidor-2, APTOS, IDRiD) for laboratory-confirmed diabetes ground truth vs. DR grades.
- **Dependencies**: WP1.
- **Files Modified/Created**: `docs/dataset_feasibility_audit.md`, `docs/data_dictionary.md`, `docs/data_governance_and_ethics.md`, `docs/clinical_reference_label_protocol.md`.
- **Gate Criteria**:
  1. Datasets classified into primary diabetes outcome, auxiliary DR representation, or external test.
  2. Provenance of diabetes labels documented (HbA1c vs. fasting glucose vs. self-report).
  3. Strict prohibition of using DR severity alone as a surrogate for diabetes diagnosis.

### WP3 — Workspace, Environment & Engineering Foundation
- **Objective**: Finalize directory structure, virtual environment, configuration files, and testing framework.
- **Dependencies**: Phase 0.
- **Files Modified/Created**: `config/*.yaml`, `requirements.txt`, `pyproject.toml`, `docs/WORKSPACE_AUDIT.md`.
- **Gate Criteria**:
  1. Virtual environment operational; dependencies verified.
  2. Configuration management centralized and modular.
  3. `.gitignore` strictly protects patient data, weights, and temporary artifacts.

### WP4 — Data Inventory, Patient Manifest & Quality Audit
- **Objective**: Build standardized patient manifests with strict schema validation, duplicate detection, and image quality checks.
- **Dependencies**: WP2, WP3.
- **Files Modified/Created**: `src/data/dataset_inventory.py`, `src/data/patient_manifest.py`, `src/data/duplicate_detection.py`, `src/data/image_quality.py`, `docs/data_quality_audit.md`.
- **Gate Criteria**:
  1. Manifest schema validated with zero inferred or hallucinated labels.
  2. Exact and perceptual image duplicates detected and cataloged.
  3. Ungradable or corrupted images identified before splitting.

### WP5 — Leakage-Resistant Splitting & Preprocessing Pipeline
- **Objective**: Implement patient-grouped stratified splitting and a reproducible preprocessing pipeline.
- **Dependencies**: WP4.
- **Files Modified/Created**: `src/data/grouped_split.py`, `src/data/preprocessing.py`, `tests/test_patient_grouping.py`, `tests/test_split_integrity.py`, `docs/patient_level_splitting_and_leakage_audit.md`, `docs/preprocessing_specification.md`.
- **Gate Criteria**:
  1. Zero patient overlap across train, validation, and internal test sets.
  2. Both eyes and repeated visits for any individual strictly isolated to one partition.
  3. Automated leakage test passes and halts pipeline on any detected leakage.
  4. Preprocessing statistics fitted solely on the training partition.

### WP6 — Baseline Model & Controlled Training Pipeline
- **Objective**: Implement a reproducible ResNet50 baseline with early stopping, weight decay, and metric tracking.
- **Dependencies**: WP5.
- **Files Modified/Created**: `src/models/baseline_resnet.py`, `src/training/trainer.py`, `src/training/loss_functions.py`, `src/training/callbacks.py`, `scripts/train_baseline.py`, `docs/model_architecture_and_rationale.md`, `docs/experiment_log.csv`.
- **Gate Criteria**:
  1. Reproducibility seed fixed; deterministic behavior enforced where supported.
  2. Training/validation loss curves logged and evaluated for overfitting.
  3. Validation AUROC and calibration evaluated; no pre-filled or fabricated metrics.

### WP7 — Advanced Model & Ablation Experiments
- **Objective**: Implement and evaluate modern deep learning backbones (EfficientNetV2, ConvNeXt, and RETFound foundation model where compute allows).
- **Dependencies**: WP6.
- **Files Modified/Created**: `src/models/efficientnet.py`, `src/models/convnext.py`, `src/models/retinal_foundation_model.py`, `docs/experiment_log.csv`.
- **Gate Criteria**:
  1. Identical patient partitions and evaluation protocols applied across all architectures.
  2. Controlled comparison against the ResNet50 baseline.
  3. Ablation studies on preprocessing and augmentation documented.

### WP8 — Generalization, Calibration & Statistical Evaluation
- **Objective**: Conduct rigorous statistical evaluation including AUROC, AUPRC, Brier score, Platt scaling calibration, and subgroup analyses.
- **Dependencies**: WP6, WP7.
- **Files Modified/Created**: `src/evaluation/classification_metrics.py`, `src/evaluation/calibration.py`, `src/evaluation/confidence_intervals.py`, `src/evaluation/subgroup_analysis.py`, `docs/evaluation_and_statistical_analysis.md`, `docs/generalization_and_external_validation.md`.
- **Gate Criteria**:
  1. Bootstrap 95% confidence intervals calculated using patient-level resampling.
  2. Probability calibration verified with calibration curves, slope, and intercept.
  3. Dedicated subgroup evaluation on **participants with no visible diabetic retinopathy (DR = 0)**.

### WP9 — Explainable AI & Clinical Plausibility Review
- **Objective**: Implement Grad-CAM++, Integrated Gradients, and visual explainability reports for true/false positives and negatives.
- **Dependencies**: WP6, WP8.
- **Files Modified/Created**: `src/explainability/gradcam.py`, `src/explainability/integrated_gradients.py`, `docs/explainability_protocol.md`, `outputs/explainability/`.
- **Gate Criteria**:
  1. Heatmaps generated without exposing patient health information.
  2. Clinical disclaimer explicitly noted: visual saliency does not constitute biological proof of causality.
  3. Qualitative audit of false positives and false negatives documented.

### WP10 — Inference & Screening-Support Prototype
- **Objective**: Develop an interactive Streamlit screening-support prototype.
- **Dependencies**: WP5, WP8, WP9.
- **Files Modified/Created**: `app/streamlit_app.py`, `src/inference/predictor.py`, `src/inference/image_validation.py`, `docs/application_and_inference_specification.md`.
- **Gate Criteria**:
  1. Complete verification pipeline: image format validation -> quality/gradability check -> calibrated risk output -> explainability visualization.
  2. Ungradable images trigger abstention rather than false confidence.
  3. Clear, prominent research disclaimer: screening prototype only, not a clinical diagnostic replacement.

### WP11 — Integrated Testing, Security & Research Reporting
- **Objective**: Execute end-to-end unit, integration, and security tests; compile the final dissertation-grade research report and model card.
- **Dependencies**: WP1 through WP10.
- **Files Modified/Created**: `tests/`, `docs/test_strategy_and_reports.md`, `docs/security_privacy_and_safety.md`, `docs/model_card.md`, `docs/risk_register.md`, `docs/final_research_report.md`.
- **Gate Criteria**:
  1. All automated test suites passing.
  2. Model Card and Risk Register fully documented.
  3. No PHI or credentials in git; all research limitations transparently disclosed.

### WP12 — Final Completion Audit & Git Release to main
- **Objective**: Final completion audit, release checklist verification, and clean push to `origin/main`.
- **Dependencies**: WP11.
- **Files Modified/Created**: `docs/GIT_RELEASE_CHECKLIST.md`, `docs/CHANGELOG.md`.
- **Gate Criteria**:
  1. Every work package completed or explicitly recorded as blocked with documented evidence.
  2. Git tree clean, branch synchronized with `origin/main`.
  3. Release push executed and verified via git output.

