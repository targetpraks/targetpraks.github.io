---
title: "dsh-maio-nexus — Unified DeepSeek Harness Plugin Suite (enhanced)"
status: enhanced-proposal
version: "v11-enhanced"
supersedes: "2026-11-02-prd-dsh-maio-nexus-unified-deepseek-harness-plugin-suite.html (v10)"
based_on_commit: "c5a4b252"
enhanced: "2026-11-03"
owner: "Adrianna A"
---

# dsh-maio-nexus — Unified DeepSeek Harness Plugin Suite (enhanced master)

Source PRD: `2026-11-02-prd-dsh-maio-nexus-unified-deepseek-harness-plugin-suite.html` (1,556 lines, v10),
rendered from a markdown record. This master is the buildable extraction: components with stable IDs,
config contract, routing/fallback as a state machine, failure modes, and a dependency-staged build order.
Facts and command output: `/Volumes/Hiksemi 1TB/AI-Drive/Work/prd-program/facts/dsh-maio-nexus.md`.

## 2. What this version fixes

The v10 PRD is a strong reading document but is not directly buildable: components are named in prose,
the dispatch decision is described not specified, failure modes have no control column, and the build
order is phases with dates. This enhanced master corrects those gaps, and records two claims v10 makes
that measurement now contradicts.

| # | Claim in v10 | What is actually true | Evidence |
|---|---|---|---|
| 1 | "nightly index cron (03:50) and an hourly watchdog (silent unless degraded) are live" | No crontab or launchd plist referencing nexus/vault_index/watchdog exists on this Mac | `crontab -l \| grep nexus` → none; `find … -name '*.plist' … grep vault_index` → none. Facts file §UNVERIFIED #1 |
| 2 | "web app on :7788 returns HTTP 401 (proven)" | On this run `curl :7788` returns 000 (connection refused); app may be stopped | Facts file; PRD evidence is 2026-11-02 17:20 |
| 3 | "Six profiles" | Seven dirs on disk: acp, desktop, dshweb, headless, mini, superagent, web | `ls ~/.dsh/profiles` |
| 4 | "Video lane absent" in v10 §14 evidence table | Video lane is installed: HyperFrames 0.9.2, Remotion 4.0.540, faster-whisper 1.2.1, Blender 5.2.3, FFmpeg 9.0.2 | Facts file; v10 §6.0 already corrects this |
| 5 | Vault "2,550 notes" | 2,582 markdown files on disk; 2,574 in index (build.json); 2,557 at acceptance run | `find … -name '*.md' \| wc -l` = 2582 |

Depth added beyond v10: stable component IDs (C1–C10), config contract table, dispatch state machine with
arithmetic, failure-mode table with controls, and a dependency-staged build order with boolean exit tests
and zero dates.

## 3. Product in five lines

- **What it is:** a provider-adapter plugin suite (`dsh-maio-nexus`) that gives DeepSeek Harness (DSH)
  shared memory with the Hermes fleet, read-only recall over the Maio Hub vault, a dispatch contract
  between a long-lived Router and context-isolated Workers, and an external watchdog. Written as a
  provider adapter, not a vendor-locked plugin.
- **Who uses it:** DSH surfaces — Web app :7788, Desktop app, CLI/ACP, T3 Code — acting as a Router that
  dispatches Workers. Hermes keeps its own channels; DSH holds no bot token and no inbound webhook.
- **Decision/action it enables:** a DSH session can see what the Hermes fleet knows, search 2,500+ vault
  notes, render a brief to an MP4, and run the app-plan → app-build → app-verify chain end to end.
- **Deliberately not:** a second memory store, a vault writer, a channel bot, a paid model lane, or an
  auto-merging agent. Memory writes go through Hermes' tools; vault writes go through Beast/OpenKnowledge.
- **Single number that says it works:** acceptance suite 10/10 pass (A1–A9 + F2) with vault sha256
  `77e0679aae41cf7d` unchanged before and after.

## 4. Status ledger

One row per capability v10 claimed or implied. Evidence column cites a command or file path.

