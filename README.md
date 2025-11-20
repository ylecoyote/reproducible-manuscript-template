# Reproducible Manuscript Template 🛡️

> **"Unit Testing for Science"**

[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem
In scientific publishing, there is a dangerous gap between your **Code** (analysis scripts) and your **Text** (manuscript/README).

1. You run an analysis and get `efficiency = 82.5%`.
2. You write "We achieved 82.5% efficiency" in your LaTeX/Markdown manuscript.
3. You improve the code, and the result changes to `84.1%`.
4. **You forget to update the text.**
5. *Result:* Internal inconsistency, reviewer confusion, or retraction.

## The Solution
This repository treats your manuscript like software. It enforces a **Contract** between your data and your text.

* **Single Source of Truth:** All numbers live in `numerical_claims.yaml`.
* **Automated Verification:** A script checks your data/figures against the contract.
* **Continuous Integration:** `git commit` is blocked if the numbers don't match.

---

## 🚀 Quick Start

**New to this?** See the [complete tutorial](TUTORIAL.md) for a step-by-step walkthrough with examples.

### 1. Install Dependencies
You need Python 3 and `pre-commit`.

```bash
pip install pyyaml pandas pre-commit
pre-commit install
```

### 2. Define Your Contract

Edit `numerical_claims.yaml`. This is where you state the results you expect to see in your paper.

```yaml
results:
  experiment_a:
    mean_efficiency: 0.854
    p_value: 0.04
```

### 3. Run the Verification

Run the script manually to check the status of your repository:

```bash
python3 verify_manuscript.py
```

**Success Output:**

```text
================================================================================
MANUSCRIPT VERIFICATION REPORT
================================================================================

Repository: /path/to/your/project
Checks run: 2
Time: 0.01s

✅ ALL CHECKS PASSED

   Passed:   2/2

Category: data
  ✅ [DAT_001] Experiment A mean efficiency

Category: figures
  ✅ [FIG_001] Figure package integrity

================================================================================
✨ SUCCESS: Manuscript is consistent.
================================================================================
```

**Failure Output (The Safety Net):**

```text
================================================================================
MANUSCRIPT VERIFICATION REPORT
================================================================================

Repository: /path/to/your/project
Checks run: 2
Time: 0.01s

❌ VERIFICATION FAILED

   Passed:   1/2
   Errors:   1

Category: data
  ❌ [DAT_001] Experiment A mean efficiency
     Details: Calculated 0.821, Expected 0.854 (diff 0.0330)
     Hint: Update numerical_claims.yaml or regenerate data

Category: figures
  ✅ [FIG_001] Figure package integrity

================================================================================
⛔ FAILED: Critical inconsistencies detected.
================================================================================
```

**Advanced Options:**

```bash
# Output JSON for CI/CD integration
python3 verify_manuscript.py --json

# Run only specific categories
python3 verify_manuscript.py --only figures data

# Combine flags
python3 verify_manuscript.py --only figures --json
```

-----

## 📂 Repository Structure

```text
.
├── numerical_claims.yaml   # The Contract (Single Source of Truth)
├── verify_manuscript.py    # The Enforcer (Verification Script)
├── .pre-commit-config.yaml # The Automation (Git Hook)
├── data/                   # Data files (raw, processed, results)
├── scripts/                # Analysis code
├── figures/                # Plots + JSON metadata
└── docs/                   # Documentation
    ├── index.md            # Project manifesto (GitHub Pages)
    └── development/        # Design docs (for contributors)
```

  * `numerical_claims.yaml`: **The Brain.** The single source of truth for all numbers.
  * `verify_manuscript.py`: **The Enforcer.** Generic framework that validates artifacts against the YAML.
  * `data/`: Raw and processed data files (CSV, JSON, etc.).
  * `scripts/`: Your analysis code. (Should output data/figures).
  * `figures/`: Generated plots.
      * *Best Practice:* Have your scripts output a sidecar JSON file (e.g., `fig1.json`) containing the raw numbers plotted. The verifier checks this metadata.

## 🛡️ How to Customize

### Adding a New Check

Open `verify_manuscript.py` and add a function with the `@framework.register_check` decorator:

```python
@framework.register_check(
    id="MY_CHECK_001",
    name="P-value threshold check",
    category="statistics",
    severity="ERROR"  # or "WARNING" or "INFO"
)
def check_p_values(claims: Dict) -> CheckResult:
    """Verify p-values meet significance threshold"""
    # 1. Load your data
    df = pd.read_csv(DATA_DIR / "results.csv")

    # 2. Get expected value from YAML
    expected = claims['results']['experiment_a']['p_value']
    threshold = claims['tolerances'].get('p_value', 0.05)

    # 3. Calculate actual value
    actual_p = df['p_value'].min()

    # 4. Compare
    passed = actual_p < threshold

    # 5. Return result
    return CheckResult(
        id="MY_CHECK_001",
        name="P-value threshold check",
        category="statistics",
        severity="ERROR",
        passed=passed,
        details=f"Min p-value: {actual_p:.4f}, Threshold: {threshold:.4f}",
        hint="Review statistical analysis" if not passed else ""
    )
```

**Categories**: Group related checks (e.g., `"data"`, `"figures"`, `"statistics"`, `"results"`). This allows selective testing with `--only category`.

**Severity Levels**:
- `ERROR`: Critical issues that block manuscript submission
- `WARNING`: Issues that should be fixed but don't block submission
- `INFO`: Advisory notices (don't cause verification to fail)

## 🤝 Contributing

Fork this template to create your own reproducible research repository. If you find a bug in the verification framework, pull requests are welcome.

**For contributors**: See [docs/development/](docs/development/) for design rationale and architecture documentation.

## License

MIT