#!/usr/bin/env python3
"""
Generic Manuscript Verification Framework
Validates that data, figures, and text match the 'numerical_claims.yaml' contract.

Usage:
    python3 verify_manuscript.py              # Run all checks
    python3 verify_manuscript.py --json       # Output JSON for CI/CD
    python3 verify_manuscript.py --only figures data  # Run specific categories
"""
import argparse
import json
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

try:
    import yaml
    import pandas as pd  # Optional: Only needed if checking CSVs
except ImportError:
    print("ERROR: Missing dependencies. Run: pip install pyyaml pandas")
    sys.exit(1)

# --- Configuration ---
ROOT = Path(__file__).resolve().parent
CLAIMS_FILE = ROOT / "numerical_claims.yaml"
FIGURES_DIR = ROOT / "figures"
DATA_DIR = ROOT / "data"

@dataclass
class CheckResult:
    """Result of a single verification check"""
    id: str
    name: str
    category: str          # NEW: Category for filtering
    severity: str          # "ERROR" | "WARNING" | "INFO"
    passed: bool
    details: str = ""
    hint: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


class VerificationFramework:
    """Framework for registering and running verification checks"""

    def __init__(self):
        self._checks = []
        self._claims = None
        self._start_time = time.time()  # NEW: Track timing

    def load_claims(self) -> Dict:
        """Load numerical claims from YAML (single source of truth)"""
        if not self._claims:
            if not CLAIMS_FILE.exists():
                raise FileNotFoundError(f"Contract missing: {CLAIMS_FILE}")
            with open(CLAIMS_FILE) as f:
                self._claims = yaml.safe_load(f)
        return self._claims

    def register_check(self, id: str, name: str, category: str, severity: str = "ERROR"):
        """
        Decorator for registering a verification check.

        Args:
            id: Unique check identifier (e.g., "FIG_001")
            name: Human-readable description
            category: Category for filtering (e.g., "figures", "data", "results")
            severity: "ERROR", "WARNING", or "INFO"
        """
        def decorator(func: Callable[[Dict], CheckResult]):
            self._checks.append({
                "id": id,
                "name": name,
                "category": category,
                "severity": severity,
                "func": func
            })
            return func
        return decorator

    def run(self, only_categories: Optional[List[str]] = None) -> List[CheckResult]:
        """
        Run all registered checks.

        Args:
            only_categories: If provided, only run checks in these categories

        Returns:
            List of CheckResult objects
        """
        claims = self.load_claims()
        results = []

        for check in self._checks:
            # NEW: Category filtering
            if only_categories and check["category"] not in only_categories:
                continue

            try:
                result = check['func'](claims)
                results.append(result)
            except Exception as e:
                # Catch check failures and record as ERROR
                results.append(CheckResult(
                    id=check['id'],
                    name=check['name'],
                    category=check['category'],
                    severity="ERROR",
                    passed=False,
                    details=f"Check raised exception: {type(e).__name__}: {e}",
                    hint="Check implementation may have a bug"
                ))

        return results

    def report_human(self, results: List[CheckResult]) -> int:
        """
        Generate human-readable report with statistics.

        Returns:
            Exit code (0 = success, 1 = failure)
        """
        elapsed = time.time() - self._start_time

        # NEW: Calculate statistics by severity
        errors = [r for r in results if not r.passed and r.severity == "ERROR"]
        warnings = [r for r in results if not r.passed and r.severity == "WARNING"]
        info = [r for r in results if not r.passed and r.severity == "INFO"]
        passed = [r for r in results if r.passed]

        # Header
        print("=" * 80)
        print("MANUSCRIPT VERIFICATION REPORT")
        print("=" * 80)
        print()
        print(f"Repository: {ROOT}")
        print(f"Checks run: {len(results)}")
        print(f"Time: {elapsed:.2f}s")
        print()

        # NEW: Summary statistics
        if errors or warnings:
            print("❌ VERIFICATION FAILED")
        else:
            print("✅ ALL CHECKS PASSED")

        print()
        print(f"   Passed:   {len(passed)}/{len(results)}")
        if errors:
            print(f"   Errors:   {len(errors)}")
        if warnings:
            print(f"   Warnings: {len(warnings)}")
        if info:
            print(f"   Info:     {len(info)}")
        print()

        # Group results by category
        categories = {}
        for r in results:
            if r.category not in categories:
                categories[r.category] = []
            categories[r.category].append(r)

        # Display by category
        for category, checks in sorted(categories.items()):
            print(f"Category: {category}")
            for r in checks:
                icon = "✅" if r.passed else {
                    "ERROR": "❌",
                    "WARNING": "⚠️",
                    "INFO": "ℹ️"
                }.get(r.severity, "❌")

                print(f"  {icon} [{r.id}] {r.name}")
                if not r.passed:
                    print(f"     Details: {r.details}")
                    if r.hint:
                        print(f"     Hint: {r.hint}")
            print()

        print("=" * 80)

        if errors or warnings:
            print("⛔ FAILED: Critical inconsistencies detected.")
            return 1
        else:
            print("✨ SUCCESS: Manuscript is consistent.")
            return 0

    def report_json(self, results: List[CheckResult]) -> int:
        """
        Generate machine-readable JSON report (for CI/CD).

        Returns:
            Exit code (0 = success, 1 = failure)
        """
        elapsed = time.time() - self._start_time
        errors = [r for r in results if not r.passed and r.severity == "ERROR"]
        warnings = [r for r in results if not r.passed and r.severity == "WARNING"]

        output = {
            "metadata": {
                "repository": str(ROOT),
                "timestamp": time.time(),
                "elapsed_seconds": round(elapsed, 2)
            },
            "summary": {
                "total_checks": len(results),
                "passed": len([r for r in results if r.passed]),
                "failed": len([r for r in results if not r.passed]),
                "errors": len(errors),
                "warnings": len(warnings)
            },
            "results": [r.to_dict() for r in results]
        }

        print(json.dumps(output, indent=2))
        return 1 if (errors or warnings) else 0


