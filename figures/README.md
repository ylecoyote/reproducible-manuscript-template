# Figures

This directory contains generated figures and their metadata.

## Purpose

Store publication-ready figures here along with metadata files that document the key numerical values displayed in each figure.

## Metadata Pattern

For each figure that displays numerical results, create a corresponding JSON metadata file:

```text
figures/
├── fig1_efficiency.png          # The actual figure
├── fig1_efficiency_metadata.json # Key values for verification
├── fig2_comparison.png
└── fig2_comparison_metadata.json
```

## Metadata Format

**Example: `fig1_efficiency_metadata.json`**

```json
{
  "figure_id": "fig1_efficiency",
  "generated_by": "scripts/generate_results.py",
  "timestamp": "2025-11-19T14:30:00",
  "key_values": {
    "mean_efficiency": 0.854,
    "p_value": 0.04,
    "sample_size": 100
  }
}
```

## Why Metadata?

The verification system **cannot reliably extract numbers from PNG/PDF files**. Instead:

1. Your script generates the figure
2. Your script also saves the key values to a JSON file
3. The verifier compares JSON values against the contract (`numerical_claims.yaml`)

This prevents the "stale figure" problem: if you update your analysis but forget to regenerate figures, the metadata will be outdated and verification will fail.

## Automatic Generation

Have your plotting scripts automatically output metadata:

```python
# At the end of your plotting script
import json
from datetime import datetime

metadata = {
    "figure_id": "fig1_efficiency",
    "generated_by": __file__,
    "timestamp": datetime.now().isoformat(),
    "key_values": {
        "mean_efficiency": float(mean_eff),  # Ensure JSON-serializable
        "p_value": float(p_val)
    }
}

with open("figures/fig1_efficiency_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)
```

## .gitignore Note

You may want to add `*_metadata.json` to `.gitignore` if these are regenerated frequently. However, committing them can help track when figures were last updated.

## See Also

- [Example metadata](fig1_example_metadata.json) - Template to copy
- [Scripts README](../scripts/README.md) - How to generate metadata from scripts