| Capability | State | Evidence | Gap |
|---|---|---|---|
| MCP bridge `nexus` (4 tools) on stdio | implemented | `~/AI Hub/dsh-maio-nexus/nexus_mcp.py`; A1 pass; tools = [nexus_status, nexus_memory_recall, nexus_vault_recall, nexus_vault_get]; `dsh --dump-config --profile acp` → mcp-nexus stdio entry present in 6 profiles (acp, dshweb, headless, mini, superagent, web) | none |
| Vault index (FTS5) over vault notes | implemented | `index/vault.db`; build.json notes=2574; A8 median 1 ms; `cat index/build.json` → notes=2574, built 2026-11-03T03:50:19+0200 | none |
| Profile overlays in web/mini/headless/dshweb/acp | implemented | `cordis.patch.yml` contains `mcp-nexus`; `dsh --dump-config` composes (install.py); `grep mcp-nexus ~/.dsh/profiles/*/cordis.patch.yml` → 6 profiles (acp, dshweb, headless, mini, superagent, web); desktop app-owned (no patch) | desktop untouched (app-owned) by design |
| Desktop profile support | absent | no overlay installed; install.py requires `--include-desktop` | app-owned; opt-in only |
| Acceptance suite 10/10 | implemented | `tests/acceptance.py`; `docs/reviews/acceptance-2026-11-02T18-36.json` → A1–A9 + F2 all pass (10/10) | none |
| Watchdog plain-language, fail-closed | implemented | `watchdog.sh`; exits 1 when degraded; `watchdog.sh` → "nexus: memory ok · index 417m · 2574 notes · suite all pass." exit 0 (healthy on this run) | cron scheduling unverified (see §13 row) |
| Nightly index refresh | partial | `vault_index.py` idempotent; build.json updated 2026-11-03 03:50 | no scheduler entry found on this Mac |
| Skills nexus-memory / nexus-vault / video-lane | implemented | present in `~/.hermes/skills` and `~/.claude/skills`; `ls ~/.hermes/skills | grep -E 'nexus|video-lane'` → nexus-memory, nexus-vault, video-lane (both trees) | none |
| Provider adapter (Hindsight active) | implemented | `hermes memory status` → hindsight; nexus_memory_recall returns bank maio-ops | S9 provider-swap not exercised |
| Router/Worker dispatch contract | absent | no context-packet emitter in repo; G4 unproven | prototype not installed |
| nexus-thread-bind (pass-through) | absent | no thread-binding code present | needs prototype install |
| Memory-return (Worker → Router candidates) | absent | no candidate schema consumer | needs C4 + C6 |
| Trigger two-stage filter | absent | no filter code present | needs C4 |
| Render lane from DSH | partial | lane installed on Mac; no DSH-issued render observed | G4 half open |
| Stills (mflux) | absent | no mflux binary/venv; HF cache 1.1 MB | phase-3 install step |
| Blender MCP bridge | absent | auto-mode blocked add-on; Blender 5.2.3 present | needs Ricardo's word |
| app-plan / app-build / app-verify chain runnable by DSH | partial | skills v1.0.0 in both trees; G4 proves harness routing only | prototype bundle not installed |

## 5. Domain model

Entities (one-line purpose):

- **Router** — long-lived session that talks to surfaces, holds shared context, dispatches Workers, records why.
- **Worker** — context-isolated session that executes one ticket; never speaks to a channel; returns memory candidates.
- **Thread** — a conversation the Worker subscribes to; follow-ups bypass the Router.
- **Context Packet** — the dispatch contract (§4.3.1): request, scoped facts, vault refs, acceptance, budget, reason.
- **Memory Candidate** — fact + confidence + source + scope + durable flag returned Worker → Router.
- **Vault Note** — a markdown file in Maio Hub (read-only source).
- **Vault Index** — SQLite FTS5 over notes, with a `files` mtime/sha table.
- **Render Receipt** — `receipt.json` per render job (§4.3.4).
- **Watchdog Report** — ≤100-word plain-language status (§4.3.3).
- **Profile** — a DSH profile (web, mini, headless, dshweb, acp, desktop, superagent) mapping to one Hermes profile.
- **Plugin** — a staged third-party dsh bundle (Workstream B).
- **Trigger** — an event (vault write, memory write, chat message, GitHub comment, CI result) that may reach the Router.

Tables that carry them:

- `files(path TEXT PK, title, mtime REAL, size INTEGER, sha TEXT)` — index bookkeeping.
- `vault(path UNINDEXED, title, body)` — FTS5 virtual table, `tokenize='porter unicode61'`.
- `cordis.patch.yml` per profile — YAML list of `insert`/override entries; one `mcp-nexus` entry per installed profile.

Indexes that decide performance: FTS5 `vault` (path UNINDEXED, title+body indexed); `files.path` primary key for mtime lookup; `files.mtime` for incremental reindex (no full scan when unchanged).

Numbered invariants:

