# Mermaid Roshan: Reef of Light — game-wide master audit

- **Audit ID:** `MA-2026-08-09`
- **Audit date:** 2026-08-09
- **Audited branch:** `codex/master-audit-20260809`
- **Synchronized code commit:** `e4528b27e2552f669de2b65c37da0243fb924eac`
- **Proposed design authority:** `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`
- **Document authority:** `PROPOSED_CANONICAL`
- **Overall cycle state:** `REPAIRING` with concurrent focused `VERIFYING`
- **Satisfaction:** **NOT SATISFIED**

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

At synchronized commit `e4528b27`, the exact game-wide scanner measures:

```text
GAME2D| model_files=513
GAME2D| model_scan_coverage_files=0
GAME2D| active_export_model_files=513
GAME2D| model_import_sidecars=157
GAME2D| active_untracked_model_import_sidecars=356
GAME2D| model_archive_files=0
GAME2D| production_3d_files=70
GAME2D| probe_3d_files=80
GAME2D| scene_3d_files=1
GAME2D| configuration_3d_files=1
GAME2D| archive_now_model_files=0
GAME2D| STATUS=UNSATISFIED
```

The Opera racer conversion at `82124b3a` reduced production 3D-file debt from
72 to 71. The medal spatial-scoreboard retirement at `8ed978be` reduced it from
71 to 70. The guarded manifest shrink at `344d8d5c` removed both stale entries,
and the exact default audit at `e4528b27` exits zero with no manifest finding.
The 513 retained model-resource count did not change. Default-mode exit zero
proves an exact inventory, not a satisfied 2D game; strict remains red while any
reported debt category is nonzero.

The current visual audit reports:

```text
VISUALAUDIT| ERROR=3  WARN=16  MANUAL=2  INFO=119  SKIP=83
VISUALAUDIT| STATE FAIL=3  REVIEW_OPEN=16  MANUAL_OPEN=2
VISUALAUDIT|       COVERAGE_GAP=83  WAIVED=0  PASS=35
VISUALAUDIT|       NOT_APPLICABLE=84  RESULT=UNSATISFIED
```

The three current visual-tool `ERROR` diagnostics reproduce:

1. Fairy Pond background saturation exceeds its foreground/tap-target set.
2. Sky Lagoon is one mural layer across twelve tiles rather than a real 2D
   parallax stack.
3. Sky Lagoon background saturation exceeds its foreground/tap-target set.

Only item 2 is a confirmed product defect. The Fairy palette diagnostic is
probably a checker false positive or coverage gap, and the Lagoon palette
diagnostic is a plausible hierarchy risk but not a confirmed art defect. Their
global source averages equally weight mutually exclusive/decorative files and
ignore the rendered state-local composite, HUD, viewport, and device. Approved
art must not be recolored or regenerated merely to make that metric green.

The former dimensional-rollback error, four playground-license errors, and
four clipped/debris playground frames are no longer current failures. They must
not be copied back into the active triage index.

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

1. Direct owner decision, 2026-08-09: remove 3D Mermaid Roshan; the game is
   true 2D; active 3D resources belong only on the deprecated-resources branch.
2. `SECURITY.md`, protected-asset/save rules, exact Godot 4.7.1-stable rules,
   and release workflow in `AGENTS.md`, excluding its stale 3D clauses.
3. `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` once tracked and reconciled.
4. A current domain document within its explicitly retained scope.
5. Historical audits and work orders as evidence only.

### 3.2 Current authority map

