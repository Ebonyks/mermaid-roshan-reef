# Master design — current work and historical triage

_Original consolidation: 2026-08-02. Re-triaged against
`audit/MASTER_AUDIT_2026-08-09.md` on 2026-08-09; synchronized through product/
runtime commit `09e5e35665fd8d1bd782693e10fc0198f756d2c8`, probe-readiness/full-local
head `ff068db002202839f920a6f9fb78c942788a3034`, and audit/evidence authority
head `9befc0f838f40eead2f42088a91206257fe217a8` on 2026-08-13. Historical
merge-integration checkpoint is `f3b0de07`; historical exact-head CI-repair
checkpoint is `af4189a9`; latest completed full-local checkpoint is `ff068db`;
current exact-head verification is successful run `31686380560` at `9befc0f8`.
Pre-fix run `31678156887` at `3fc151c8` remains historical red evidence for
fixed-frame Opera reveal sampling. Matching APK and external acceptance remain
open._

This is a navigation and lifecycle crosswalk, not a bug dump and not a set of
canonical finding records. The complete current index, evidence limits,
required finding fields, repair protocol and satisfaction gate live in the
dated master audit. An older `OW-*` item survives below so existing links and
decision history remain legible; it is actionable only where a current
`MA-*` item explicitly owns it.

Lifecycle words use the master-audit taxonomy. `HISTORICAL_EVIDENCE` is a
document-authority state, not an open finding. Never turn a dated report into a
current defect without reproducing its premise.

At historical exact merge `f3b0de07`, GAME2D recorded the 68-production/
77-probe checkpoint. The current Opera repair reports 509 model files/509 active
exports, 157 tracked sidecars, 352 active-untracked generated sidecars, 66
production 3D files, 74 probe 3D files, one scene, and one configuration and
remains **`UNSATISFIED`**. Exact regression is `NO_REGRESSION`, all 14 stress
controls pass, and strict remains open. The `f3b0de07` inventory had 315 tracked Markdown paths, 195
GDScript files under `scripts/`, 106 probe scripts and an 8,519-line
`scripts/main.gd`; runtime `09e5e356` retains 195/106 and has an 8,647-line
`scripts/main.gd`. `NO_REGRESSION` is not completion. The overall master-audit
cycle is `REPAIRING`. Product/audit commit `09e5e356` passes its exact focused
matrix and a full local `scripts/ci.sh` run under official Godot
`4.7.1.stable.official.a13da4feb`: exit 0 after 1463.4 seconds, all 64 trusted
local probes, 74 GAME2D unit tests, 14 stress controls, and 93 visual-contract
unit tests green. Probe-only `ff068db` preserves the runtime and passes a newer
full local suite in 1379.3 seconds with all 64 trusted probes. Its Castle interaction approval candidate
`1754c880e4ef3df87daed47e1a8ec1ed36e114956ae86dbc50a74e40bba392d9`
covers 13 assets/104 frames in the machine/review ledger. Twenty-two rendered
1280×720 Mobile captures (nine routes and thirteen careers) were visually
inspected for diagnosis/review only;
neither the candidate nor those V4 captures grant device, child, owner, or
authoritative visual acceptance. Current exact-head run `31686380560` succeeds
at authority SHA `9befc0f838f40eead2f42088a91206257fe217a8`: the probes job runs
09:24:08–09:57:48 UTC (33m40s) with exactly 63 remote trusted probe headings,
and static checks, import, full analyzer, trusted probes, boot, Dust and Opera
advisories, and the Opera manifest are green. Windows runs
09:24:08–09:27:55 UTC (3m47s) and ends
`MUSIC|check 42/42|picture_xmas`. Remote GAME2D is exact 509/66/74
`NO_REGRESSION`/`UNSATISFIED`. All five capture/upload pairs completed at the
workflow level and uploaded diagnostic artifacts, not capture gates or visual passes. Raw Sky
Lagoon `LAGOONSHOT` output has 21 `OK`, 44 `FAIL`, and `DONE` (66 diagnostic
lines), so that diagnostic internally fails. The run is not warning-clean:
existing Vulkan-surface
fallback to OpenGL 3 and ObjectDB/resource/texture-leak diagnostics remain.
Run `31678156887` at `3fc151c8` remains historical red evidence because
Detective/Nursery were sampled four frames into the 0.25-second reveal;
`ff068db` replaces that guess with bounded fail-closed semantic readiness.
Matching APK, authoritative visual, exact voice, listening, device, child,
owner, and strict-zero 2D evidence remain open. The nine current room
captures also show residual P2 lower-body/tail occlusion from the route cards.
The global visual result is unchanged at 16 FAIL, 17 REVIEW_OPEN, two
MANUAL_OPEN, 86 COVERAGE_GAP, 32 PASS, and 94 NOT_APPLICABLE.

