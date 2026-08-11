# Mermaid Roshan: Reef of Light — game-wide master audit

- **Audit ID:** `MA-2026-08-09`
- **Audit date:** 2026-08-09
- **Audited branch:** `codex/master-audit-20260809`
- **Integration commit:**
  `ad36ee9f` (parents `7b5d1209b4c4823fbf9ed39193c8b1700a288497`
  and `245c16137fae82271dabac456d5ab04d843463a8`)
- **Last completed full local checkpoint:**
  `a3d3bce18dd73d0ac87f2fb4bac397e2b4396180`
- **Proposed design authority:** `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`
- **Change and rollback ledger:**
  `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md`
- **Document authority:** `PROPOSED_CANONICAL`
- **Audit program status:** `IN_PROGRESS`
- **Overall cycle state:** `REPAIRING` with concurrent focused `VERIFYING`
- **Satisfaction:** **UNSATISFIED**

This document is the proposed audit-cycle and triage ledger for the 2026-08-09
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

At integration commit `ad36ee9f`, the exact
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

The same integration review incorporates every newer 2026-08-09 Opera and
music change instead of preserving the audit's earlier Ballerina premise. The
shipping Opera table now contains **13 careers, 53 phases, and 27 distinct
modes**, with no generic `bop` phase. All 13 Roshan career atlases account for
**208 reviewed runtime frames**. The current Ballerina is the dedicated
three-act Pearl Mirror → Ribbon Trail → Grand Twirl recital documented by
`BALLERINA_PARTY_REBUILD_2026-08-09.md`; it uses the accepted
`roshan_ballerina_sheet_a.png` hash
`c829784d4085e9cd9765cf0114a0f65bfe3f662ed8acc423223b726a0f003995`
as held pose keys and a one-shot curtain call, not the old looping Ballerina
art or generic phase set. Boxer now owns a five-phase, full-stage two-glove
specialist surface. Candymaker's syrup pour now has one complete, phone-legible
mold, a generous pitcher target, and one shared painted-spout/stream/hit
geometry.

Racer remains a true-Canvas three-phase activity. The upstream device-only 3D
kart restoration was rejected during reconciliation: shipping `RACE` uses the
same Canvas surface, a `circle` gesture, no widget, goal `0.9`, and exact
`op_racer_lap_two` speech. There is no device/headless implementation split and
no external kart child. The music program adds **42 deterministic area cues**
on top of the 15 legacy files (14 score files plus the `banjo.ogg` SFX); its
machine composition, hash, codec, loop, loudness, and routing evidence is
green, while human two-wrap/style listening, voice intelligibility, mono
fold-down, and Lenovo Tab M11 review remain open.

The Castle personalization update is also integrated: the saved logo now
replaces both painted purple shell banners in the Craft Room and both in the
Stuffie Playroom, retains the Craft board badge, remains input-transparent, and
does not appear in rooms with no registered banner. This is a bounded Canvas
overlay repair, not evidence that the still-spatial Castle rooms satisfy the
game-wide 2D contract.

The resolved integration content committed as `ad36ee9f` completes exact Godot 4.7.1-stable local
`scripts/ci.sh` in 826.4 seconds with all 63 trusted probes green. This is a
strong integration result, but a remote exact-head run does not yet exist. It
does not close strict 2D, live visual
capture, APK, audio-listening, device, child, protected-voice, or owner gates.

No P0 audit item is currently indexed from the repository evidence reviewed for
this round. Missing runtime, device, child, manual-art, and off-repository
evidence prevents the stronger claim that no P0 exists.

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
| `V3 RUNTIME` | Exact Godot 4.7.1 analyzer/import and focused/full trusted probes |
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
2. Direct owner product decision, 2026-08-09, within those boundaries: remove
   3D Mermaid Roshan; the game is true 2D; active 3D resources belong only on
   the deprecated-resources branch.
3. Exact Godot 4.7.1-stable requirements and the remaining current operational
   rules in `AGENTS.md`, excluding its stale 3D clauses.
4. `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` once tracked and reconciled.
5. A current domain document within its explicitly retained scope.
6. Historical audits and work orders as evidence only.

### 3.2 Current authority map

