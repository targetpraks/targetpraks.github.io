---
title: Infinity Brands — ClickUp implementation (deep build)
status: enhanced-proposal
version: 2.0-master
supersedes: 2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html
based_on_commit: c5a4b252
enhanced: 2026-11-03
owner: Bruce Wayne
---

# ClickUp: the deep build (entity model, schema, automations, migration)

## What this version fixes

- The deep build specifies 28 custom fields and 26 automation rules. The build edition (`clickup-build-v3.md`) specifies 16 fields and 12 automations, with an explicit cut list. **The build edition governs the build set.** This document keeps the deep build's extra fields and rules as conditional scope, each tagged `conditional` or `superseded`, and names the conflict rather than averaging it. Cited: build edition lines 80–81 and 640–650 (`2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html:80-81`, `2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html:640-650`); deep build automations at `2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:8480`.
- The deep build's field register (28 fields) is adopted as the implementation detail behind the build edition's 16-field core; finance, approval and agent fields (F_OBLIGATION_TYPE … F_HUMAN_APPROVED) are `conditional` on their feature being approved, not part of the core 16.
- The earlier implementation pass (`2026-10-29-infinity-brands-clickup-implementation-prd.html`, 2143 lines) is the v1.0 baseline; this document supersedes it. Differences are not re-litigated here.
- No workspace exists. Everything below is specification.
- The earlier 2,143-line implementation pass is superseded by this document; the `-2` duplicates were diffed and their content delta is formatting and summary callouts only, not requirements.

## Product in five lines

1. What it is: the deep build — entity model, field-by-field schema, 26-rule automation manifest (12 in the build set), routing table, store-opening stage model, finance completeness algorithm, and migration order.
2. Who uses it: the builder and the QA agent; Ricardo approves the open decisions.
3. Decision/action it enables: a builder can implement without guessing field types, statuses, routing, or automation triggers.
4. Deliberately not: a replacement for the register or the build edition; it conforms to them and flags conflicts.
5. The number that says it works: the Store Completeness Index and the finance completeness algorithm run against the 16-field (plus conditional) schema without a missing key.

## Status ledger

| Capability | State | Evidence | Gap |
|---|---|---|---|
| Entity model (Workspace→Space→Folder→List→Task) | partial | Deep build §23 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:2511`) | Not implemented |
| Field register (28 fields) | partial | Deep build §24 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:3161`) | 16 in build set; 12 conditional |
| Status model and transition matrix | partial | Deep build §25 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:3825`) | Not implemented |
| Permissions / RACI matrix | partial | Deep build §26 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:4896`) | Not implemented |
| Intake routes and forms | partial | Deep build §27 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:5678`) | 3 forms in build set, not 4 |
| Finance recurrence + Store Completeness Index | partial | Deep build §28 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:6574`) | Depends on finance fields |
| Reporting / dashboards / metric dictionary | partial | Deep build §29 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:7574`) | 4 dashboards in build set |
| Automation manifest (26 rules) | partial | Deep build §30 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:8442`) | 12 in build set; 14 conditional/superseded |
| Commercial model (40 users) | partial | Deep build §31 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:9208`) | Pricing UNVERIFIED — no API access |
| Test harness + runbook | partial | Deep build §32 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:9773`) | 14 tests in build set, not 112 |
| Contradictions ledger | partial | Deep build §33.3 (`2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html:10440`) | Carried into this document |

## Domain model

Entities with one-line purpose (deep build §23):
- **Workspace**: single tenant; billing unit.
- **Space**: accountable function (11).
- **Folder**: brand / client / store / year / quarter grouping.
- **List**: work container; carries tasks and views.
- **Task**: one piece of work, one home Space.
- **Field**: 16 core + up to 12 conditional; see schema below.
- **Status**: per-workflow contract; see transition matrix.
- **Automation**: 12 build-set rules (+14 conditional).
- **Goal / Task Target**: OKR cascade.
- **Doc**: meeting minutes, decisions, SOPs, SLA reports.
- **Dashboard**: 4, one card per question.
- **Team**: 10 on Business.
- **Template**: 7 document templates.

Tables that carry them (columns that matter):
- `spaces.csv`: id, name, prefix, accountable, shape.
- `fields.csv`: id, display name, type, applies-to, required, options, edit rights, consumed by.
- `views.csv`: name, filter, sort, scope (5 standard).
- `automations.csv`: id, trigger, condition, action.
- `goals.csv`: level, owner, check-in.
- `tests.csv`: id, area, expected value.
- `migration.csv`: source, what moves, what does not, owner.

Indexes that decide performance: (1) task by assignee+status; (2) task by Brand+Work Type+Quarter; (3) Goal/Task Target by owner.

