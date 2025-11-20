# Tutorial: Complete End-to-End Workflow

This tutorial walks through the complete reproducible manuscript workflow using a simple example.

## Scenario

You're analyzing an experiment measuring efficiency across 100 samples. You want to ensure your manuscript, figures, and data stay consistent as you iterate on the analysis.

## Step 1: Install Dependencies

```bash
pip install pyyaml pandas pre-commit matplotlib
pre-commit install
```

## Step 2: Run the Example Analysis

Run the provided example script to generate data and figures:

```bash
python3 scripts/example_analysis.py
```

**Output:**
```
============================================================
Example Analysis Script
============================================================

1. Generating example data...
   ✓ Generated 100 samples

2. Calculating statistics...
   ✓ Mean efficiency: 0.854
   ✓ Std deviation: 0.119
   ✓ P-value: 0.0400

3. Generating figure...
   ✓ Saved: figures/fig1_example.png

4. Saving metadata for verification...
   ✓ Saved: figures/fig1_example_metadata.json
============================================================
```

**Check what was created:**

```bash
ls figures/
# fig1_example.png
# fig1_example_metadata.json
```

## Step 3: Define Your Contract

Edit `numerical_claims.yaml` to define what values you expect:

```yaml
metadata:
  version: "1.0"
  last_updated: "2025-11-19"

tolerances:
  efficiency: 0.01
  p_value: 0.01

results:
  experiment_a:
    mean_efficiency: 0.854
    p_value: 0.04
    sample_size: 100

figures:
  required:
    - filename: "fig1_example.png"
      generator: "scripts/example_analysis.py"
      metadata_file: "fig1_example_metadata.json"
```

## Step 4: Add a Verification Check

Add a check to `verify_manuscript.py` that validates your results:

```python
@framework.register_check(
    id="EXAMPLE_001",
    name="Verify example experiment efficiency",
    category="results",
    severity="ERROR"
)
def check_example_efficiency(claims: Dict) -> CheckResult:
    """Verify that figure metadata matches contract"""
    import json
    from pathlib import Path

    # Load expected values from contract
    expected_eff = claims['results']['experiment_a']['mean_efficiency']
    tolerance = claims['tolerances']['efficiency']

    # Load actual values from figure metadata
    metadata_path = Path("figures/fig1_example_metadata.json")
    if not metadata_path.exists():
        return CheckResult(
            "EXAMPLE_001",
            "Example efficiency check",
            "results",
            "ERROR",
            False,
            "Metadata file not found",
            "Run: python3 scripts/example_analysis.py"
        )

    with open(metadata_path) as f:
        metadata = json.load(f)

    actual_eff = metadata['key_values']['mean_efficiency']

    # Compare
    passed = abs(actual_eff - expected_eff) < tolerance

    details = f"Expected: {expected_eff}, Actual: {actual_eff}, Diff: {abs(actual_eff - expected_eff):.4f}"

    return CheckResult(
        "EXAMPLE_001",
        "Example efficiency check",
        "results",
        "ERROR",
        passed,
        details,
        "Update numerical_claims.yaml or regenerate data" if not passed else ""
    )
```

## Step 5: Run Verification

```bash
python3 verify_manuscript.py
```

**Expected output:**

```
================================================================================
MANUSCRIPT CONSISTENCY VERIFICATION REPORT
================================================================================

Checks run: 1
Time: 0.01s

✅ ALL CHECKS PASSED

Category: results
  ✅ [EXAMPLE_001] Verify example experiment efficiency

================================================================================
✨ SUCCESS: Manuscript is consistent and ready for submission.
================================================================================
```

## Step 6: Test the Safety Net

Let's intentionally introduce an error to see the system catch it.

**Modify the contract** (introduce wrong value):

```yaml
results:
  experiment_a:
    mean_efficiency: 0.900  # ← Wrong! Should be 0.854
```

**Run verification again:**

```bash
python3 verify_manuscript.py
```

**Output:**

```
================================================================================
MANUSCRIPT CONSISTENCY VERIFICATION REPORT
================================================================================

Checks run: 1
Time: 0.01s

❌ VERIFICATION FAILED

Category: results
  ❌ [EXAMPLE_001] Verify example experiment efficiency
     Details: Expected: 0.900, Actual: 0.854, Diff: 0.0460
     Hint: Update numerical_claims.yaml or regenerate data

================================================================================
⛔ FAILED: Critical inconsistencies detected.
================================================================================
```

**Fix it back:**

