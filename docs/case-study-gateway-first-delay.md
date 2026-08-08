# Case study: control-plane work before accepted value

## Case boundary

This is a sanitized operational case study. It contains no credentials, private source code, customer data, or internal security topology.

## Observed situation

- The owner reported approximately two weeks of delay while AI advisors repeatedly prioritized a hard-enforcement Gateway. `OWNER_REPORTED`
- The owner reported no accepted user/customer value from that interval. `OWNER_REPORTED`
- Static and package checks existed during the work, but those checks did not by themselves establish physical enforcement, runtime adoption, or customer value. `INTERNAL_EVIDENCE_SUMMARY`
- The recovery created a clean `WITHOUT_GATEWAY` baseline, preserved legacy assets in a restoreable freeze area, passed twelve architecture tests, and locked a controlled local Git commit/tag. `VERIFIED_LOCAL`

## Root-cause interpretation

The incident was not evidence that Gateways are inherently wrong. It was evidence of a sequencing failure:

```text
control-plane design
before
one bounded value flow
before
real demand and incident evidence
```

The same word, “Gateway,” was also used for different responsibilities: network routing, policy evaluation, mutation authority, audit evidence, and human approval. That category collapse made it difficult to remove unnecessary infrastructure without also appearing to remove essential controls.

## Recovery rule

Separate the controls, then justify each one:

```text
Capability boundary
→ Inline validation/policy
→ Human approval for protected actions
→ Evidence and verification
→ Centralized Gateway only when a direct trigger exists
```

## What changed

- Legacy material was preserved rather than deleted.
- The active architecture no longer required Gateway completion before project work.
- Git became the restoreable system baseline.
- Protected external, financial, publication, and irreversible actions still require owner authority.
- Every finite Work Package must expose `OWNER_HOURS_REQUIRED`.

## What this case does not prove

- It does not prove that inline controls are sufficient for every project.
- It does not prove production security.
- It does not establish market demand for this toolkit.
- It does not establish revenue.