| Source | State | Scope |
|---|---|---|
| Owner's 2026-08-09 true-2D directions | `OWNER_DECISION` | Highest-precedence medium and resource-retirement decision |
| This audit | `PROPOSED_CANONICAL` | Audit-item states, evidence, closure, and history for this round; section 5 remains an index until full records exist |
| `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` | `PROPOSED_CANONICAL` | Stable `DL-*` rules and acceptance contract |
| `AGENTS.md` except named stale 3D passages | `BINDING_OPERATIONAL` | Engine, security, save, protected art, workflow, and release rules |
| `SECURITY.md` | `BINDING_OPERATIONAL` | Threat model and protected data |
| `WORKFLOW_BRANCHING_2026-07-18.md` | `BINDING_OPERATIONAL` | Dev/master promotion process |
| `ASSET_LICENSES.md` | `BINDING_LEDGER` | Current and historical asset provenance |
| `tools/audit_game_2d.py`, manifest, and tests | `BINDING_DOMAIN` | Exact shrinking-debt inventory and zero-debt enforcement |
| `tools/audit_roshan_2d.py` and tests | `BINDING_DOMAIN` | Narrow no-model Roshan enforcement; not whole-game 2D satisfaction |
| `tools/audit_roshan_sprite_clipping.py` and current frame roster | `BINDING_DOMAIN` | 2D source-frame cutoff/ghost/import contract |
| Current cinematic protocols and `tools/audit_cinematic.py` | `BINDING_DOMAIN` | Full-frame cinematic-only delivery |
| `VISUAL_AUDIT_TOOL.md` methodology | `SUPPORTING_CURRENT` | Falsifiability and explicit unresolved evidence; its Sprite3D allowance is stale |
| `codex/deprecated-resources-roshan-20260809` at `9329d9a6` | `HISTORICAL_EVIDENCE` | Exact archived 3D resources; never a production fallback or merge source |

### 3.3 Design-language confirmation state

The proposed comprehensive design language is based on the current owner
decision and triage of prior masters, audits, repair records, art rules,
touch/voice/save contracts, and current machine evidence. Its child, visual,
interaction, motion, audio, cinematic, performance, save, provenance, and QA
rules are current.

It remains `PROPOSED_CANONICAL` until:

- it and this audit are tracked through the narrow `.gitignore` exception;
- `design/00` through `design/05`, `AGENTS.md`, `CLAUDE.md`, and active domain
  documents are reconciled in an explicitly authorized later slice;
- the documentation ledger covers every tracked Markdown path;
- a documentation gate proves references, statuses, and forbidden current 3D
  claims are consistent.

This proposed status does not weaken the direct owner decision. It prevents an
untracked draft from falsely claiming completed repository-wide reconciliation.

---

## 4. Evidence at synchronized commit

### 4.1 Repository snapshot

| Fact | Result |
|---|---:|
| Tracked Markdown files, excluding these two untracked drafts | 296 |
| Expected tracked Markdown count once both drafts are added | 298 |
| `scripts/main.gd` | 8,465 lines |
| GDScript files under `scripts/` | 187 |
| `scripts/probe_*.gd` files | 103 |
| Names in the local trusted loop | 61 |
| Names in the remote headless trusted loop | 60 |

The sole intended loop difference is the display-only
`probe_human_art_audit`; `probe_opera_pipe` remains in both blocking loops.

### 4.2 Game-wide true-2D gate

#### 4.2.1 Full checkpoint at `344d8d5c`

```text
GODOT=<exact Godot 4.7.1-stable binary> scripts/ci.sh
exit 0
61 trusted local probes reached accepted verdicts
GAME2D unit contract: 73 tests OK
GAME2D stress contract: 14 falsification/control assertions ALL OK
GAME2D regression gate: NO_REGRESSION at 513 models / 70 production files
```

This is the most recent exact full parser/lint/import/static-gate/trusted-probe
checkpoint. It verifies `MA-2D-003`: the guarded manifest at `344d8d5c` matches
the Opera and medal shrink, and the stale-entry failure is gone. The full suite
does not make the game 2D: `NO_REGRESSION` explicitly means the exact baseline
did not grow while strict debt remains.

The self-tests prove the scanner can fail for model payloads, disguised files,
archives, sidecars, runtime APIs, dynamic loaders, custom data, native/plugin
sources, scene/config debt, incomplete history, and dishonest refreshes.

#### 4.2.2 Focused current-HEAD evidence at `e4528b27`

Only the following current-HEAD evidence is claimed:

```text
python -m gdtoolkit.parser scripts/audio_director.gd scripts/opera_career_world_2d.gd scripts/probe_opera_2d.gd
PASS

python tools/lint_inference.py scripts/audio_director.gd scripts/opera_career_world_2d.gd scripts/probe_opera_2d.gd
PASS

<Godot 4.7.1-stable> --headless -s scripts/probe_opera_2d.gd
ALL OK

<Godot 4.7.1-stable> --headless -s scripts/probe_voice.gd
ALL OK

<Godot 4.7.1-stable> --headless -s scripts/probe_opera.gd
ALL OK

python -B tools/audit_game_2d.py
exit 0
GAME2D| DEBT| model_files=513| model_scan_coverage_files=0| active_export_model_files=513| model_import_sidecars=157| active_untracked_model_import_sidecars=356| model_archive_files=0| production_3d_files=70| probe_3d_files=80| scene_3d_files=1| configuration_3d_files=1| archive_now_model_files=0
GAME2D| STATUS| UNSATISFIED
```