```yaml
results:
  experiment_a:
    mean_efficiency: 0.854  # ← Correct
```

## Step 7: Enable Pre-Commit Hook

The pre-commit hook automatically runs verification before each commit.

**Try committing with an error:**

```bash
# Introduce error again
echo "mean_efficiency: 0.900" >> numerical_claims.yaml

# Try to commit
git add .
git commit -m "Test commit with error"
```

**Output:**

```
Manuscript Verification...........................Failed
- hook id: verify-manuscript
- exit code: 1

❌ VERIFICATION FAILED
[... error details ...]

⛔ Commit blocked due to verification failures.
```

**Fix and retry:**

```bash
# Fix the error
git checkout numerical_claims.yaml

# Commit successfully
git add .
git commit -m "Add verified results"
```

```
Manuscript Verification...........................Passed
[main abc1234] Add verified results
```

## Step 8: Update Your Analysis

Let's simulate updating the analysis code:

**Modify `scripts/example_analysis.py`** (change line 17):

```python
# Old: efficiencies = np.random.normal(0.85, 0.12, n_samples)
efficiencies = np.random.normal(0.87, 0.12, n_samples)  # New mean!
```

**Regenerate:**

```bash
python3 scripts/example_analysis.py
```

**Run verification:**

```bash
python3 verify_manuscript.py
```

**Output:**

```
❌ VERIFICATION FAILED
Details: Expected: 0.854, Actual: 0.870, Diff: 0.0160
```

**Update the contract:**

```yaml
results:
  experiment_a:
    mean_efficiency: 0.870  # ← Updated to match new analysis
```

**Verify again:**

```bash
python3 verify_manuscript.py
# ✅ ALL CHECKS PASSED
```

## Step 9: The Complete Workflow

**The verified workflow becomes:**

1. **Update analysis code** → Run script → Generates data + metadata
2. **Update contract** → Reflect new expected values
3. **Run verification** → Ensures consistency
4. **Commit** → Pre-commit hook verifies automatically
5. **Submit manuscript** → Confidence that numbers match!

## Common Patterns

### Adding Multiple Experiments

```yaml
results:
  experiment_a:
    mean_efficiency: 0.854
  experiment_b:
    mean_efficiency: 0.912
  experiment_c:
    mean_efficiency: 0.788
```

### Checking CSV Files Directly

```python
@framework.register_check(
    id="DATA_001",
    name="Check raw CSV data",
    category="data",
    severity="ERROR"
)
def check_csv_data(claims: Dict) -> CheckResult:
    """Verify CSV data matches contract"""
    df = pd.read_csv(DATA_DIR / "results.csv")
    expected = claims['results']['experiment_a']['mean_efficiency']
    tolerance = claims['tolerances']['absolute']

    actual = df['efficiency'].mean()
    passed = abs(actual - expected) < tolerance

    return CheckResult(
        id="DATA_001",
        name="Check raw CSV data",
        category="data",
        severity="ERROR",
        passed=passed,
        details=f"CSV mean: {actual:.3f}, Expected: {expected:.3f}",
        hint="Regenerate CSV data" if not passed else ""
    )
```

### Tolerance Management

```yaml
tolerances:
  efficiency: 0.01      # ±1%
  p_value: 0.001        # ±0.1%
  ratio: 0.05           # ±5%
  temperature: 0.1      # ±0.1K
```

### Advanced Features

**Category Filtering** - Test only specific parts during development:

```bash
# Only check figures
python3 verify_manuscript.py --only figures

# Check multiple categories
python3 verify_manuscript.py --only data figures

# Useful when iterating on specific analyses
python3 verify_manuscript.py --only statistics
```

**JSON Output** - For CI/CD integration:

```bash
# Output JSON for GitHub Actions
python3 verify_manuscript.py --json > results.json

# Combine with category filtering
python3 verify_manuscript.py --only figures --json
```

**Severity Levels** - Control what blocks submission:

```python
# ERROR: Blocks submission (exit code 1)
severity="ERROR"

# WARNING: Should fix, but doesn't block (exit code 1)
severity="WARNING"

# INFO: Advisory only, doesn't fail (exit code 0)
severity="INFO"
```

## Next Steps

- Read [How to Customize](README.md#-how-to-customize) for advanced checks
- See [docs/development/](docs/development/) for design rationale
- Adapt to your domain (replace efficiency with your metrics)

---

**You now have a fully verified manuscript workflow!** Any time you change analysis code, figures, or claims, the verification system ensures everything stays in sync.