---

## Current lifecycle and acceptance-blocking work

| Current owner | Lifecycle | Current scope |
|---|---|---|
| `MA-2D-002` | `IN_PROGRESS` | Convert every remaining runtime/probe/scene/config/model category to strict-zero true Canvas/Node2D 2D; remaining 3D is shrinking debt, never scaffolding |
| `MA-DOC-001` | `VERIFIED_FIXED` | Current authority documents are reconciled to the 2026-08-09 true-2D decision and exact Godot 4.7.1-stable; exhaustive per-document classification remains separately open as `MA-DOC-002` |
| `MA-DOC-002` | `CONFIRMED_OPEN` | Produce an exhaustive one-row-per-tracked-Markdown authority ledger with precise partial-supersession scope; this file does not pretend that is complete |
| `MA-DOC-003` | `BLOCKED_EXTERNAL` | Obtain the off-repository Alpha journal or replace it with a fresh equally scoped audit; do not assume its unnamed entries are fixed or open |
| `MA-DOC-004` | `VERIFIED_FIXED` | The comprehensive design language and master audit are tracked, indexed and admitted through the narrow audit-source exception; later synchronization drift reopens this finding |
| `MA-DOC-005` | `CONFIRMED_OPEN` | Create linked full records for material active items before calling them canonical findings |
| `MA-VIS-002` | `CONFIRMED_OPEN` | Replace Sky Lagoon's one mural layer with genuine Canvas/`Sprite2D` differential layers and prove seams, ownership, overdraw and runtime/device quality |
| `MA-VIS-003` / `MA-VIS-004` | `REPORTED_UNCONFIRMED` | Replace source-average palette/figure-ground diagnostics with state-local Canvas + HUD evidence before changing approved art |
| `MA-VIS-005` | `VERIFIED_FIXED` | The visual contract now proves unique target ownership, effective descendant Canvas order and decoded-alpha overlap per relevant card; missing live product evidence remains open as `MA-VIS-006` |
| `MA-VIS-006` | `CONFIRMED_OPEN` | Resolve all applicable visual review/manual/coverage gaps with commit-pinned evidence |
| `MA-PLAY-001` | `CONFIRMED_OPEN` | Prove every current child-visible destination from a fresh save without direct/debug entry, including return, re-entry, touch, voice and save behavior |
| `MA-ACCESS-001` / `MA-ACCESS-002` / `MA-ACCESS-003` | `BLOCKED_EXTERNAL` | Obtain authorized exact objective recordings/diegetic equivalents, the Lamba semantic recording, and Evie's exact Seek tap-tree cue; protected family audio must not be modified |
| `MA-TOUCH-001` | `FIXED_PENDING_VERIFICATION` | Complete target-phone hold/drag/multitouch/focus-loss evidence |
| `MA-DOLLS-001` | `VERIFIED_FIXED` | Faron's catcher is a bounded Canvas activity with real touch, passive safety, save/medal/replay and teardown evidence |
| `MA-SEEK-001` | `VERIFIED_FIXED` | Animated Evie/Lamb-a' Canvas meadow supersedes the vinyl pair card, low-grade preview bush and four retired meadow GLBs; exact Evie objective speech remains `MA-ACCESS-003` |
| `MA-OPERA-001` | `FIXED_PENDING_VERIFICATION` | Chef behavior/art routing passes runtime `09e5e356` and the latest full-local probe head `ff068db`; predecessor `e2c25878` retains its historical local proof. Final-SHA two-aspect capture, device and owner review still decide closure |
| `MA-OPERA-002` / `MA-OPERA-004` | `CONFIRMED_OPEN` | Detective's painted crown is not proved healed, and no complete accepted all-career capture matrix exists |
| `MA-OPERA-003` / `MA-OPERA-006` | `CONFIRMED_OPEN` | Split and re-audit the remaining fallback/art-fiction/voice subclaims; several subclaims changed, so the older grouped wording cannot be closed or imported wholesale |
| `MA-OPERA-005` | `FIXED_PENDING_VERIFICATION` | Latest Ballerina atlas and three-act specialist pass runtime `09e5e356` and latest full-local probe head `ff068db`; predecessor `e2c25878` and exact-head run `31661887863` at `e0677ae4` retain historical proof. Run `31678156887` is red only for route-readiness sampling, not Ballerina behavior. Authoritative capture, device, child and owner review remain |
| `MA-OPERA-007` | `OWNER_DECISION_REQUIRED` | Decide the above-water Farmer/Doctor setting before treating it as a defect or repair |
| `MA-OPERA-008` | `VERIFIED_FIXED` | The Canvas Racer's lap-two cue and finale defect are fixed. The formerly separate ordinary-headless source split is tracked independently as current `MA-OPERA-010` `FIXED_PENDING_VERIFICATION` evidence |
| `MA-OPERA-009` | `FIXED_PENDING_VERIFICATION` | Dedicated five-phase one-finger Canvas Boxer passes runtime `09e5e356` and latest full-local probe head `ff068db`; predecessor `e2c25878` and exact-head run `31661887863` at `e0677ae4` retain historical proof. Run `31678156887` is red only for route-readiness sampling, not Boxer behavior. Authoritative capture, device, child and owner review remain. Boxer V2 is only a separate docs-branch proposal |
| `MA-OPERA-010` | `FIXED_PENDING_VERIFICATION` | Commit `e2c25878` uses one Canvas lifecycle for ordinary unforced and display entry and contains no external-kart route. Exact focused, full local, and exact-head remote lifecycle/passive/teardown/re-entry evidence is green; external acceptance remains |
| `MA-OPERA-011` | `FIXED_PENDING_VERIFICATION` | Commit `e2c25878` removes the three owner-cut bosses from cards, gates, completion, and runtime. Save slots 4/9/14 are permanent raw-preserving tombstones, live mask is `0xBDEF`, and focused, full local, and exact-head remote migration/reward/suspend/leave evidence is green; external acceptance remains |
| `MA-OPERA-012` | `FIXED_PENDING_VERIFICATION` | Runtime `09e5e356` distributes all thirteen careers through exact Castle rooms, resolves Racer to Movie Lounge, deletes the all-career lobby with no hidden backdoor, preserves sparse save/reward identity, restores the exact launching room, and fixes layers. Probe-only `ff068db` adds bounded fail-closed semantic readiness and passes the 1379.3-second/64-probe full-local gate. Exact authority head `9befc0f8` passes run `31686380560` with 63 remote trusted headings, but the run is not warning-clean; its five workflow-completed/uploaded diagnostic pairs are non-authoritative and raw Sky Lagoon output internally fails. APK/device/child/owner/exact-voice/accepted-visual gates and residual P2 card occlusion remain open |
| `MA-AUDIO-001` | `FIXED_PENDING_VERIFICATION` | 42 deterministic new cues pass local machine gates; exact authority-head run `31686380560` passes Windows in 3m47s and ends `MUSIC|check 42/42|picture_xmas`. Human two-wrap listening, voice intelligibility, mono fold-down and Lenovo M11 mix review remain open |
| `MA-CI-002` | `VERIFIED_FIXED` | Current parity is 64 local / 63 remote trusted entries with only the human-art display probe local. Runtime `09e5e356` completes all 64 locally in 1463.4 seconds; probe/evidence head `ff068db` preserves runtime and is the latest full-local checkpoint at 1379.3 seconds/all 64 under exact Godot 4.7.1. Exact authority-head run `31686380560` executes exactly 63 remote trusted headings successfully at `9befc0f8`; machine gates are green, but existing Vulkan/resource-leak warnings and the internally failed Sky Lagoon diagnostic remain |
| `MA-CI-003` | `CONFIRMED_OPEN` | Give every one of the 106 probe scripts exactly one trusted, runtime-visual, advisory, diagnostic, obsolete or quarantined classification |
| `MA-CHANGE-001` | `VERIFIED_FIXED` | CHG-001–028 cover 75 unique catalog-owned commit references. CHG-027 owns Opera distribution runtime `09e5e356` plus probe-readiness `ff068db`; CHG-028 owns material rollback-control `d991fdf3` plus authority `9befc0f8` synchronization as a narrow exception while routine self-hash/count maintenance remains CHG-023. The written ledger and read-only planner agree exactly, only CHG-020/021/022/024 emit guarded scripts, the other 24 refuse automation, and 22 unit plus independent adversarial checks are green |
| `MA-PERF-001` / `MA-CHILD-001` | `BLOCKED_EXTERNAL` | Record exact-release device performance and an observed child golden path |
| `MA-RELEASE-001` | `FIXED_PENDING_VERIFICATION` | Historical merge `f3b0de07` completes exact local CI in 1437.1 seconds with 64 probes; failed `31648427712` and repaired replacement `31649113587` preserve the newline-hash history. Runtime `09e5e356` completes full local CI in 1463.4 seconds/all 64; probe-only `ff068db` passes full local in 1379.3 seconds/all 64. Exact authority head `9befc0f8` passes run `31686380560`; all five capture/upload pairs completed at the workflow level and uploaded diagnostic/non-authoritative artifacts, Sky Lagoon internally fails, and the run is not warning-clean. Matching APK, authoritative visual, exact voice/listening, device, child, owner and strict-2D evidence remain open |