| Source | State | Scope |
|---|---|---|
| Owner's 2026-08-09 true-2D directions | `OWNER_DECISION` | Highest-precedence medium and resource-retirement decision |
| This audit | `PROPOSED_CANONICAL` | Audit-item states, evidence, closure, and history for this round; section 5 remains an index until full records exist |
| `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` | `PROPOSED_CANONICAL` | Stable `DL-*` rules and acceptance contract |
| `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md` | `BINDING_OPERATIONAL` | Stable `CHG-*` change groups, benefit/risk/dependency evidence, and guarded per-change rollback plans; never permission to bypass protected-asset, save, security, medium, or release gates |
| `AGENTS.md` except named stale 3D passages | `BINDING_OPERATIONAL` | Engine, security, save, protected art, workflow, and release rules |
| `SECURITY.md` | `BINDING_OPERATIONAL` | Threat model and protected data |
| `WORKFLOW_BRANCHING_2026-07-18.md` | `BINDING_OPERATIONAL` | Dev/master promotion process |
| `ASSET_LICENSES.md` | `BINDING_LEDGER` | Current and historical asset provenance |
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

### 3.3 Design-language confirmation state

The proposed comprehensive design language is based on the current owner
decision and triage of prior masters, audits, repair records, art rules,
touch/voice/save contracts, and current machine evidence. Its child, visual,
interaction, motion, audio, cinematic, performance, save, provenance, and QA
rules are current.

Both proposed documents are tracked. Commit `9289dd81` reconciled
`AGENTS.md`, `CLAUDE.md`, `design/00` through `design/05`, and the named
medium-authority surfaces to game-wide true 2D without weakening security,
save, protected-art, engine, cinematic, or release rules. It remains
`PROPOSED_CANONICAL` until:

- the documentation ledger covers every tracked Markdown path exactly once;
- every material active audit item links to a complete canonical record; and
- a documentation gate proves unique IDs, resolvable references, lifecycle
  validity, table/fence integrity, and forbidden current 3D claims.

This proposed status does not weaken the direct owner decision. It prevents a
tracked but still incomplete ledger/record system from falsely claiming
completed repository-wide documentation control.

---

## 4. Evidence at the integration snapshot and named historical commits

### 4.1 Repository snapshot

| Fact | Result |
|---|---:|
| Tracked Markdown files | 307 |
| `scripts/main.gd` | 8,519 lines |
| GDScript files under `scripts/` | 192 |
| `scripts/probe_*.gd` files | 105 |
| Names in the local trusted loop | 63 |
| Names in the remote headless trusted loop | 62 |

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

#### 4.2.3 Integration commit `ad36ee9f` pending remote exact-head verification

The resolved integration now has the real merge identity `ad36ee9f`, with
parents `7b5d1209` and `245c1613`. Its runtime/static content completed the
local full gate below; remote exact-head execution and matching APK/device
evidence remain pending. Current focused evidence is:

```text
GAME2D unit contract: 73 tests OK
GAME2D stress contract: 14 falsification/control assertions ALL OK
GAME2D regression: NO_REGRESSION at 509 models / 68 production files
GAME2D strict/default inventory state: UNSATISFIED
Opera deterministic art: 39 governed files match
Opera Roshan animation audit: 13 careers / 208 reviewed frames ALL OK
Area-music deterministic build check: 42/42 ALL OK
Probe parity audit (default and stress): ALL OK
Exact integration-content scripts/ci.sh: exit 0 after 826.4 seconds
All 63 trusted local probes reached accepted verdicts
```

The complete local integration gate uses exact Godot 4.7.1-stable, performs the
fresh import, static gates, GAME2D regression check, analyzer, and all 63
trusted local probes, and exits zero after 826.4 seconds. Parser and inference
lint are also green for all 22 changed/new GDScripts. Focused exact runtime
probes independently remain green for Opera2D, Nursery, Detective, Opera
gesture quality (271 checks), audio, picture games, interaction, passive play,
voice, and the surrounding Opera path. The resolved content is integration
commit `ad36ee9f`; remote exact-head CI remains pending, as do Mobile capture,
APK, device, child, and owner gates.

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

The current `ad36ee9f` integration audit reproduces the same
state totals: **16 FAIL, 17 REVIEW_OPEN, two MANUAL_OPEN, 86 COVERAGE_GAP,
32 PASS, and 94 NOT_APPLICABLE**. The unchanged totals are not evidence that
the merge is visually accepted; the missing live Canvas capture matrix still
fails closed and remote fresh-runtime strict evidence remains open.

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
  `NO_REGRESSION`, and all 61 then-trusted probes. Integration commit
  `ad36ee9f` also completes the exact local `scripts/ci.sh` gate in 826.4
  seconds with all 63 current trusted probes. It still has no remote exact-head
  result; that is not inferred from the local run.
