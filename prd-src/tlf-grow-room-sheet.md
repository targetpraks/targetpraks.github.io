---
title: The Local Farmer — one grow room sheet, and the arithmetic that has to hold
status: enhanced-proposal
version: 2.0-master
supersedes: 2026-10-26-tlf-grow-room-master-one-sheet-prd.html (and its restyled twin tlf-grow-room-master-prd-2026-10.html)
based_on_commit: 11e6e11c
enhanced: 2026-11-03
owner: Bruce Wayne
---

# One grow room sheet (v2)

## What this version fixes

- The evidence line claims **2,910 sourced facts**. The file it cites holds **14,520 facts across 794 documents**
  (`wc -l AI-Drive/Agent-Output/batman/brand-knowledge/TLF/facts.all.jsonl`). The wrong number was never load-bearing,
  but it is the number a reader uses to judge everything else.
- The **−67.1 kg variance** is not reproducible. `17.3 × 4.33 − 17.04 = 57.9`, and `(67.1 + 17.04) ÷ 17.3 = 4.86`
  periods, so no printed input produces it. The dashboards' own variance cells sum to −41.93 kg and −48.21 kg.
- The machine rule prices **10 kg per machine per month**, which the same document's occupancy rule forbids: at 120 g
  and 95% the ceiling is **8.885 kg**. 10 kg needs 20.3 harvestable trays a period against 18 available, or 131 g a
  tray. The 24-month payback test then never binds — it reads 2.95 months either way.
- The two published grow-room files are **one document in two themes**, not two opinions: body identical after
  stripping `<style>` (14,332 characters each). They must not be revised separately.
- "Built and live, nine tabs" is stated but not evidenced here: Zoho Sheet was not queried in this pass. It is
  `unverified`, not `implemented`, in the ledger below.

## Product in five lines

1. **What it is:** one operating sheet for the grow room — capacity, client demand, the machine order decision,
   harvested yield and invoiced rand on one surface, with the arithmetic visible.
2. **Who uses it:** the TLF GM and the grower standing in the room; finance reads the invoice tab.
3. **Decision it enables:** sow this much, quote this client this start date, order or hold the next machine — each
   answer derived, not argued.
4. **Deliberately not:** an accounting system, a costing model, or a replacement for the harvest ledger, which stays
   the append-only log.
5. **The number that says it works:** the machines figure the plan prints matches an independent recomputation to the
   same integer on every row, and no tab prints a capacity number that was typed rather than computed.

## Status ledger

States used: `implemented` (proven by a command), `partial` (exists, incomplete), `absent` (proven missing),
`unverified` (not checked in this pass).

| Capability | State | Evidence | Gap |
|---|---|---|---|
| Six source workbooks exist and disagree | implemented | 794 documents / 14,520 facts in the TLF sweep; every workbook the source PRD names is present, 19 to 1,985 facts each | none — this is the problem being solved |
| Harvest ledger with 130 trays / 17.04 kg / 69.12 kg target | implemented | `harvest_ledger_snapshot.pdf` facts in the sweep; weekly rows 45/28/19/17/10/11 sum to 130 trays and 17.04 kg | ledger's capacity target is 2× the room (69.12 = 8.64 × 8 sessions) |
| Weekly capacity arithmetic (spaces × 7 ÷ cycle × g × reliability) | implemented | recomputed: 4→8.21, 5→10.26, 7→14.36, 8→16.42, 10→20.52 kg | correct, and contradicted by every other TLF document |
| Replacement sheet, nine tabs, filed in TLF_Reporting | unverified | UNVERIFIED — Zoho Sheet and WorkDrive were not queried in this pass | must be inspected tab by tab before any tab is trusted |
| Machines-needed calculator (kg/day → machines) | partial | four-row table in the source PRD; machine counts reproduce | spaces column rounds inconsistently; 246 trays printed as 491 spaces |
| Yield log against model | absent | no sheet artefact; ledger is a separate file | append-only log with g/tray, variance, failed trays |
| Invoice yield from Zoho Books | absent | source PRD reports Books refusal `6018` (UNVERIFIED here); invoice tab takes pastes | sell-through and realised R/kg are unmeasured |
| Retirement of the five model sheets | absent | nothing archived; no `_Retired` folder evidenced | five surfaces still disagree |
| Machine order rule as a stamped decision | absent | source PRD states the rule in prose only | needs a decision row with parameters frozen at the moment of the call |

