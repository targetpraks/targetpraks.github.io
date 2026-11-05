---
title: Infinity Brands — ClickUp requirements register (governing)
status: enhanced-proposal
version: 3.0-master
supersedes: 2026-11-02-infinity-brands-clickup-requirements-prd-v3-0.html
based_on_commit: c5a4b252
enhanced: 2026-11-03
owner: Bruce Wayne
---

# ClickUp: the governing requirements register

## What this version fixes

- The requirements baseline (`2026-11-02-...-requirements-prd-v3-0.html`) and the build edition (`2026-11-02-...-prd-v3-1-build-edition.html`) disagree on counts: 26 automation rules vs 12, 112 indexed tests vs 14, 4 forms vs 3. The build edition is the later document and publishes an explicit cut list, so **the build edition governs configuration counts**; the requirements baseline governs requirement intent. Cited: requirements baseline line 1287 (`2026-11-02-infinity-brands-clickup-requirements-prd-v3-0.html:1287`); build edition lines 80–81 and 640–650 (`2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html:80-81`, `2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html:640-650`).
- R11 in the requirements baseline ends mid-sentence ("documents that capture a…"). The build edition names it as an open item and refuses to invent scope. This register keeps R11 open and does not fabricate content.
- The deep build (`2026-11-01-...-implementation-prd-v2-0-deep-build.html`) assumes 28 custom fields and 26 automations. The build edition cuts automations to 12 and fields to 16. Where the deep build names a field or rule that the build edition drops, the build edition wins and the deep build must say so (see `clickup-implementation-v2.md`).
- No ClickUp account or trial exists. Every workspace claim below is `absent` or `UNVERIFIED — no API access`. Nothing has been purchased or configured.
- The near-duplicate `-2.html` pairs were diffed. Requirements `-2` is 1,356 lines against 1,656; the content delta is formatting and a `[!summary]` callout only. Build-edition `-2` is 711 lines against 786, same result. The longer file is the record; both agree on every requirement, field, automation and test.

## Product in five lines

1. What it is: a single ClickUp workspace that replaces Zoho Projects, Cliq and Coda for Infinity Brands, organised by function (Space) with brand, work type and quarter as fields.
2. Who uses it: ~40 humans across ten functional teams, plus guests per client.
3. Decision/action it enables: one answer to "what is outstanding for this person / brand / quarter" without opening three tools.
4. Deliberately not: a CRM, a sprint/whiteboard tool, a per-brand workspace, or a Cliq history importer.
5. The number that says it works: the proof cohort moves the majority of its new work into ClickUp by day 30 of the pilot (kill criterion in `clickup-build-v3.md` §8).

## Status ledger

| Capability | State | Evidence | Gap |
|---|---|---|---|
| ClickUp workspace exists | absent | `agent-keys.env` has no `CLICKUP_*` key; process env has none | No account or trial exists |
| Spaces (11) | absent | UNVERIFIED — no API access | None created |
| Folders / Lists | absent | UNVERIFIED — no API access | None created |
| Custom fields (16) | absent | UNVERIFIED — no API access | None created |
| Statuses | absent | UNVERIFIED — no API access | None defined |
| Views (5 per Space) | absent | UNVERIFIED — no API access | None created |
| Automations (12) | absent | UNVERIFIED — no API access | None created |
| Goals / OKRs (Space 10) | absent | UNVERIFIED — no API access | None created |
| Meetings & Minutes (Space 11) | absent | UNVERIFIED — no API access | None created |
| Chat pilot | absent | UNVERIFIED — no API access | Wave two only |
| Dashboards (4) | absent | UNVERIFIED — no API access | None created |
| Spreadsheet importer route | partial | Build edition §7 states importer takes Excel/CSV/JSON/TSV/TXT into an existing List | Not exercised; no data exported yet |
| Requirements register (this doc) | implemented | `prd-src/clickup-requirements-v3.md` (this file) | — |
| Configuration pack (7 CSVs) | implemented | 7 files under `AI-Drive/Agent-Output/batman/clickup-prd-v3-1/config/`; data rows 11/16/5/12/6/14/6; `ls .../config/` → 7 CSVs present; `2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html:768-769` | Not committed to the repo; not applied to a workspace |

## Domain model

Entities (one-line purpose):
- **Workspace**: the single tenant; billing unit; holds all Spaces.
- **Space**: accountable function; one owner; never a brand.
- **Folder**: brand, client, store or year/quarter grouping inside a Space.
- **List**: the work container inside a Folder; carries tasks.
- **Task**: one piece of work with one home (Space); never duplicated across Spaces.
- **Field**: Brand, Work Type, Function, Quarter etc.; a field cannot steal a task from its function.
- **View**: one of five standard views, identical in every Space.
- **Automation**: a rule with trigger + condition + action; counted and capped.
- **Goal**: company/team objective; Task Target ties it to real work.
- **Doc**: meeting minutes, decisions, SOPs; one home per template.
- **Dashboard**: one card per question; four in total.
- **Team**: reporting group; ten on Business, permission-sharing only on Business Plus.
- **Template**: one of seven document templates with a named home and owner.

