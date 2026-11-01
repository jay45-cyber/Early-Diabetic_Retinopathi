# Data Governance, Ethics & Patient Privacy Protocol

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Applicable Standards**: HIPAA Privacy Rule, Indian Digital Personal Data Protection (DPDP) Act 2023, Declaration of Helsinki  

---

## 1. Principles of Medical Data Ethics

1. **Patient De-Identification & Privacy**:
   - All direct identifiers (patient names, phone numbers, Aadhaar numbers, national identity cards, clinic registration numbers) must be permanently purged or cryptographically hashed before ingest.
   - Any re-identification mapping key must remain strictly under institutional control and is completely forbidden from entering repository storage, logs, or code.
2. **Authorized Data Acquisition**:
   - Only publicly accessible, institutional, or ethically approved datasets with appropriate Data Use Agreements (DUA) (e.g., PhysioNet, Kaggle Academic, IEEE DataPort) shall be utilized.
   - Web scraping of unverified patient photographs or unauthorized hospital PACS scraping is strictly prohibited.
3. **No Protected Health Information (PHI) in Version Control**:
   - Strict `.gitignore` rules prevent raw images, patient manifests with potential indirect identifiers, and local training logs from being committed to Git.

---

## 2. Storage Boundaries & Access Controls

- **Raw Data Layer (`data/raw/`)**: Read-only directory containing immutable original archives and checksum manifests.
- **Interim Data Layer (`data/interim/`)**: Contains quality-filtered images and standardized crops with intermediate metadata.
- **Processed Data Layer (`data/processed/`)**: Contains standardized, preprocessed tensors and frozen partition manifests.
- **Git Repository Boundary**: Git tracks only modular source code, configuration files, test scripts, and aggregate non-identifiable documentation.

