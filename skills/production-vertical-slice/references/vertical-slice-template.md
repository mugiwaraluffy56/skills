# Feature vertical-slice ledger

Append this to the project's **existing** accepted implementation plan/task. Do not create duplicate tracking systems.

## Baseline

- Task and acceptance/spec references:
- Repo(s), base/head revision(s), checked status:
- Existing user journeys and published interfaces to preserve:
- Compatibility prerequisites (version, API, migrations, runtime config):

## Slice S-01 — a complete observable result

| Stage | Authority or actual component | Concrete paths or contract | Failure/recovery | Evidence/test |
|---|---|---|---|---|
| Entry and actor | UI/API/CLI | | | |
| Authorization and input | server / policy | | | |
| State and side effects | store/worker/external system | | | |
| Response/progress | transport + event | | | |
| Presentation | UI/CLI/client | | | |
| Reconnect/cancel/upgrade | relevant boundary | | | |

Accepted requirement IDs:

Constraints and their official/policy provenance:

Live-service/multi-repo dependencies and release gating:

## Acceptance crosswalk

| ID | Real code paths | Tests and meaningful assertion | Observed result | Env + revision | Evidence level | Remaining blocker |
|---|---|---|---|---|---|---|
| F-01 | | | | | | |

## Changed-state truth table

| Initial state | Event | Required permission | Authoritative state after event | Public representation | Recovery test |
|---|---|---|---|---|---|
| ready | start | permitted | durable pending | accepted (not completed) | real API+state |
| pending | remote timeout | permitted | unknown until reconciled | actionable unknown | no blind retry |
| running | stop | permitted | stop requested then contained | separate states | cancellation race |