Numbered invariants (carried from the register, I1–I8) plus implementation invariants:
- I9: Status transitions follow the per-workflow contract; illegal transitions are blocked and logged.
- I10: Finance completeness requires the full key set (obligation type, amount, period key, paid date, expiry, completeness flag); a missing key fails the algorithm, it does not skip.
- I11: Store-opening work advances only when the stage checklist register is satisfied.
- I12: Agent-raised tasks land in Intake Drafts (sandbox) and cannot reach a real List without a human approval gate.

## Field-by-field schema (core 16)

The build edition's 16-field core, in creation order:

| ID | Display name | Type | Applies to | Required | Notes |
|---|---|---|---|---|---|
| F_BRAND | Brand | Dropdown | All tasks | Yes | Brand register |
| F_BU | Business unit | Dropdown | All tasks | Yes | BU1–BU6, BO1, BO2, FXS; set on intake |
| F_FUNCTION | Function | Dropdown | All tasks | Yes | 143-type taxonomy, versioned |
| F_QUARTER | Quarter | Text/Dropdown | All tasks | Yes | Naming rule: quarter lives in Folder + name |
| F_WORK_TYPE | Work-Type | Dropdown | All tasks | Yes | Briefed-In, Daily, Recurring, Reporting, Projects/Ad-hoc, Meeting Action |
| F_PRIORITY | Priority Level | Dropdown | All tasks | Yes | High, Medium, Urgent |
| F_FREQUENCY | Frequency | Dropdown | All tasks | Yes | Once Off, Monthly, Weekly |
| F_CLIENT_BRAND | Client / Brand | Dropdown | All tasks | Yes | 14 brands |
| F_ENGAGEMENT_TIER | Engagement Tier | Dropdown | All tasks | Yes | HOF, ZOR, COR, ZEE |
| F_SERVICE_TIER | Service Tier | Dropdown | Service tasks | Yes | Gold, Black, Silver |
| F_DUE | Due date/time | Date | All tasks | Yes | ISO YYYY-MM-DDTHH:MM |
| F_OWNER | Owner / functional owner | User | All tasks | Yes | Workspace user |
| F_REQUESTED_BY | Requested by | Text/User | All tasks | Yes | Audit |
| F_RESPONSE_DUE | Response Due | Date | Service tasks | Yes | First response clock |
| F_RESOLUTION_DUE | Resolution Due | Date | Service tasks | Yes | Resolution clock |
| F_FIRST_RESPONSE_AT | First Response At | Date | Service tasks | No | Set by R-08-04 |

## Conditional fields (deep build only, not in the core 16)

| ID | Display name | Type | Condition to include |
|---|---|---|---|
| F_STORE | Store / Location | Dropdown | Store-opening work in scope |
| F_RACI_R/A/C/I | RACI roles | Text | RACI reporting approved (D6) |
| F_OBLIGATION_TYPE | Obligation type | Dropdown | Finance completeness in scope |
| F_AMOUNT | Amount | Currency | Finance completeness in scope |
| F_PERIOD_KEY | Period key | Text | Finance completeness in scope |
| F_PAID_DATE | Paid date | Date | Finance completeness in scope |
| F_EXPIRY_DATE | Expiry date | Date | Certificate/licence tasks in scope |
| F_COMPLETE | Completeness flag | Checkbox | Finance completeness in scope |
| F_APPROVAL_STATE | Approval state | Dropdown | Creative approval workflow in scope |
| F_APPROVER | Approver | User | Creative approval workflow in scope |
| F_AGENT_RUN_ID | Agent run ID | Text | Agent contract in scope |
| F_AGENT_CONFIDENCE | Agent confidence | Number | Agent contract in scope |
| F_HUMAN_APPROVED | Human-approved flag | Checkbox | Agent contract in scope |

Conflict named: the deep build ships all 28 as core; the build edition ships 16. Adopting 28 without the finance/approval/agent features being approved inflates the schema and the setup cost. Resolution is D6.

## Automations (build set = 12, deep build = 26)

The two documents do not share a rule register. The build edition ships `automations.csv` with 12 rules `A01–A12`; the deep build ships 26 rules `R-08-01–R-08-26`. Only seven deep-build rules have a direct conceptual counterpart in the build set. The build edition is later and governs; the deep build's rules are `superseded` unless their feature is separately approved.

**Build set (verified: 12 data rows in `AI-Drive/Agent-Output/batman/clickup-prd-v3-1/config/automations.csv`):**

