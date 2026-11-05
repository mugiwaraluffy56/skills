---
name: feature-discovery
description: "Discover complete, user-relevant feature requirements before coding in any software project. Use for new features, major behavior changes, integrations, APIs, voice, chat, payments, agents, data models, backend services and UI journeys when compatibility, provider capabilities, edge cases, defaults or acceptance criteria may be missed. Research and specify; do not implement code. Skip for purely mechanical changes."
---

# Feature Discovery — design the right feature before implementing it

## Purpose and stop boundary

A feature request expresses a product outcome, not permission to build the smallest easily passing implementation. Produce a sourced capability/compatibility matrix, an end-to-end journey, justified constraints, meaningful failure scenarios and observable acceptance criteria. This is **discovery**, not implementation. Do not edit product code, invoke the implementer, or silently substitute a small MVP for a full requested capability.

Respect existing repository instructions, accepted specifications and product decisions. Do not invent a new spec system if one exists. If the project is new, use `docs/features/<slug>/discovery.md` as a default, and clearly distinguish proposed architecture from actual code. Where an `oss-reuse-atlas` research library already exists, consult its pinned sources rather than rediscovering everything; update stale claims if necessary. An entire new atlas is not required for every small feature.

## 1. Establish the actual starting point

- Read applicable `AGENTS.md`, README, product/architecture documents, ADRs, API/DB schemas, test setup, CI, deployment constraints and the current source tree. Check version/branch and working-tree changes. The code proves what is implemented; aspirational docs describe intent.
- Trace at least one existing adjacent user journey through entrypoint, API/transport, validation, state owner, adapters, storage, UI and tests as applicable. Identify existing extension mechanisms and behavior to preserve.
- For multi-repo features, inspect **each accessible owner** and the exact interfaces, DTOs, events, versions and rollout dependencies. Document inaccessible repos as unverified. Do not call an interface complete because one end exists.
- Record the project’s actual runtime, users, deployment model, trust boundaries, language/stack and hard product exclusions. Never carry a different project's constraints into this one.

## 2. Derive complete but relevant product scope

Describe the journey from the user’s perspective: discovery/entry → setup → main action → result → later use/change → disable/stop → recovery. Adapt this sequence to the feature; do not force unrelated steps. Identify every legitimate major variant of the user's request (auth methods, input types, browser/device modes, API versions, access roles, large/small payloads, interactive/batch workflows, etc.).

Examine as applicable:

- Actor, permissions, prerequisites, navigation, onboarding and discoverability.
- Inputs/formats/variants, validation, defaults, configurable controls and documented unsupported combinations.
- Authoritative state, persistence, identity, transitions, progress, retries, cancellation, timeouts, reconnect, concurrency, idempotency and crash recovery.
- External effects, remote providers, service credentials, rate limits, billing and operational ownership.
- UI states: empty, loading, partial, pending, denied, expired/revoked, unavailable, failed, recovered and successful. Include accessibility and mobile/responsive behavior where it affects use.
- Compatibility: old clients, existing data, migrations, deployments, historical configurations, feature flags and regressions.
- Privacy/security, observability, performance and supportability proportional to actual risk.

Examples illustrate distinctions, not mandatory requirements: voice dictation is not the same as conversational voice and playback; chat rendering is not the same as durable streams and reconnection; API-key syntax is not proof of authorization; model context window, output-token capacity and application spending budget are separate dimensions.

## 3. Research external reality, not just conventions

For features depending on outside protocols/APIs/ecosystems, use current **primary** documentation: API reference, supported modes, version, errors, authentication, limits, pricing, sample clients and deprecations. Record an exact source URL, when checked, and applicable version. Inspect source paths and tests in at least one relevant mature OSS peer where available; more for materially different approaches. Explain what is observed in code versus only claimed in README. Screenshots and marketing are discovery leads, not behavioral proof. No need to research external APIs for a local layout-only change.

Create a **capability matrix** with columns: capability/variant, official support, peer implementation paths, current product support, user relevance, decision, evidence and acceptance ID. Use `supported`, `conditional`, `unsupported`, `unknown`, or `not applicable`. Do not turn `unknown` into `unsupported`; do not copy every competitor feature by default.

**Mandatory constraint provenance:** Any cap, allowlist, timeout, key-format restriction, size, retry count, rate/parallelism bound, default, feature exclusion or fallback must trace to one of: an official provider/protocol limit; an approved product/security/cost decision; or a measured, explicitly reviewed engineering tradeoff. Record units, scope, who owns it, whether configurable and user-visible failure behavior. Never invent a small hardcoded ceiling for convenience. Conversely, do not infer that absence of a documented cap means unlimited or safe.

Screen proposed integrations against actual product policies, legal terms and credential handling. Document source versions and uncertainty, particularly where providers differ by plan, geography, account status or model.

## 4. Write observable, challengeable acceptance criteria

Prefer the existing repository task/spec/acceptance convention; otherwise save `docs/features/<slug>/discovery.md` with the structure in `references/discovery-template.md`. Include:

1. User outcome and the complete essential user journey.
2. Relevant existing behavior and architecture/ownership map with exact code paths.
3. Capability/compatibility matrix and official/OSS references.
4. Constraint provenance register (especially numeric bounds).
5. Failure, permission, stop/retry, recovery and compatibility scenarios.
6. Acceptance IDs (`F-01` etc.) stating **observable results**, including positive and meaningful negative/boundary cases; assign source owner and proposed verification seam (unit, integration, browser, live) where known.
7. `essential now`, `recommended later`, and `explicitly excluded`; give a reason and source for each material exclusion.
8. Unknowns, blockers, decisions required, and a `READY` / `NOT READY` verdict.

A real requirement is not “create endpoint X”; it is “authorized actor performs Y, authoritative state changes to Z, UI/client shows the correct outcome, and recovery or denial behaves as specified.” Avoid irrelevant enterprise features unless the requested feature needs them. Ask only about consequential product choices; make reversible, evidence-backed routine decisions and label assumptions.

## 5. Handoff and regression controls

`READY` requires coverage of every essential journey and relevant variants, traceable restrictions, clear ownership of touched boundaries and verification of failure cases. If not ready, identify exactly what remains unknown; never conceal it to make implementation start. Do not weaken already accepted criteria. If implementation later discovers a missed essential behavior, reopen discovery and apply the repository's approved change/supersession process rather than rewriting history.

Hand off the requirements dossier to `production-vertical-slice` or the repository's chosen implementation workflow. For a user who requested only research/specification, stop here. No code or production changes.

## Red flags

Reject scope based on the easiest demo, happy-path only, one auth variant from many legitimate options, guessed limits (e.g. 2,048 output tokens), UI without durable behavior, misrepresented provider support, a chosen reference without actual source inspection, or treating a mocked response as acceptance.