Tables that carry them (columns that matter):
- `spaces.csv`: id, name, prefix, accountable, shape.
- `fields.csv`: name, type, required-where, values, creation order.
- `views.csv`: name, filter, sort, scope.
- `automations.csv`: id, trigger, condition, action, why.
- `goals.csv`: level, owner, check-in cadence.
- `tests.csv`: id, area, expected value.
- `migration.csv`: source, what moves, what does not, owner.

Indexes that decide performance: (1) task lookup by assignee + status; (2) task lookup by Brand + Work Type + Quarter; (3) Goal/Task Target join by owner.

Numbered invariants:
- I1: One Workspace per tenant. Per-brand workspaces multiply seats and break cross-brand reporting.
- I2: A task has exactly one home Space; brand/work type/quarter are fields, never Folders that relocate the task.
- I3: Space = function, Folder = brand/client/store/year. Never the reverse.
- I4: Sub-teams are reporting groups only, never permission boundaries, on Business.
- I5: Ten Teams maximum on Business; step up to Business Plus only on a named trigger.
- I6: Chat is wave two; Cliq stays read-only until export for legal/HR is signed off.
- I7: Nothing is deleted in any source system during migration; both run one full cycle.
- I8: Every rollup gets a named mechanism (dashboard card, automation-written field, or agent-computed field) before build.

## Feature table

| ID | Feature | Priority | Why it matters | Acceptance test (expected value) |
|---|---|---|---|---|
| F1 | One workspace per tenant (not per brand) | P0 | Per-brand tenancy multiplies seats and breaks cross-brand reporting | Workspace count = 1 |
| F2 | Ten Teams as the function layer | P0 | Business ceiling; sub-teams are reporting groups only | Teams count = 10 on Business |
| F3 | Eleven Spaces, function-owned | P0 | Space = accountable function | Spaces count = 11 with named owners |
| F4 | Five standard views in every Space | P1 | Predictability over cleverness | Views per Space = 5, names identical |
| F5 | Sixteen fields in creation order | P0 | Fields run structure and service clocks | Fields count = 16 |
| F6 | Brand / Work Type / Function / Quarter as the four structural fields | P0 | A field cannot steal a task from its function | All four present and required where stated |
| F7 | Service clock fields (tier, response due, resolution due, first response at) | P0 | SLA reporting needs timestamps | 4 clock fields present |
| F8 | Goals & OKRs Space (Space 10) with year/quarter Folders | P1 | Company → team → individual cascade | Goal Folders = 1 per year + 1 per quarter |
| F9 | Task Targets instead of individual Goals | P1 | A personal Goal not tied to a task is self-assessment | Individual-level object = Task Target |
| F10 | Meetings & Minutes Space (Space 11), private | P1 | Minutes are the most sensitive routine document | Space 11 visibility = private |
| F11 | AI Notetaker writes a Doc per meeting | P2 | Makes the archive self-filing | One Doc per meeting created automatically |
| F12 | Chat pilot in wave two, two groups, task-created bar | P2 | Cheap to try, expensive to get wrong | Tasks created from messages is the measured bar |
| F13 | Client Folders in Space 08 with guest sharing | P1 | Client delivery isolation without a new workspace | One Folder per client, guest access scoped |
| F14 | Guest rule: same-domain accounts are members, never guests | P0 | Prevents silent seat spend | A company-domain address resolves to member |
| F15 | Spreadsheet importer migration route | P0 | Verified capability; no Zoho importer exists | Import into existing List succeeds with report |
| F16 | Dual run one full cycle, then freeze | P0 | Missed recurrences surface before trust | Both systems run ≥ one cycle before freeze |
| F17 | Seven document templates with named homes | P2 | No one asks where a document goes | 7 templates × named home × owner |
| F18 | Four dashboards, one card per question | P1 | EXCO / MANCO / team / OKR visibility | Dashboards count = 4 |

## Architecture and API surface

Configuration pack (machine-readable, beside this document): `spaces.csv`, `fields.csv`, `views.csv`, `automations.csv`, `goals.csv`, `tests.csv`, `migration.csv` — 7 files, row counts 11/16/5/12/6/14/6.

ClickUp REST API v2 (`https://api.clickup.com/api/v2`) is the only integration surface. Principals: human members (OAuth), agent service account (token, least privilege), guest (view or permission-controlled, billed beyond allowance). Conventions: pagination via `page`/`limit`; idempotency via resolve-or-create by name, never by id; versioning via the API v2 prefix. No write is performed by this register; the setup runner (`AI Hub/saas-setup/clickup_setup.py`) exists but is not run here.

