# Data

This directory contains data files used in your analysis.

## Purpose

Store your raw and processed data files here:

- **Raw data**: Input data from experiments or simulations
- **Processed data**: Cleaned, transformed, or aggregated data
- **Results**: Output from analysis scripts (CSV, JSON, etc.)

## Recommended Structure

```text
data/
├── raw/              # Original, unmodified data
│   └── experiment_a.csv
├── processed/        # Cleaned/transformed data
│   └── experiment_a_cleaned.csv
└── results/          # Analysis outputs
    └── summary_statistics.csv
```

## Data Format Best Practices

### CSV Files

Use CSV for tabular data that will be verified:

```csv
sample_id,efficiency,p_value,timestamp
1,0.85,0.04,2025-01-15
2,0.87,0.03,2025-01-16
```

**Tips:**
- Include headers in the first row
- Use consistent naming conventions
- Document units in column names or metadata
- Use ISO 8601 for dates (`YYYY-MM-DD`)

### JSON Files

Use JSON for hierarchical or metadata:

```json
{
  "experiment": "A",
  "date": "2025-01-15",
  "results": {
    "mean_efficiency": 0.854,
    "p_value": 0.04
  }
}
```

## Version Control Considerations

### Should You Commit Data?

**Commit small data:**
- Summary tables (< 1 MB)
- Aggregated results
- Reference datasets
- Metadata files

**Don't commit large data:**
- Raw experimental outputs (> 10 MB)
- High-resolution images
- Large simulation results

**Alternatives for large data:**
- Use Git LFS (Large File Storage)
- Store on external repositories (Zenodo, OSF, Figshare)
- Document retrieval in `data/DOWNLOAD.md`

## Integration with Verification

The verification script can check data files:

```yaml
# In numerical_claims.yaml
results:
  experiment_a:
    mean_efficiency: 0.854
    source_file: "data/results/experiment_a.csv"
    source_column: "efficiency"
```

Then in `verify_manuscript.py`:

```python
@framework.register_check(
    id="DATA_001",
    name="Verify experiment A results",
    category="data",
    severity="ERROR"
)
def check_experiment_a(claims: Dict) -> CheckResult:
    """Verify CSV data matches contract"""
    df = pd.read_csv(DATA_DIR / "results/experiment_a.csv")
    expected = claims['results']['experiment_a']['mean_efficiency']
    tolerance = claims['tolerances']['absolute']

    actual = df['efficiency'].mean()
    passed = abs(actual - expected) < tolerance

    return CheckResult(
        id="DATA_001",
        name="Experiment A results",
        category="data",
        severity="ERROR",
        passed=passed,
        details=f"Actual: {actual:.3f}, Expected: {expected:.3f}",
        hint="Regenerate data/results/experiment_a.csv" if not passed else ""
    )
```

## See Also

- [Scripts README](../scripts/README.md) - How analysis scripts use data
- [Verification guide](../README.md#-how-to-customize) - Adding data checks