Current P2/owner-decision work remains indexed in the master audit: asset
orphans/NPOT residency, exhaustive probe classification, the standalone
fire-arena role, combat/device review,
remaining Opera gaps, audio listening, and structural code debt. Roshan atlas
repacking is `DEFERRED_WITH_REASON`; universal costume layers are
`DISMISSED_NOT_A_DEFECT`.

Branch status is not implementation status: current Candymaker is integrated;
Painter-purpose and Arborist worktrees are uncommitted candidates; Boxer V2 is
docs-only on a separate branch. None expands the current 13-career table, and
none changes the owner-directed Castle-room distribution or revives the three
cut Opera bosses.

The sealed Castle Kitchen controller was deliberately excluded from this
repair. Its current Chef configuration is valid and covered by focused probes,
so no child-facing start failure is reproduced. Handling a hypothetical future
invalid `OperaAct.start()` result at that caller is separate `MA-CODE-002`
hardening and requires renewed owner visual approval before the Castle file is
changed.

`MA-ASSET-005` is also `DISMISSED_NOT_A_DEFECT` as a source-UID finding:
tracked sponge/starfish GLBs and sidecars validate, and an isolated fresh import
is warning-free. Four stale ignored local `.godot/imported` cache files caused
the warnings. Those GLBs remain ordinary 3D-removal debt under `MA-2D-002`;
the cache diagnosis does not approve them for the final medium.

