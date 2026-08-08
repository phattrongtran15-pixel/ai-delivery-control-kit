# Recover commands without activating the Gateway

## Decision

`GATEWAY_RUNTIME = HOLD`

`COMMAND_ASSETS = FROZEN_REUSABLE_ASSET`

This pattern applies when useful commands, policies, tests, and contracts exist inside a Gateway implementation, but the current system has one active agent and no verified concurrency bottleneck.

## Why separate them

A command is a capability contract. A Gateway is one possible coordination and enforcement runtime. Removing a runtime dependency does not require deleting the capabilities that were placed behind it.

The same separation applies to safety controls. Authenticated agent identity, designated-folder boundaries, message provenance, inbox schema validation, and prompt-injection defenses can be enforced inline before centralized coordination is justified.

## Recovery sequence

1. Freeze the original tree with a restore path; do not delete or silently adopt it.
2. Inventory every command by name, purpose, inputs, outputs, mutability, permissions, evidence, tests, and dependencies.
3. Mark each command `REUSE`, `REWRITE`, `REFERENCE_ONLY`, `DUPLICATE`, `UNSAFE`, or `UNKNOWN`.
4. Extract one command contract at a time into the active system without importing the old Gateway authority or gate state.
5. Run positive, negative, permission, idempotency, recovery, and evidence tests.
6. Activate only the command that passes its own acceptance gate.
7. Keep the Gateway runtime inactive until a direct trigger is verified.

## Gateway reactivation triggers

- At least two agents execute shared commands concurrently **and** centralized coordination is measurably needed.
- A verified duplicate-execution, queue, lock, rate-limit, or shared-resource contention incident occurs.
- Inter-agent inbox traffic creates a verified provenance, injection, or isolation incident that inline controls cannot contain.
- A confirmed external, compliance, tenant, or enterprise requirement mandates centralized enforcement.
- Several independent teams duplicate the same policies and a bounded central pilot has accepted-value evidence.
- Around fifty or more active AI workers is an explicit scale-review trigger in this operating model, but not automatic approval.

Agent count alone is a signal, not proof. With one active agent and no direct trigger, the recommended state remains `INLINE_CONTROLS_FIRST`.

## Control placement by scale

| Current state | Placement |
|---|---|
| One agent | Inline identity, path, approval, evidence, and input-defense controls |
| Several concurrent agents | Measure queue/lock/rate-limit/idempotency contention before centralizing |
| Approximately 50+ AI workers | Mandatory architecture review for hierarchy, traffic shaping, isolation, and bounded Gateway pilot |
| Verified incident or external mandate | Scope a Gateway to the evidenced trigger and independently verify enforcement |

## Work Package requirement

Every recovery Work Package must include `OWNER_HOURS_REQUIRED`, exact frozen source reference, no-copy/adoption boundary, command-level tests, rollback, and Ron approval for protected actions.