Default-audit exit zero proves that the current inventory exactly matches the
guarded shrinking manifest. It is not `NO_REGRESSION`, `PASS`, or strict
satisfaction. No exact full `scripts/ci.sh` run is claimed at `e4528b27`; the
`344d8d5c` full checkpoint cannot be inherited across the voice/caption change.

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
- `archive_now_model_files=0` means no further retained model is currently
  proved removable solely as an orphan. It does not mean the remaining 513 are
  accepted; further removal requires tested 2D conversion or new dependency
  proof.

No protected file under `assets/book/`, `assets/audio/voices/`, or
`assets/characters/friends/` was modified by these retirements.

### 4.4 Static visual audit with partial, unpinned runtime facts

Command:

```text
python -B tools/audit_visual_design.py -v --no-report
```

The most recent local result is `3 ERROR / 16 WARN / 2 MANUAL / 119 INFO / 83
SKIP`, overall `UNSATISFIED`. It is not commit-pinned runtime evidence.

The 16 review-open warnings comprise current orphan-art reports, eight Lagoon
duplicate-generation families, Lagoon engine-layer bypass, Fairy/Lagoon weak
figure-ground luminance, and Lagoon NPOT residency cost. The two manual items
are Fairy and Lagoon phone/M11 squint reviews. The 83 skips are coverage gaps,
not passes.

The audit consumes ignored `audit/visual_runtime_facts.json`. That local file
covers only Reef and Sky Lagoon, embeds no commit, Godot version, build, or
capture provenance, and supplies no Reef target facts. Therefore these totals
are useful V1 static triage plus partial unpinned runtime input, not reproducible
exact-HEAD V3 evidence or visual closure.

The current palette/figure-ground implementation averages source files rather
than a true state-local Canvas composite. It equally weights mutually exclusive
states and decorative art, whether or not they render together, and omits HUD,
viewport, local effects, and device presentation. Fairy's saturation error is
therefore likely a false positive/coverage gap. Lagoon remains a plausible
hierarchy risk, but the current metric cannot confirm an art defect. A separate
visual evidence-contract repair is in flight outside this synchronized snapshot
and is not pre-credited here.

The visual manifest's `overhead_canvas` claim for Fairy is also false current
metadata: Fairy runtime and its probe still enforce 3D presentation. That debt
belongs to `MA-2D-002`; the label is not evidence of Canvas completion.

### 4.5 Evidence not claimed

- No exact full `scripts/ci.sh` result is claimed at current HEAD `e4528b27`;
  the exact exit-zero full checkpoint is `344d8d5c` only.