---

## Historical `OW-*` crosswalk

<a id="ow-1"></a>
### OW-1 — authority-file contradiction

`VERIFIED_FIXED` under `MA-DOC-001`. On 2026-08-02, `CLAUDE.md` described the
2.5D/Meshy direction differently from `AGENTS.md`, and both quoted stale code
counts. The authorized 2026-08-09 reconciliation replaces both current
directions with true 2D, and the tracked/indexed authority gate now verifies
that repair. Exhaustive classification of every Markdown file remains the
separate open `MA-DOC-002` scope.

<a id="ow-2"></a>
### OW-2 — missing `world_style` reversibility toggle

`DISMISSED_NOT_IN_PROJECT`. The 2026-07-27 charter required a route back to the
3D world. The 2026-08-09 final-medium decision supersedes dimensional rollback;
adding this toggle would restore a rejected production direction. General
feature flags may still protect unrelated risky behavior changes.

<a id="ow-3"></a>
### OW-3 — Sky Lagoon is one mural, not a layer stack

`CONFIRMED_OPEN` as `MA-VIS-002`. The durable problem is the absence of
differential visual layers. Closure must use true Canvas/`Sprite2D` layers;
`SideScrollStage`, `Sprite3D`, a filename change or 3D tap projection cannot
close it.

<a id="ow-4"></a>
### OW-4 — per-object occlusion is not proved

`VERIFIED_FIXED` as `MA-VIS-005`, with its old depth-buffer prescription
`SUPERSEDED`. The visual contract now validates unique target ownership,
effective descendant Canvas order and decoded-alpha overlap for each relevant
card. Missing live product evidence remains separately open as `MA-VIS-006`.