## Domain model

| Entity | Purpose |
|---|---|
| Parameter | one named fact the whole sheet reads: cycle days, spaces per machine, yield, reliability, price |
| Machine | a physical unit with 36 spaces; capacity is a function of machine count, never a typed number |
| Batch | one sowing on one date into one machine: the unit the yield log counts |
| Harvest | trays taken from a batch on a date, with grams; the only source of actual yield |
| Client | a buyer, with channel and price basis |
| Order | a client's demand in one 7-day period, confirmed or prospect — the only place demand is entered |
| Invoice | grams sold and rand received, pasted from Books |
| Plan period | one 7-day row joining demand to capacity and naming the sowing and harvest |
| Machine decision | a dated verdict with the parameters that produced it |

Sheet tables that carry them, with the columns that decide correctness:

| Tab | Key columns (type) | Notes |
|---|---|---|
| Settings | `key` text PK · `value` decimal(12,4) · `unit` text · `changed_by` text · `changed_at` timestamp | one row per parameter, no duplicates; the only typed numbers in the workbook |
| Capacity | `machines` int PK · `spaces` int · `trays_7d` decimal(6,2) · `kg_7d` decimal(6,3) · `kg_day` decimal(6,3) · `kg_month` decimal(6,3) · `rand_month` decimal(10,2) | every cell except `machines` is a formula over Settings |
| Yield Log | `date` date · `machine` text · `trays_sown` int · `trays_harvested` int · `kg_harvested` decimal(7,3) · `failed_trays` int · `g_per_tray` decimal(6,2) | append-only; `g_per_tray = kg × 1000 ÷ trays_harvested` |
| Demand | `period` text (ISO 7-day key) · `client` text · `channel` text · `kg` decimal(7,2) · `price_kg` decimal(8,2) · `status` enum(Confirmed, Prospect) | unique on (`period`,`client`,`channel`) |
| Plan | `period` text PK · `demand_kg` · `capacity_kg` · `headroom_kg` · `pct_used` · `trays_to_sow` · `kg_to_harvest` · `verdict` enum | 13 rows, all formulas except the period key |
| Prospects | `client` · `kg_day` decimal(5,2) · `days_7d` int · `price_kg` · `kg_7d` · `trays_7d` · `spaces` · `machines` int · `servable_today` bool · `first_period` text | `days_7d` is the delivery-days answer that moves the machine count by two |
| Invoices | `invoice_no` text PK · `date` · `client` · `grams` int · `rand` decimal(10,2) · `source` text · `pasted_by` text | unique on `invoice_no`; `source` names paste or CSV and the file |
| Machine decision | `decided_at` timestamp · `peak_demand_kg` · `machines_needed` · `machines_held` · `shortfall` · `capital_rand` · `contribution_rand` · `payback_months` · `verdict` enum(ORDER, HOLD, NO) | stamped with the Settings snapshot used |

The three keys that decide whether the sheet holds together:

1. `Demand(period, client, channel)` — unique. A second row for the same client in the same period double-counts demand and can trigger a machine that is not needed.
2. `Invoices(invoice_no)` — unique. The paste lane is where duplicates enter, and a duplicated invoice inflates sell-through above 1.
3. `Yield Log(date, machine)` — the sort key every variance cell reads; unsorted, `g_per_tray` silently points at the wrong batch.

Invariants:

