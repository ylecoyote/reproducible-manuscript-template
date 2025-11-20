# Version Management System

**Status:** v8.7 (2025-11-19)
**Single Source of Truth:** `config/numerical_claims.yaml`

## Overview

This project uses a **YAML-first versioning system** where all version information originates from a single source of truth: [`config/numerical_claims.yaml`](../config/numerical_claims.yaml). This ensures consistency across code, documentation, and build artifacts.

## Version Structure

**Format:** `MAJOR.MINOR[LETTER]`

- **Major (8.x)**: Manuscript generation/submission cycle
- **Minor (x.7)**: Significant infrastructure, new analyses, major revisions
- **Letter (xA-Z)**: Iterative corrections, minor updates, expert feedback responses

**Examples:**
- `8.7` = Infrastructure milestone (JSON metadata pipeline)
- `8.6H` = 8th expert feedback iteration on version 8.6
- `9.0` = New submission (different journal or complete rewrite)

## Single Source of Truth

### config/numerical_claims.yaml

All version information lives here:

```yaml
metadata:
  version: "8.7"
  last_updated: "2025-11-19"
  manuscript_hash: ""  # Set at git tag
  description: "Numerical claims registry"

version_history:
  - version: "8.7"
    date: "2025-11-19"
    description: "Complete JSON metadata pipeline"
    changes:
      - "Added JSON metadata sidecars for all 9 figures"
      - "YAML-first verification architecture validated"
      - "End-to-end reproducibility pipeline operational"
    significance: "Infrastructure milestone"
    commit: ""  # Filled at git tag
```

**This is the ONLY place where version should be manually updated.**

## Automatic Version Propagation

### 1. Overleaf Package (`scripts/prepare_overleaf_updated.sh`)

Reads version dynamically:

```bash
VERSION=$(python3 -c "import yaml; data = yaml.safe_load(open('config/numerical_claims.yaml')); print(data['metadata']['version'])")
OUTPUT_ZIP="manuscript_overleaf_v${VERSION}.zip"
```

✅ **No manual updates needed**

### 2. Pre-Commit Hook (`.git/hooks/pre-commit`)

Displays current version and reminds about version bumps when >5 significant files change:

```
💡 Version Check
   Detected 12 significant file changes
   Current version: v8.7

   Consider version bump if this represents:
     • New analysis results
     • Infrastructure changes
     • Manuscript submission/revision
```

✅ **No manual updates needed**

### 3. Verification System (`analysis/verify_manuscript_consistency.py`)

Reads version from YAML for reporting:

```python
import yaml
config = yaml.safe_load(open('config/numerical_claims.yaml'))
print(f"Claims version: {config['metadata']['version']}")
```

✅ **No manual updates needed**

## How to Update Version

### Step 1: Edit YAML (Only Manual Step)

Edit `config/numerical_claims.yaml`:

```yaml
metadata:
  version: "8.8"  # Increment
  last_updated: "2025-11-XX"

version_history:
  - version: "8.8"  # Add new entry at top
    date: "2025-11-XX"
    description: "Brief description"
    changes:
      - "Change 1"
      - "Change 2"
    significance: "Major/Minor/Patch"
    commit: ""  # Leave blank
```

### Step 2: Commit Changes

```bash
git add config/numerical_claims.yaml
git commit -m "Bump version to v8.8"
```

### Step 3: Create Git Tag

```bash
git tag -a v8.8 -m "Version 8.8: <description>"
git push origin v8.8
```

### Step 4: Update Commit Hash in YAML

```bash
COMMIT_HASH=$(git rev-parse HEAD)
# Update commit field in YAML version_history for v8.8
git add config/numerical_claims.yaml
git commit --amend --no-edit
git tag -f v8.8 -m "Version 8.8: <description>"
git push origin v8.8 --force
```

## Version Decision Tree

```
Is this a new submission to a different journal?
├─ YES → Bump MAJOR (8.x → 9.0)
└─ NO → Continue...

Does it include new analyses, infrastructure, or major manuscript changes?
├─ YES → Bump MINOR (8.6 → 8.7)
└─ NO → Continue...

Is it iterative corrections/expert feedback?
├─ YES → Add LETTER (8.7 → 8.7A)
└─ NO → No version bump needed
```

## Verification

All scripts that need version info should **read from YAML**:

```python
# ✅ CORRECT
import yaml
config = yaml.safe_load(open('config/numerical_claims.yaml'))
version = config['metadata']['version']

# ❌ WRONG - Don't hardcode!
version = "8.7"
```

```bash
# ✅ CORRECT
VERSION=$(python3 -c "import yaml; print(yaml.safe_load(open('config/numerical_claims.yaml'))['metadata']['version'])")

# ❌ WRONG - Don't hardcode!
VERSION="8.7"
```

## Finding Hardcoded Versions

Run this command to find any remaining hardcoded version references:

```bash
# Search for version patterns (excluding historical docs)
grep -r "v8\." --include="*.py" --include="*.sh" --include="*.md" . \
    | grep -v ".git" \
    | grep -v "_tmp/" \
    | grep -v "figures/" \
    | grep -v "docs/development"  # Historical records OK
```

Expected results:
- `config/numerical_claims.yaml` - ✅ Single source of truth
- Historical docs in `docs/development/` - ✅ OK (these are records)
- Everything else - ❌ Should read from YAML

## Integration with Git

### Tags

Git tags mark version milestones:

```bash
git tag -l "v*"
# v8.6H
# v8.7
```

### Commit Messages

Use version in commit messages when appropriate:

```bash
git commit -m "Bump version to v8.7

- Complete JSON metadata pipeline
- YAML-first verification validated
- End-to-end reproducibility achieved"
```

### Branches (Optional)

For major work, consider version branches:

```bash
git checkout -b v8.7-dev
# ... work ...
git checkout main
git merge v8.7-dev
git tag v8.7
```

## Best Practices

### DO ✅

- **Update YAML first** before any other version-related changes
- **Create git tags** for all version milestones
- **Read version dynamically** in all scripts
- **Document changes** in version_history
- **Use semantic versioning** (major.minor[letter])

### DON'T ❌

- **Hardcode versions** in scripts or documentation
- **Skip version_history updates** when bumping version
- **Forget to create git tags** for milestones
- **Bump version** for trivial commits
- **Use arbitrary version numbers** (follow semantic structure)

## Automation Opportunities

### Current State
- ✅ Version reading fully automated
- ✅ Pre-commit reminder implemented
- ⚠️ Version bump still manual (by design)

### Future Enhancements
- Add `scripts/bump_version.py` helper script
- Integrate version into PDF metadata
- Add version badge to README
- Generate CHANGELOG.md from version_history

## Troubleshooting

**Issue:** Script shows wrong version
**Solution:** Check that script reads from YAML, not hardcoded

**Issue:** Pre-commit hook doesn't show version
**Solution:** Ensure `.git/hooks/pre-commit` is executable and YAML is valid

**Issue:** Multiple version references found
**Solution:** Use grep command above to find and fix hardcoded versions

**Issue:** Git tag conflicts
**Solution:** Use `git tag -f v8.7` to force update (be cautious)

## Summary

**Single Source of Truth:** `config/numerical_claims.yaml`
**Propagation:** Automatic via scripts reading YAML
**Updates:** Manual YAML edit → git commit → git tag
**Validation:** Pre-commit hook + grep search

This system ensures version consistency across the entire project while maintaining human control over when versions change.
