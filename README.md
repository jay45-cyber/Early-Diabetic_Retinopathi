# Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3119/)
[![Research Grade Medical AI](https://img.shields.io/badge/research-medical%20AI-red.svg)](#)
[![Status: Phase 0/WP1 Active](https://img.shields.io/badge/status-Phase%200%20Complete-green.svg)](docs/PROJECT_STATUS.md)

## 1. Project Overview & Identity
- **Academic Context**: M.Tech Machine Learning and Artificial Intelligence Research Project.
- **Primary Research Objective**: Investigate whether deep learning can identify retinal microvascular and morphological characteristics associated with previously undiagnosed Type 2 diabetes from retinal fundus photographs.
- **Core Clinical Investigation**: Determine if the model can identify diabetes-associated retinal patterns in individuals **without clinically visible diabetic retinopathy (DR)**.
- **Primary Clinical Output**: A calibrated diabetes screening-risk score suitable as an assistive screening-support tool.
- **Secondary Outputs**: Explainability heatmaps (Grad-CAM++ / Integrated Gradients), automated image quality assessment, subgroup analysis, and an interactive screening prototype.

> [!IMPORTANT]
> **Scientific Integrity & Medical AI Principles**:
> 1. DR severity grades (e.g. from APTOS/IDRiD) are **not** substitutes for laboratory-confirmed diabetes ground truth (HbA1c / FPG / OGTT).
> 2. A normal retinal image does not indicate a non-diabetic individual.
> 3. Visible DR does not independently substitute for clinical diabetes verification.
> 4. Patient-level separation is strictly enforced: both eyes and multiple visits for any participant remain in the exact same partition.

---

## 2. Repository Structure
```
project_ML/
├── config/                 # YAML configuration files (project, dataset, training, evaluation)
├── docs/                   # Single source of truth for living research documentation
│   ├── development_logs/   # Contemporeneous dated work-item logs
│   ├── PROJECT_STATUS.md   # Current status, work packages, blockers, and next actions
│   ├── IMPLEMENTATION_PLAN.md # Approved Phase 1 WP1-WP12 roadmap
│   ├── WORKSPACE_AUDIT.md  # Hardware, software, and environment baseline
│   └── ...                 # Full suite of technical specifications and protocols
├── data/                   # Data directories (raw, interim, processed, external_test, manifests)
├── notebooks/              # Jupyter notebooks for exploratory data analysis and audits
├── src/                    # Modular source code
│   ├── data/               # Manifest generation, quality audit, duplicate detection, splitting
│   ├── models/             # ResNet50 baseline, EfficientNetV2, ConvNeXt, foundation models
│   ├── training/           # Reproducible trainer, loss functions, callbacks
│   ├── evaluation/         # Metrics, calibration curves, confidence intervals, leakage audits
│   ├── explainability/     # Grad-CAM, Integrated Gradients, clinical plausibility
│   ├── inference/          # Predictor, input validation, risk scoring
│   └── utils/              # Seed, logging, config loader
├── scripts/                # Standalone execution scripts
├── tests/                  # Automated pytest suite (leakage, grouping, preprocessing, inference)
├── app/                    # Streamlit screening-support prototype
├── models/checkpoints/     # Model weights (tracked locally, excluded from git)
├── outputs/                # Evaluation figures, metrics tables, and explainability plots
├── requirements.txt        # Python dependency manifest
├── pyproject.toml          # Package configuration and test markers
└── .gitignore              # Strict privacy, PHI, and artifact safety rules
```

---

## 3. Environment & Getting Started
```powershell
# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Install core dependencies
pip install -r requirements.txt
```

---

## 4. Documentation Source of Truth
All research progress, implementation logs, scientific decisions, and test results are contemporaneously recorded in [`docs/`](docs/).
- [Implementation Plan (WP1–WP12)](docs/IMPLEMENTATION_PLAN.md)
- [Project Status & Work Package Tracker](docs/PROJECT_STATUS.md)
- [Workspace & Hardware Audit](docs/WORKSPACE_AUDIT.md)
- [Traceability Matrix](docs/TRACEABILITY_MATRIX.md)

