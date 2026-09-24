# Mermaid Roshan: Reef of Light — game-wide master audit

## 0. Planning entry

Planning guidance updated 2026-09-05 against integration source `775ceee1`.
This is a document/selected-fact review, not a new whole-game runtime audit.
The dated evidence below retains its original commit and acceptance limits;
"current" claims in that sealed snapshot do not describe today's build.
Game-wide audit satisfaction remains **UNSATISFIED**.

| Planning question | Current answer and authority |
|---|---|
| How should an agent develop a chapter? | Use the [chapter guide](../design/09_CHAPTER_DEVELOPMENT_GUIDE.md) and [brief](../design/templates/CHAPTER_BRIEF_V1.md). The owner approves premise/boundaries; the agent develops the playable result within them, without another routine planning/expansion checkpoint. |
| How much invention is delegated? | Owner decision 2026-09-05 permits minor characters/optional threads preserving canon and free reuse, modification, and combination of mechanics within child/save/medium rules. Major character/plot changes remain reserved. |
| How should unused assets inform the plan? | Strategically shortlist existing families for story/play benefit, thematic fit, readiness, and integration cost. Suitable discoveries may shape activities within scope. Unused status alone is neither approval nor a reason for inclusion. |
| Which chapter sources control? | [Chapter 2 spine](../design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md), [cake progression](../design/CHAPTER2_CAKE_VISUAL_PROGRESSION_2026-08-31.md), and scoped [early Chapter 3 route](../design/FAIRY_CONSERVATORY_CHAPTER3_2026-08-30.md). |
| Where does Northern/Ice World development belong? | [Northern planning branch](../design/chapters/NORTHERN_ICE_WORLD.md), now with a [Nordic/Christmas draft and visual guide](../design/chapters/NORTHERN_CHRISTMAS_DRAFT.md): preserve the existing art investment, remix restaurant cooking with customer orders, and explore returning/new careers. Design exploration is authorized; runtime implementation and the proposed chapter ending are not commissioned by this entry. |
| Where are canon and reusable examples? | [Chapter reference library](../design/10_CHAPTER_REFERENCE_LIBRARY.md), including acceptance limits and asset discovery sources. Seed entries are static references, not newly accepted exemplars. |
| What facts must be refreshed? | Engine pins in [godot_baseline.json](../tools/godot_baseline.json); global `OPERA_ACTIVE_STAR_MASK` in [SaveState](../scripts/save_state.gd); actual code/probe availability; scoped owner decisions in the ledger. |
| What blocks what? | A missing cue, device session, or owner decision blocks its dependent work or acceptance claim. Continue independent authorized work. Shared regression/integration gates and strict-zero whole-game 2D satisfaction retain their scopes. |
| What makes menus, arrows and teaching cues visually consistent? | The [Pearl Stage UI language](../design/11_UI_PEARL_STAGE_LANGUAGE.md), governed by `DL-UI-VIS-01` through `DL-UI-VIS-10`: painted shell/pearl surfaces, rainbow flourishes, grouped ornament and clear picture-first actions. Reuse its component and review packet across the game. |

### UI design branch — 2026-09-05

Owner commissioned a richer, slightly maximalist Roshan UI family inspired by
the opera-house worlds, beginning with menu concepts. Work branch:
`codex/ui-opera-design-language-20260905`, source baseline
`aad0d450d8b8f1381badeeb4bcb939181115ab00`. This is a design-development
extension of the master audit, not a new whole-game acceptance claim.

Sol/Luna generate the bounded menu/component studies; Astra independently
records [artifact-bound pass/fail reviews](UI_PEARL_STAGE_CONCEPT_REVIEW_2026-09-05.md).
Root applies the same canonical visual, non-reader, touch, provenance and
evidence rules. Repeat the [UI review packet](../design/11_UI_PEARL_STAGE_LANGUAGE.md)
for every adopted menu, arrow and tutorial component. The historical
`MENU_UI_SYSTEM_AUDIT_2026-08-01.md` census is a discovery seed, not proof that
the new treatment is implemented or accepted.

| Claim | Evidence boundary |
|---|---|
| Design direction defined | Section 21 rules and the component/layout specification |
| Concept visual PASS/FAIL | Astra's exact-image review; native and phone-size artifact inspection only |
| Runtime rollout | Not implemented by this concept round; shared consumers and exact-build tests required |
| Device / child / owner acceptance | Not established by generated images or AI review |
| Master satisfaction | Remains **UNSATISFIED**; existing findings and sealed scores unchanged |

### Next bounded planning work

| Deliverable | Prerequisite | Next evidence |
|---|---|---|
| Northern Christmas world draft, art shortlist and restaurant brief | Owner requested a gameplan and detailed visual guide before game production; keep tracing remaining art from the confirmed July 29 forest | Review the linked draft's mood/premise/career mix; bind final buildings and states with source/usage/authority evidence before implementation |
| Representative playable activity, then expansion | Explicit chapter implementation commission and verified extension path | Intentional/passive/repeat/save/return tests, in-context captures, and applicable full gates |
| Playable review and reference-library promotion | Implemented candidate | Exact build and required device/child/owner review; preserve missing evidence as open |

Section 13 owns remediation, not the creative-production sequence. Select work
by child impact and dependencies, use section 9 for defects, and use the chapter
guide for new content (`DL-PLAN-01` through `DL-PLAN-06`). Run
`python -B tools/audit_document_authority.py` for the live inventory and selected
active-fact checks; do not hand-copy its counts into planning rules.

---

## Sealed audit snapshot and subsequent round metadata

- **Audit ID:** `MA-2026-08-09`
- **Audit date:** 2026-08-09
- **Current audit-control candidate branch:**
  `codex/sky-lagoon-canvas-repair-20260813`; integrated evidence head
  `441adf35f7dbdeb67d36fbf1a2217b87d3040d47`, a governance-only descendant of
  sealed product source commit
  `51d0abc0d32855a8ba32932599fedd8f59b398b7`, exact parent
  `1b7d6bdaf89ebc7c9bdeae16fbde0e14079fd8a8`; exactly 19 paths,
  3,318 insertions and 3,517 deletions
- **Historical CI-repair checkpoint:**
  `af4189a99cfd5a32d0df0f75185f6912d3889399`
- **Historical local merge-integration commit:**
  `f3b0de078898a8b4faddb2c738c4403180eff928` (parents
  `ea6185fdb1a687a20a6d118bdc368400e2c30f60` and
  `5f58ef0a9db7aa9593f85131e1b855e51b84aea8`)
- **Current Opera product/runtime commit:**
  `09e5e35665fd8d1bd782693e10fc0198f756d2c8`
- **Current probe-readiness checkpoint:**
  `ff068db002202839f920a6f9fb78c942788a3034`; this changes only
  `scripts/probe_opera.gd` and preserves the `09e5e356` runtime
- **Historical integrated product/dev audit baseline:**
  `18b6150c01e1587100dca97c85ebad03f369825a`; later audit/governance
  integration preserves the `09e5e356` product runtime and `ff068db` probe
  readiness behavior
- **Sealed document-authority source chain:** first source
  `5ed0c75460c9afd5ab574ff2c4a907c1075964f0`, with exact parent
  `18b6150c01e1587100dca97c85ebad03f369825a`, followed by hardening source
  `7eb945957776ab3458a9de71c8be9937e2354720`, whose exact parent is `5ed0c754`;
  their exact union is 22 paths and neither changes game runtime
- **Document-authority verification parent:** CHG-023 maintenance commit
  `e6edf559af219edd4e5ce38cab0c5094483be5c6`, exact parent `51887315`; dev Probe
  Suite run `31722047536` succeeds at that exact SHA with 63/63 unique remote
  headings in 34m25s, 36 document tests, six/six stress controls, 316/316
  inventory/ledger parity, 34 active/36 retained records, and music 42/42 in
  3m33s. Earlier branch run `31719143975` is corroborating history at the same
  SHA, not the latest integrated predecessor run. The source preserves the
  unchanged two-source CHG-029 chain
- **Current committed full local verification:** exact official Godot
  `4.7.1.stable.official.a13da4feb`; `scripts/ci.sh` over exact integrated-head
  bytes `441adf35` exits 0 after 1,391.5 seconds with all 64 unique trusted
  local headings completed. This governance-only head preserves the exact
  `51d0abc0` product source, whose own source-byte run exits 0 after 1,404.5
  seconds/all 64 with no trusted-probe, script, parse, or compile failure.
  Advisory diagnostics remain scoped below.
  Historical document checkpoint `51887315` exits 0 after
  1,435.2 seconds/all 64, and first source `5ed0c754` exits 0 after 1,359.8
  seconds/all 64
- **Last historical exact-head remote checkpoint:**
  `dacef1405b6a8cb470117e824aebac3a8ca500af`, GitHub run `31457593351`
- **Historical exact-head remote verification (predecessor runtime):**
  `e0677ae4c4f5e48258ff57c38f82e25f2dc3d9d0`, GitHub run `31661887863`;
  both required jobs succeed
- **Failed pre-fix distribution-head remote attempt:** GitHub run `31678156887` at
  pre-fix head `3fc151c8b3b6c054d0f6e6ab89f84a9f464f3f20` is red only because
  Ubuntu `probe_opera` sampled the 0.25-second reveal after a fixed four frames;
  its Detective/Nursery stable-Canvas compound failed before ambient layer 15
  could settle to 11. All other executed gates/probes and Windows passed
- **Latest completed exact-parent remote verification:** dev Probe Suite run
  `31722047536` succeeds at exact `e6edf559`; its probes job takes 34m25s,
  includes exactly 63 unique trusted headings and the green document controls
  above, while Windows music completes in 3m33s at 42/42. Earlier branch run
  `31719143975` also succeeds at exact e6 in 33m18s/4m24s. Their inherited Sky
  output is the historical predecessor diagnostic—21 `OK`, 44 `FAIL`, one
  `DONE`—not the result of the new harness
- **Historical Sky remote diagnostic:** Probe Suite run `31728755204` completed
  overall `SUCCESS` at predecessor source `7391c53c`, but its nonblocking Sky
  subprocess emitted 20 PASS rows and then
  `LAGOONSHOT|GLOBAL|FAIL|rendering_method|gl_compatibility`, `RESULT|FAIL`, and
  process exit 1 after the runner lacked `VK_KHR_surface`. This failed renderer
  proof remains explicit history; it is not current-source evidence
- **Current integrated-head remote state:** topic Probe Suite run `31760207048`
  and dev Probe Suite run `31762132976` both succeed at exact `441adf35`.
  Their probes jobs take 33m39s each; their music jobs take 3m18s and 3m56s.
  Both complete the 63/63 unique remote loop with zero hard failures, document
  controls at 36 tests/six stress/316 inventory/316 ledger/34 active/36
  records, and music 42/42. The Sky capture subprocess remains nonblocking and
  internally failed in each run: requested Mobile cannot create
  `VK_KHR_surface`, falls back through llvmpipe to `gl_compatibility`, emits 20
  PASS rows plus summary `20/20/20/20` with zero failed/skipped rows, then
  emits `GLOBAL`/`RESULT` FAIL and exits 1. PNGs upload; no remote JSON or
  Mobile-renderer PASS exists. Workflow success is therefore exact-head
  machine evidence, not remote visual acceptance
- **Current Sky Lagoon local evidence:** run-14 emits 20/20 ordered 1280×720
  Mobile/Speedy captures with zero failed, skipped, or global rows. Its manifest
  SHA-256 is
  `AEAC7C72E0A3BFF992713127261DD00ED69049947DFB6723AA66365F5712DE34` and
  current visual-probe SHA-256 is
  `B9EAF5E0738CFB61CCD3E34ACFEA420AEADAB4E3ADE80B40A2CFD1F227569C6C`.
  The manifest records `source_revision` as unknown; those exact hashes bind
  the manifest, embedded PNG identities, and visual-probe script, not the full
  source revision. Save output is isolated and restored. Two independent
  human reviews approve this local candidate; no remote, device, child, owner,
  or accepted-visual authority transfers
- **Current integrated-head Android dev build:** workflow-run Android
  `31763879294` succeeds with raw checkout and package source exact
  `441adf35f7dbdeb67d36fbf1a2217b87d3040d47`, version code 1414, and
  branch/tag `dev`/`android-dev`. It publishes a 596,033,220-byte APK with
  SHA-256 `f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`;
  the 82-byte checksum sidecar has SHA-256
  `43e892cfb6c9a3847e1a8760d5cad4dd8fb36719d63db0625ec8b2fa3ba8e651`.
  `441adf35` is governance-only over unchanged `51d0abc0` product bytes.
  Historical run `31724927769` belongs to e6, and run `31695675866` belongs to
  `18b6150c`. Device, child, owner, exact-voice, human-listening, strict-2D,
  and accepted-visual gates remain open
- **Canonical design authority:** `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`
- **Change and rollback ledger:**
  `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md`
  (`CHG-001`–`031`: 31 IDs, 79 uniquely owned commit references, four
  guarded-script emitters, 25 planner tests, and 27 manual/refusal groups)
- **Current audit round:** `MA-2026-08-26` code-refinement round at
  integration head `9a1754c1b1987dd2b9745fea8d8048f65f6d1ce2` (2026-08-25),
  169 commits past sealed evidence head `441adf35`; round record
  `MASTER_AUDIT_2026-08-26.md`, criteria deltas in sections 5, 12, 13, and
  14 and `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` section 18, Codex
  implementation handoff
  `CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md`
- **Document authority:** `CANONICAL_CURRENT`
- **Audit program status:** `IN_PROGRESS`
- **Overall cycle state:** `REPAIRING` with concurrent focused `VERIFYING`
- **Satisfaction:** **UNSATISFIED**

This document is the canonical current audit-cycle and triage ledger for the 2026-08-09
master-audit round. It consolidates earlier audits, records the owner's final
game-wide true-2D decision, separates current defects from historical reports
and rejected ideas, and preserves every repair transition. Section 5 is an
index, not a substitute for the complete canonical records defined in section
10.

It does not treat a shrinking-debt result as a pass. It does not substitute a
static repository review for Godot runtime evidence, Mobile-renderer captures,
target-device measurements, an observed child session, protected-voice work,
or owner visual acceptance.

---

## 1. Executive verdict

The project has strong automated gameplay coverage, a coherent illustrated
storybook identity, and many verified child-safety repairs. Mermaid Roshan's
3D model and model pipeline are retired from the active tree. The whole game,
however, is not yet a true-2D runtime.

At local merge-integration commit `f3b0de07`, the exact
game-wide scanner measures:

```text
GAME2D| model_files=509
GAME2D| model_scan_coverage_files=0
GAME2D| active_export_model_files=509
GAME2D| model_import_sidecars=157
GAME2D| active_untracked_model_import_sidecars=352
GAME2D| model_archive_files=0
GAME2D| production_3d_files=68
GAME2D| probe_3d_files=77
GAME2D| scene_3d_files=1
GAME2D| configuration_3d_files=1
GAME2D| archive_now_model_files=0
GAME2D| STATUS=UNSATISFIED
```

The Opera racer conversion at `82124b3a` reduced production 3D-file debt from
72 to 71, and the medal spatial-scoreboard retirement at `8ed978be` reduced it
from 71 to 70. Dolls became a bounded true-Canvas catcher at `5df75427`; the
animated Seek actor kit landed at `8fa90111`; and `27bda85d` rebuilt Seek as a
true-Canvas activity while removing four archived meadow GLBs. The guarded
manifest shrink at `a3d3bce1` now records the resulting 509-model/68-production
inventory. Default and regression modes exit zero; strict exits nonzero because
known debt is not a waiver. A smaller exact inventory is progress, not a
satisfied 2D game.

The Opera retirement/lifecycle repair shrank source-category debt, and current
Sky source `51d0abc0` removes the obsolete spatial promenade/probe references:
models remain 509/509 active and sidecars remain 157 tracked plus 352 generated,
while production 3D files are now 65 and probe 3D files are 70; the scene and
configuration counts remain one each. Exact regression is
`NO_REGRESSION`, all 14 falsification controls pass, and strict remains
`UNSATISFIED`.

The current visual audit reports:

```text
VISUALAUDIT| ERROR=16  WARN=17  MANUAL=2  INFO=126  SKIP=86
VISUALAUDIT| STATE FAIL=16  REVIEW_OPEN=17  MANUAL_OPEN=2
VISUALAUDIT|       COVERAGE_GAP=86  WAIVED=0  PASS=32
VISUALAUDIT|       NOT_APPLICABLE=94  RESULT=UNSATISFIED
```

This is a clean-HEAD `--fresh-runtime --strict` run using exact Godot
4.7.1-stable. The strengthened contract at `3b7a7e66` and `fea916a8` correctly
rejects legacy 3D staging and refuses to inherit PASS authority from saved or
manual facts. Twelve active zone surfaces emit legacy-3D failures; Sky Lagoon
also fails its Canvas layer, engine-layer, draw-order, and occlusion contracts.
The source-average palette checks remain review risks, not hard art failures.
The fresh probe returned no rendered Canvas capture outputs, so every affected
runtime check stayed `COVERAGE_GAP` and strict failed closed. Approved art must
not be recolored or regenerated merely to make a source-average heuristic
green.

The former dimensional-rollback error, four playground-license errors, four
clipped/debris playground frames, the Dolls spatial catcher, and Seek's vinyl
pair/low-quality meadow presentation are no longer current failures. They stay
in history and anti-regression coverage rather than returning to active triage.

The same integration review incorporates the newer Opera/music runtime,
including the diegetic rooms and borderless minigame presentation, instead of
preserving the audit's earlier Ballerina premise. The shipping Opera table now
contains **13 careers, 53 phases, and 27 distinct modes**, with no generic
`bop` phase. All 13 Roshan career atlases account for **208 reviewed runtime
frames**. The current Ballerina is the dedicated
three-act Pearl Mirror → Ribbon Trail → Grand Twirl recital documented by
`BALLERINA_PARTY_REBUILD_2026-08-09.md`; it uses the accepted
`roshan_ballerina_sheet_a.png` hash
`c829784d4085e9cd9765cf0114a0f65bfe3f662ed8acc423223b726a0f003995`
as held pose keys and a one-shot curtain call, not the old looping Ballerina
art or generic phase set. Boxer now owns a five-phase, full-stage two-glove
specialist surface. Candymaker's syrup pour now has one complete, phone-legible
mold, a generous pitcher target, and one shared painted-spout/stream/hit
geometry.

The Racer path is a true-Canvas three-phase activity. Its
`RACE` phase uses the same Canvas surface, a `circle` gesture, no widget, goal
`0.9`, and exact `op_racer_lap_two` speech. The current repair removes the
ordinary-headless legacy lobby/kart path and drives ordinary unforced entry
through the same Canvas controllers. Its exact focused and full local Godot
4.7.1 lifecycle, passive, teardown, and re-entry evidence is green, moving
`MA-OPERA-010` to `FIXED_PENDING_VERIFICATION`. Exact-head run `31661887863`
is green; external acceptance remains.
The music program
adds **42 deterministic area cues**
on top of the 15 legacy files (14 score files plus the `banjo.ogg` SFX); its
machine composition, hash, codec, loop, loudness, and routing evidence is
green, while human two-wrap/style listening, voice intelligibility, mono
fold-down, and Lenovo Tab M11 review remain open.

Those career counts now ship behind the owner-directed Castle-room
distribution. Commit `09e5e356` gives every one of the thirteen live careers
one exact room-owned picture route: Royal Kitchen owns Chef/Candymaker; Opera
Hall owns Ballerina/Pop Star/Magician; Royal Library owns Detective; Craft Room
owns Painter; Stuffie Playroom owns Doctor/Boxer; Bubble Bath owns Nursery;
Mermaid Pool owns Astronaut; Family Dining Room owns Farmer; and Movie Lounge
is the resolved sole home for Racer. The rejected three-floor all-career lobby
and its source file are deleted, no hidden direct route reconstitutes it, and
each activity returns to the exact room that launched it. This moves
`MA-OPERA-012` to `FIXED_PENDING_VERIFICATION`, not `VERIFIED_FIXED`: current
integrated evidence head `441adf35` preserves the Opera runtime, passes exact
local/topic/dev machine gates, and has a matching dev APK. Historical source
`7391c53c` completes overall remote
run `31728755204`, but that run's Sky subprocess fails required-Mobile renderer
identity. Current topic/dev runs likewise retain a failed Sky renderer proof,
with PNG-only output and no remote JSON/Mobile PASS. Device, child, owner,
exact-voice, human-listening, strict-2D, and accepted visual evidence remain
open. The 9 room-route captures also expose
a residual
P2 composition issue: the 154×154 lower-center career cards clear controls but
obscure Roshan's lower body/tail. Section 16 / commit
`3d1236fe` also cuts the Curtain Dragon, Shadow Phantom, and Midnight Maestro;
section 17 / commit `ef2fd982` retains any future boss-fight role for
Ember-aligned henchmen, not those Opera characters. The current repair removes
the three Opera boss cards, gates, completion requirements, and runtime. Save
slots 4/9/14 are permanent raw-preserving tombstones, the live completion mask
is `0xBDEF`, and effective progress counts only the thirteen careers. Focused
migration/reward/passive/suspend/leave evidence is green, so `MA-OPERA-011` is
`FIXED_PENDING_VERIFICATION`, not closed.

The product/runtime commit `09e5e356` Opera/Castle distribution slice passes
its exact focused matrix and a full local `scripts/ci.sh` run under official
Godot `4.7.1.stable.official.a13da4feb`: exit 0 after 1463.4 seconds, all 64
trusted local probes, 74 GAME2D unit tests, all 14 falsification controls, 93
visual-contract unit tests, and exact `NO_REGRESSION` are green. Probe-only
follow-up `ff068db` preserves that runtime and completes a newer exact full-local
run in 1379.3 seconds with all 64 trusted probes green. Castle
interaction approval candidate
`1754c880e4ef3df87daed47e1a8ec1ed36e114956ae86dbc50a74e40bba392d9`
covers 13 assets and 104 frames in the machine/review ledger. It is not owner
acceptance. Twenty-two 1280×720 Mobile captures—nine Castle room routes and
thirteen career surfaces—were rendered and visually inspected as
diagnostic/review evidence only; they are not target-device, child, owner, or
authoritative visual acceptance. Historical exact-head remote run
`31661887863`, belongs to predecessor integrated SHA
`e0677ae4c4f5e48258ff57c38f82e25f2dc3d9d0`: Ubuntu succeeds in 33m8s through
checkout/checksum, exact Godot, static/import/full analyzer, all 63 trusted
probes, boot, Dust/Opera advisories, Opera manifest, and five diagnostic
capture/upload pairs; remote GAME2D is 509/66/74 exact
`NO_REGRESSION`/`UNSATISFIED`. Windows succeeds in 6m52s and ends
`MUSIC|check 42/42|picture_xmas`. The five pairs grant no authoritative visual,
device, child, or owner acceptance. Later run `31678156887` at pre-fix audit
head `3fc151c8` is genuinely red, but only because Ubuntu `probe_opera` sampled
the 0.25-second reveal after a fixed four frames: the Detective and Nursery
stable-Canvas compound checks ran before the Castle ambient layer 15 settled to
Opera layer 11. Every other executed gate/probe and the Windows job passed, so
the run is not evidence of a production routing, lifecycle, save, reward, or
return defect. Commit `ff068db` changes only `scripts/probe_opera.gd`, replaces
the frame guess with a bounded, fail-closed semantic wait for the exact routed
stage/layer/reveal state, and passes full local CI. Exact successor authority
head `9befc0f8` passes run `31686380560`: Ubuntu completes static/import/full
analyzer, exactly 63 trusted headings, boot, both advisories, the Opera
manifest in 33m40s; Windows completes in 3m47s and ends
`MUSIC|check 42/42|picture_xmas`. All five capture/upload pairs completed at the
workflow level and uploaded diagnostic artifacts; they are not capture gates or visual
passes. Raw Sky Lagoon `LAGOONSHOT` output has 21 `OK`, 44 `FAIL`, and `DONE`
(66 diagnostic lines), so that diagnostic internally fails. Workflow success
is not a warning-clean result: existing Vulkan-surface fallback and ObjectDB/
resource/texture-leak diagnostics remain in the logs. Matching APK and every
external acceptance gate were open at that checkpoint. Predecessor integrated
dev/audit head `18b6150c` passes successor Probe Suite run `31693492735` with
exactly 63 remote trusted headings in the 29m41s probes job and music 42/42.
Its capture outputs remain diagnostic/nonaccepted: raw Sky Lagoon is 21 `OK` /
44 `FAIL` / `DONE`, with 20 PNGs in the artifact. Android dev run
`31695675866` succeeds at the same exact head and publishes a 596,041,412-byte
APK with SHA-256
`fb4979473441d416f7b07914b1396f5f883935d4c08bf077baed3dfb91b78941`.

Later integrated predecessor `e6edf559` passes dev Probe Suite run
`31722047536`: probes complete 63/63 in 34m25s, document controls report
36 tests/six stress/316 parity/34 active/36 retained, and music completes
42/42 in 3m33s. Workflow-run Android `31724927769` uses raw checkout/package
source exact e6 and publishes a 596,041,412-byte APK with SHA-256
`66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c`.
Earlier branch run `31719143975` is corroborating e6 history.
Device, child, owner, exact-voice, human-listening, accepted-visual, and strict-
zero 2D evidence remain open. The
global visual audit remains unchanged and
`UNSATISFIED` at 16 FAIL, 17 REVIEW_OPEN, two
MANUAL_OPEN, 86 COVERAGE_GAP, 32 PASS, and 94 NOT_APPLICABLE.

Sealed Sky source `51d0abc0`, exact parent `1b7d6bda`, changes exactly 19 paths
with 3,318 insertions and 3,517 deletions. It replaces the spatial promenade
with one owned true-Canvas stage: a `CanvasLayer` at layer -1, literal
6144×2048 master-pixel `Node2D` space, six-by-two 1024×1024 `Sprite2D` backdrop,
base/rear/landmark/interactive/actor/foreground layers, and a sole `Camera2D`.
Rear and foreground cards use real differential parallax; rendering, movement,
touch, navigation, and external-route return all share the same master
coordinate. The generic Player and `Camera3D` are hidden/inactive while this
phase owns the screen. Approved existing art is reused unchanged; no art,
asset, protected original, audio, workflow, or save-schema file changes.

The same slice increases frog/otter readability, separates and grounds all five
animal presentations, strengthens non-reading focus cues, repairs immutable-rest
seesaw contact, and makes Canvas navigation/touch ownership cancel on manual
movement, pause, focus, overlays, and transitions. It proves real Reef, Castle,
Northern, Galaxy, Ember, and kart exits/returns plus re-entry and save state,
but does not claim a whole-world fresh-save child traversal.

The exact source bytes pass official-Godot full local CI in 1,404.5 seconds/all
64. Run-14 supplies 20/20 ordered local 1280×720 Mobile/Speedy frames, manifest
SHA-256 `AEAC7C72E0A3BFF992713127261DD00ED69049947DFB6723AA66365F5712DE34`,
and current visual-probe SHA-256
`B9EAF5E0738CFB61CCD3E34ACFEA420AEADAB4E3ADE80B40A2CFD1F227569C6C`.
Those hashes bind the manifest, its embedded PNG hashes, and the visual-probe
script—not the full source revision, which remains `unknown`. Two independent
human reviews approve the local candidate, moving `MA-VIS-002` from
`CONFIRMED_OPEN` to `FIXED_PENDING_VERIFICATION`; `MA-VIS-006` remains
`CONFIRMED_OPEN` because game-wide visual gaps and external acceptance remain.
Historical `7391c53c` run `31728755204` retains the failed remote
`gl_compatibility` evidence. Integrated head `441adf35` adds exact local/topic/
dev machine and matching-APK evidence over unchanged source `51d0abc0`, but
its Sky subprocess still lacks remote JSON/Mobile PASS. No target-phone, M11,
child, owner, or accepted-visual result is claimed.

The exact 19-path source boundary is:

```text
scripts/arena/sky_lagoon_promenade.gd
scripts/living_world.gd
scripts/main.gd
scripts/pause_menu.gd
scripts/probe_audit.gd
scripts/probe_boot_display.gd
scripts/probe_galaxy_state.gd
scripts/probe_interaction.gd
scripts/probe_l2.gd
scripts/probe_l2_living_cards.gd
scripts/probe_l2_reenter.gd
scripts/probe_northern.gd
scripts/probe_ocean_kingdoms.gd
scripts/probe_sky_lagoon_animals.gd
scripts/probe_sky_lagoon_art.gd
scripts/probe_touch_stress.gd
scripts/probe_train.gd
scripts/touch_ui.gd
tools/game_2d_migration_manifest.json
```

The sealed Castle Kitchen controller was deliberately excluded. Its current
Chef configuration is valid and probed, so no child-facing failure is
reproduced. A speculative recovery branch for a future invalid
`OperaAct.start()` result would require renewed owner visual approval and stays
separate `MA-CODE-002` debt.

The Castle personalization update is also integrated: the saved logo now
replaces both painted purple shell banners in the Craft Room and both in the
Stuffie Playroom, retains the Craft board badge, remains input-transparent, and
does not appear in rooms with no registered banner. This is a bounded Canvas
overlay repair, not evidence that the still-spatial Castle rooms satisfy the
game-wide 2D contract.

The reconciled content committed as `f3b0de07` completes exact Godot
4.7.1-stable local `scripts/ci.sh` with exit 0 after 1437.1 seconds and all 64
trusted probes green. All static, Opera art/provenance, animation, music, and
probe-parity gates in that run are green. This closes local merge integration
only. Historical workflow/parity commit `dacef140` completed remote run
`31457593351`. The next exact-head run, `31648427712` at docs-sync child
`bbc817ef`, again proved the pinned Windows area-music delivery 42/42, but its
Ubuntu job stopped before import, analyzer, or probes because Opera
`PROVENANCE.json` contained the raw CRLF checkout hash of the declared text
input `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/GENERATION.json`
while Linux read LF bytes. Repair checkpoint `af4189a9` addresses only that
boundary: the declared text source is LF-canonical for hashing, every binary
source stays byte-exact, and the provenance record is refreshed. Ten focused
checker tests, the Windows Opera-art check at 42/42, and an LF-clean archive
check at 42/42 are green. Replacement run `31649113587` then succeeds at exact
`af4189a9`: the 35m27s Ubuntu job passes static checks, import, the full
analyzer, all 63 current remote trusted probes, boot, Dust/Opera advisory
balance, the Opera manifest, and five diagnostic capture/upload pairs; the
3m55s Windows job passes music 42/42. The captures are diagnostic, not accepted
visual evidence. No full local suite at `af4189a9`, and no APK, device, child,
owner, human-listening, strict-2D, or authoritative visual-evidence result, is
claimed.

No P0 audit item is currently indexed from the repository evidence reviewed for
this round. Missing runtime, device, child, manual-art, and off-repository
evidence prevents the stronger claim that no P0 exists.

### 1.1 How to read the 1–5 ratings

These are audit ratings, not a claim about what the child likes. A high score
means the implementation, evidence, and child-facing design are all strong;
it does not erase a separately listed defect. No area receives 5/5 in this
round because the exact release candidate still lacks the complete phone,
Lenovo Tab M11, observed-child, listening, and owner-acceptance record.

