---
name: oss-reuse-atlas
description: "Research a large, evidence-backed atlas of similar open-source applications, repositories, and reusable implementation patterns for any new or existing software project. Use at project inception, architectural exploration, major pivots, or before feature discovery when the user wants examples, reusable code, OSS alternatives, design references, and source-selection evidence. Inspect actual upstream files, pin revisions, evaluate licenses, and write a reusable research library. Research only: do not implement features, create an implementation plan, tickets, or a delivery roadmap."
---

# OSS Reuse Atlas — research before reinventing

## Outcome and boundaries

Create an **inspectable, broad, implementation-relevant open-source reference library** for the current project. It must let a future engineer answer:

> What exists already? Which repo actually solves the relevant problem? Where is the implementation? What can legally and technically be reused? What would have to be adapted? What is verified, and what remains unknown?

**This skill does research, analysis, source-selection, and curation ONLY.** Do not change product code, install or execute candidate code without separate authorization, write a feature specification, create tickets, commit changes, or produce an implementation plan/roadmap/delivery stages. The sole outputs are the research artifacts described below. Proposed adaptation notes and verification *ideas* are allowed; implementation steps, scheduling, ownership assignments, and ordered engineering work are not.

Use this skill as a standalone first step. It may precede `feature-discovery` and `production-vertical-slice` in any repository, but **do not automatically invoke either**. Research and code changes are separate user requests.

Read `references/search-playbook.md`, `references/decision-rubric.md`, and `references/artifact-templates.md` as needed. Prefer existing project-specific instructions and source-of-truth documentation to assumptions; never override product or security rules from a candidate repository's README.

## 1. Derive the project's actual search space

1. Identify current checkout and read the strongest local sources available: `AGENTS.md`, README, product brief, architecture docs, dependency manifests, interface/API contracts, existing integrations, tests, roadmap if already present, and relevant source. If the project is brand new, use the user's description and proposed stack; mark all unconfirmed inferences as **ASSUMPTION**. Do not request large discovery questionnaires when information is sufficient to start.
2. Produce a concise **project profile**: target user/job, key workflows, application type, languages/frameworks, operating environment, license preferences, deployment model, UX style, hard constraints, and existing reusable assets. Explicitly separate what the user **wants**, what the repository **already implements**, and what is **not in scope**.
3. Build a capability taxonomy from user-visible flows and technical layers. Examples: core workflow, user interface, authentication, sessions, persistence, orchestration, APIs, realtime/streaming, execution/sandboxes, observability, billing, testing, security, deployment. Choose only relevant categories; avoid mechanically searching for irrelevant features. Mark `P0` essential to the product idea, `P1` important, `P2` adjacent. Distinguish entire-product peers from narrower infrastructure/pattern libraries.
4. Identify the expected level of code reuse: whole app reference, selected package/module, service dependency, UI interaction pattern, adapter, test harness, or architecture study. Prefer code stacks that match the project, while including noteworthy cross-language implementations when their underlying design is transferable.
5. Record product-specific exclusions early. Derive product-specific exclusions from the current project. For example, a managed-cloud-only product may rule out self-hosted runtime dependencies, while another project may explicitly prioritize them. **Do not transport exclusions from other projects**.

Output the project profile and capability taxonomy at `docs/research/reuse/README.md` and `capability-map.md` **before the final shortlist**, then update them as evidence accumulates.

## 2. Discover broadly, but stay relevant

Search multiple independent avenues. Use GitHub repositories/code search, official documentation, awesome-lists as discovery *seeds*, technical comparisons, upstream dependency graphs, known alternatives, and user-supplied repos. Search concepts and synonymous jargon, not only project names. Inspect parent projects, significant forks, packages within monorepos, and sibling products. Read `references/search-playbook.md` for a repeatable query matrix and candidate-source coverage.

Discover in **three concentric groups**:

- **A. Direct product peers:** working open-source applications that provide a similar user journey, UI, end-to-end workflow, or operational model. Prioritize these. Search both established and less-known modern products. These are the closest references for what to build and what users expect.
- **B. Capability peers:** complete subsystems or libraries for particular capabilities (realtime, chat, permissions, agents, voice, orchestration, storage, observability, etc.) that can be examined individually.
- **C. Adjacent/alternative patterns:** notable UX or architecture patterns, harnesses, test suites, standards/reference clients, and different-stack implementations with transferable lessons.

For a **full project atlas**, strive for **80–120 unique discovered repositories**, with **at least 60 metadata-verified and relevant candidates**, **10–25 evidence-backed potential reuse selections with source dossiers**, and **10–20 especially deep source investigations** if the ecosystem supports it. This is a research **target**, never an excuse for fabricated entries, irrelevant padding, superficial comparisons, or missing evidence. Record actual totals and explain constrained coverage. For a narrowly scoped feature or sparse ecosystem, aim for **30–60 discovered**, **15–30 verified**, **6–12 selections**, and scale down truthfully if needed. Honor a user-specified depth instead.