- The earlier two invalid-UID warnings were reproduced as stale ignored local
  `.godot/imported` cache artifacts. Source GLBs and tracked sidecars are valid,
  and an isolated fresh project import is warning-free. Their reachable 3D
  resources remain medium debt under `MA-2D-002`, but no source-UID defect is
  inferred from that local cache.
- Current-HEAD strict GAME2D was run and failed as required; no zero-debt result
  is claimed.
- No complete live visual-runtime capture matrix is claimed; fresh-runtime
  strict produced no accepted Canvas captures and failed closed.
- No target-phone or M11 performance/thermal/audio/touch result is claimed.
- No observed child golden-path session is claimed.
- No owner identity/style acceptance is inferred.
- The 36 unnamed items mentioned by an off-repository Alpha journal are not
  imported as current bugs. The journal must be obtained or replaced by a fresh
  equally scoped audit.

---

## 5. Triage item index — not canonical finding records

This section is a navigation and lifecycle index. Its rows intentionally omit
many mandatory fields and therefore are not canonical finding records under
section 10 or Design section 17. `MA-*` remains a stable audit-item identifier,
but an indexed item may be called a canonical finding only after a linked record
contains every mandatory field. No abbreviated row is closure evidence.

### 5.1 P0/P1 and acceptance-blocking indexed items

