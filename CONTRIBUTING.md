# Contributing

Contributions should preserve three invariants:

1. No claim of demand, revenue, security, or production readiness without linked evidence.
2. Protected actions remain owner-approved even when Gateway use is not recommended.
3. New decision rules require tests and a falsifiable trigger.

Run before opening a pull request:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python -m ai_delivery_control assess examples/pre_value_project.json
python -m ai_delivery_control validate-work-package examples/work_package.json
```

Please open an issue for behavioral changes before submitting a large patch.