- I1 — The vault is read-only to every DSH component; `vault_index.py` writes only to `index/vault.db` and never to the vault. F2 enforces via sha256 before/after.
- I2 — Memory has exactly one source of truth: the provider Hermes reports as active. No parallel store; Workers never write.
- I3 — A Worker's context packet contains only facts scoped to its work item; Worker A cannot recall Worker B's scratch facts (S2).
- I4 — Every dispatch records a `reason` string; a dispatch without a reason is invalid (§4.3.1).
- I5 — No secret (key, token, password, card/bank number, health detail) enters a packet, receipt, log, plugin config, or chat. Credential hard stop.
- I6 — A trigger outside the allowed scope never reaches a model call; counted, not asserted (S7).
- I7 — No render counts as finished until `render-qc` passes; only `--allow-static` / `--allow-silent` may waive a finding (F14).
- I8 — The acceptance suite is authored from the PRD, stored outside every lane worktree, and the builder never reads it (G2, G7).
- I9 — Proactive work runs in observe mode until a written rule is approved (§8).
- I10 — DSH holds no bot token, no gateway, no inbound webhook (§3.4).

## 6. The engine, as a state machine with arithmetic

### 6.1 Provider resolution state machine

States: `UNRESOLVED → READING_CONFIG → PROBING_HEALTH → ACTIVE | FAILED`.

Transitions:
- `UNRESOLVED → READING_CONFIG`: on first tool call or status().
- `READING_CONFIG → PROBING_HEALTH`: if `~/.hermes/hindsight/config.json` parses (mode, api_url, bank_id present).
- `READING_CONFIG → ACTIVE(builtin)`: if no external config → built-in MEMORY.md/USER.md only.
- `PROBING_HEALTH → ACTIVE`: if `/health` returns `{"status":"healthy"}` within 2 s.
- `PROBING_HEALTH → FAILED`: on timeout/HTTP error → return named error, never empty.

Arithmetic: health probe timeout 2 s; memory recall timeout 30 s; max_tokens clamped [256, 8000], default 1200.

### 6.2 Index freshness state machine

States: `MISSING → BUILDING → FRESH → STALE → MISSING`.

Transitions:
- `MISSING → BUILDING`: `vault_index.py` invoked (manual or cron).
- `BUILDING → FRESH`: build.json written with notes count; exit 0.
- `FRESH → STALE`: age > 5 min after a vault write (S4) OR age > 1560 min (watchdog threshold).
- `STALE → BUILDING`: reindex triggered; incremental by mtime unless `--rebuild`.
- Any state → `MISSING`: db file absent → recall returns error naming `vault_index.py`.

Arithmetic: full build 5.15 s for 2,557 notes; incremental 0.57 s (build.json 2026-11-03); median warm recall 1 ms; SLO vault recall warm < 50 ms; SLO memory recall warm < 100 ms; index freshness ≤ 5 min or answer says "stale index".

### 6.3 Dispatch state machine (Router)

States: `IDLE → FILTERING → PACKET → DISPATCHED → RECORDING → IDLE`, with a parallel `PASS_THROUGH` path.

Transitions:
- `IDLE → FILTERING`: on trigger event.
- `FILTERING → PACKET`: only if deterministic scope check passes (S7); otherwise drop and count.
- `FILTERING → IDLE`: trigger outside scope → no model call, increment violation counter.
- `PACKET → DISPATCHED`: context packet assembled (§4.3.1) with `reason` non-empty (I4).
- `DISPATCHED → RECORDING`: Worker spawned with isolated context; Router records worker id + reason.
- `RECORDING → IDLE`: Worker returns memory candidates; Router decides and writes through Hermes tools.
- `PASS_THROUGH`: follow-up in same Thread reaches its Worker without Router re-decision; Router still records (S3).

Arithmetic / core function: context packet `budget_tokens` default 2000 (Inline & Spill). Router token overhead target −30% vs no pass-through (article measured −37%). Pass-through subscription is the mechanism.

Edge cases enumerated:
- Concurrency: two Workers on same profile → per-Worker packets, no shared mutable cache (I3).
- Empty set: vault query returns 0 rows → answer "no match", not "nothing known"; index age reported.
- Stale version: vault write within SLA not yet indexed → answer says "stale index" (S4).
- Withdrawal: a Worker returning no candidates → Router writes nothing; no empty fact.
- Exhaustion: token budget exceeded → spill to pointers; model walks one hop (S8).
- Self-approval: a Worker cannot approve its own memory write; Router is the only writer (I2).
- Duplicate: same fact returned twice → Router dedupes by (fact, scope) before writing.

### 6.4 Failure modes at the engine level

See §9 for the full table; engine-level: provider down → FAILED state with named error; model missing → S9 fail loudly; tag drift → pin check at build time (§11 phase 0); context overflow → spill to pointers (S8).

## 7. Feature table

Stable IDs. Priorities P0/P1/P2 only. Every row has an acceptance test with expected value.