- **I1 Space-time.** For any 7-day window, `trays_harvested ≤ spaces × 7 ÷ cycle_days`. This is the invariant the 17.28 kg target breaks.
- **I2 One source.** Capacity is computed only from Settings. No tab may hold a typed capacity, yield or price.
- **I3 One rounding rule.** `trays = CEILING(kg × 1000 ÷ (yield_g × reliability))`; `spaces = trays × cycle_days ÷ 7`; `machines = CEILING(spaces ÷ spaces_per_machine)`, each rounded at its own step and printed rounded. No row may ceil one column and floor the next.
- **I4 Sell-through ≤ 1.** Invoiced grams in a period ≤ harvested grams in that period. A breach means harvest rows are missing, not that sales are extraordinary.
- **I5 Stamped decisions.** A machine verdict carries the Settings snapshot it used; changing yield later never rewrites a past decision.
- **I6 No divide by zero.** `g_per_tray` exists only where `trays_harvested > 0`.
- **I7 Append-only log.** A correction is a new row flagged as a correction; no historical row is edited.
- **I8 Reliability once.** 95% is applied at capacity. Actuals are actuals and carry no reliability factor.

## The engine, as a state machine with arithmetic

Tray states and transitions:

    SOWN ──► GROWING ──► HARVEST_READY ──► HARVESTED
              │                 │
              └────► FAILED ◄───┘        (contamination, mould, power loss)

- `SOWN → GROWING` on the sowing date; occupancy begins.
- `GROWING → HARVEST_READY` at `cycle_days` from sowing (10–14 days in practice).
- `HARVEST_READY → HARVESTED` on the harvest date, which writes one Yield Log row.
- Any state `→ FAILED` writes a `failed_trays` count and no grams. A failed tray consumes its space for the full cycle and yields nothing — the reason reliability is 95% and not 100%.

Pure functions at the core, with inputs and units:

    capacity(machines, spaces_per_machine, cycle_days, yield_g, reliability)
      trays_7d = machines × spaces_per_machine × 7 ÷ cycle_days      [tray-harvests per 7-day period]
      kg_7d    = trays_7d × yield_g × reliability ÷ 1000             [kg per 7-day period]

    machines_required(kg_7d, yield_g, reliability, cycle_days, spaces_per_machine)
      trays    = CEILING(kg_7d × 1000 ÷ (yield_g × reliability))     [trays]
      spaces   = trays × cycle_days ÷ 7                              [spaces]
      machines = CEILING(spaces ÷ spaces_per_machine)                [machines]

Worked, at Settings defaults (36 spaces, 14-day cycle, 120 g, 95%, 4.33 periods a month):

| Machines | Spaces | Trays/7d | kg/7d | kg/day | kg/month | R/month at R0.4504/g |
|---|---|---|---|---|---|---|
| 4 | 144 | 72 | 8.21 | 1.17 | 35.54 | 16,008 |
| 5 | 180 | 90 | 10.26 | 1.47 | 44.43 | 20,009 |
| 7 | 252 | 126 | 14.36 | 2.05 | 62.20 | 28,013 |
| 8 | 288 | 144 | 16.42 | 2.35 | 71.08 | 32,015 |
| 10 | 360 | 180 | 20.52 | 2.93 | 88.85 | 40,019 |

Edge cases, each with its rule:

| Case | Rule |
|---|---|
| `cycle_days ≠ 14` | everything derives from the parameter; 7 days doubles capacity, 21 days cuts it by a third |
| `cycle_days < 7` | more than one cycle is in flight per space; `trays_7d` exceeds `spaces`, which is legal, and I1 is rewritten as `trays_7d ≤ spaces × 7 ÷ cycle_days` |
| `yield_g = 0` or `reliability = 0` | capacity returns 0 and `machines_required` returns an error cell, never a divide-by-zero string |
| Empty demand | Plan prints 0 and `pct_used = 0`, and the verdict is HOLD with the shortfall stated |
| Demand exactly at 90% | the threshold is `>`, so 90.0% is HOLD. The sheet must print the gap to the threshold, not just the verdict |
| Duplicate (period, client, channel) | unique key rejects the second row; the sheet shows the existing row's address |
| Order withdrawn after sowing | the batch is not un-sown; the kg moves to the next period's headroom and the withdrawal is a note on the order row |
| Exhaustion (all spaces sown) | `trays_to_sow` clips to `spaces − occupied` and prints 0, never negative |
| Stale Settings between plan and harvest | I5 keeps the decision; the plan recomputes and prints the parameter version it used |
| Self-approval (grower writes yield and signs the machine decision) | role matrix forbids it; the decision tab records `decided_by` and refuses the same name as `logged_by` |
| Duplicate invoice | `invoice_no` unique; a repeated paste is rejected with the original row named |
| Harvest logged with 0 trays | I6 blocks `g_per_tray`; the row is still written so the failure is visible |

