---
title: Migrate the fleet's memory from Hindsight to Mnemosyne
status: enhanced-proposal
version: 2.1-master
supersedes: 2026-10-30-prd-migrate-the-fleet-s-memory-from-hindsight-to-mnemosyne.html
based_on_commit: 11e6e11c
enhanced: 2026-11-03
owner: Bruce Wayne
---

# Migrating the fleet's memory (v2.1)

## What this version fixes

- **"PROPOSED — nothing executed" is false.** Phase 0 ran on 2026-11-02 06:42–06:44: six JSONL files and a manifest
  under `AI-Drive/Agent-Output/adrianna/memory-migration-2026-10-30/`, all six sha256 values verified. An install,
  rollout and revert were also scripted and at least partly run that morning (`rollout_profiles.sh`,
  `revert_mnemosyne.sh`, `cleanup_mnemosyne.sh`, `.env.bak-mnemosyne-20261102T070554`). Nothing of Mnemosyne remains.
- **"29 configs; dexter, lois, shadow have none"** is stale. There are **32 live config files** (31 profiles plus the
  main config) and every one names `provider: hindsight` — the three named profiles got it in the 2026-11-02 config
  rewrite. What they lack is a **bank binding**: 28 of 31 have `hindsight/config.json`. So they are half-wired, which
  is worse than the original claim: they will write somewhere, just not where anyone chose.
- **The counts are stale and were already stale when printed.** 166,333 facts at 09:00 became 175,023 at 10:41 the
  next day, and the three banks take about 129 new facts an hour. Every count in this document is timestamped.
- **The Phase 0 export decays.** It froze 171,425 facts; 28 hours later the same banks hold 175,023. A frozen export
  cannot be the import source — the archive is evidence and a rehearsal, and the cut-over needs a fresh one.
- **The bake-off comparison understated the gap the other way.** Re-scored from the saved runs, Hindsight is 20/22 at
  rank one and 22/22 at rank five; Mnemosyne is 17/22 and 20/22. Both are 13/13 on single-fact recall. The decision is
  about cost and egress, not about quality — and the document should say so in one line instead of implying parity.

## Product in five lines

1. **What it is:** a migration of the fleet's long-term memory from a 4.5 GB cloud-extracted Hindsight container to a
   local SQLite engine, without losing a fact, a timestamp or a source.
2. **Who uses it:** every Hermes profile in the fleet; the seats that write memory unattended (beast, scribe, builder,
   the executive seats) matter most.
3. **Decision it enables:** which engine holds the fleet's memory, at what running cost and with what rollback.
4. **Deliberately not:** a memory redesign. Extraction quality, consolidation and "dreaming" are follow-ups, not scope.
5. **The number that says it works:** facts in each bank after import equal facts exported for it within 0.5%, and a
   rollback returns a real memory id from the original bank before anything is deleted.

## Status ledger

States: `implemented` (proven by a command), `partial` (exists, incomplete), `absent` (proven missing),
`unverified` (not checked in this pass).

| Capability | State | Evidence | Gap |
|---|---|---|---|
| Hindsight serving the fleet | implemented | `/health` healthy; 3 live banks, 175,023 facts at 10:41; `hermes memory status` → `Provider:  hindsight` | runs a cloud extractor at `ollama.com` |
| Phase 0 export with per-file hash | implemented | `manifest.json` + 6 JSONL, 171,425 facts, all six `shasum -a 256` match | frozen at 2026-11-02 06:44; now 3,598 facts behind |
| Mnemosyne installed and enabled | absent | `hermes plugins list \| grep -c mnemosyne` → 0; `~/.hermes/plugins/mnemosyne` absent | reinstall at the catalog sha |
| Per-profile bank isolation | absent | no `memory.mnemosyne.*` key in any of the 32 configs | isolation must precede the first write |
| Import with identity preserved | partial | `import_facts.py` exists and ran (its cleanup notes a 224 MB store); drops facts under 40 chars, dedupes in-process only | 1,133 facts would be lost; a second run duplicates everything |
| Reconciliation against the export | absent | no reconciled counts survive; the cleanup removed the store | A5 cannot be claimed |
| Rollback | partial | nightly volume tar (15 archives, newest 1.3 GB), `revert_mnemosyne.sh`, 28 per-profile provider configs | no written rollback test; new writes after a flip are not covered |
| Canary on one profile | absent | no canary bank or probe set recorded | A3 unproven |
| Decommission | absent | volume live, 4.522 GB | follows the freeze |
| Consolidation of the imported facts | absent | 90,868 facts pending consolidation in Hindsight today; the importer sets no consolidation | follow-up scope, stated as such |

