# Case study: control-plane work before accepted value

## Case boundary

This is a sanitized operational case study. It contains no credentials, private source code, customer data, or internal security topology.

## Observed situation

- The owner reported approximately two weeks of delay while AI advisors repeatedly prioritized a hard-enforcement Gateway. `OWNER_REPORTED`
- The owner reported no accepted user/customer value from that interval. `OWNER_REPORTED`
- Static and package checks existed during the work, but those checks did not by themselves establish physical enforcement, runtime adoption, or customer value. `INTERNAL_EVIDENCE_SUMMARY`
- The recovery created a clean `WITHOUT_GATEWAY` baseline, preserved legacy assets in a restoreable freeze area, passed twelve architecture tests, and locked a controlled local Git commit/tag. `VERIFIED_LOCAL`
- The owner confirmed that the current operating baseline has one active agent, so simultaneous-agent contention is not currently present. `OWNER_CONFIRMED`
- The owner also confirmed that the frozen Gateway contains reusable command/capability work intended to coordinate broader functions and future multi-agent concurrency. `OWNER_CONFIRMED`
- The owner described additional controls beyond API routing: authenticated agent/machine identity, designated-folder enforcement, protection policy, and defensive handling of inter-agent inbox data. `OWNER_CONFIRMED`
- The owner's intended hierarchy threshold is approximately fifty or more AI workers; this is a design threshold, not measured current demand. `OWNER_CONFIRMED_DESIGN_RULE`

## Root-cause interpretation

The incident was not evidence that the Gateway or its commands were inherently wrong. It was evidence of a sequencing and activation failure:

```text
control-plane design
before
one bounded value flow
before
real demand and incident evidence
```

The same word, “Gateway,” was also used for different responsibilities: network routing, policy evaluation, mutation authority, audit evidence, and human approval. That category collapse made it difficult to remove unnecessary infrastructure without also appearing to remove essential controls.

At one active agent, a concurrency chokepoint has no present workload to coordinate. If multiple agents later execute shared commands simultaneously, queueing, locking, rate limits, idempotency, and contention evidence can justify a bounded Gateway. The reusable commands do not need to be deleted while the runtime remains inactive.

Identity, path boundaries, provenance, inbox validation, and prompt-injection defenses remain useful controls even without a centralized Gateway. They can run inline for one agent and migrate behind a Gateway only when scale or a direct incident justifies that move.

## Recovery rule

Separate the controls, then justify each one:

```text
Capability boundary
→ Inline validation/policy
→ Human approval for protected actions
→ Evidence and verification
→ Preserve reusable command contracts independently
→ Centralized Gateway only when a direct trigger exists
```

## What changed

- Legacy material was preserved rather than deleted.
- Gateway runtime and command assets were separated: runtime remains inactive; commands remain `FROZEN_REUSABLE_ASSET` pending inventory and independent tests.
- The active architecture no longer required Gateway completion before project work.
- Git became the restoreable system baseline.
- Protected external, financial, publication, and irreversible actions still require owner authority.
- Every finite Work Package must expose `OWNER_HOURS_REQUIRED`.

## What this case does not prove

- It does not prove that inline controls are sufficient for every project.
- It does not prove production security.
- It does not prove a concurrency bottleneck while only one agent is active.
- It does not establish market demand for this toolkit.
- It does not establish revenue.
