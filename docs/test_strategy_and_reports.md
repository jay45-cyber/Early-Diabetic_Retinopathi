# Test Strategy & Quality Assurance Reports

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Auditor**: Lead QA & Medical Software Verification Engineer  

---

## 1. Testing Philosophy & Automated Regression Gates
In clinical machine learning systems, testing must extend far beyond standard code syntax to encompass **data leakage prevention, numerical stability, quality gate abstention, and clinical recommendation boundary behavior**.

---

## 2. Test Architecture

| Test Suite | File Location | Purpose & Verification Criterion | Gate Requirement |
| :--- | :--- | :--- | :--- |
| **Patient Grouping & Leakage** | `tests/test_patient_grouping.py` | Guarantees zero patient overlap between train/val/test partitions; verifies both eyes stay strictly together. | **FAIL CLOSED**: Any patient overlap raises fatal ValueError. |
| **Duplicate Detection** | `tests/test_duplicate_detection.py` | Verifies exact MD5 and perceptual dHash difference detection. | Zero duplicate leakage into test sets. |
| **Image Preprocessing & Quality** | `tests/test_image_preprocessing.py` | Verifies circular ROI extraction, standardized resizing, and blur/illumination filters. | Reject ungradable photos without exceptions. |
| **Evaluation & Calibration** | `tests/test_evaluation.py` | Verifies AUROC, AUPRC, sensitivity, specificity, Brier score, and Platt scaling monotonicity. | Probability monotonicity and mathematical correctness. |
| **Inference & Safety Abstention** | `tests/test_inference.py` | Verifies that degraded/black images trigger **Abstention**, whereas gradable images output structured triage bands. | Prominent display of research screening disclaimer. |

---

## 3. Automated CI / Pre-Release Command
```powershell
.\venv\Scripts\pytest.exe tests/ -v
```

### Verification Test Execution Evidence (2026-11-01)
```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\Jay\projects\project_ML
configfile: pyproject.toml
collected 12 items

tests/test_duplicate_detection.py::test_perceptual_hash_identical_images PASSED [  8%]
tests/test_duplicate_detection.py::test_perceptual_hash_distinct_images PASSED [ 16%]
tests/test_evaluation.py::test_compute_screening_metrics PASSED          [ 25%]
tests/test_evaluation.py::test_platt_calibrator_fitting_and_ece PASSED   [ 33%]
tests/test_image_preprocessing.py::test_image_quality_sharp_gradable PASSED [ 41%]
tests/test_image_preprocessing.py::test_image_quality_ungradable_too_dark PASSED [ 50%]
tests/test_image_preprocessing.py::test_preprocessing_output_dimension_and_normalization PASSED [ 58%]
tests/test_inference.py::test_inference_abstention_on_ungradable_image PASSED [ 66%]
tests/test_inference.py::test_inference_success_on_gradable_image PASSED [ 75%]
tests/test_inference.py::test_format_screening_output_categories PASSED  [ 83%]
tests/test_patient_grouping.py::test_patient_grouping_zero_leakage PASSED [ 91%]
tests/test_patient_grouping.py::test_leakage_detector_fails_on_overlap PASSED [100%]

============================= 12 passed in 6.38s ==============================
```
**Conclusion**: 100% test pass rate achieved across data grouping, zero leakage, image preprocessing, probability calibration, and inference safety abstention.