| Rule | Trigger | Condition | Action | Deep-build counterpart |
|---|---|---|---|---|
| A01 | Task created | Recurring, Frequency empty | Comment asking for Frequency | none |
| A02 | Task created | Service Tier set | Set Response Due | R-08-03 |
| A03 | Status becomes Delivered | First Response At empty | Stamp First Response At | R-08-04 |
| A04 | Date reached | Recurring task due today | Create next occurrence | none (deep build §28.2 rule) |
| A05 | Form submitted | Any | Create task in 00 Requests, Source=Form | R-08-01, R-08-02 |
| A06 | Chat message flagged | Any | Create task with message linked | none |
| A07 | Task overdue two days | Priority High or Urgent | Notify owner and lead | R-08-05, R-08-08 |
| A08 | Goal pace below plan | Progress behind quarter | Post to team Channel | none |
| A09 | Meeting Doc created | Any | Create action tasks from action lines | none |
| A10 | Bulk change or import | Any | Write a line to the Configuration Register | none |
| A11 | Guest added to a Folder | Any | Notify account owner | none |
| A12 | Weekly, Monday 06:00 | — | Post team agenda to Channel | R-08-23 (closest) |

**Deep-build rules not in the build set:** R-08-06, R-08-07, R-08-09 to R-08-22, R-08-24 to R-08-26 — 19 rules, `superseded` unless their feature is approved (finance completeness, creative approval, agent contract, store openings, expiry tracking, budget monitor). Adopting them without the feature recreates the 26-rule sprawl the build edition cut.

Conflict named: a rule ID from the deep build cannot be imported into the build set. `automations.csv` is the only rule register for the build; the deep build's R-IDs are reference material, not deployable rules.

## The engine — status machine and finance arithmetic

**States** (per workflow, deep build §25): `Intake → Accepted → In Design → In Review → Approved → Production → Published` for creative; `Intake → Accepted → In Progress → Waiting → Resolved → Verified → Closed` for service; `Planned → In Progress → Evidence Due → Verified → Closed` for finance controls. `Cancelled` is terminal from any non-terminal state.

**Transitions that must be blocked**: a task cannot move to `Approved` without an approver and a current asset version; cannot move to `Verified` with `Verification Result = Pending`; cannot move to `Published` without an approval; cannot move to `Closed` with an open dependency. Illegal transitions are refused and logged (I9).

**Pure function at the core** — finance completeness:

```
finance_completeness(period_key, obligations, evidence) -> {expected, actual, missing[], duplicates[], late[], score}
```

Inputs: `period_key` (`YYYY-MM`), the obligation register rows active for that key, and evidence rows (task + document URL + paid date). Outputs: counts and a score in `[0,1]`. The function is pure: same inputs, same score; no clock, no network.

**Edge cases, each with an expected value**:
- Empty set: `expected = 0` → `score = 1` and `missing = []` (an empty month is complete, not a failure).
- Duplicate key: two evidence rows for one obligation → `duplicates` contains the key, `score` is reduced by one count, never silently deduplicated.
- Stale version: evidence submitted against a superseded obligation version → counted as `late`, not `missing`.
- Withdrawal: obligation cancelled mid-period → excluded from `expected`; its evidence is ignored.
- Exhaustion: all obligations verified → `score = 1`, `missing = []`.
- Self-approval: approver = requester → transition refused; the function does not accept the evidence.
- Concurrency: two approvers act on the same task version → the second write is rejected on version mismatch, not merged.

## Feature table

Implementation features (deep-build scope) that realise the register and build set:

| ID | Feature | Priority | Why it matters | Acceptance test (expected value) |
|---|---|---|---|---|
| F31 | Entity model Workspace→Space→Folder→List→Task | P0 | Builder needs one canonical hierarchy | 5 levels documented with ownership |
| F32 | Field-by-field schema (16 core + 12 conditional) | P0 | Two builders must not create different field sets | 16 core fields + conditional table present |
| F33 | Status model and transition matrix | P0 | Illegal transitions must be blocked | Per-workflow contracts + matrix loaded |
| F34 | Permissions and RACI matrix | P0 | Information boundaries enforced | Access matrix × role complete |
| F35 | Intake routes and forms (3 forms, not 4) | P0 | One request door per function | 3 forms × questions × routing |
| F36 | Finance recurrence + Store Completeness Index | P1 | Finance completeness measurable | SCI computes from the key set |
| F37 | Reporting, dashboards and metric dictionary | P1 | One card per question | 4 dashboards × metric definitions |
| F38 | Automation manifest (12 build-set + 14 conditional) | P0 | Rules counted and capped | 12 adopted, mapping table present |
| F39 | Commercial model (40 users) | P1 | Cost arithmetic before payment | 40-user scenario costed |
| F40 | Test harness and implementation runbook | P1 | Repeatable build and review | 14 tests + runbook steps |
| F41 | Contradictions ledger carried forward | P0 | Conflicts named, not averaged | Ledger present with resolution |
| F42 | Migration order Zoho → ClickUp | P0 | Installations die at import | 4 stages with exit tests |
| F43 | Conditional adoption table for dropped automations | P1 | Prevents silent rule loss | 14 rules tagged conditional/superseded |
| F44 | Agent contract with human gate | P2 | Unreviewed work cannot ship | Sandbox + approval gate enforced |
| F45 | Store-opening stage model | P2 | Premature openings blocked | Stage advances only on checklist |