## Domain model

| Entity | Purpose |
|---|---|
| Bank | an isolation domain: `maio`, `maio-ops`, `maio-personal`; one per group of profiles |
| Document | one retained conversation chunk as ingested, with a content hash and a length |
| Chunk | a slice of a document that facts are extracted from |
| Memory (fact) | one extracted statement with a type, a timestamp and a source document |
| Observation | a consolidated belief built from several facts, carrying a proof count |
| Link | a typed edge between memories: semantic, temporal, entity, caused-by |
| Entity | a named thing the extractor resolved, used for graph traversal |
| Operation | a server-side unit of work with a status; where a failed import shows up |

Columns that decide correctness, from the live API:

| Table | Deciding columns (type) |
|---|---|
| `documents` | `id` text PK · `content_hash` text · `created_at` timestamptz · `text_length` int · `memory_unit_count` int · `document_metadata` jsonb · `tags` text[] |
| `memories` | `id` uuid PK · `text` text · `fact_type` enum(world, experience, observation) · `document_id` text FK · `chunk_id` text · `mentioned_at` timestamptz · `proof_count` int · `state` enum(valid, invalidated) · `source_memory_ids` uuid[] · `metadata` jsonb |
| `links` | `from_id` uuid · `to_id` uuid · `link_type` enum(semantic, temporal, entity, caused_by) |
| `operations` | `id` uuid · `status` enum(pending, processing, completed, failed) |

Scale today: 175,023 memories, 4,465 documents, 6,611,274 links, 30,734 observations.

The three indexes that decide performance and, here, correctness:

1. `memories(document_id)` — the upsert path resolves a document by id and deletes its memory units before rebuild.
2. `memories(mentioned_at)` — temporal recall and every ordering claim depend on it.
3. `documents(content_hash)` — the only handle that can tell a duplicate ingestion from a legitimate second session.

Invariants:

- **I1 Identity.** Every imported memory carries the source id it came from (`hindsight_id`) under a unique key. Two imports of the same record resolve to one row.
- **I2 Timestamp.** `mentioned_at` survives import as the record's own time, not the import time. A memory's position on the timeline is part of the memory.
- **I3 Source.** Every imported memory names its document and its bank. A memory with no source is a rumour and must not be imported.
- **I4 Kind.** `fact_type` survives import. Collapsing world, experience and observation into one kind destroys the distinction between a statement and a belief with evidence.
- **I5 Single writer per bank.** Exactly one engine writes a bank at a time. Dual-write is not permitted, because it cannot be reconciled by id across two id spaces.
- **I6 Read-back before delete.** Nothing in Hindsight is stopped or removed until a recall against the new engine returns a real id from the old one.
- **I7 One archive of record.** The export directory plus its manifest and hashes is the archive. No second, drifting copy is created.
- **I8 Reversibility.** Every profile can return to Hindsight by changing one line and restoring its config file.

## The engine, as a state machine with arithmetic

A migration is a state machine over banks, and the states are checkable:

    EXPORTED ─► HASHED ─► IMPORTED ─► RECONCILED ─► CUT_OVER ─► FROZEN ─► DECOMMISSIONED
                  │            │            │
                  └────────────┴────────────┴──────► ABORTED  (bank stays on Hindsight)

- `EXPORTED` — every document and every memory of one bank is on disk, counts recorded at the start.
- `HASHED` — a sha256 per file, written into the manifest; the state is only reachable when the re-read hash matches.
- `IMPORTED` — every record written into the target bank with I1–I4 intact. Resumable: the import key is the source id, so a restart re-walks and updates rather than appends.
- `RECONCILED` — imported equals exported per bank within tolerance, with missing and extra lists printed, not summarised.
- `CUT_OVER` — the profile's `memory.provider` names the new engine, verified by `hermes memory status`.
- `FROZEN` — the old bank takes no new writes; the container is stopped but the volume is held.
- `DECOMMISSIONED` — the volume is removed, only on an explicit go-ahead, only after the hold.

