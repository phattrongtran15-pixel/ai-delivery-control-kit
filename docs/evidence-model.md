# Evidence model

The toolkit uses explicit claim states:

| State | Contract |
|---|---|
| `VERIFIED` | A reproducible test, transaction record, public URL, or independently inspectable artifact supports the claim. |
| `OWNER_REPORTED` | The owner stated the fact; independent measurement is unavailable. |
| `INFERENCE` | The conclusion follows from listed evidence but is not itself directly observed. |
| `MEASUREMENT_MISSING` | The required evidence has not been collected. |
| `HOLD` | An authority, safety, external-action, or acceptance gate is not satisfied. |

## Non-substitution rules

- A plan is not implementation.
- A repository is not adoption.
- CI is not production behavior.
- A public artifact is not demand.
- A lead is not revenue.
- Revenue exists only when transaction evidence exists.
- Static tests do not prove OS-level security enforcement.

## FIRST VERIFIED VALUE

`FIRST_VERIFIED_VALUE` requires all of the following:

1. A bounded output exists.
2. The intended user or customer receives it under the required approval.
3. Acceptance evidence identifies what value was actually obtained.
4. The evidence is linked to the output and time of delivery.

Publication without use remains `OUTPUT_PUBLISHED`; it does not automatically become `FIRST_VERIFIED_VALUE`.
