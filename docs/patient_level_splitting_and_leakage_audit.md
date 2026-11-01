# Patient-Level Splitting & Leakage Prevention Protocol

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Auditor**: Lead AI Research Engineer  

---

## 1. The Critical Data Leakage Hazard in Ophthalmic AI
In ophthalmological computer vision datasets, single participants routinely contribute multiple images:
1. **Bilateral Images**: Left eye (OS) and Right eye (OD).
2. **Multiple Fields**: Macula-centered, optic-disc centered, peripheral fields.
3. **Serial Follow-up Visits**: Images captured across multiple clinic visits.

If images are split randomly at the image level, a patient's left eye might appear in the training set while their right eye appears in the test set. Because both eyes share identical genetic background, systemic blood pressure, chronic glycemic exposure, and optical aberrations, the model easily memorizes patient-specific idiosyncrasies rather than learning generalized disease features. This produces **falsely inflated test accuracy (optimism bias)** that completely collapses on external clinical deployment.

---

## 2. Mandatory Splitting Rules

```
                             All Clinical Records & Retinal Images
                                              |
                               +--------------v---------------+
                               | Group By: participant_id     |
                               | (Both Eyes + All Visits)     |
                               +--------------+---------------+
                                              |
               +------------------------------+------------------------------+
               |                                                             |
      +--------v--------+                                           +--------v--------+
      | Development Set |                                           | External Cohort |
      | (e.g. BRSET)    |                                           | (Genuinely      |
      +--------+--------+                                           | Independent)    |
               |                                                    +-----------------+
    Stratified Group Split
       (70% / 15% / 15%)
               |
  +------------+------------+
  |            |            |
+-v-----+   +--v---+   +----v-------+
| Train |   | Val  |   | Locked Test|
| (70%) |   | (15%)|   | (15%)      |
+-------+   +------+   +------------+
```

1. **Atomic Unit of Partitioning**: The atomic unit is the unique individual (`participant_id`).
2. **Both-Eyes Rule**: The left eye (OS) and right eye (OD) of any participant **must never be separated** across different partitions.
3. **Locked Test Partition**: The internal test partition (15%) is strictly isolated and frozen. No hyperparameter tuning, threshold calibration, or architecture exploration may touch this partition.
4. **Independent External Cohort**: When external datasets (e.g., from separate geographic regions or clinical centers) are evaluated, they must remain completely independent.

---

## 3. Mathematical Verification of Zero Leakage

Let $P_{\text{train}}, P_{\text{val}}, P_{\text{test}}$ represent the sets of participant identifiers in the training, validation, and test partitions, respectively. The splitting algorithm must satisfy:

$$P_{\text{train}} \cap P_{\text{val}} = \emptyset$$
$$P_{\text{train}} \cap P_{\text{test}} = \emptyset$$
$$P_{\text{val}} \cap P_{\text{test}} = \emptyset$$

### Automated Leakage Check Algorithm:
```python
def verify_split_integrity(train_manifest, val_manifest, test_manifest):
    train_patients = set(train_manifest["participant_id"].unique())
    val_patients = set(val_manifest["participant_id"].unique())
    test_patients = set(test_manifest["participant_id"].unique())
    
    leakage_train_val = train_patients.intersection(val_patients)
    leakage_train_test = train_patients.intersection(test_patients)
    leakage_val_test = val_patients.intersection(test_patients)
    
    assert len(leakage_train_val) == 0, f"LEAKAGE DETECTED between Train and Val: {len(leakage_train_val)} patients!"
    assert len(leakage_train_test) == 0, f"LEAKAGE DETECTED between Train and Test: {len(leakage_train_test)} patients!"
    assert len(leakage_val_test) == 0, f"LEAKAGE DETECTED between Val and Test: {len(leakage_val_test)} patients!"
```
The automated test suite (`tests/test_patient_grouping.py`) runs this verification before any model checkpointing or evaluation begins.

