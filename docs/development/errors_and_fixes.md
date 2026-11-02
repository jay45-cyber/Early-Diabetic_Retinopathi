# Errors & Fixes Log

**Project**: Explainable AI for Early Type 2 Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Last Updated**: 2026-11-02  

---

| Issue ID | Date | Component | Error Description | Root Cause | Resolution | Regression Guard |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-001** | 2026-11-01 | Environment | `git: command not recognized` | Git missing from system PATH. | Installed portable MinGit 2.56.0 in User AppData and updated User PATH. | Automated version check in CI. |
| **ERR-002** | 2026-11-01 | Environment | Python installer exit code 50 | Installer attempted to install shared launcher to Program Files. | Configured `InstallAllUsers=0 Include_launcher=0 TargetDir=...` | Virtualenv validation test. |
| **ERR-003** | 2026-11-01 | Git | Git push hung on credential prompt | Headless shell cannot pop browser OAuth window. | Installed GitHub CLI (`gh`), authenticated via web device flow `1118-398A`. | Git credential helper configured. |
| **ERR-004** | 2026-11-01 | Testing | `ModuleNotFoundError: No module named 'src'` | Pytest did not include current directory in sys.path. | Added `pythonpath = ["."]` to `[tool.pytest.ini_options]` in `pyproject.toml`. | Pytest module discovery test. |
| **ERR-005** | 2026-11-01 | Preprocessing | Tensor dtype mismatch: `float64 != float32` | Array normalization upcast to float64 due to float tuple operations. | Explicitly appended `.astype(np.float32)` in `normalize_to_tensor`. | `test_preprocessing_output_dimension_and_normalization`. |

