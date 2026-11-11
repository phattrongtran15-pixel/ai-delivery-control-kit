# KE_HOACH — RON-SHO Semantic Asset Canary V2

## Mission
Complete one GitHub-only semantic file-purpose and requirement trace canary in one authorized pass. Scope: existing ai-delivery-control-kit sandbox branch. No local laptop, no paid LLM/API, no main mutation, no merge, no production deploy.

## Authorization and checkpoint
- User authorized full bounded implementation and testing on GitHub in one pass (11 Nov 2026).
- Repo: phattrongtran15-pixel/ai-delivery-control-kit
- Original main checkpoint: 981c88592c78e908c1ce9c39dec93fa7718c4cd4
- Pre-V2 sandbox checkpoint: f252688dc692ce668a060c9b78144d99c69ca082
- Allowed changes: new files under sandbox/semantic_asset_canary_v2/ and a new isolated GitHub Actions workflow under .github/workflows/.
- Rollback: reset sandbox branch to f252688d or discard branch, subject to explicit rollback request. main must stay on original SHA.
- Protected authority is not granted to modify Core X, production or secrets.

## Five steps, one authorized execution
1. [x] Inspect scope and pin main/sandbox SHA; read repo source, tests, schemas and README.
2. [x] Design evidence contract with four requirements and two deliberate missing/negative paths.
3. [ ] Commit analyzer, independent verifier, manifest, and Actions workflow atomically to sandbox.
4. [ ] Execute GitHub Actions with existing unit tests, syntax/static extraction and adversarial verification; read job logs and artifact.
5. [ ] Read back main SHA, consolidate evidence and publish the final human-readable handoff; no implicit human acceptance of unverified claims.

## Result definitions
- PASS_SOURCE_ONLY: file SHA, AST symbol, test call and document anchor independently confirmed.
- STATIC_TRACE_PRESENT: document + source symbol + test invocation exist. NOT runtime behavior.
- HOLD_INCOMPLETE_TRACE: any required link missing.
- SOURCE_DECLARED: a literal source description, not proof of original creator intent.
- INFERENCE: technical role derived from syntax/path; still not accepted.
- UNKNOWN: unsupported original intent, missing evidence, or unexplained file.

## Negative cases
- Undocumented file must remain UNKNOWN.
- Misleading docstring may be quoted only as SOURCE_DECLARED, not VERIFIED.
- Injection-like document text must never override classification.
- Tampered hash, fabricated PASS trace, and fabricated human acceptance must be rejected by a separate verifier.

## Output
GitHub Actions artifact contains:
- ASSET_PROFILES_V2.json
- REPORT_V2.md
- VERIFICATION_V2.json

No new model API is invoked; actual neural/LLM semantic understanding and production Core X behavior are outside this canary. The user has authorized this bounded run, not unverified fact claims.
