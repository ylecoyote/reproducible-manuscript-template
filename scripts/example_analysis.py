#!/usr/bin/env python3
"""
example_analysis.py - Example showing the contract-driven workflow

This script demonstrates:
1. Loading data
2. Performing calculations
3. Generating a figure
4. Outputting metadata for verification
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_example_data():
    """Generate synthetic experiment data"""
    np.random.seed(42)
    n_samples = 100

    # Simulate an experiment with ~85% efficiency
    efficiencies = np.random.normal(0.85, 0.12, n_samples)
    efficiencies = np.clip(efficiencies, 0, 1)  # Keep in [0, 1]

    return efficiencies


def calculate_statistics(data):
    """Calculate key statistics"""
    return {
        "mean_efficiency": float(np.mean(data)),
        "std_dev": float(np.std(data)),
        "sample_size": len(data),
        # Simplified p-value calculation (normally use scipy.stats)
        "p_value": 0.04  # Placeholder for actual statistical test
    }


def create_figure(data, stats):
    """Generate figure showing efficiency distribution"""
    fig, ax = plt.subplots(figsize=(8, 5))

    # Histogram
    ax.hist(data, bins=20, alpha=0.7, color='steelblue', edgecolor='black')

    # Add mean line
    ax.axvline(stats['mean_efficiency'], color='red', linestyle='--',
               linewidth=2, label=f"Mean: {stats['mean_efficiency']:.3f}")

    ax.set_xlabel('Efficiency')
    ax.set_ylabel('Frequency')
    ax.set_title('Experiment A: Efficiency Distribution')
    ax.legend()
    ax.grid(alpha=0.3)

    return fig


def save_metadata(stats, script_name, figure_id):
    """Save metadata for verification"""
    metadata = {
        "figure_id": figure_id,
        "generated_by": script_name,
        "timestamp": datetime.now().isoformat(),
        "key_values": {
            "mean_efficiency": round(stats['mean_efficiency'], 3),
            "p_value": stats['p_value'],
            "sample_size": stats['sample_size']
        }
    }

    metadata_path = OUTPUT_DIR / f"{figure_id}_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    return metadata_path


def main():
    """Main workflow"""
    print("=" * 60)
    print("Example Analysis Script")
    print("=" * 60)

    # 1. Generate/load data
    print("\n1. Generating example data...")
    data = generate_example_data()
    print(f"   ✓ Generated {len(data)} samples")

    # 2. Calculate statistics
    print("\n2. Calculating statistics...")
    stats = calculate_statistics(data)
    print(f"   ✓ Mean efficiency: {stats['mean_efficiency']:.3f}")
    print(f"   ✓ Std deviation: {stats['std_dev']:.3f}")
    print(f"   ✓ P-value: {stats['p_value']:.4f}")

    # 3. Create figure
    print("\n3. Generating figure...")
    fig = create_figure(data, stats)
    figure_path = OUTPUT_DIR / "fig1_example.png"
    fig.savefig(figure_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"   ✓ Saved: {figure_path}")

    # 4. Save metadata for verification
    print("\n4. Saving metadata for verification...")
    metadata_path = save_metadata(stats, "scripts/example_analysis.py", "fig1_example")
    print(f"   ✓ Saved: {metadata_path}")

    # 5. Verification reminder
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Update numerical_claims.yaml with expected values:")
    print("   results:")
    print("     experiment_a:")
    print(f"       mean_efficiency: {stats['mean_efficiency']:.3f}")
    print(f"       p_value: {stats['p_value']:.2f}")
    print("\n2. Run verification:")
    print("   python3 verify_manuscript.py")
    print("\n3. Commit with pre-commit hook enabled:")
    print("   git add .")
    print("   git commit -m 'Add example analysis'")
    print("=" * 60)


if __name__ == "__main__":
    main()
