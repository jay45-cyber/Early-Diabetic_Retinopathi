# Project Risk Register & Mitigation Strategy

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Last Updated**: 2026-11-01  

---

| Risk ID | Category | Description | Likelihood | Impact | Mitigation Strategy | Owner | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | Clinical Data | DR severity used as false proxy for diabetes diagnosis. | High | Fatal | Enforced ADR-001: Require independent laboratory HbA1c/FPG ground truth; audit APTOS/IDRiD to prevent control group contamination. | Clinical AI Lead | Mitigated |
| **RSK-02** | Methodology | Bilateral eye correlation causes patient-level data leakage. | High | Critical | Enforced ADR-002: Grouped patient k-fold splitting; automated leakage tests fail pipeline if overlap occurs. | ML Architect | Mitigated |
| **RSK-03** | Hardware | Local compute has 5.74 GB RAM & no discrete NVIDIA GPU. | Certain | Moderate | Cap local batch sizes (8–16); structure modular PyTorch scripts for export to GPU-accelerated cloud nodes. | MLOps Lead | Active |
| **RSK-04** | Algorithmic | Overconfidence in uncalibrated neural network probabilities. | High | High | Enforced post-hoc Platt scaling and reliability curve verification on validation partition. | Biostatistician | Mitigated |
| **RSK-05** | Interpretability | Model relies on border vignetting or camera dust shortcuts. | Moderate | High | Automated image circular cropping and Grad-CAM++ saliency plausibility checks across error quadrants. | CV Engineer | Mitigated |
| **RSK-06** | Governance | Accidental exposure of Protected Health Information (PHI). | Low | High | Rigorous `.gitignore` rules, cryptographic hashing of IDs, zero raw patient data in Git. | Security Lead | Mitigated |