## Feature table

| ID | Feature | Priority | Why it matters | Acceptance test (expected value) |
|---|---|---|---|---|
| F1 | Settings tab as the single input block | P0 | Every other number derives from it; one place to change a fact | all 8 parameters present (cycle_days, spaces_per_machine, yield_g, reliability, price_kg, build_cost_rand, franchisee_price_rand, periods_per_month); changing `yield_g` from 120 to 150 moves the 4-machine kg/7d from 8.21 to 10.26 |
| F2 | Capacity table, machines 1–12 | P0 | The room's ceiling and the price of the next machine | 12 rows; machines=4 reads 8.21 kg/7d; machines=7 reads 14.36 |
| F3 | Capacity in rand at Settings price | P1 | Turns kilograms into the number a bank asks about | machines=4 at R0.4504/g reads R16,008/month (±R1) |
| F4 | One rounding rule across the workbook | P0 | The source table's 246 trays / 491 spaces row is a contradiction | for 4 kg/day × 7 days the sheet prints 246 trays, 492 spaces, 14 machines |
| F5 | Space-time guard (I1) | P0 | Blocks the 17.28 kg target from ever being entered as capacity | entering 17.28 kg/7d for 4 machines returns a violation naming 8.21 |
| F6 | Demand entry, one row per client per period | P0 | Duplicate rows invent demand and buy machines | second row for the same client and period is rejected, first row address shown |
| F7 | Confirmed vs prospect split | P0 | Machines bought on hope sit at 40% utilisation | Plan counts only `Confirmed`; a 14 kg prospect week shows 0 kg demand and a separate prospect line |
| F8 | 13-period rolling plan | P0 | Sowing now harvests later; the plan is the only place that link exists | 13 rows; period 1 `trays_to_sow` = CEILING(period 2 demand) with `kg_to_harvest` from the same batch |
| F9 | Headroom and percent-used per period | P1 | Shows how close the room is before it is full | 14 kg demand on 8.21 kg capacity prints headroom −5.79 and 170% |
| F10 | Machine verdict per period | P0 | The order decision must be one word with a reason | demand 8.0 kg against 8.21 capacity in two consecutive periods prints ORDER; 7.0 prints HOLD with gap 0.39 kg |
| F11 | Payback arithmetic at the real yield | P0 | 10 kg/month overstates contribution by 12% | contribution uses 8.885 kg/machine → R4,001.88, payback 3.32 months at R13,294 |
| F12 | Two price bases kept apart | P0 | R13,294 build cost and R45,000 franchisee price are a 3.38× spread | the tab prints both, labels which one the verdict used, and never mixes them in one cell |
| F13 | Prospects calculator (kg/day and delivery days in, machines out) | P0 | Answers a client in the meeting, with a start date | 2 kg/day 7 days → 7 machines; 2 kg/day weekdays → 5 machines |
| F14 | First servable period per prospect | P1 | A quote without a start date is a wish | prospect needing 7 machines against 4 held returns the period the 3rd machine's harvest lands |
| F15 | Yield Log append-only with variance | P0 | Actuals against model is the only feedback loop | a row with 18 trays and 2.2 kg reads 122.2 g/tray and variance +2.2 g against 120 |
| F16 | Failed-tray tracking | P1 | Reliability is a guess until failures are counted | 2 failed of 18 shows 11.1% failure and recomputes the period's realised reliability |
| F17 | Realised reliability feeding Settings | P2 | 95% should be measured, not assumed | after 4 periods the Settings suggestion reads the trailing average and never auto-applies |
| F18 | Invoice paste with provenance | P0 | Sell-through is the only check on what is earned per kg | pasted row records `source`, `pasted_by`, date; duplicate `invoice_no` rejected |
| F19 | Sell-through per period | P0 | Grams invoiced ÷ grams harvested | period with 1.8 kg invoiced and 2.2 kg harvested reads 81.8% |
| F20 | Realised price per kg | P0 | Rand ÷ harvested kg is the price actually obtained | 1.8 kg for R1,260 reads R700/kg |
| F21 | Sell-through > 1 alert | P1 | Impossible sell-through means missing harvest rows | 110% returns a flag naming the period and the likely missing harvest date |
| F22 | Cost of the next machine | P1 | Capital decision needs the marginal kg, not the average | machines 4→5 prints +2.05 kg/7d and +R4,001.88/month |
| F23 | Decision stamp with parameter snapshot | P0 | Yield changes must not rewrite history | decision row keeps the `yield_g` and `price_kg` used, readable after Settings change |
| F24 | Monthly CSV snapshot with a hash | P1 | The sheet is not a database; the snapshot is the record | CSV written to AI-Drive with a sha256 line; re-export of unchanged data matches the hash |
| F25 | Retirement notice inside the sheet | P2 | Five surfaces disagree because nobody is told which one counts | Start Here names the five superseded files, the archive folder, and the date of the move |

