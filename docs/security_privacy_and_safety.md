# Security, Privacy & Clinical Safety Protocol

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Auditor**: Lead AI Research Engineer / MLOps Lead  

---

## 1. Protected Health Information (PHI) & Secret Safety
1. **Zero Secret Footprint**: No API keys, credentials, private access tokens, or institutional passwords are committed to Git.
2. **Patient Identifier Cryptographic Hashing**: All patient IDs are irreversibly hashed. Direct medical record numbers (MRNs) are purged at ingestion.
3. **Automated Git Exclusions**: The repository [`.gitignore`](file:///c:/Users/Jay/projects/project_ML/.gitignore) prevents accidental staging of `.csv`, `.parquet`, `.png`, `.pt`, `.pth`, `.onnx`, and `.log` files.

---

## 2. Clinical Safety Guardrails
1. **No Therapeutic Recommendations**: The AI engine never outputs drug dosages, insulin regimens, or medical management plans.
2. **Referral Guidance Only**: Outputs are categorized strictly into triage referral recommendations:
   - *Low Risk*: Routine annual ophthalmic and health screening.
   - *Moderate Risk*: Recommended clinical consultation and baseline fasting blood glucose check within 3 months.
   - *High Risk*: Priority referral for confirmatory venous HbA1c testing.
3. **Abstention Protocol**: Low-quality images halt inference with an ungradable alert.