| ID | Severity | Lifecycle | Verification | Indexed issue | Closure requirement |
|---|---|---|---|---|---|
| `MA-2D-002` | P1 | `IN_PROGRESS` | V2/V3 partial | Section 1 records 509 model/export files, 157 tracked model sidecars, 352 active untracked sidecars, 68 production 3D files, 77 probe 3D files, one 3D scene, and one 3D configuration; scan-coverage, model-archive, and archive-now counts are zero. Dolls and Seek are converted, but current player, Fairy, and other active surfaces still enforce legacy 3D | All eleven GAME2D categories reach zero; strict gate, import, focused/surrounding/full probes green |
| `MA-DOC-002` | P1 | `CONFIRMED_OPEN` | V1 | The old document ledger is incomplete and lacks exact partial-supersession scope | Exhaustive unique row for every tracked Markdown path |
| `MA-DOC-003` | P1 | `BLOCKED_EXTERNAL` | V1 | An off-repository journal is said to hold 36 unnamed entries described as findings | Import source evidence or replace with fresh equal-scope audit; do not assume the entries are current |
| `MA-DOC-005` | P1 | `CONFIRMED_OPEN` | V1 | Material active audit items do not yet have linked full canonical records containing every section-10 field | Create and validate one complete linked record per material active item before calling it a canonical finding or starting its next repair |
| `MA-VIS-002` | P1 | `CONFIRMED_OPEN` | V1 | Sky Lagoon remains one mural layer across twelve tiles | True Canvas/`Sprite2D` differential layers with seams/ownership/overdraw green and runtime/device review; `SideScrollStage`, `Sprite3D`, or filename-only relabeling cannot close it |
| `MA-VIS-003` | P1 | `REPORTED_UNCONFIRMED` | V1; `REVIEW_OPEN` | Reproduced source-average saturation diagnostics flag Fairy and Lagoon, but Fairy is probably a false positive/coverage gap and Lagoon is only a plausible hierarchy risk | True state-local Canvas composite with HUD/viewport/runtime/device evidence; do not recolor or regenerate approved art merely to satisfy the current average |
| `MA-VIS-006` | P1 | `CONFIRMED_OPEN` | V2/V3 partial | Approved fresh-runtime contract is fail-closed, but clean HEAD has 16 failures, 17 reviews, two manual items, and 86 coverage gaps because no live Canvas capture output was accepted | Implement every required live state adapter/capture; every applicable FAIL/REVIEW/MANUAL/COVERAGE_GAP explicitly resolved |
| `MA-PLAY-001` | P1 | `CONFIRMED_OPEN` | V1/V3 partial | No end-to-end fresh-save, child-visible, no-cheat world reachability proof exists | Enter/leave/re-enter every visible destination without direct debug calls; save/seam/touch/voice checks |
| `MA-ACCESS-001` | P1 | `BLOCKED_EXTERNAL` | V1 | Required exact voice cues remain absent for some objectives | Authorized exact recordings or independently sufficient spoken/diegetic design; playback/device/child evidence |
| `MA-ACCESS-002` | P1 | `BLOCKED_EXTERNAL` | V1 | Lamba's current semantic role still maps to legacy “bunny-fish” recordings | Owner-approved re-record/re-render and exact-key/device listening evidence |
| `MA-ACCESS-003` | P1 | `BLOCKED_EXTERNAL` | V1/V3 partial | Seek has an accurate visual wiggle/U-cue/peek and an available Evie hide-and-seek recording, but no exact protected Evie recording says “tap the wiggly tree” | Owner-authorized exact Evie objective recording plus queue, device-listening, and child-comprehension evidence; do not modify protected audio |
| `MA-TOUCH-001` | P1 | `FIXED_PENDING_VERIFICATION` | V3 reported | Held travel/medallion path lacks real-phone hold/drag/multitouch/focus-loss evidence | Recorded target-phone pass |
| `MA-OPERA-001` | P1 | `FIXED_PENDING_VERIFICATION` | V3 partial | Chef now uses the accepted batter pitcher, source-true stream/fill behavior, mitt-gated oven, achieved cake, and deterministic topping art; the old cutoff/fallback/wrong-object report is not a current code premise | Remote exact-head gate for the integrated branch, then accepted two-aspect/device/owner art review |
| `MA-OPERA-002` | P1 | `CONFIRMED_OPEN` | V4 partial | Detective's “missing” crown remains painted into the scene evidence | Healed owned source, narrative/capture verification |
| `MA-OPERA-004` | P1 | `CONFIRMED_OPEN` | V1 | Opera capture harness has not produced accepted evidence for all careers | Repair harness; capture and human-review all careers/widgets/scuffles/stress states |
| `MA-OPERA-009` | P1 | `FIXED_PENDING_VERIFICATION` | V3 partial | Boxer now has a full-stage five-phase two-glove specialist with optional multitouch, sequential one-finger completion, no health/loss, passive rejection, touch-owner cleanup, and stable existing save bit | Remote exact-head gate for the integrated branch, two-aspect and target-device touch/performance review, child comprehension, and owner visual acceptance |
| `MA-PERF-001` | P1 | `BLOCKED_EXTERNAL` | V0 | No current target-device frame-time, hitch, memory, thermal, or latency matrix | U0 device matrix at exact release candidate meets design thresholds |
| `MA-CHILD-001` | P1 | `BLOCKED_EXTERNAL` | V0 | No current observed five-minute child golden-path record | Private/safe observed session meets section 12 |
| `MA-RELEASE-001` | P1 | `FIXED_PENDING_VERIFICATION` | V3 integration commit plus failed remote static gate | Exact local full CI is green at historical `a3d3bce1`, and the resolved integration content committed as `ad36ee9f` exits zero after 826.4 seconds with all 63 current trusted probes. Exact-head GitHub run `31455723446` at `57bc08d1` then failed before import because the Opera generated-art checker required platform-identical PNG compression bytes; it did not report a gameplay/probe failure. A focused IDAT-only portability repair is locally green but still needs a committed replacement remote run, matching APK, and device acceptance | Commit the scoped checker/test/log repair, obtain a green remote exact-head probe run, then require matching build and device evidence at the eventual release candidate; rerun locally if runtime/static content changes |

### 5.2 P2/P3 and owner-decision indexed items

