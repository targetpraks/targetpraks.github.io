---
title: Infinity Brands — ClickUp build edition (under the register)
status: enhanced-proposal
version: 3.1-master
supersedes: 2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html
based_on_commit: c5a4b252
enhanced: 2026-11-03
owner: Bruce Wayne
---

# ClickUp: the build edition (under the register)

## What this version fixes

- The build edition is the later document and governs configuration counts (12 automations, 16 fields, 5 views, 14 tests). Where the requirements baseline or the deep build state a larger number, the larger number is the pre-cut design and is not the build. Cited: build edition lines 80–81 and 640–650 (`2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html:80-81`, `2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html:640-650`).
- The requirements baseline's R11 ("documents that capture a…") is carried forward as an open item, not filled. This document does not invent scope for it.
- The deep build's 26-rule automation manifest and 28-field register are superseded by the 12-rule / 16-field build set. Any deep-build reference to a dropped rule or field must be marked `superseded` (see `clickup-implementation-v2.md`).
- No workspace exists. Every item below is a specification, not a status report.
- The `-2.html` build-edition duplicate was diffed: 711 lines against 786; content delta is formatting and a summary callout only. The longer file is the record.

## Product in five lines

1. What it is: the executable build of the register — one Workspace, eleven Spaces, ten Teams, a seven-file configuration pack, a migration route off Zoho, and a thirty-day pilot with a kill criterion.
2. Who uses it: the proof cohort (Finance daily control, Technology service desk) plus the Visibility cohort (Leadership) in wave one; everyone else after.
3. Decision/action it enables: a build that can be run by a person or an agent without another meeting, with two blocking decisions left to Ricardo (plan tier, rollup mechanism) and three non-blocking owner questions.
4. Deliberately not: a second system run forever; the kill criterion stops funding if the proof cohort does not move.
5. The number that says it works: tasks created in ClickUp as a share of new work in the cohort's function reaches a majority by day 30.

## Status ledger

| Capability | State | Evidence | Gap |
|---|---|---|---|
| Configuration pack (7 CSVs) | implemented | 7 files under `AI-Drive/Agent-Output/batman/clickup-prd-v3-1/config/`; data rows 11/16/5/12/6/14/6; `ls .../config/` → 7 CSVs present; `2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html:768-769` | Not committed to the repo; not applied to a workspace |
| Workspace skeleton (1 Workspace, 10 Teams, 11 Spaces) | absent | UNVERIFIED — no API access | Stage B |
| Fields (16) | absent | UNVERIFIED — no API access | Stage B |
| Views (5 per Space) | absent | UNVERIFIED — no API access | Stage B |
| Automations (12) | absent | UNVERIFIED — no API access | Stage C |
| Goals / OKRs (6-goal skeleton) | absent | UNVERIFIED — no API access | Stage C |
| Meetings Space 11 + AI Notetaker | absent | UNVERIFIED — no API access | Stage C |
| Dashboards (4) | absent | UNVERIFIED — no API access | Stage C |
| Document templates (7) | absent | UNVERIFIED — no API access | Stage C |
| Migration (Zoho → ClickUp) | absent | Build edition §7 specifies spreadsheet importer route | Stage D, data-bearing |
| Pilot (30 days, 2 cohorts) | absent | Build edition §8 specifies cohorts and kill criterion | Stage E |
| Chat pilot (wave two) | absent | Build edition §6 | After Stage E |

## Domain model

Same entities as the register (`clickup-requirements-v3.md` §Domain model): Workspace, Space, Folder, List, Task, Field, View, Automation, Goal, Doc, Dashboard, Team, Template. This document adds the **configuration pack** as the build artifact: seven CSV files that are the single source a builder reads. No second schema is introduced; the deep build's entity model is adopted where it does not conflict with the build set, and conflicts are listed in `clickup-implementation-v2.md` §contradictions.

## Feature table

Build-stage deliverables (F19+) that realise the register's F1–F18:

| ID | Feature | Priority | Why it matters | Acceptance test (expected value) |
|---|---|---|---|---|
| F19 | Author the seven-file configuration pack | P0 | The whole build is a pack, not a rule book | 7 files present, row counts 11/16/5/12/6/14/6 |
| F20 | Lock the six decisions the register left open | P0 | Six were ours to answer; two remain Ricardo's | 6 decisions recorded with reasoning |
| F21 | Migration specification (Zoho Projects, Cliq, Coda) | P0 | Installations die at the import step | Route documented for all 3 sources with loss points named |
| F22 | Dual-run one full cycle before freeze | P0 | Missed recurrences surface in the old tool | Both systems run ≥ one cycle |
| F23 | Thirty-day pilot with proof + visibility cohorts | P0 | A build needs a way to fail | Cohorts named; kill criterion stated before start |
| F24 | Step-up triggers for Business Plus (4 named) | P1 | Prevents plan drift | 4 triggers listed; no step-up without one |
| F25 | Seven document templates with named homes | P2 | No one asks where a document goes | 7 templates × home × owner |
| F26 | Four dashboards, one card per question | P1 | EXCO/MANCO/team/OKR visibility | Dashboards count = 4 |
| F27 | Guest budget per client, monthly review | P1 | Prevents seat creep | Budget number set and reviewed monthly |
| F28 | Chat pilot measured on tasks created from messages | P2 | Messages prove nothing | Bar = tasks created from messages |
| F29 | Import into existing Lists, never fresh Lists | P0 | Reorganising after import loses fields | Import target = existing List |
| F30 | Comment/attachment loss accepted in writing before import | P0 | History loss must be consented | Written acceptance recorded |