<a id="ow-5"></a>
### OW-5 — source-average palette/figure-ground report

`REPORTED_UNCONFIRMED` as `MA-VIS-003`/`MA-VIS-004`. The 2026-07-28 values are
historical diagnostics, not authority to repaint. The metric averages mutually
exclusive and non-rendered files; reproduce a state-local Canvas/HUD composite
first. Fairy is likely a false positive; Lagoon is a plausible but unconfirmed
hierarchy risk.

<a id="ow-6"></a>
### OW-6 — world reachability lacks a full proof

`CONFIRMED_OPEN` as `MA-PLAY-001`. A Lagoon-to-Reef route has focused evidence,
but no current fresh-save no-cheat traversal covers the whole player-visible
graph. The 2026-08-02 destination list is historical and must be freshly
enumerated before repair.

<a id="ow-7"></a>
### OW-7 — reef pilot / migration-order violation

`DISMISSED_NOT_A_DEFECT`. Sky Lagoon shipping before the proposed pilot is
useful `HISTORICAL_EVIDENCE` about process, but cannot be repaired
retroactively and does not authorize the old 2.5D migration order.

<a id="ow-8"></a>
### OW-8 — engine-consolidation backlog

`SUPERSEDED` as a single queue. Duplicated input remains a current risk under
`MA-CODE-002`; E1/Zelda expansion is `DEFERRED_WITH_REASON`; Spline3,
physical-standee and other 3D prescriptions are superseded. Conversion work
must be behavior-preserving true 2D, not speculative engine growth.

<a id="ow-9"></a>
### OW-9 — asset hygiene and weight

The 2026-07-28 counts are `HISTORICAL_EVIDENCE`, superseded by current
`MA-ASSET-001` and `MA-ASSET-004` measurements: Castle 2.1 MB (9/15 PNGs),
Galaxy 11.7 MB (32/32), Opera 166.5 MB (453/548), Lagoon 41.9 MB (48/90), and
Lagoon 10/41 NPOT textures with about 11.6 MB uncompressed simultaneous
residency. Delete only after reachability, provenance, archive and surrounding
tests. A string-reference orphan report is review evidence, not proof that a
dynamically loaded atlas is unreachable.

<a id="ow-10"></a>
### OW-10 — incomplete visual-audit evidence

`CONFIRMED_OPEN` as `MA-VIS-006`. The current issue is broader than flipping a
command-line flag: every applicable review, manual item and coverage gap needs
commit-pinned evidence, and the audit must measure the final Canvas runtime.

<a id="ow-11"></a>
### OW-11 — screen-space living-world overlay

`SUPERSEDED` as a 3D-depth repair prescription. The 2026-08-02 observation is
historical evidence. Any current overlay defect must be freshly reproduced
against `DL-LAY-*`; retained ambient art belongs in intentional 2D Canvas/
parallax roles and remaining spatial staging belongs to `MA-2D-002`.

<a id="ow-12"></a>
### OW-12 — old probe-count gap

`SUPERSEDED` by the split `MA-CI-002` / `MA-CI-003` lifecycle. The old “96
total / 45 outside” count is stale. The merged tree counts 106 probe scripts,
with 64 local and 63 remote trusted entries; the sole intended loop difference
is display-only `probe_human_art_audit`. Blocking-loop parity is fixed locally
and `VERIFIED_FIXED` remotely under `MA-CI-002`: exact head
`dacef1405b6a8cb470117e824aebac3a8ca500af` completes GitHub run
`31457593351` successfully in 34m19s with all 62 remote trusted probes green.
Exhaustive one-class-per-probe disposition remains `CONFIRMED_OPEN` under
`MA-CI-003`.

<a id="ow-13"></a>
### OW-13 — proposed world-map geography

`DEFERRED_WITH_REASON`. The mirror axis, kelp placement, seam form and preview
scope were never approved. They are not current bugs. `MA-PLAY-001` owns the
separate requirement to prove the graph that actually ships.

<a id="ow-14"></a>
### OW-14 — old Opera request inventory