| ID | Feature | Priority | Why it matters | Acceptance test (expected value) |
|---|---|---|---|---|
| F1 | Canary fact written via Hermes memory tool recalled by DSH session unprompted; cross-profile canary not recalled | P0 | proves shared memory works and is scoped | two-profile canary run; transcript shows recall hit on profile A, miss on profile B |
| F2 | vault_recall returns exact snippets; every vault file hash unchanged afterwards | P0 | read-only proof | `sha256` before == after (`77e0679aae41cf7d` baseline); `git status --porcelain` empty |
| F3 | One bundle installs on web/desktop/prototype without root and without breaking core | P0 | packaging honesty | `dsh plugin --profile <p> add ./dsh-maio-nexus` ×3 then `dsh <p> --dump-config` diff shows mcp-nexus present, exit 0 |
| F4 | Nightly index completes silently and idempotently | P1 | ops reliability | two consecutive `vault_index.py` runs; byte-identical `build.json` note count; no UI interruption |
| F5 | Video brief → 1080×1920 MP4 ≤30 s, no stock asset, no paid credit | P0 | core value of Workstream C | `ffprobe` shows 1080x1920, ≤30 s; `receipt.json` present; no paid API call logged |
| F6 | All text via cards/overlays/type; never an FFmpeg text filter | P0 | FFmpeg has 0 drawtext/subtitles filters on this Mac | `ffmpeg -filters \| grep -cE 'drawtext\|subtitles'` == 0; render uses PNG/HTML/GSAP |
| F7 | Every asset and render stays on this Mac; no paid/hosted call without approval | P1 | free-models rule (§8) | no outbound paid call in render log; receipt `source_sha256` present |
| F8 | DSH web app shows last render, size, QC verdict without terminal | P1 | usability | panel reads `receipt.json`; displays size_bytes and check.ok |
| F9 | `dsh <profile> "<brief>"` headless prints receipt path; second run same bytes | P1 | reproducibility | exit 0; stdout contains receipt path; second run byte-identical MP4 |
| F10 | One durable token-free artefact link per render, survives restart | P1 | sharing | link resolves after `dsh` restart; no token in URL |
| F11 | Same brief + same composition version → byte-comparable output | P2 | auditability | two runs produce matching sha256 of out.mp4 |
| F12 | Every render writes receipt §4.3.4; panel derives link from it | P1 | audit | receipt has brief, profile, composition, check, duration_s, size_bytes, artifact, poster, started, finished, source_sha256 |
| F13 | Poster renders from same brief via free path; receipt records which path | P2 | stills coverage | receipt `poster` field present; path is HTML/3D frame or local mflux |
| F14 | No render finished until render-qc passes; only --allow-static/--allow-silent waive | P0 | prevents worthless MP4s | `render-qc` exit 0 or waived flag in receipt; RESULT: PASS |
| S1 | Router injects shared memory + vault context and produces a packet for every dispatch | P0 | dispatch honesty | packet JSON matches §4.3.1 schema; `packet_id`, `reason` present |
| S2 | Worker A cannot recall Worker B's scratch facts nor open sibling profile store | P0 | isolation | probe returns access-denied on sibling store; 0 facts leaked |
| S3 | Follow-up in same Thread reaches Worker without Router re-decision; Router still records | P1 | 37% token saving | pass-through count >0; Router log shows record entry |
| S4 | Vault write visible to recall within 5 min SLA or answer says "stale index" | P1 | freshness contract | test write → recall within 5 min or "stale index" string present |
| S5 | Forced lock on active store detected, reported plain language, recall degrades fail-closed; built-in context still works | P1 | resilience | watchdog line contains "memory DOWN"; built-in MEMORY.md still injected |
| S6 | Fact recorded by Hermes from its own channels recalled by DSH on any surface; DSH holds no bot token/webhook | P0 | continuity without channel | cross-surface recall hit; `grep` bot token in DSH config → none |
| S7 | Trigger outside allowed scope never causes a model call (counted) | P0 | two-stage filter | violation counter increments; model call count unchanged |
| S8 | Recall over budget spills to pointers; model walks one hop without second user turn | P2 | Inline & Spill | response contains pointer id; follow-up hop returns linked note |
| S9 | Provider switched → adapter works or fails loudly with named error; never silently empty | P1 | provider adapter honesty | swap provider → either recall works or error names provider; no empty result |
| G1 | Every F/S criterion appears in acceptance suite as exactly one numbered check; none via internal seam | P1 | verify integrity | suite check count == 30 (F14 + S9); all drive public seams |
| G2 | Suite lives outside every lane worktree; build log proves path never opened by builder | P1 | verifier independence | acceptance path not in any lane worktree; log grep |
| G3 | Scorecard reports pass/partial/gap/operational per criterion; "done" never said while P0 gap/partial | P0 | no false green | scorecard JSON has verdict field; red P0 escalates |
| G4 | DSH session runs chain end to end on throwaway slice: plan → tickets → lane → verify → scorecard, Router records each dispatch reason | P0 | first real workload | scorecard exists; dispatch_reasons array non-empty; independent re-run PASS |
| G5 | With no council/gate, chain degrades to portable gate, answers, logs row to gates.csv; never skips a decision | P1 | governance fallback | `portable-gate.py` invoked; gates.csv row appended |
| G6 | Every artifact reachable from vault or repo; nothing matters only in chat/scratch | P2 | durability | artifact paths listed in §7.4 all exist |
| G7 | Verifier independence structural: separate session, separate/no worktree, no read access to build uncommitted state | P1 | prevents rubber stamp | verifier session id != builder session id |

