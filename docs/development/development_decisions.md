# Development Decisions & Architecture Records

**Project**: Explainable AI for Early Type 2 Diabetes Risk Screening Using Retinal Fundus Images in Rural India  

---

## DEC-001: Separation of DR Grading from Diabetes Diagnosis
- **Context**: Medical AI literature frequently confounds Diabetic Retinopathy detection with Type 2 diabetes prediction.
- **Decision**: Restrict the primary supervised target strictly to laboratory-confirmed diabetes status (HbA1c >= 6.5%, FPG >= 126 mg/dL). DR severity is treated as a clinical covariate, enabling the dedicated $\text{DR} = 0$ sub-clinical screening investigation.
- **Status**: **Approved & Enforced**.

## DEC-002: Modular Ingestion Adapter Pattern
- **Context**: Diverse public datasets (BRSET, APTOS, IDRiD, Messidor) present divergent column naming, label semantics, and directory layouts.
- **Decision**: Implement the Adapter design pattern under `src/data/adapters/`. Each adapter maps raw dataset quirks into the unified `patient_manifest` schema without modifying original raw data.
- **Status**: **Approved & Enforced**.

## DEC-003: Patient-Grouped Stratified Partitioning
- **Context**: Random image-level splitting introduces massive data leakage due to bilateral ocular correlation.
- **Decision**: Partition strictly by participant ID (`participant_id`). Both eyes and all longitudinal clinic visits remain grouped in the same partition.
- **Status**: **Approved & Enforced**.

## DEC-004: Decoupled Cloud GPU Training Support
- **Context**: Host development environment possesses integrated graphics and 5.74 GB RAM.
- **Decision**: Provide `notebooks/colab_gpu_pipeline.ipynb` enabling zero-friction cloud GPU execution on Google Colab while maintaining identical code modules.
- **Status**: **Approved & Enforced**.