`SUPERSEDED` as a queue by the later August 3–9 Opera audits and scoped
specialist documents. `BALLERINA_PARTY_REBUILD_2026-08-09.md` now controls
Ballerina, `design/BOXING_GAME_PROJECT_2026-08-09.md` controls Boxer, and
`MA-OPERA-008` controls the reconciled Canvas Racer. Their earlier Ballerina,
Boxer and real-kart sections are historical; previously closed request
symptoms must not be imported as stale findings. This queue supersession does
not erase the distinct direct owner directions now owned by `MA-OPERA-011` and
`MA-OPERA-012`: cut the three Opera bosses with tombstoned slots, and distribute
the thirteen careers through Castle rooms instead of the all-career hub.

<a id="ow-15"></a>
### OW-15 — Lamba audio still uses the legacy noun

`BLOCKED_EXTERNAL` as `MA-ACCESS-002`. The visual/semantic role changed, but
the protected recording still says “bunny-fish.” Closure requires an
owner-approved recording or re-render plus exact-key and device-listening
evidence. Do not edit or substitute protected audio without authorization.

<a id="ow-16"></a>
### OW-16 — dungeon lock-and-key redesign

`DEFERRED_WITH_REASON`. This is optional future design, not a defect in the
current game and not implementation authorization. Existing dungeon behavior,
if retained, still requires true-2D conversion and normal no-fail testing.

<a id="ow-17"></a>
### OW-17 — Zelda-grammar verb expansion

`DEFERRED_WITH_REASON`. Grab/push/switch and the proposed E1 growth path wait
until the current game, conversion and device evidence are complete. Zelda
remains a mechanics reference only; no Zelda content may enter the project.

<a id="ow-18"></a>
### OW-18 — broad CC0-to-original campaign

`DEFERRED_WITH_REASON` as a broad campaign. Address named live defects one at a
time, reuse approved art first, preserve provenance, and never mass-delete or
redesign for novelty. An old asset is removed only after its replacement or
non-reachability proof and surrounding gates are green.

<a id="ow-19"></a>
### OW-19 — Meshy migration and missing key

`SUPERSEDED` / `DISMISSED_NOT_IN_PROJECT`. The migration is removed, not
paused; the absent API key is not a blocker. `NPC_3D_WORKORDER_2026-07-19.md`
and related batches are historical evidence and must never be submitted.

<a id="ow-20"></a>
### OW-20 — structural code debt

`CONFIRMED_OPEN` only through fresh `MA-CODE-001`/`MA-CODE-002` evidence:
`main.gd` is 8,647 lines at current `09e5e356`, and string state, duplicated input, save frequency,
material churn and remaining 3D glue are risks. Specific July dead-code claims
are historical leads until reproduced.

<a id="ow-21"></a>
### OW-21 — device and child evidence absent

`BLOCKED_EXTERNAL` as `MA-PERF-001`/`MA-CHILD-001`, with phone-only touch and
combat review tracked separately. Headless inference cannot establish frame
pacing, thermal behavior, touch latency, audio intelligibility, phone-size
readability or child comprehension.

---

## Repair order

Follow the current order in `audit/MASTER_AUDIT_2026-08-09.md`, not the 2026-08-02
OW ordering:

1. Finish authority/document controls and full finding records.
2. Continue one tested true-2D gameplay family at a time until every GAME2D
   category is zero.
3. Finish verification of the focused Opera lifecycle/boss-retirement/
   Castle-distribution repair:
   keep slots 4/9/14 as raw-preserving tombstones, the live mask at `0xBDEF`,
   and one Canvas entry path while preserving the green full-local and exact
   authority-head run `31686380560` evidence while completing matching APK and
   external acceptance. Preserve all thirteen exact Castle-room
   owners, Movie Lounge Racer, the deleted all-career lobby, and exact-room
   return. Move/restage the route cards so Roshan's lower body/tail remains
   visible without shrinking touch targets. Complete
   capture/device/child/owner acceptance for the merged Ballerina/Boxer/Racer
   repairs, close current Opera art defects and the confirmed Lagoon Canvas layering defect;
   establish state-local visual evidence before changing art.
4. Resolve protected voice gaps through authorized sources.
5. Re-enumerate and prove the child-visible world graph.
6. Preserve the verified blocking-loop parity guard and classify every probe;
   retire only with explicit evidence.
7. Complete music listening/voice/mono/device review, keep the same-SHA full
   suite green after changes, then complete capture, device and child gates and
   repeat the
   master audit from `INVENTORYING`.

No state in this document permits calling the game or master audit satisfied.