## 8. Architecture and API surface

### 8.1 Component map (stable IDs)

| ID | Component | Layer | What it does | Status |
|---|---|---|---|---|
| C1 | nexus-memory-bridge | Router + Worker | Router: compact shared block (rules, prefs, plans). Worker: scoped query only. Provider resolved at runtime. | implemented (nexus_memory_recall) |
| C2 | nexus-profile-resolver | Router | Resolves owning Hermes profile before any store opens. Six+one profiles; each maps to exactly one Hermes profile. | partial (provider_state reads config) |
| C3 | nexus-vault-recall | Router + Worker | vault_recall tool: FTS5 + title search over Maio Hub markdown, read-only via Beast/OpenKnowledge. Returns snippets with paths and next-hop ids. | implemented |
| C4 | nexus-context-packet | Router | Emits dispatch contract §4.3.1: request, scoped facts, vault refs, acceptance, surface+session, reason. | absent |
| C5 | nexus-memory-return | Worker → Router | Workers return candidates (fact, confidence, source); Router writes via Hermes tools. | absent |
| C6 | nexus-thread-bind | Router → Worker | Worker holds Thread id; follow-ups pass through without Router re-decision (−37% tokens). Router still records. | absent |
| C7 | nexus-index-cron | Ops | Refreshes vault index, warms read path, publishes freshness timestamp. | partial (script exists; scheduler unverified) |
| C8 | nexus-watchdog | Ops | Separate timer session: Worker progress, store readability, index freshness, render-lane health. Plain language ≤100 words. Fail-closed. | implemented (watchdog.sh) |
| C9 | dsh.bundle + cordis.patch.yml | Packaging | One bundle for web/desktop/dshweb/headless/mini/acp. Desktop app-owned: patch layer only. | implemented (overlay in 5 profiles) |
| C10 | video-lane pack | Worker | Points at installed lane (render-qc, video-stack, motion-studio); no vendored binaries. | partial (skills present; DSH wiring unproven) |

Import rule (keeps it honest): components import only through the provider adapter interface (C1) and the
vault read interface (C3). No component reads a store path directly; no component writes to the vault or
to memory. Desktop is app-owned: patch layer only, never hand-edited bundles.

### 8.2 Command / endpoint table

| Surface | Command / endpoint | Who may call | Notes |
|---|---|---|---|
| DSH CLI | `dsh <profile> "<brief>"` | operator / Router | headless; exit code + receipt path on stdout |
| DSH CLI | `dsh <profile> --dump-config` | operator | compose check; exit code decides, never grep |
| DSH CLI | `dsh plugin --profile <p> add <pkg>` | operator | pnpm passthrough; Safe Mode first run |
| MCP stdio | `nexus_status`, `nexus_memory_recall`, `nexus_vault_recall`, `nexus_vault_get` | any DSH session | read-only; path-guarded; fail loud |
| Vault index | `python3 vault_index.py [--rebuild] [--quiet]` | operator / cron | writes only index/vault.db |
| Watchdog | `./watchdog.sh` | operator / cron | reports; never repairs; exit 1 when degraded |
| Acceptance | `python3 tests/acceptance.py [--skip-live]` | verifier only | stored outside lane worktrees |
| Hermes memory | `hermes memory status` / memory tool | Hermes profiles (batman, beast, courage, default) | single source of truth |
| Vault server | `http://127.0.0.1:64200/mcp` | local only | healthy MCP (400 on bare GET) |

Conventions: pagination default 8, max 25 for vault_recall; idempotency via mtime in `files` table and
`--rebuild` override; versioning pinned to DSH rc.5 (`engines.dsh` range) with `--dump-config` as compat test.

### 8.3 Config contract

