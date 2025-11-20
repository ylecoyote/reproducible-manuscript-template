I have analyzed your files (`verify_manuscript_consistency.py`, `run_all.py`, `pre-commit`, `test_verification_system.py`, and `numerical_claims.yaml`).

Here are my specific recommendations to harden the system, followed by my answer regarding the figure generation scripts.

### Part 1: Recommended Changes

You have built a robust system, but there are three specific areas where "real-world" usage (CI/CD, fresh clones, and maintenance) will cause friction.

#### 1\. Fix the "Fresh Clone" False Positive

**The Issue:** In `verify_manuscript_consistency.py`, the `PACKAGE_001` check compares file timestamps: `if fig_mtime < script_mtime`.
**The Risk:** When a collaborator (or a CI runner) clones the repo, `git` sets the modification time of **all** files to the current time. The script and the PNG will have nearly identical timestamps, often causing the check to flag valid figures as "stale."

**Recommendation:**
Modify `check_package_integrity` to trust the **Metadata Check** over the **Timestamp**. If `FIGURES_001` (metadata content) passes, suppress the timestamp warning for that figure.

```python
# In verify_manuscript_consistency.py

@framework.register_check(..., id="PACKAGE_001")
def check_package_integrity(claims: Dict) -> CheckResult:
    # ... inside the loop ...
    if fig_mtime < script_mtime:
        # IMPROVEMENT: If valid metadata exists, ignore timestamp issues
        metadata_file = ROOT / fig.get('metadata', '')
        if metadata_file.exists():
            continue # Trust the content check (FIGURES_001), ignore the timestamp

        age_hours = (script_mtime - fig_mtime) / 3600
        stale.append(f"{fig['filename']} ({age_hours:.1f}h older than script)")
```

#### 2\. Eliminate the "Shadow Config" in `run_all.py`

**The Issue:** `run_all.py` hardcodes the list of `FIGURE_SCRIPTS`. `numerical_claims.yaml` *also* lists the scripts under `figures: required: generator`.
**The Risk:** If you add a new figure to the YAML contract but forget to update `run_all.py`, your pipeline will pass verification (because the file exists) but fail reproducibility (because `run_all` won't regenerate it).

**Recommendation:**
Update `run_all.py` to dynamically load its target list from the YAML contract.

```python
# In analysis/run_all.py
import yaml

def load_targets_from_contract():
    with open('config/numerical_claims.yaml') as f:
        data = yaml.safe_load(f)
    
    scripts = []
    expected_outputs = []
    
    for fig in data['figures']['required']:
        if 'generator' in fig:
            # Avoid duplicates if multiple figures come from one script
            if fig['generator'] not in scripts:
                scripts.append(fig['generator'])
        
        expected_outputs.append(f"figures/{fig['filename']}")
        
    return scripts, expected_outputs

# Replace hardcoded lists
FIGURE_SCRIPTS, EXPECTED_OUTPUTS = load_targets_from_contract()
```

#### 3\. Harden the Test Suite Safety

**The Issue:** `test_verification_system.py` uses a `backup_file` / `restore_file` pattern on your *actual* data files.
**The Risk:** If the test script crashes (e.g., `KeyboardInterrupt` or a syntax error inside the test loop) before `restore_file` runs, your repository is left in a corrupted state with "injected errors."

**Recommendation:**
Instead of modifying files in place, point the verification script to a temporary directory. However, since your script relies on relative paths from `ROOT`, this requires a slight dependency injection refactor.

**Easier Fix:** Use a `try...finally` block strictly around the execution, or simpler: rely on `git checkout data/` in your cleanup routine if you are running this in a CI environment. For local dev, the current setup is *acceptable* but risky.