| Rating | Meaning in this audit |
|---|---|
| **5 — release-proven** | Exact release build is automated, no-fail and non-reader-safe, true Canvas where required, accepted on target devices, observed with the intended child, and approved by the owner |
| **4 — strong** | Purposeful, child-readable, and well covered by focused/runtime evidence; one or more device, child, owner, listening, or final-capture gates remain |
| **3 — workable** | Functional and valuable, but has a material clarity, art, medium, reachability, performance, or evidence gap |
| **2 — major repair** | Playable or promising, but its current 3D architecture, controls, readability, art, or route substantially conflicts with the final product contract |
| **1 — absent or unsuitable** | Missing, unreachable, broken, purely conceptual, or not usable as a current child-facing game |

### 1.2 What this audit program actually changed

This is the short human-readable answer to “what changed?” The detailed
positive/negative record and individual rollback path for every row lives in
the companion [change and rollback ledger](MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md).

| Change | Positive effect | Risk, limit, or unfinished work | Rollback owner |
|---|---|---|---|
| Roshan 2D authority and frame repairs | Removed the active Roshan model fallback, repaired named clipped frames, and made accepted 2D identity the rule | Identity/style still need owner acceptance at the eventual release SHA; do not restore retired models as a shortcut | `CHG-001`, `CHG-009`, `CHG-011` |
| Companion no-fail repair | Removed a child-facing timeout/failure path and added passive patient-care coverage | The surrounding companion/living-world presentation is still spatial and lacks final child/device evidence | `CHG-002` |
| Medal and other feedback overlays | Replaced bounded spatial feedback with Canvas overlays without changing save meaning | These repairs do not convert the worlds that launch them | `CHG-007` |
| Game-wide 2D scanner and archive | Made every model/sidecar/3D API measurable, fail-closed, and shrink-only; archived verified retired bytes | The current result is still 509 models and 65 production-3D files, so green regression mode means “did not get worse,” never “finished” | `CHG-008`, `CHG-009`, `CHG-026`, `CHG-031` |
| Dolls catcher | Rebuilt Faron's catcher as a bounded Canvas activity with real routed drag, safe misses, passive rejection, save, replay, and teardown | Exact objective voice, M11, observed child, and owner capture acceptance remain | `CHG-012` |
| Seek / Evie and Lamb-a' | This was **not** a wholesale import of the old 3D game. The useful hide-and-seek loop was rebuilt as a fourteen-node Canvas meadow; vinyl/static actors and low-grade `k_bush2` presentation were replaced by frame-swapped Evie/Lamb-a' art and approved meadow/tree art; four meadow GLBs were retired | The exact Evie “tap the wiggly tree” recording is missing; generated identity/motion and device/child acceptance remain open | `CHG-013`; voice debt `MA-ACCESS-003` |
| Opera Racer | Ordinary unforced and display entry now use the same three-phase Canvas circle activity and exact lap-two cue; no Opera controller attaches the external kart | Focused, full-local, and exact-head remote evidence is green, but device/child/owner verification remains under `MA-OPERA-010` | `CHG-010`, `CHG-024`, `CHG-026` |
| Opera specialists, art, and Castle distribution | Integrated the current 13-career/53-phase/27-mode table, 208 reviewed Roshan cells, dedicated Ballerina and Boxer surfaces, phone-safe Candymaker, diegetic rooms, deterministic music, stable retirement of the three owner-cut boss slots, and one exact thematic Castle-room route per live career. Racer's sole home is Movie Lounge; the all-career lobby is deleted; each activity returns to its launching room | `MA-OPERA-011` and `MA-OPERA-012` await external verification. Current route cards obscure Roshan's lower body/tail (residual P2), exact voice gaps remain, and the 22 captures are diagnostic rather than accepted | `CHG-016`–`CHG-020`, `CHG-024`, `CHG-026`, `CHG-027` |
| Castle logo presentation | Replaced the matching painted shell banners with the child's saved Canvas logo without stealing input | Castle rooms themselves remain spatial; personalization is not a Castle-wide 2D pass | `CHG-021`, `CHG-024` |
| Visual evidence contract | Replaced easy-to-forge palette/capture claims with fresh runtime, source-bound, fail-closed evidence rules | Current live Canvas adapters are incomplete, so 16 failures and 86 coverage gaps remain rather than becoming false passes | `CHG-006`, `CHG-014` |
| Sky Lagoon true-Canvas promenade | Replaced the spatial/mural stage with an owned six-layer Canvas stack, master-coordinate Camera2D movement/touch, five readable animals, three repaired playground actions, and exact route/return/re-entry coverage while reusing approved art unchanged | Exact local/topic/dev machine gates and a matching APK exist through `441adf35`, but the remote Sky subprocess lacks requested-Mobile PASS/JSON; target-device, child, owner, and accepted-visual evidence remain open | `CHG-031` |
| CI, master documents, and rollback control | Reconciled newer development work with the audit, ran exact 4.7.1 local/remote gates, and created stable `CHG-*` records with guarded rollback planning | This controls change; it does not itself prove APK, device, child, owner, listening, visual, or strict-2D acceptance | `CHG-005`, `CHG-011`, `CHG-015`, `CHG-022`–`CHG-026` |

### 1.3 Whole-game systems scorecard

| System | Rating | What works | What keeps it from the next rating / best next improvement |
|---|---:|---|---|
| Child safety and no-fail behavior | **4/5** | Passive negative gates, mercy, no-loss specialists, safe Dolls misses, and companion timeout removal are strong | Observe the intended child across every route; prove every wrong/idle path remains kind and non-paying |
| Save, rewards, and replay | **4/5** | Append-compatible save, backup/recovery, upgrade-only medals, replay/idempotence, and many exact probes | Run the final APK upgrade/recovery matrix and a long-session write-frequency/teardown soak |
| Touch and non-reader access | **3/5** | One-finger specialist games, large targets, picture cues, routed-touch probes, and voice/pointer rules exist | Close exact voice gaps and run phone/M11 hold, drag, focus, competing-Control, and thumb-occlusion tests |
| Navigation and discoverability | **3/5** | Storybook UI, explicit interaction targets, and many route/re-entry probes are valuable | Prove every visible destination from a fresh save without debug shortcuts, reading, or proximity guesswork |
| Visual art and cohesion | **2/5** | Strong storybook sources, improved Opera/Castle art, and bounded Canvas games show the target quality | Resolve 16 hard visual failures, 86 evidence gaps, mixed 3D/Canvas staging, and large orphan inventories before broad regeneration |
| Voice, music, and sound | **3/5** | Family voices are protected; 42 new deterministic cues pass hash/codec/loop/routing gates | Perform human two-wrap/style/ducking/mono checks, record authorized missing objective lines, and test M11 speakers |
| Performance and device fitness | **2/5** | Mobile renderer is binding and several node/texture budgets are probed | Measure release-candidate P50/P95/P99 frame time, hitches, memory, thermal behavior, load time, and touch latency on target devices |
| QA and release automation | **4/5** | Exact 4.7.1 analyzer, 64 local/63 remote probe roster, import/boot gates, deterministic art/music, regression and falsification controls are unusually strong; integrated `441adf35` is exact local/topic/dev-machine green with a matching APK, while run-14 has manifest/PNG/probe hashes | Obtain a requested-Mobile remote Sky PASS/JSON, classify all 106 probes, complete live visual adapters, and exercise the matching APK on target devices |
| Architecture and maintainability | **2/5** | Satellites, bounded surfaces, the collapsed Canvas-only Opera controllers, the Sky Canvas satellite, and the centralized Castle career-route registry demonstrate safer ownership | `main.gd` and string-owned state remain large; 65 production-3D files and broad game-wide spatial debt keep change risk high |
| Provenance, protected assets, and rollback | **4/5** | Protected sources stayed untouched; licences, archive proof, 31 stable change groups, and guarded inverse plans exist | Append every later material branch/merge to the ledger and run its rollback gates before integration |

### 1.4 World and area scorecard

| Area | Rating | Strengths | Main problem and recommendation |
|---|---:|---|---|
| Storybook UI and menus | **3/5** | Picture-first direction, touch targets, and route probes are solid | Prove the complete fresh-save graph, focus/back behavior, and root-viewport Canvas evidence on phone |
| Sky Lagoon | **3/5** | Source `51d0abc0` now owns a true six-layer Canvas promenade, readable focus cues, five route-safe animals, repaired playground contact, strong gameplay probes, and a deterministic 20-state local Mobile review; integrated `441adf35` adds exact machine/build evidence | Requested-Mobile remote Sky PASS/JSON, target-device, child, owner, and accepted-visual evidence remain open; preserve the implemented Canvas lifecycle and repair only concrete failures from those gates |
| Reef / home ocean | **2/5** | Broad exploration, characters, districts, and many regression probes | Free-swim spatial staging and mixed affordances are hard for a non-reader; convert one bounded route family and prove every return path |
| Pearl Castle rooms | **3/5** | Dense interactions, strong room identity, saved logo personalization, and good probe coverage | Room shells remain spatial and capture coverage is incomplete; convert shell/order without losing the interaction catalogue |
| Courtyard and train | **2/5** | Recognizable transit and destination links | Purpose and direct-touch routes remain bound to spatial traversal; define the child-facing route first, then Canvas-convert it |
| Northern world | **2/5** | Substantial kingdom art and gameplay content | Legacy free-swim/3D staging and incomplete current visual inventory; re-inventory live routes before another art pass |
| Ember Fortress | **2/5** | Playable fire-themed progression and probes | Heavy spatial architecture and unclear long-term product role; decide keep/retire, then convert only the accepted loop |
| Fairy Pond | **3/5** | Complete declared 2D art family and a gentle no-fail fantasy loop | Runtime remains a spatial scroller and figure-ground review is open; port the existing verb to Canvas before recoloring approved art |
| Galaxy | **2/5** | Bespoke concept and meaningful scripted content | Legacy rail/planet staging plus 32/32 orphan PNGs; owner must choose conversion or retirement before more asset work |
| Living world and companions | **3/5** | Care, follow, collection, and no-fail repairs create a warm persistent world | Ambient shell is spatial and exact care speech/device evidence is incomplete; move ownership and cues into bounded Canvas surfaces |
| Current distributed Opera careers | **3/5** | Best content breadth: 13 reusable careers, current specialist games, exact thematic Castle-room ownership, Movie Lounge Racer, exact-room return, career art, voices, music, no all-career lobby, and no reachable cut-boss ladder | Full local and exact-head remote machine evidence are green, but matching APK/device/child/owner/exact-voice/accepted-visual gates remain; move or restage the lower-center cards so Roshan's lower body/tail remains visible |
| Picture-game wing | **4/5** | Multiple bounded Canvas games with simple input, shared teardown, rewards, and passive checks | Capture every state at phone ratios and verify timing/voice with the intended child |

### 1.5 Non-Opera activity scorecard