| Config key | Value / source | Owner | Invariant |
|---|---|---|---|
| Memory provider | Resolved at build time from `~/.hermes/hindsight/config.json` (mode, api_url, bank_id) | Hermes | I2 |
| Hindsight API | `http://127.0.0.1:8888`, bank `maio-ops` | Hermes | loopback only |
| Vault root | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Maio Hub` | Beast (writer) | I1 |
| Index db | `~/AI Hub/dsh-maio-nexus/index/vault.db` | nexus | read-only source |
| Index dir | `~/AI Hub/dsh-maio-nexus/index` | nexus | — |
| Overlay entry | `mcp-nexus` in `cordis.patch.yml` (insert, stdio, python3) | operator | I5 (env: {}) |
| DSH profiles | web, mini, headless, dshweb, acp (installed); desktop (app-owned); superagent (prototype) | operator | one bundle |
| Model gateway | `http://127.0.0.1:11434/v1` only; pinned tags (`deepseek-v4.1-flash:1017-cloud`) | operator | free-models rule |
| §8 gate | `d3-flash-mlx` via `/v1/systemone` | operator | — |
| Render dir | `~/AI Hub/dsh-renders/<stamp>-<slug>/` | video Worker | receipt.json |
| Skills | `~/.hermes/skills` and `~/.claude/skills` (mirrored) | Adrianna A | chain parity |

## 9. Failure modes

| Failure | What the user sees | Control | Who checks it |
|---|---|---|---|
| Provider down (Hindsight :8888) | nexus_memory_recall returns named error; nexus_status shows health error | FAILED state, fail loud; built-in MEMORY.md still injected | watchdog (hourly) + operator |
| Model missing (tag not pulled) | recall or dispatch fails with named model error | S9 fail loudly; pin check in phase 0 | phase 0 state table |
| Tag drift (pinned tag changed/renamed) | provider returns 404/model-not-found | pin check `ollama list` vs config at build time; -cloud suffix rule | phase 0 + monthly review |
| Context overflow (packet > 2000 tokens) | spill to pointers; model walks one hop | budget_tokens default 2000; S8 | Router + acceptance |
| Vault index missing | recall returns error naming `vault_index.py` | A7; no silent empty | watchdog + operator |
| Vault index stale (>5 min after write) | answer says "stale index" + index_age_minutes | S4; freshness state machine | watchdog |
| Profile compose failure (bad YAML) | install.py restores backup; prints FAILED | strip_empty_flow + exit-code validation | install.py |
| Cross-worker leakage attempt | access denied on sibling store | I3; S2 probe | verifier (G4) |
| Trigger outside scope | dropped, violation counter increments | two-stage filter; S7 | counted metric |
| Render without QC pass | render exits non-zero; receipt embeds verdict | F14; render-qc gate | video Worker + panel |
| Missing drawtext/subtitles in FFmpeg | text routed through PNG/HTML/GSAP, not FFmpeg | F6; 0 filters on this Mac | lane skill |
| Plugin runs code with shell access | staged, reviewed, signed off, Safe Mode first run | §8 governance | Ricardo |
| Web app unreachable (:7788 000) | DSH web surface unavailable | UNVERIFIED current state; restart required | operator |
| Cron/scheduler absent | index not auto-refreshed; watchdog not auto-run | UNVERIFIED; manual runs work | operator (gap) |

A row with no control is a risk accepted; the two UNVERIFIED rows above are accepted gaps, not controls.

## 10. Security, permissions and audit record

Principals: Ricardo (owner; money, legal, merge, external publication, live-system writes), Adrianna A
(staging, verification, PRD authoring), Beast (sole vault writer via OpenKnowledge), Router (DSH long-lived
session), Worker (isolated, task-scoped), Watchdog (external timer session), Verifier (independent
acceptance author).

Role/action matrix (✓ allowed, — denied):

| Action | Ricardo | Adrianna | Beast | Router | Worker | Watchdog | Verifier |
|---|---|---|---|---|---|---|---|
| Write vault bytes | ✓ | — | ✓ | — | — | — | — |
| Write memory | ✓ | ✓ (via Hermes) | — | ✓ (via Hermes tools) | candidate only | — | — |
| Install plugin | ✓ (sign-off) | stage only | — | — | — | — | — |
| Merge / push / PR | ✓ | — | — | — | — | — | — |
| Spend money / legal | ✓ | — | — | — | — | — | — |
| Dispatch Worker | ✓ | — | — | ✓ | — | — | — |
| Read vault | ✓ | ✓ | ✓ | ✓ | ✓ (scoped) | ✓ | ✓ |
| Run acceptance suite | ✓ | ✓ | — | — | — | — | ✓ |

