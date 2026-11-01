# Documentation Architecture & Single Source of Truth

This `docs/` directory is the single source of truth for the entire research project, adhering strictly to the **Mandatory Documentation Rule** defined in the master research specification.

## Core Living Records
- [WORKSPACE_AUDIT.md](WORKSPACE_AUDIT.md): Comprehensive inventory of local compute, memory, storage, OS, Python runtime, Git remote, and baseline environment constraints.
- [PROJECT_STATUS.md](PROJECT_STATUS.md): Current overarching status, active work packages, blockers, and next actions.
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md): The unified single-phase implementation plan covering Work Packages WP1 through WP12.
- [PROGRESS_TRACKER.md](PROGRESS_TRACKER.md): Dated milestone and work-package progress with verifiable acceptance criteria.
- [TRACEABILITY_MATRIX.md](TRACEABILITY_MATRIX.md): Traceability from research questions and clinical objectives to code, configs, tests, and outputs.
- [scientific_assumptions_and_decisions.md](scientific_assumptions_and_decisions.md): Architecture Decision Records (ADR) detailing clinical, statistical, and algorithmic choices.
- [errors_and_resolutions.md](errors_and_resolutions.md): Contemporaneous debugging log capturing root causes, fixes, and regression guards.
- [experiment_log.csv](experiment_log.csv): Machine-readable log of every completed model experiment.
- [GIT_RELEASE_CHECKLIST.md](GIT_RELEASE_CHECKLIST.md): Strict verification checklist governing commits and the final WP12 release push.

## Specialized Protocols & Specifications
- [research_scope.md](research_scope.md) & [research_questions.md](research_questions.md): Clinical definition of systemic diabetes screening vs. diabetic retinopathy detection.
- [dataset_feasibility_audit.md](dataset_feasibility_audit.md): Systematic audit of public fundus datasets (BRSET, Messidor-2, EyePACS, APTOS, IDRiD).
- [clinical_reference_label_protocol.md](clinical_reference_label_protocol.md): Clinical ground truth standard (HbA1c, FPG, OGTT thresholds).
- [patient_level_splitting_and_leakage_audit.md](patient_level_splitting_and_leakage_audit.md): Grouped patient partitioning and leakage prevention rules.
- [preprocessing_specification.md](preprocessing_specification.md): Circular crop, illumination normalization, and image gradability criteria.
- [model_architecture_and_rationale.md](model_architecture_and_rationale.md): Model hierarchy from baseline ResNet50 to foundation models.
- [explainability_protocol.md](explainability_protocol.md): Grad-CAM++, Integrated Gradients, and medical plausibility review guidelines.
- [application_and_inference_specification.md](application_and_inference_specification.md): Streamlit screening prototype specification and safety disclaimers.

## Development Logs
All substantial tasks are recorded contemporaneously in [`docs/development_logs/`](development_logs/) using the standard work item template.