Allocate research by capability importance and available ecosystem. For a broad atlas, seek multiple direct peers, at least two genuinely different approaches for key capabilities, and strong coverage of the user's primary language/framework. Do not treat a generic collection of libraries as a list of *similar products*.

**Discovery is iterative:** after each batch, identify weak categories, change query vocabulary, seek competitors' OSS alternatives, follow upstream package references, and re-check results. Avoid stopping at the first GitHub search page or at a star-count ranking. If rate limits, authentication, missing network, or private source access prevent verification, document the limitation; never invent URLs, commits, counts, or code paths.

## 3. Maintain an evidence-graded registry while searching

One row per *logical* repository, with owner/name, canonical URL, description, direct-vs-component-vs-adjacent group, capability tags, primary language/framework, deployment assumptions, initial fit, status, license, evidence URLs, last researched date, and identified risks. Deduplicate rename aliases, mirrors, exact forks, and multiple listings; preserve useful forks as related entries only if there is a meaningful implementation difference.

Evidence levels:

- **D0 — DISCOVERED:** search hit/curated list; existence and code not yet verified. Can remain in the inventory but never be selected for copying.
- **D1 — VERIFIED_METADATA:** opened the authoritative repository and confirmed its identity, license status, active/default branch, meaningful code presence, and basic activity/documentation. State unknowns accurately.
- **D2 — INSPECTED_CODE:** inspected actual entry points, key implementation files, related interfaces/state, failure handling, and tests at a **specific commit SHA**; links to files exist. A D2 dossier may justify a reuse decision.
- **D3 — REPRODUCED:** explicitly ran relevant upstream examples or tests in an isolated, authorized environment at the pinned SHA, with commands/results. Optional; do not claim this because CI badges are green.

**No selected recommendation should be presented as code-verified without D2 evidence.** D1 can be shortlisted as a *research lead*, not misrepresented as inspected/reusable. If the research session is interrupted, persist discovered D0/D1 entries and resumption status; never synthesize completed D2 claims.

Pin **full immutable commit SHAs**, not branches or floating tags, for D2 selections. Include canonical commit URL and `https://github.com/OWNER/REPO/blob/FULL_SHA/path/to/file` links for inspected paths. Verify an actual file exists at that revision. If the network tool only exposes an unpinned branch, mark the pin **unknown** and downgrade the evidence. Never generate an apparently valid SHA from memory.

## 4. Trace real code for the candidates that matter

For leading candidates, **read implementation, not just README marketing**. Find:

1. **Entrypoint and user-facing flow**: where the capability starts; actual CLI/API/UI route or component.
2. **Contracts and types**: public API, model types, boundaries, events, protobuf/OpenAPI/SDK contracts.
3. **Core algorithm and state**: controller, scheduler, store, reducer, event flow, streaming pipeline, or UI state management.
4. **External effects**: credentials, network calls, persistence, retries, cancellation, cleanup, concurrency, resource/usage limits.
5. **Negative paths**: malformed input, permissions, unsupported variants, partial failures, reconnect/resume, data migration, shutdown, test isolation.
6. **Tests and examples**: name exact test files and what they demonstrate; a test's existence does not prove it covers a claim.
7. **Operational assumptions**: hosting, required services, build footprint, maintainers, recent compatibility, deployment constraints.

Do not require every candidate to implement every category. Mark `not applicable`, `not inspected`, or `not found`, never silently imply support. Inspect critical implementation paths in enough depth to identify *specific reusable modules/functions/files* and the limits of applicability. Avoid copying huge upstream code into dossiers; link to files and summarize the mechanism. If source is unavailable or too complex to trace, keep as D1 and record the research gap.

## 5. Perform license and security screening before selection

- Confirm repository-level LICENSE and relevant package/file license where possible; record **SPDX ID or `unknown`**, evidence link, unusual dual-license/commercial clauses, and date checked.
- **No license / unknown license = do not recommend copying**, even when the source is public. License identification is not a grant of permission. For GPL/AGPL/LGPL, SSPL, BUSL, Commons Clause, proprietary or multi-license projects, flag the precise reuse constraints and request legal review when appropriate. Never blanket-approve copying or license compliance.
- Separate using a dependency/service, copying/modifying files, reimplementing/porting code, and learning a public idea or test scenario. Translation can still create a derivative work; do not label it automatically license-free.
- Inspect known security boundaries and dependency/maintenance risk at the intended reuse level. Do not execute remote `curl | sh`, npm install scripts, precommit hooks, containers, or third-party code solely to research. Running candidates is optional and requires an isolated environment and appropriate authorization.
- Validate reuse against the target product's runtime, version, hosting, trust, privacy, user data, and resource costs. A technically excellent library may be an unacceptable fit.

