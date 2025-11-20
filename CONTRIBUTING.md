# Contributing to Reproducible Manuscript Template

Thank you for considering contributing to this project! This template aims to help scientists write reproducible papers with automated verification.

## How to Contribute

### Reporting Bugs

If you find a bug, please [open an issue](../../issues/new?template=bug_report.md) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Your environment (OS, Python version)

### Suggesting Features

We welcome feature requests! Please [open a feature request](../../issues/new?template=feature_request.md) describing:
- The problem you're trying to solve
- Your proposed solution
- Your scientific domain (helps us understand diverse use cases)

### Contributing Code

1. **Fork the repository**
   ```bash
   gh repo fork ylecoyote/reproducible-manuscript-template
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   python3 verify_manuscript.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

6. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow [PEP 8](https://pep8.org/) for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### Documentation

- Update README.md if adding new features
- Add examples for new verification checks
- Document any new configuration options

### Testing

Before submitting a PR:

- [ ] Run `python3 verify_manuscript.py` successfully
- [ ] Test with the example script: `python3 scripts/example_analysis.py`
- [ ] Verify pre-commit hook works: `pre-commit run --all-files`
- [ ] Check that documentation builds correctly

## Project Structure

Understanding the codebase:

- **`verify_manuscript.py`**: Core verification framework
- **`numerical_claims.yaml`**: Example contract configuration
- **`scripts/`**: Example analysis scripts
- **`docs/development/`**: Design documentation and case studies

For detailed architecture information, see [docs/development/](docs/development/).

## Types of Contributions We're Looking For

### High Priority

- **Domain-specific examples**: Show how this works in different scientific fields
- **Verification check recipes**: Pre-built checks for common scenarios
- **Integration guides**: How to use with LaTeX, Overleaf, Jupyter, etc.
- **Bug fixes**: Especially edge cases in verification logic

### Medium Priority

- **Documentation improvements**: Clearer explanations, more examples
- **Tooling integrations**: GitHub Actions, GitLab CI, etc.
- **Performance improvements**: Faster verification for large projects

### Nice to Have

- **Visualization tools**: Dashboard for verification results
- **IDE plugins**: VSCode/PyCharm integration
- **Alternative backends**: Support for HDF5, NetCDF, etc.

## Community Guidelines

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Celebrate diversity in scientific approaches

## Questions?

If you have questions about contributing:

1. Check existing [issues](../../issues) and [discussions](../../discussions)
2. Review the [development documentation](docs/development/)
3. Open a new [discussion](../../discussions/new) if needed

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make scientific publishing more reproducible!** 🔬