| ID | Severity | Lifecycle | Verification | Indexed issue / decision |
|---|---|---|---|---|
| `MA-VIS-004` | P2 | `REPORTED_UNCONFIRMED` | V1; `COVERAGE_GAP` | Current source-average figure/ground values are Fairy 0.039 vs 0.040 and Lagoon about 0.004, but the metric does not measure the rendered local state and cannot confirm an art defect. Closure requires true state-local Canvas/HUD/viewport/device evidence, not recoloring approved art to satisfy the average |
| `MA-ASSET-001` | P2 | `CONFIRMED_OPEN` | V1 | Current orphan PNG reports: Castle 9/15 at 2.1 MB, Galaxy 32/32 at 11.7 MB, Opera 453/548 at 166.5 MB, Lagoon 48/90 at 41.9 MB |
| `MA-ASSET-004` | P2 | `CONFIRMED_OPEN` | V1 | Lagoon has 10/41 NPOT textures, about 11.6 MB uncompressed residency cost |
| `MA-CI-002` | P2 | `FIXED_PENDING_VERIFICATION` | V2/current static | Local/remote blocking-loop parity now covers the new Opera Detective and gesture-quality probes: 63 local names versus 62 remote names, with display-only `probe_human_art_audit` the intended difference; default and stress parity audits are green |
| `MA-CI-003` | P2 | `CONFIRMED_OPEN` | V1 | All 105 probe scripts still need exactly one trusted/runtime-visual/advisory/diagnostic/obsolete/quarantined classification |
| `MA-ROSHAN-003` | P2 | `DEFERRED_WITH_REASON` | V1/V3 reported | Atlas repacking is an optimization; current owned-pixel windows and engine sampling probes are green |
| `MA-ROSHAN-004` | P2 | `DISMISSED_NOT_A_DEFECT` | V1 | Universal 2D costume layers are optional future design, not a missing required feature |
| `MA-PLAY-002` | P2 | `OWNER_DECISION_REQUIRED` | V1 | Standalone fire-arena reward/flag/medal role needs a truthful home or retirement |
| `MA-COMBAT-001` | P2 | `FIXED_PENDING_VERIFICATION` | V3 reported | Phone-only wave count, slash-band scale, and tutorial discoverability remain for device review |
| `MA-OPERA-003` | P2 | `CONFIRMED_OPEN` | V1/V4 partial | The grouped old pipe/echo/Nursery fallback claim is partially repaired by current authored pipe, echo, bottle, pat, and blanket behavior, but its unresolved subclaims have not yet been split and re-audited against accepted captures |
| `MA-OPERA-005` | P2 | `FIXED_PENDING_VERIFICATION` | V3 partial | The old Ballerina art/mechanic is superseded by the accepted 1024×1024 4×4 mermaid atlas and dedicated three-act full-stage recital; focused probes and the complete local integration gate are green. Closure still requires the remote exact-head gate, two-aspect capture, M11/child play, and owner identity/style acceptance |
| `MA-OPERA-006` | P2 | `CONFIRMED_OPEN` | V1/V3 partial | Nursery, Farmer, and Racer received material art-fiction repairs, but the grouped historical claim must be split and re-audited; remaining protected-voice mismatches stay open rather than being inferred fixed |
| `MA-OPERA-007` | P2 | `OWNER_DECISION_REQUIRED` | V1 | Farmer/Doctor above-water setting differs from the other Opera backdrops |
| `MA-AUDIO-001` | P2 | `FIXED_PENDING_VERIFICATION` | V3 partial | Forty-two unique deterministic area cues have complete score/render hashes, 48 kHz stereo OGG delivery, loop/import metadata, loudness/peak/seam measurements, routing ownership, and focused audio/full-branch evidence. Human style and two-wrap listening, voice-over intelligibility and ducking, mono fold-down, music-off transition review, and Lenovo Tab M11 start/loop/performance acceptance remain open |
| `MA-CHANGE-001` | P2 | `VERIFIED_FIXED` | V2/V3 process evidence | Twenty-three stable `CHG-*` records now partition 64 owned source commits and document seven merge-topology commits, covering all 71 reachable audit commits. Every record names paths, benefit, plausible harm, dependencies, evidence, gates, and rollback class. The planner imports no Git/filesystem mutation API; only CHG-020/021/022 can emit guarded stdout scripts, while the other 20 refuse automation. | Fourteen unit tests, exact ledger/catalog source parity, clean non-mutation CLI replay, Git-history checks, GAME2D no-regression, and independent adversarial approval are green. Future material changes must append under the stable ID or add the next ID; drift reopens this finding. |
| `MA-CODE-001` | P2 | `CONFIRMED_OPEN` | V1 | `main.gd` is 8,519 lines against the extraction-only <2,500 target |
| `MA-CODE-002` | P2 | `CONFIRMED_OPEN` | V1 | String state, duplicated input, save frequency, material churn, and remaining 3D glue are structural risks |

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
| `MA-OPERA-008` | P1 | `VERIFIED_FIXED` | V3 partial: focused runtime only | Racer finale requested a ride-selection recording for a circle gesture and could leave stale caption/fallback output | `e4528b27`; exact `op_racer_lap_two` pooled recording, hidden caption, quiet fallback, parser/lint, and focused Opera2D/voice/Opera probes; full CI at that checkpoint is not claimed |

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
| `EV-2D-014` | `MA-2D-002`, `MA-OPERA-008` | Reject the upstream device-only 3D kart restoration while retaining all newer Opera work | Current `7b5d1209` + `245c1613` reconciliation; shipping Racer has three Canvas phases, no external kart node/device split, exact `op_racer_lap_two` speech, passive rejection, completion, teardown, and re-entry coverage |

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
| `EV-CI-003` | `MA-CI-002`, `MA-RELEASE-001` | Integrate new Opera/art/music gates into both blocking environments | Integration commit `ad36ee9f`; local loop 63, remote headless loop 62, display-only human-art probe is the sole intended difference, and default/stress parity checks are green. The local full gate exits zero after 826.4 seconds with all 63. First exact-head execution `31455723446` at `57bc08d1` reached the shared static gate and failed there on cross-platform Opera PNG compression, so replacement exact-head verification remains open. |
| `EV-CI-004` | `MA-RELEASE-001`, `MA-CHANGE-001` | Diagnose and constrain the remote-only Opera generated-art false rejection | GitHub run `31455723446` plus focused local mutations: only recompression of an identical PNG scanline stream may differ; CRC-checked structure, all other chunks, mode, dimensions, pixels, semantic text, and checked-in delivery-byte provenance remain strict. All 39 local artifacts and positive/negative unit controls are green; introducing commit and replacement remote evidence remain pending. |
| `EV-CHANGE-001` | `MA-CHANGE-001` | Make the large audit program reviewable and reversions granular | `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md`, `tools/plan_audit_rollback.py`, and 14 unit tests; CHG-001–023 cover 64 uniquely owned source commits plus seven explicit topology commits, only CHG-020/021/022 emit guarded stdout scripts, all other groups refuse automation, CLI execution leaves Git status byte-identical, and independent adversarial review approves the catalog/history/safety contract |
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
| `EV-ASSET-001` | `MA-ASSET-004` | Lagoon texture residency measured by simultaneous use | `76c30a66` |
| `EV-ASSET-002` | `MA-ASSET-003`, `MA-ROSHAN-002` | Four clipped/debris playground frames replaced and licensed | `a1be9a1e`; all 41 current Lagoon runtime assets licensed |
| `EV-VOICE-001` | `MA-ACCESS-001` | Duplicate objective speech prevented | `17813082` |
| `EV-VOICE-002` | `MA-ACCESS-001` | Speech stops across skip/advance/clear/teardown | `c86d3a7d` |
| `EV-VOICE-003` | `MA-ACCESS-001` | Opera phase re-prompts retain speaker/cue identity | `8b5ca161` |
| `EV-VOICE-004` | `MA-ACCESS-001` | Shadowed duplicate voice-generator keys rejected | `1c6e0c24` |
| `EV-VOICE-005` | `MA-ACCESS-001` | Brawl prompts bind to one Huluu cue | `e8485d54` |
| `EV-ASSET-003` | `DL-ASSET-04` | Castle delivery provenance is newline-stable | `df5b4cf7` |
| `EV-CASTLE-001` | `DL-VIS-10`, `DL-SAVE-01`, `DL-INT-01` | Apply the child's saved Castle logo to every matching purple shell banner without stealing room input | `9e75e8e3` plus current integration; two Craft Room and two Stuffie Playroom replacements, Craft badge, saved color/symbol, no overlay in unregistered rooms, and focused interaction coverage |
| `EV-AUTH-001` | `MA-DOC-001`, `MA-DOC-002` | Reconcile current authority to true 2D while preserving the incomplete-ledger state | `9289dd81`; operational/design authorities updated; exhaustive 307-document classification remains open |
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
| 3D Opera bosses/outfits/rivals, 3D companion bodies, or Curve3D/Spline3 presentation prescriptions | `SUPERSEDED` | Preserve gameplay goals during tested 2D conversion |
| Device-only real-3D Opera kart with a headless/probe Canvas bypass | `SUPERSEDED` | Current Racer is one true-Canvas implementation on device and in probes; no external kart child or device-dependent medium split is accepted |
| `OPERA_MINIGAME_QUALITY_AUDIT_2026-08-09.md`'s 52-phase total and its old Ballerina, generic Boxer, and nested-kart Racer descriptions | `SUPERSEDED` in those scopes | Current shipping table is 13 careers/53 phases/27 modes; latest Ballerina, Boxer, and Canvas Racer authorities control while non-conflicting prop provenance/repairs remain supporting evidence |
| `OPERA_QUALITY_OVERHAUL_2026-08-09.md`'s 52-phase/19-mode/single-`bop` snapshot and requirement to loop every Ballerina row chronologically | `SUPERSEDED` in those scopes | Current Opera has 53 phases/27 modes/no generic `bop`; Ballerina frames are held pose keys because adjacent silhouette jumps are 41.6–47.3%, with only a one-shot curtain call |
| Earlier Ballerina atlas attempts, generic PHRASE/POSE/RIBBON/TWIRL route, or any leg/feet-like candidate | `SUPERSEDED` | `BALLERINA_PARTY_REBUILD_2026-08-09.md` and accepted generation `exec-a4dfa550-5374-43b6-a5e0-16a9d3d4b81c.png` control; prior leg/feet-like candidates remain rejected evidence, and the runtime atlas remains a one-tail mermaid at exact hash `c829784d4085e9cd9765cf0114a0f65bfe3f662ed8acc423223b726a0f003995` |
| Boxer manifest's retained `opera_boxer_outfit.glb`, `opera_boxer_dressing.glb`, and `opera_rival_boxer.glb` as useful runtime resources | `SUPERSEDED` | The Canvas specialist does not require them; while active they remain exact GAME2D transition debt and must retire through the normal tested archive path |
| Music audit's temporary retained `race` cue for an Opera nested kart | `SUPERSEDED` for current Opera Racer | There is no nested kart segment to own that cue; the Canvas Racer stays under its Opera career music unless a future separately approved Canvas transition says otherwise |
| Roshan 2D atlas repacking | `DEFERRED_WITH_REASON` | Optimization; current sampling contract is green |
| Universal costume layers | `DISMISSED_NOT_A_DEFECT` | Optional feature, not audit closure work |
| Gabby | `DISMISSED_NOT_IN_PROJECT` | IP hold under `attic/gabby/` only |
| Sparkle guide fish implementation | `DISMISSED_NOT_IN_PROJECT` | Wayfinding need survives through voice, pointers, landmarks, and helping current |
| Whole-card bounce/spin/hover as meaningful object action | `DISMISSED_NOT_IN_PROJECT` | Feedback only; interaction changes a truthful object part/state |
| Seek's vinyl `characters/stickers/pearl_friend.png` pair card and `assets/mg/k_bush2.png` preview art as active actors/environment | `SUPERSEDED` for Seek | `8fa90111`/`27bda85d` replace them with frame-animated Evie/Lamb-a' actors and approved high-grade tree cards; the protected friend source remains untouched and neither legacy file is globally reclassified outside this bounded runtime use |
| Old Opera request-list scope | `SUPERSEDED` | Later August 3–5 audits replace the older requested-work inventory |
| Opera DO-NOT-PROMOTE B1–B6 condition | `VERIFIED_FIXED` | `3e479e68` records closure of that bounded gate; later indexed issues remain separate |
| Chapter 2, daily rhythm, naming, gifting, tending, decorating, additional minigames | `DEFERRED_WITH_REASON` | Existing game, 2D conversion, and device evidence first |
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
  `MA-VIS-002`, `003`, `004`, and `006` remain open. Current clean-HEAD result
  is 16 FAIL, 17 REVIEW_OPEN, two MANUAL_OPEN, and 86 COVERAGE_GAP.