The pure function at the core:

    reconcile(exported_set, imported_set, key=hindsight_id) → {
        missing: [id],        # exported, not imported          → blocks CUT_OVER
        extra:   [id],        # imported, not in the export     → blocks CUT_OVER (unknown provenance)
        duplicated: [key],    # key present more than once      → blocks CUT_OVER (I1 broken)
        matched: int,         # key present in both
        tolerance: (imported - exported) / exported
    }

    pass  ⇔ missing = 0 ∧ extra = 0 ∧ duplicated = 0 ∧ |tolerance| ≤ 0.005

Reconciliation is per bank and per file, and the comparison is on the id, never on the text. Text comparison looks
precise and is not: the extractor rewrites phrasing, so two runs over the same source produce different strings for the
same fact.

Edge cases, each with its rule:

| Case | What happens | Rule |
|---|---|---|
| A record is re-indexed twice | a second write of the same source id | I1 upsert on `hindsight_id`; the second write updates in place. Without that key the second run duplicates all 171,425 facts and doubles every proof count |
| A document is re-ingested under its old `document_id` | Hindsight deletes the document and its memory units, then rebuilds: new uuid per memory, chunk ids renumbered, `proof_count` reset, links to the old nodes orphaned | never re-import a document into a bank that already holds it; import facts, not documents |
| Empty bank | reconcile prints `matched 0`, `tolerance 0`, and passes trivially | a bank with 0 exported records cannot be "verified" — mark it `not applicable`, not `pass` |
| Stale export | imported count is 3,598 lower than live | re-export at cut-over with the fleet paused, or import the delta by id; never mix a frozen export with live counts |
| Record invalidated between export and import (`state: invalidated`) | it is in the export but should not be live | carry `state` and `invalidated_at`; import invalidated records as archived, not as valid memories |
| Fact under 40 characters | the current importer skips it silently | remove the length filter; the measured loss is 536 + 409 + 188 = 1,133 facts |
| Duplicate text across banks | same sentence in two banks is legitimate | dedupe within a bank by id, never across banks by text |
| Import dies at record 40,000 | restart would re-add the first 40,000 under the old importer | idempotent key + resumable cursor; restart re-walks and matches |
| Disk exhaustion mid-import | partial bank, unknown state | import into a bank suffixed `_stage`, reconcile, then promote by rename or re-point |
| Self-approval (the operator marks reconciliation pass) | nobody checked | the reconciler prints the numbers; a second principal reads them |
| Two profiles writing one bank | facts from unrelated seats mixed | I5 + per-profile bank; the 28 existing bindings show the fleet already depends on this |

What must be preserved, stated precisely, because this is the whole migration:

1. **Identity** — the source id of every record, carried as `hindsight_id` under a unique constraint, so a record can be found again after the engine changes.
2. **Timestamp** — `mentioned_at` as the record's own time, plus `created_at` of its document, so "when did this happen" keeps its answer.
3. **Source** — `document_id`, `bank`, and the original `fact_type`, so a fact can be traced to the conversation it came from and remains a statement rather than a belief.
4. **State** — `valid` / `invalidated` with `invalidated_at`, so a withdrawn fact does not come back to life.
5. **Links** — the 6.6 M typed edges are not re-creatable. Either they are migrated as first-class rows, or the document states in writing that the new engine starts with a flat memory and rebuilds links over time. Silence here is the defect.

What breaks if a record is re-indexed twice, concretely: with a stable key, nothing but wasted time. Without one, the
bank doubles, every `proof_count` doubles (a belief supported by 3 facts is now supported by 6), the reconciliation
tolerance check fails by 100%, and the export archive stops being a description of the live bank. That is why I1 sits
above every other requirement in this document.

## Feature table