- No current-HEAD strict GAME2D run or zero-debt result is claimed.
- No complete runtime capture matrix is claimed.
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
| `MA-2D-002` | P1 | `IN_PROGRESS` | V2/V3 partial | Section 1 records 513 model/export files, 157 tracked model sidecars, 356 active untracked sidecars, 70 production 3D files, 80 probe 3D files, one 3D scene, and one 3D configuration; scan-coverage, model-archive, and archive-now counts are zero. Current player and Fairy runtime/probe staging still enforce legacy 3D | All eleven GAME2D categories reach zero; strict gate, import, focused/surrounding/full probes green |
| `MA-DOC-001` | P1 | `CONFIRMED_OPEN` | V1 | Current authority documents still prescribe 2.5D/Sprite3D/real-3D/model work | Authorized reconciliation plus documentation gate |
| `MA-DOC-002` | P1 | `CONFIRMED_OPEN` | V1 | The old document ledger is incomplete and lacks exact partial-supersession scope | Exhaustive unique row for every tracked Markdown path |
| `MA-DOC-003` | P1 | `BLOCKED_EXTERNAL` | V1 | An off-repository journal is said to hold 36 unnamed entries described as findings | Import source evidence or replace with fresh equal-scope audit; do not assume the entries are current |
| `MA-DOC-004` | P1 | `IN_PROGRESS` | V1 | The master-audit draft was hidden by broad `/audit/` ignore behavior, while both proposed documents remain untracked and unindexed | Narrow ignore exception, tracked documents, status/reference checks |
| `MA-DOC-005` | P1 | `CONFIRMED_OPEN` | V1 | Material active audit items do not yet have linked full canonical records containing every section-10 field | Create and validate one complete linked record per material active item before calling it a canonical finding or starting its next repair |
| `MA-VIS-002` | P1 | `CONFIRMED_OPEN` | V1 | Sky Lagoon remains one mural layer across twelve tiles | True Canvas/`Sprite2D` differential layers with seams/ownership/overdraw green and runtime/device review; `SideScrollStage`, `Sprite3D`, or filename-only relabeling cannot close it |
| `MA-VIS-003` | P1 | `REPORTED_UNCONFIRMED` | V1; `REVIEW_OPEN` | Reproduced source-average saturation diagnostics flag Fairy and Lagoon, but Fairy is probably a false positive/coverage gap and Lagoon is only a plausible hierarchy risk | True state-local Canvas composite with HUD/viewport/runtime/device evidence; do not recolor or regenerate approved art merely to satisfy the current average |
| `MA-VIS-006` | P1 | `CONFIRMED_OPEN` | V1 plus unpinned partial runtime facts | Visual audit retains 83 coverage gaps and two manual reviews | Commit-pinned applicable facts generated; every SKIP/MANUAL explicitly resolved |
| `MA-PLAY-001` | P1 | `CONFIRMED_OPEN` | V1/V3 partial | No end-to-end fresh-save, child-visible, no-cheat world reachability proof exists | Enter/leave/re-enter every visible destination without direct debug calls; save/seam/touch/voice checks |
| `MA-ACCESS-001` | P1 | `BLOCKED_EXTERNAL` | V1 | Required exact voice cues remain absent for some objectives | Authorized exact recordings or independently sufficient spoken/diegetic design; playback/device/child evidence |
| `MA-ACCESS-002` | P1 | `BLOCKED_EXTERNAL` | V1 | Lamba's current semantic role still maps to legacy “bunny-fish” recordings | Owner-approved re-record/re-render and exact-key/device listening evidence |
| `MA-TOUCH-001` | P1 | `FIXED_PENDING_VERIFICATION` | V3 reported | Held travel/medallion path lacks real-phone hold/drag/multitouch/focus-loss evidence | Recorded target-phone pass |
| `MA-OPERA-001` | P1 | `CONFIRMED_OPEN` | V4 partial | Chef BAKE/POUR art retains named cutoff/fallback/wrong-object defects | Approved art and full two-aspect capture matrix |
| `MA-OPERA-002` | P1 | `CONFIRMED_OPEN` | V4 partial | Detective's “missing” crown remains painted into the scene evidence | Healed owned source, narrative/capture verification |
| `MA-OPERA-004` | P1 | `CONFIRMED_OPEN` | V1 | Opera capture harness has not produced accepted evidence for all careers | Repair harness; capture and human-review all careers/widgets/scuffles/stress states |
| `MA-PERF-001` | P1 | `BLOCKED_EXTERNAL` | V0 | No current target-device frame-time, hitch, memory, thermal, or latency matrix | U0 device matrix at exact release candidate meets design thresholds |
| `MA-CHILD-001` | P1 | `BLOCKED_EXTERNAL` | V0 | No current observed five-minute child golden-path record | Private/safe observed session meets section 12 |
| `MA-RELEASE-001` | P1 | `FIXED_PENDING_VERIFICATION` | V3 checkpoint only | Full CI is green at `344d8d5c`, but no same-SHA full suite, APK, or device acceptance is recorded at current HEAD `e4528b27` | Same-SHA analyzer/import/full probes/build/device evidence |

### 5.2 P2/P3 and owner-decision indexed items