## Architecture and API surface

The system is one Zoho Sheet plus a monthly CSV snapshot. There is no service to build.

Package layout, and the one rule that keeps it honest:

    TLF_Reporting/TLF Grow Room Master      (the workbook; 9 tabs, in this order)
      1 Start Here        what it is, the eight parameters named, who owns it, what it excludes
      2 Settings          the input block — the only typed numbers
      3 Capacity          machines 1–12, formulas only
      4 Demand            one row per client per period
      5 Plan              13 periods, formulas only
      6 Prospects         kg/day in, machines and start period out
      7 Machines          the decision rows, stamped
      8 Yield Log         append-only actuals
      9 Invoices          paste lane + sell-through + realised price
    AI-Drive/Agent-Output/tlf/grow-room/<YYYY-MM>.csv    the immutable monthly snapshot

Import rule: **tabs 1 and 2 may be typed into; tabs 3–7 are formulas over Settings and Demand; tab 8 is append-only;
tab 9 is paste-only.** A formula in tab 3–7 that does not trace to Settings is a defect, and the workbook is rejected
by the reviewer who checks it.

Command and access table:

| Action | Who may do it | How |
|---|---|---|
| Change a parameter | GM only | edit Settings; `changed_by` and `changed_at` are typed, not formulas |
| Add a demand row | GM, grower | one row per client per period; the unique key rejects a second |
| Add a harvest row | grower | append at the bottom of Yield Log; corrections are new flagged rows |
| Paste invoices | finance | paste into Invoices with `source` filled; never edit an existing `invoice_no` |
| Read everything | any TLF staff member | view-only link |
| Export the monthly CSV | Bruce (agent) or the GM | read-only export, hash recorded, filed in AI-Drive |

Conventions the build must keep:

- Units in every header (`kg/7d`, `g/tray`, `R/kg`, `R/month`). A header without a unit is a defect.
- Named ranges for the eight parameters; no bare constants inside formulas.
- `CEILING` at each step, per I3, and the printed value is the ceiling, never the unrounded number.
- Period keys are ISO 7-day keys (`2026-W44`), sortable as text, never a date the sheet has to parse.
- 4.33 is a display divisor for "per month" only. No decision is computed on a month; decisions are computed on 7-day periods.

## Failure modes

