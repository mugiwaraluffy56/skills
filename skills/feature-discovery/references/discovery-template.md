# Feature discovery dossier template

Default location: `docs/features/<slug>/discovery.md`, but prefer an existing project task/spec location. This is a **template**, not a second tracker.

## Source and outcome

- Task ID, requested outcome, dated references, repo(s), branch/revision, author/actor.
- User journey: entry, setup, main result, repeat/change/stop, failure/recovery.
- What code already does vs what product documentation proposes (paths and status).
- Relevant published contract(s), owner of state/effects, relevant service/repo boundary.

## Capability / compatibility matrix

| ID | User-relevant capability / variant | Official support + version/date/URL | Open-source comparator + specific file/test path | Existing implementation + status | Essential / recommended / excluded | Acceptance ID | Rationale |
|---|---|---|---|---|---|---|---|
| C-01 | Example | supported / conditional / unsupported / unknown | URL+commit+file | source path or absent | essential | F-01 | why |

Do not confuse a provider's input context window, maximum generated output, business budget and request size. For other domains, specify comparable units precisely.

## Constraints register

| ID | Limit/default/exclusion and units | Scope (per account/request/model/tenant/etc.) | Primary source or approved decision | Changeable? owner? | User-visible failure | Test |
|---|---|---|---|---|---|---|
| L-01 | TBD | TBD | URL / decision path | TBD | TBD | F-... |

No ungrounded hardcoded thresholds. `unknown` means unknown, not unlimited.

## Journey, failure and recovery matrix

| Case | Actor/state | Trigger | Expected authoritative result | User-visible result | Retry/recovery | Verification boundary |
|---|---|---|---|---|---|---|
| J-01 | eligible | success path | persisted/observed | correct status | refresh safe | unit+integration+UI if applicable |
| J-02 | unauthorized | protected action | no effect | denied | safe return | negative authorization |
| J-03 | uncertain external effect | lost response | reconcile exact operation | pending/unknown | do not blind replay | fault injection |

## Acceptance criteria

For each F-XX:

- **Given** real prior state and permission...
- **When** user/caller performs action...
- **Then** observable result/state is...
- **And** relevant negative/boundary behavior is...
- **Owner + seam** source files/services and unit/integration/rendered/live evidence needed.

## Scope and readiness

- Essential now (every item maps to accepted F-XX):
- Recommended next (explicitly not in scope):
- Excluded (explain why not relevant/allowed/feasible):
- Backward compatibility, operational risks, data migration:
- Unknowns and decisions (clearly identify consequence):
- Verdict: `READY` / `NOT READY` with rationale.