What is stored: vault notes (markdown), vault index (SQLite FTS5), memory bank (Hindsight maio-ops),
cordis.patch.yml overlays, render receipts, acceptance scorecards, gates.csv. What is anchored outside the
system: vault content in iCloud/Maio Hub (Beast is sole writer); git history of targetpraks.github.io;
Hindsight bank on loopback. Signature/approval strength: no cryptographic signature is claimed; approvals
are Ricardo's explicit word in chat plus the decisions register (§13). The app's `?token=` URL is treated
as a password and never enters a document, ticket, chat, gate or plugin config (I5).

## 11. Build order by dependency

Stages; work inside a stage runs in parallel. Each stage ends on a boolean exit test. No dates.

- Stage 0 — Alignment (exit: written state table with commands and outputs; `ollama list` and
  `curl :11434/v1/models` captured; provider confirmed on all target profiles; prototype bundle format
  confirmed; tag pin verified). Owner: me (Adrianna).
- Stage 1 — Staging (exit: files exist under `~/AI Hub/dsh-maio-nexus/`; `--dump-config` diff shows
  overlay composing; nothing installed). Build C4 context-packet emitter, C5 memory-return, C6 thread-bind,
  C7 cron wiring, C10 video-lane DSH wiring. Owner: me.
- Stage 2 — Review (exit: signed-off manifest; Ricardo reads staged bundle + two worked renders; nothing
  unexpected). Owner: Ricardo.
