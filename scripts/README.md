# Analysis Scripts

This directory contains your analysis code that generates data and figures.

## Purpose

Put your data analysis, plotting, and computation scripts here. These scripts should:

1. **Read raw data** from input files
2. **Perform calculations** and generate results
3. **Output structured data** (CSV, JSON) that can be verified
4. **Generate figures** with accompanying metadata files

## Best Practices

### Output Metadata

When generating figures, also output a JSON file with the key numerical values:

```python
import json

# After generating your plot
metadata = {
    "figure_id": "fig1",
    "key_values": {
        "mean_efficiency": calculated_efficiency,
        "p_value": p_value
    }
}

with open("../figures/fig1_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)
```

This allows the verification script to check the actual values used in the figure.

### Example Script Structure

```python
#!/usr/bin/env python3
"""
generate_results.py - Example analysis script
"""
import pandas as pd
import matplotlib.pyplot as plt
import json

# 1. Load data
df = pd.read_csv("../data/experiment_a.csv")

# 2. Calculate results
mean_efficiency = df['efficiency'].mean()
p_value = calculate_p_value(df)  # Your statistical test

# 3. Generate figure
plt.figure()
plt.plot(df['time'], df['efficiency'])
plt.savefig("../figures/fig1_efficiency.png")

# 4. Save metadata for verification
metadata = {
    "figure_id": "fig1_efficiency",
    "generated_by": "generate_results.py",
    "key_values": {
        "mean_efficiency": round(mean_efficiency, 3),
        "p_value": round(p_value, 4)
    }
}

with open("../figures/fig1_efficiency_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"✓ Generated fig1_efficiency.png")
print(f"✓ Mean efficiency: {mean_efficiency:.3f}")
print(f"✓ P-value: {p_value:.4f}")
```

## Integration with Verification

The [verify_manuscript.py](../verify_manuscript.py) script will:

1. Load expected values from [numerical_claims.yaml](../numerical_claims.yaml)
2. Compare them against your output data (CSV files, JSON metadata)
3. Check that figures are newer than their generator scripts
4. Report any mismatches

## See Also

- [Example script](example_analysis.py) - Working example showing the pattern
- [How to Customize](../README.md#-how-to-customize) - Adding custom verification checks