| ID | Feature | Priority | Why it matters | Acceptance test (expected value) |
|---|---|---|---|---|
| F1 | Export every bank to JSONL with counts at start | P0 | The archive is the only thing that survives a bad migration | 3 banks × 2 files; `wc -l` equals the count read at the same minute, exactly |
| F2 | sha256 per file in a manifest | P0 | An unhashed archive is a guess | 6 hashes in `manifest.json`, each equal to `shasum -a 256` of its file |
| F3 | Stable import key `hindsight_id` under a unique index | P0 | Without it, a second import duplicates 171,425 records | importing the same file twice leaves the bank's count unchanged |
| F4 | Timestamp preservation | P0 | "When did this happen" is half of what a memory is | a record mentioned 2026-10-14 imports with `mentioned_at` 2026-10-14, not the import date |
| F5 | Source and kind preservation | P0 | A belief and a statement must stay distinguishable | imported observation stays `observation` with its `proof_count`, not `world` with 1 |
| F6 | Per-profile bank isolation before first write | P0 | Two seats sharing a bank cannot be un-mixed later | writing in profile A leaves profile B's recall empty |
| F7 | Resumable, idempotent import | P0 | A 175 k-record import will be interrupted | interrupt at 40,000, restart, final count equals the export count |
| F8 | Remove the <40-character filter | P0 | 1,133 facts are lost silently today | imported count includes the 536 maio-ops records under 40 chars |
| F9 | Per-bank reconciliation with missing/extra/duplicate lists | P0 | A tolerance alone hides which records went missing | `missing=0, extra=0, duplicated=0, tolerance ≤ 0.5%` for each of the 3 banks |
| F10 | Reconcile on id, not text | P0 | The extractor rewrites phrasing between runs | two runs over one source produce different text and the same id set |
| F11 | Canary profile with the 13 single-fact probe questions | P0 | One profile fails cheaply; 31 fail expensively | 13/13 at rank one, scored by `scorer.py` against `corpus.json` |
| F12 | `hermes memory status` proof of the switch | P0 | The config file is not the runtime | `grep -qE "^  Provider: +mnemosyne$"` exits 0 |
| F13 | Rollback drill, written and run | P0 | An untested rollback is a hope; P1 defect by definition | flip back, recall returns a real id from `maio-ops`, completed before any deletion |
| F14 | Writes after cut-over are exportable | P1 | Rollback loses anything the new engine wrote unless it can be exported | export the canary bank after 24 hours of use and re-import into Hindsight without duplicates |
| F15 | No cloud egress on a write | P0 | The entire point is local | `dig +short ollama.com` resolved, then `nettop` shows no connection to that address during one retain and one recall |
| F16 | First-run embedding download pre-warmed | P1 | A cold start that stalls is an outage | model present locally; a start with the network down still recalls |
| F17 | Prompt growth measured, not guessed | P1 | 41 declared tools sit in every prompt | tool count and first-turn prompt tokens recorded; flag if above +2,000 |
| F18 | Per-profile config diff before and after | P0 | 32 files change; one missed file is a seat on the wrong engine | `grep -c "provider: mnemosyne"` equals 32 after rollout, 0 after rollback |
| F19 | Bank mapping table, one row per profile | P1 | Three profiles today have no binding at all | 31 rows; bank column never empty |
| F20 | Export freshness check at cut-over | P0 | The archive is already 3,598 facts behind | export timestamp later than the last write to every bank, printed |
| F21 | Operation-failure review | P1 | 84 failed operations and 2,825 failed consolidations exist today | failures enumerated by bank; each classified lost or retryable |
| F22 | Archive retention and location | P1 | 78.7 MB of fact text plus 43 MB of documents must outlive the container | archive present in AI-Drive, manifest hashes verified, retention rule written |
| F23 | Decommission only after the hold | P0 | Deleting the volume is the one irreversible act | volume still listed on the day after cut-over; removal is a separate, logged action |
| F24 | Consolidation plan stated, not implied | P2 | 90,868 facts await consolidation and 30,734 observations exist | follow-up document named, scope and owner stated |
| F25 | Link-preservation decision recorded | P0 | 6.6 M typed edges are not rebuilt by accident | one written line: migrated as rows, or explicitly dropped |

## Architecture and API surface

