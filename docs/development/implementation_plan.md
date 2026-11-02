# Unified Phase 1 Implementation Plan

**Document**: `docs/development/implementation_plan.md`  
**Date**: 2026-11-02  
**Implementation Phase**: **PHASE 1 — CONTINUED RESEARCH ENGINEERING, DATA INTEGRATION, MODEL DEVELOPMENT AND FINAL RELEASE**  

---

## 1. Principles of Implementation
1. **Single Unified Phase**: All ongoing work packages (WP1 through WP12) execute sequentially within this single Phase 1.
2. **Scientific Rigor Over Speed**: Never fabricate datasets, synthetic samples, or benchmark metrics.
3. **Contemporaneous Documentation**: Every engineering task must update the corresponding `docs/` documents in real time.

---

## 2. Work Package Execution Plan

### WP1 — Research & Documentation Verification
- Cross-check all clinical research definitions, literature matrices, and gap analyses.
- Verify separation between DR grading (ICDR 0–4) and systemic diabetes prediction (HbA1c/FPG).
- Ensure zero unverified claims exist in documentation.

### WP2 — Dataset Ingestion & Integration
- Implement modular dataset adapters under `src/data/adapters/`:
  - `brset_adapter.py`: Parses PhysioNet BRSET schema, extracts participant IDs, EHR diabetes diagnoses, and DR grades.
  - `aptos_adapter.py`: Ingests APTOS 2019 images and grades, explicitly tagging records as auxiliary DR representations.
  - `idrid_adapter.py`: Ingests Indian rural hospital cohort with DR lesions.
  - `messidor_adapter.py`: Ingests Messidor/Messidor-2 for external domain validation.
  - `local_folder_adapter.py`: Scans user-provided local folder structures.

### WP3 — Data Validation & Quality Auditing
- Create `src/data/data_validator.py` performing automated checks on image integrity, dimensions, format, perceptual duplicate detection, and camera/site distributions.
- Produce comprehensive JSON and Markdown audit reports.

### WP4 — Patient Manifest & Leakage-Safe Splitting
- Formalize grouped patient partitioning supporting site and camera held-out splits.
- Guarantee that both eyes (OD/OS) and serial visits remain permanently locked to the same partition.

### WP5 — Preprocessing & Augmentation
- Formalize circular retinal masking, bounding contour cropping, resolution resizing ($384 \times 384$), and ImageNet standardization.
- Enforce training-only data augmentation.

### WP6 — Baseline ML & Deep Learning
- Formalize model zoo in `src/models/`:
  - `baseline_resnet.py`: ResNet50 benchmark.
  - `efficientnet.py`: EfficientNetV2-S.
  - `convnext.py`: ConvNeXt-Tiny/Small architecture.
  - `retinal_foundation_model.py`: RETFound foundation model adapter interface.
  - `multimodal_model.py`: Image + tabular clinical metadata late-fusion network.

### WP7 — Cloud GPU Training Preparation
- Create `notebooks/colab_gpu_pipeline.ipynb`:
  - Interactive Google Colab notebook for GPU training (T4/A100).
  - Mounts Google Drive, clones repo, verifies CUDA, runs training, saves checkpoints, and logs metrics.

### WP8 — Generalization & Anti-Overfitting Engineering
- Expand `src/evaluation/confidence_intervals.py` with patient-level bootstrap resampling (1,000 iterations).
- Refine Platt probability calibration and Expected Calibration Error (ECE) calculations.
- Implement DR=0 subgroup evaluation pipeline.

### WP9 — Explainable AI Development
- Implement `src/explainability/integrated_gradients.py` and `src/explainability/occlusion.py` alongside Grad-CAM++.
- Add four-quadrant error analysis (TP, TN, FP, FN) visual reporting.

### WP10 — Application & Inference Improvements
- Upgrade `app/streamlit_app.py` with model versioning, metadata inputs, uncertainty estimation, and clear ungradable image alerts.

### WP11 — Testing, Security & Reproducibility
- Expand pytest suite to cover adapters, new models, and end-to-end integration flows.
- Perform privacy and credential safety scans against `.gitignore`.

### WP12 — Final Integration & Release
- Verify all acceptance gates.
- Produce `docs/project_management/final_project_report.md`.
- Commit and push final release to `origin/main`.