- **Evidence:** approved contract commits `3b7a7e66` and `fea916a8`, plus the
  clean fresh-runtime strict result and limitations in section 4.4. Saved or
  manual facts carry no PASS authority.
- **Repair:** fix the confirmed Lagoon mural with true Canvas/`Sprite2D`
  differential layers while preserving unique object ownership and seams;
  `SideScrollStage`, `Sprite3D`, or filename-only relabeling is not closure. For
  the palette items, first replace global source averages with true state-local
  Canvas/HUD composites emitted by implemented closed adapters. Change art only
  if that evidence confirms a defect and the owner accepts the correction;
  never recolor/regenerate approved art to satisfy the old metric. The current
  tool already validates occlusion per relevant live card and fails closed;
  product adapters must now produce the required live evidence.
- **Surrounding tests:** visual unit/stress/strict, scene congruency, resolution,
  seams, overdraw, ownership, Lagoon gameplay/re-entry, 1280×720 and wide-phone
  capture, M11 squint, owner review.
- **Acceptance:** true Canvas layers close the confirmed mural defect; pinned
  private fresh-runtime state-local evidence resolves each palette
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
- **Acceptance:** remote exact-head gate for the integrated audit branch,
  authoritative
  two-aspect Mobile capture, one-finger target-device comfort/performance and
  voice review, child comprehension, and owner identity/style acceptance.
  Boxer's three retained GLBs are separate `MA-2D-002` debt and cannot become a
  fallback for the Canvas specialist.

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
   exact Godot 4.7.1, refresh the shrink-only manifest, and prove no debt growth.
