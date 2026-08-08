# Multi-agent control boundary

## Responsibilities that must not be collapsed

1. **API routing and traffic shaping** — destination, queue, rate limit, backpressure.
2. **Identity** — authenticated agent/machine identity; caller payload cannot grant itself a role.
3. **Capability policy** — which action a role may request.
4. **Path boundary** — writes only inside explicitly designated roots after normalization.
5. **Protected-action approval** — owner receipt bound to action, resource, payload, policy, and expiry.
6. **Inter-agent data defense** — provenance, schema validation, instruction/data separation, quarantine, and injection handling.
7. **Evidence** — work/run IDs, decision, control version, output, and review state.
8. **Downstream binding** — the entry decision must bind to the operating-system service, container/runtime, executor, and returned evidence.

These controls may be inline in a one-agent system. A Gateway becomes a candidate when several agents need one shared enforcement and coordination point; it becomes justified only with a direct incident or confirmed external requirement.

## Congestion evidence to collect

- Peak concurrent agents and commands.
- Queue depth and wait time.
- Lock/contention time and timeout count.
- Duplicate or out-of-order execution count.
- API rate-limit and retry volume.
- Inbox rejection, quarantine, and injection findings.
- Resource saturation and recovery time.

Without these measurements, “the Gateway will be needed” is a risk hypothesis, not runtime evidence.

## Activation gate

Gateway necessity and Gateway activation are different decisions. A bounded pilot remains `HOLD` until all three are evidenced:

- Downstream execution binding passes an end-to-end test across the declared lanes.
- A business/demand or direct external requirement exists.
- A finite resource budget is approved.

If any row is missing, preserve the frozen asset and stop spending on runtime repair.