The migration is a set of scripts beside the fleet, not a service.

    AI Hub/memory-bakeoff/                    rehearsal kit (today)
      corpus.json  scorer.py                  the 24-question probe set and its scorer
      export_banks.py                         Phase 0: bank → JSONL + manifest
      import_facts.py                         Phase 3: JSONL → Mnemosyne (to be rewritten: I1–I4)
      rollout_profiles.sh / revert_mnemosyne.sh / cleanup_mnemosyne.sh
    AI-Drive/Agent-Output/adrianna/memory-migration-2026-10-30/
      <bank>.facts.jsonl  <bank>.documents.jsonl  manifest.json
    ~/.hermes/profiles/<profile>/hindsight/config.json    the bank binding, per profile
    ~/.hermes/config.yaml                                  memory.provider, the switch

One import rule that keeps it honest: **the archive is read-only after hashing.** Nothing rewrites a JSONL file; a
re-export writes a new dated directory. A migration whose source changes while it runs cannot be reconciled.

Endpoints used, and by whom:

| Endpoint | Method | What for | Who may call |
|---|---|---|---|
| `/v1/default/banks` | GET | bank list and counts | anyone, read-only |
| `/v1/default/banks/{bank}/documents` | GET | document ids, hashes, lengths | migration operator |
| `/v1/default/banks/{bank}/memories/list` | GET | paged facts with timestamps and types | migration operator |
| `/v1/default/banks/{bank}/stats` | GET | nodes, links, observations, operation status | anyone, read-only |
| `/v1/default/banks/{bank}/export` | GET | server-side export alternative to paging | migration operator |
| `/memories` (POST) | POST | write path — **never** used to re-import into the same bank | nobody during this migration |

Conventions the build must keep:

- Pagination at 200 records, offset-stable within a run; a run records its start count so drift is visible.
- Idempotency by `hindsight_id`, never by text.
- Versioning: the archive directory is dated; the manifest is versioned by its own start timestamp.
- No dual-write. A bank has one writer; the flip is atomic per profile.

## Failure modes

| Failure | What the user sees | Control | Who checks it |
|---|---|---|---|
| Second import run duplicates everything | a bank that doubles overnight | I1 unique key on `hindsight_id`; F3 test runs the import twice | migration operator |
| Facts silently dropped by the length filter | a short preference the fleet no longer remembers | F8 removes the filter; count reconciliation includes them | reconcile step |
| Documents re-ingested under their old id | Hindsight deleting and rebuilding units, links orphaned | import facts, never documents; the write path is not used against a live bank | migration operator |
| Export stale at cut-over | imported bank missing the last day of work | F20 freshness check; re-export with the fleet paused | migration operator |
| Isolation left off | every profile reads every other profile's memory | F6 before the first write; F18 config diff proves the setting | canary reviewer |
| Rollback untested | discovering at 02:00 that the flip does not revert | F13 drill executed and written before any deletion | Ricardo's go-ahead gate |
| New writes lost on rollback | a period of work vanishes when the provider flips back | F14 exportable new writes; or accept and state the window in writing | migration operator |
| Embedding model download stalls a cold start | gateway hangs on first retain | F16 pre-warm and an offline start test | canary reviewer |
| Prompt growth from 41 tools | slower, dearer turns on 31 profiles | F17 measures on the canary; fallback is a smaller engine, not trimming | canary reviewer |
| Operation backlog hides failed writes | retries never surface as errors | F21 enumerates 84 failed operations and 2,825 failed consolidations | migration operator |
| Someone removes the volume early | the archive is the only copy left | F23: removal is separate, logged and gated | Ricardo |

## Security, permissions and the audit record

Principals: Ricardo (authority), Bruce (agent, migration operator and verifier), each profile's agent (writer of its own
bank), the Hindsight container (process), the Mnemosyne database (file).

| Role | Read banks | Export | Import | Flip a profile | Delete the volume |
|---|---|---|---|---|---|
| Ricardo | yes | yes | no | approves | approves |
| Bruce (agent) | yes | yes | yes, into a staging bank | prepares, does not approve | no |
| Profile agent | own bank | no | no | no | no |
| Container / process | all, at runtime | no | no | no | no |

What is stored: conversation transcripts and extracted statements — names, preferences, prices, plans, and whatever
staff and Ricardo have said in session. Some of it is personal. The archive holds the full original text of every
document (43 MB in the current export), which is strictly more than the facts.

