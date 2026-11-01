# Errors & Resolutions Log

**Project Identity**: Explainable AI for Early Diabetes Risk Screening Using Retinal Fundus Images in Rural India  
**Last Updated**: 2026-11-01  

---

## Logged Issues & Fixes

### ERR-001: Git Command Not Recognized
- **Date**: 2026-11-01
- **Severity**: Blocker
- **Symptoms**: `git : The term 'git' is not recognized as the name of a cmdlet, function, script file, or operable program.`
- **Root Cause**: Git was not pre-installed on the host operating system, and system-level winget installation failed due to UAC elevation requirements.
- **Resolution**: Downloaded official 64-bit MinGit archive (`v2.56.0`), extracted to `C:\Users\Jay\AppData\Local\Programs\Git`, and configured in user environment `PATH`.
- **Regression Guard**: Verified via `git --version` in child processes.

### ERR-002: Python Installer Exit Code 50
- **Date**: 2026-11-01
- **Severity**: Blocker
- **Symptoms**: Winget Python 3.11 installation failed with `exit code: 50`.
- **Root Cause**: The default Python bootstrapper attempted to install the shared Py launcher to `C:\Program Files`, which requires local Administrator privileges.
- **Resolution**: Executed the installer with non-elevated parameters: `/quiet InstallAllUsers=0 Include_launcher=0 PrependPath=1 TargetDir=C:\Users\Jay\AppData\Local\Programs\Python\Python311`.
- **Regression Guard**: Virtual environment created and verified with `.\venv\Scripts\python.exe --version`.

### ERR-003: Headless Git Push Authentication Hang
- **Date**: 2026-11-01
- **Severity**: Blocker
- **Symptoms**: `git push -u origin main` hung indefinitely in background execution without output.
- **Root Cause**: GitHub deprecated password authentication; `git push` over HTTPS prompted interactively for credentials, which cannot render in a headless shell.
- **Resolution**: Installed GitHub CLI via winget, initiated device flow authentication (`gh auth login --web`), presented one-time device code `1118-398A` for user web approval, configured git credentials (`gh auth setup-git`), and successfully pushed.
- **Regression Guard**: Future pushes use the configured credential helper automatically.

