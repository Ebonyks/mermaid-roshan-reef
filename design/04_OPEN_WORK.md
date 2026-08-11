# Master design — current work and historical triage

_Original consolidation: 2026-08-02. Re-triaged against
`audit/MASTER_AUDIT_2026-08-09.md` on 2026-08-09._

This is a navigation and lifecycle crosswalk, not a bug dump and not a set of
canonical finding records. The complete current index, evidence limits,
required finding fields, repair protocol and satisfaction gate live in the
dated master audit. An older `OW-*` item survives below so existing links and
decision history remain legible; it is actionable only where a current
`MA-*` item explicitly owns it.

Lifecycle words use the master-audit taxonomy. `HISTORICAL_EVIDENCE` is a
document-authority state, not an open finding. Never turn a dated report into a
current defect without reproducing its premise.

At the synchronized merged working-tree snapshot, GAME2D reports 509
model/export files, 68 production 3D files and 77 probe 3D files and remains
**`UNSATISFIED`**. The same inventory has 307 tracked Markdown paths, 192
GDScript files under `scripts/`, 105 probe scripts and an 8,519-line
`scripts/main.gd`. `NO_REGRESSION` is not completion. The overall master-audit
cycle is `REPAIRING`.

---

## Current lifecycle and acceptance-blocking work

| Current owner | Lifecycle | Current scope |
|---|---|---|
| `MA-2D-002` | `IN_PROGRESS` | Convert every remaining runtime/probe/scene/config/model category to strict-zero true Canvas/Node2D 2D; remaining 3D is shrinking debt, never scaffolding |
| `MA-DOC-001` | `IN_PROGRESS` | Reconcile current-authority documents with the 2026-08-09 medium decision and exact Godot 4.7.1-stable |
| `MA-DOC-002` | `CONFIRMED_OPEN` | Produce an exhaustive one-row-per-tracked-Markdown authority ledger with precise partial-supersession scope; this file does not pretend that is complete |
| `MA-DOC-003` | `BLOCKED_EXTERNAL` | Obtain the off-repository Alpha journal or replace it with a fresh equally scoped audit; do not assume its unnamed entries are fixed or open |
| `MA-DOC-004` | `IN_PROGRESS` | Track, index and gate the comprehensive design language and master audit |
| `MA-DOC-005` | `CONFIRMED_OPEN` | Create linked full records for material active items before calling them canonical findings |
| `MA-VIS-002` | `CONFIRMED_OPEN` | Replace Sky Lagoon's one mural layer with genuine Canvas/`Sprite2D` differential layers and prove seams, ownership, overdraw and runtime/device quality |
| `MA-VIS-003` / `MA-VIS-004` | `REPORTED_UNCONFIRMED` | Replace source-average palette/figure-ground diagnostics with state-local Canvas + HUD evidence before changing approved art |
| `MA-VIS-005` | `CONFIRMED_OPEN` | Validate occlusion for every relevant 2D card, not one aggregate role |
| `MA-VIS-006` | `CONFIRMED_OPEN` | Resolve all applicable visual review/manual/coverage gaps with commit-pinned evidence |
| `MA-PLAY-001` | `CONFIRMED_OPEN` | Prove every current child-visible destination from a fresh save without direct/debug entry, including return, re-entry, touch, voice and save behavior |
| `MA-ACCESS-001` / `MA-ACCESS-002` / `MA-ACCESS-003` | `BLOCKED_EXTERNAL` | Obtain authorized exact objective recordings/diegetic equivalents, the Lamba semantic recording, and Evie's exact Seek tap-tree cue; protected family audio must not be modified |
| `MA-TOUCH-001` | `FIXED_PENDING_VERIFICATION` | Complete target-phone hold/drag/multitouch/focus-loss evidence |
| `MA-DOLLS-001` | `VERIFIED_FIXED` | Faron's catcher is a bounded Canvas activity with real touch, passive safety, save/medal/replay and teardown evidence |
| `MA-SEEK-001` | `VERIFIED_FIXED` | Animated Evie/Lamb-a' Canvas meadow supersedes the vinyl pair card, low-grade preview bush and four retired meadow GLBs; exact Evie objective speech remains `MA-ACCESS-003` |
| `MA-OPERA-001` | `FIXED_PENDING_VERIFICATION` | Chef behavior/art routing and the resolved merged-worktree local full suite are green; final-SHA two-aspect capture, device and owner review still decide closure |
| `MA-OPERA-002` / `MA-OPERA-004` | `CONFIRMED_OPEN` | Detective's painted crown is not proved healed, and no complete accepted all-career capture matrix exists |
| `MA-OPERA-003` / `MA-OPERA-006` | `CONFIRMED_OPEN` | Split and re-audit the remaining fallback/art-fiction/voice subclaims; several subclaims changed, so the older grouped wording cannot be closed or imported wholesale |
| `MA-OPERA-005` | `FIXED_PENDING_VERIFICATION` | Latest Ballerina atlas and three-act specialist pass the local full suite and exact-head remote gate; authoritative capture, device, child and owner review remain |
| `MA-OPERA-007` | `OWNER_DECISION_REQUIRED` | Decide the above-water Farmer/Doctor setting before treating it as a defect or repair |
| `MA-OPERA-008` | `VERIFIED_FIXED` | Racer uses one true-Canvas Tune / To the Line / racing-circle path and exact lap-two cue; the rejected device-only 3D kart branch is superseded |
| `MA-OPERA-009` | `FIXED_PENDING_VERIFICATION` | Dedicated five-phase one-finger Canvas Boxer passes the local full suite and exact-head remote gate; authoritative capture, device, child and owner review remain |
| `MA-AUDIO-001` | `FIXED_PENDING_VERIFICATION` | 42 deterministic new cues pass local machine gates and the pinned-Windows exact-head job verifies 42/42 deliveries; human two-wrap listening, voice intelligibility, mono fold-down and Lenovo M11 mix review remain |
| `MA-CI-002` | `VERIFIED_FIXED` | V3 exact-head at `dacef1405b6a8cb470117e824aebac3a8ca500af`, GitHub run `31457593351`, succeeds in 34m19s: 63 local / 62 remote trusted entries differ only by the human-art display probe, and all 62 remote entries pass |
| `MA-CI-003` | `CONFIRMED_OPEN` | Give every one of the 105 probe scripts exactly one trusted, runtime-visual, advisory, diagnostic, obsolete or quarantined classification |
| `MA-CHANGE-001` | `VERIFIED_FIXED` | CHG-001–023 assign 67 owned source commits plus seven topology commits, all 74 reachable audit commits through `dacef140`; the written ledger and read-only planner agree exactly, only three guarded diagnostics emit scripts, and 15 unit plus independent adversarial checks are green |
| `MA-PERF-001` / `MA-CHILD-001` | `BLOCKED_EXTERNAL` | Record exact-release device performance and an observed child golden path |
| `MA-RELEASE-001` | `FIXED_PENDING_VERIFICATION` | Resolved integration content at `ad36ee9f` completes exact Godot 4.7.1 local `scripts/ci.sh` in 826.4 seconds; exact audit/CI head `dacef140` completes remote run `31457593351` in 34m19s with Windows music 42/42 and Ubuntu static/import/analyzer/62 trusted probes/boot/balance/five diagnostic capture-upload pairs green. Matching APK, authoritative visual, listening, device, child, owner and strict-2D evidence remain open |

