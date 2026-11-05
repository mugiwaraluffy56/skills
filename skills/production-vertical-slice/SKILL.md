---
name: production-vertical-slice
description: "Implement complete observable software features across all actually required frontend, backend, database, worker, integration and runtime boundaries. Use after feature discovery or an accepted feature spec for nontrivial development, multi-repository workflows, real-world error recovery, tests, UI integration and compatibility. Works alongside an installed implement/TDD skill; not a substitute for fresh requirements discovery or independent acceptance."
---

# Production Vertical Slice — finish the user journey, not a code path

## Purpose

Turn accepted requirements into **working, testable, user-usable behavior** through every boundary needed for that feature. Avoid endpoint-only, visual-only, adapter-only and fixture-only implementations mistakenly called complete. Reuse existing architecture, tooling, CI and acceptance gates rather than imposing a new framework on every repository.

Read project instructions and accepted specs first. If requirements are ambiguous, incomplete, or contain unjustified constraints, resolve discovery before editing code. If `feature-discovery` is installed and its use is permitted, it is an optional integration. Otherwise inspect adjacent code and primary documentation, map the actor-to-result journey and failure variants, identify constraints and consequential decisions, and agree observable acceptance criteria with the user. Stop implementation while essential decisions remain unresolved. Use available `AGENTS.md`, existing task plans, accepted requirement IDs, named checks and gate tools. If they do not exist, keep a lightweight acceptance checklist in the project's established task location and avoid introducing a heavyweight gate unless the user requests one.

## 1. Build a complete delivery map

Read the accepted feature dossier, current code, tests, caller paths and product behavior. Map each acceptance ID onto the real ownership boundaries required (not necessarily all): UI, client state, API, auth, domain model, persistence, async queue/worker, provider/SDK, analytics/audit, infrastructure, deployment/config, and release validation.

For a multi-repo feature, record **exact compatible source revisions**, contract DTOs/versioning, migration order and test environments. If a required repo or service is inaccessible, preserve a clear handoff and mark end-to-end qualification blocked; do not pretend it exists. Preserve surrounding behavior, user data, published APIs, compatibility and migration safety.

A real vertical slice is:

`user / caller → authorization → validated command → authoritative state or external effect → response/events → user-visible result → failure/recovery → test evidence`

For backend/CLI-only software, replace the UI step with its actual public-facing client output. For UI-only work, do not fabricate backend behavior. Trace actual responsibilities rather than touching every layer mechanically.

## 2. Decompose by observable results

Plan the smallest number of **coherent functional slices**, each satisfying explicit acceptance IDs. Give each slice: inputs, actor/permission, state owner, execution path, success/failure transitions, cancel/retry/reconnect, side-effect guarantees, compatibility, actual code paths and tests. Use `references/vertical-slice-template.md` as an addition to the existing plan—not a competing system.

- Derive provider and model limits from provider/model metadata or explicit reviewed policy. Avoid arbitrary hardcoded defaults and overrestrictive validation.
- Distinguish enqueued from running, requested from observed, sent from acknowledged, and locally paired from externally authorized.
- Make permission denial, partial failure, stale response, unknown external effect, service outage and recovery visible/usable when relevant.
- Preserve source-of-truth ownership: no pretend persisted state in browser memory, fake success, invented reviews, simulated providers or unclickable controls.
- For external side effects, enforce auth, scope, consent/approvals and secrets at the trusted boundary; honor idempotency and reconcile uncertain outcomes instead of blind retry.
- For high-risk data changes, assess migrations, rollback, existing records, concurrency and compatibility before mutation.
- For UX, verify discoverability, action affordances, errors/loading/empty states, accessibility, navigation and responsive behavior where applicable. Do not render a wall of text in place of a usable interface.

## 3. Execute with the repository's development discipline

Use the actual project's tools and language. Follow **test-driven or characterization-first** practice for meaningful changes: reproduce the defect with a failing test, implement the real behavior, demonstrate green tests, then refactor safely. A test that merely checks that a component exists, a fake `200` was returned or a build compiled is insufficient.

If Matt Pocock's `/implement` or a similar skill is installed and explicitly invoked/permitted by this harness, use it for bounded slices. Do **not** claim you invoked a model-disabled skill indirectly. This vertical-slice skill is the coordinating **quality discipline**, not a replacement for the project's coding tools.

After each slice:

1. Run focused relevant tests and inspect assertions.
2. Confirm the caller-to-effect-to-response path and precise failure behavior.
3. Check changed contracts, dependent clients, migrations and existing user workflows.
4. Check diff against original acceptance IDs; reopen discovery for materially missed requirements, using the standalone procedure above or an available discovery skill. Never shrink accepted scope to fit the code.
5. Record exact commands, environment, source revision and truthful test result.

For independent subagents, only parallelize work with unambiguous ownership and integration contracts; integrate and rerun authoritative checks in the controlling checkout. Do not silently commit, deploy, pay providers, modify production secrets or perform external actions beyond the user's authorization.

## 4. Verify the actual system seam

Choose checks that reflect the feature, not a ritual list: unit, protocol/contract, integration (real HTTP/database/process), browser interactions, accessibility, security, load/performance, failure injection and live provider qualifications when required. Fixtures can test client handling but cannot prove provider access or real service reliability. A green screenshot, mocked UI, code lint, single passing route or locally paired process does not prove end-to-end production behavior.

Where applicable, test duplicate submission, lost acknowledgement, revoked access, interrupted streams, cancellation races, oversized inputs, provider 429/timeouts, data restarts and compatible upgrades. Tests and reviews must bind to the actual code revision; rerun after changes. A missing live environment is a **qualification gap**, not permission to claim live validation.

## 5. Prepare independent acceptance

Produce a traceable ledger:

`acceptance ID → code paths → actual observable result → test/check + assertions → source revision → evidence level → unresolved blocker`

If `adversarial-acceptance` is installed and permitted, use it with the **original request**, discovery, accepted scope, current diff, base revision and reproducible test/run instructions. Otherwise perform the same acceptance check directly: reconstruct the original journey and supported variants, trace each acceptance ID through the real system, run relevant positive/negative/recovery checks, and record defects separately from evidence gaps. Use an authorized independent reviewer when available; otherwise label the result **self-review**, not independent acceptance. Repair issues without weakening the acceptance standard. Completion requires all applicable accepted criteria demonstrated; report separately: implemented, locally verified, independently reviewed (or not independently reviewed), and live/production qualified. No sibling skill is required to complete this procedure.

## Failure conditions

Do not call the work complete if: it only compiles; UI controls are dead; one side of a required contract is absent; a provider test is simulated but claimed live; limits lack provenance; state or billing is fabricated; error/recovery paths are ignored; tests assert the wrong ceiling; requirements were silently removed; or no trace connects acceptance to observed behavior.
