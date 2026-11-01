# Changelog

All notable technical and research changes to the **Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India** project are documented contemporaneously in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), adhering to Semantic Versioning.

---

## [0.1.0] - 2026-11-01
### Added
- **Phase 0 Baseline**: Initialized workspace, completed hardware and software audit (`docs/WORKSPACE_AUDIT.md`).
- **Git & GitHub Integration**: Configured Git credentials for `jay45-cyber`, synchronized remote `origin/main`, created initial commit `cc8a192`.
- **Runtime Environment**: Installed Python 3.11.9, created project virtual environment (`venv`), established `requirements.txt` and `pyproject.toml`.
- **Directory Hierarchy**: Established complete research scaffolding (`config/`, `docs/`, `data/`, `notebooks/`, `src/`, `tests/`, `app/`, `outputs/`).
- **Configuration Management**: Created modular YAML configs (`project_config.yaml`, `dataset_config.yaml`, `training_config.yaml`, `evaluation_config.yaml`).
- **Living Documentation**: Published full suite of foundational documentation:
  - `IMPLEMENTATION_PLAN.md` (WP1–WP12 end-to-end plan)
  - `PROJECT_STATUS.md` and `PROGRESS_TRACKER.md`
  - `TRACEABILITY_MATRIX.md`
  - `research_scope.md` and `research_questions.md`
  - `dataset_feasibility_audit.md` (distinguishing DR grading from diabetes)
  - `clinical_reference_label_protocol.md` (HbA1c / FPG standards)
  - `patient_level_splitting_and_leakage_audit.md`
  - `preprocessing_specification.md`
  - `model_architecture_and_rationale.md`
  - `evaluation_and_statistical_analysis.md`
  - `explainability_protocol.md`
  - `application_and_inference_specification.md`
  - `security_privacy_and_safety.md`
  - `model_card.md`
  - `risk_register.md`
  - `scientific_assumptions_and_decisions.md` (ADR-001 through ADR-004)
  - `errors_and_resolutions.md` (ERR-001 through ERR-003)
  - `development_logs/2026-11-01_phase0_workspace_audit.md`