## Architecture and API surface

Deep build §16 and §30: ClickUp REST v2, OAuth for humans, token for the agent service account, least privilege, idempotency via resolve-or-create by name, pagination via page/limit, versioning via the v2 prefix. No write is performed by this document. Setup runner: `AI Hub/saas-setup/clickup_setup.py` (dry-run supported).

## Failure modes

| Failure | What the user sees | Control | Who checks it |
|---|---|---|---|
| Schema inflation (28 fields as core) | Setup cost and confusion | Core 16 + conditional; D6 | Ricardo |
| Automation sprawl (26 rules) | Rules that break | 12 build-set; conditional adoption | Bruce Wayne |
| Illegal status transition | Work stuck or skipped | I9; transition matrix | QA agent |
| Finance completeness with missing key | Silent gap in reporting | I10; algorithm fails loud | Finance lead |
| Store stage advances early | Premature opening | I11; checklist gate | Express Ops |
| Agent task reaches a real List | Unreviewed work shipped | I12; sandbox + human gate | Human reviewer |

## Security, permissions and the audit record

Principals and matrix as in the register. Implementation-specific: agent service account holds only resolve-or-create scopes, no delete; R-08-21/22 require a human approval gate before a draft leaves Intake Drafts; approval actors are checked by user ID (deep build §27 notes a native guard gap — flagged as a defect to fix before build).

## Build order by dependency

Stage 1 — Schema lock (no writes):
- Decide D6 (field set) and D7 (automation adoption) and the deep-build open questions carried below.
- Exit: core 16 fields and 12 automations are named; conditional set is explicit.

Stage 2 — Provision (parallel, no data):
- Create Workspace, Teams, Spaces, Folders, Lists, 16 fields, 5 views per Space.
- Exit: field register matches §Field-by-field schema; views present.

Stage 3 — Behaviour (parallel):
- 12 automations, status contracts, 4 dashboards, 7 templates.
- Exit: automation manifest = 12; transition matrix loaded.

Stage 4 — Migration (sequential):
- Zoho export → spreadsheet importer into existing Lists → dual run one cycle.
- Exit: import report reviewed; no field lost.

Stage 5 — Conditional features (only if approved):
- Finance completeness, approval workflow, agent contract, store openings, expiry tracking.
- Exit: each conditional feature's tests pass independently.

## Decisions register

| # | Question | Recommended answer | Cost of each alternative |
|---|---|---|---|
| D6 | Core 16 fields or full 28? | Core 16; add conditional fields only when their feature is approved | 28 up front inflates setup cost and scope |
| D7 | Adopt which of the 14 non-build automations? | Adopt only those whose feature is approved (table above) | Adopting all 26 recreates the sprawl the build edition cut |
| D8 | Creative approval workflow in v1? | Defer to v2 unless a named approver is assigned | Adds 4 rules and 2 fields with no owner |
| D9 | Agent contract in v1? | Defer; the guard gap (§27) must be fixed first | Unreviewed agent tasks reach real Lists |
| D10 | Store-opening module in v1? | Include only if store openings are scheduled this year | Adds 1 rule and 1 field with no consumer |

## Evidence appendix

Commands run (outputs in `facts/clickup.md`):
- `git rev-parse --short HEAD` → `c5a4b252`
- `wc -l` on the six source HTML files
- `env | grep -i clickup` → no match
- `grep -n "R-08-" 2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html` → 26 rules listed
- `sed` extraction of the field register (lines 3157–3450)

Files read:
- `2026-11-01-infinity-brands-clickup-implementation-prd-v2-0-deep-build.html` (10532 lines)
- `2026-10-29-infinity-brands-clickup-implementation-prd.html` (2143 lines)
- `2026-11-02-infinity-brands-clickup-prd-v3-1-build-edition.html` (786 lines)
- `2026-11-02-infinity-brands-clickup-requirements-prd-v3-0.html` (1656 lines)
- `PRD-STRENGTH-STANDARD.md` (106 lines)
- `briefs/clickup-stack.md` (37 lines)
path">
/Volumes/Hiksemi 1TB/DevMini/targetpraks.github.io/prd-src/clickup-implementation-v2.md