# Anti-pattern: Gateway-first before verified value

## Signal

The project cannot deliver one bounded user outcome because a shared control plane is not “complete.”

## Typical symptoms

- Governance packages grow while accepted outputs remain zero.
- Static PASS is discussed as though it proves runtime enforcement.
- Multiple responsibilities are hidden under the word `Gateway`.
- The owner becomes a command runner or log courier.
- No trigger connects the Gateway to a real incident, buyer requirement, or multi-team scale problem.

## Decision test

Ask:

1. Is there a verified incident that inline controls failed to stop?
2. Is there a confirmed buyer/compliance requirement?
3. Are multiple teams or tenants duplicating the same policies?
4. Does at least one accepted-value flow already exist?

If all answers are no, use the smallest enforceable controls and ship the bounded flow. Record the missing evidence instead of inventing a maturity percentage.

## Exit criteria

The anti-pattern is resolved when project execution no longer depends on speculative central infrastructure and protected actions remain fail-closed.
