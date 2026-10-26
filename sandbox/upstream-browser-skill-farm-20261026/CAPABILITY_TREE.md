# Capability Growth Tree — nine required RON-SHO layers

Current evidence is **staging only**, not acceptance of full AIOS platform. CI run: [40348875505](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/40348875505).

~~~mermaid
flowchart TD
  A["1. Browser monitor — PARTIAL"] --> B["2. Isolated multi-client MCP — VERIFIED staging"]
  B --> C["3. Skill learning — browser trace candidate; no autonomous LLM"]
  C --> D["4. Record/replay/verify — VERIFIED staging"]
  D --> E["5. Action cache — VERIFIED staging"]
  E --> F["6. Cross-agent searchable memory — SQLite FTS5 VERIFIED staging"]
  F --> G["7. Automation — GitHub Actions VERIFIED"]
  G --> H["8. Shared memory — GitHub job handoff VERIFIED; cloud/local live UNKNOWN"]
  H --> I["9. Growing capability tree — versioned graph; live registry UNKNOWN"]
~~~

- **Observe**: Run local Chromium sessions under staging fixture. BrowserOS source available but browser GUI product not deployed.
- **Learn**: Candidate skill from observed action, independent source readback, test-only approval.
- **Remember**: Actual SQLite FTS5 stores versioned skill; a different job retrieves and validates it.
- **Reuse**: Pre-action retrieval plus fingerprint-keyed cached action; stale/unauthorized matches denied.
- **Govern**: No production PolicyGate or canonical RonSkillStore mutation.
- **Grow**: JSON lineage, Mermaid tree, evidence links. xyflow live UI not deployed.

**Do not count source download, CLI --help, source snapshot, or simulated actor label as actual running integration.**