9. Run parser, lint, analyzer, import, static gates, and all trusted probes.
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

Every one of the current 105 probe scripts receives exactly one state:

- `TRUSTED_BLOCKING`
- `RUNTIME_VISUAL_BLOCKING`
- `ADVISORY_CAPTURE`
- `DIAGNOSTIC_TOOL`
- `OBSOLETE_DELETE`
- `QUARANTINED_WITH_REASON`

Local/remote blocking-loop parity is fixed locally under `MA-CI-002` and awaits
the exact-merge remote run; exhaustive classification remains separately open
as `MA-CI-003`.

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
      true 2D and exact Godot 4.7.1-stable.
- [ ] Every material indexed audit item has a linked complete canonical record
      containing all section-10 fields.
- [ ] The off-repository Alpha journal is imported or replaced by a fresh,
      equally scoped audit; unnamed reports are not assumed fixed or open.
- [ ] Visual stress is green and every applicable failure, review, manual item,
      and coverage gap has an explicit accepted disposition.
- [ ] Exact Godot 4.7.1-stable parser, lint, analyzer, fresh import, static
      gates, and all 63 current trusted local probes are green at one integrated
      commit. Historical `a3d3bce1` remains green for its then-current 61-probe
      suite; the resolved content committed as `ad36ee9f` completes the current
      full local gate in 826.4 seconds, but the remote exact-head run remains
      open.
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

