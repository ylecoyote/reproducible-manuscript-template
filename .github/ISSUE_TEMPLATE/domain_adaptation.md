---
name: Domain Adaptation Example
about: Share how you adapted this template to your scientific domain
title: '[Domain] '
labels: 'domain-specific, user-story'
assignees: ''
---

**Scientific Domain:**
(e.g., astrophysics, computational biology, climate science, machine learning, etc.)

**What did you adapt?**
- [ ] Custom verification checks
- [ ] Data format handling (CSV, HDF5, NetCDF, etc.)
- [ ] Figure metadata structure
- [ ] Statistical tests
- [ ] Other (please describe)

**Brief Description:**
Describe how you modified the template for your field.

**Code Example (optional):**
```python
# Share your custom check if relevant
@framework.register_check(
    id="MY_001",
    name="Your custom check",
    category="your_category",
    severity="ERROR"
)
def your_custom_check(claims: Dict) -> CheckResult:
    # Your implementation
    pass
```

**Lessons Learned:**
What worked well? What was challenging? What would you recommend to others in your field?

**Additional Context:**
Add any other context, screenshots, or links that might help others adapt the template to similar domains.