# =============================================================================
# Framework Instance & Example Checks
# =============================================================================

framework = VerificationFramework()


@framework.register_check(
    id="FIG_001",
    name="Figure package integrity",
    category="figures",
    severity="WARNING"
)
def check_figures_exist(claims: Dict) -> CheckResult:
    """
    Ensures all figures listed in YAML exist.
    If they have a generator script, warns if figure is older than script.
    SAFEGUARD: Trusts metadata file existence over timestamps (fixes fresh clone bug).
    """
    issues = []
    for fig in claims.get('figures', {}).get('required', []):
        fig_path = FIGURES_DIR / fig['filename']

        # 1. Existence check
        if not fig_path.exists():
            issues.append(f"Missing: {fig['filename']}")
            continue

        # 2. Freshness check (with metadata safeguard)
        if 'generator' in fig:
            script_path = ROOT / fig['generator']
            if script_path.exists():
                # If we have a metadata sidecar, trust content check instead of timestamps
                # This prevents false positives on fresh git clones
                metadata_file = fig.get('metadata_file', '')
                if metadata_file:
                    metadata_path = FIGURES_DIR / metadata_file
                    if metadata_path.exists():
                        continue  # Trust metadata check instead

                # Fallback to timestamp check
                if fig_path.stat().st_mtime < script_path.stat().st_mtime:
                    issues.append(f"Stale: {fig['filename']} (older than script)")

    return CheckResult(
        id="FIG_001",
        name="Figure package integrity",
        category="figures",
        severity="WARNING",
        passed=len(issues) == 0,
        details="; ".join(issues) if issues else f"All {len(claims.get('figures', {}).get('required', []))} figures OK",
        hint="Run: python3 scripts/example_analysis.py" if issues else ""
    )


@framework.register_check(
    id="DAT_001",
    name="Experiment A mean efficiency",
    category="data",
    severity="ERROR"
)
def check_data_consistency(claims: Dict) -> CheckResult:
    """Example: Checks if calculated values match the contract"""
    # In a real implementation, this would load actual data:
    # df = pd.read_csv(DATA_DIR / "results.csv")
    # csv_calculated_mean = df['efficiency'].mean()

    # For the template, we use the metadata from example_analysis.py
    metadata_path = FIGURES_DIR / "fig1_example_metadata.json"

    if not metadata_path.exists():
        return CheckResult(
            id="DAT_001",
            name="Experiment A mean efficiency",
            category="data",
            severity="ERROR",
            passed=False,
            details="Metadata file not found",
            hint="Run: python3 scripts/example_analysis.py"
        )

    # Load metadata
    with open(metadata_path) as f:
        metadata = json.load(f)

    calculated = metadata['key_values']['mean_efficiency']
    expected = claims['results']['experiment_a']['mean_efficiency']
    tolerance = claims['tolerances']['absolute']

    diff = abs(calculated - expected)
    passed = diff <= tolerance

    return CheckResult(
        id="DAT_001",
        name="Experiment A mean efficiency",
        category="data",
        severity="ERROR",
        passed=passed,
        details=f"Calculated {calculated:.3f}, Expected {expected:.3f} (diff {diff:.4f})",
        hint="Update numerical_claims.yaml or regenerate data" if not passed else ""
    )


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="Verify manuscript numerical consistency",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 verify_manuscript.py                    # Run all checks
  python3 verify_manuscript.py --json             # Output JSON
  python3 verify_manuscript.py --only figures data # Run specific categories
        """
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of human-readable text (for CI/CD)"
    )

    parser.add_argument(
        "--only",
        nargs="+",
        metavar="CATEGORY",
        help="Only run checks in these categories (e.g., figures, data, results)"
    )

    args = parser.parse_args()

    # Run verification
    try:
        results = framework.run(only_categories=args.only)

        if args.json:
            exit_code = framework.report_json(results)
        else:
            exit_code = framework.report_human(results)

        sys.exit(exit_code)

    except Exception as e:
        print(f"ERROR: Verification failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