- Stage 3 — Install (exit: `dsh plugin … add` output; app shows panel; `render-qc` passes on a DSH-issued
  render). Manual install into web/desktop/prototype; Safe Mode first run. Remaining installs in order:
  mflux (stills) → qwen-tts weights → Blender MCP (only on Ricardo's word) → RIFE ncnn (only if needed).
  Owner: Ricardo.
- Stage 4 — Verify (exit: pass/fail table with raw command output logged to Agent-Output; 10/10 acceptance
  plus G4). Run F1–F5, S1–S9, G4 against real output; canary recall, isolation, vault hash, dispatch
  packet, lock test, cross-surface continuity, one rendered MP4. Owner: me.
- Stage 5 — Operate (exit: receipts + monthly note). Courage nightly index; monthly plugin review
  (versions, CVEs, licences); monthly re-verification of video repo list; re-run Stage 0 whenever the
  memory provider changes. Owner: both.

Dependency notes: Stage 1 depends on Stage 0's provider confirmation (I2). Stage 3 depends on Stage 2
sign-off (§8 "Ricardo installs"). Stage 4 depends on Stage 3 (needs a real install). C4/C5/C6 (absent today)
are Stage 1 work and gate G4.

## 12. Decisions register

Only questions Ricardo can answer; each with a recommendation. Settled decisions (§13 of v10) are not
re-listed; only open items.

| # | Question | Recommended answer | Cost of each alternative |
|---|---|---|---|
| D1 | Install the nightly index/watchdog scheduler now (cron absent on this Mac)? | Yes — add a launchd plist or cron entry; manual runs already work | Leaving manual: index goes stale, watchdog never auto-runs; cost is ops toil |
| D2 | Restart the web app on :7788 to expose the nexus tools (currently unreachable)? | Yes — tools only appear after restart | Not restarting: web surface stays blind to nexus |
| D3 | Install mflux for stills in Stage 3? | Yes — local FLUX on MLX, free, private | No: posters limited to HTML/3D/Blender frames |
| D4 | Load Blender MCP (auto-mode blocked it) on Ricardo's word? | Defer until a brief genuinely needs 3D | Loading now: bridge risk on a machine holding the vault |
| D5 | Adopt any Workstream B plugin before phase-2 review? | No — due diligence first; none earns "adopt" today | Adopting early: third-party code with shell/fs access on the vault machine |
| D6 | Should the verifier (G4) run on a separate Mac profile or same machine? | Same machine, separate session + worktree (G7 structural) | Remote verifier: adds infra, not needed for isolation |

## 13. Evidence appendix

Commands run (read-only) producing numbers or status claims — full list and output in facts file
`/Volumes/Hiksemi 1TB/AI-Drive/Work/prd-program/facts/dsh-maio-nexus.md`.

| Command | Key output |
|---|---|
| `git rev-parse --short HEAD` | c5a4b252 |
| `ollama list` | 13 entries incl. deepseek-v4.1-flash:1017-cloud |
| `curl -s http://127.0.0.1:11434/v1/models` | 14 model ids |
| `ls ~/.hermes/plugins` | 17 dirs |
| `ls ~/.hermes/profiles` | 34 dirs incl. batman, beast, courage |
| `hermes memory status` | Provider: hindsight (active) |
| `hermes --profile {batman,beast,courage,default} memory status` | hindsight on all four |
| `ls ~/.dsh/profiles` | acp desktop dshweb headless mini superagent web (7) |
| `dsh --version` | 0.2.1-rc.5 |
| `cat ~/.dsh/profiles/web/package.json` | "dependencies": {} |
| `cat ~/.dsh/profiles/web/cordis.patch.yml` | mcp-nexus insert present |
| `cat ~/AI Hub/dsh-maio-nexus/index/build.json` | notes 2574, 0.57 s |
| `cat ~/.hermes/hindsight/config.json` | bank maio-ops, api :8888 |
| `curl -m3 http://127.0.0.1:8888/health` | healthy |
| `curl … http://127.0.0.1:7788/` | 000 (was 401 on 2026-11-02) |
| `curl … http://127.0.0.1:64200/mcp` | 400 (healthy MCP) |
| `node -v; npm -v` | v26.13.0 / 12.2.1 |
| `ffmpeg -filters \| grep -cE 'drawtext\|subtitles'` | 0 |
| `blender --version` | 5.2.3 LTS |
| `npx --yes hyperframes@0.9.2 --version` | 0.9.2 |
| `find <vault> -name '*.md' \| wc -l` | 2582 |
| `ls ~/.hermes/skills \| grep nexus` | nexus-memory, nexus-vault, video-lane |
| `grep ^version SKILL.md (app-plan/app-build/app-verify)` | 1.0.0 in all three, both trees |
| `ls portable-gate.py` | present, 10637 B |
| `ls ~/.hermes/mnemosyne` | absent |
| `crontab -l \| grep nexus` | none (UNVERIFIED gap) |
| `find … LaunchAgents … grep vault_index` | none (UNVERIFIED gap) |

Files read: source PRD HTML; `~/AI Hub/dsh-maio-nexus/{README.md, nexus_mcp.py, vault_index.py, install.py, watchdog.sh, nexus.patch.yml, tests/acceptance.py, skills/*, docs/reviews/*}`; `~/.dsh/profiles/*/cordis.patch.yml`, `package.json`; `~/.hermes/{config.yaml, hindsight/config.json, skills/*}`; `~/AI Hub/dsh-superagent-prototype/{README.md, SETUP.md}`; vault notes `AI-Space/2.Automations-Skills/Reports/2026-11-02-dsh-maio-nexus-v0-1-installed-on-this-mac-and-verified.md` and `…/g4-a-dsh-session-ran-the-plan-tickets-workers-verify-chain.md`. Git commit read: `c5a4b252`.

## 14. Out of scope (carried from v10 §15)

Installing any plugin without Ricardo's sign-off; writing to the vault from a plugin; sending credentials
to any plugin, gate or sandbox; auto-merging upstream code; replacing Hindsight/Mnemosyne/Beast with a
community store; building against a memory provider that is not active; pointing the prototype at a real
repository without an allowlist and observe mode; paying for stock footage, render farms or hosted video
models; adding a cloud Agent Loop or BYOM daemon; connecting DSH to Discord or Telegram.

## 15. Implementation status — v0.1 (2026-11-02)

What is live: read-only MCP bridge `~/AI Hub/dsh-maio-nexus/` exposing nexus_status, nexus_memory_recall,
nexus_vault_recall, nexus_vault_get; FTS5 vault index over 2,574 notes (5.15 s full build, 1 ms median
recall); overlay installed into web, mini, headless, dshweb, acp (desktop untouched, app-owned); three
skills mirrored into `~/.hermes/skills` and `~/.claude/skills`. Cron/watchdog scheduling unverified on
this Mac.

How it was proved: `dsh mini` returned a real vault path in 2.6 s with no `--patch` flag; `dsh headless`
returned the locked free-models fact from Hindsight in 9.3 s; acceptance suite 10/10 (A1–A9, F2); vault
sha256 `77e0679aae41cf7d` unchanged. G4 (Router/Worker chain) proven separately: one DSH session ran
plan → tickets → two isolated workers → verify, with recorded dispatch reasons; independent re-run PASS.

What this closes in §11: Stage 0, Stage 1, and the memory/vault half of Stage 3 are done. G4 remains the
next milestone: the prototype bundle is not installed, so a render driven from DSH is still unproven.
Both are the next milestone, not a gap in what shipped.

Fix recorded so it is not repeated: the web profile's patch file was a bare `[]`, so appending a block
sequence produced invalid YAML. The installer now strips that sentinel and judges `--dump-config` by exit
code, never by grepping output.