| Activity | Rating | What works | Main limitation / next improvement |
|---|---:|---|---|
| Fetch | **2/5** | Friendly timed throw/retrieve loop with no need for punishment | Spatial swimming/aim and no accepted animated Chuck Canvas actor; rebuild as a generous one-finger Canvas timing surface |
| Dolls | **4/5** | Verified Canvas drag, safe misses, passive no-award, save/medal/replay, teardown, and Mobile captures | Add exact objective speech and complete M11/child/owner acceptance |
| Seek (Evie/Lamb-a') | **4/5** | Animated Canvas actors, approved meadow/tree art, four large targets, kind wrong taps, save/replay, multi-aspect review | Record the exact Evie tap-tree cue and run target-device/child identity review |
| Secret Treasure | **2/5** | Sequential discovery/reward idea and reusable accepted detective art | Current route is dormant/spatial; choose a canonical sunken-wreck / Secret Cave entry and build/prove the bounded Canvas activity before claiming reachability |
| Melody | **2/5** | Clear seven-note collection premise | Legacy 3D theater and reading/route uncertainty; rebuild as a direct Canvas sound-and-orb sequence with spoken pointing |
| Pearl Shop | **2/5** | Purchases/save meaning work and Beans has an exact cue | 3D navigation, text prices, proximity-plus-tap grammar, missing picture-card kit and missing exact shop speech; needs a purpose-built Canvas shop package |
| Play-place checkpoint course | **2/5** | Existing checkpoints and playful vertical course | Spatial/analog precision conflicts with the age target; reduce to readable lanes or a bounded Canvas course |
| Penguin and rainbow slides | **2/5** | Understandable downhill/rail fantasy | Legacy 3D steering and reward discovery depend on spatial inference; use one-axis touch assist and a visible picture objective |
| Kart race outside Opera | **2/5** | Deep drift/turbo implementation for an older player | Too control-dense and fully spatial for this target; simplify to a Canvas rail or owner-retire it rather than reuse it for Opera |
| Combat arena and tutorial | **3/5** | No-fail one-button action, tutorial, and strong functional probes | Convert the room and waves to Canvas, then prove scale/discoverability on phone without increasing aggression |
| Dungeon | **2/5** | Ten rooms and substantial combat/puzzle variety | Large spatial route/precision burden and no child-path proof; preserve objectives while converting one room family at a time |
| Fairy game | **3/5** | Gentle fantasy, assist/mercy potential, and complete declared art | Spatial scroller and incomplete state capture; Canvas-port before expanding mechanics |
| Dust Bunny / boss | **3/5** | Friendly cleaning fiction, authored animation, boss probes, and no-loss framing | Mixed staging, rapid visual load, and device/performance evidence remain; keep difficulty expressive rather than punitive |
| Garden picture game | **4/5** | Direct Canvas growing, feedback, and reward | Add state-complete phone capture and child comprehension evidence |
| Snowman picture game | **4/5** | Large coal targets and a readable build/face/chase sequence | Check fastest chase, thumb occlusion, and exact voice timing on phone |
| Trampoline picture game | **4/5** | Simple one-button bounce with clear cause and effect | Verify latency, repetition fatigue, and audio timing on device |
| Slide picture-game launcher | **3/5** | Clear Canvas start interaction | Its destination inherits Lagoon/slide spatial debt; finish the destination rather than polishing only the launcher |
| Christmas-tree picture game | **4/5** | Direct placement, strong seasonal identity, and clear reward | Prove non-reading order cues and all target sizes on the smallest phone |
| Dance | **4/5** | True-Canvas simple lane rhythm and friendly feedback | Measure audio/touch latency and observe whether a four-year-old understands the beat without text |
| Critter collection | **3/5** | Friendly approach/catch/save loop | Depends on mixed living-world staging; move critter hit ownership and cues into Canvas and prove no accidental capture |
| Stuffie battle | **3/5** | No-fail attack/dodge identity and strong emotional attachment | Legacy arena/model use, including Lamb-a' debt, and device readability; Canvas-convert without changing protected friend art |
| Toy-castle brawler | **2/5** | Cooperative, no-fail intent | Legacy side-scroll spatial engine and passive/readability debt; preserve the verbs in a true Canvas room |
| Companion/care wing | **3/5** | Persistent follow/care/token systems and removed timeout failure | Spatial presentation and some exact speech/device/child gaps; make every care need independently visible and spoken |

### 1.6 Current Opera career scorecard

The scores below evaluate the **current integrated 13-career table**, not every
historical branch. The following section compares historical/candidate versions.

| Career | Rating | Best qualities | Main limitation / next improvement |
|---|---:|---|---|
| Chef | **4/5** | Purposeful pitcher/stream/oven/cake/topping actions and governed art | Complete two-aspect/device/owner art review and exact child comprehension pass |
| Detective | **2/5** | Varied lens, clue, choice, and reveal interactions | Painted-in crown/source ownership and incomplete state evidence make the mystery less causal; repair the scene and capture every clue state |
| Ballerina | **4/5** | Dedicated Pearl Mirror, Ribbon Trail, and Grand Twirl acts; held pose keys, one-shot curtain call, assistance, passive rejection | Accepted A-atlas is best integrated, but phone/M11/child/owner acceptance remains; newer B-sheet is only a separate candidate |
| Candymaker | **4/5** | Complete mold, measured spout, generous pitcher target, monotonic fill, authored ladle/fill states | Run final device/owner review and keep the newer authored syrup art synchronized with probes |
| Stuffie Doctor | **3/5** | X-ray and care verbs fit the preschool helper fantasy | Grouped fallback/voice claims and setting decision remain open; audit each action and speak each noun exactly |
| Farmer | **3/5** | Care/herd actions and recognizable job identity | Above-water setting/voice/art evidence is incomplete; capture and resolve the setting rather than add more generic phases |
| Boxer | **4/5** | Five full-stage phases, two owned gloves, sequential one-finger path, no health/loss, robust teardown | Device/child/owner proof remains; do not reintroduce its three GLBs or treat docs-only V2 as implemented |
| Magician | **3/5** | Vanish, tracking, rope, cabinet, and portal variety | Lamba/bunny-fish semantic voice debt and incomplete all-state capture; correct speech/causality before adding tricks |
| Painter | **3/5** | Current sunrise paint/stamp/gallery route works and uses the shared Canvas framework | Less purposeful than the uncommitted party-banner candidate; review/rebase that candidate rather than merging its dirty worktree wholesale |
| Astronaut | **3/5** | Pipes, patch, valve, and launch provide good job variety | No state-complete accepted capture/device evidence; review each tool's hit/feedback separately |
| Racer | **4/5** | Ordinary unforced/display entry now share the simple three-phase Canvas circle game with the exact lap cue | Preserve the green full-local and exact-head gates; finish child, device, and owner visual acceptance |
| Pop Star | **3/5** | Strong music/lane/crowd identity and career-specific art | Audio latency, all-state capture, and device/owner review remain open |
| Nursery Nurse | **4/5** | Cooperative Faron framing, bottle/pat/blanket/catch flow, no opponent, speaker-aware prompts | Finish exact voice/state captures plus device/child review |
| Retired Opera boss material (Curtain Dragon, Shadow Phantom, Midnight Maestro) | **1/5** | Existing art may remain as unused historical/reuse material; focused, full-local, and exact-head remote evidence no longer expose the acts | All three are cut by direct owner ruling. Keep save slots 4/9/14 as permanent tombstones, finish external verification, and do not convert or rehabilitate them as Opera bosses |

### 1.7 Opera House version and branch comparison

“Best” means best supported by current evidence, not the newest timestamp. A
branch row may contain useful art without being safe to merge as a whole.
This inventory groups branch aliases that resolve to the same commit as one
version. It rates materially distinct committed runtimes and documentation-only
candidates separately; rescue refs are preservation evidence, not additional
product versions.

| Version / repository location | Status and rating | Pros | Cons / regression risk | Verdict |
|---|---|---|---|---|
| Stable `origin/master` `e924d9ba` | Released but superseded quality, **2/5** | Known stable lineage and broad Opera content | 86 career phases, 29 generic `bop` phases, no dedicated Ballet/Boxing surface, external 3D kart, central floor hub, and three now-cut bosses | Keep only as release history; do not use it as the design baseline |
| Earlier flat/2.5D/hybrid Opera prototype branches and ledgers | Reference/review versions, **2–3/5** | Large visual idea inventory and useful provenance | Many are review-only, generic, spatial, duplicated, or semantically obsolete; not independently shippable games | Mine accepted source ideas only; never merge a prototype family wholesale |
| `32e1a7e8` quality overhaul / `ecad384e` minigame-quality generation | Superseded integration steps, **2/5** | Established 13 career art families, specialist props, and 208-frame evidence | Dated counts/mechanics plus the rejected central floor hub and cut-boss ladder | Supporting provenance, not current mechanics or navigation authority |
| Historical pre-audit integration parent `ea6185fd` (formerly `origin/dev`) | Best pre-audit content integration at that checkpoint, **2/5** | 53 phases, no generic `bop`, current Candymaker, diegetic/borderless Opera, Ballerina/Boxer specialists | Retains the rejected all-career hub, reachable cut bosses, and additional 3D debt; lacks the master audit controls; it is not the current development parent | Reuse bounded career content only through the audited reconciliation |
| Reconciled runtime/audit merge `f3b0de07` plus CI repair `af4189a9` | **Best overall audited repair base, 2/5** | Combines current career content with shrink-only audit controls, Canvas display Racer, 64/63 probes, exact local/remote evidence, and granular rollback | Whole game remains UNSATISFIED; the all-career floor picker and cut bosses are not the accepted product, while ordinary-headless kart, 509 models, and external gates remain | Safest repair base, not an accepted Opera structure and not release-ready |
| Opera retirement/lifecycle commit `e2c25878`, verified at integrated head `e0677ae4` | Committed and exact-head verified predecessor repair, **3/5 runtime / 2/5 hub** | One Canvas lifecycle, no external Opera kart/boss engine, 13 live careers, raw-preserving tombstones 4/9/14, `0xBDEF` completion, focused/full-local/exact-head gates green, 17 inspected diagnostic Mobile renders, and append-only `CHG-026` rollback coverage | The three-page all-career hub remains rejected; device, child, owner, and authoritative visual gates are pending | Best predecessor machine-verified Opera runtime; superseded as the current navigation baseline by `09e5e356` |
| Castle-room distribution runtime `09e5e356`, probe-readiness `ff068db`, product source `51d0abc0`, and integrated evidence head `441adf35` | **Best current audited Opera runtime, 3/5**; `MA-OPERA-012` `FIXED_PENDING_VERIFICATION` | All 13 careers have exact thematic room owners; Movie Lounge is Racer's sole home; the central lobby is deleted with no hidden backdoor; exact-room return, stable sparse save bits, rewards, layer ownership, pause/re-entry, and teardown are proved. Runtime `09e5e356` passes full exact-Godot CI in 1463.4 seconds; probe-only `ff068db` passes the newer 1379.3-second/64-probe full-local suite. Product source `51d0abc0` passes exact local CI in 1,404.5 seconds/all 64; governance-only `441adf35` passes exact local/topic/dev machine gates and has Android `31763879294`; 9 route plus 13 career captures exist | Pre-fix run `31678156887` remains red from fixed-four-frame fade sampling. Historical Sky 21/44/DONE and `7391c53c`'s failed remote renderer subprocess remain predecessor history. Current Sky remote subprocesses also fail requested-Mobile renderer identity and provide PNGs only. Device, child, owner, exact-voice, listening, strict-2D, and accepted-visual review remain open; lower-center route cards obscure Roshan's lower body/tail in all nine room captures | Current implementation winner and correct navigation baseline; keep `FIXED_PENDING_VERIFICATION`, preserve exact integrated machine/APK evidence, and repair residual P2 card composition before acceptance |
| Old generic/incorrect Ballerina versions | Rejected/superseded, **1–2/5** | Demonstrated basic phase flow | Human legs/feet or old art, generic PHRASE/POSE/RIBBON/TWIRL logic, and misleading looped playback | Preserve only as rejection/history evidence |
| Integrated Ballerina A-atlas and three-act specialist (`0447188f` lineage, retained in `09e5e356`) | **Best current Ballerina, 4/5** | One-tail accepted identity, Pearl Mirror/Ribbon Trail/Grand Twirl, held poses, one-shot cheer, assists and probes | Final two-aspect/M11/child/owner evidence remains | Keep as current authority |
| Device-acceptance Ballerina branch `fd0f1813` | Diverged evidence branch, **3/5** | Adds dedicated Ballet shot sizing/device-review tooling | It diverges from current audited source `51d0abc0` and is not the integrated runtime | Salvage focused probe/evidence ideas only after rebase |
| Game-wide animation-doubling branch `20e9b1f2` | Clean committed post-snapshot candidate, **3/5 potential 4** | 159 compositions grow 921→1842 cels; focused audits pass 13 Opera careers/416 cells, 39 Castle fixtures/624 cells, playground 24 cells, and 14 imp families/302 cells | Based directly on pre-audit `ea6185fd`, changes 694 files, has no exact-head remote run, and a GAME2D comparison fails with 1,132 findings: 771 models, 76 production-3D and 85 probe-3D files; it retains the legacy 3D Racer path | Cherry-pick/rebase bounded art/runtime pieces onto the audit line only after identity, memory, M11, strict GAME2D, and full CI review; never merge wholesale |
| Boxer V1 specialist (`8d67c2bd`, integrated) | **Best implemented Boxer, 4/5** | Five phases, true Canvas, two gloves, one-finger sequential completion, no loss | Device/child/owner acceptance and legacy GLB retirement remain | Keep and finish external acceptance |
| Boxer V2 branch `ed4851a0` | Docs-only concept, **not implemented** | Strong deterministic counterboxing/mastery design without punishment | 782-line proposal only; added complexity and optional Jolt/3D language conflict with final medium | Review as a future design, not a game version |
| Candymaker pre-`39746756` | Superseded, **2/5** | Core pour idea existed | Cropped/conflicting mold, small/poorly registered pour, weak phone causality | Do not restore |
| Candymaker Pixel 10 repair `39746756` | Strong repair, **4/5** | Complete mold shell, generous target, measured spout, 30/60 fps monotonic tests | Earlier visual state set | Valid ancestor and fallback comparison, not the newest art |
| Candymaker authored syrup rebuild `cd39cae4`, retained in `09e5e356` | **Best current Candymaker, 4/5** | Authored empty mold, cavity fill, full/empty ladle, provenance and expanded probes | Device/owner/child acceptance still open | Keep as current version |
| Current generic Painter retained in `09e5e356` | Integrated development version, **3/5** | Functional sunrise paint/stamp/gallery route, now discovered from the Craft Room | Less purposeful artifact and continuity than the newer proposal | Current implemented Painter until a replacement is cleanly integrated |
| `codex/painter-purpose-20260811` worktree | Uncommitted candidate, **potential 4/5** | Four continuous party-banner steps, helper, persistent result, one-finger purpose | Branch ref equals `ea6185fd`; actual 12-file plus untracked-surface implementation is dirty and unproven at an exact commit; save/logo coupling is broad | Review and rebuild as a bounded commit; do not credit or merge the worktree |
| `codex/arborist-tree-doctor` worktree | Uncommitted fourteenth-career candidate, **potential 4/5; current 1/5 because absent** | True Canvas/PNG tree-care game with inspect, prune, root-water, wrap, bloom; coherent caregiving fiction and dedicated art/probe | Ref is stale `ecad384e`; implementation/art are dirty/untracked, five exact family voices are missing, and no exact-head full/device/owner evidence exists | There is no missing Arborist 3D “base model” to import; finish the Canvas career as a clean rebased feature if the owner accepts it |
| Canvas Racer plus current lifecycle repair | **Best Opera Racer, 4/5** | Simple circle gesture, exact speech, one ordinary/display Canvas implementation, passive/replay/teardown/re-entry coverage, and green full-local/exact-head gates | Device/child/owner verification remains | Keep the current single Canvas path; never restore the split or external kart |
| Unmerged Claude Opera story/diversification branch `55ba40d8` | Docs-only proposal, **not implemented** | Useful narrative/diversification ideas | Three documentation commits, no current runtime or accepted asset evidence | Review after current careers meet capture/device/child gates |

The overall current implementation winner remains runtime **`09e5e356`**, with
probe/evidence follow-up **`ff068db`**. The runtime realizes the
owner-directed Castle-room distribution, keeps only Ballerina, Pop Star, and
Magician in Opera Hall, resolves Racer to Movie Lounge, deletes the all-career
lobby, preserves the sparse save namespace, and passes the full local exact-
Godot suite; the follow-up changes no production behavior and makes route
readiness fail closed. Exact parent `e6edf559` preserves those runtime bytes and
passes dev Probe Suite run `31722047536`; earlier branch run `31719143975` is
corroborating e6 history. Historical source `7391c53c` and overall run
`31728755204` retain its failed remote Sky renderer subprocess. Current source
`51d0abc0` preserves Opera behavior and passes exact official-Godot full local
CI in 1,404.5 seconds/all 64. Governance-only integrated head `441adf35`
passes exact local CI in 1,391.5 seconds/all 64 and topic/dev Probe runs
`31760207048`/`31762132976`; Android `31763879294` publishes its matching
596,033,220-byte APK at SHA-256
`f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`.
Run-14 Sky outputs are a 20/20 local
approval candidate with manifest/PNG/probe hashes—not a source-revision,
device, owner, or accepted-visual proof.
Their product rollback record is `CHG-027`, authority synchronization is
`CHG-028`, and the later sealed fail-closed document-control migration is
`CHG-029`; Sky diagnostic ownership is `CHG-030`. Device, child, owner,
exact-voice, listening, strict-2D, and
accepted-visual gates remain open, so the result is not verified or release-
ready. Within
the repair base, Dolls, Seek, the picture
games, Ballerina, Boxer, Candymaker, Racer, Chef, and Nursery are the strongest
individual activities. “Best” still means **best source to repair**, not 5/5
or ready for promotion.

---

## 2. Audit-state taxonomy

### 2.1 Audit-cycle states

| State | Meaning | This round |
|---|---|---|
| `INVENTORYING` | Enumerate code, assets, documents, probes, reports, owner decisions, and external evidence | Complete for the synchronized repository; external journal/device/child evidence remains absent |
| `AUDITING` | Compare behavior, presentation, architecture, and evidence with named rules | Complete for current static scope; runtime/device scope incomplete |
| `CONFIRMING` | Reproduce or falsify reports and reject stale premises | In progress for coverage gaps, device, child, protected voices, and manual art review |
| `TRIAGING` | Assign severity, lifecycle, verification, duplicates, supersession, and ownership | Complete for indexed items here; repeated when new evidence arrives |
| `REPAIRING` | Fix one confirmed issue at a time | **Current overall state** |
| `VERIFYING` | Run focused, surrounding, full-suite, capture, device, and child gates | In progress for completed slices |
| `RE-AUDITING` | Repeat from a clean current build after the list closes | Pending |
| `SATISFIED` | Every condition in section 12 is met at one exact commit | No |

A later state never erases earlier evidence. A round can be repairing one
finding while confirming another and verifying a third.

### 2.2 Finding lifecycle

| Lifecycle | Meaning |
|---|---|
| `REPORTED_UNCONFIRMED` | A source reports it; current evidence has not reproduced it |
| `CONFIRMED_OPEN` | Current evidence reproduces it and no accepted fix exists |
| `IN_PROGRESS` | An authorized repair is actively being made |
| `FIXED_PENDING_VERIFICATION` | A repair exists but required verification is incomplete |
| `VERIFIED_FIXED` | Required closure evidence is recorded and green |
| `REGRESSED` | A previously verified fix fails again |
| `OWNER_DECISION_REQUIRED` | Competing valid outcomes require owner intent |
| `BLOCKED_EXTERNAL` | Required device, protected source, credential, private record, or person is unavailable |
| `DEFERRED_WITH_REASON` | Valid work is intentionally scheduled later; not silently open |
| `WAIVED_WITH_REASON` | A named rule violation is accepted for a bounded scope, owner, date, and review trigger |
| `DISMISSED_NOT_A_DEFECT` | Evidence shows the report violates no current rule |
| `DISMISSED_NOT_IN_PROJECT` | The idea or feature is no longer part of the project |
| `SUPERSEDED` | A later decision or implementation replaced the premise |
| `DUPLICATE` | Another finding is the canonical owner |

### 2.3 Severity

| Severity | Meaning |
|---|---|
| `P0 / BLOCKER` | Lost progress, unrecoverable activity, crash/wedge, release corruption, or primary path unavailable |
| `P1 / HIGH` | Major child-visible quality, comprehension, touch, identity, accessibility, medium, or release-evidence failure |
| `P2 / MEDIUM` | Material polish, performance, consistency, coverage, or maintainability risk |
| `P3 / LOW` | Bounded cleanup or minor child-visible defect |

### 2.4 Verification levels

| Level | Evidence |
|---|---|
| `V0 NONE` | No current evidence |
| `V1 STATIC` | Source, asset, hash, dimension, dependency, or deterministic static evidence |
| `V2 UNIT` | Falsifiable unit/stress tests with negative controls |
| `V3 RUNTIME` | Exact Godot 4.7.2-stable analyzer/import and focused/full trusted probes |
| `V4 CAPTURE` | Mobile-renderer screenshots/video at supported aspect ratios |
| `V5 DEVICE` | Target phone/M11 touch, performance, thermal, memory, audio, and squint evidence |
| `V6 CHILD` | Observed intended-child session without adult verbal instruction |
| `V7 OWNER` | Explicit owner identity/style/narrative/exception acceptance |

`reported` or `partial` evidence never closes a finding whose acceptance record
requires missing levels. `ERROR`, `WARN`, `MANUAL`, `INFO`, and `SKIP` are tool
results, not lifecycle values.

### 2.5 Document authority states

| State | Meaning |
|---|---|
| `OWNER_DECISION` | Direct dated owner direction; the newest conflict controls |
| `CANONICAL_CURRENT` | Current game-wide normative design or audit source |
| `PROPOSED_CANONICAL` | Prepared canonical source pending tracking, reconciliation, and gates |
| `BINDING_OPERATIONAL` | Current security, engine, workflow, save, or protected-asset rule |
| `BINDING_LEDGER` | Required provenance or exhaustive document inventory |
| `BINDING_DOMAIN` | Current rule for one narrow domain |
| `SUPPORTING_CURRENT` | Useful current detail that cannot redefine the canonical rule |
| `HISTORICAL_EVIDENCE` | Retained failure, implementation, or decision evidence; not current direction |
| `PROPOSAL_DEFERRED` | Unapproved future design; not a current bug or instruction |

Document authority and idea lifecycle are separate. A historical document may
preserve a useful measurement while its 3D recommendation is `SUPERSEDED`.

---

## 3. Authority and comprehensive design-language confirmation

### 3.1 Current precedence

1. Binding `SECURITY.md`, protected-asset/save rules, credential and filesystem
   safeguards, and the release workflow in `AGENTS.md`. A content or design
   decision never weakens these boundaries.
2. Direct dated owner product decisions within those boundaries; the newest
   controls its exact scope. These include the 2026-08-09 true-2D ruling and
   2026-09-05 chapter delegation, asset strategy, and mechanic-reuse direction.
3. Exact Godot 4.7.2-stable requirements and the remaining current operational
   rules in `AGENTS.md`, excluding its stale 3D clauses.
4. Canonical-current `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`.
5. A current domain document within its explicitly retained scope.
6. Historical audits and work orders as evidence only.

### 3.2 Current authority map

| Source | State | Scope |
|---|---|---|
| Owner's 2026-08-09 true-2D directions | `OWNER_DECISION` | Highest-precedence medium and resource-retirement decision |
| This audit | `CANONICAL_CURRENT` | Audit-item states, evidence, closure, and history for this round; section 5 remains an index linked to complete stable records |
| `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` | `CANONICAL_CURRENT` | Stable `DL-*` rules and acceptance contract, subordinate to binding operational/security rules and direct owner decisions |
| `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md` | `BINDING_OPERATIONAL` | Stable `CHG-*` change groups, benefit/risk/dependency evidence, and guarded per-change rollback plans; never permission to bypass protected-asset, save, security, medium, or release gates |
| `AGENTS.md` except named stale 3D passages | `BINDING_OPERATIONAL` | Engine, security, save, protected art, workflow, and release rules |
| `SECURITY.md` | `BINDING_OPERATIONAL` | Threat model and protected data |
| `WORKFLOW_BRANCHING_2026-07-18.md` | `BINDING_OPERATIONAL` | Dev/master promotion process |
| `ASSET_LICENSES.md` | `BINDING_LEDGER` | Current and historical asset provenance |
| `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` | `OWNER_DECISION` in sections 10 and 16–17; remainder mixed/deferred | Commit `7426c187` distributes all thirteen careers through Castle rooms and makes Opera Hall one venue; commit `3d1236fe` cuts Curtain Dragon, Shadow Phantom, and Midnight Maestro and retires their stable save bits in place; section-17 commit `ef2fd982` assigns any future boss fights to Ember-aligned henchmen without reviving the Opera bosses. Other chapter/story proposals remain deferred unless separately adopted |
| `BALLERINA_PARTY_REBUILD_2026-08-09.md` | `BINDING_DOMAIN` | Current three-act Ballerina interaction, held-pose playback, assistance, and verification contract; supersedes older Ballerina mechanics and atlas-playback claims |
| `MUSIC_AUDIT_2026-08-09.md` | `BINDING_DOMAIN` | Current 42-cue composition, delivery, routing, and human/device listening contract, except its nested 3D-kart row is superseded by the current Canvas Racer |
| `design/BOXING_GAME_PROJECT_2026-08-09.md` | `BINDING_DOMAIN` | Current five-phase Boxer specialist and no-loss/save contract; partially superseded only where its three retained GLBs are transition debt rather than accepted dependencies. `opera_rival_boxer_match.png` remains valid 2D identity/source art and provenance despite the source document's misleading “3D resources” heading; any legacy `Sprite3D` consumer is `MA-2D-002` callsite debt, not a defect in the PNG. |
| `OPERA_MINIGAME_QUALITY_AUDIT_2026-08-09.md` | `SUPPORTING_CURRENT` | Current non-destructive prop provenance and non-conflicting interaction repairs; partially superseded where its 52-phase count and old Ballerina, Boxer, and kart Racer descriptions are historical |
| `OPERA_QUALITY_OVERHAUL_2026-08-09.md` | `SUPPORTING_CURRENT` | Current career-quality rationale and 208-frame audit evidence; partially superseded where its 52-phase/19-mode baseline, single-`bop` Boxer, kart Racer, and chronological-loop claim for Ballerina are historical |
| `assets_src/imagegen/opera_minigame_quality_2026-08-09/REVIEW.md` | `SUPPORTING_CURRENT` | Codex visual/provenance review of 39 governed art outputs; owner review remains pending |
| `assets_src/imagegen/opera_roshan_animation_2026-08-09/PROMPTS.md` | `HISTORICAL_EVIDENCE` | Exact accepted generation prompts and hashes; provenance, not runtime direction |
| `tools/audit_game_2d.py`, manifest, and tests | `BINDING_DOMAIN` | Exact shrinking-debt inventory and zero-debt enforcement |
| `tools/audit_roshan_2d.py` and tests | `BINDING_DOMAIN` | Narrow no-model Roshan enforcement; not whole-game 2D satisfaction |
| `tools/audit_roshan_sprite_clipping.py` and current frame roster | `BINDING_DOMAIN` | 2D source-frame cutoff/ghost/import contract |
| Current cinematic protocols and `tools/audit_cinematic.py` | `BINDING_DOMAIN` | Full-frame cinematic-only delivery |
| `VISUAL_AUDIT_TOOL.md` methodology | `BINDING_DOMAIN` | Fresh-runtime visual evidence, Canvas-only runtime staging, falsifiability, and explicit unresolved-evidence contract at `3b7a7e66` plus `fea916a8` |
| `codex/deprecated-resources-roshan-20260809` at `9329d9a6` | `HISTORICAL_EVIDENCE` | Exact archived 3D resources; never a production fallback or merge source |
| Owner commits `0277071f`/`9a1754c1`, 2026-08-25 | `OWNER_DECISION` | The true-2D three-floor Opera House venue (`scripts/opera_house_venue_2d.gd`) is the Opera Hall room interior hosting only its three resident careers through invisible painted portal regions; it preserves the no-central-lobby ruling and is the newest owner direction on Opera navigation |
| `MASTER_AUDIT_2026-08-26.md` (this directory) | `SUPPORTING_CURRENT` | The 2026-08-26 code-refinement round record: comprehensive analysis at integration head `9a1754c1`, scorecard movement, goal set G1–G12, and orchestration rationale; its normative deltas are applied in this document's sections 5, 12, 13, and 14 and in design 06 section 18 |
| `BOSS_ENCOUNTER_VISUAL_AUDIT_2026-09-05.md` (this directory) | `SUPPORTING_CURRENT` | Scoped Grand Puff, reusable encounter-cue and bounded CombatTutorial evidence. `BEV-001`–`005`/`010` map to `MA-VIS-006`, `MA-PLAY-001`, `MA-TOUCH-001` and `MA-2D-002`; `BEV-006`–`009` map to `MA-2D-002`, `MA-VIS-006` and the exact-voice gap. Focused V3 and tracked source-bound local agent-review V4 do not change canonical lifecycle, baseline counts or `UNSATISFIED`. |
| `design/08_TARGET_ARCHITECTURE.md` | `BINDING_DOMAIN` | The Mode Platform remodel, produced on direct owner request 2026-08-26: the growth law (`DL-CODE-11`), the GameMode/ModeRegistry/ModeDirector/Services contracts, the structure ratchet (`DL-CODE-12`), and migration plan M0–M6 that absorbs goals G7/G10/G11's structural halves. Section 9 of that document reserves four design decisions for explicit owner confirmation; the rest binds as each migration step lands suite-green |
| `design/09_CHAPTER_DEVELOPMENT_GUIDE.md` and `design/templates/CHAPTER_BRIEF_V1.md` | `BINDING_DOMAIN` | Owner-directed chapter delegation, asset/mechanic reuse, planning method, and required brief fields under `DL-PLAN-01` through `DL-PLAN-06`; no new product acceptance |
| `design/10_CHAPTER_REFERENCE_LIBRARY.md` | `SUPPORTING_CURRENT` | Source-linked continuity, seed patterns, asset discovery, and dated implementation availability |
| `design/chapters/NORTHERN_ICE_WORLD.md` | `BINDING_DOMAIN` for owner direction; detailed proposals deferred | Northern future-chapter planning and restaurant/customer-order opportunity; exact art binding and runtime implementation remain open |
| `CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md` | `SUPPORTING_CURRENT` | Implementation work packages for the 2026-08-26 round, addressed to the implementing agent; subordinate to this audit's protocol and gates |

### 3.3 Design-language confirmation state

The canonical comprehensive design language is based on the current owner
decision and triage of prior masters, audits, repair records, art rules,
touch/voice/save contracts, and current machine evidence. Its child, visual,
interaction, motion, audio, cinematic, performance, save, provenance, and QA
rules are current.

Both documents are tracked. Commit `9289dd81` reconciled
`AGENTS.md`, `CLAUDE.md`, `design/00` through `design/05`, and the named
medium-authority surfaces to game-wide true 2D without weakening security,
save, protected-art, engine, cinematic, or release rules. The previously
proposed state required:

- the documentation ledger covers every tracked Markdown path exactly once;
- every material active audit item links to a complete canonical record; and
- a documentation gate proves unique IDs, resolvable references, lifecycle
  validity, table/fence integrity, and forbidden current 3D claims.

CHG-029 sources `5ed0c754`/`7eb94595` satisfy those structural requirements.
Exact CHG-023 maintenance checkpoint `51887315` then passes official Godot
4.7.1 full local CI in 1,435.2 seconds/all 64 and exact-head Probe Suite run
`31710377034`, including the 36-test/six-stress document gate and 316/316 plus
36/36 parity. The audit and design language are therefore
`CANONICAL_CURRENT`. This authority transition does not weaken direct owner,
security, protected-asset, save, engine, workflow, or release rules, and it does
not make the still-`UNSATISFIED` game-wide audit complete.

---

## 4. Evidence at the integration snapshot and named historical commits

### 4.1 Repository snapshot

| Fact | Result |
|---|---:|
| Tracked Markdown files | 316 |
| `scripts/main.gd` | 8,734 lines at current source `51d0abc0` (historical `09e5e356`: 8,647) |
| GDScript files under `scripts/` | 195 |
| `scripts/probe_*.gd` files | 106 |
| Names in the local trusted loop | 64 |
| Names in the remote headless trusted loop | 63 |

The sole intended loop difference is the display-only
`probe_human_art_audit`; `probe_opera_pipe` remains in both blocking loops.

### 4.2 Game-wide true-2D gate

#### 4.2.1 Historical full checkpoint at `344d8d5c`

```text
GODOT=<exact Godot 4.7.1-stable binary> scripts/ci.sh
exit 0
61 trusted local probes reached accepted verdicts
GAME2D unit contract: 73 tests OK
GAME2D stress contract: 14 falsification/control assertions ALL OK
GAME2D regression gate: NO_REGRESSION at 513 models / 70 production files
```

This historical checkpoint verifies `MA-2D-003`: the guarded manifest at
`344d8d5c` matches
the Opera and medal shrink, and the stale-entry failure is gone. The full suite
does not make the game 2D: `NO_REGRESSION` explicitly means the exact baseline
did not grow while strict debt remains.

The self-tests prove the scanner can fail for model payloads, disguised files,
archives, sidecars, runtime APIs, dynamic loaders, custom data, native/plugin
sources, scene/config debt, incomplete history, and dishonest refreshes.

#### 4.2.2 Last completed full and manifest checkpoint at `a3d3bce1`

The synchronized runtime HEAD completed the exact local full gate:

```text
GODOT=<exact Godot 4.7.1-stable binary> scripts/ci.sh
exit 0 after 1434.3 seconds
fresh import completed
all static gates completed successfully
GAME2D regression: NO_REGRESSION at 509 models / 68 production files
all 61 trusted local probes reached accepted verdicts
```

The run repeatedly emitted nonfatal invalid-UID fallback warnings for
`assets/props/gen2/sponge_tubes.glb` and
`assets/props/gen2/starfish.glb`. They did not fail the gate. Later source and
isolated-import review proved the warnings came from four stale ignored local
`.godot/imported` cache files rather than the tracked GLBs or sidecars, so
`MA-ASSET-005` is dismissed as a source defect. The GLBs themselves remain
unrelated game-wide 3D medium debt under `MA-2D-002`.

The same synchronized clean HEAD was also checked in all three GAME2D modes:

```text
python -B tools/audit_game_2d.py
exit 0
GAME2D| DEBT| model_files=509| model_scan_coverage_files=0| active_export_model_files=509| model_import_sidecars=157| active_untracked_model_import_sidecars=352| model_archive_files=0| production_3d_files=68| probe_3d_files=77| scene_3d_files=1| configuration_3d_files=1| archive_now_model_files=0
GAME2D| STATUS| UNSATISFIED
GAME2D| RESULT| UNSATISFIED - inventory is exact, but tracked/active 3D/model debt remains

python -B tools/audit_game_2d.py --regression
exit 0
GAME2D| RESULT| NO_REGRESSION - exact shrinking baseline; migration debt remains UNSATISFIED

python -B tools/audit_game_2d.py --strict
exit nonzero
GAME2D| RESULT| STRICT FAIL - migration debt remains; known debt is not a waiver
```

Commit `a3d3bce1` removes only the proved stale entries produced by the Dolls,
Seek, visual-probe, and surrounding-code shrink. Default exit zero proves that
the current inventory exactly matches the guarded manifest. Regression exit
zero proves that the baseline did not grow. Neither is `PASS`; strict truthfully
remains red. The exact `a3d3bce1` full run proves current import, static gates,
and all trusted probes; it does not satisfy strict 2D, visual, warning-free,
APK, device, voice, child, or owner acceptance gates. Any later code, art,
import, probe, or audit-tool change must earn a new exact full checkpoint.

#### 4.2.3 Historical CI repair, local merge integration, and remote verification

Historical merge `f3b0de078898a8b4faddb2c738c4403180eff928`, with parents
`ea6185fdb1a687a20a6d118bdc368400e2c30f60` and
`5f58ef0a9db7aa9593f85131e1b855e51b84aea8`, reconciles the complete audit
history into the newer `origin/dev` runtime. Its runtime/static content
completed the local full gate below. Workflow/parity repair `dacef140` remains
historical remote evidence for its own exact head; it is not remote evidence
for `f3b0de07`. Its focused evidence was:

```text
GAME2D unit contract: 74 tests OK
GAME2D stress contract: 14 falsification/control assertions ALL OK
GAME2D exact inventory: 509 models / 509 active exports
GAME2D sidecars: 157 tracked / 352 active-untracked generated
GAME2D source debt: 68 production / 77 probe / 1 scene / 1 configuration
GAME2D regression: NO_REGRESSION
GAME2D strict/default inventory state: UNSATISFIED
Opera deterministic/generated art and provenance gates: ALL OK
Opera diegetic hotspot and borderless-minigame art gates: ALL OK
Opera Roshan animation audit: 13 careers / 208 reviewed frames ALL OK
Area-music deterministic build check: 42/42 ALL OK
Probe parity audit (default and stress): ALL OK
Exact merge-integration scripts/ci.sh: exit 0 after 1437.1 seconds
All 64 trusted local probes reached accepted verdicts
```

The complete local integration gate uses exact Godot 4.7.1-stable, performs the
fresh import, static gates, GAME2D regression check, analyzer, and all 64
trusted local probes, and exits zero after 1437.1 seconds. Current Opera is 13
careers, 53 playable phases, and 27 modes; its newer diegetic rooms,
borderless art, phone-safe Candymaker, current Ballerina/Boxer specialists, and
display/forced-2D Canvas Racer are all present. Exact-head GitHub run
`31457593351` at `dacef140` remains valid historical evidence for that older
SHA only.

The historical newline-stability CI-repair checkpoint is
`af4189a99cfd5a32d0df0f75185f6912d3889399`. Its parent `bbc817ef` contains
the prior documentation synchronization above the
`f3b0de07` merge. Exact-head run `31648427712` at `bbc817ef` succeeded in the
pinned Windows area-music job with 42/42 deliveries, then failed only in the
Ubuntu static step: the generated Opera provenance recorded a raw CRLF hash
for declared text input
`assets_src/imagegen/opera_candymaker_syrup_2026-08-10/GENERATION.json`, while
the Linux checkout supplied LF bytes. Import, analyzer, the 63 remote probes,
boot, and runtime captures did not execute and cannot be inferred green.

Repair `af4189a9` LF-canonicalizes hashing only for that declared text input,
preserves byte-exact hashing for every binary input, and refreshes the checked
provenance. Ten focused checker tests, a Windows Opera-art check of 42/42, and
an LF-clean archive check of 42/42 are green. This is focused repair evidence,
not a new full local checkpoint. Replacement exact-head run `31649113587` at
`af4189a9` succeeds: the Ubuntu probes job completes in 35m27s with static
checks, import, the full analyzer, all current 63 remote trusted probes, boot,
Dust/Opera advisory balance, and the Opera manifest green. All five diagnostic
capture/upload workflow steps complete and upload artifacts; the pinned Windows
music job completes in 3m55s with 42/42 deliveries green. The five captures remain diagnostic artifacts and
grant no authoritative visual PASS. This closes exact-head remote CI for the
repair checkpoint only. A full local suite at `af4189a9`, matching APK, Mobile
acceptance capture, target device, child, owner, listening, strict-2D, and
authoritative visual evidence remain pending.

#### 4.2.4 Preceding Opera retirement/lifecycle slice — focused, full local, and exact-head remote green

Commit `e2c25878`, built from audit checkpoint `41087f66`, has this bounded
evidence:

```text
Exact Godot: 4.7.1.stable.official.a13da4feb
Exact focused Opera/lifecycle/save/surrounding matrix: ALL OK
Commit e2c25878 scripts/ci.sh: exit 0 after 1428.6 seconds
Trusted local probes: all 64 green
GDScript parser, inference lint, Godot --check-only analyzer, import, and static gates: green
GAME2D unit contract: 74 tests OK
GAME2D stress contract: 14/14 falsification/control assertions ALL OK
Visual-contract unit tests: 93 tests OK
GAME2D exact inventory: 509 models / 509 active exports
GAME2D sidecars: 157 tracked / 352 active-untracked generated
GAME2D source debt: 66 production / 74 probe / 1 scene / 1 configuration
GAME2D regression: NO_REGRESSION
GAME2D strict/default inventory state: UNSATISFIED
Castle interaction approval candidate: 1754c880e4ef3df87daed47e1a8ec1ed36e114956ae86dbc50a74e40bba392d9
Castle candidate ledger coverage: 13 assets / 104 frames
Opera V4 Mobile diagnostic review: 17 captures at 1280x720, visually inspected
Exact-head verification SHA: e0677ae4c4f5e48258ff57c38f82e25f2dc3d9d0
Exact-head GitHub run: 31661887863 SUCCESS
Ubuntu probes job: SUCCESS in 33m8s; all 63 trusted headings green
Remote GAME2D: 509 models / 66 production / 74 probe; NO_REGRESSION / UNSATISFIED
Windows music job: SUCCESS in 6m52s; MUSIC|check 42/42|picture_xmas
Remote visual output: five diagnostic capture/upload pairs; non-authoritative
```

The focused `probe_opera.gd` path enters through ordinary unforced
`main._start_opera_now()`, proves all thirteen and only thirteen live career
slots, exercises Racer without an external kart, rejects 45 idle frames per
career, preserves raw legacy bits, counts effective progress from mask
`0xBDEF`, awards +3 first-time/+1 replay and +50 exactly once, and covers
teardown/re-entry. It also proves an earned result survives application pause
and leaving during the curtain-call delay. Save fixtures cover historical
`opera_progress`, retired-only bits, all live bits, and old `0xFFFF` completion.
The surrounding Opera2D, Nursery, Detective, living-world, audio, load,
recovery, Castle-art, imp-animation, UI, and balance probes are green in the
focused matrix.

This predecessor evidence moves `MA-OPERA-010` and `MA-OPERA-011` to
`FIXED_PENDING_VERIFICATION`. It does not close them: the full local gate for
commit `e2c25878` and exact-head run `31661887863` at integrated SHA `e0677ae4`
are green, but external acceptance remains. The Castle candidate is
machine/review-ledger evidence, not
owner approval, and the seventeen V4 renders are diagnostic/review evidence
rather than target-device, child, owner, or authoritative visual acceptance.
At that checkpoint it did not implement the Castle-room distribution in
`MA-OPERA-012`. Current commit `09e5e356` does so in the following slice. The
global audit remains `UNSATISFIED`.

The Castle Kitchen controller was deliberately left unchanged. Its current
Chef config is valid and covered by the focused path. A speculative recovery
branch for a future invalid `OperaAct.start()` result would modify a sealed
Castle visual controller and requires renewed owner visual approval; that
latent hardening remains separate `MA-CODE-002` debt.

#### 4.2.5 Castle-room career distribution — full local and exact-head remote green; external verification open

Commit `09e5e35665fd8d1bd782693e10fc0198f756d2c8` implements the owner-directed
distribution without changing the thirteen live career identities or sparse
16-bit save namespace. Probe-only follow-up
`ff068db002202839f920a6f9fb78c942788a3034` preserves those runtime bytes:

```text
Exact Godot: 4.7.1.stable.official.a13da4feb
Exact focused Castle/Opera/lifecycle/save/layer matrix: ALL OK
Commit 09e5e356 scripts/ci.sh: exit 0 after 1463.4 seconds
Commit ff068db scripts/ci.sh: exit 0 after 1379.3 seconds
Trusted local probes: all 64 green
GAME2D exact inventory: 509 models / 66 production / 74 probe / 1 scene / 1 configuration
Castle room-route captures: 9 at 1280x720, diagnostic
Opera career captures: 13 at 1280x720, diagnostic
Pre-fix exact-head run 31678156887 at 3fc151c8: RED, probe readiness sampling only
Historical authority-head run 31686380560 at 9befc0f8: SUCCESS, 63 remote headings
Predecessor dev-head Probe Suite 31693492735 at 18b6150c: SUCCESS, 63 headings, probes 29m41s, music 42/42
Predecessor dev-head Android run 31695675866 at 18b6150c: SUCCESS
Matching predecessor APK: 596041412 bytes; SHA256 fb4979473441d416f7b07914b1396f5f883935d4c08bf077baed3dfb91b78941
Historical CHG-023 Probe Suite 31710377034 at 51887315: SUCCESS, 63 headings, probes job 41m12s, trusted loop 18m02s, music 42/42 ALL OK in 4m08s
Earlier branch e6 Probe Suite 31719143975: SUCCESS, 63 headings, probes 33m18s, music 42/42 in 4m24s
Integrated-predecessor dev Probe Suite 31722047536 at e6edf559: SUCCESS, 63 headings, probes 34m25s, document 36/stress 6/316 parity/34 active/36 retained, music 42/42 in 3m33s
Integrated-predecessor Android run 31724927769: raw checkout/package source e6edf559, SUCCESS
Latest predecessor APK: 596041412 bytes; SHA256 66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c
```

`scripts/castle_career_routes.gd` is the single mapping authority. Royal Kitchen
owns Chef/Candymaker; Opera Hall Ballerina/Pop Star/Magician; Royal Library
Detective; Craft Room Painter; Stuffie Playroom Doctor/Boxer; Bubble Bath
Nursery; Mermaid Pool Astronaut; Family Dining Room Farmer; and Movie Lounge
Racer. `scripts/opera_lobby_2d.gd` is deleted. The Opera Hall guide can activate
only its current visible room card; stale or direct tuples are revalidated and
cannot become a hidden all-career backdoor. Every launched activity restores
the exact room, room music, HUD, player, and touch state that owned it.

The probe contract also fixes the layer stack: career 10, Opera ambient 11,
HUD/caption 12, Opera pause 13, Castle 14, Castle ambient 15, Castle pause 16,
with the shared pause sheet/fade at 29/30. Stable live mask `0xBDEF`, permanent
tombstones 4/9/14, first-win/replay rewards, passive rejection, pause, close,
teardown, and re-entry remain green.

Run `31678156887` is retained as a real failed run, not rewritten as green and
not dismissed as a workflow-regex false positive. Ubuntu reached the compound
stable-Canvas assertion after only four process frames; Detective and Nursery
were sampled while the 0.25-second reveal still intentionally suspended the
LivingWorld transition from Castle ambient layer 15 to Opera layer 11. Their
raw viewport-touch launches, passive safety, saves/rewards, exact-room returns,
dedicated probes, and every other executed gate/probe passed; Windows also
passed. `ff068db` changes only `scripts/probe_opera.gd`: it uses a bounded wait
for the Opera instance, completed/input-transparent reveal, exact
`opera.act.NN` stage, and layer 11, then hard-fails with observed state if that
semantic readiness never arrives. This is an evidence repair, not a production
runtime change. Exact successor authority head `9befc0f8` passes replacement
run `31686380560`: Ubuntu completes the 63-heading machine-gate workflow in
33m40s and Windows ends music 42/42 in 3m47s. All five capture/upload pairs
completed at the workflow level and uploaded diagnostic artifacts, but they are not capture gates or
visual passes; raw Sky Lagoon `LAGOONSHOT` output has 21 `OK`, 44 `FAIL`, and
`DONE` (66 diagnostic lines), so that diagnostic internally fails. The run also
retains existing Vulkan fallback and resource-leak diagnostics and is not
warning-clean.

Predecessor integrated dev/audit head `18b6150c` passes its exact-head Probe Suite run
`31693492735`: exactly 63 remote trusted headings complete in the 29m41s probes
job and music ends 42/42. Its capture output is still diagnostic/nonaccepted;
raw Sky Lagoon remains 21 `OK` / 44 `FAIL` / `DONE` and the artifact contains
20 PNGs. Android dev run `31695675866` succeeds at the same exact head and
publishes a 596,041,412-byte APK with SHA-256
`fb4979473441d416f7b07914b1396f5f883935d4c08bf077baed3dfb91b78941`.

Historical CHG-023 verification head `51887315` separately passes exact-head
Probe Suite run `31710377034`; no matching `51887315` APK exists. That bounded
predecessor evidence
moves `MA-OPERA-012` to `FIXED_PENDING_VERIFICATION`; it does not
close it. The 22 renders are diagnostic, and the nine route captures reveal a
residual P2 composition defect: the 154×154 lower-center choice cards do not
collide with controls, but they obscure Roshan's lower body/tail. Current
integrated-predecessor `e6edf559` machine and matching-APK evidence are green.
Historical predecessor source `7391c53c` completes overall remote run `31728755204`, while its
Sky subprocess fails required-Mobile renderer identity; matching-APK evidence
remains open. Device, child
comprehension/navigation, owner review, exact-voice closure, human listening, strict-2D
satisfaction, and accepted visual evidence are still required.

#### 4.2.6 Historical CHG-030 Sky Lagoon capture diagnostic — local source green; product and remote acceptance remained open

This subsection is retained as predecessor evidence at `7391c53c`. Its
present-tense statements describe that checkpoint only and are superseded for
current product authority by the true-Canvas `51d0abc0` evidence in sections
1.4, 4.4, 5, and `EV-VIS-007`.

Commit `7391c53cd6981a256bd8bfe40ccbb9f72fb723fe`, exact parent
`e6edf559af219edd4e5ce38cab0c5094483be5c6`, is a two-file diagnostic slice:
`scripts/probe_sky_lagoon_art.gd` plus its exact entry in
`tools/game_2d_migration_manifest.json`. It changes no runtime, gameplay,
workflow, save schema, protected art, voice, friend, asset, or final-medium
content. The probe's SHA-256 is
`f28413263c0bedeed421fae6e9de4626095f03b6010bade8380ad7fb5aa07db9`; the
updated GAME2D manifest SHA-256 is
`8c70b9aeaba5302322bdd44ca84d8a2b76fca053a091753e0e04676ee407fb00`.

The exact official `4.7.1.stable.official.a13da4feb` full local
`scripts/ci.sh` run exits zero after 1,402.3 seconds with all 64 trusted probes.
The focused renderer run uses `mobile`, Speedy quality, the production player
camera, and a 1280×720 viewport. It writes the exact twenty ordered arrival,
route, animal, playground, action, castle, day, and night captures; all 20 rows
pass, all 20 PNGs are present, and all 1,078 semantic/render/save assertions
pass. The manifest proves the normal save and backup fingerprints unchanged,
isolated-save cleanup, in-memory plane-departure restoration, time-of-day
restoration, target/action/animal state, output identity, and nonblank renders.

That was reliable **local Mobile diagnostic generation**, not visual acceptance. The
predecessor workflow marked the capture step `continue-on-error` and uploaded PNGs only;
it did not upload the JSON manifest or make its result blocking. Predecessor-source
Probe Suite run `31728755204` completes overall `SUCCESS` after a 40m05s probes
job (17m50s trusted step, 63 headings) and 3m38s music job at 42/42. Its Sky
step is not green: raw output reports 20 PASS rows and the exact 20/20/20/20/0/0
summary, then `GLOBAL|FAIL|rendering_method|gl_compatibility`, `RESULT|FAIL`, and
process exit 1 because the runner lacks `VK_KHR_surface` and falls back from
required Mobile to OpenGL. `continue-on-error` masks that internal failure and
the artifact uploads PNGs but no JSON. Thus that predecessor's machine gates were
overall green, while its remote Sky diagnostic, renderer proof, APK, device,
child, owner, and art-acceptance gates remain open.
Historical runs `31686380560`, `31693492735`, `31710377034`, and `31719143975`
retain their 21-OK/44-FAIL/one-DONE predecessor result as history only.

Those predecessor frames prevented a false quality conclusion by exposing the
then-current one-mural/spatial promenade, small animals, subtle focus cues,
animal/Roshan overlap, weak grounding, and seesaw contact. Source `51d0abc0`
repairs that bounded cluster without changing approved source art:
`MA-VIS-002` is now `FIXED_PENDING_VERIFICATION`, while `MA-VIS-006` remains
`CONFIRMED_OPEN` for game-wide evidence and external acceptance.

### 4.3 Archive and resource-retirement evidence

- Archive branch `codex/deprecated-resources-roshan-20260809` is present locally
  and on origin at `9329d9a6`.
- Exact first-slice and orphan-slice model blobs were verified by content hash
  before deletion from the active branch.
- `86d0c243` retired 130 non-active model payloads, 57 tracked sidecars, and two
  model-bearing archives after archive verification.
- `0b75c60c` retired 124 active/export model payloads and 22 tracked sidecars
  after the hardened dependency proof found no exact, dynamic, packaged,
  iterator, formatted-loader, custom-data, or opaque production reachability.
- `27bda85d` retired `meadow_bush_0.glb` through `meadow_bush_3.glb` from the
  active tree only after their exact bytes were verified on the archive branch;
  the animated Canvas meadow owns no active model fallback.
- `archive_now_model_files=0` means no further retained model is currently
  proved removable solely as an orphan. It does not mean the remaining 509 are
  accepted; further removal requires tested 2D conversion or new dependency
  proof.

No protected file under `assets/book/`, `assets/audio/voices/`, or
`assets/characters/friends/` was modified by these retirements. Seek's protected
Evie/Lamb-a' sheet was read only as a reference; generated source masters and
non-destructive runtime derivatives landed at new paths.

### 4.4 Fresh-runtime visual evidence gate

Command:

```text
python -B tools/audit_visual_design.py --fresh-runtime --strict \
  --godot <exact Godot 4.7.1-stable> --no-report
```

At clean HEAD `a3d3bce1` the command exits nonzero with:

```text
VISUALAUDIT| ERROR=16  WARN=17  MANUAL=2  INFO=126  SKIP=86
VISUALAUDIT| STATE FAIL=16  REVIEW_OPEN=17  MANUAL_OPEN=2
VISUALAUDIT|       COVERAGE_GAP=86  WAIVED=0  PASS=32
VISUALAUDIT|       NOT_APPLICABLE=94  RESULT=UNSATISFIED
warning: fresh Godot probe unavailable (fresh runtime response contains no
rendered capture outputs); runtime checks will report COVERAGE_GAP
```

The historical `f3b0de07` local merge-integration audit and predecessor commit
`e2c25878` reproduce the same state totals: **16 FAIL, 17 REVIEW_OPEN, two
MANUAL_OPEN, 86 COVERAGE_GAP, 32 PASS, and 94 NOT_APPLICABLE**. The unchanged
totals are not evidence that either commit is visually accepted; they are an
advisory `UNSATISFIED` result. The
missing live Canvas capture matrix still fails closed. Exact-head run
`31649113587` uploads five diagnostic capture families, but those artifacts do
not satisfy the authoritative same-process fresh-runtime strict contract.
Commit `e2c25878` additionally rendered and visually inspected seventeen
1280×720 Mobile captures covering its lobby pages and thirteen career stages.
They are useful diagnostic/review evidence only: they do not change the global
16/17/2/86/32/94 totals and do not grant device, child, owner, identity/style,
or authoritative visual acceptance.

Current commit `09e5e356` retains those unchanged global
**16/17/2/86/32/94** totals and adds twenty-two 1280×720 diagnostic captures:
nine exact Castle room routes and thirteen career stages. They remain
non-authoritative and expose residual P2 lower-body/tail occlusion from the
route cards; they do not grant visual acceptance.

Commits `3b7a7e66` and `fea916a8` are the approved current visual-evidence
contract. They require a same-process random 256-bit one-use challenge, exact
Godot/Mobile/1280×720/stretch and clean-Git/source bindings, private immutable
capture snapshots, visible/hidden/restored target evidence, decoded-pixel layer
identity, alpha-aware coverage/occlusion, effective Canvas ordering, real touch
reach, source projection, and closed state adapters. The contract imports the
canonical GAME2D classifier and treats active `Sprite3D`, other spatial classes,
low-level 3D server calls, model loads, and unresolved dynamic/native paths as
`FAIL` or `COVERAGE_GAP`, never Canvas proof. `fea916a8` additionally binds
active ignored/custom-root runtime sources so ignored production code cannot
escape source closure.

Saved JSON, saved PNGs, manual facts, re-encoded duplicate layers, labels, and
self-consistent renewed hashes have diagnostic value only. They cannot grant
PASS, suppress a static risk, or replace the private current-process challenge.
The current run therefore did not fall back to saved facts when the probe
returned no live Canvas captures; it failed closed with 86 coverage gaps.

The 17 review-open results comprise four current orphan-art families, eight Sky
Lagoon duplicate-generation families, two Fairy and two Lagoon source-average
palette/figure-ground risks, and Lagoon NPOT residency cost. The two manual
items remain Fairy and Lagoon phone/M11 squint review. Source averages may guide
triage but cannot confirm a rendered art defect. Fairy is now honestly labelled
`legacy_3d_debt`, not `overhead_canvas`; its two required runtime states remain
explicitly unimplemented coverage gaps.

### 4.5 Evidence boundaries

- Exact local `scripts/ci.sh` is historically green at runtime commit
  `a3d3bce1`, after 1434.3 seconds with fresh import, static gates, GAME2D
  `NO_REGRESSION`, and all 61 then-trusted probes. Current local merge commit
  `f3b0de07` completes the exact local gate in 1437.1 seconds with all 64
  current trusted probes. Historical remote run `31457593351` at `dacef140`
  independently completes both required jobs for that older SHA; it is not
  inferred as an exact-head result for the current branch. Run `31648427712`
  at `bbc817ef` proves its Windows area-music job only; the Ubuntu static
  newline-hash failure prevented import/analyzer/probe execution. Replacement
  run `31649113587` succeeds at exact `af4189a9`: Ubuntu completes static,
  import, full analyzer, all 63 remote trusted probes, boot, advisory balance,
  Opera manifest, and five diagnostic capture/upload pairs in 35m27s; Windows
  verifies music 42/42 in 3m55s. The repair checkpoint still has no full local
  suite.
- The earlier two invalid-UID warnings were reproduced as stale ignored local
  `.godot/imported` cache artifacts. Source GLBs and tracked sidecars are valid,
  and an isolated fresh project import is warning-free. Their reachable 3D
  resources remain medium debt under `MA-2D-002`, but no source-UID defect is
  inferred from that local cache.
- Strict GAME2D at historical full checkpoint `f3b0de07` was run and failed as
  required; predecessor commit `e2c25878` and current commit `09e5e356` remain
  `UNSATISFIED`, and no zero-debt result or full-suite result at `af4189a9` is
  claimed.
- No complete live visual-runtime capture matrix is claimed; fresh-runtime
  strict produced no accepted Canvas captures and failed closed. The five
  green remote capture/upload pairs are diagnostic and cannot fill this gate.
- Predecessor exact-head Probe Suite run `31693492735` is green at `18b6150c` with
  63 remote headings in the 29m41s probes job and music 42/42. Android dev run
  `31695675866` is also green at exact `18b6150c` and publishes the matching
  596,041,412-byte APK (SHA-256
  `fb4979473441d416f7b07914b1396f5f883935d4c08bf077baed3dfb91b78941`).
- Latest integrated predecessor `e6edf559` is green in dev Probe Suite run
  `31722047536` (63/63, probes 34m25s, document 36/six/316/34 active/36
  retained, music 42/42 in 3m33s). Android run `31724927769` uses raw
  checkout/package source exact e6 and publishes the latest predecessor APK
  (596,041,412 bytes; SHA-256
  `66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c`).
  Neither predecessor machine/build result supplies source-head, device, or
  acceptance evidence.
- No target-phone or M11 performance/thermal/audio/touch result is claimed.
- No observed child golden-path session is claimed.
- No owner identity/style acceptance is inferred.
- No human two-wrap, voice-mix, mono, or device listening result is inferred
  from deterministic audio checks.
- Painter purpose and Arborist remain uncommitted branch/worktree candidates,
  not current runtime facts. Boxer V2 is a docs-only branch candidate. The
  current Candymaker implementation is integrated.
- The 36 unnamed items mentioned by an off-repository Alpha journal are not
  imported as current bugs. The journal must be obtained or replaced by a fresh
  equally scoped audit.

---

### 4.6 Historical validation record moved from the satisfaction checklist

The following dated evidence was preserved from the former section-12 gate
paragraph on 2026-09-05. It is historical evidence only; the active gate uses
the current engine baseline and current roster. No new pass is claimed.

Historical `a3d3bce1` remains green for its then-current 61-probe
      suite; historical merge `f3b0de07` completes the full local gate in 1437.1
      seconds. Historical `dacef140` completes remote run `31457593351` for its
      own SHA. Run `31648427712` at `bbc817ef` proves Windows area music 42/42
      but stops in Ubuntu static checks on the declared-text newline hash; it
      remains a failed run. Replacement `31649113587` succeeds at exact
      `af4189a9` with both required jobs, all 63 remote trusted probes, boot,
      and deterministic music 42/42 green. No full local suite at `af4189a9`
      itself is claimed. Predecessor Opera commit `e2c25878` separately
      completes full local `scripts/ci.sh` under exact official Godot with exit
      0 after 1428.6 seconds; run `31661887863` succeeds at integrated SHA
      `e0677ae4` with all 63 remote probes and deterministic music 42/42 green.
      Distribution runtime `09e5e356` completes the full local suite in 1463.4
      seconds with all 64 trusted probes green. Pre-fix audit-head run
      `31678156887` is red only because Ubuntu `probe_opera` sampled the
      0.25-second reveal after four frames; every other executed gate/probe and
      Windows passed. Probe-only `ff068db` adds a bounded fail-closed semantic
      wait and completes the newer full local suite in 1379.3 seconds with all
      64 probes green. Exact authority head `9befc0f8` passes replacement run
      `31686380560` with exactly 63 remote headings in 33m40s and Windows 42/42
      in 3m47s. The run is not warning-clean. All five capture/upload pairs
      completed at the workflow level and uploaded diagnostic artifacts; raw Sky Lagoon output internally fails
      21 `OK` / 44 `FAIL` / `DONE`. First document-authority source `5ed0c754`
      then completes official-Godot full local CI in 1,359.8 seconds/all 64.
      Exact CHG-023 maintenance head `51887315`, parent `7eb94595`, is the latest
      completed full-local checkpoint at 1,435.2 seconds/all 64 and passes
      exact-head run `31710377034`: Ubuntu takes 41m12s, the trusted 63-heading
      loop takes 18m02s, and Windows music is 42/42 ALL OK in 4m08s. The run
      retains runner warnings, legacy resource diagnostics, and raw Sky Lagoon
      21 `OK` / 44 `FAIL` / one `DONE`; that is now predecessor history, not the
      current diagnostic. Historical source `7391c53c`, parent `e6edf559`,
      completes its local/overall-remote machine history while its Sky
      subprocess fails required-Mobile renderer identity. Current true-Canvas
      source `51d0abc0` passes exact local official-Godot CI in 1,404.5
      seconds/all 64 and run-14 is 20/20 local Mobile/Speedy with manifest/PNG
      and probe hashes `AEAC7C72…DE34` and `B9EAF5E0…9C6C`; its source revision
      remains unknown. Integrated head `441adf35` passes exact local/topic/dev
      machine gates and has a matching APK, while its remote Sky subprocess
      still lacks requested-Mobile PASS/JSON.
      This full matrix must repeat at the eventual release candidate, so
      release satisfaction remains unchecked.

---

## 5. Triage item index — not canonical finding records

This section is a navigation and lifecycle index. Its rows intentionally omit
many mandatory fields and therefore are not canonical finding records under
section 10 or Design section 17. `MA-*` remains a stable audit-item identifier,
but an indexed item may be called a canonical finding only after a linked record
contains every mandatory field. No abbreviated row is closure evidence.

Complete material canonical records are linked below, including retained
terminal history. The section-5 lifecycle tables remain
the compact navigation view; these links open the complete section-10 records:

| Domain | Canonical records |
|---|---|
| Medium and document control | [`MA-2D-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-2d-002), [`MA-DOC-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-002), [`MA-DOC-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-003), [`MA-DOC-005`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-005) |
| Visual and assets | [`MA-VIS-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-002), [`MA-VIS-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-003), [`MA-VIS-004`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-004), [`MA-VIS-006`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-006), [`MA-VIS-007`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-007), [`MA-ASSET-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-asset-001), [`MA-ASSET-004`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-asset-004) |
| Play, access, touch, and combat | [`MA-PLAY-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-001), [`MA-PLAY-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-002), [`MA-ACCESS-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-001), [`MA-ACCESS-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-002), [`MA-ACCESS-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-003), [`MA-TOUCH-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-touch-001), [`MA-COMBAT-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-combat-001) |
| Opera | [`MA-OPERA-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-001), [`MA-OPERA-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-002), [`MA-OPERA-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-003), [`MA-OPERA-004`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-004), [`MA-OPERA-005`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-005), [`MA-OPERA-006`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-006), [`MA-OPERA-007`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-007), [`MA-OPERA-009`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-009), [`MA-OPERA-010`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-010), [`MA-OPERA-011`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-011), [`MA-OPERA-012`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-012) |
| QA, audio, release, and external evidence | [`MA-PERF-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-perf-001), [`MA-CHILD-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-child-001), [`MA-RELEASE-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-release-001), [`MA-CI-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-003), [`MA-AUDIO-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-audio-001) |
| Deferred optimization and structure | [`MA-ROSHAN-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-roshan-003), [`MA-CODE-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-code-001), [`MA-CODE-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-code-002) |
| Code refinement (2026-08-26 round) | [`MA-CI-004`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-004), [`MA-CI-005`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-005), [`MA-CI-006`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-006), [`MA-CI-007`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-007), [`MA-CODE-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-code-003), [`MA-CODE-004`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-code-004), [`MA-CODE-005`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-code-005), [`MA-PERF-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-perf-002), [`MA-PERF-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-perf-003), [`MA-SAVE-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-save-001), [`MA-AUDIO-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-audio-002), [`MA-TOUCH-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-touch-002) |
| Font and typography (2026-08-30 round) | [`MA-TYPE-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-type-001), [`MA-TYPE-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-type-002), [`MA-TYPE-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-type-003), [`MA-TYPE-004`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-type-004), [`MA-TYPE-005`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-type-005), [`MA-TYPE-006`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-type-006), [`MA-TYPE-007`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-type-007) |

### 5.1 P0/P1 and acceptance-blocking indexed items

| ID | Severity | Lifecycle | Verification | Indexed issue | Closure requirement |
|---|---|---|---|---|---|
| `MA-2D-002` | P1 | `IN_PROGRESS` | V2/V3 partial | Source `51d0abc0` records 509 model/export files, 157 tracked model sidecars, 352 active untracked sidecars, 65 production 3D files, 70 probe 3D files, one 3D scene, and one 3D configuration; regression is exact `NO_REGRESSION`, all 14 stress controls pass, and archive-now is zero. Sky joins Dolls, Seek, and bounded Opera as converted/retired slices, but remaining active surfaces still enforce legacy 3D | All eleven GAME2D categories reach zero; strict gate, import, focused/surrounding/full probes green |
| `MA-DOC-002` | P1 | `VERIFIED_FIXED` | V2/V3 exact maintenance-head local plus remote | CHG-029 sources `5ed0c754`/`7eb94595` preserve the exact 316-path Git-declared Markdown inventory with 316 unique rows and explicit mixed/supersession scope. Exact CHG-023 maintenance head `51887315` passes official Godot 4.7.1 full local in 1,435.2 seconds/all 64 and Probe Suite run `31710377034`; 36 tests, six mutation controls, and 316/316 parity are green | Preserve one-row-per-path coverage as inventory changes; future drift regresses the terminal finding |
| `MA-DOC-003` | P1 | `BLOCKED_EXTERNAL` | V1 | An off-repository journal is said to hold 36 unnamed entries described as findings | Import source evidence or replace with fresh equal-scope audit; do not assume the entries are current |
| `MA-DOC-005` | P1 | `VERIFIED_FIXED` | V2/V3 exact maintenance-head local plus remote | CHG-029 sources `5ed0c754`/`7eb94595` provide all 36 material P1/P2 items as linked complete stable records with the mandatory exact field set. Exact CHG-023 maintenance head `51887315` passes official Godot 4.7.1 full local and Probe Suite run `31710377034`; 36 tests, six mutation controls, and then-current 36/36 active-record parity are green. After this and `MA-DOC-002` transition terminal, current parity is 34 active/36 retained records | Keep terminal records stable through future lifecycle transitions; later parity or field drift regresses the finding |
| `MA-VIS-002` | P1 | `FIXED_PENDING_VERIFICATION` | V3/V4 exact local source/capture plus integrated machine/build; external open | Source `51d0abc0` replaces the spatial promenade with an owned `CanvasLayer` -1, 6144×2048 `Node2D` master, 6×2 `Sprite2D` backdrop, differential layer stack, real parallax, and sole `Camera2D`. Exact source-byte CI is green in 1,404.5 seconds/all 64; run-14 is 20/20 local Mobile/Speedy with manifest/PNG/probe hashes, but its source revision is unknown. Integrated `441adf35` passes exact local/topic/dev machine gates and has a matching APK, while both remote Sky subprocesses fail requested-Mobile renderer identity and provide no JSON/Mobile PASS | Preserve true Canvas and pass requested-Mobile remote Sky proof, target-device, child, owner, and accepted-visual review; `SideScrollStage`, `Sprite3D`, capture-tool success, or filename-only relabeling cannot close it |
| `MA-VIS-003` | P1 | `REPORTED_UNCONFIRMED` | V1; `REVIEW_OPEN` | Reproduced source-average saturation diagnostics flag Fairy and Lagoon, but Fairy is probably a false positive/coverage gap and Lagoon is only a plausible hierarchy risk | True state-local Canvas composite with HUD/viewport/runtime/device evidence; do not recolor or regenerate approved art merely to satisfy the current average |
| `MA-VIS-006` | P1 | `CONFIRMED_OPEN` | V2/V3 contract plus V4 local Sky candidate and integrated machine/build | Source `51d0abc0` repairs the bounded Sky defects and run-14 supplies 20/20 locally reviewed Mobile/Speedy frames. Integrated `441adf35` adds exact machine/build evidence, but its remote Sky subprocess lacks Mobile PASS/JSON, no device/owner acceptance exists, and the global report remains 16 failures, 17 reviews, two manual items, and 86 coverage gaps | Implement every required live state adapter/capture; every applicable FAIL/REVIEW/MANUAL/COVERAGE_GAP explicitly resolved with device/owner review |
| `MA-VIS-007` | P1 | `FIXED_PENDING_VERIFICATION` | V3/V4 exact local and multi-review; integration/external open | The repeated Bubble Bath report was a layered pixel-ownership failure compounded by an abandoned branch, stale regeneration/review paths, and node-only probes. The repair regenerates seven Castle and two Opera complete backgrounds, retires both false bath cards and the incomplete tent-flap card, fixes the cupboard rest frame, binds every source/hash/route, reviews all 96 retained V4 frames against the exact runtime underlay, and passes exact Godot 4.7.2 Mobile one-bathtub dirty/clean captures plus the complete local CI suite | Preserve the fail-closed ownership/generator/frame gates; integrate the exact green topic to `dev`; then retain distinct target-device, child, and owner visual acceptance evidence before terminal closure |
| `MA-PLAY-001` | P1 | `CONFIRMED_OPEN` | V1/V3 partial | No end-to-end fresh-save, child-visible, no-cheat world reachability proof exists | Enter/leave/re-enter every visible destination without direct debug calls; save/seam/touch/voice checks |
| `MA-ACCESS-001` | P1 | `BLOCKED_EXTERNAL` | V1 | Required exact voice cues remain absent for some objectives | Authorized exact recordings or independently sufficient spoken/diegetic design; playback/device/child evidence |
| `MA-ACCESS-002` | P1 | `BLOCKED_EXTERNAL` | V1 | Lamba's current semantic role still maps to legacy “bunny-fish” recordings | Owner-approved re-record/re-render and exact-key/device listening evidence |
| `MA-ACCESS-003` | P1 | `BLOCKED_EXTERNAL` | V1/V3 partial | Seek has an accurate visual wiggle/U-cue/peek and an available Evie hide-and-seek recording, but no exact protected Evie recording says “tap the wiggly tree” | Owner-authorized exact Evie objective recording plus queue, device-listening, and child-comprehension evidence; do not modify protected audio |
| `MA-TOUCH-001` | P1 | `FIXED_PENDING_VERIFICATION` | V3 exact local automation | Source `51d0abc0` scopes Classic Sky taps, cancels Canvas travel/focus across manual input, pause, overlays, transitions, and focus loss, and passes real gear/resume plus 240-event stress; real-phone hold/drag/multitouch/focus-loss evidence is absent | Recorded target-phone pass |
| `MA-OPERA-001` | P1 | `FIXED_PENDING_VERIFICATION` | V3 partial | Chef now uses the accepted batter pitcher, source-true stream/fill behavior, mitt-gated oven, achieved cake, and deterministic topping art; the old cutoff/fallback/wrong-object report is not a current code premise. Current Chef config is valid/probed; speculative invalid-config recovery in the sealed Castle Kitchen controller was deliberately excluded pending renewed owner visual approval | Accepted two-aspect/device/owner art review; any later Castle caller hardening proceeds separately under `MA-CODE-002` |
| `MA-OPERA-002` | P1 | `CONFIRMED_OPEN` | V4 partial | Detective's “missing” crown remains painted into the scene evidence | Healed owned source, narrative/capture verification |
| `MA-OPERA-004` | P1 | `CONFIRMED_OPEN` | V1 | Opera capture harness has not produced accepted evidence for all careers | Repair harness; capture and human-review all careers/widgets/scuffles/stress states |
| `MA-OPERA-009` | P1 | `FIXED_PENDING_VERIFICATION` | V3 partial | Boxer now has a full-stage five-phase two-glove specialist with optional multitouch, sequential one-finger completion, no health/loss, passive rejection, touch-owner cleanup, and stable existing save bit. A newer Boxer V2 document exists only on an unmerged docs branch and is not current runtime authority | Two-aspect and target-device touch/performance review, child comprehension, and owner visual acceptance; separately review the V2 proposal before any authority or implementation change |
| `MA-OPERA-010` | P1 | `FIXED_PENDING_VERIFICATION` | V3 full local plus exact-head remote | Commit `e2c25878` uses one Canvas lifecycle for ordinary unforced and display entry and contains no external-kart route. Exact focused coverage, the full local Godot 4.7.1 startup/Racer/idle/passive/close/suspend/reward/teardown/re-entry gate, and exact-head run `31661887863` at `e0677ae4` are green | Pass authoritative Mobile/device/child/owner acceptance before closure; rollback is recorded under `CHG-026` |
| `MA-OPERA-011` | P1 | `FIXED_PENDING_VERIFICATION` | V3 full local plus exact-head remote | Commit `e2c25878` removes all three owner-cut bosses from cards, gates, completion, voices/music routes, and runtime. Slots 4/9/14 remain raw-preserving tombstones (`0x4210`), live mask/completion is `0xBDEF`, effective progress is 0–13, and focused/full-local/exact-head migration/reward/passive/suspend/leave/re-entry evidence is green | Pass authoritative visual/device/child/owner gates before closure; rollback is recorded under `CHG-026` |
| `MA-OPERA-012` | P1 | `FIXED_PENDING_VERIFICATION` | V3 exact local/remote/build plus V4 diagnostics; external open | Runtime `09e5e356` distributes all thirteen careers through exact thematic Castle rooms, selects Movie Lounge as Racer's sole home, deletes the all-career lobby with no hidden backdoor, preserves stable sparse save bits/rewards, restores the exact launching room, and fixes Canvas layers. Its full 1463.4-second/64-probe local suite is green; probe-only `ff068db` passes a newer 1379.3-second/64-probe full-local suite. Historical predecessors preserve bounded evidence. Integrated head `441adf35` preserves unchanged `51d0abc0` Opera behavior, passes exact local/topic/dev machine gates, and Android `31763879294` publishes its matching APK. Twenty-two local Opera/Castle 1280×720 captures remain diagnostic; all nine room captures show residual P2 lower-body/tail occlusion | Complete phone/M11, child navigation/comprehension, owner, exact-voice/listening, strict-2D, and accepted-visual gates; adjust route-card composition without weakening target size or reintroducing the hub |
| `MA-PERF-001` | P1 | `BLOCKED_EXTERNAL` | V0 | No current target-device frame-time, hitch, memory, thermal, or latency matrix | U0 device matrix at exact release candidate meets design thresholds |
| `MA-CHILD-001` | P1 | `BLOCKED_EXTERNAL` | V0 | No current observed five-minute child golden-path record | Private/safe observed session meets section 12 |
| `MA-TYPE-001` | P1 | `CONFIRMED_OPEN` | V1 | No explicit project font, default-font Theme, deterministic fallback chain, font licence row, or live-glyph coverage authority exists | Select and license an explicit authority; prove all live code points, exact APK delivery, and device/child/owner acceptance |
| `MA-TYPE-003` | P1 | `CONFIRMED_OPEN` | V1 | Child-action/state and adjacent text includes 15–24 px uses with no enforced role floor or reading-dependency exception contract | Enforce the 28 px child floor, bounded 22 px adult-caption exception, picture/voice redundancy, and exact-device/child evidence |
| `MA-TYPE-004` | P1 | `CONFIRMED_OPEN` | V1 | Critical UI semantics use Unicode/emoji without packaged coverage classification or controlled authored replacements | Classify all live code points and prove or replace every critical semantic glyph with device/child/owner evidence |
| `MA-TYPE-006` | P1 | `IN_PROGRESS` | V1 | Forty-five `Label3D` constructors across thirteen production files retain child-visible typography in the rejected spatial medium | Convert each semantic family to Canvas ownership, reach zero without fallback, and preserve focused/full/device behavior evidence |
| `MA-TYPE-007` | P1 | `BLOCKED_EXTERNAL` | V0/V1 gap | No typography-specific exact-APK M11/older-phone, adult-caption, child-path, or owner acceptance matrix exists | Complete the commit/APK/font-hash-bound device and human matrix in `DL-TYPE-12` |
| `MA-CI-004` | P1 | `CONFIRMED_OPEN` | V1 | The Day One wing and start-menu routing — the fresh-save entry arc — have eight dedicated probes and zero of them run in either trusted roster at `9a1754c1`, so a regression on the New Game path ships ungated | Classify and promote the deterministic Day One/start-menu probes into both rosters; a deliberately injected routing break must turn the gate red |
| `MA-CI-005` | P1 | `CONFIRMED_OPEN` | V1 | The central passive probe's progress snapshot reads only pearls, trophies, stickers, and medals; opera stars, combat, castle interaction, companion, and Day One reward surfaces are invisible to the zero-input negative test, and per-probe idle checks are opt-in | Extend the snapshot to every save-backed reward surface with a fail-closed mutation test per section 10 acceptance |
| `MA-RELEASE-001` | P1 | `FIXED_PENDING_VERIFICATION` | V3 exact local/remote/build plus V4 current source/capture; external open | Historical evidence remains preserved. Product source `51d0abc0` passes exact local CI in 1,404.5 seconds/all 64 and run-14 20/20 local Mobile/Speedy evidence. Integrated `441adf35` passes exact local/topic/dev machine gates and Android `31763879294` publishes its matching APK. Both remote Sky subprocesses still fail requested-Mobile renderer identity after 20 PASS rows and upload PNGs only | Require requested-Mobile remote Sky proof, target-device matrix, child, owner, authoritative visual, exact-voice/human-listening, strict-2D, clean warning/capture triage, and clean re-audit gates |

#### 5.1.1 Subordinate workstream — interactive/background pixel ownership

`MA-VIS-007` is the named child workstream of the game-wide live-evidence gap
`MA-VIS-006`. It owns the repeated failure cycle in which an interactive
foreground card is accepted while a baked, blurred, partial, or silhouette
copy remains in its background, or an automated background-heal recipe leaves
a visible smear that later animation frames uncover.

The workstream is fail-closed. A repair is not complete when a node disappears,
when the foreground card differs numerically from the background, or when an
unmerged topic branch contains the change. Closure requires all of the
following at one exact candidate:

1. enumerate every runtime background/interactive-card pairing and bind the
   inspected sources, generators, manifests, and visual states to the audit;
2. inspect the complete authored-frame sequence, including the largest exposed
   footprint rather than frame zero alone;
3. preserve protected and approved originals, then restore only the confirmed
   background gap as a full clean plate before slicing runtime tiles;
4. record source, prompt/method, hashes, normalization, licensing, and explicit
   proof that no guide or foreground-card pixel became delivery background;
5. make generators, manifests, audits, and runtime probes reject both duplicate
   pixels and blurred/interpolated placeholder holes;
6. capture dirty and clean live Mobile frames under exact Godot 4.7.2-stable,
   retain human review as distinct from machine PASS, and pass focused plus
   surrounding tests; and
7. merge the green topic into `dev` and verify the exact `dev` head before any
   release claim. A topic-only or stale-branch result is explicitly incomplete.

### 5.2 P2/P3 and owner-decision indexed items

| ID | Severity | Lifecycle | Verification | Indexed issue / decision |
|---|---|---|---|---|
| `MA-VIS-004` | P2 | `REPORTED_UNCONFIRMED` | V1; `COVERAGE_GAP` | Current source-average figure/ground values are Fairy 0.039 vs 0.040 and Lagoon about 0.004, but the metric does not measure the rendered local state and cannot confirm an art defect. Closure requires true state-local Canvas/HUD/viewport/device evidence, not recoloring approved art to satisfy the average |
| `MA-ASSET-001` | P2 | `CONFIRMED_OPEN` | V1 | Current orphan PNG reports: Castle 9/15 at 2.1 MB, Galaxy 32/32 at 11.7 MB, Opera 453/548 at 166.5 MB, Lagoon 48/90 at 41.9 MB |
| `MA-ASSET-004` | P2 | `CONFIRMED_OPEN` | V1 | Lagoon has 10/41 NPOT textures, about 11.6 MB uncompressed residency cost |
| `MA-CI-002` | P2 | `VERIFIED_FIXED` | V3 current local parity and exact-head remote execution | Current blocking-loop parity is 64 local names versus 63 remote names, with display-only `probe_human_art_audit` the intended difference; default and stress checks are green. Exact CHG-023 maintenance head `51887315` executes all 64 locally in 1,435.2 seconds under official Godot 4.7.1 and all 63 remote headings in run `31710377034`; the trusted loop takes 18m02s. Historical red run `31678156887` remains a genuine probe-readiness sample, not a parity regression. Runner warnings, legacy resource diagnostics, and non-authoritative Sky output do not undo the verified roster/parity contract |
| `MA-CI-003` | P2 | `CONFIRMED_OPEN` | V1 | All 106 probe scripts still need exactly one trusted/runtime-visual/advisory/diagnostic/obsolete/quarantined classification |
| `MA-ROSHAN-003` | P2 | `DEFERRED_WITH_REASON` | V1/V3 reported | Atlas repacking is an optimization; current owned-pixel windows and engine sampling probes are green |
| `MA-ROSHAN-004` | P2 | `DISMISSED_NOT_A_DEFECT` | V1 | Universal 2D costume layers are optional future design, not a missing required feature |
| `MA-PLAY-002` | P2 | `OWNER_DECISION_REQUIRED` | V1 | Standalone fire-arena reward/flag/medal role needs a truthful home or retirement |
| `MA-COMBAT-001` | P2 | `FIXED_PENDING_VERIFICATION` | V3 reported | Phone-only wave count, slash-band scale, and tutorial discoverability remain for device review |
| `MA-OPERA-003` | P2 | `CONFIRMED_OPEN` | V1/V4 partial | The grouped old pipe/echo/Nursery fallback claim is partially repaired by current authored pipe, echo, bottle, pat, and blanket behavior, but its unresolved subclaims have not yet been split and re-audited against accepted captures |
| `MA-OPERA-005` | P2 | `FIXED_PENDING_VERIFICATION` | V3 partial | The old Ballerina art/mechanic is superseded by the accepted 1024×1024 4×4 mermaid atlas and dedicated three-act full-stage recital; focused, last-full-local, and exact-head remote gates are green. Closure still requires accepted two-aspect capture, M11/child play, and owner identity/style acceptance; the remote diagnostic captures do not fill that evidence |
| `MA-OPERA-006` | P2 | `CONFIRMED_OPEN` | V1/V3 partial | Nursery, Farmer, and Racer received material art-fiction repairs, but the grouped historical claim must be split and re-audited; remaining protected-voice mismatches stay open rather than being inferred fixed |
| `MA-OPERA-007` | P2 | `OWNER_DECISION_REQUIRED` | V1 | Farmer/Doctor above-water setting differs from the other Opera backdrops |
| `MA-AUDIO-001` | P2 | `FIXED_PENDING_VERIFICATION` | V3 partial | Forty-two unique deterministic area cues have complete score/render hashes, 48 kHz stereo OGG delivery, loop/import metadata, loudness/peak/seam measurements, routing ownership, and focused audio/full-branch evidence. Topic/dev runs `31760207048`/`31762132976` at exact `441adf35` complete music 42/42 in 3m18s/3m56s; earlier e6, `7391c53c`, and branch runs are historical corroboration. Human style/two-wrap, voice-over intelligibility/ducking, mono fold-down, music-off transition, and Lenovo Tab M11 start/loop/performance gates remain open |
| `MA-CHANGE-001` | P2 | `VERIFIED_FIXED` | V2/V3 process evidence | Thirty-one stable records, `CHG-001` through `CHG-031`, cover 79 unique catalog-owned commit references. Manual/non-emitting CHG-031 owns exact 19-path source `51d0abc0`, including `scripts/probe_northern.gd`, at +3,318/-3,517. Only CHG-020/021/022/024 emit guarded stdout scripts; the other 27 refuse automation. Twenty-five planner tests, exact ledger/catalog parity, non-mutation replay, Git-history checks, GAME2D no-regression, and adversarial approval are green; future drift reopens the finding. |
| `MA-CODE-001` | P2 | `CONFIRMED_OPEN` | V1 | `main.gd` is 8,734 lines at current source `51d0abc0` against the extraction-only <2,500 target; historical `09e5e356` was 8,647 |
| `MA-CODE-002` | P2 | `CONFIRMED_OPEN` | V1 | String state, duplicated input, save frequency, material churn, and remaining 3D glue are structural risks; the 2026-08-26 round decomposes bounded sub-findings out of this group |
| `MA-CODE-003` | P2 | `CONFIRMED_OPEN` | V1 | Eight verbatim clone families (pointer glyphs, action-press reads, material factories, AABB kits, avatar spawns, start/end scaffolds, stage input maps, act teardown lists) violate the one-implementation rule `DL-CODE-05` |
| `MA-CODE-004` | P2 | `CONFIRMED_OPEN` | V1 | 409 distinct raw string keys own cross-system state in `g`, up from 380 thirteen days earlier; a typo fails silently (`DL-CODE-04`) |
| `MA-TYPE-002` | P2 | `CONFIRMED_OPEN` | V1 | Historical `0ddbe656` lacked role-owned typography and complete picture-button state. The current candidate adds eight role tokens and complete picture-button styling, but bypass clusters and exhaustive migration/capture evidence remain open. |
| `MA-TYPE-005` | P2 | `CONFIRMED_OPEN` | V1 | Historical `0ddbe656` lacked translation keys, role-owned wrapping, and longest-string/130%-expansion evidence. The current candidate adds focused exact-English fit checks only; closure still requires stable keys/placeholders and both expansion/aspect matrices without critical truncation, overlap, or target shrink. |
| `MA-CODE-005` | P3 | `CONFIRMED_OPEN` | V1 | Dead but fully wired loss-message code (`_fail_line`, unused `_end_game` lose branch) sits adjacent to the no-fail invariant (`DL-CODE-09`) |
| `MA-PERF-002` | P2 | `CONFIRMED_OPEN` | V1 | `_sparkle_burst` allocates a node, mesh, and material per call from 141 sites with no tier gate, on a permanent wayfinder cadence (`DL-CODE-07`) |
| `MA-PERF-003` | P2 | `CONFIRMED_OPEN` | V1 | The newest child-facing surfaces (Canvas Melody, Day One director, side-scroll stage, remaining spatial Galaxy/companion layers) carry zero quality-tier awareness (`DL-CODE-08`) |
| `MA-SAVE-001` | P2 | `CONFIRMED_OPEN` | V1 | Child-visible castle interaction progress lives only in unpersisted `m.g` scratch and resets on app kill (`DL-CODE-03`) |
| `MA-AUDIO-002` | P2 | `CONFIRMED_OPEN` | V1 | The mic capture player targets a "Mic" bus absent from `default_bus_layout.tres`, depending on a runtime bus rename to avoid audible self-capture |
| `MA-TOUCH-002` | P2 | `CONFIRMED_OPEN` | V1 | The side-scroll swim branch reads the emulated mouse without the reserved-zone guard, so a held UI medallion steers Roshan |
| `MA-CI-006` | P2 | `CONFIRMED_OPEN` | V1 | Promotion accepts any green probe run for dev's SHA rather than the latest push run, and nothing pins the executed roster against the expected one |
| `MA-CI-007` | P2 | `CONFIRMED_OPEN` | V1 | 38 probes carry private frame-wait helpers and duplicated boot scaffolding; wall-clock waits mix with scaled engine time, the flake class that already produced one red release-gate run |

### 5.3 Resolved indexed items retained for anti-regression history

| ID | Severity | Lifecycle | Verification | Indexed issue | Closure evidence |
|---|---|---|---|---|---|
| `MA-DOC-001` | P1 | `VERIFIED_FIXED` | V1 | Current authority documents prescribed 2.5D/Sprite3D/real-3D/model work | `9289dd81`; `AGENTS.md`, `CLAUDE.md`, design masters, ledger, and Roshan authority reconciled to game-wide true 2D while binding security/save/cinematic/release rules remain intact |
| `MA-DOC-004` | P1 | `VERIFIED_FIXED` | V1 | The master-audit draft was hidden by broad `/audit/` ignore behavior and both proposed documents were untracked/unindexed | `806ffb95` tracks both documents through the narrow audit-source exception; `9289dd81` indexes and ledgers them; `96317f8b` separately ignores only local `/tmp/*` review artifacts |
| `MA-2D-003` | P2 | `VERIFIED_FIXED` | V2/V3 | Opera and medal conversions left stale production-file entries in the shrink-only manifest | `344d8d5c`; guarded manifest refresh, exact full CI exit 0, GAME2D 73-unit/14-stress contracts, and `NO_REGRESSION` at 513/70 |
| `MA-DOLLS-001` | P1 | `VERIFIED_FIXED` | V3/V4 focused | Faron's catcher used legacy spatial presentation and did not fully prove real touch, passive safety, save, replay, and teardown on its replacement | `5df75427`; one bounded Canvas layer, approved nursery tiles, real press/drag/release routing, safe misses, passive no-save/no-award, medal/save/replay, weakref teardown, and 1280×720 Mobile capture coverage |
| `MA-SEEK-001` | P1 | `VERIFIED_FIXED` | V3/V4 focused | Seek used a vinyl pair card, low-quality `k_bush2` draft, static-transform acting, and four meadow GLBs below the surrounding game's quality/medium bar | `8fa90111` plus `27bda85d`; provenance-locked animated Evie/Lamb-a' kit, fourteen-node Canvas meadow, frame-swapped actors, four large routed targets, no-fail/passive/save/replay/teardown coverage, reviewed 16:9/16:10/20:9/4:3 captures, and four byte-verified GLBs retired; exact Evie objective speech remains separately open as `MA-ACCESS-003` |
| `MA-VIS-005` | P2 | `VERIFIED_FIXED` | V2/V3 focused | The visual tool could credit aggregate/bounding-box occlusion without proving each live target and painted overlap | `3b7a7e66` plus `fea916a8`; unique target ownership, effective descendant Canvas order, decoded-alpha overlap, transparent-hole/low-alpha rejection, source closure, and fail-closed fresh-runtime behavior; missing live product evidence remains `MA-VIS-006`, not a false PASS |
| `MA-ASSET-003` | P1 | `VERIFIED_FIXED` | V1/V3 reported | Four current Sky Lagoon playground assets lacked complete license-ledger coverage | `a1be9a1e`; all 41 current Lagoon runtime assets licensed and roster/audit gates updated |
| `MA-ASSET-005` | P2 | `DISMISSED_NOT_A_DEFECT` | V1/V3 diagnostic | Local runs warned that `sponge_tubes.glb` and `starfish.glb` referenced invalid texture UIDs | Source GLBs and tracked sidecars validate, while an isolated fresh project import is warning-free; the warnings came from four stale ignored `.godot/imported` cache artifacts. The resources remain separate 3D medium debt under `MA-2D-002`, not a source-UID defect. |
| `MA-ROSHAN-002` | P1 | `VERIFIED_FIXED` | V1/V3 reported | Two playground poses were genuinely clipped and two intact poses retained detached edge debris | `a1be9a1e`; exact replacements, pixel/import/runtime/Mobile-render checks, and clipping-audit tests |
| `MA-OPERA-008` | P1 | `VERIFIED_FIXED` | V3 partial: bounded cue/finale defect | The Canvas Racer finale requested a ride-selection recording for a circle gesture and could leave stale caption/fallback output | `e4528b27`; exact `op_racer_lap_two` pooled recording, hidden caption, quiet fallback, parser/lint, and focused Canvas Opera2D/voice/Opera probes. This closure remains bounded; the later ordinary-headless lifecycle repair is tracked independently as `MA-OPERA-010` `FIXED_PENDING_VERIFICATION` |

The old claim that Lagoon exceeded its 24 MB simultaneous zone budget is
`DISMISSED_NOT_A_DEFECT`: corrected residency measurement reports about
22.4 MB. `MA-ASSET-004` preserves the distinct NPOT cost without changing
approved pixels merely to clear a metric.

---

## 6. Supporting repair evidence — not canonical finding records

`EV-*` is a stable evidence-record identifier. Each row links to an indexed
`MA-*` item or controlling `DL-*` rule; it does not silently create or close a
canonical finding. Lifecycle remains in section 5, and the full-record contract
remains in section 10.

### 6.1 Current true-2D program evidence

| Evidence ID | Related item(s) | Evidence scope | Checkpoint and result |
|---|---|---|---|
| `EV-2D-001` | `MA-2D-002` | Roshan model/pipeline retirement sub-slice | `3be5b44b`; narrow clean/stress/unit gate |
| `EV-2D-002` | `MA-2D-002` | Picture-game feedback converted to 2D stage nodes | `21ae8391`; bounded feedback, teardown, re-entry, and passive coverage in `probe_mg2d` |
| `EV-2D-003` | `MA-2D-002` | Wardrobe try-on converted to a 2D overlay | `be3fb490`; overlay identity/bounds/teardown coverage in `probe_ui_system` |
| `EV-2D-004` | `MA-2D-002` | Medal award feedback converted to a 2D overlay | `fe3616b4`; rapid replacement, bounded nodes, save/rank/teardown coverage in `probe_rank` |
| `EV-2D-005` | `MA-2D-002` | Game-wide shrinking-debt gate contract | `e0877b65`, `d6240be8`, `b3ad3842`; 73 unit tests and 14 stress controls; gate verification is not game satisfaction |
| `EV-2D-006` | `MA-2D-002` | Archive non-runtime model sources | `86d0c243`; exact archive preservation and guarded manifest shrink |
| `EV-2D-007` | `MA-2D-002` | Archive unreachable active/export models | `0b75c60c`; dependency proof, import, focused surrounding probes, guarded shrink |
| `EV-PLAY-001` | `MA-PLAY-001` | Strengthen companion no-fail coverage without claiming a 2D conversion | `f8efeb0a`; patient waiting, no removal/blocking, legacy-save preservation, passive/teardown/re-entry coverage |
| `EV-2D-008` | `MA-2D-002` | Opera racer finale retained in Canvas | `82124b3a`; external kart launch/control/teardown removed; passive/identity/bounds/input/reward/weakref/re-entry probe coverage |
| `EV-2D-009` | `MA-2D-002` | Retire medal legacy spatial scoreboard | `8ed978be`; production 3D-file debt 71→70; `probe_rank` adds legacy cleanup, Canvas tally, bounded-node, save, and idempotence assertions, followed by the `344d8d5c` full checkpoint |
| `EV-2D-010` | `MA-2D-002`, `MA-2D-003` | Record Opera/medal shrink and remove stale manifest entries | `344d8d5c`; exact full CI exit 0, 61 trusted probes, GAME2D 513/70 `NO_REGRESSION` |
| `EV-OPERA-001` | `MA-OPERA-008`, `MA-RELEASE-001` | Use exact racer circle recording and prevent stale caption/yay fallback | `e4528b27`; parser/lint plus exact Godot 4.7.1 Opera2D, voice, and Opera probes all green; full CI at that checkpoint was not run |
| `EV-OPERA-002` | `MA-OPERA-001`, `003`, `006` | Replace wrong semantic props and generic object motion with causal job actions | `2119ab39` plus current integration; 39 governed files reproduce byte-for-byte, including four generated missing-tool roles and 35 reviewed derived/source outputs; owner visual/device review remains open |
| `EV-OPERA-003` | `MA-OPERA-005` | Replace the old Ballerina art/phase premise with the three-act recital and accepted atlas | `3dd98fbe`, `7d9e6c5f`, `0447188f`, and current integration; accepted runtime atlas SHA-256 `c829784d…003995`, held-pose keys, one-shot curtain call, 5/10-second assists, passive rejection, and exact focused Opera/Ballerina probes green |
| `EV-OPERA-004` | `MA-OPERA-009` | Rebuild Boxer as a full-stage two-glove specialist | `8d67c2bd` plus current integration; five exact phases, independent touch ownership, sequential one-finger completion, no-loss contact, passive rejection, teardown/re-entry, and stable save-bit coverage in focused probes |
| `EV-OPERA-005` | `MA-OPERA-006` | Make Candymaker's syrup pour phone-playable and semantically coherent | `39746756` plus current integration; complete shell mold, generous pitcher hit target, measured left-spout transform shared by drawing/stream/hit logic, monotonic fill, and focused quality/probe coverage |
| `EV-2D-011` | `MA-2D-002`, `MA-DOLLS-001` | Convert Faron's Dolls catcher to one bounded true-Canvas activity | `5df75427`; approved nursery world tiles, real one-finger input, passive/wrong/safe-landing behavior, progress/save/medal/replay, control ownership, teardown/weakrefs, and Mobile capture checks |
| `EV-ASSET-004` | `MA-SEEK-001`, `DL-ASSET-01`, `DL-ASSET-02` | Fill the proved animated Evie/Lamb-a' gap without modifying protected references | `8fa90111`; source atlases, prompts, manifest, exact hashes, deterministic alpha/despill builder, runtime animation atlases/portrait, licence entries, and six builder tests |
| `EV-2D-012` | `MA-2D-002`, `MA-SEEK-001`, `MA-ACCESS-003` | Rebuild Seek as the animated Canvas meadow and retire its spatial/vinyl presentation | `27bda85d`; four real routed targets, animated hide/peek/reveal/celebrate states, persistent non-reading cues, kind wrong input, passive no-award, save/replay/re-entry/teardown, reviewed multi-aspect captures, and four exact archived GLBs removed; exact Evie tap-tree recording remains open |
| `EV-2D-013` | `MA-2D-002`, `MA-2D-003` | Record the Dolls/Seek/visual-probe shrink without relaxing the baseline | `a3d3bce1`; default exact and regression modes green at 509 models/68 production files/77 probe files; strict remains `UNSATISFIED` |
| `EV-2D-014` | `MA-2D-002`, `MA-OPERA-008`, `MA-OPERA-010` | Preserve the display/forced-2D Canvas Racer during the earlier Opera reconciliation | Current Canvas branch has three phases, exact `op_racer_lap_two` speech, passive rejection, completion, teardown, and re-entry coverage. Exact `f3b0de07` source review corrects the broader old claim: ordinary headless still has a legacy lobby/racer route that may attach `scripts/kart.gd`; it remains open debt rather than being hidden by the forced-2D probes |

The archive branch name retains “roshan” for history but is the preservation
authority only for resources already archived there. It is never an active
source, fallback, rollback target, or claim that reachable 3D debt is retired.

### 6.2 Other child-safety and quality evidence

| Evidence ID | Related item/rule | Evidence scope | Checkpoint and result |
|---|---|---|---|
| `EV-PLAY-002` | `MA-PLAY-001` | Companion boo-boos wait without removal, blocking, or lost legacy progress | `0522d1fa`; stuffie/load coverage |
| `EV-TOUCH-001` | `MA-TOUCH-001` | Snowman coal touch controls meet `StorybookUI.MIN_TOUCH` | `82f9828c`; `probe_mg2d` |
| `EV-CI-001` | `MA-CI-002` | Trusted local/remote probe parity and Opera-pipe coverage | `7e6d699d`; clean plus drift mutations |
| `EV-CI-002` | `MA-RELEASE-001`, `MA-2D-002`, `MA-ASSET-005` | Preserve the last exact local full gate without conflating regression control with strict satisfaction or stale local cache | Runtime commit `a3d3bce1`; exact Godot 4.7.1-stable, fresh import, all static gates, GAME2D 509/68 `NO_REGRESSION`, and all 61 then-trusted probes green; exit 0 after 1434.3 seconds. Later isolated-import evidence classifies its UID warnings as stale ignored cache, while the GLBs remain medium debt. |
| `EV-CI-003` | `MA-CI-002`, `MA-RELEASE-001` | Integrate new Opera/art/music gates into both blocking environments | Integration commit `ad36ee9f`; local loop 63, remote headless loop 62, display-only human-art probe is the sole intended difference, and default/stress parity checks are green. The local full gate exits zero after 826.4 seconds with all 63. First exact-head execution `31455723446` at `57bc08d1` exposed the cross-platform Opera PNG compression defect later repaired by `EV-CI-004`; final replacement evidence is `EV-CI-005`. |
| `EV-CI-004` | `MA-RELEASE-001`, `MA-CHANGE-001` | Diagnose and constrain the remote-only Opera generated-art false rejection | Repair commit `fe10ffd2`; GitHub run `31456633826` proves `CHECK OK: 39` on Linux. Focused mutations permit only recompression of an identical PNG scanline stream; CRC-checked structure, all other chunks, mode, dimensions, pixels, semantic text, and checked-in delivery-byte provenance remain strict. Eight focused gate tests plus 14 rollback tests are green. |
| `EV-CI-005` | `MA-RELEASE-001`, `MA-CI-002`, `MA-AUDIO-001` | Keep deterministic music verification blocking without misrepresenting its render environment | Repair commit `dacef140`; run `31457593351` succeeds on the exact SHA with two required jobs. The pinned `windows-2025` job uses `actions/setup-python` commit `5fda3b95`, Python 3.13.14, NumPy 2.5.1, SciPy 1.18.0, and the existing SHA-256-pinned FFmpeg 8.1.2 installer, exactly matching the manifest's recorded render dependencies, and reports all 42 deliveries green. The Ubuntu job independently passes Opera 39/39, GAME2D 509/68/77 `NO_REGRESSION`/`UNSATISFIED`, all 62 headless trusted probes and boot; five diagnostic capture/upload pairs also complete successfully without being promoted to blocking or accepted visual evidence. Parity now fails with `PRB007` if either local or remote music verifier disappears. |
| `EV-CI-006` | `MA-RELEASE-001`, `MA-2D-002`, `MA-OPERA-010` | Reconcile the audit history with the newer development runtime without overstating closure | Merge `f3b0de07` (parents `ea6185fd` and `5f58ef0a`); exact Godot 4.7.1 local `scripts/ci.sh` exits 0 after 1437.1 seconds with 64 trusted probes, GAME2D 74 unit tests plus 14 falsification controls, 509 models/509 active, 157 tracked plus 352 generated sidecars, 68 production/77 probe/one scene/one config, and all then-current static/Opera provenance gates green. It was the committed full-local checkpoint for that reconciliation; later commit `e2c25878` supplies the 66/74 predecessor full-local result and current `09e5e356` retains that inventory while adding distribution evidence. `EV-CI-008` supplies exact-head remote evidence for `af4189a9` only; APK/device/child/owner/listening/strict-2D/authoritative visual evidence remains open. |
| `EV-CI-007` | `MA-RELEASE-001`, `MA-CI-002`, `MA-AUDIO-001`, `MA-CHANGE-001` | Diagnose and narrowly repair the current cross-platform Opera provenance failure without weakening binary integrity | Exact-head run `31648427712` at `bbc817ef`: the pinned Windows area-music job succeeds 42/42; Ubuntu fails only in the static Opera-art gate because generated provenance held the raw CRLF checkout hash of declared text input `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/GENERATION.json` while Linux read LF, so import/analyzer/63 probes never run. Repair `af4189a9` canonicalizes LF only for that declared text source, keeps every binary hash byte-exact, refreshes provenance, and passes 10 focused tests plus Windows and LF-clean Opera checks at 42/42. The failed run remains failed; `EV-CI-008` records its successful replacement. Full local CI at `af4189a9` remains unclaimed. |
| `EV-CI-008` | `MA-RELEASE-001`, `MA-CI-002`, `MA-AUDIO-001` | Verify the newline-stable repair at the exact remote head without promoting diagnostics into acceptance | GitHub run `31649113587` succeeds at exact `af4189a9`. The Ubuntu probes job completes in 35m27s: static gates, import, full analyzer, all current 63 remote trusted probes, boot, Dust/Opera advisory balance, and the Opera manifest are green. Five diagnostic capture/upload workflow steps complete and upload artifacts; the pinned Windows job completes in 3m55s with music 42/42. This closes exact-head remote CI only; the captures remain diagnostic, and APK/device/child/owner/listening/strict-2D/authoritative visual/full-local-at-`af4189a9` evidence remains open. |
| `EV-CI-009` | `MA-RELEASE-001`, `MA-CI-002`, `MA-AUDIO-001`, `MA-OPERA-010`, `MA-OPERA-011` | Verify the integrated Opera retirement/lifecycle predecessor head without promoting diagnostics into acceptance | GitHub run `31661887863` succeeds at exact SHA `e0677ae4c4f5e48258ff57c38f82e25f2dc3d9d0`. Ubuntu succeeds in 33m8s after checkout/checksum, exact Godot, static gates, import, full analyzer, exactly 63 trusted probe headings, boot, Dust/Opera advisories, Opera manifest, and five diagnostic capture/upload pairs. `OPERA`, `OPERA2D`, Nursery, and Detective are green; `OPERA_DIEGETIC_PATHS` reports 2247 checks/13 careers/64 stations/53 phases/48 spurs. Remote GAME2D is exact 509/66/74 `NO_REGRESSION`/`UNSATISFIED`. Windows succeeds in 6m52s with terminal line `MUSIC\|check 42/42\|picture_xmas`. This closes exact-head machine verification for that predecessor only; the capture pairs are non-authoritative. Later distribution and failed-readiness evidence are recorded in `EV-CI-010`/`011`; successful successor remote evidence is `EV-CI-012`, while APK/device/child/owner/human-listening/strict-2D/authoritative visual gates remain open. |
| `EV-CI-010` | `MA-RELEASE-001`, `MA-CI-002`, `MA-OPERA-010`, `MA-OPERA-011`, `MA-OPERA-012` | Verify the current Castle-room distribution locally without promoting diagnostic renders into acceptance | Commit `09e5e35665fd8d1bd782693e10fc0198f756d2c8` completes exact official Godot 4.7.1 `scripts/ci.sh` in 1463.4 seconds with all 64 trusted local probes green. Focused probes cover all 13 exact room mappings, Movie Lounge Racer, no all-career lobby/backdoor, exact-room return, sparse save bits/rewards, pause/layer ownership, teardown and re-entry. Twenty-two 1280×720 renders (9 routes + 13 careers) are diagnostic; route cards obscure the lower body/tail. Later failed-run/readiness evidence is `EV-CI-011`; its successful exact-head successor is `EV-CI-012`. APK, device, child, owner, exact voice, listening, strict-2D, and accepted visual evidence remain open. |
| `EV-CI-011` | `MA-RELEASE-001`, `MA-CI-002`, `MA-OPERA-012` | Preserve the failed distribution-head remote result and repair probe readiness without mislabeling runtime behavior | GitHub run `31678156887` at `3fc151c8b3b6c054d0f6e6ab89f84a9f464f3f20` is genuinely red: Ubuntu `probe_opera` reports only the Detective and Nursery stable-Canvas compound checks failed after a fixed four-frame sample of the 0.25-second reveal. Raw launches, passive safety, save/reward, exact-room return, all surrounding Opera probes, every other executed gate/probe, and Windows pass; no script/resource/runtime error occurs. Probe-only commit `ff068db002202839f920a6f9fb78c942788a3034` preserves runtime `09e5e356`, replaces the frame guess with a bounded fail-closed wait for the exact Opera instance/reveal/stage/layer state, and completes exact official Godot full local CI in 1379.3 seconds with all 64 trusted probes green. `EV-CI-012` records the successful exact-head replacement without rewriting this failed run. |
| `EV-CI-012` | `MA-RELEASE-001`, `MA-CI-002`, `MA-AUDIO-001`, `MA-OPERA-010`, `MA-OPERA-011`, `MA-OPERA-012`, `MA-CHANGE-001` | Verify the synchronized distribution authority head remotely while preserving diagnostic limits | GitHub run `31686380560` succeeds at exact `9befc0f838f40eead2f42088a91206257fe217a8`. Ubuntu `probes` runs 09:24:08–09:57:48 UTC (33m40s): static gates, import, full analyzer, exactly 63 remote trusted probe headings, boot, Dust/Opera advisories, and Opera manifest are green. Windows runs 09:24:08–09:27:55 UTC (3m47s) and ends `MUSIC\|check 42/42\|picture_xmas`. All five capture/upload pairs completed at the workflow level and uploaded diagnostic artifacts; they are not capture gates or visual passes. Raw Sky Lagoon `LAGOONSHOT` output has 21 `OK`, 44 `FAIL`, and `DONE` (66 diagnostic lines), so the Sky Lagoon diagnostic internally fails. The run is not warning-clean: existing missing-Vulkan-surface/OpenGL fallback and ObjectDB/resource/texture-leak diagnostics remain. No matching APK, device, child, owner, exact-voice, listening, strict-2D satisfaction, or accepted-visual evidence is claimed. |
| `EV-CI-013` | `MA-RELEASE-001`, `MA-CI-002`, `MA-AUDIO-001`, `MA-OPERA-012` | Verify the exact integrated dev/audit head and publish its matching dev APK without promoting diagnostics into acceptance | Probe Suite run `31693492735` succeeds at exact `18b6150c01e1587100dca97c85ebad03f369825a`: the probes job completes in 29m41s with exactly 63 remote trusted headings and music completes 42/42. Raw Sky Lagoon output remains diagnostic and internally reports 21 `OK`, 44 `FAIL`, and `DONE`; the artifact contains 20 PNGs, none accepted. Android dev run `31695675866` succeeds at the same exact head and publishes a 596,041,412-byte APK with SHA-256 `fb4979473441d416f7b07914b1396f5f883935d4c08bf077baed3dfb91b78941`. Device, child, owner, exact-voice, human-listening, strict-2D, and accepted-visual gates remain open. |
| `EV-DOC-001` | `MA-DOC-002`, `MA-DOC-005` | Seal and harden an exhaustive document-authority chain without claiming source-head closure | First source `5ed0c75460c9afd5ab574ff2c4a907c1075964f0`, parent `18b6150c01e1587100dca97c85ebad03f369825a`, establishes the exact 316-path inventory, 316 unique ledger rows, 36 linked complete records, validator/tests, and blocking local/remote CI wiring; exact official Godot 4.7.1 `scripts/ci.sh` is green there in 1,359.8 seconds/all 64. Contiguous hardening source `7eb945957776ab3458a9de71c8be9937e2354720`, exact parent `5ed0c754`, adds multiline stale-claim controls and synchronizes evidence; 36 focused tests and six mutation controls are green. The first source touches high-risk `.github/workflows/probes.yml`, limited to three read-only Python commands under existing `contents: read`; the second source changes no workflow path. At that source checkpoint no direct full-local or remote result existed for `7eb94595`, so both findings remained `FIXED_PENDING_VERIFICATION`; `EV-DOC-002` records their later terminal transition. |
| `EV-DOC-002` | `MA-DOC-002`, `MA-DOC-005` | Verify the unchanged document-authority chain locally and remotely at its exact maintenance head | CHG-023 maintenance commit `51887315bd537db2d16bdafcac1bbfa808352351`, exact parent `7eb945957776ab3458a9de71c8be9937e2354720`, changes documentation/planner metadata without changing the CHG-029 sources, validator, workflow, runtime, save, protected assets, audio, or gameplay. Exact official Godot 4.7.1 `scripts/ci.sh` exits zero after 1,435.2 seconds with all 64 trusted local probes. Probe Suite run `31710377034` succeeds at the same SHA: Ubuntu runs 14:28:33–15:09:45 UTC (41m12s), its trusted loop takes 18m02s with exactly 63 headings, the document static gate reports 36 tests/six stress/316/316/36/36 ALL OK, and Windows completes in 4m08s with raw 42/42 ALL OK. Raw Sky Lagoon remains 21 OK/44 FAIL/one DONE and non-authoritative; runner warnings, legacy resource diagnostics, APK, device, child, owner, voice, listening, strict-2D, visual, and release gates remain separate. This evidence moves only `MA-DOC-002` and `MA-DOC-005` to `VERIFIED_FIXED`. |
| `EV-CI-014` | `MA-DOC-002`, `MA-DOC-005`, `MA-CI-002` | Preserve the earlier branch verification of the exact Sky diagnostic parent without transferring its capture result | Earlier branch Probe Suite run `31719143975` succeeds at exact `e6edf559af219edd4e5ce38cab0c5094483be5c6`: probes 33m18s with 63/63 unique headings; document authority 36 tests, six/six stress, 316/316 inventory/ledger and 34 active/36 retained records; Windows music 42/42 in 4m24s. Its 21-OK/44-FAIL/one-DONE Sky output is retained as predecessor history only. |
| `EV-CI-015` | `MA-DOC-002`, `MA-DOC-005`, `MA-CI-002`, `MA-RELEASE-001`, `MA-AUDIO-001`, `MA-OPERA-012` | Verify and package the latest integrated predecessor without transferring acceptance to current source | Dev Probe Suite run `31722047536` succeeds at exact `e6edf559af219edd4e5ce38cab0c5094483be5c6`: probes 34m25s with 63/63 unique headings; document authority 36 tests, six/six stress, 316/316 inventory/ledger and 34 active/36 retained records; Windows music 42/42 in 3m33s. Workflow-run Android `31724927769` uses raw checkout/package source exact e6 and publishes a 596,041,412-byte dev APK with SHA-256 `66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c`. No exact `7391c53c` APK, device, child, owner, voice, listening, strict-2D, or accepted-visual result is transferred. |
| `EV-CI-016` | `MA-DOC-002`, `MA-DOC-005`, `MA-CI-002`, `MA-RELEASE-001`, `MA-AUDIO-001`, `MA-OPERA-012`, `MA-VIS-002`, `MA-VIS-006` | Verify and package the integrated true-Canvas authority head without converting a nonblocking renderer failure into visual acceptance | Governance-only head `441adf35f7dbdeb67d36fbf1a2217b87d3040d47` preserves unchanged CHG-031 product source `51d0abc0`. Exact official-Godot local `scripts/ci.sh` exits 0 in 1,391.5 seconds with all 64 unique headings. Topic Probe run `31760207048` succeeds with probes 33m39s and music 3m18s; dev Probe run `31762132976` succeeds with probes 33m39s and music 3m56s. Both exact-head runs complete the 63/63 unique remote loop with zero hard failures, document controls 36 tests/six stress/316 inventory/316 ledger/34 active/36 records, and music 42/42. Both nonblocking Sky diagnostics request Mobile but lack `VK_KHR_surface`, fall back through llvmpipe to `gl_compatibility`, print 20 PASS rows plus summary `20/20/20/20` with failed 0/skipped 0, then emit `GLOBAL`/`RESULT` FAIL and exit 1; PNGs upload, but no remote JSON or Mobile-renderer PASS exists. Android run `31763879294` checks out/packages exact `441adf35`, version code 1414, branch/tag `dev`/`android-dev`, and publishes a 596,033,220-byte APK with SHA-256 `f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`; its 82-byte checksum sidecar has SHA-256 `43e892cfb6c9a3847e1a8760d5cad4dd8fb36719d63db0625ec8b2fa3ba8e651`. No device, child, owner, accepted-visual, listening, strict-2D, or release acceptance transfers. This authority synchronization is CHG-023 maintenance, not CHG-032. |
| `EV-CHANGE-001` | `MA-CHANGE-001` | Make the large audit program reviewable and reversions granular | `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md`, `tools/plan_audit_rollback.py`, and 25 planner tests; CHG-001–031 cover 79 unique catalog-owned commit references. Only CHG-020/021/022/024 emit guarded stdout scripts; the other 27 groups refuse automation. Manual CHG-031 owns exact 19-path source `51d0abc0`, including `scripts/probe_northern.gd`, at +3,318/-3,517. Planner/ledger agree, CLI execution leaves Git status byte-identical, and adversarial checks are green. |
| `EV-AUDIO-001` | `MA-AUDIO-001` | Compose, render, route, and deterministically verify every newly authored area cue | `0da07e24`, `27c2c95d`, and current integration; 42/42 scores and OGGs have unique hashes, loop/import metadata, measured codec/loudness/peak/seam evidence, routing probes, license entries, and exact build checks. Human listening, mono, voice mix, and M11 evidence remain open. |
| `EV-PLAY-003` | `MA-PLAY-001` | Visible, voiced Lagoon→Reef route and Pause fallback | `986010c0`; focused/re-entry/sibling probes |
| `EV-PLAY-004` | `MA-PLAY-001` | Exercise the default Hybrid Lagoon portal through the actual explicit interaction route | `e6e56f8b`; proves proximity alone does not enter, selects enabled `reef:lagoon`, activates it through the touch-interactable path, and keeps Classic/no-touch proximity behavior green |
| `EV-ROSHAN-001` | `MA-ROSHAN-002` | Playground/animal completion settles visible Roshan art | `711879ec`; Lagoon probes |
| `EV-CIN-001` | `DL-CIN-12` | Cinematic orientation/aspect/SAR/rotation blocking | `b50f2477`; focused cinematic unit suite |
| `EV-VIS-001` | `MA-VIS-006` | Visual audit preserves explicit unresolved-evidence states | `219fe593`; strict blocks review/manual/coverage gaps |
| `EV-VIS-002` | `MA-VIS-006` | Lagoon touch facts use real hit diameter | `6e04706d` |
| `EV-VIS-003` | `MA-VIS-002`, `MA-VIS-003` | Lagoon active-art/congruency evidence corrected | `09027504` |
| `EV-VIS-004` | `MA-VIS-005`, `MA-VIS-006` | Replace saved-fact/Sprite3D allowances with a fail-closed fresh-runtime Canvas evidence contract | `3b7a7e66`; one-use same-process challenge, immutable captures, clean Git/source/engine binding, live layers/targets/state adapters, decoded-alpha geometry, real touch reach, and adversarial unit/stress controls |
| `EV-VIS-005` | `MA-VIS-005`, `MA-VIS-006` | Bind active ignored and custom-root runtime sources into visual evidence closure | `fea916a8`; an ignored production helper cannot renew PASS, while review-only ignored output remains non-authoritative |
| `EV-VIS-006` | `MA-VIS-002`, `MA-VIS-006`, `MA-RELEASE-001` | Replace obsolete Sky capture assertions with a deterministic current-state diagnostic without accepting the product art | Source `7391c53cd6981a256bd8bfe40ccbb9f72fb723fe`, exact parent `e6edf559`; exactly two changed files. Exact official Godot 4.7.1 full local exits zero after 1,402.3 seconds/all 64. Local Mobile/Speedy 1280×720 output is 20/20 ordered PNGs, 20 PASS rows, and 1,078 assertions with isolated save/restoration evidence. Probe SHA-256 `f28413263c0bedeed421fae6e9de4626095f03b6010bade8380ad7fb5aa07db9`; GAME2D manifest SHA-256 `8c70b9aeaba5302322bdd44ca84d8a2b76fca053a091753e0e04676ee407fb00`. Review exposes tiny frog/otter and subtle-focus P1 risks plus animal/Roshan overlap, weak grounding, and seesaw-contact P2 defects. Exact-source run `31728755204` is overall green, but raw Sky output has 20 PASS rows followed by `GLOBAL\|FAIL\|rendering_method\|gl_compatibility`, `RESULT\|FAIL`, and exit 1 because the runner lacks `VK_KHR_surface`; continue-on-error masks the failure and only PNGs upload. No remote manifest, APK, device, child, owner, art acceptance, or `MA-VIS-002`/`006` closure is claimed. |
| `EV-VIS-007` | `MA-VIS-002`, `MA-VIS-006`, `MA-TOUCH-001`, `MA-PLAY-001`, `MA-RELEASE-001` | Convert Sky Lagoon's promenade to a true-Canvas owned stage and repair its bounded visual/input lifecycle | Source `51d0abc0d32855a8ba32932599fedd8f59b398b7`, parent `1b7d6bdaf89ebc7c9bdeae16fbde0e14079fd8a8`; exactly 19 paths including `scripts/probe_northern.gd`, +3,318/-3,517. The stage uses CanvasLayer/Node2D/Sprite2D/Camera2D, 6144×2048 master space, a 6×2 backdrop, differential layers/parallax, five animals, three actions, and real route/return/re-entry/touch cancellation. Exact source-byte official-Godot CI is green in 1,404.5 seconds/all 64. Run-14 is local Mobile/Speedy 20/20 with manifest SHA-256 `AEAC7C72E0A3BFF992713127261DD00ED69049947DFB6723AA66365F5712DE34` and visual-probe SHA-256 `B9EAF5E0738CFB61CCD3E34ACFEA420AEADAB4E3ADE80B40A2CFD1F227569C6C`; these bind the manifest/PNGs and probe script, while `source_revision` remains unknown. GAME2D is 509/65/70 `NO_REGRESSION` and `UNSATISFIED`. `EV-CI-016` adds exact integrated machine/APK evidence but records the current remote Sky renderer failure. No art/assets/workflow/save-schema changes or device/child/owner/accepted-visual result are claimed. |
| `EV-VIS-008` | `MA-VIS-006`, `MA-PLAY-001`, `MA-TOUCH-001`, `MA-2D-002` | Rebuild Grand Puff interaction and share its child-visible encounter grammar with Pepper and the bounded CombatTutorial presentation repair | `BOSS_ENCOUNTER_VISUAL_AUDIT_2026-09-05.md`; exact Godot 4.7.2 focused Grand Puff/Combat/CombatTutorial probes are green, including pause, passive/spam/held, geometry, checkpoint/re-entry and reward-idempotence controls. Tracked local packet `audit/boss_encounter_2026-09-05/manifest.json` binds 17 normalized source hashes and 13 unmodified Mobile PNGs across Dust 1280×720/1560×720 and tutorial root3 1280×720; all hashes recheck. The source remains an uncommitted candidate; durable remote commit, combined CI, residual 3D conversion, exact tutorial voice, device, child and owner gates remain open. No canonical lifecycle or baseline count changes. |
| `EV-ASSET-001` | `MA-ASSET-004` | Lagoon texture residency measured by simultaneous use | `76c30a66` |
| `EV-ASSET-002` | `MA-ASSET-003`, `MA-ROSHAN-002` | Four clipped/debris playground frames replaced and licensed | `a1be9a1e`; all 41 current Lagoon runtime assets licensed |
| `EV-VOICE-001` | `MA-ACCESS-001` | Duplicate objective speech prevented | `17813082` |
| `EV-VOICE-002` | `MA-ACCESS-001` | Speech stops across skip/advance/clear/teardown | `c86d3a7d` |
| `EV-VOICE-003` | `MA-ACCESS-001` | Opera phase re-prompts retain speaker/cue identity | `8b5ca161` |
| `EV-VOICE-004` | `MA-ACCESS-001` | Shadowed duplicate voice-generator keys rejected | `1c6e0c24` |
| `EV-VOICE-005` | `MA-ACCESS-001` | Brawl prompts bind to one Huluu cue | `e8485d54` |
| `EV-ASSET-003` | `DL-ASSET-04` | Castle delivery provenance is newline-stable | `df5b4cf7` |
| `EV-CASTLE-001` | `DL-VIS-10`, `DL-SAVE-01`, `DL-INT-01` | Apply the child's saved Castle logo to every matching purple shell banner without stealing room input | `9e75e8e3` plus current integration; two Craft Room and two Stuffie Playroom replacements, Craft badge, saved color/symbol, no overlay in unregistered rooms, and focused interaction coverage |
| `EV-AUTH-001` | `MA-DOC-001`, `MA-DOC-002` | Reconcile current authority to true 2D while preserving the then-incomplete-ledger state | `9289dd81`; operational/design authorities updated. At that historical checkpoint, exhaustive classification remained open; later sealed-source local evidence is `EV-DOC-001`. |
| `EV-HYGIENE-001` | `MA-DOC-004`, `MA-VIS-006` | Keep local captures/profiles/review builds out of production Git status | `96317f8b`; `/tmp/*` ignored while existing tracked fixtures remain tracked; ignored evidence never gains PASS authority |

These rows are bounded supporting evidence. None is inflated into a current-HEAD
full release pass or a complete record for a broader indexed item.

---

## 7. Superseded, dismissed, and deferred ideas

| Source/idea | Lifecycle | Current disposition |
|---|---|---|
| Real/modelled Roshan; v2/v3/v4 GLB/rig/skeleton fallback hierarchy | `SUPERSEDED` | Approved RGBA family on true 2D canvas is the only target |
| Meshy migration for Roshan, NPCs, companions, or world zones | `SUPERSEDED` | The direction is removed, not paused; remaining reachable 3D is migration debt and a missing key is not a blocker |
| Sprite3D/Node3D/Camera3D as acceptable final “2D” scaffolding | `SUPERSEDED` | Counted as shrinking game-wide debt |
| Landed GLBs stay until a zone migrates | `SUPERSEDED` | Resources belong only on the archive branch after tested retirement |
| Dimensional `world_style` rollback to 3D | `DISMISSED_NOT_IN_PROJECT` | Final 2D medium is not an experiment awaiting reversal |
| Historical Sky Lagoon migration order/pilot violation | `DISMISSED_NOT_A_DEFECT` | Process lesson; cannot be repaired retroactively |
| Jolt physical standees, 3D garnish, lights, spatial shaders, or particles as future direction | `DISMISSED_NOT_IN_PROJECT` | Convert/remove; no new 3D runtime work |
| 3D Opera outfits/rivals, 3D companion bodies, or Curve3D/Spline3 presentation prescriptions | `SUPERSEDED` | Preserve accepted gameplay goals during tested 2D conversion; this does not preserve the separately cut Opera boss acts |
| Curtain Dragon, Shadow Phantom, or Midnight Maestro as reachable Opera bosses, floor gates, finale cards, or required completion stars | `DISMISSED_NOT_IN_PROJECT`; runtime removal is machine-verified and external acceptance remains pending | Owner ruling `3d1236fe` cuts all three. Commit `e2c25878` removes their engine/UI/gates, preserves stable save bits 4/9/14 as raw tombstones, and passes focused/full-local/exact-head evidence; `MA-OPERA-011` remains `FIXED_PENDING_VERIFICATION` for authoritative visual/device/child/owner acceptance, while existing art remains unused historical/reuse material |
| No boss fights anywhere after the three Opera bosses are cut | `SUPERSEDED` | `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` section 17 / `ef2fd982` keeps boss fights only where Ember-aligned henchmen earn a narrative role; it does not restore the three Opera bosses or their save bits |
| One three-floor Opera picker as the final hub for all thirteen careers | `SUPERSEDED`; removed from current runtime | Owner direction `7426c187` distributes the jobs through thematic Castle rooms. Commit `09e5e356` implements that mapping, resolves Racer to Movie Lounge, deletes the picker, and guards against a hidden backdoor. `MA-OPERA-012` remains `FIXED_PENDING_VERIFICATION`, not closed, until a matching current APK plus visual, device, child, owner, exact-voice, listening, and other external acceptance complete |
| Device-only real-3D Opera kart with a headless/probe Canvas bypass | `SUPERSEDED` as design authority; source removal is machine-verified and external acceptance remains pending | Final authority requires one true-Canvas implementation. Commit `e2c25878` removes the exact `f3b0de07` ordinary-headless legacy route, and focused/full-local/exact-head evidence exercises one Canvas path; `MA-OPERA-010` remains `FIXED_PENDING_VERIFICATION`, while kart/3D debt outside Opera remains separate `MA-2D-002` work |
| `OPERA_MINIGAME_QUALITY_AUDIT_2026-08-09.md`'s 52-phase total and its old Ballerina, generic Boxer, and nested-kart Racer descriptions | `SUPERSEDED` in those scopes | Current shipping table is 13 careers/53 phases/27 modes; latest Ballerina, Boxer, and Canvas Racer authorities control while non-conflicting prop provenance/repairs remain supporting evidence |
| `OPERA_QUALITY_OVERHAUL_2026-08-09.md`'s 52-phase/19-mode/single-`bop` snapshot and requirement to loop every Ballerina row chronologically | `SUPERSEDED` in those scopes | Current Opera has 53 phases/27 modes/no generic `bop`; Ballerina frames are held pose keys because adjacent silhouette jumps are 41.6–47.3%, with only a one-shot curtain call |
| Earlier Ballerina atlas attempts, generic PHRASE/POSE/RIBBON/TWIRL route, or any leg/feet-like candidate | `SUPERSEDED` | `BALLERINA_PARTY_REBUILD_2026-08-09.md` and accepted generation `exec-a4dfa550-5374-43b6-a5e0-16a9d3d4b81c.png` control; prior leg/feet-like candidates remain rejected evidence, and the runtime atlas remains a one-tail mermaid at exact hash `c829784d4085e9cd9765cf0114a0f65bfe3f662ed8acc423223b726a0f003995` |
| Boxer manifest's retained `opera_boxer_outfit.glb`, `opera_boxer_dressing.glb`, and `opera_rival_boxer.glb` as useful runtime resources | `SUPERSEDED` | The Canvas specialist does not require them; while active they remain exact GAME2D transition debt and must retire through the normal tested archive path |
| Music audit's temporary retained `race` cue for an Opera nested kart | `SUPERSEDED` as final direction | The Canvas Racer stays under its Opera career music. Commit `e2c25878` removes the former legacy headless kart route; the old music recommendation does not regain authority |
| Painter-purpose worktree / branch | `UNCOMMITTED_CANDIDATE` | Purpose-focused Painter runtime edits are not part of current product/audit commit `09e5e356`; review, rebase, audit, and commit independently before any authority or shipping claim |
| Arborist career worktree / branch | `UNCOMMITTED_CANDIDATE` | Arborist art, surface, save, lobby, probe, and audit files are not part of current product/audit commit `09e5e356`; it is not a fourteenth current career or base model |
| Boxer V2 branch document | `DOCS_ONLY_CANDIDATE` | `design/BOXING_GAME_V2_2026-08-12.md` exists on a separate branch only; current authority remains the integrated five-phase Boxer until that proposal is independently reviewed and adopted |
| Roshan 2D atlas repacking | `DEFERRED_WITH_REASON` | Optimization; current sampling contract is green |
| Universal costume layers | `DISMISSED_NOT_A_DEFECT` | Optional feature, not audit closure work |
| Gabby | `DISMISSED_NOT_IN_PROJECT` | IP hold under `attic/gabby/` only |
| Sparkle guide fish implementation | `DISMISSED_NOT_IN_PROJECT` | Wayfinding need survives through voice, pointers, landmarks, and helping current |
| Whole-card bounce/spin/hover as meaningful object action | `DISMISSED_NOT_IN_PROJECT` | Feedback only; interaction changes a truthful object part/state |
| Seek's vinyl `characters/stickers/pearl_friend.png` pair card and `assets/mg/k_bush2.png` preview art as active actors/environment | `SUPERSEDED` for Seek | `8fa90111`/`27bda85d` replace them with frame-animated Evie/Lamb-a' actors and approved high-grade tree cards; the protected friend source remains untouched and neither legacy file is globally reclassified outside this bounded runtime use |
| Old Opera request-list scope | `SUPERSEDED` | Later August 3–5 audits replace the older requested-work inventory |
| Opera DO-NOT-PROMOTE B1–B6 condition | `VERIFIED_FIXED` | `3e479e68` records closure of that bounded gate; later indexed issues remain separate |
| Unadopted Chapter 2 plot, daily rhythm, naming, gifting, tending, decorating, and additional-minigame proposals | `DEFERRED_WITH_REASON` | Existing game, 2D conversion, and device evidence first. This deferral does **not** include the binding section-10 Castle-room career distribution or sections-16–17 Opera-boss retirement/Ember-antagonist rulings |
| Dungeon lock/key and Zelda-grammar expansion | `DEFERRED_WITH_REASON` | Proposal, not a current defect or implementation authorization |
| Broad CC0→original replacement campaign | `DEFERRED_WITH_REASON` | Address named live defects individually; no speculative mass redesign |

The following documents remain historical evidence, not work orders:
`NPC_3D_WORKORDER_2026-07-19.md`, `CHARACTER_PIPELINE.md`,
`CHARACTER_CUSTOMIZATION.md`, `CHARACTER_RUNBOOK.md`,
`gen2/ROSHAN_V2_WORKORDER.md`, `docs/ROSHAN_FINAL_MODEL_2026-07-18.md`,
`docs/ROSHAN_RIG_AUDIT.md`, `docs/ROSHAN_POSE_STRESS_2026-07-18.md`,
`gen2/generated/MEASURED_INTERFACE_SHEET_2026-07-19.md`, and all 3D/Blender/
Meshy conversion handoffs. Preserve them for why/history; never execute their
model recommendations.

---

## 8. Expanded acceptance notes for highest-priority indexed items

These notes improve repair planning but still are not complete canonical
finding records; section 10 controls that designation.

### MA-2D-002 — game-wide true-2D conversion

- **Rules:** `DL-MED-01` through `DL-MED-10`, `DL-PERF-03`, `DL-QA-09`.
- **State:** P1, `IN_PROGRESS`, V2/V3 partial.
- **Reproduction:** `python -B tools/audit_game_2d.py` and strict mode after an
  exact Godot 4.7.1 import.
- **Child impact:** mixed 3D and canvas architectures preserve inconsistent
  camera, input, occlusion, rendering, performance, and art-language behavior.
- **Repair:** one bounded gameplay family at a time; preserve verbs, save, and
  protected art; archive exact 3D resources; replace runtime with Node2D/
  CanvasItem/Control/Sprite2D; delete old resources only after dependency proof.
- **Surrounding tests:** positive and passive input, teardown/weakrefs, re-entry,
  save/load, caller/sibling probes, import, GAME2D unit/stress/regression/strict,
  and the full trusted suite.
- **Acceptance:** all eleven GAME2D categories named by `DL-QA-09` are zero at
  one exact commit; strict says satisfied; no protected-art, gameplay, save,
  touch, voice, or performance regression.

### MA-VIS-002/003/004/005/006 — current visual acceptance cluster

- **State:** `MA-VIS-005`'s false-occlusion tool path is `VERIFIED_FIXED`;
  `MA-VIS-002` is `FIXED_PENDING_VERIFICATION`, while `003`, `004`, and `006`
  remain open. Current clean-HEAD result
  is 16 FAIL, 17 REVIEW_OPEN, two MANUAL_OPEN, and 86 COVERAGE_GAP.
- **Evidence:** approved contract commits `3b7a7e66` and `fea916a8`, true-Canvas
  source `51d0abc0`, run-14 local Mobile evidence with manifest/PNG/probe hashes, and the clean
  fresh-runtime strict result and limitations in section 4.4. Saved or manual
  facts carry no PASS authority.
- **Repair:** preserve the implemented Lagoon Canvas/`Sprite2D` differential
  layers, unique object ownership, seams, touch lifecycle, and route state;
  preserve exact integrated machine/APK evidence and obtain requested-Mobile
  remote Sky PASS/JSON, device, child, owner, and accepted-visual evidence
  and repair only concrete failures. `SideScrollStage`, `Sprite3D`, or a
  filename-only relabeling is not an acceptable inverse. For
  the palette items, first replace global source averages with true state-local
  Canvas/HUD composites emitted by implemented closed adapters. Change art only
  if that evidence confirms a defect and the owner accepts the correction;
  never recolor/regenerate approved art to satisfy the old metric. The current
  tool already validates occlusion per relevant live card and fails closed;
  product adapters must now produce the required live evidence.
- **Surrounding tests:** visual unit/stress/strict, scene congruency, resolution,
  seams, overdraw, ownership, Lagoon gameplay/re-entry, 1280×720 and wide-phone
  capture, M11 squint, owner review.
- **Acceptance:** exact-source and external evidence verifies the implemented
  true-Canvas layers; pinned private fresh-runtime state-local evidence resolves each palette
  `REVIEW_OPEN`/`COVERAGE_GAP`; no applicable failure/review/manual/coverage gap
  and no new seam, duplicate, cutoff, ownership, touch, or performance defect.

### MA-SEEK-001 — animated true-2D Seek/Lamb-a' quality repair

- **State:** P1 bounded presentation defect, `VERIFIED_FIXED`, V3/V4 focused;
  protected exact-objective speech is separately `MA-ACCESS-003`.
- **Evidence:** `8fa90111` and `27bda85d`; new generated source/runtime paths,
  deterministic builder contract, exact archive proof, focused exact-Godot
  probe evidence, and reviewed 1280×720, 16:10, 20:9, and 4:3 captures.
- **Repair:** one fourteen-node Canvas stage uses approved seam-free background
  and high-grade tree cards plus real frame-swapped Roshan, Evie, and Lamb-a'
  actors. The former vinyl pair card and `k_bush2` preview draft are forbidden
  in this runtime. Lamb-a' is fully hidden until the authored opaque peek, then
  uses actual peek/reveal/hop/celebrate frames rather than opacity leakage or a
  transform-only sticker wobble.
- **Surrounding tests:** four generous routed touch targets through real
  `Viewport.push_input`, persistent no-reading assist, kind wrong target,
  60-second passive no-score/no-save, one-award save/medal/trophy, replay,
  control ownership, bounded nodes, teardown/weakrefs, portrait non-intercept,
  and multi-aspect bounds.
- **Acceptance:** the bounded visual, medium, touch, save, and lifecycle defect
  is closed without modifying protected originals. Overall 2D, device, child,
  and exact Evie “tap the wiggly tree” voice gates remain open and prevent a
  broader satisfaction claim.

### MA-OPERA-005/009 — current Ballerina and Boxer specialists

- **State:** both are `FIXED_PENDING_VERIFICATION`, V3 partial. The old
  Ballerina uniqueness premise and generic Boxer route are not current
  implementations, but neither specialist has final device/child/owner
  acceptance.
- **Ballerina evidence:** three full-stage acts, exact existing protected cues,
  5/10-second non-paying assists, monotonic progress, shared paint/hit geometry,
  both twirl directions, no generic card/combat/race, accepted 4×4 atlas hash
  `c829784d4085e9cd9765cf0114a0f65bfe3f662ed8acc423223b726a0f003995`,
  held pose keys, and a non-looping curtain call. The 41.6–47.3% neighboring
  silhouette jumps forbid treating each row as a normal temporal loop.
- **Boxer evidence:** five specialist modes, two independently owned gloves,
  optional two-touch but complete sequential one-finger play, no health/lives/
  damage/lost progress, one padded imp state machine, no generic combat layer,
  passive rejection, focus/close cleanup, and unchanged existing save bit 128.
- **Acceptance:** authoritative two-aspect Mobile capture, one-finger
  target-device comfort/performance and
  voice review, child comprehension, and owner identity/style acceptance.
  Boxer's three retained GLBs are separate `MA-2D-002` debt and cannot become a
  fallback for the Canvas specialist.

### MA-OPERA-010 — alternate ordinary-headless Opera lifecycle

| Field | Record |
|---|---|
| `id` | `MA-OPERA-010` |
| `title` | Ordinary unforced headless Opera used a legacy lobby/kart lifecycle different from the Canvas display route |
| `rule_ids` | `DL-MED-04`, `DL-INT-10`, `DL-SAVE-03`, `DL-QA-12` |
| `domain` / `zone` | Pearl Opera entry, Racer, lifecycle ownership, and test parity |
| `source` | Exact source comparison of display/forced-2D and ordinary-unforced paths at `f3b0de07`/`41087f66` |
| `severity` | P1 |
| `lifecycle` | `FIXED_PENDING_VERIFICATION` |
| `verification` | V3 full local plus exact-head remote: commit `e2c25878`, based on audit checkpoint `41087f66`, completes local `scripts/ci.sh` under exact official Godot `4.7.1.stable.official.a13da4feb` in 1428.6 seconds; run `31661887863` succeeds at exact integrated SHA `e0677ae4` |
| `reproduction` | Before repair, ordinary unforced headless startup selected the legacy lobby and `opera_act.gd` could attach `scripts/kart.gd`, while display/forced tests used Canvas. In the current repair, ordinary `main._start_opera_now()` creates the same `OperaLobby2D`/Canvas career route and no Opera controller contains an external-kart lifecycle |
| `child_impact` | Device and automated paths could exercise different games, hiding save, reward, teardown, and Racer failures until release |
| `evidence` | Current `scripts/opera_house.gd`, `scripts/opera_act.gd`, `scripts/main.gd`, and rewritten `scripts/probe_opera.gd`; focused exact Godot 4.7.1 ordinary-start/Racer/idle/reward/close/re-entry matrix green; GAME2D source shrink 68→66 production and 77→74 probe files; exact-head Ubuntu `OPERA`, `OPERA2D`, and `OPERA_DIEGETIC_PATHS` plus all 63 trusted headings green |
| `owner_decision` | Opera Racer is one true-Canvas career activity everywhere; an external kart or probe-only Canvas bypass is not accepted |
| `fix` | Collapse the Opera house/act lifecycle to Canvas-only entry and career ownership; fail closed on invalid/retired configs; preserve player, touch, music, reward, save, cancel, and return ownership |
| `surrounding_tests` | Ordinary unforced startup, all thirteen card routes, exact Racer cue/circle, 45 idle frames per career, no external kart, cancel/finish, pause and leave during earned-win delay, save/replay, teardown/re-entry, parser/lint/analyzer/GAME2D, surrounding Opera/living/audio/UI probes |
| `acceptance` | Authoritative supported-aspect capture, target-device touch/performance, child comprehension, and owner acceptance; focused, full-local, exact-head remote, and rollback evidence are already green |
| `closure` | Focused implementation, full-local runtime evidence, and exact-head run `31661887863` are green; commit `e2c25878` is recorded under `CHG-026`. APK/device/child/owner and authoritative visual gates remain pending |
| `relationships` | Split from bounded `MA-OPERA-008`; related game-wide source debt remains `MA-2D-002`; central navigation remains `MA-OPERA-012` |
| `history` | 2026-08-10: source split confirmed and assigned this ID. 2026-08-12: Canvas-only commit `e2c25878` passes focused and full local exact-Godot evidence, is recorded under `CHG-026`, and moves to `FIXED_PENDING_VERIFICATION`; run `31661887863` later verifies exact integrated head `e0677ae4` without filling external acceptance |

### MA-OPERA-011 — owner-cut Opera boss retirement

| Field | Record |
|---|---|
| `id` | `MA-OPERA-011` |
| `title` | Curtain Dragon, Shadow Phantom, and Midnight Maestro remain reachable and required after the owner cut all three |
| `rule_ids` | `DL-MED-04`, `DL-INT-13`, `DL-SAVE-01`, `DL-SAVE-06` |
| `domain` / `zone` | Pearl Opera routing, progression, save compatibility, and legacy boss runtime |
| `source` | `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` section 16; owner-cut commit `3d1236febdccf3fc816ba31d528744941ed4c3a9`; section-17 clarification commit `ef2fd982c770af72b2c5a6943704f5b8707d3e5a` |
| `severity` | P1 |
| `lifecycle` | `FIXED_PENDING_VERIFICATION` |
| `verification` | V3 full local plus exact-head remote: commit `e2c25878`, based on exact pre-repair checkpoint `41087f6634a416540b23a984d1f445b0bdab5f2f`, completes local `scripts/ci.sh` under exact official Godot `4.7.1.stable.official.a13da4feb` in 1428.6 seconds; run `31661887863` succeeds at exact integrated SHA `e0677ae4` |
| `reproduction` | At `41087f66`, `OperaHouse.ACTS` exposed bosses at indices 4/9/14, floor gates depended on them, and completion required all 16 bits. Current source keeps a stable 16-slot table but marks 4/9/14 retired, exposes only 13 cards, opens every transitional page directly, rejects boss configs, and completes when `(stars & 0xBDEF) == 0xBDEF` |
| `child_impact` | Before repair, the child was diverted into three cut encounters and required to clear them. Current focused evidence removes that route while preserving every earned career bit; external verification still blocks closure |
| `evidence` | Current `scripts/opera_house.gd` (`RETIRED_ACT_INDICES`, `LIVE_ACT_INDICES`, `RETIRED_STAR_MASK = 0x4210`, `ACTIVE_STAR_MASK = 0xBDEF`), `scripts/opera_lobby_2d.gd` (13 live cards/no finale card), `scripts/opera_act.gd` (boss/retired fail-closed), `scripts/save_state.gd` (raw mask plus live progress), and rewritten Opera/load/recovery/living/UI probes; exact focused/full-local Godot 4.7.1 matrix and all 63 exact-head trusted headings green |
| `owner_decision` | Cut Curtain Dragon, Shadow Phantom, and Midnight Maestro; retain their save-bit positions as unused gaps; any later boss fights belong to narratively relevant Ember henchmen and do not revive these acts |
| `fix` | Removed the three acts from reachable lists/cards/gates/completion; preserved career indices and raw legacy bits while retiring 4/9/14 in place; changed effective progress/completion to the thirteen live careers; removed the Opera boss/3D runtime. Existing art stays unused and is not deleted merely to close routing |
| `surrounding_tests` | Fresh/no-star, every individual career bit, all thirteen live bits, legacy saves with each/all retired bits, legacy `opera_progress` values, completion/reward exactly once, no passive award, close/re-entry, no boss card/voice/music/runtime reachability, no shifted career credit, exact import/analyzer/GAME2D/full trusted suite |
| `acceptance` | V4 supported-aspect/authoritative review confirms no stale boss UI; device/child/owner gates complete; focused/full-local/exact-head remote evidence and rollback under `CHG-026` are already green |
| `closure` | Focused V3 migration, routing, reward, passive, suspend, leave, teardown, and re-entry evidence plus full-local and exact-head gates are green, and commit `e2c25878` is recorded under `CHG-026`. Seventeen 1280×720 Mobile renders and five remote capture/upload pairs remain diagnostic/review evidence. Device/child/owner and authoritative visual gates remain pending |
| `relationships` | Implements the owner decision that supersedes old Opera-boss authority; related to `MA-2D-002`, `MA-OPERA-010`, `MA-OPERA-012`, and `MA-PLAY-001`; Ember henchman proposals are separate new content, not replacements in these save slots |
| `history` | 2026-08-02: `3d1236fe` records the owner cut and in-place bit retirement; `ef2fd982` clarifies that Ember-aligned boss fights do not restore the Opera bosses. 2026-08-12: reachable boss/gating/probe source at `41087f66` reproduced; commit `e2c25878` retires it, passes focused and full local exact-Godot evidence, is recorded under `CHG-026`, and moves to `FIXED_PENDING_VERIFICATION`; run `31661887863` later verifies exact integrated head `e0677ae4` without filling external acceptance |

### MA-OPERA-012 — Castle-room career distribution implemented; external and visual verification pending

| Field | Record |
|---|---|
| `id` | `MA-OPERA-012` |
| `title` | All thirteen careers now enter through their exact thematic Castle rooms; closure evidence remains incomplete |
| `rule_ids` | `DL-INT-12`, `DL-UI-01`, `DL-UI-03`, `DL-SAVE-04` |
| `domain` / `zone` | Pearl Castle rooms, Opera Hall, career discovery, routing, and return lifecycle |
| `source` | `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` section 10; owner-direction commit `7426c187c49d8153174c6a72e4ed5b97ed14387b`; sections 16–17 later remove the proposed Opera finale card without reversing room distribution |
| `severity` | P1 |
| `lifecycle` | `FIXED_PENDING_VERIFICATION` |
| `verification` | V3 exact local/remote/build plus V4 diagnostics: exact focused paths and `scripts/ci.sh` at runtime `09e5e356` are green in 1463.4 seconds/all 64; 22 Mobile renders were inspected. Pre-fix run `31678156887` remains red from fixed-frame sampling, while probe-only `ff068db` passes a 1379.3-second/64-probe local suite. Historical heads preserve bounded machine history. Product source `51d0abc0` preserves Opera behavior and passes full local in 1,404.5 seconds/all 64; integrated `441adf35` passes local/topic/dev machine gates and has a matching APK. V5, V6, and authoritative visual acceptance are absent |
| `reproduction` | From each Castle room, activate its current career picture card, complete or cancel the activity, and return. Royal Kitchen exposes Chef/Candymaker; Opera Hall Ballerina/Pop Star/Magician; Royal Library Detective; Craft Room Painter; Stuffie Playroom Doctor/Boxer; Bubble Bath Nursery; Mermaid Pool Astronaut; Family Dining Room Farmer; Movie Lounge Racer. Each path returns to that exact room. No all-career lobby or direct off-room tuple is reachable |
| `child_impact` | The primary P1 navigation defect is implemented: a non-reader can discover each job through the room that explains it. Residual P2 visual impact remains because the 154×154 lower-center cards obscure Roshan's lower body/tail in all nine room captures, and child comprehension has not yet been observed |
| `evidence` | Runtime `09e5e356`; probe-readiness `ff068db`; historical predecessor chain; `scripts/castle_career_routes.gd`; deletion of `scripts/opera_lobby_2d.gd`; guarded room-card ownership; exact focused probes; full local 1463.4-second runtime, 1379.3-second repaired-head, 1,435.2-second maintenance-head, 1,404.5-second product-source, and 1,391.5-second integrated-head gates; exact `441adf35` topic/dev runs `31760207048`/`31762132976`; exact-head Android `31763879294` and APK size/hash `596,033,220`/`f04d0fef…a72d8`; nine route plus thirteen career diagnostics. Source `51d0abc0` changes the Sky slice, not Opera; external or visual acceptance does not transfer |
| `owner_decision` | Distribute all thirteen careers through thematic Castle rooms. Opera Hall promotes only Ballerina, Pop Star, and Magician. Royal Kitchen promotes Chef/Candymaker; Library Detective; Craft Room Painter; Stuffie Playroom Doctor/Boxer; Bubble Bath Nursery; Mermaid Pool Astronaut; Dining Room Farmer. Movie Lounge is the resolved sole home for Racer |
| `fix` | Implemented at `09e5e356`: the shared route registry assigns one exact owner room per career; existing activities and sparse save bits remain stable; the all-career lobby is deleted; off-room/hidden routes are rejected; exact launching-room state, music, HUD, player, and touch ownership are restored; career/ambient/HUD/pause/Castle layers are explicit |
| `surrounding_tests` | One canonical hotspot per career, all thirteen routes, wrong/idle/passive input, room close/back/re-entry, activity cancel/finish return to the launching room, save/load and existing stars, no duplicate rewards, no hidden central all-career route, Opera Hall exactly three promotions, smallest-phone target sizes, fresh-save no-debug reachability |
| `acceptance` | Exercise the matching current APK; V4 accepted review confirms legible routes without lower-body/tail occlusion; V5/V6 confirm phone/M11 touch/readability and child discovery without reading or adult route instructions; owner, exact-voice, human-listening, and strict-2D gates complete |
| `closure` | Not closed. Exact integrated machine/build gates are green at `441adf35`, but device, child, owner, exact-voice, listening, strict-2D, and accepted visual evidence remain open, and the residual P2 route-card composition needs correction |
| `relationships` | Related to `MA-OPERA-011`, `MA-PLAY-001`, `MA-VIS-006`, and Castle `MA-2D-002` conversion; it preserves current career mechanics rather than superseding the specialist findings |
| `history` | 2026-08-02: `7426c187` records the owner room-distribution direction. 2026-08-12: runtime `09e5e356` implements all thirteen routes and deletes the lobby; `ff068db` repairs semantic readiness after red run `31678156887`. Historical heads preserve bounded remote/build history. Integrated `441adf35` preserves unchanged `51d0abc0` Opera behavior and adds exact local/topic/dev machine plus APK evidence; external/visual gates remain open. Lifecycle remains `FIXED_PENDING_VERIFICATION` |

### MA-AUDIO-001 — deterministic area-music rollout

- **State:** P2, `FIXED_PENDING_VERIFICATION`, V3 partial.
- **Machine evidence:** 42 unique declarative scores and production OGGs,
  complete score/renderer/PCM/OGG hashes, 48 kHz stereo delivery, exact loop
  tags and Godot imports, −18.05 to −17.97 LUFS-I, −8.76 to −4.10 dBTP,
  deterministic `--check`, route ownership, stale-close protection, and focused
  audio/probe evidence. Fifteen legacy directory files remain: 14 score assets
  and `banjo.ogg` as SFX.
- **Open human/device evidence:** two-wrap musical and seam listening, every
  cue's style/area identity, speech intelligibility and ducking, music-off
  persistence, mono fold-down, and Lenovo Tab M11 start/loop/memory review.
  No automated measurement grants those passes.
- **2026-08-24 all-audio extension:**
  `AUDIO_QUALITY_AUDIT_2026-08-24.txt` and the deterministic 303-row ledger
  extend measurement and disposition coverage to every voice, legacy score,
  ambience, UI cue, Castle/combat SFX, and fallback. The pass removes the
  clipping global UI tap, adds two exact Racer objective voices, true-peak
  repairs three unprotected generated voices, and preserves all six protected
  recordings byte-for-byte. It also adds `DL-SND-10` through `DL-SND-17` and
  `DL-QA-16`, because `MA-AUDIO-001` previously specified the 42 new scores but
  not complete runtime-audio quality. The aggregate state remains
  `FIXED_PENDING_VERIFICATION`: 31 legacy listening-led candidates, 126 bounded
  generated-voice peak candidates, exact protected-voice gaps, owner identity,
  mono, device, child, and human listening remain open. No bulk transcode or
  metadata-only upsample is accepted as repair.

### MA-PLAY-001 — normal-play reachability

- **State:** P1, `CONFIRMED_OPEN`, V1/V3 partial.
- **Current closure:** Lagoon→Reef is verified by `986010c0`; it does not prove
  the rest of the graph.
- **Repair:** first freshly enumerate current player-visible destinations, then
  add only owner-approved obvious child-visible routes. Do not copy the old
  August 2 destination list as current fact without reproduction.
- **Acceptance:** fresh-save no-cheat traversal through every door/seam and
  return path, with save/load, re-entry, voice/pointer, touch, and V5/V6
  comprehension evidence.

### MA-ACCESS-001/002/003 — protected voice gaps

- **State:** P1, `BLOCKED_EXTERNAL`, V1.
- **Repair:** do not modify protected family recordings. Obtain authorized exact
  recordings/re-rendering, including Evie's Seek tap-tree objective, or
  explicitly redesign a cue so spoken and diegetic channels independently
  communicate the objective.
- **Acceptance:** exact-key inventory, no wrong noun or required generic
  fallback, queue/ducking/teardown probes, device listening, and child
  comprehension.

### MA-PERF-001 / MA-CHILD-001 — real-product evidence

- **State:** P1, `BLOCKED_EXTERNAL`, V0.
- **Repair:** run the product before guessing a code fix: cold boot, main
  activities, transitions, 30-minute soak, P50/P95/P99, worst hitch, memory,
  thermal, touch latency, audio, save retention, then an observed five-minute
  child golden path.
- **Acceptance:** section 12 thresholds at the exact release candidate.

---

## 9. Individual repair and regression protocol

1. Freeze ID, rule, commit, reproduction, severity, lifecycle, and required
   evidence before editing.
2. Before calling an indexed item a finding, create its complete section-10
   record and link it from section 5.
3. Capture a failing baseline or falsifiable negative test.
4. Inventory affected code/art/audio/save/input and protected paths.
5. Apply the smallest truthful repair; do not bundle unrelated redesign.
6. Test correct, wrong, passive, repeated, cancel/focus-loss, teardown, re-entry,
   and save/load behavior as applicable.
7. Test caller, callee, sibling mode, shared helper, and zero-input guard.
8. For asset or medium changes, verify archive hashes/dependencies, import with
   exact Godot 4.7.2-stable, refresh the shrink-only manifest, and prove no debt growth.
9. Run parser, lint, analyzer, import, static gates, and all trusted probes,
   including ordinary-headless and display lifecycle paths rather than relying
   only on forced-2D test configuration.
10. Capture runtime/device/child/owner evidence where the acceptance record
   requires it.
11. Use `FIXED_PENDING_VERIFICATION` until every required level is present.
12. When no active item remains, repeat inventory, audit, confirmation, triage,
   repair verification, and re-audit from a clean build.

No probe is patched to accept a behavior regression unless the behavior change
is the explicit task. No generated-art or model deletion bypasses provenance,
protected paths, or surrounding-system tests.

---

## 10. Required finding fields

Section 5 contains indexed audit items, not canonical findings. A complete
record must exist at a stable linked path and contain every field below before
the project calls an item a canonical finding. An index may preserve a reported
lifecycle such as `VERIFIED_FIXED`, but the abbreviated row is not itself the
closure record and cannot authorize a new repair. Unknown evidence is written
explicitly as missing or blocked; a field is never omitted.

| Field | Requirement |
|---|---|
| Stable ID | `MA-<DOMAIN>-NNN`; never reused |
| Title | One falsifiable sentence |
| Rule IDs | One or more `DL-*` rules |
| Domain / zone | Code, art, audio, touch, save, performance, plus location |
| Source | Owner report, audit, tool, probe, capture, or observation |
| Severity | P0, P1, P2, or P3 |
| Lifecycle | One exact value from section 2.2 |
| Verification | Highest completed level, with `partial`/`reported` qualifier |
| Reproduction | Exact build, state, action, device, and aspect ratio |
| Child impact | Concrete consequence for this player |
| Evidence | Paths, lines, hashes, logs, captures, device/session evidence |
| Owner decision | Exact text/date when intent controls outcome |
| Fix | Minimal authorized intervention |
| Surrounding tests | Positive, negative, passive, sibling, teardown, save/re-entry |
| Acceptance | Observable closure conditions and required verification levels |
| Closure | Exact command/capture/device/session, result, commit, and date |
| Relationships | Duplicate, supersedes, superseded-by, or regression-of IDs |
| History | Timestamped transitions; never overwritten |

---

## 11. Audit-tool and documentation-control work

### 11.1 Visual audit

- `3b7a7e66` and `fea916a8` are the approved contract baseline: preserve their
  stress-first ordering, one-use fresh-runtime authority, complete source/Git
  closure, immutable capture handling, and strict unresolved-evidence semantics.
- Replace stale rule citations with stable `DL-*` IDs.
- The tool now treats `Sprite3D`/`Node3D`, spatial resources/APIs, and active
  model loads as transition debt; never restore the former allowance.
- Inventory all current player-visible zones; 86 current coverage gaps cannot
  close the game.
- Keep per-card decoded-alpha occlusion, unique target ownership, effective
  descendant draw order, source projection, and real touch reach fail-closed.
- Implement closed state adapters that generate fresh same-process
  Godot/Mobile/1280×720 Canvas/HUD captures; saved or manual facts remain
  diagnostic only and cannot suppress source risks or grant PASS.
- Fairy is now honestly `legacy_3d_debt`; implement and convert its intro/boss
  states rather than relabelling the current 3D runtime.
- Resolve every `MANUAL`, applicable `SKIP`, and `REVIEW_OPEN`; never convert
  missing evidence to pass.

### 11.2 Probe classification

Every one of the current 106 probe scripts receives exactly one state:

- `TRUSTED_BLOCKING`
- `RUNTIME_VISUAL_BLOCKING`
- `ADVISORY_CAPTURE`
- `DIAGNOSTIC_TOOL`
- `OBSOLETE_DELETE`
- `QUARANTINED_WITH_REASON`

Local/remote blocking-loop parity is `VERIFIED_FIXED` under `MA-CI-002` by
exact-head run `31457593351` for its then-current roster. Later run
`31648427712` stopped at the Opera provenance static gate before entering the
current remote probe loop; it remains failed evidence rather than being
retroactively recolored. Replacement run `31649113587` at exact `af4189a9`
executes all current 63 remote trusted probes successfully. Exhaustive
classification remains separately open as `MA-CI-003`.

### 11.3 Documentation control

Commit `9289dd81` completed the authorized `AGENTS.md`/`CLAUDE.md` and
`design/00` through `design/05` medium reconciliation without weakening valid
security/save/protected-art/workflow/cinematic rules. This integration adds
seven new Markdown sources plus the updated asset ledger. Their exact partial
authority is recorded in section 3.2: the Ballerina and music briefs are
current domain authorities; the Boxer brief is current except for retained-3D
resource language; the two general Opera audits retain non-conflicting repair
and provenance evidence but not their older counts, Ballerina/Boxer/Racer
mechanics, or Ballerina playback premise. The remaining gate must:

- give every tracked Markdown file one authority row and explicit valid scope;
- flag partial supersession rather than marking a mixed document wholly current;
- reject current-authority claims such as “real 3D Roshan,” “Sprite3D is final
  2D,” “landed GLBs stay,” or “Meshy migration paused,” except inside clearly
  marked historical/debt evidence;
- reject Godot 4.4 as a release baseline;
- verify unique IDs and resolvable `DL-*`/`MA-*` references.

Contiguous CHG-029 sources `5ed0c75460c9afd5ab574ff2c4a907c1075964f0`
and `7eb945957776ab3458a9de71c8be9937e2354720` implement and harden that
repository-side gate:
`design/05_DOC_LEDGER.md` classifies the exact 316-path Git-declared Markdown
inventory with 316 unique rows; section 5 links all 36 material records in
`audit/findings/ACTIVE_FINDINGS_2026-08-13.md`; and
`tools/audit_document_authority.py`, 36 focused unit tests, six mutation stress
controls, and blocking local/remote CI wiring enforce inventory, exact fields,
lifecycle/severity, rule, link, table, fence, and current-authority claims fail
closed, including wrapped stale evidence claims. Exact official Godot 4.7.1
full local CI is historically green at first source `5ed0c754` in 1,359.8
seconds/all 64. Exact CHG-023 maintenance checkpoint `51887315`, parent
`7eb94595`, then passes the current full local gate in 1,435.2 seconds/all 64
and exact-head Probe Suite run `31710377034`; the remote static phase reports
36 tests, six/six stress, 316/316 inventory/ledger, and then-current 36/36
active/records, all green. This moves `MA-DOC-002` and `MA-DOC-005` to
`VERIFIED_FIXED`; the current validator consequently reports 34 active items
while retaining all 36 records, and promotes this audit plus design 06 to
`CANONICAL_CURRENT`. Terminal records and
history remain in the canonical register. The CHG-029 source chain, exact
22-path boundary, and rollback start remain `5ed0c754`/`7eb94595`; `51887315`
and this prose synchronization are CHG-023 maintenance.

---

## 12. Master-audit satisfaction gate

This round may move to `SATISFIED` only when all conditions are true at one
exact commit. This is the operational checklist for `DL-QA-09` and
`DL-QA-10`:

- [ ] No P0/P1 remains in `REPORTED_UNCONFIRMED`, `CONFIRMED_OPEN`,
      `IN_PROGRESS`, `FIXED_PENDING_VERIFICATION`, `REGRESSED`,
      `OWNER_DECISION_REQUIRED`, `BLOCKED_EXTERNAL`, or
      `DEFERRED_WITH_REASON`. A P0/P1 `WAIVED_WITH_REASON` also blocks unless
      the owner explicitly accepts its residual risk for this exact round; a
      `DUPLICATE` is resolved only when its canonical owner is resolved.
- [ ] Every P2/P3 is `VERIFIED_FIXED`, explicitly deferred, waived, dismissed,
      superseded, or a duplicate whose canonical owner is resolved, with
      evidence.
- [ ] GAME2D strict has no manifest finding and reports zero
      `model_files`, `model_scan_coverage_files`, `active_export_model_files`,
      `model_import_sidecars`, `active_untracked_model_import_sidecars`,
      `model_archive_files`, `production_3d_files`, `probe_3d_files`,
      `scene_3d_files`, `configuration_3d_files`, and
      `archive_now_model_files`. Default exit zero and `NO_REGRESSION` are
      insufficient.
- [ ] The archive/preservation record is complete and no archived 3D resource
      is an active fallback or dependency.
- [ ] Authority docs, exhaustive ledger, and documentation gate agree with
      true 2D and exact Godot 4.7.2-stable at the candidate revision. Historical
      document-control closure in section 11.3 is not a new baseline or full
      semantic-consistency pass.
- [x] Every material indexed audit item has a linked complete canonical record
      containing all section-10 fields.
- [ ] The off-repository Alpha journal is imported or replaced by a fresh,
      equally scoped audit; unnamed reports are not assumed fixed or open.
- [ ] Visual stress is green and every applicable failure, review, manual item,
      and coverage gap has an explicit accepted disposition.
- [ ] Exact Godot 4.7.2-stable parser, lint, analyzer, fresh import, static
      gates, and the complete current trusted probe rosters pass at the
      candidate integration commit. Verify roster parity rather than copying
      historical probe counts. Prior run evidence is retained in section 4.6
      and never substitutes for this candidate gate.
- [ ] Full runtime capture covers every activity at 1280×720 and a representative
      wide-phone aspect ratio.
- [ ] Target phone and M11 meet P95 ≤33.3 ms, P99 ≤50 ms, no normal-path hitch
      >100 ms, no low-memory kill, and no thermal collapse in a 30-minute soak.
- [ ] Touch, voice, pointer, haptic, pause/focus loss, save/load, teardown,
      return, and re-entry pass on device.
- [ ] An observed five-minute child golden path completes without adult verbal
      instruction, reading, trapped state, accidental reward, lost progress,
      obvious presentation break, or frame-time breach.
- [ ] Owner accepts identity/style and every deliberate exception.
- [ ] A clean second master-audit pass discovers no new P0/P1 issue.

Code-refinement conditions, added by the 2026-08-26 criteria update
(`DL-CODE-01` through `DL-CODE-10`; round record
`MASTER_AUDIT_2026-08-26.md` in this directory). These give the
architecture-and-maintainability dimension the same operational footing as
the medium, visual, and evidence gates:

- [ ] `scripts/main.gd` is at or below the standing coordinator target below
      2,500 lines through reviewed mechanical extractions, and no other
      gameplay script exceeds 3,000 lines without its recorded decomposition
      plan (`DL-CODE-01`, `DL-CODE-02`).
- [ ] No per-frame allocation remains in tick/draw paths, burst effects are
      pooled, and every child-facing surface has a Speedy-tier path or a
      recorded measured budget note (`DL-CODE-07`, `DL-CODE-08`).
- [ ] Durable child-visible progress is save-backed — no reward or visible
      completion state lives only in per-activity scratch (`DL-CODE-03`).
- [ ] The distinct string-state-key count is at or below its recorded
      baseline (409 at `9a1754c1`) and the named clone families each have one
      shared implementation (`DL-CODE-04`, `DL-CODE-05`).
- [ ] Every shipped mode has a driving trusted probe in both rosters and
      zero-input negative coverage over its reward surface (`DL-CODE-10`);
      the central passive snapshot covers every save-backed reward field.
- [ ] No dead code adjacent to a child-safety invariant remains
      (`DL-CODE-09`).
- [ ] The Mode Platform growth law holds (`DL-CODE-11`,
      `design/08_TARGET_ARCHITECTURE.md`): for migrated families, new
      content lands as a mode script plus a registry row with `main.gd`
      untouched, demonstrated by the platform's growth-law test; and the
      structure ratchet (`DL-CODE-12`) is armed and blocking with budgets
      monotone and no waiver outstanding past expiry.

These criteria are a framework, not a ceiling: a material defect outside
them is still a finding, and a recurring off-list defect class earns a rule
in `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` section 18 in the same
commit as the audit that justified it.

Current result: **`IN_PROGRESS` / `UNSATISFIED`; the audit remains
`REPAIRING`, not `SATISFIED`.**

---

## 13. Current repair order

1. Preserve the now-verified document-control contract while authorizing every
   later repair: exact CHG-023 maintenance head `51887315`, parent `7eb94595`,
   passes official Godot 4.7.1 full local CI in 1,435.2 seconds/all 64 and
   exact-head Probe Suite run `31710377034`. Keep the 316-path inventory, 316
   unique ledger rows, 36 linked complete records, fail-closed tool/tests, and
   local/remote CI wiring synchronized. `MA-DOC-002` and `MA-DOC-005` are
   `VERIFIED_FIXED`; future drift regresses them. CHG-029 still owns only
   sources `5ed0c754`/`7eb94595`, and later bookkeeping remains CHG-023.
2. Preserve sealed true-Canvas source `51d0abc0`, exact parent `1b7d6bda`, and
   its 19-path +3,318/-3,517 boundary. Its exact local source-byte suite passes
   in 1,404.5 seconds/all 64; run-14 is 20/20 local Mobile/Speedy with manifest
   hash `AEAC7C72…DE34` and visual-probe hash `B9EAF5E0…9C6C`. Preserve the
   unknown `source_revision` truth and the historical `7391c53c` remote
   `gl_compatibility` failure. Preserve exact `441adf35` local/topic/dev machine
   evidence and Android `31763879294`; next obtain a requested-Mobile remote
   Sky PASS/JSON. Neither artifact upload nor local review grants acceptance.
3. Treat the Sky local product slice as implemented but still pending external
   verification. Preserve its CanvasLayer/Node2D/Sprite2D/Camera2D ownership,
   real parallax, master-coordinate touch/navigation, five readable animals,
   repaired focus/grounding/contact, and route/return/re-entry behavior. Close
   `MA-VIS-002` only after target-device and owner/accepted-visual evidence.
   Continue one tested true-2D gameplay family from the exact
   509-model/65-production-file inventory until every GAME2D category is zero;
   archive exact resources before active deletion.
4. Implement live fresh-runtime Canvas adapters for converted surfaces and then
   Fairy; keep every missing or nonaccepted capture as a gap.
5. Preserve the verified current Ballerina, Boxer, Candymaker, and 42-cue
   machine evidence, predecessor exact-head run `31661887863`, the green runtime
   `09e5e356` 1463.4-second full-local gate, and the probe-only `ff068db`
   1379.3-second/64-probe full-local gate. Preserve red run `31678156887` as
   readiness-failure history and preserve successful exact-head machine-
   workflow run `31686380560` with its warning/internal-diagnostic limits.
   Preserve historical exact `18b6150c` Probe Suite run `31693492735` and
   matching Android run `31695675866`. Preserve the latest integrated-
   predecessor e6 dev Probe Suite `31722047536` and exact-source package run
   `31724927769` with APK SHA-256 `66d16de5…ca17c`; every predecessor APK is
   machine/build evidence, not device or child acceptance. Finish external
   verification of the focused `MA-OPERA-010`/`011`/`012` repair: keep
   one Canvas lifecycle, no external
   Opera kart/boss engine, raw-preserving save tombstones 4/9/14, and live mask
   `0xBDEF`. Do not change the sealed Castle Kitchen caller without renewed
   owner visual approval; its current Chef config is valid/probed. Preserve the
   implemented exact Castle-room distribution, Movie Lounge Racer, deleted
   all-career lobby, and exact-room returns. Move/restage the route cards so they
   do not obscure Roshan's lower body/tail, repair remaining Opera capture and
   exact-voice coverage, and split the stale grouped Opera art claims.
   Confirm or dismiss palette risks only from current state-local evidence.
6. Reconcile protected voice gaps, including Evie's exact Seek tap-tree cue,
   through owner-authorized sources.
7. Rebuild and prove the complete child-visible world graph.
8. Classify all probes and remove only proved obsolete assets/code.
9. Preserve the historical `a3d3bce1`, `ad36ee9f`, and `dacef140` evidence and
   the 1437.1-second exact local gate at `f3b0de07`. Preserve failed run
   `31648427712` as evidence of the CRLF/LF provenance defect, not as a pass;
   replacement `31649113587` is green at exact `af4189a9`. Rerun local and
   remote gates whenever runtime/static content changes and at the eventual
   release candidate, then produce the accepted capture matrix, exercise the
   matching APK,
   target-device U0 pass, audio listening matrix, and child golden path.
10. Repeat the master audit from `INVENTORYING`; satisfaction cannot come from
    closing only the first list.
11. Execute the 2026-08-26 code-refinement round: the comprehensive analysis,
    goal set G1–G12, and implementation sequencing live in
    `MASTER_AUDIT_2026-08-26.md` (this directory), with the Codex work
    packages in `CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md`
    at the repository root. Safety and gate hardening precede structural
    refactors; every package is probe-gated under the section-9 protocol and
    the new section-12 code-refinement conditions; findings
    `MA-CI-004`, `MA-CI-005`, `MA-CI-006`, `MA-CI-007`, `MA-CODE-003`,
    `MA-CODE-004`, `MA-CODE-005`, `MA-PERF-002`, `MA-PERF-003`,
    `MA-SAVE-001`, `MA-AUDIO-002`, and `MA-TOUCH-002` are its scope, with
    `MA-CODE-001` the binding constraint. The structural stage executes
    through the Mode Platform remodel and migration plan M0–M6 in
    `design/08_TARGET_ARCHITECTURE.md` (owner-requested 2026-08-26): the
    remodel changes where growth lands (`DL-CODE-11`) and arms the
    structure ratchet (`DL-CODE-12`) so the coordinator target is enforced
    by CI rather than intention.

---

## 14. Change history

| Date | State | Change |
|---|---|---|
| 2026-08-09 | `INVENTORYING` | Prior masters, audits, work orders, status sources, code, assets, probes, and owner decisions inventoried |
| 2026-08-09 | `AUDITING` | Static design/code/art/tool evidence compared; visual and dimensional gates run |
| 2026-08-09 | `CONFIRMING` | Current reports separated from pre-fix symptoms, optional ideas, and superseded 3D premises |
| 2026-08-09 | `TRIAGING` | Canonical severity, lifecycle, verification, authority, supersession, dismissal, and deferral states created |
| 2026-08-09 | `REPAIRING` | Roshan model retirement, child-safety fixes, visual/tool corrections, and true-2D slices proceed individually |
| 2026-08-09 | focused `VERIFYING` | GAME2D 73-unit/14-stress contract green; exact synchronized inventory remains 513 models/71 production files and `UNSATISFIED` |
| 2026-08-09 | `REPAIRING` | Opera racer finale converted to Canvas at `82124b3a`; stale manifest entry and post-slice full gate remain open |
| 2026-08-09 | focused `VERIFYING` | `f8efeb0a` strengthens companion patient/no-fail, passive, teardown, re-entry, and legacy-save coverage without claiming companion 2D completion |
| 2026-08-09 | `REPAIRING` | `8ed978be` retires the medal legacy spatial scoreboard and reduces production 3D-file debt 71→70 |
| 2026-08-09 | focused `VERIFYING` | `344d8d5c` removes both stale manifest entries; exact full `scripts/ci.sh` exits 0 with 61 trusted probes and GAME2D 513/70 `NO_REGRESSION`; strict remains unsatisfied |
| 2026-08-09 | focused `VERIFYING` | `e4528b27` binds the racer circle phase to exact `op_racer_lap_two` speech and clears stale caption/fallback behavior; parser, lint, Opera2D, voice, Opera, and default GAME2D audit are green, but no full CI at that checkpoint is claimed |
| 2026-08-09 | `CONFIRMING` | `9289dd81` reconciles operational/design authority to game-wide true 2D, explicitly superseding real-3D/Meshy/Sprite3D final direction while preserving binding security, save, protected-art, cinematic, engine, and release rules |
| 2026-08-09 | focused `VERIFYING` | `5df75427` moves Faron's Dolls catcher to a bounded Canvas activity and locks real touch, passive safety, save/medal/replay, teardown, and Mobile capture behavior |
| 2026-08-09 | `REPAIRING` | `8fa90111` adds the provenance-locked animated Evie/Lamb-a' source/runtime kit for the named Seek asset gap; protected references remain unchanged |
| 2026-08-09 | focused `VERIFYING` | `27bda85d` rebuilds Seek as a fourteen-node animated Canvas meadow, supersedes its vinyl pair/`k_bush2` runtime drafts, removes four byte-verified archived GLBs, and passes focused real-touch/passive/save/replay/multi-aspect review; exact Evie objective speech remains open |
| 2026-08-09 | focused `VERIFYING` | `e6e56f8b` drives the default Hybrid Lagoon portal through the actual explicit interaction route, proves proximity alone does not enter, and preserves Classic/no-touch behavior |
| 2026-08-09 | `CONFIRMING` | `96317f8b` keeps local `/tmp/*` review artifacts out of production status without deleting evidence or granting ignored facts authority |
| 2026-08-09 | focused `VERIFYING` | `3b7a7e66` replaces saved-fact and Sprite3D allowances with the fail-closed same-process fresh-runtime visual evidence contract |
| 2026-08-09 | focused `VERIFYING` | `fea916a8` extends visual source closure to active ignored/custom-root runtime sources; review-only ignored output remains non-authoritative |
| 2026-08-09 | `REPAIRING` | `a3d3bce1` records the exact 509-model/68-production/77-probe GAME2D shrink; default and regression modes are green while strict remains `UNSATISFIED` |
| 2026-08-09 | focused `VERIFYING` | Exact local full `scripts/ci.sh` at runtime HEAD `a3d3bce1` exits 0 after 1434.3 seconds: exact Godot 4.7.1-stable, fresh import, all static gates, GAME2D `NO_REGRESSION`, and all 61 trusted probes green. Repeated invalid-UID fallbacks for `sponge_tubes.glb` and `starfish.glb` remain nonfatal open 3D/resource-hygiene debt under `MA-ASSET-005`; the run is not warning-free or release-clean. |
| 2026-08-09 | `IN_PROGRESS` | Clean fresh-runtime visual strict at `a3d3bce1` fails closed at 16 FAIL/17 REVIEW_OPEN/2 MANUAL_OPEN/86 COVERAGE_GAP/32 PASS/94 NOT_APPLICABLE because no live Canvas capture output was accepted; strict 2D, voice, device, child, owner, and clean re-audit closure remain open |
| 2026-08-10 | `CONFIRMING` | All newer `origin/dev` documents and runtime through `245c1613` are reviewed against audit `HEAD` `7b5d1209`. Current Opera authority is 13 careers/53 phases/27 modes/208 frames; older 52-phase, generic Ballerina/Boxer, looping-Ballerina, and nested-kart descriptions are partially superseded rather than silently retained. |
| 2026-08-10 | focused `VERIFYING` | `MA-OPERA-005` moves to `FIXED_PENDING_VERIFICATION`: current Ballerina uses the accepted `c829784d…003995` one-tail atlas, held pose keys, one-shot curtain call, and dedicated Pearl Mirror/Ribbon Trail/Grand Twirl specialist with focused exact-Godot probes green; capture/device/child/owner acceptance remains open. |
| 2026-08-10 | focused `VERIFYING` | `MA-OPERA-009` is created as `FIXED_PENDING_VERIFICATION` for the five-phase two-glove Boxer specialist; `39746756`'s phone-safe Candymaker pour is integrated; exact merged Opera/Nursery/Detective/gesture/passive/voice probes are green while remote exact-head and device gates remain open. |
| 2026-08-10 | focused `VERIFYING` | `MA-AUDIO-001` is created as `FIXED_PENDING_VERIFICATION`: deterministic score/render/import/routing evidence is complete for 42 new cues, while human two-wrap/style/voice/mono and Lenovo Tab M11 listening remain open. |
| 2026-08-10 | focused `VERIFYING` | `MA-CI-002` moves to `FIXED_PENDING_VERIFICATION` after the 63-local/62-remote roster and default/stress parity gates include the new Opera probes; final remote exact-head execution remains open. Exhaustive classification of all 105 probes is preserved separately as new `MA-CI-003`, `CONFIRMED_OPEN`. |
| 2026-08-10 | `CONFIRMING` | `MA-ASSET-005` is dismissed as a source defect after valid tracked GLBs/sidecars and a warning-free isolated fresh import prove four ignored local import-cache files caused the UID warnings; the GLBs remain separate GAME2D medium debt. |
| 2026-08-10 | `VERIFIED_FIXED` | `MA-CHANGE-001` adds the append-only CHG-001–023 change/rollback ledger and read-only planner: 64 owned source commits plus seven merge-topology commits cover all 71 reachable audit commits; 14 tests, non-mutation replay, exact Git-history checks, GAME2D no-regression, and independent adversarial review are green. |
| 2026-08-10 | `REPAIRING` | Earlier reconciliation preserved the display/forced-2D Canvas Racer with exact `op_racer_lap_two` speech at merge `ad36ee9f`. The later exact `f3b0de07` review narrows this historical claim: an ordinary-headless legacy lobby/kart source path remained and is now explicit `MA-OPERA-010` debt. |
| 2026-08-10 | focused `VERIFYING` | The resolved integration content committed as `ad36ee9f` completes exact Godot 4.7.1 `scripts/ci.sh` in 826.4 seconds with fresh import, all static gates, GAME2D `NO_REGRESSION`, and all 63 trusted local probes then in the roster green. At that historical checkpoint, remote exact-head CI remained pending; strict 2D, visual, audio-listening, device, child, and owner gates stayed open. |
| 2026-08-10 | `REPAIRING` | Exact-head GitHub run `31455723446` at process commit `57bc08d1` fails before import in `prepare_opera_minigame_art.py --check-only`: Linux and Windows reproduce identical RGBA pixels but not identical PNG compression bytes. CHG-015 is widened with an IDAT-only comparison repair and strict chunk/mode/size/scanline/pixel/delivery-hash negative controls; the replacement exact-head run remains pending. |
| 2026-08-10 | focused `VERIFYING` | `fe10ffd2` and exact-head run `31456633826` prove all 39 governed Opera minigame artifacts green on Linux. The same run then exposes a separate missing-FFmpeg integration error before import; music verification is moved, not removed, to a parallel checksum-pinned Windows job matching its recorded render toolchain. Replacement exact-head evidence remains pending. |
| 2026-08-10 | focused `VERIFIED_FIXED` | Workflow/parity repair `dacef140` completes exact-head run `31457593351` successfully in 34m19s. The pinned Windows job verifies 42/42 deterministic music deliveries; Ubuntu passes static gates, import, analyzer, GAME2D 509/68/77 `NO_REGRESSION`/`UNSATISFIED`, all 62 trusted probes, boot, and advisory balance. All five capture/upload pairs completed at the workflow level and uploaded diagnostic artifacts; they are not visual passes. This closes the two CI integration defects only; release, strict-2D, visual, listening, device, child, and owner gates remain open. |
| 2026-08-12 | focused `VERIFYING` | Merge `f3b0de07` reconciles newer `origin/dev` parent `ea6185fd` with audit parent `5f58ef0a`. Exact Godot 4.7.1 local `scripts/ci.sh` exits 0 after 1437.1 seconds with all 64 trusted probes and current static/provenance gates green. GAME2D has 74 unit tests plus 14 falsification controls and remains exact `NO_REGRESSION`/`UNSATISFIED` at 509 models/509 active, 157 tracked plus 352 generated sidecars, 68 production/77 probe/one scene/one config. Visual advisory remains `UNSATISFIED` at 16 FAIL/17 REVIEW_OPEN/2 MANUAL_OPEN/86 COVERAGE_GAP/32 PASS/94 NOT_APPLICABLE. This closes local merge integration only; exact-head remote/APK/device/child/owner/listening/strict-2D/authoritative visual evidence remains open. |
| 2026-08-12 | `CONFIRMING` | Exact source review narrows `MA-OPERA-008` to its display/forced-2D Canvas cue/finale repair. Ordinary headless startup still selects a legacy Opera lobby and may attach `scripts/kart.gd`; new `MA-OPERA-010` keeps that lifecycle and `MA-2D-002` debt open instead of allowing forced-2D probes to certify it away. Current Candymaker is integrated; Painter purpose and Arborist are uncommitted candidates, and Boxer V2 is docs-only on a separate branch. |
| 2026-08-12 | `CONFIRMING` | At this historical checkpoint, binding owner directions in `7426c187`, `3d1236fe`, and section-17 clarification `ef2fd982` are restored to the central authority chain. `MA-OPERA-011` keeps the then-reachable but owner-cut Curtain Dragon/Shadow Phantom/Midnight Maestro, their gates, and their boss runtime open while requiring stable save slots 4/9/14 to become inert tombstones. `MA-OPERA-012` separately keeps that checkpoint's three-floor all-career Canvas picker open as transitional/rejected final routing until all thirteen careers are distributed through Castle rooms and Opera Hall promotes only Ballerina/Pop Star/Magician. No runtime fix is claimed in this row; later rows record both repairs. |
| 2026-08-12 | `REPAIRING` / focused `VERIFYING` | Exact-head run `31648427712` at `bbc817ef` passes the pinned Windows area-music job 42/42 but fails only the Ubuntu static Opera-art gate: generated provenance held the raw CRLF checkout hash of declared text `GENERATION.json`, while Linux read LF. Import, analyzer, probes, boot, and captures did not run. Repair `af4189a9` canonicalizes only that declared text hash to LF, leaves binary hashes byte-exact, refreshes provenance, and passes 10 focused tests plus Windows and LF-clean archive checks at 42/42. At this historical point, replacement exact-head remote and a full local suite at `af4189a9` had not run. |
| 2026-08-12 | focused `VERIFIED_FIXED` | Replacement exact-head run `31649113587` succeeds at `af4189a9`. Ubuntu completes static checks, import, the full analyzer, all current 63 remote trusted probes, boot, Dust/Opera advisory balance, Opera manifest, and five diagnostic capture/upload pairs in 35m27s; pinned Windows music completes 42/42 in 3m55s. This closes exact-head remote CI only. The captures remain diagnostic; at this historical point `f3b0de07` was still the last full local checkpoint, and APK/device/child/owner/listening/strict-2D/authoritative visual gates remained open. |
| 2026-08-12 | focused `VERIFYING` | Opera retirement/lifecycle commit `e2c25878` removes the ordinary-unforced legacy lobby/kart split and the three owner-cut boss routes while preserving the 16-slot raw save namespace, tombstones 4/9/14 (`0x4210`), live mask `0xBDEF`, and thirteen-career effective progress. Exact focused Godot 4.7.1 startup/all-career/Racer/idle/save/reward/pause/leave/teardown/re-entry and surrounding matrices are green. GAME2D is exact `NO_REGRESSION` at 509 models, 157+352 sidecars, 66 production, 74 probes, one scene, one config; all 74 unit tests and 14 stress controls pass. Seventeen 1280×720 Mobile renders were visually inspected as diagnostic/review evidence, leaving global visual 16/17/2/86/32/94 unchanged. `MA-OPERA-010`/`011` move to `FIXED_PENDING_VERIFICATION`; `MA-OPERA-012` remains P1 `CONFIRMED_OPEN`. The sealed Castle Kitchen caller was deliberately unchanged because current Chef config is valid/probed and any speculative caller hardening requires renewed owner visual approval. This row records the focused phase; the following rows record its full-local and exact-head verification. `CHG-026` records the exact 32-path commit and manual inverse. At this focused-only point, external verification remained pending. |
| 2026-08-12 | focused `VERIFYING` | Opera commit `e2c25878` completes `scripts/ci.sh` with exit 0 after 1428.6 seconds under exact official Godot `4.7.1.stable.official.a13da4feb`: all 64 trusted local probes, 74 GAME2D unit tests, 14 stress controls, and 93 visual-contract unit tests are green. Castle interaction approval candidate `1754c880e4ef3df87daed47e1a8ec1ed36e114956ae86dbc50a74e40bba392d9` covers 13 assets/104 frames in the machine/review ledger. The 17 V4 Mobile renders remain diagnostic/review evidence, not device/child/owner or authoritative visual acceptance. At this local-only point exact-head remote had not yet run; the following row records it. The global audit remains `UNSATISFIED`; `MA-OPERA-010`/`011` remain `FIXED_PENDING_VERIFICATION`; `MA-OPERA-012` remains P1 `CONFIRMED_OPEN`; `CHG-026` records the exact commit and manual inverse. |
| 2026-08-12 | focused `VERIFYING` | GitHub run `31661887863` succeeds at exact integrated SHA `e0677ae4c4f5e48258ff57c38f82e25f2dc3d9d0`. Ubuntu succeeds in 33m8s through checkout/checksum, exact Godot, static/import/full analyzer, exactly 63 trusted probe headings, boot, Dust/Opera advisories, Opera manifest, and five diagnostic capture/upload pairs. `OPERA`, `OPERA2D`, Nursery, and Detective are green; `OPERA_DIEGETIC_PATHS` reports 2247 checks/13 careers/64 stations/53 phases/48 spurs. Remote GAME2D remains 509/66/74 exact `NO_REGRESSION`/`UNSATISFIED`. Windows succeeds in 6m52s and ends `MUSIC\|check 42/42\|picture_xmas`. This closes exact-head machine verification for that predecessor only; the five pairs remain non-authoritative and APK/device/child/owner/human-listening/strict-2D/authoritative visual evidence remains open. At this checkpoint `MA-OPERA-010`/`011` remain `FIXED_PENDING_VERIFICATION` and `MA-OPERA-012` remains P1 `CONFIRMED_OPEN`; the next row records its later implementation. |
| 2026-08-12 | focused `VERIFYING` | Runtime commit `09e5e35665fd8d1bd782693e10fc0198f756d2c8` implements all thirteen exact Castle-room career routes, selects Movie Lounge as Racer's sole home, deletes the three-floor all-career lobby, rejects hidden/off-room routes, restores each exact launching room, preserves sparse bits/tombstones/live mask/rewards, and fixes explicit career/ambient/HUD/pause/Castle layers. Exact focused probes and full local official-Godot CI are green; `scripts/ci.sh` exits 0 after 1463.4 seconds with all 64 trusted probes. Twenty-two 1280×720 renders (nine routes plus thirteen careers) are diagnostic only; lower-center cards obscure Roshan's lower body/tail in all nine route captures (residual P2). `MA-OPERA-012` moves to `FIXED_PENDING_VERIFICATION`, not verified. `CHG-027` records the exact commit and manual inverse. At that checkpoint exact-head remote, matching APK, device, child navigation/comprehension, owner, exact-voice, accepted-visual, listening, and strict-2D gates remained open. |
| 2026-08-13 | focused `VERIFYING` | GitHub run `31678156887` at pre-fix audit head `3fc151c8b3b6c054d0f6e6ab89f84a9f464f3f20` is genuinely red, not a `FAILURE_RE` false positive: Ubuntu `probe_opera` reports only Detective and Nursery failed the stable-Canvas compound after a fixed four-frame sample of the 0.25-second reveal. Their launches, passive behavior, saves/rewards, exact-room returns, dedicated probes, all other executed gates/probes, and Windows pass; no product script/resource/runtime error appears. Probe-only commit `ff068db002202839f920a6f9fb78c942788a3034` preserves runtime `09e5e356`, replaces the frame guess with a bounded fail-closed wait for the exact instance/reveal/stage/layer state, and passes exact official-Godot full local CI in 1379.3 seconds with all 64 trusted probes. `MA-OPERA-012` remains `FIXED_PENDING_VERIFICATION`; at that checkpoint replacement exact-head remote and every APK/device/child/owner/voice/visual/listening/strict-2D gate remained open. CHG-027 then owned both commits and the rollback catalog contained 27 IDs/73 owned references/four emitters/21 tests/23 manual groups. |
| 2026-08-13 | focused control `VERIFYING` | Contiguous commits `d991fdf3fbdb229de8685c3e52917b280942adb5` and `9befc0f838f40eead2f42088a91206257fe217a8` materially synchronize executable rollback controls/tests and the current audit/design authority across an exact ten-path union without changing runtime. CHG-028 owns this bounded documentation migration as a narrow exception; routine future self-hash/count maintenance remains CHG-023. The current catalog is 28 IDs/75 owned references/four emitters/22 tests/24 manual groups. The synchronization preserves red run `31678156887`, repaired-head local evidence, and every then-open remote/APK/external gate rather than claiming new acceptance. |
| 2026-08-13 | focused `VERIFYING` | GitHub run `31686380560` succeeds at exact authority head `9befc0f838f40eead2f42088a91206257fe217a8`. Ubuntu runs 09:24:08–09:57:48 UTC (33m40s) and completes static/import/full analyzer, exactly 63 remote trusted headings, trusted probes, boot, Dust/Opera advisories, and Opera manifest green. Windows runs 09:24:08–09:27:55 UTC (3m47s) and ends `MUSIC\|check 42/42\|picture_xmas`. All five capture/upload pairs completed at the workflow level and uploaded diagnostic artifacts, not capture gates or visual passes. Raw Sky Lagoon `LAGOONSHOT` output has 21 `OK`, 44 `FAIL`, and `DONE` (66 diagnostic lines), so that diagnostic internally fails. The run is not warning-clean: existing Vulkan-to-OpenGL fallback and ObjectDB/resource/texture-leak diagnostics remain. No matching APK, device, child, owner, exact-voice, listening, strict-2D satisfaction, or accepted-visual evidence is claimed. |
| 2026-08-13 | focused `VERIFYING` | Exact integrated dev/audit head `18b6150c01e1587100dca97c85ebad03f369825a` passes Probe Suite run `31693492735`: exactly 63 remote trusted headings complete in the 29m41s probes job and music completes 42/42. Capture output remains diagnostic/nonaccepted; raw Sky Lagoon reports 21 `OK`, 44 `FAIL`, and `DONE`, with 20 PNGs. Android dev run `31695675866` succeeds at the same exact head and publishes a 596,041,412-byte APK with SHA-256 `fb4979473441d416f7b07914b1396f5f883935d4c08bf077baed3dfb91b78941`. Device, child, owner, exact-voice, human-listening, strict-2D, accepted-visual, and residual P2 route-card gates remain open. |
| 2026-08-13 | focused document control `VERIFYING` | Sealed source `5ed0c75460c9afd5ab574ff2c4a907c1075964f0`, exact parent `18b6150c01e1587100dca97c85ebad03f369825a`, expands `design/05_DOC_LEDGER.md` to the exact 316-path Git-declared Markdown inventory with 316 unique rows, links 36 complete stable records from section 5, and adds a fail-closed document-authority tool, 35 focused tests, six mutation stress controls, and blocking local/remote CI wiring. It changes exactly 19 paths with 2,645 insertions/232 deletions and no runtime, save, protected-art, audio, asset, generated-art, or gameplay behavior. Exact official Godot 4.7.1 full local CI is green in 1,359.8 seconds with all 64 trusted probes. `.github/workflows/probes.yml` is a high-risk workflow scope; its change is limited to three read-only Python commands under existing `contents: read` and adds no action, package, credential, secret, network, publication, or write permission. CHG-029 owns this manual, non-emitting documentation migration; the catalog is now 29 IDs/76 owned references/four emitters/23 tests/25 manual groups. `MA-DOC-002` and `MA-DOC-005` remain `FIXED_PENDING_VERIFICATION`, and the audit remains `IN_PROGRESS` / `UNSATISFIED`, because no exact-head remote result is claimed for `5ed0c754`. Stable records remain after later terminal transitions so history is preserved. |
| 2026-08-13 | focused document hardening `VERIFYING` | Contiguous hardening source `7eb945957776ab3458a9de71c8be9937e2354720`, exact parent `5ed0c75460c9afd5ab574ff2c4a907c1075964f0`, changes exactly 13 paths with 479 insertions/160 deletions. It overlaps ten first-source paths and adds the changelog, planner, and planner test, producing an exact 22-path union. Summed source churn is 3,124 insertions/392 deletions; the exact `18b6150c`→`7eb94595` net diff is 3,024/292. It adds multiline stale-claim regressions and synchronizes sealed evidence without runtime/save/protected-art/audio/asset/generated-art/gameplay or workflow changes. CHG-029 owns both sources; the post-head exact-hash/count synchronization is CHG-023 maintenance, not a third source or CHG-030. Current catalog: 29 IDs/77 owned references/four emitters/23 planner tests/25 manual groups. Document authority is 36/36 tests, six/six stress, 316/316 inventory/ledger, and 36/36 active/records green. First source full local remains 1,359.8 seconds/all 64; no exact-head full-local or remote result is claimed for `7eb94595`, so `MA-DOC-002`/`005` remain `FIXED_PENDING_VERIFICATION` and the audit remains `IN_PROGRESS` / `UNSATISFIED`. |
| 2026-08-13 | focused document control `VERIFIED_FIXED` | Exact CHG-023 maintenance checkpoint `51887315bd537db2d16bdafcac1bbfa808352351`, parent `7eb945957776ab3458a9de71c8be9937e2354720`, synchronizes the CHG-029 boundary and current authority across 11 documentation/planner paths with 298 insertions/213 deletions and no runtime, workflow, save, protected-art, audio, asset, generated-art, or gameplay change. Exact official Godot 4.7.1 `scripts/ci.sh` exits zero after 1,435.2 seconds/all 64. Probe Suite run `31710377034` succeeds at the same SHA: Ubuntu runs 14:28:33–15:09:45 UTC (41m12s), the trusted loop takes 18m02s with exactly 63 headings, the document static gate reports 36 tests/six stress/316/316/36/36 ALL OK, and Windows completes in 4m08s with raw 42/42 ALL OK. Raw Sky Lagoon remains 21 OK/44 FAIL/one DONE and non-authoritative; runner warnings, legacy resource diagnostics, matching APK, device, child, owner, voice, listening, strict-2D, visual, and release gates remain open. `MA-DOC-002`/`005` move to `VERIFIED_FIXED`; the master audit and design 06 become `CANONICAL_CURRENT`, while the game-wide audit remains `IN_PROGRESS` / `UNSATISFIED`. CHG-029 still owns only `5ed0c754`/`7eb94595` over 22 paths; this checkpoint and the terminal-lifecycle prose sync remain CHG-023 maintenance, with 29 IDs/77 references/four emitters/23 tests/25 manual groups unchanged. |
| 2026-08-13 | focused Sky diagnostic `VERIFYING` | Exact parent `e6edf559af219edd4e5ce38cab0c5094483be5c6` passes latest integrated dev Probe Suite run `31722047536` with probes 34m25s/63-of-63, document controls 36 tests/six stress/316 parity/34 active and 36 retained, and music 3m33s/42-of-42. Earlier branch run `31719143975` is corroborating e6 history. Workflow-run Android `31724927769` uses raw checkout/package source exact e6 and publishes the latest predecessor 596,041,412-byte APK at SHA-256 `66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c`. Two-file source `7391c53cd6981a256bd8bfe40ccbb9f72fb723fe` then replaces obsolete Sky courtyard/custom-camera assertions with the production camera and twenty ordered promenade states spanning all five live animals; no runtime, workflow, asset, save schema, protected-art, voice, friend, or gameplay file changes. Exact official Godot 4.7.1 full local CI exits zero after 1,402.3 seconds/all 64. The local Mobile/Speedy capture manifest is 20/20 PASS with 20 exact 1280×720 PNGs and 1,078 assertions; probe SHA-256 is `f28413263c0bedeed421fae6e9de4626095f03b6010bade8380ad7fb5aa07db9` and GAME2D manifest SHA-256 is `8c70b9aeaba5302322bdd44ca84d8a2b76fca053a091753e0e04676ee407fb00`. Normal save fingerprints and in-memory plane/time state are restored. Exact-source Probe Suite run `31728755204` completes overall `SUCCESS`: probes 40m05s with a 17m50s trusted step/63 headings and music 3m38s/42-of-42. Its nonblocking Sky step internally fails: 20 PASS rows and summary `20/20/20/20/0/0` are followed by `GLOBAL\|FAIL\|rendering_method\|gl_compatibility`, `RESULT\|FAIL`, and exit 1 because the runner lacks `VK_KHR_surface`; PNGs upload, JSON does not. The locally reviewed frames expose tiny frog/otter and subtle-focus P1 risks plus animal/Roshan overlap, grounding, and seesaw-contact P2 defects; the one-mural/spatial runtime remains, so `MA-VIS-002`/`006` stay `CONFIRMED_OPEN`. Workflow remains continue-on-error/PNG-only, and no remote diagnostic PASS/JSON/APK/device/child/owner/art acceptance is claimed. Manual/non-emitting CHG-030 owns the source; the current catalog is 30 IDs/78 unique references/four emitters/24 tests/26 manual groups. The audit remains `IN_PROGRESS` / `UNSATISFIED`. |
| 2026-08-13 | focused Sky true-Canvas repair `VERIFYING` | Sealed source `51d0abc0d32855a8ba32932599fedd8f59b398b7`, exact parent `1b7d6bdaf89ebc7c9bdeae16fbde0e14079fd8a8`, changes exactly 19 paths including `scripts/probe_northern.gd`, with 3,318 insertions and 3,517 deletions. It replaces the spatial promenade with a `CanvasLayer` -1, literal 6144×2048 `Node2D` master, six-by-two `Sprite2D` backdrop, differential Canvas layers, real parallax, and a sole `Camera2D`; movement, touch, focus, pause cancellation, save/return, all five animals, three playground actions, and Reef/Castle/Northern/Galaxy/Ember/kart transitions use that owned Canvas lifecycle. No art, asset, protected original, audio, workflow, or save-schema file changes. The exact source bytes pass official Godot 4.7.1 full local CI in 1,404.5 seconds with all 64 unique trusted headings completed and no trusted-probe, script, parse, or compile failure; advisory diagnostics remain scoped evidence rather than a warning-clean claim. Run-14 supplies 20/20 local 1280×720 Mobile/Speedy frames with zero failed/skipped/global rows, manifest SHA-256 `AEAC7C72E0A3BFF992713127261DD00ED69049947DFB6723AA66365F5712DE34`, and visual-probe SHA-256 `B9EAF5E0738CFB61CCD3E34ACFEA420AEADAB4E3ADE80B40A2CFD1F227569C6C`; those hashes bind its manifest/PNGs and probe script, not the full source revision, which remains `unknown`. Two independent human reviews approve the local candidate. GAME2D is 509 models/65 production/70 probe files, exact `NO_REGRESSION`, 14/14 stress, and still `UNSATISFIED`. `MA-VIS-002` moves from `CONFIRMED_OPEN` to `FIXED_PENDING_VERIFICATION`; `MA-2D-002` stays `IN_PROGRESS`; `MA-VIS-006` stays `CONFIRMED_OPEN`; `MA-TOUCH-001` and `MA-RELEASE-001` stay `FIXED_PENDING_VERIFICATION`; `MA-PLAY-001` stays open; `MA-PERF-001`/`MA-CHILD-001` stay external. Historical `7391c53c` run `31728755204` retains its failed remote `gl_compatibility` subprocess. No exact-source remote/APK/device/child/owner/accepted-visual claim exists. Manual/non-emitting CHG-031 owns the source; catalog totals are 31 IDs/79 references/four emitters/25 planner tests/27 manual groups. Overall audit remains `IN_PROGRESS` / `UNSATISFIED`. |
| 2026-08-13 | integrated Sky authority/build `VERIFYING` | Governance-only integrated evidence head `441adf35f7dbdeb67d36fbf1a2217b87d3040d47` preserves unchanged CHG-031 product source `51d0abc0`. Exact official-Godot local `scripts/ci.sh` exits 0 in 1,391.5 seconds with all 64 unique headings. Topic Probe run `31760207048` succeeds with probes 33m39s and music 3m18s; dev Probe run `31762132976` succeeds with probes 33m39s and music 3m56s. Both exact-head runs complete 63/63 unique remote headings with zero hard failures, document controls 36 tests/six stress/316 inventory/316 ledger/34 active/36 records, and music 42/42. Both nonblocking Sky diagnostics request Mobile but miss `VK_KHR_surface`, fall back through llvmpipe to `gl_compatibility`, emit 20 PASS rows plus summary `20/20/20/20` with failed 0/skipped 0, then emit `GLOBAL`/`RESULT` FAIL and exit 1; PNGs upload, no remote JSON or Mobile PASS. Android run `31763879294` succeeds at exact checkout/package HEAD `441adf35`, version code 1414, `dev`/`android-dev`, and publishes a 596,033,220-byte APK with SHA-256 `f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`; the 82-byte checksum sidecar has SHA-256 `43e892cfb6c9a3847e1a8760d5cad4dd8fb36719d63db0625ec8b2fa3ba8e651`. This closes exact integrated machine/build provenance only. Run-14 `source_revision` remains unknown and no device/child/owner/accepted-visual/listening/strict-2D/release acceptance transfers. Lifecycle remains `MA-2D-002` `IN_PROGRESS`, `MA-VIS-002`/`MA-TOUCH-001`/`MA-OPERA-012`/`MA-RELEASE-001` `FIXED_PENDING_VERIFICATION`, `MA-VIS-006` `CONFIRMED_OPEN`, `MA-PLAY-001` open, and `MA-PERF-001`/`MA-CHILD-001` external. The synchronization is CHG-023 maintenance, not CHG-032. Overall audit remains `IN_PROGRESS` / `UNSATISFIED`. |
| 2026-08-26 | `CONFIRMING` | The code-refinement round re-inventories the tree at integration head `9a1754c1` (169 commits past sealed evidence head `441adf35`): the Canvas Melody rebuild, Castle Canvas2D baseline rooms, Day One wing (start-menu New Game routing, dirty pool, art studio), Harper/Fiona slide canvas, game-wide audio remediation, and the 2026-08-25 owner Opera House venue landed after the last audited head, so the round's measurements are pinned to `9a1754c1` while every sealed historical claim above stands unchanged for its own commit. The owner venue commits are recognized in section 3.2 as the newest Opera navigation direction, premise-consistent with `MA-OPERA-012`. |
| 2026-08-26 | `TRIAGING` | Criteria update: design 06 gains section 18 (`DL-CODE-01`–`DL-CODE-10`), section 12 gains the code-refinement conditions, and the framework clause is recorded. Twelve bounded findings open (`MA-CI-004`–`MA-CI-007`, `MA-CODE-003`–`MA-CODE-005`, `MA-PERF-002`, `MA-PERF-003`, `MA-SAVE-001`, `MA-AUDIO-002`, `MA-TOUCH-002`), decomposing `MA-CODE-002` per its own fix plan; `MA-CODE-001` is re-measured at 10,499 lines and named the round's binding constraint; `MA-CODE-001`, `MA-CODE-002`, and `MA-OPERA-012` histories are appended. The round record is `MASTER_AUDIT_2026-08-26.md`; implementation is handed to Codex via `CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md` under section 13 item 11. No lifecycle claim beyond V1 static evidence is made by this round; this documentation-only integration is CHG-023 maintenance (rollback: revert its commit), consuming no new CHG ID; the audit remains `IN_PROGRESS` / `UNSATISFIED`. |
| 2026-08-26 | `TRIAGING` | Owner direction, same day: the round's shrink goals alone are insufficient — a comprehensive remodel must change the architecture so continued expansion no longer grows `main.gd`. `design/08_TARGET_ARCHITECTURE.md` (`BINDING_DOMAIN`, code structure) answers it: the Mode Platform formalizes the MiniGame contract's plumbing into a ModeDirector, declarative ModeRegistry, and owned Services; the growth law becomes rule `DL-CODE-11`, the CI structure ratchet becomes `DL-CODE-12`, section 12 gains the matching gate condition, and the Codex handoff gains Stage C (WP-C0–C6 = migration M0–M6, absorbing the structural halves of G7/G10/G11). Section 9 of design 08 reserves four decisions for explicit owner confirmation. Documentation-only; CHG-023 maintenance; audit remains `IN_PROGRESS` / `UNSATISFIED`. |
| 2026-09-05 | focused boss-encounter evidence `VERIFYING` | Indexes `BOSS_ENCOUNTER_VISUAL_AUDIT_2026-09-05.md` as `SUPPORTING_CURRENT`. Focused exact-4.7.2 probes cover Grand Puff, Pepper and the bounded CombatTutorial repair. Tracked local packet `audit/boss_encounter_2026-09-05/manifest.json` binds 17 normalized source hashes and 13 unmodified final Mobile PNGs; all hashes recheck, final Dust 1280×720/1560×720 runs end `DONE`, tutorial root3 ends `ALL OK`, and all capture error logs are empty. This cross-reference preserves `MA-2D-002`, `MA-VIS-006`, `MA-PLAY-001`, `MA-TOUCH-001` and the exact-voice gap at their canonical states. Durable remote commit, combined CI, residual 3D, device, child and owner acceptance remain open; inventory baselines and overall `IN_PROGRESS` / `UNSATISFIED` are unchanged. |

| 2026-09-05 | `TRIAGING` | Owner-directed planning integration: add the planning front page, chapter guide/brief/reference library, Northern restaurant planning branch, and `DL-PLAN-01` through `DL-PLAN-06`. Record delegated playable-chapter development, minor canon-preserving additions, strategic unused assets, and free mechanic remixing. Correct active engine and Chapter 2/global progression references, preserve historical evidence, and distinguish reserved architecture choices from recommendations. No runtime, art, device, child, owner-product, release, or finding-closure claim is added. |

No later state is added without its required evidence.