| Failure | What the user sees | Control | Who checks it |
|---|---|---|---|
| Capacity typed instead of computed | a number that survives a Settings change | I2: reviewer edits `yield_g` and confirms every capacity cell moves | GM on sign-off |
| Double-counted harvest (the 17.28 kg error) | capacity 2× the room, promises missed by half | F5 space-time guard rejects the entry and names the ceiling | grower weekly |
| Duplicate demand row | a machine ordered for a client counted twice | `Demand` unique key on (period, client, channel) | GM at entry |
| Duplicate invoice paste | sell-through above 100% | `Invoices` unique key on `invoice_no`; F21 flag | finance monthly |
| Inconsistent rounding | 246 trays beside 491 spaces | F4 prints trays, spaces and machines from one rounding chain | reviewer on the tab |
| Stale parameters mid-cycle | a plan that no longer matches the room | F23 stamp; the plan prints the parameter version used | GM weekly |
| Invoice lane empty because Books refuses | sell-through blank, price unknown | paste lane with provenance; the blank is labelled as a missing feed, not zero | finance monthly |
| Harvest not logged for a period | capacity looks used, yield looks absent | F21 cross-checks harvest rows against sown batches | grower weekly |
| Failed trays unreported | realised yield drifts below plan with no explanation | F16 failed-tray count per row, F17 realised reliability | grower weekly |
| Workbook edited by someone outside the role matrix | history shows an edit with no owner | WorkDrive sharing set to view-only for everyone but GM, grower, finance | Bruce monthly |
| Five old sheets still circulating | two answers to the same question | F25 notice on Start Here, archive folder, one link | GM on retirement |

## Security, permissions and the audit record

Principals: GM (owner), grower (operator), finance (invoice lane), Bruce (agent, read and export), TLF staff (read).

| Role | Settings | Demand | Yield Log | Invoices | Export |
|---|---|---|---|---|---|
| GM | write | write | read | read | yes |
| Grower | read | write | write | read | no |
| Finance | read | read | read | write | yes |
| Bruce (agent) | read | read | read | read | yes |
| TLF staff | read | read | read | read | no |

What is stored: client names, delivery volumes, price per kilogram, per-machine yield and failure rates — commercially
sensitive, not personal data. No ID numbers, no bank details, no health data.

Anchored outside the system: the monthly CSV in AI-Drive with a sha256 of its content, and the WorkDrive version
history. Together these give a defensible record of what the sheet said in a given month.

How strong the audit claim is, stated honestly: WorkDrive version history is evidence, not proof. The owner of the
workbook can restore an older revision and the history shows a restore, not what was overwritten. The monthly CSV plus
its hash makes quiet edits visible from the next snapshot onward, and does nothing about edits made between snapshots.
No signature is claimed and none should be.

## Build order by dependency

Stage A — skeleton and input block.
Work: workbook in the TLF_Reporting folder, nine tabs, the eight parameters typed once in Settings, named ranges,
  headers carrying units.
Exit test: every later tab reads cycle days, yield, reliability and price from Settings, and no constant appears in a
  formula outside the Settings tab.

Stage B — capacity and the guard.
Work: machines 1–12 table, the rounding chain, the space-time guard. Runs in parallel with Stage C's data entry.
Exit test: 4 machines reads 8.21 kg per 7-day period and 7 machines reads 14.36, matching an independent
  recomputation to two decimals; entering 17.28 kg is rejected by the guard.

Stage C — demand and plan.
Work: Demand with its unique key, the 13-period plan, headroom, percent used, the verdict row.
Exit test: entering 14 kg in a single period against today's 8.21 kg capacity prints headroom −5.79, 170% used, and
  names 7 machines as the covering count.

Stage D — prospects and the machine decision.
Work: kg/day and delivery days in, machines and first servable period out; the stamped decision row; both price bases.
Exit test: 2 kg/day for 7 days returns 7 machines and 2 kg/day for 5 days returns 5; a decision row still reads its
  original yield after Settings is changed.

Stage E — yield log, invoices and the snapshot.
Work: append-only log with g/tray and variance, failed-tray counts, the paste lane with provenance, sell-through and
  realised price, the monthly CSV export with its hash.
Exit test: a full month of harvest rows and pasted invoices produces g/tray, variance, sell-through and R/kg with no
  formula pointing at an empty cell, and the exported CSV's hash reproduces on a second export of unchanged data.

Stage F — retirement and signposting.
Work: archive folder `_Retired — superseded by TLF Grow Room Master` under TLF_Reporting, the five model sheets moved
  and set read-only, the Start Here notice written.
Exit test: the TLF GM opens one link, finds every number the five files used to answer, and no live folder still
  presents a superseded model sheet as current.

## Decisions register

