# Adversarial acceptance report

Default: append to the existing project review/evidence record. Prefer the project's accepted tests and reviewer protocol.

## Context and provenance

- Original request / accepted criteria (direct links):
- Source baseline/head commits and observed running revision:
- Environment, test access and provider/service qualification:
- Actual reviewer/tester identities or **self-review** label:
- Date, test tools and known missing dependencies:

## Requirements crosswalk

| ID | Original user-observable expected result | Code/runtime path inspected | Observed behavior (not just intent) | Exact test command + meaningful assertion | Level of evidence | Verdict | Blocker |
|---|---|---|---|---|---|---|---|
| F-01 | | | | | | satisfied / partial / missing / contradicted / unverified | |

## Independent adversarial cases

| Scenario | Expected behavior | Test input / invocation | Actual result | Fixture or real service? | Source revision | Defect or qualification gap |
|---|---|---|---|---|---|---|
| Uncommon legitimate variant | | | | | | |
| Auth revoked during operation | | | | | | |
| Boundary around configured maximum | | | | | | |
| Lost acknowledgment and reconcile | | | | | | |

Only include cases relevant to this feature.

## Defects and disposition

- Scope defects (missing or unjustifiably narrowed requested capabilities):
- Implementation defects (incorrect effects/UI/security/reliability):
- Qualification gaps (missing real/live/operational verification):
- Fixes attempted and new test results:
- Remaining unverified claims and severity:

## Verdict

Select one: `NOT READY — SCOPE`, `NOT READY — IMPLEMENTATION`, `LOCALLY VERIFIED — LIVE PENDING`, `QUALIFIED FOR <ENVIRONMENT>`, `BLOCKED/UNVERIFIED`.

Describe exact qualified workload, platform, version and evidence. Green static checks never imply production readiness.
