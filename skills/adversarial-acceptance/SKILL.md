---
name: adversarial-acceptance
description: "Independently evaluate whether an implemented software feature actually satisfies the original user request and is appropriately qualified. Use after nontrivial feature work, before release, after suspiciously easy green tests, for integrations and cross-repository features, or when scope, compatibility, security, user journey or operational readiness is disputed. Review and test; do not fabricate results or silently rewrite requirements."
---

# Adversarial Acceptance — challenge what was built

## Goal and independence

Treat the implementer's completion report, green CI, spec checklist and screenshot as **hypotheses**, not evidence of the full requested product outcome. Try to disprove scope completeness, correctness and qualification at the actual boundary users depend on.

Read the original user request and approved product decisions **before** reading the implementation explanation. If available, assign independent reviewer/tester agents the request, spec, base/current revision, actual diff and runnable seams. If independence is unavailable, perform a clearly labeled self-review; never invent a reviewer identity or record an unperformed live observation. Honor any existing project's formal reviewer/evidence process.

## 1. Reconstruct the expectation independent of the code

Rebuild the user journey and major variants: setup, permissions, interaction, status/result, persistence, change/stop, errors, and recovery. Cross-check approved requirements with current official API/protocol constraints and relevant upstream code where external compatibility matters. Audit the scope **itself**, not only the accepted tests.

Look for missing legitimate auth modes/formats, states, versions, provider/model capabilities, UI entrypoints, supported input sizes, connected subsystems, migrations and recovery semantics. Challenge numeric bounds, defaults, allowlists, timeouts and fallback logic. A test that asserts an invented `2048` cap is a regression in the wrong direction, not proof of good behavior. Identify the actual provenance and scope of every material constraint.

If an essential requirement is missing, record a **scope defect** and follow the repo's approved spec-change process. Use `feature-discovery` only if installed and permitted; otherwise reconstruct the missing journey/variants from the original request and source evidence, propose observable criteria, and ask the user to resolve consequential scope choices before re-evaluating acceptance. No sibling skill is required. Do not silently reclassify the missing requirement as an optional improvement.

## 2. Trace and test actual running boundaries

For each acceptance ID, trace as applicable:

`client/user → authentication/authorization → validation → API/transport → DB/worker/provider/effect → durable response/events → presentation → interruption/recovery`

Test representative positive, negative and boundary cases *derived from the contract*, not just cases chosen by implementer. Examples only when relevant: revoked credentials/tenant boundaries, malformed but legitimate variants, lost acknowledgement, duplicate commands, stale revisions, provider 429/timeouts, cancellation races, reconnect/reload, old data migration, high/low limits, accessibility and empty/error UX.

For multi-repo changes, verify both contract ends and served revisions; repo compatibility is an observed fact, not a claim. If environment or permission blocks live testing, record exactly what remains unverified.

## 3. Separate evidence levels

- **Static:** reviewed code, lint, typecheck, build; does not prove behavior.
- **Unit/contract:** tested narrow logic, including meaningful negative assertions.
- **Integration:** real HTTP/database/process boundaries; fake remote provider proves adapter behavior only.
- **Rendered client:** real navigation and UI states, including errors; intercepted requests are still fixtures.
- **Live qualification:** authorized real provider/infra/identity/worker boundary with observed request/result, credentials policy, cost/limits and exact served revision.
- **Operational qualification:** deployment, monitoring, actual version, rollback/recovery and workload validation as required by launch risk.

Maintain distinct `passed`, `failed`, `not run`, `blocked` and `not applicable` states. Check tests are nonvacuous and executable at current source revision. Never manufacture review receipts or weaken test assertions/evidence policy to get a passing status.

## 4. Review four dimensions where applicable

1. **Scope/product:** Is the customer actually able to finish the intended journey? Are essential supported variants and constraints represented faithfully?
2. **Correctness/compatibility:** Are state transitions, API/SDK versions, persistence, recovery, external effects and migrations correct across affected callers?
3. **Security/reliability:** Are identity/tenant boundaries, secrets, permissions, cost/resource limits and ambiguous effects handled safely? Label unverified risk rather than alleging a proven vulnerability without evidence.
4. **UX/operability:** Can users discover, understand, change, stop and recover the feature? Does error/empty/loading state communicate truth, and can operators diagnose a failure?

Use `references/acceptance-template.md` and existing project review artifacts. Record observed commands/results, inputs, revision, fixtures vs live, reproduction of defects and accepted requirement IDs. For each ID report `satisfied`, `partial`, `missing`, `contradicted` or `unverified`.

## 5. Provide a credible verdict and correction loop

Separate:

- **Scope defect**: relevant requested capability or legitimate variant missing/unsupported without a recorded product decision.
- **Implementation defect**: promised behavior fails, is misleading, is insecure, or regresses an existing flow.
- **Qualification gap**: code may work, but required live or independent evidence was not obtained.

Send grounded findings and reproductions to implementer; demand fixes to implementation, not retroactive weakening of acceptance. Re-run affected checks and inspect the final diff after repairs. Final verdict: `NOT READY — SCOPE`, `NOT READY — IMPLEMENTATION`, `LOCALLY VERIFIED — LIVE PENDING`, `QUALIFIED FOR <SPECIFIC ENVIRONMENT>`, or `BLOCKED/UNVERIFIED`.

Never claim generic "production ready" from isolated unit tests or fixture-only demos. State exactly which environment, workload, permissions and version were genuinely qualified.