Anchored outside the system: the nightly volume tar (15 archives, newest 1.3 GB, 14-day retention) and the hashed JSONL
archive. Both live on the Hiksemi volume, which is a single point of failure for both — worth stating plainly.

How strong the audit claim is: **sha256 proves the archive has not changed since it was written. It proves nothing
about who wrote it or whether it is complete.** Completeness comes only from the count comparison at export time, and
that comparison is against a live, drifting database. There is no signature, no notary, and no append-only log of the
migration's own actions beyond the scripts themselves. The honest sentence is: the archive is verifiable, the migration
is reproducible, and neither is attested.

## Build order by dependency

Stage 0 — re-export at cut-over (Phase 0 exists and must be repeated).
Work: run `export_banks.py` against all three banks with the fleet paused or accepting drift, write a fresh manifest,
  verify every hash, record the export time and each bank's last-write time.
Exit test: the export time is later than the last write in every bank, all six hashes match, and each file's line count
  equals the count read at the same minute.

Stage 1 — isolation and the bank map. Runs in parallel with Stage 2.
Work: one row per profile in a bank map; `memory.mnemosyne.profile_isolation true` and a bank name per profile before any
  write; the three profiles with no binding today get one.
Exit test: 31 rows, no empty bank column, and a write in one profile is invisible to another.

Stage 2 — the importer, rewritten to the invariants.
Work: `hindsight_id` unique key, timestamp, source, kind and state preserved, resumable, no length filter.
Exit test: importing the same file twice leaves the bank's count unchanged, and a record whose mention date
  precedes the import by a month reads its own date back.

Stage 3 — canary on one profile.
Work: install at the catalog sha, enable, flip the canary, restart, run the probe set and one real retain.
Exit test: `Provider:  mnemosyne` matches the regex, the 13 single-fact questions score 13/13 at rank one, and one new retain is recallable
  within the same session.

Stage 4 — import and reconcile every bank.
Work: stage into a suffixed bank, import, reconcile on id, print missing/extra/duplicate lists.
Exit test: for each bank, missing = 0, extra = 0, duplicated = 0, tolerance within 0.5%, and the link decision recorded.

Stage 5 — rollback drill, before rollout.
Work: flip the canary back, recall a real id from `maio-ops`, flip forward again, export the new writes.
Exit test: the rollback recall returns a real memory id, the forward flip re-passes the probe, and no duplicate appears
  after the round trip.

Stage 6 — wave rollout.
Work: two lines per profile in waves — the writing seats, then the executive seats, then the rest; a config diff after
  each wave.
Exit test: `grep -c "provider: mnemosyne"` equals the number of profiles in the wave, and the probe passes on a
  sampled profile from each wave.

Stage 7 — freeze, hold and decommission.
Work: stop the container once no profile writes to it; hold the volume; remove it only on a separate go-ahead.
Exit test: 14 consecutive days with zero writes to every Hindsight bank, then the volume listing is empty and the
  archive hashes still verify.

## Decisions register

| # | Question | Recommended answer | Cost of each alternative |
|---|---|---|---|
| 1 | Migrate all three banks, or migrate two and start `maio` fresh? | Migrate all three. `maio` holds 58,781 facts and the fleet's shared context; a fresh start throws away the fleet's memory of its own decisions | A fresh `maio` is cleaner and cheaper to import, and loses every cross-company recollection on day one |
| 2 | Delete the Hindsight volume after the hold, or keep it forever? | Keep it as a cold archive. 4.5 GB costs almost nothing; the irreversible act buys 4.5 GB | Deleting reclaims 4.5 GB once and removes the only copy that is not a tar |
| 3 | Which profile is the canary? | `scribe` — it writes constantly, so failures surface immediately, and it is not the seat that talks to you | Batman as canary fails in the seat that runs the fleet, which is the wrong blast radius |
| 4 | Are the 6.6 M links migrated, or explicitly dropped? | Dropped, in writing, with a rebuild plan. Migrating them is a second project | Dropping them costs graph recall until the new engine learns its own edges; migrating them costs a build nobody has scoped |
| 5 | One bank for the fleet, or the current three? | Keep three. Isolation already exists in the bindings and three banks match three audiences | One bank is simpler to operate and mixes work memory with personal memory |
| 6 | Who signs the reconciliation pass? | Bruce prepares, Ricardo reads the printed numbers. One human pair of eyes on an irreversible step | An agent-only sign-off is faster and has nobody to answer to if a bank is short |
| 7 | Consolidation and "dreaming" now, or a follow-up? | Follow-up. 90,868 facts are already unconsolidated in Hindsight; importing that backlog into a new engine is a separate problem | Doing it now delays the migration behind the hardest part of the old system |

