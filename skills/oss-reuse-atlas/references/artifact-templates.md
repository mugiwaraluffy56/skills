# Reuse research artifact contracts and examples

These are **research data structures**, not a task/implementation plan. Save in the target project at `docs/research/reuse/` or the project's chosen research folder. All paths below are portable, relative or canonical source URLs. Use real values, never placeholders or made-up SHA values when presenting completed research.

## `repositories.json`

```json
{
  "schema_version": 1,
  "project": "Your project name",
  "researched_at": "YYYY-MM-DD",
  "repositories": [
    {
      "id": "owner/repository",
      "url": "https://github.com/owner/repository",
      "group": "direct|component|adjacent",
      "capabilities": ["capability-tag"],
      "stack": ["language", "framework"],
      "license": "SPDX-ID-or-unknown",
      "maintenance": "current|stable|inactive|unknown",
      "evidence_level": "D0|D1|D2|D3",
      "pinned_commit": null,
      "evidence_urls": ["https://github.com/owner/repository"],
      "dossier": null,
      "known_gaps": ["Not yet code inspected"]
    }
  ]
}
```

For D2/D3, replace `pinned_commit` with a real full 40-character SHA verified at the repository, and `dossier` with a relative path like `dossiers/owner--repository.md`. Use exact revision-pinned file URLs in the dossier. Do not call D0/D1 "verified code."

## `reuse-decisions.json`

```json
{
  "schema_version": 1,
  "decisions": [
    {
      "repository_id": "owner/repository",
      "decision": "study_pattern_or_tests",
      "status": "selected",
      "capabilities": ["capability-tag"],
      "why": "Actual fit supported by the pinned dossier",
      "upstream_files": ["src/relevant/file.rs"],
      "upstream_tests": ["tests/relevant_test.rs"],
      "pinned_commit": "REPLACE_WITH_VERIFIED_40_HEX_SHA",
      "adaptation_notes": "Differences from target project, without task sequence",
      "licensing_risks": "What was checked and what is uncertain",
      "not_proven": ["Real integration into this project"],
      "possible_equivalence_checks": ["Behavioral contract comparison"]
    }
  ]
}
```

Allowed `decision` values: `use_dependency_or_service`, `copy_or_adapt`, `port_or_translate`, `study_pattern_or_tests`, `defer`, `reject`. A `selected` decision must point to a D2/D3 record and real pinned SHA. A D0/D1 can be a `defer` or `reject`, or an unselected research lead, not a source-verified selection. `status` must be `selected`, `deferred`, or `rejected`, consistent with decision.

**Legal caution:** A discovered public repo is not automatically licensed for reuse. An absent/unknown license precludes recommending copying code; language-porting could still be derivative. Record relevant file-level conditions and uncertainties rather than giving blanket legal approval.

## `progress.json`

```json
{
  "schema_version": 1,
  "researched_at": "YYYY-MM-DD",
  "completed_query_families": ["direct product peers", "stack-specific"],
  "pending_capabilities": ["unverified-category"],
  "resume_notes": "Next research question, no task milestones",
  "counts": {
    "discovered": 1,
    "metadata_verified_or_more": 0,
    "code_inspected_or_more": 0,
    "reproduced": 0,
    "selected": 0,
    "deferred": 0,
    "rejected": 0
  }
}
```

Counts must be computed from the final registry, never manually inflated to meet a target.

## `dossiers/owner--repository.md`

```md
# owner/repository — source dossier

- Canonical repository: https://github.com/owner/repository
- Inspected immutable commit: FULL_VERIFIED_SHA
- License: SPDX and relevant upstream license URLs
- Status: code inspected (D2), not executed (unless D3 evidence exists)
- Useful for: identified product capability
- Relevance/compatibility: stack and deployment assumptions

## Path trace

| Concern | Pinned file URL | Observed behavior | Test path / gaps |
|---|---|---|---|
| Entry | exact SHA file link | observed | exact SHA test link |
| Types/contracts | exact SHA file link | observed | ... |
| Durable state / workflow | exact SHA file link | observed | ... |
| Permissions / external effects | exact SHA file link | observed | ... |
| Failures / recovery | exact SHA file link | observed | ... |

## Source-backed reuse evaluation

- Exact item worth using/studying:
- What it handles, and what it **does not** support:
- Proposed decision (not integrated):
- Licensing / maintenance / security implications:
- Unknowns and no-proof boundaries:
- Possible future behavior-equivalence checks (no implementation sequence):
```

## Other Markdown research files

- `README.md`: project profile, source dates, counts, best full-product analogues, how to navigate the research. Explicitly distinguish selected references from integrated code.
- `capability-map.md`: `capability → product peers → component candidates → source-level evidence → unknowns`.
- `research-gaps.md`: missing licenses, unavailable sources, weak categories, broken pins, unverified variants. Include links to source evidence.

Do **not** generate `implementation-roadmap.md`, plan files, tickets, milestones, ordered delivery stages, or code. This skill stops at the research library.