| ID | Severity | Lifecycle | Verification | Indexed issue / decision |
|---|---|---|---|---|
| `MA-VIS-004` | P2 | `REPORTED_UNCONFIRMED` | V1; `COVERAGE_GAP` | Current source-average figure/ground values are Fairy 0.039 vs 0.040 and Lagoon about 0.004, but the metric does not measure the rendered local state and cannot confirm an art defect. Closure requires true state-local Canvas/HUD/viewport/device evidence, not recoloring approved art to satisfy the average |
| `MA-VIS-005` | P2 | `CONFIRMED_OPEN` | V1 | Occlusion audit passes when only 1/6 depth roles overlap; validate every relevant 2D card |
| `MA-ASSET-001` | P2 | `CONFIRMED_OPEN` | V1 | Current orphan PNG reports: Castle 2.1 MB, Galaxy 11.7 MB, Opera 163.7 MB (458/494 PNGs), Lagoon 47.3 MB |
| `MA-ASSET-004` | P2 | `CONFIRMED_OPEN` | V1 | Lagoon has 10/41 NPOT textures, about 11.6 MB uncompressed residency cost |
| `MA-CI-002` | P2 | `CONFIRMED_OPEN` | V1 | All 103 probe scripts need one trusted/advisory/diagnostic/obsolete/quarantined classification |
| `MA-ROSHAN-003` | P2 | `DEFERRED_WITH_REASON` | V1/V3 reported | Atlas repacking is an optimization; current owned-pixel windows and engine sampling probes are green |
| `MA-ROSHAN-004` | P2 | `DISMISSED_NOT_A_DEFECT` | V1 | Universal 2D costume layers are optional future design, not a missing required feature |
| `MA-PLAY-002` | P2 | `OWNER_DECISION_REQUIRED` | V1 | Standalone fire-arena reward/flag/medal role needs a truthful home or retirement |
| `MA-COMBAT-001` | P2 | `FIXED_PENDING_VERIFICATION` | V3 reported | Phone-only wave count, slash-band scale, and tutorial discoverability remain for device review |
| `MA-OPERA-003` | P2 | `CONFIRMED_OPEN` | V1/V4 partial | Authored pipe/echo/Nursery-care art gaps still use fallbacks |
| `MA-OPERA-005` | P2 | `CONFIRMED_OPEN` | V1 | Ballerina remains the named uniqueness outlier pending full capture |
| `MA-OPERA-006` | P2 | `CONFIRMED_OPEN` | V1 | Named Nursery/Farmer/Racer/voice-oval art-fiction mismatches remain |
| `MA-OPERA-007` | P2 | `OWNER_DECISION_REQUIRED` | V1 | Farmer/Doctor above-water setting differs from the other Opera backdrops |
| `MA-CODE-001` | P2 | `CONFIRMED_OPEN` | V1 | `main.gd` is 8,465 lines against the extraction-only <2,500 target |
| `MA-CODE-002` | P2 | `CONFIRMED_OPEN` | V1 | String state, duplicated input, save frequency, material churn, and remaining 3D glue are structural risks |

### 5.3 Resolved indexed items retained for anti-regression history

| ID | Severity | Lifecycle | Verification | Indexed issue | Closure evidence |
|---|---|---|---|---|---|
| `MA-2D-003` | P2 | `VERIFIED_FIXED` | V2/V3 | Opera and medal conversions left stale production-file entries in the shrink-only manifest | `344d8d5c`; guarded manifest refresh, exact full CI exit 0, GAME2D 73-unit/14-stress contracts, and `NO_REGRESSION` at 513/70 |
| `MA-ASSET-003` | P1 | `VERIFIED_FIXED` | V1/V3 reported | Four current Sky Lagoon playground assets lacked complete license-ledger coverage | `a1be9a1e`; all 41 current Lagoon runtime assets licensed and roster/audit gates updated |
| `MA-ROSHAN-002` | P1 | `VERIFIED_FIXED` | V1/V3 reported | Two playground poses were genuinely clipped and two intact poses retained detached edge debris | `a1be9a1e`; exact replacements, pixel/import/runtime/Mobile-render checks, and clipping-audit tests |
| `MA-OPERA-008` | P1 | `VERIFIED_FIXED` | V3 partial: focused runtime only | Racer finale requested a ride-selection recording for a circle gesture and could leave stale caption/fallback output | `e4528b27`; exact `op_racer_lap_two` pooled recording, hidden caption, quiet fallback, parser/lint, and focused Opera2D/voice/Opera probes; current-HEAD full CI is not claimed |

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
| `EV-OPERA-001` | `MA-OPERA-008`, `MA-RELEASE-001` | Use exact racer circle recording and prevent stale caption/yay fallback | `e4528b27`; parser/lint plus exact Godot 4.7.1 Opera2D, voice, and Opera probes all green; current-HEAD full CI not run |

