# Anti-pattern: Gateway-first before verified value

## Signal

The project cannot deliver one bounded user outcome because a shared control plane is not “complete.”

## Typical symptoms

- Governance packages grow while accepted outputs remain zero.
- Static PASS is discussed as though it proves runtime enforcement.
- Multiple responsibilities are hidden under the word `Gateway`.
- The owner becomes a command runner or log courier.
- No trigger connects the Gateway to a real incident, buyer requirement, or multi-team scale problem.
- The entry Gateway is discussed as complete while downstream service/container/executor binding remains unverified.

## Decision test

Ask:

1. Is there a verified incident that inline controls failed to stop?
2. Is there a confirmed buyer/compliance requirement?
3. Are at least two agents actually executing shared commands concurrently?
4. Is there measured queue, lock, rate-limit, duplicate-execution, or resource-contention evidence?
5. Are multiple teams or tenants duplicating the same policies?
6. Does at least one accepted-value flow already exist?

If all answers are no, use the smallest enforceable controls and ship the bounded flow. Record the missing evidence instead of inventing a maturity percentage.

## Exit criteria

The anti-pattern is resolved when project execution no longer depends on speculative central infrastructure and protected actions remain fail-closed.

Do not confuse deactivating the Gateway runtime with deleting its useful commands. Freeze, inventory, extract, and test reusable command contracts independently; reactivate central coordination only after a direct concurrency or external-control trigger exists.

Even after a need is identified, activation stays on hold without verified downstream end-to-end binding, real demand, and an approved resource budget.