Current P2/owner-decision work remains indexed in the master audit: asset
orphans/NPOT residency, exhaustive probe classification, the standalone
fire-arena role, combat/device review,
remaining Opera gaps, audio listening, and structural code debt. Roshan atlas
repacking is `DEFERRED_WITH_REASON`; universal costume layers are
`DISMISSED_NOT_A_DEFECT`.

`MA-ASSET-005` is also `DISMISSED_NOT_A_DEFECT` as a source-UID finding:
tracked sponge/starfish GLBs and sidecars validate, and an isolated fresh import
is warning-free. Four stale ignored local `.godot/imported` cache files caused
the warnings. Those GLBs remain ordinary 3D-removal debt under `MA-2D-002`;
the cache diagnosis does not approve them for the final medium.

---

## Historical `OW-*` crosswalk

<a id="ow-1"></a>
### OW-1 — authority-file contradiction

`IN_PROGRESS` under `MA-DOC-001`. On 2026-08-02, `CLAUDE.md` described the
2.5D/Meshy direction differently from `AGENTS.md`, and both quoted stale code
counts. The authorized 2026-08-09 reconciliation replaces both current
directions with true 2D. Closure still needs the documentation gate; editing
the prose alone is not a verified fix.

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

`CONFIRMED_OPEN` as `MA-VIS-005`, with its old depth-buffer prescription
`SUPERSEDED`. The current requirement is explicit 2D `z_index`/Canvas ordering
for every relevant card while Roshan remains findable.

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
total / 45 outside” count is stale. The merged tree counts 105 probe scripts,
with 63 local and 62 remote trusted entries; the sole intended loop difference
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
symptoms must not be imported as stale findings.

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
`main.gd` is 8,519 lines, and string state, duplicated input, save frequency,
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
3. Complete capture/device/child/owner acceptance for the merged
   Ballerina/Boxer/Racer repairs, close current Opera art defects and the
   confirmed Lagoon Canvas layering defect;
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