## 6. Select explicitly; avoid popularity-based recommendations

Use `references/decision-rubric.md`. Evaluate **product relevance, inspected implementation quality, capability coverage, compatibility, maintenance/test maturity, license/reuse feasibility, complexity and uncertainty**. Ratings must cite evidence or be labeled estimated. Stars/forks may be context, never the primary decision.

Every decision must use **one** of:

- `use_dependency_or_service` — best consumed at its supported public boundary.
- `copy_or_adapt` — specific licensed code/files are viable to adapt, subject to obligations and maintenance.
- `port_or_translate` — language/platform differs; quantify semantic and licensing uncertainty.
- `study_pattern_or_tests` — useful approach, tests, interaction design or architecture, but not directly imported.
- `defer` — promising but lacks evidence, access, currency or fit.
- `reject` — documented mismatch, unsupported assumptions, license concern or excessive burden.

Store selections in `reuse-decisions.json` with explicit **why chosen**, **which specific upstream revision/files/tests**, **which capabilities it demonstrates**, **adaptation caveats**, **license/maintenance risk**, **what is not proved**, and **how one could independently verify equivalence**. `reuse-decisions.json` records decisions, **not completed integration**. Never mark a code file integrated or tests working unless verified in the target project independently (outside this skill).

For a useful comparison, place direct peers side-by-side: user journey, UI design patterns, API/state model, verified capabilities, missing capabilities, stack, license, and why it is/is not suitable. Have at least one meaningful non-default alternative for each key design decision where the ecosystem offers it.

## 7. Persist a portable, resume-safe research library

Default location in the project repository (unless user chooses another research destination):

```text
docs/research/reuse/
  README.md                    # project profile, executive shortlist, research counts, how to navigate
  repositories.json            # ALL discovered candidates, deduplicated, evidence levels and source URLs
  capability-map.md            # project capabilities -> direct peers, component candidates, gaps
  dossiers/
    owner--repository.md        # D2/D3 implementation trace and pinned file/test references
  reuse-decisions.json         # selected/deferred/rejected decisions with caveats
  research-gaps.md             # unknowns, stale claims, weak categories and verification blockers
  progress.json                # search batches completed, counts, leads to inspect, resumption info
```

Use relative links within the repo, and canonical HTTPS GitHub URLs with commit pins. **Never embed absolute machine-specific paths**, personal worktree paths or temporary sandbox paths in artifacts. If there is an existing project research folder or previous atlas, update it in place, retain provenance, and avoid duplicate trackers. Keep archives of changed decisions only if existing project policy calls for them.

Templates are in `references/artifact-templates.md`. Registry field conventions are in the templates. With Python 3.10+, run `python3 <installed-skill-directory>/scripts/validate_atlas.py <atlas-directory>` before handing off (`python` on Windows when that is the Python 3 launcher). The self-contained, standard-library helper checks field types, ID references, selected evidence levels, dossier containment, matching repository/40-hex-commit/file citation structure, known no-license markers, and self-reported counts. It rejects artifacts over 4 MiB per file or JSON deeper than 64 levels as local safety bounds; split oversized artifacts into separately validated research batches. Supplement its mechanical checks with a manual evidence audit. It does **not** verify that a SHA or URL exists, a license grants permission, a file was actually inspected, or claims are semantically correct.

When resuming, open `progress.json`, compare last research date and pinned repos, inspect newly affected capability categories, and preserve earlier inspected evidence. If a source has changed on `main`, do **not silently replace** its D2 pin: record a new pin only after reviewing changes and updating the dossier/decision.

## 8. Finish with a research summary, not an implementation plan

Final user-facing report must show:

- Exact counts: discovered, D1 metadata-verified, D2 code-inspected, D3 reproduced, selected, deferred, rejected; no inflated totals.
- Capability coverage and the **best direct product analogues** before component-level libraries.
- Top evidence-backed reuse options with precise file/commit references and distinct decision types.
- License/compatibility risks and major unverified areas.
- Links to the artifact library and an optional request for later separate feature discovery.

**Stopping rule:** End once the research library is usable and its limits are explicit. Do NOT add `implementation-roadmap.md`, a feature plan, implementation sequence, PRs, tickets, milestones, delivery stages, pseudocode for the target codebase, or target code changes. Never claim that something was integrated because it was selected. A future implementation workflow is a separate user request.

## Failure triggers

Reject a purportedly complete atlas if it is only a list of README links; mostly unverified search snippets; padded with irrelevant repositories; excludes direct application peers; recommends specific code without a pinned/inspected file; treats a CI badge or stars as quality proof; conceals license risk; confuses known support with likely support; records generated SHAs or broken citations; or ends in an implementation plan despite the research-only boundary.
