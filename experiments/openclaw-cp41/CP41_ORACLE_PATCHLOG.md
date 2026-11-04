# CP4.1 sandbox verification enhancement #2

- Previous HEAD: \`691b307b8a0436ecc79378f09665abee0e219cbe\`.
- Previous successful run: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/41796052832
- Independent artifact read-back: 7/7 PASS; agent exec code 0, model two turns, toolSummary exec=1, fake workflow create/validate/test/evidence 1 each.
- Found oracle weakness: duplicate test used a boolean/effect summary \`tests=1\` rather than separately recording inbound requests and effective test executions.
- Narrow fix: add \`testRequests\` (request count) and \`testExecutions\` (actual idempotent effect count). Assert duplicate has two test requests and one test execution; agent happy path one each.
- This proves simulated receiver-side deduplication, NOT n8n's native execution idempotency.
- Rollback: prior source blob \`c51279348c68e03c390ae04f65c3b773596cfc5c\`; no default-branch change.