The archive branch name retains “roshan” for history but is the preservation
authority only for resources already archived there. It is never an active
source, fallback, rollback target, or claim that reachable 3D debt is retired.

### 6.2 Other child-safety and quality evidence

| Evidence ID | Related item/rule | Evidence scope | Checkpoint and result |
|---|---|---|---|
| `EV-PLAY-002` | `MA-PLAY-001` | Companion boo-boos wait without removal, blocking, or lost legacy progress | `0522d1fa`; stuffie/load coverage |
| `EV-TOUCH-001` | `MA-TOUCH-001` | Snowman coal touch controls meet `StorybookUI.MIN_TOUCH` | `82f9828c`; `probe_mg2d` |
| `EV-CI-001` | `MA-CI-002` | Trusted local/remote probe parity and Opera-pipe coverage | `7e6d699d`; clean plus drift mutations |
| `EV-PLAY-003` | `MA-PLAY-001` | Visible, voiced Lagoon→Reef route and Pause fallback | `986010c0`; focused/re-entry/sibling probes |
| `EV-ROSHAN-001` | `MA-ROSHAN-002` | Playground/animal completion settles visible Roshan art | `711879ec`; Lagoon probes |
| `EV-CIN-001` | `DL-CIN-12` | Cinematic orientation/aspect/SAR/rotation blocking | `b50f2477`; focused cinematic unit suite |
| `EV-VIS-001` | `MA-VIS-006` | Visual audit preserves explicit unresolved-evidence states | `219fe593`; strict blocks review/manual/coverage gaps |
| `EV-VIS-002` | `MA-VIS-006` | Lagoon touch facts use real hit diameter | `6e04706d` |
| `EV-VIS-003` | `MA-VIS-002`, `MA-VIS-003` | Lagoon active-art/congruency evidence corrected | `09027504` |
| `EV-ASSET-001` | `MA-ASSET-004` | Lagoon texture residency measured by simultaneous use | `76c30a66` |
| `EV-ASSET-002` | `MA-ASSET-003`, `MA-ROSHAN-002` | Four clipped/debris playground frames replaced and licensed | `a1be9a1e`; all 41 current Lagoon runtime assets licensed |
| `EV-VOICE-001` | `MA-ACCESS-001` | Duplicate objective speech prevented | `17813082` |
| `EV-VOICE-002` | `MA-ACCESS-001` | Speech stops across skip/advance/clear/teardown | `c86d3a7d` |
| `EV-VOICE-003` | `MA-ACCESS-001` | Opera phase re-prompts retain speaker/cue identity | `8b5ca161` |
| `EV-VOICE-004` | `MA-ACCESS-001` | Shadowed duplicate voice-generator keys rejected | `1c6e0c24` |
| `EV-VOICE-005` | `MA-ACCESS-001` | Brawl prompts bind to one Huluu cue | `e8485d54` |
| `EV-ASSET-003` | `DL-ASSET-04` | Castle delivery provenance is newline-stable | `df5b4cf7` |

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
| Roshan 2D atlas repacking | `DEFERRED_WITH_REASON` | Optimization; current sampling contract is green |
| Universal costume layers | `DISMISSED_NOT_A_DEFECT` | Optional feature, not audit closure work |
| Gabby | `DISMISSED_NOT_IN_PROJECT` | IP hold under `attic/gabby/` only |
| Sparkle guide fish implementation | `DISMISSED_NOT_IN_PROJECT` | Wayfinding need survives through voice, pointers, landmarks, and helping current |
| Whole-card bounce/spin/hover as meaningful object action | `DISMISSED_NOT_IN_PROJECT` | Feedback only; interaction changes a truthful object part/state |
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

- **State:** three P1 and two P2 indexed items remain open; V1 plus unpinned,
  partial runtime facts.