## Evidence appendix

Read at commit `11e6e11c` (`11e6e11c928440a17e412b6c7bad10308a04ea38`), 2026-11-03. Full command log:
`AI-Drive/Work/prd-program/facts/tlf-and-memory.md`.

| # | Command | Output summarised |
|---|---|---|
| E1 | `curl /health` | `{"status":"healthy","database":"connected"}` |
| E2 | `curl /v1/default/banks` at 10:41 | maio-ops 69,414 · maio 58,781 · maio-personal 46,828 · test bank 2 → 175,023 facts |
| E3 | `curl /stats` per bank | links 6,611,274 · documents 4,465 · observations 30,734 · pending consolidation 90,868 · failed consolidations 2,825 · last consolidated 2026-10-05 |
| E4 | `docker inspect hindsight` | image `ghcr.io/vectorize-io/hindsight@sha256:50311d02…` · LLM `gpt-oss:20b` at `https://ollama.com/v1` · embeddings local · volume 4.522 GB · pg data 4.3 G |
| E5 | `grep -l "provider: hindsight" config.yaml profiles/*/config.yaml` | 32 files |
| E6 | count `profiles/*/hindsight/config.json` and group by `bank_id` | 28 bindings: maio 14, maio-ops 6, maio-personal 8; without: dexter, lois, shadow |
| E7 | `hermes --version` / `hermes plugins list` / `hermes memory status` | v0.22.5 · mnemosyne rows 0, hindsight 1.2.1 · `Provider:  hindsight` (two spaces) |
| E8 | `hermes-agent/plugin-catalog/mnemosyne.yaml` | 41 declared tools · requires_hermes ≥ 0.21.4 · version 0.7.3 · bge-small-en-v1.5 from Hugging Face |
| E9 | `cat manifest.json` + `shasum -a 256 *.jsonl` | 171,425 facts, 4,335 documents, 6 of 6 hashes match |
| E10 | recount of the export vs live banks | 171,425 → 175,023 = +3,598 in 28 hours, about 129 an hour |
| E11 | measure `import_facts.py` filters against the export | short < 40 chars: 536 / 409 / 188; duplicate text[:400]: 1,514 / 1,436 / 595; observations 11,278 / 10,744 / 8,712 |
| E12 | `python3 scorer.py corpus.json results_*.json` | Hindsight 20/22 @1, 22/22 @5, MRR 0.97 · Mnemosyne 17/22, 20/22, 0.89 · BM25 16/22, 0.83 · 24 queries, 22 scoreable |
| E13 | `POST /memories` description in `/openapi.json` | "If a memory item has a `document_id` that already exists, the old document and its memory units will be deleted before creating new ones (upsert behavior)." |
| E14 | `~/Library/LaunchAgents/com.maio.backup.plist`, `backup.sh` lines 104–110, `ls AI-Drive/Backups/hindsight` | daily 03:30, volume tar with the container stopped, 14-day retention, 15 archives, newest 1.3 GB |
| E15 | `ls ~/.hermes/plugins/mnemosyne`, `ls ~/.hermes/mnemosyne` | both absent; rollout/revert/cleanup scripts dated 2026-11-02 and `.env.bak-mnemosyne-20261102T070554` remain |

Files read: the source HTML, `~/.hermes/config.yaml`, all 31 `profiles/*/config.yaml` and `hindsight/config.json`,
`~/.hermes/plugins/hindsight/{__init__.py,config_schema.py,README.md}`, `~/.config/maio-stack/backup.sh`,
`~/Library/LaunchAgents/com.maio.backup.plist`, the `AI Hub/memory-bakeoff/` kit, and the migration export directory.
The original PRD file was not modified; `git status --short` shows `prd-src/` untracked and nothing else.