| # | Question | Recommended answer | Cost of each alternative |
|---|---|---|---|
| 1 | Retire the five model sheets into an archive folder, or leave them where they are? | Retire, never delete. Read-only archive, one signposting line. | Left in place, six surfaces keep disagreeing and the GM quotes whichever is open |
| 2 | Planning yield: 120 g, measured 131 g, or funding 140 g? | 120 g until four consecutive periods beat it | At 140 g every promise date is missed by a sixth; at 131 g the plan flatters itself on a good month |
| 3 | Machine price basis for payback: R13,294 build cost or R45,000 franchisee price? | Build cost for our own capital; franchisee price in the franchise pack | One basis for both under-prices the franchise or overstates our payback by 3.38× |
| 4 | Does a signed prospect count toward the machine trigger? | No — confirmed orders only, prospects on their own line | Machines bought on hope, sitting at 40% utilisation like the last four |
| 5 | Fix the Zoho Books seat so invoices can be read by API? | Yes — sell-through is the only check on what we earn per kg | The invoice tab stays hand-fed and sell-through is never reviewed |
| 6 | Who owns the workbook: the GM or the grower? | GM owns it, grower writes the log. One name on the file. | Shared ownership means neither changes a parameter when the room changes |
| 7 | Which figure is the room's official capacity: 8.21 kg or 8.64 kg per 7-day period? | 8.21 kg — the 95% rule is a standing policy, and 8.64 assumes every tray succeeds | Quoting 8.64 makes every failure look like a performance problem instead of a reliability number |

## Evidence appendix

Read at commit `11e6e11c` (`11e6e11c928440a17e412b6c7bad10308a04ea38`), 2026-11-03. Full command log:
`AI-Drive/Work/prd-program/facts/tlf-and-memory.md`.

| # | Command | Output summarised |
|---|---|---|
| E1 | `wc -l 2026-10-26-…html tlf-grow-room-master-prd-2026-10.html …mnemosyne.html` | 211 / 211 / 239 lines |
| E2 | python3 strip-`<style>`-and-compare on the two grow-room files | body equal after style strip: True; 14,332 chars each; all 26 raw diff lines are CSS variables |
| E3 | `wc -l …/brand-knowledge/TLF/facts.all.jsonl` and a distinct-`source_path` count | 14,520 facts, 794 documents |
| E4 | recompute capacity for machines 4/5/7/8/10 at 36 spaces, 14-day cycle, 120 g, 95%, 4.33 | 8.21 / 10.26 / 14.36 / 16.42 / 20.52 kg per 7-day period; every printed row reproduces |
| E5 | per-machine monthly ceiling under four yield assumptions | 8.885 kg at 120 g/95%; 9.353 at 120 g/100%; 10.21 at 131 g; 10.912 at 140 g |
| E6 | backwards table recomputation, 2/3/4/2 kg per day | machines 7/11/14/5 match; spaces printed 246/368/491/176 against computed 245.6/368.4/491.2/175.4 |
| E7 | September ledger arithmetic from the sweep's own facts | 8.64 kg per harvest × 2 = 17.28; physical ceiling 144 × 7 ÷ 14 = 72 tray-harvests; 69.12 kg = 8.64 × 8 sessions; variance −52.08 |
| E8 | variance reconstruction | 17.3 × 4.33 − 17.04 = 57.9; (67.1 + 17.04) ÷ 17.3 = 4.86; dashboard cells sum to −41.93 and −48.21 |
| E9 | payback and contribution | 13,294 ÷ 4,504.00 = 2.95 periods-equivalent months; at 8.885 kg → R4,001.88 and 3.32; 45,000 ÷ 13,294 = 3.38 |
| E10 | grep the sweep for the profile and collateral claims | 25–30 kg per machine per month appears in four profile/proposal documents; implies 51–61 trays a period against 18 available |
| E11 | grep the sweep for `Pico` | no market-comparison fact exists — the R60–R100 claim is unsupported by the corpus |

Files read: the three source HTML files listed above, `PRD-STRENGTH-STANDARD.md`,
`briefs/tlf-and-memory.md`, and `AI-Drive/Agent-Output/batman/brand-knowledge/TLF/facts.all.jsonl`.
The original PRD files were not modified; `git status --short` shows `prd-src/` untracked and nothing else.