- **Evidence:** current local visual output and limitations in section 4.4.
- **Repair:** fix the confirmed Lagoon mural with true Canvas/`Sprite2D`
  differential layers while preserving unique object ownership and seams;
  `SideScrollStage`, `Sprite3D`, or filename-only relabeling is not closure. For
  the palette items, first replace global source averages with true state-local
  Canvas/HUD composites. Change art only if that evidence confirms a defect and
  the owner accepts the correction; never recolor/regenerate approved art to
  satisfy the old metric. Validate occlusion per relevant card, not by one
  aggregate depth value.
- **Surrounding tests:** visual unit/stress/strict, scene congruency, resolution,
  seams, overdraw, ownership, Lagoon gameplay/re-entry, 1280×720 and wide-phone
  capture, M11 squint, owner review.
- **Acceptance:** true Canvas layers close the confirmed mural defect; pinned
  state-local evidence resolves the palette `REVIEW_OPEN`/`COVERAGE_GAP`; no
  applicable failure/review/manual/coverage gap and no new seam, duplicate,
  cutoff, ownership, touch, or performance defect.

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

### MA-ACCESS-001/002 — protected voice gaps

- **State:** P1, `BLOCKED_EXTERNAL`, V1.
- **Repair:** do not modify protected family recordings. Obtain authorized exact
  recordings/re-rendering, or explicitly redesign a cue so spoken and diegetic
  channels independently communicate the objective.
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

- Preserve stress-first ordering and complete-evidence strict semantics.
- Replace stale rule citations with stable `DL-*` IDs.
- Treat Sprite3D/Node3D presentations as transition debt, not valid final 2D.
- Inventory all current player-visible zones; 83 skips cannot close the game.
- Validate occlusion per relevant card/role.
- Generate commit/Godot/build-pinned, state-local Canvas/HUD runtime facts at
  appropriate viewports and aspect ratios; do not infer a rendered palette from
  equal-weight source averages.
- Correct Fairy's false `overhead_canvas` metadata only when evidence matches
  runtime; relabeling its current 3D implementation cannot close `MA-2D-002`.
- Resolve every `MANUAL`, applicable `SKIP`, and `REVIEW_OPEN`; never convert
  missing evidence to pass.

### 11.2 Probe classification

Every one of the current 103 probe scripts receives exactly one state:

- `TRUSTED_BLOCKING`
- `RUNTIME_VISUAL_BLOCKING`
- `ADVISORY_CAPTURE`
- `DIAGNOSTIC_TOOL`
- `OBSOLETE_DELETE`
- `QUARANTINED_WITH_REASON`

Local/remote blocking-loop parity is verified; exhaustive classification is
still `MA-CI-002`.

### 11.3 Documentation control

A later authorized reconciliation must:

- update `AGENTS.md`/`CLAUDE.md` and `design/00` through `design/05` without
  weakening their valid security/save/protected-art/workflow rules;
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
- [ ] Exact Godot 4.7.1-stable parser, lint, analyzer, import, and every trusted
      probe are green at the same commit.
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

Current result: **not complete; the audit remains `REPAIRING`, not
`SATISFIED`.**

---

## 13. Current repair order

1. Track this audit/design-language slice, create the missing complete item
   records, then explicitly authorize and reconcile older authority/index/
   ledger documents.
2. Continue one tested true-2D gameplay family from the exact 513-model/
   70-production-file inventory until every GAME2D
   category is zero; archive exact resources before active deletion.
3. Repair Opera capture coverage and named current art defects.
4. Repair the confirmed Lagoon Canvas-layer defect; generate state-local
   evidence to confirm or dismiss Fairy/Lagoon palette reports; then resolve
   per-card occlusion and remaining visual evidence gaps.
5. Reconcile protected voice gaps through owner-authorized sources.
6. Rebuild and prove the complete child-visible world graph.
7. Classify all probes and remove only proved obsolete assets/code.
8. Run an exact current-HEAD full suite, capture matrix, target-device U0 pass,
   and child golden path.
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
| 2026-08-09 | focused `VERIFYING` | `e4528b27` binds the racer circle phase to exact `op_racer_lap_two` speech and clears stale caption/fallback behavior; parser, lint, Opera2D, voice, Opera, and default GAME2D audit are green, but no current-HEAD full CI is claimed |

No later state is added without its required evidence.