## Architecture and API surface

Same as the register: ClickUp REST API v2, resolve-or-create by name, pagination, least-privilege service account. Build-specific conventions: (1) the configuration pack is the single source; (2) import runs into existing Lists; (3) no delete in any source system during migration; (4) both systems run one full cycle.

## Failure modes

| Failure | What the user sees | Control | Who checks it |
|---|---|---|---|
| Pack drifts from the build | Builder reads two truths | Pack is the single source; PRDs cite it | Bruce Wayne |
| Import into a fresh List | Fields lost in reorganisation | F29; import target rule | Project lead |
| Pilot judged on feelings | No evidence for year two | Measured bars in F23 | Ricardo |
| Business Plus drift | Cost with no use | F24 triggers | Ricardo |
| Rollup mechanism undecided | Broken reporting | D2 (decisions register) | Doc owner |
| Chat pilot judged on messages | False busy-ness | F28 bar | Bruce Wayne |

## Security, permissions and the audit record

Same principals and matrix as the register. Build-specific: the service account used by the setup runner holds only the scopes needed for resolve-or-create; no delete scope; migration runs read-only against Zoho exports. Legal/HR Cliq export must be signed off before Cliq goes read-only.

## Build order by dependency

Stage A — Resolve and decide (no writes):
- Record answers to D1–D5 (decisions register) plus the two Ricardo-only decisions (plan tier, rollup mechanism).
- Exit: every open decision has a recorded answer or explicit deferral; no `[open]` remains in the pack.

Stage B — Provision the skeleton (parallel, no data):
- Create the one Workspace, ten Teams, eleven Spaces, Folders, Lists, sixteen fields, five views per Space.
- Exit: F1–F7, F19 pass against the live workspace.

Stage C — Content and behaviour (parallel):
- Space 10 goals (6-goal skeleton), Space 11 meetings + AI Notetaker, four dashboards, seven templates, twelve automations.
- Exit: F8–F12, F17–F18, F25–F26 pass.

Stage D — Migration (sequential, data-bearing):
- Export Zoho Projects to Excel; run spreadsheet importer into existing Lists; dual run one full cycle.
- Exit: F15, F16, F21, F22, F29, F30 pass; import report reviewed.

Stage E — Pilot and gate:
- Proof + Visibility cohorts, thirty days, kill criterion.
- Exit: F23 passes (majority of new work in ClickUp by day 30) or stop and keep Zoho.

Stage F — Wave two (only if Stage E passes):
- Chat pilot in two groups; Cliq goes read-only after export sign-off.
- Exit: F12, F28 pass.

## Decisions register

| # | Question | Recommended answer | Cost of each alternative |
|---|---|---|---|
| D1 | Plan tier: Business ($17) or Business Plus (unpublished)? | Start Business; step up only on a named trigger (F24) | Business Plus costs more with no use absent a trigger |
| D2 | Rollup mechanism per Coda rollup? | Per rollup: dashboard card / automation-written field / agent-computed field | Formulas cannot do rollups; reporting breaks silently |
| D3 | R11 scope? | Keep open until Ricardo finishes the sentence | Inventing scope commits unknown work |
| D4 | Fund the pilot year? | Yes, after Stage A decisions recorded | No pilot = no evidence for year two |
| D5 | Guest budget per client? | Set a number, review monthly | Unlimited guests drift into seat spend |

## Evidence appendix

Commands run (outputs in `facts/clickup.md`):
- `git rev-parse --short HEAD` → `c5a4b252`
- `wc -l` on the six source HTML files
- `env | grep -i clickup` → no match (no API access)
- `grep -i clickup ~/.config/agent-keys.env` → no match

Files read:
- `2026-11-02-infinity-brands-clickup-requirements-prd-v3-0.html` (1656 lines)
- `2026-11-02-infinity-brands-clickup-requirements-prd-v3-0-2.html` (1356 lines)
- `2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html` (786 lines)
- `2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition-2.html` (711 lines)
- `2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html` (10532 lines)
- `2026-10-29-infinity-brands-clickup-implementation-prd.html` (2143 lines)
- `PRD-STRENGTH-STANDARD.md` (106 lines)
path">
/Volumes/Hiksemi 1TB/DevMini/targetpraks.github.io/prd-src/clickup-build-v3.md