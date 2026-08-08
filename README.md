# AI Delivery Control Kit

`OSS_RECOVERY_DIVIDEND-01` turns an infrastructure-first AI project failure into a small, reusable control toolkit.

It helps a builder answer two questions before adding a centralized Gateway or control plane:

1. What is the smallest control stack required by the current risk?
2. What evidence would justify centralizing enforcement later?

The toolkit is deliberately **not anti-Gateway**. It separates four control layers that are often conflated:

- hard boundaries and capability removal;
- inline validation and policy checks;
- human approval for protected actions;
- centralized Gateway/control-plane enforcement.

## What it includes

- A deterministic Gateway-necessity assessment CLI.
- A Work Package validator that requires `OWNER_HOURS_REQUIRED`.
- A sanitized case study of a two-week infrastructure-first delay.
- A reusable anti-pattern card and demand-validation contract.
- A command-library recovery pattern that preserves useful capabilities without activating an unnecessary Gateway runtime.
- A multi-agent control boundary covering identity, designated paths, inbox/provenance defense, and congestion evidence.
- JSON Schemas, examples, unit tests, and CI.

## Quick start

Python 3.10+ is required. The core package has no runtime dependencies.

```bash
python -m pip install -e .
python -m unittest discover -s tests -p "test_*.py" -v
python -m ai_delivery_control assess examples/pre_value_project.json
python -m ai_delivery_control validate-work-package examples/work_package.json
```

The installed command is also available as `ai-delivery-control`.

## Decision states

| State | Meaning |
|---|---|
| `INLINE_CONTROLS_FIRST` | Hard boundaries, scoped capabilities, inline checks, evidence, and HITL are currently sufficient. |
| `CENTRAL_POLICY_CANDIDATE` | Multiple shared control signals exist; central policy evaluation may reduce duplication. |
| `CENTRAL_GATEWAY_CANDIDATE` | Scale and accepted-value evidence justify a bounded Gateway pilot. |
| `GATEWAY_JUSTIFIED` | A verified incident or confirmed external requirement directly justifies Gateway enforcement. |

The result is a decision aid, not security certification.

For a one-agent system, the tool explicitly separates `GATEWAY_RUNTIME = HOLD` from `COMMAND_ASSETS = FROZEN_REUSABLE_ASSET`. See [command-library recovery](docs/command-library-recovery.md).

## Evidence discipline

This repository distinguishes:

- `VERIFIED`: backed by a reproducible test or public artifact.
- `OWNER_REPORTED`: stated by the project owner but not independently measured.
- `INFERENCE`: a reasoned interpretation.
- `MISSING`: evidence does not yet exist.

No demand, revenue, production readiness, or security claim is inferred from repository existence, CI, stars, or a submitted application.

## Project status

- Local build and tests: `VERIFIED` when the test receipt is present.
- Public repository and release: `VERIFIED` at [phattrongtran15-pixel/ai-delivery-control-kit](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit).
- Public CI: `VERIFIED` for Python 3.10, 3.11, and 3.12 on release commit `332c62c16ca573ce3e6ae277ab5f10cad0d25465`.
- External demand: `MEASUREMENT_MISSING` until a real user action is recorded.
- Revenue: `0 VERIFIED` until transaction evidence exists.

See [the recovery report](reports/OSS_RECOVERY_DIVIDEND-01.md), [publication receipt](reports/PUBLICATION_RECEIPT.json), and [evidence model](docs/evidence-model.md).

## License

MIT. See [LICENSE](LICENSE).