Current result: **`IN_PROGRESS` / `UNSATISFIED`; the audit remains
`REPAIRING`, not `SATISFIED`.**

---

## 13. Current repair order

1. Keep the dedicated `codex/master-audit-20260809` branch synchronized; create
   the missing complete item records and finish the exhaustive 307-document
   ledger/document-control gate. Authority reconciliation itself is complete at
   `9289dd81`.
2. Continue one tested true-2D gameplay family from the exact 509-model/
   68-production-file inventory until every GAME2D
   category is zero; archive exact resources before active deletion.
3. Implement live fresh-runtime Canvas adapters, beginning with converted
   surfaces and then Fairy/Lagoon; keep every missing capture as a gap.
4. Verify the merged Ballerina, Boxer, Candymaker, and 42-cue music slices on
   the remote exact audit-branch head, then repair remaining Opera capture coverage and split
   the stale grouped Opera art claims. Continue with the confirmed Lagoon
   Canvas-layer defect. Confirm or dismiss palette risks only from current
   state-local evidence.
5. Reconcile protected voice gaps, including Evie's exact Seek tap-tree cue,
   through owner-authorized sources.
6. Rebuild and prove the complete child-visible world graph.
7. Classify all probes and remove only proved obsolete assets/code.
8. Preserve both the exact `a3d3bce1` historical full gate and the 826.4-second
   `ad36ee9f` integration local gate; run the 62-probe remote suite at the exact
   current audit-branch SHA (and rerun local if runtime/static content changes),
   then produce the capture matrix, matching APK, target-device U0 pass, audio
   listening matrix, and child golden path.
9. Repeat the master audit from `INVENTORYING`; satisfaction cannot come from
    closing only the first list.

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
| 2026-08-10 | `REPAIRING` | Reconciliation rejects the upstream device-only real-3D kart path and preserves the one-implementation Canvas Racer with exact `op_racer_lap_two` speech. Merge commit `ad36ee9f` integrates `7b5d1209` and `245c1613`; remote exact-head verification remains open. |
| 2026-08-10 | focused `VERIFYING` | The resolved integration content committed as `ad36ee9f` completes exact Godot 4.7.1 `scripts/ci.sh` in 826.4 seconds with fresh import, all static gates, GAME2D `NO_REGRESSION`, and all 63 current trusted local probes green. Remote exact-head CI remains pending; strict 2D, visual, audio-listening, device, child, and owner gates stay open. |
| 2026-08-10 | `REPAIRING` | Exact-head GitHub run `31455723446` at process commit `57bc08d1` fails before import in `prepare_opera_minigame_art.py --check-only`: Linux and Windows reproduce identical RGBA pixels but not identical PNG compression bytes. CHG-015 is widened with an IDAT-only comparison repair and strict chunk/mode/size/scanline/pixel/delivery-hash negative controls; the replacement exact-head run remains pending. |

No later state is added without its required evidence.