## Failure modes

| Failure | What the user sees | Control | Who checks it |
|---|---|---|---|
| Per-brand workspace creep | Seat count multiplies, cross-brand reporting breaks | I1 invariant; one Workspace | Ricardo (money) |
| Task duplicated across Spaces | Same work counted twice | I2; one home Space | Function lead |
| Permission sharing assumed on Business | Access not granted | I4/I5; Business Plus triggers only | Ricardo |
| Chat pilot judged on messages | Feels busy, proves nothing | Measured on tasks created from messages | Bruce Wayne |
| Guest creep | Unplanned seat spend | Guest budget per client, monthly review | Finance |
| Comment/attachment loss on import | History gone | Accept in writing before import | Project lead |
| Formula illusions on rollups | Broken reporting | Named mechanism per rollup first | Doc owner |
| Two systems, one habit | People stay in Zoho | Dual run one cycle, then freeze | Ricardo |

## Security, permissions and the audit record

Principals: Ricardo (sponsor, money), function leads (accountable per Space), members (humans), guests (view or permission-controlled, billed beyond allowance), agent service account (least privilege, no delete). Role/action matrix: members create/edit tasks in their Space; guests view or permission-controlled per Folder; agents read/write only their scoped Lists; no principal deletes during migration (I7). Stored: tasks, fields, comments (lost on import — accepted in writing), attachments (lost on import — accepted in writing). Anchored outside the system: legal/HR Cliq export, Coda rollup mechanisms, the verification checklist before any payment. Signature/approval strength: ClickUp native approvals are a status, not a cryptographic signature; legal-grade evidence lives in the exported archives, not in ClickUp.

## Build order by dependency

Stage A — Resolve and decide (no writes):
- Ricardo answers the decisions register (plan tier, rollup mechanism, R11 scope, pilot funding, guest budget).
- Exit: every open decision has a recorded answer or an explicit deferral.

Stage B — Provision the skeleton (parallel, no data yet):
- Create the one Workspace, ten Teams, eleven Spaces, Folders, Lists, sixteen fields, five views per Space.
- Exit: F1–F7 acceptance tests pass against the live workspace.

Stage C — Content and behaviour (parallel):
- Goals/OKRs Space 10, Meetings Space 11, four dashboards, seven templates, twelve automations.
- Exit: F8–F12, F17–F18 pass.

Stage D — Migration (sequential, data-bearing):
- Export Zoho Projects to Excel; run spreadsheet importer into existing Lists; dual run one cycle.
- Exit: F15–F16 pass; import report reviewed; no field lost.

Stage E — Pilot and gate:
- Proof cohort (Finance daily control, Technology service desk) plus Visibility cohort (Leadership); thirty days; kill criterion.
- Exit: majority of new work in ClickUp by day 30, or stop and keep Zoho.

## Decisions register

| # | Question | Recommended answer | Cost of each alternative |
|---|---|---|---|
| D1 | Business at $17/seat or Business Plus at unpublished rate? | Start Business; step up only if a trigger in build edition §8 fires | Business Plus costs more with no use unless sub-team permission sharing, >10 Teams, >40 scheduled report sends, or Doc page protection are needed |
| D2 | What does each Coda rollup become? | Decide per rollup: dashboard card, automation-written field, or agent-computed field; never a formula | Leaving it to formulas breaks reporting silently |
| D3 | Does R11 ("documents that capture a…") get scope now? | No — keep open until Ricardo finishes the sentence | Inventing scope commits build to unknown work |
| D4 | Fund the pilot year? | Yes, only after Stage A decisions recorded | No pilot means no evidence for a second year |
| D5 | Guest budget per client? | Set a number and review monthly | Unlimited guests drift into seat spend |

## Evidence appendix

Commands run (outputs summarised in `facts/clickup.md`):
- `git rev-parse --short HEAD` → `c5a4b252`
- `wc -l` on the six source HTML files (counts in facts file)
- `env | grep -i clickup` → no match
- `grep -i clickup ~/.config/agent-keys.env` → no match

Files read:
- `2026-11-02-infinity-brands-clickup-requirements-prd-v3-0.html` (1656 lines)
- `2026-11-02-infinity-brands-clickup-requirements-prd-v3-0-2.html` (1356 lines)
- `2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html` (786 lines)
- `2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition-2.html` (711 lines)
- `2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html` (10532 lines)
- `2026-10-29-infinity-brands-clickup-implementation-prd.html` (2143 lines)
- `PRD-STRENGTH-STANDARD.md` (106 lines)
- `briefs/clickup-stack.md` (37 lines)
path">
/Volumes/Hiksemi 1TB/DevMini/targetpraks.github.io/prd-src/clickup-requirements-v3.md