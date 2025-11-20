# Changelog

All notable changes to the Reproducible Manuscript Template.

## [2.0.0] - 2025-11-19

### Added - Enhanced Verification Framework

**Major Features:**
- **Category Filtering**: `--only` flag to run specific check categories
- **JSON Output**: `--json` flag for CI/CD integration
- **Enhanced Statistics**: Detailed pass/fail counts by severity level
- **Timing Information**: Execution time tracking
- **INFO Severity**: Three-level system (ERROR/WARNING/INFO)
- **Improved Error Handling**: Better exception catching and reporting
- **Category Grouping**: Results organized by category in output

**New Command-Line Options:**
```bash
python3 verify_manuscript.py --only figures data  # Category filtering
python3 verify_manuscript.py --json               # JSON output
python3 verify_manuscript.py --only figures --json # Combined
```

**Enhanced CheckResult:**
- Added `category` field for grouping
- Added `to_dict()` method for JSON serialization
- Updated all examples to use new signature

**Framework Improvements:**
- `register_check()` now requires `category` parameter
- Better human-readable output formatting
- Separate `report_human()` and `report_json()` methods
- Proper exit codes for CI/CD integration

### Updated

**Core Files:**
- `verify_manuscript.py`: Complete rewrite with 5 new features (380 lines)
- `numerical_claims.yaml`: Fixed `metadata` → `metadata_file` consistency
- `.github/workflows/verify.yml`: Updated to generate both text and JSON outputs

**Documentation:**
- `README.md`: Updated with new command-line examples and enhanced output samples
- `TUTORIAL.md`: Added "Advanced Features" section with examples
- `data/README.md`: Updated check example with new signature
- All code examples updated to use new `@framework.register_check()` signature

**Examples:**
- `scripts/example_analysis.py`: Works with new verification system
- `figures/fig1_example_metadata.json`: Compatible template

### Directory Structure

**Added:**
- `data/` directory with comprehensive README
- `scripts/` directory with example and README
- `figures/` directory with example metadata
- `.github/` templates (issues, PRs, workflows)
- `LICENSE` (MIT)
- `CONTRIBUTING.md`
- `TUTORIAL.md`
- `.gitignore`
- `docs/development/case-study/` (archived original project docs)

**Enhanced:**
- All README files updated with current patterns
- Consistent examples across all documentation

### Breaking Changes

**`register_check()` Signature:**
```python
# Old (v1.x)
@framework.register_check("CHECK_ID", "Name", severity="ERROR")

# New (v2.0)
@framework.register_check(
    id="CHECK_ID",
    name="Name",
    category="category_name",  # Required
    severity="ERROR"
)
```

**CheckResult Constructor:**
```python
# Old (v1.x)
CheckResult("ID", "Name", "ERROR", passed)

# New (v2.0)
CheckResult(
    id="ID",
    name="Name",
    category="category",  # Required
    severity="ERROR",
    passed=passed,
    details="...",
    hint="..."
)
```

### Migration Guide

To upgrade from v1.x to v2.0:

1. **Add `category` to all checks:**
   ```python
   @framework.register_check(
       id="MY_001",
       name="My check",
       category="data",  # Add this
       severity="ERROR"
   )
   ```

2. **Update CheckResult calls:**
   ```python
   return CheckResult(
       id="MY_001",
       name="My check",
       category="data",  # Add this
       severity="ERROR",
       passed=passed,
       details="...",
       hint="..."
   )
   ```

3. **Update YAML if using figure metadata:**
   ```yaml
   # Change this:
   metadata: "figures/fig1_metadata.json"
   # To this:
   metadata_file: "fig1_metadata.json"
   ```

### Compatibility

- **Python**: 3.8+ (tested on 3.11)
- **Dependencies**: `pyyaml`, `pandas` (unchanged)
- **Backward compatibility**: Check signatures must be updated

---

## [1.0.0] - Initial Release

Initial template with basic verification framework.

**Features:**
- Basic decorator-based check registration
- YAML contract definition
- Simple pass/fail reporting
- Pre-commit hook integration
- Two example checks (figures, data)
