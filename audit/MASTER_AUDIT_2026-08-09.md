# Mermaid Roshan: Reef of Light — game-wide master audit

- **Audit ID:** `MA-2026-08-09`
- **Audit date:** 2026-08-09
- **Audited branch:** `codex/audit-reconcile-20260812`
- **Latest CI-repair checkpoint:**
  `af4189a99cfd5a32d0df0f75185f6912d3889399`
- **Current local merge-integration commit:**
  `f3b0de078898a8b4faddb2c738c4403180eff928` (parents
  `ea6185fdb1a687a20a6d118bdc368400e2c30f60` and
  `5f58ef0a9db7aa9593f85131e1b855e51b84aea8`)
- **Last completed full local checkpoint:**
  `f3b0de078898a8b4faddb2c738c4403180eff928`
- **Last historical exact-head remote checkpoint:**
  `dacef1405b6a8cb470117e824aebac3a8ca500af`, GitHub run `31457593351`
- **Latest exact-head remote verification:**
  `af4189a99cfd5a32d0df0f75185f6912d3889399`, GitHub run `31649113587`;
  both required jobs succeed.
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

The display/forced-2D Racer path is a true-Canvas three-phase activity. Its
`RACE` phase uses the same Canvas surface, a `circle` gesture, no widget, goal
`0.9`, and exact `op_racer_lap_two` speech. This is not yet the only source
path: ordinary headless startup still selects the legacy Opera lobby, and
`opera_act.gd` can still load `scripts/kart.gd` and attach an external kart
child. That retained lifecycle is open as `MA-OPERA-010` and game-wide debt as
`MA-2D-002`; the forced-2D probe path cannot certify it away. The music program
adds **42 deterministic area cues**
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
| Game-wide 2D scanner and archive | Made every model/sidecar/3D API measurable, fail-closed, and shrink-only; archived verified retired bytes | The result is still 509 models and 68 production-3D files, so green regression mode means “did not get worse,” never “finished” | `CHG-008`, `CHG-009` |
| Dolls catcher | Rebuilt Faron's catcher as a bounded Canvas activity with real routed drag, safe misses, passive rejection, save, replay, and teardown | Exact objective voice, M11, observed child, and owner capture acceptance remain | `CHG-012` |
| Seek / Evie and Lamb-a' | This was **not** a wholesale import of the old 3D game. The useful hide-and-seek loop was rebuilt as a fourteen-node Canvas meadow; vinyl/static actors and low-grade `k_bush2` presentation were replaced by frame-swapped Evie/Lamb-a' art and approved meadow/tree art; four meadow GLBs were retired | The exact Evie “tap the wiggly tree” recording is missing; generated identity/motion and device/child acceptance remain open | `CHG-013`; voice debt `MA-ACCESS-003` |
| Opera Racer | Display/device play now uses the three-phase Canvas circle activity and exact lap-two cue | Ordinary unforced headless startup still retains a legacy lobby to `scripts/kart.gd`; this is explicit `MA-OPERA-010`, not hidden by the forced-2D probe | `CHG-010`, `CHG-024` |
| Opera specialists and art | Integrated the current 13-career/53-phase/27-mode table, 208 reviewed Roshan cells, dedicated Ballerina and Boxer surfaces, phone-safe Candymaker, diegetic rooms, and deterministic music | Several careers still need state-complete captures, exact speech, device/child review, and removal of retained 3D source paths | `CHG-016`–`CHG-020`, `CHG-024` |
| Castle logo presentation | Replaced the matching painted shell banners with the child's saved Canvas logo without stealing input | Castle rooms themselves remain spatial; personalization is not a Castle-wide 2D pass | `CHG-021`, `CHG-024` |
| Visual evidence contract | Replaced easy-to-forge palette/capture claims with fresh runtime, source-bound, fail-closed evidence rules | Current live Canvas adapters are incomplete, so 16 failures and 86 coverage gaps remain rather than becoming false passes | `CHG-006`, `CHG-014` |
| CI, master documents, and rollback control | Reconciled newer development work with the audit, ran exact 4.7.1 local/remote gates, and created stable `CHG-*` records with guarded rollback planning | This controls change; it does not itself prove APK, device, child, owner, listening, visual, or strict-2D acceptance | `CHG-005`, `CHG-011`, `CHG-015`, `CHG-022`–`CHG-025` |

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
| QA and release automation | **4/5** | Exact 4.7.1 analyzer, 64 local/63 remote probe roster, import/boot gates, deterministic art/music, regression and falsification controls are unusually strong | Classify all 106 probes, complete live visual adapters, build the matching APK, and keep final branch-head CI green |
| Architecture and maintainability | **2/5** | Satellites and bounded surfaces demonstrate safe extraction patterns | `main.gd` and string-owned state remain large; 68 production-3D files and ordinary-headless Opera divergence keep change risk high |
| Provenance, protected assets, and rollback | **4/5** | Protected sources stayed untouched; licences, archive proof, 25 stable change groups, and guarded inverse plans exist | Append every later material branch/merge to the ledger and run its rollback gates before integration |

### 1.4 World and area scorecard

| Area | Rating | Strengths | Main problem and recommendation |
|---|---:|---|---|
| Storybook UI and menus | **3/5** | Picture-first direction, touch targets, and route probes are solid | Prove the complete fresh-save graph, focus/back behavior, and root-viewport Canvas evidence on phone |
| Sky Lagoon | **2/5** | Rich approved panorama/prop art, animated animals, and strong gameplay probes | It still fails true layer stack, draw order, occlusion, and engine-layer contracts; build genuine Canvas layers, then capture at phone ratios |
| Reef / home ocean | **2/5** | Broad exploration, characters, districts, and many regression probes | Free-swim spatial staging and mixed affordances are hard for a non-reader; convert one bounded route family and prove every return path |
| Pearl Castle rooms | **3/5** | Dense interactions, strong room identity, saved logo personalization, and good probe coverage | Room shells remain spatial and capture coverage is incomplete; convert shell/order without losing the interaction catalogue |
| Courtyard and train | **2/5** | Recognizable transit and destination links | Purpose and direct-touch routes remain bound to spatial traversal; define the child-facing route first, then Canvas-convert it |
| Northern world | **2/5** | Substantial kingdom art and gameplay content | Legacy free-swim/3D staging and incomplete current visual inventory; re-inventory live routes before another art pass |
| Ember Fortress | **2/5** | Playable fire-themed progression and probes | Heavy spatial architecture and unclear long-term product role; decide keep/retire, then convert only the accepted loop |
| Fairy Pond | **3/5** | Complete declared 2D art family and a gentle no-fail fantasy loop | Runtime remains a spatial scroller and figure-ground review is open; port the existing verb to Canvas before recoloring approved art |
| Galaxy | **2/5** | Bespoke concept and meaningful scripted content | Legacy rail/planet staging plus 32/32 orphan PNGs; owner must choose conversion or retirement before more asset work |
| Living world and companions | **3/5** | Care, follow, collection, and no-fail repairs create a warm persistent world | Ambient shell is spatial and exact care speech/device evidence is incomplete; move ownership and cues into bounded Canvas surfaces |
| Opera House lobby and careers | **3/5** | Best content breadth: 13 careers, current specialist games, diegetic rooms, career art, voices, and music | 166.5 MB orphan review, incomplete all-career capture, retained 3D engines/headless kart, and several voice/device gaps keep it below 4 |
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
| Racer | **4/5** | Display/device path is a simple three-phase Canvas circle game with the exact lap cue | Remove the ordinary-headless legacy lobby/kart path and run child/device visual acceptance |
| Pop Star | **3/5** | Strong music/lane/crowd identity and career-specific art | Audio latency, all-state capture, and device/owner review remain open |
| Nursery Nurse | **4/5** | Cooperative Faron framing, bottle/pat/blanket/catch flow, no opponent, speaker-aware prompts | Finish exact voice/state captures plus device/child review |
| Opera boss acts (Dragon, Phantom, Maestro) | **2/5** | Distinct finales, music, and established encounter logic | All three remain legacy spatial/device presentations rather than final Canvas specialists; convert or explicitly retire each before calling Opera fully 2D |

### 1.7 Opera House version and branch comparison

“Best” means best supported by current evidence, not the newest timestamp. A
branch row may contain useful art without being safe to merge as a whole.
This inventory groups branch aliases that resolve to the same commit as one
version. It rates materially distinct committed runtimes and documentation-only
candidates separately; rescue refs are preservation evidence, not additional
product versions.

| Version / repository location | Status and rating | Pros | Cons / regression risk | Verdict |
|---|---|---|---|---|
| Stable `origin/master` `e924d9ba` | Released but superseded quality, **2/5** | Known stable lineage and broad Opera content | 86 career phases, 29 generic `bop` phases, no dedicated Ballet/Boxing surface, and display Racer can launch the external 3D kart | Keep only as release history; do not use it as the design baseline |
| Earlier flat/2.5D/hybrid Opera prototype branches and ledgers | Reference/review versions, **2–3/5** | Large visual idea inventory and useful provenance | Many are review-only, generic, spatial, duplicated, or semantically obsolete; not independently shippable games | Mine accepted source ideas only; never merge a prototype family wholesale |
| `32e1a7e8` quality overhaul / `ecad384e` minigame-quality generation | Superseded integration steps, **3/5** | Established 13 career art families, specialist props, and 208-frame evidence | Dated 52-phase/19-mode counts, generic old Ballerina/Boxer premises, and retained kart descriptions | Supporting provenance, not current mechanics authority |
| Current development parent `origin/dev` `ea6185fd` | Best pre-audit product integration, **3/5** | 53 phases, no generic `bop`, current Candymaker, diegetic/borderless Opera, Ballerina/Boxer specialists | Does not contain the new master GAME2D controls or audit removals; ordinary source still carries more 3D debt | Use only through the audited reconciliation, not directly as the new audit baseline |
| Reconciled runtime/audit merge `f3b0de07` plus CI repair `af4189a9` | **Best overall audited integration, 3/5** | Combines current dev content with shrink-only audit controls, Canvas display Racer, 64/63 probes, exact local/remote evidence, and granular rollback | Whole game remains UNSATISFIED; ordinary-headless kart, 509 models, device/child/owner/listening/visual gates remain | Current master-audit reference and safest integration base; not release-ready |
| Old generic/incorrect Ballerina versions | Rejected/superseded, **1–2/5** | Demonstrated basic phase flow | Human legs/feet or old art, generic PHRASE/POSE/RIBBON/TWIRL logic, and misleading looped playback | Preserve only as rejection/history evidence |
| Integrated Ballerina A-atlas and three-act specialist (`0447188f` lineage, in `f3b0de07`) | **Best current Ballerina, 4/5** | One-tail accepted identity, Pearl Mirror/Ribbon Trail/Grand Twirl, held poses, one-shot cheer, assists and probes | Final two-aspect/M11/child/owner evidence remains | Keep as current authority |
| Device-acceptance Ballerina branch `fd0f1813` | Diverged evidence branch, **3/5** | Adds dedicated Ballet shot sizing/device-review tooling | Four commits unique but seven commits behind current dev; not the current integrated runtime | Salvage focused probe/evidence ideas only after rebase |
| Game-wide animation-doubling branch `20e9b1f2` | Clean committed post-snapshot candidate, **3/5 potential 4** | 159 compositions grow 921→1842 cels; focused audits pass 13 Opera careers/416 cells, 39 Castle fixtures/624 cells, playground 24 cells, and 14 imp families/302 cells | Based directly on pre-audit `ea6185fd`, changes 694 files, has no exact-head remote run, and a GAME2D comparison fails with 1,132 findings: 771 models, 76 production-3D and 85 probe-3D files; it retains the legacy 3D Racer path | Cherry-pick/rebase bounded art/runtime pieces onto the audit line only after identity, memory, M11, strict GAME2D, and full CI review; never merge wholesale |
| Boxer V1 specialist (`8d67c2bd`, integrated) | **Best implemented Boxer, 4/5** | Five phases, true Canvas, two gloves, one-finger sequential completion, no loss | Device/child/owner acceptance and legacy GLB retirement remain | Keep and finish external acceptance |
| Boxer V2 branch `ed4851a0` | Docs-only concept, **not implemented** | Strong deterministic counterboxing/mastery design without punishment | 782-line proposal only; added complexity and optional Jolt/3D language conflict with final medium | Review as a future design, not a game version |
| Candymaker pre-`39746756` | Superseded, **2/5** | Core pour idea existed | Cropped/conflicting mold, small/poorly registered pour, weak phone causality | Do not restore |
| Candymaker Pixel 10 repair `39746756` | Strong repair, **4/5** | Complete mold shell, generous target, measured spout, 30/60 fps monotonic tests | Earlier visual state set | Valid ancestor and fallback comparison, not the newest art |
| Candymaker authored syrup rebuild `cd39cae4`, integrated through `ea6185fd`/`f3b0de07` | **Best current Candymaker, 4/5** | Authored empty mold, cavity fill, full/empty ladle, provenance and expanded probes | Device/owner/child acceptance still open | Keep as current version |
| Current generic Painter in `ea6185fd`/`f3b0de07` | Integrated development version, **3/5** | Functional sunrise paint/stamp/gallery route | Less purposeful artifact and continuity than the newer proposal | Current implemented Painter until a replacement is cleanly integrated |
| `codex/painter-purpose-20260811` worktree | Uncommitted candidate, **potential 4/5** | Four continuous party-banner steps, helper, persistent result, one-finger purpose | Branch ref equals `ea6185fd`; actual 12-file plus untracked-surface implementation is dirty and unproven at an exact commit; save/logo coupling is broad | Review and rebuild as a bounded commit; do not credit or merge the worktree |
| `codex/arborist-tree-doctor` worktree | Uncommitted fourteenth-career candidate, **potential 4/5; current 1/5 because absent** | True Canvas/PNG tree-care game with inspect, prune, root-water, wrap, bloom; coherent caregiving fiction and dedicated art/probe | Ref is stale `ecad384e`; implementation/art are dirty/untracked, five exact family voices are missing, and no exact-head full/device/owner evidence exists | There is no missing Arborist 3D “base model” to import; finish the Canvas career as a clean rebased feature if the owner accepts it |
| Canvas Racer in `f3b0de07` | **Best Opera Racer, 4/5** | Simple circle gesture, exact speech, same implementation on display/device, passive/replay/teardown coverage | Ordinary unforced headless still reaches legacy kart source | Keep Canvas version and delete the split rather than restoring kart |
| Unmerged Claude Opera story/diversification branch `55ba40d8` | Docs-only proposal, **not implemented** | Useful narrative/diversification ideas | Three documentation commits, no current runtime or accepted asset evidence | Review after current careers meet capture/device/child gates |

The overall winner is therefore the **`f3b0de07` reconciled integration with
the `af4189a9` portability repair**, not stable `master`, raw `dev`, or a newer
dirty/candidate worktree. Within it, Dolls, Seek, the picture games, Ballerina,
Boxer, Candymaker, Racer, Chef, and Nursery are the strongest individual
activities. “Best” still means **best current repair base**, not 5/5 or ready
for promotion.

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
| Tracked Markdown files | 315 |
| `scripts/main.gd` | 8,519 lines |
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

#### 4.2.3 Latest CI repair, local merge integration, and remote verification

Current merge `f3b0de078898a8b4faddb2c738c4403180eff928`, with parents
`ea6185fdb1a687a20a6d118bdc368400e2c30f60` and
`5f58ef0a9db7aa9593f85131e1b855e51b84aea8`, reconciles the complete audit
history into the newer `origin/dev` runtime. Its runtime/static content
completed the local full gate below. Workflow/parity repair `dacef140` remains
historical remote evidence for its own exact head; it is not remote evidence
for `f3b0de07`. Current focused evidence is:

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

The latest CI-repair checkpoint is
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
Dust/Opera advisory balance, the Opera manifest, and all five diagnostic
capture/upload pairs green; the pinned Windows music job completes in 3m55s
with 42/42 deliveries green. The five captures remain diagnostic artifacts and
grant no authoritative visual PASS. This closes exact-head remote CI for the
repair checkpoint only. A full local suite at `af4189a9`, matching APK, Mobile
acceptance capture, target device, child, owner, listening, strict-2D, and
authoritative visual evidence remain pending.

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

The current `f3b0de07` local merge-integration audit reproduces the same
state totals: **16 FAIL, 17 REVIEW_OPEN, two MANUAL_OPEN, 86 COVERAGE_GAP,
32 PASS, and 94 NOT_APPLICABLE**. The unchanged totals are not evidence that
the merge is visually accepted; they are an advisory `UNSATISFIED` result. The
missing live Canvas capture matrix still fails closed. Exact-head run
`31649113587` uploads five diagnostic capture families, but those artifacts do
not satisfy the authoritative same-process fresh-runtime strict contract.

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
- Strict GAME2D at the last full checkpoint `f3b0de07` was run and failed as
  required; no zero-debt result or full-suite result at `af4189a9` is claimed.
- No complete live visual-runtime capture matrix is claimed; fresh-runtime
  strict produced no accepted Canvas captures and failed closed. The five
  green remote capture/upload pairs are diagnostic and cannot fill this gate.
- Exact-head remote CI is green at `af4189a9`; no matching APK result is
  claimed.
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
| `MA-OPERA-001` | P1 | `FIXED_PENDING_VERIFICATION` | V3 partial | Chef now uses the accepted batter pitcher, source-true stream/fill behavior, mitt-gated oven, achieved cake, and deterministic topping art; the old cutoff/fallback/wrong-object report is not a current code premise | Accepted two-aspect/device/owner art review |
| `MA-OPERA-002` | P1 | `CONFIRMED_OPEN` | V4 partial | Detective's “missing” crown remains painted into the scene evidence | Healed owned source, narrative/capture verification |
| `MA-OPERA-004` | P1 | `CONFIRMED_OPEN` | V1 | Opera capture harness has not produced accepted evidence for all careers | Repair harness; capture and human-review all careers/widgets/scuffles/stress states |
| `MA-OPERA-009` | P1 | `FIXED_PENDING_VERIFICATION` | V3 partial | Boxer now has a full-stage five-phase two-glove specialist with optional multitouch, sequential one-finger completion, no health/loss, passive rejection, touch-owner cleanup, and stable existing save bit. A newer Boxer V2 document exists only on an unmerged docs branch and is not current runtime authority | Two-aspect and target-device touch/performance review, child comprehension, and owner visual acceptance; separately review the V2 proposal before any authority or implementation change |
| `MA-OPERA-010` | P1 | `CONFIRMED_OPEN` | V1/V3 split-path evidence | Display/forced-2D Opera uses the Canvas lobby and Canvas Racer, but ordinary headless startup still selects the legacy lobby and `opera_act.gd` can load `scripts/kart.gd` and attach an external kart child. Forced-2D probes therefore cover only the Canvas branch | Remove the legacy lobby/racer medium split and external kart lifecycle; prove ordinary headless and display use the same Canvas path, then run passive, close/re-entry, surrounding and full exact-head gates |
| `MA-PERF-001` | P1 | `BLOCKED_EXTERNAL` | V0 | No current target-device frame-time, hitch, memory, thermal, or latency matrix | U0 device matrix at exact release candidate meets design thresholds |
| `MA-CHILD-001` | P1 | `BLOCKED_EXTERNAL` | V0 | No current observed five-minute child golden-path record | Private/safe observed session meets section 12 |
| `MA-RELEASE-001` | P1 | `FIXED_PENDING_VERIFICATION` | V3 local merge and exact-head remote green; release acceptance open | Merge `f3b0de07` exits exact local Godot 4.7.1 CI after 1437.1 seconds with all 64 trusted probes. Failed run `31648427712` at `bbc817ef` proves Windows music 42/42 but stops on the Ubuntu declared-text newline hash. Repair `af4189a9` preserves binary-exact hashing and passes focused cross-platform checks. Replacement run `31649113587` then succeeds at exact `af4189a9`: Ubuntu static/import/full analyzer/all 63 remote probes/boot/advisory balance/Opera manifest/five diagnostic capture pairs are green in 35m27s, and Windows music 42/42 is green in 3m55s. The captures grant no visual acceptance, and no full local suite at `af4189a9` is claimed | Require a matching APK and target-device matrix at the eventual release candidate, plus the still-open child, owner, authoritative visual, listening, strict-2D, and clean re-audit gates |

### 5.2 P2/P3 and owner-decision indexed items

| ID | Severity | Lifecycle | Verification | Indexed issue / decision |
|---|---|---|---|---|
| `MA-VIS-004` | P2 | `REPORTED_UNCONFIRMED` | V1; `COVERAGE_GAP` | Current source-average figure/ground values are Fairy 0.039 vs 0.040 and Lagoon about 0.004, but the metric does not measure the rendered local state and cannot confirm an art defect. Closure requires true state-local Canvas/HUD/viewport/device evidence, not recoloring approved art to satisfy the average |
| `MA-ASSET-001` | P2 | `CONFIRMED_OPEN` | V1 | Current orphan PNG reports: Castle 9/15 at 2.1 MB, Galaxy 32/32 at 11.7 MB, Opera 453/548 at 166.5 MB, Lagoon 48/90 at 41.9 MB |
| `MA-ASSET-004` | P2 | `CONFIRMED_OPEN` | V1 | Lagoon has 10/41 NPOT textures, about 11.6 MB uncompressed residency cost |
| `MA-CI-002` | P2 | `VERIFIED_FIXED` | V3 current local/remote parity and execution | Current blocking-loop parity is 64 local names versus 63 remote names, with display-only `probe_human_art_audit` the intended difference; default and stress checks are green. Historical run `31457593351` executed the then-current 62 remote probes at `dacef140`. After failed pre-loop run `31648427712`, replacement exact-head run `31649113587` executes all current 63 remote trusted probes successfully at `af4189a9`; the last complete local suite remains the 64-probe `f3b0de07` checkpoint |
| `MA-CI-003` | P2 | `CONFIRMED_OPEN` | V1 | All 106 probe scripts still need exactly one trusted/runtime-visual/advisory/diagnostic/obsolete/quarantined classification |
| `MA-ROSHAN-003` | P2 | `DEFERRED_WITH_REASON` | V1/V3 reported | Atlas repacking is an optimization; current owned-pixel windows and engine sampling probes are green |
| `MA-ROSHAN-004` | P2 | `DISMISSED_NOT_A_DEFECT` | V1 | Universal 2D costume layers are optional future design, not a missing required feature |
| `MA-PLAY-002` | P2 | `OWNER_DECISION_REQUIRED` | V1 | Standalone fire-arena reward/flag/medal role needs a truthful home or retirement |
| `MA-COMBAT-001` | P2 | `FIXED_PENDING_VERIFICATION` | V3 reported | Phone-only wave count, slash-band scale, and tutorial discoverability remain for device review |
| `MA-OPERA-003` | P2 | `CONFIRMED_OPEN` | V1/V4 partial | The grouped old pipe/echo/Nursery fallback claim is partially repaired by current authored pipe, echo, bottle, pat, and blanket behavior, but its unresolved subclaims have not yet been split and re-audited against accepted captures |
| `MA-OPERA-005` | P2 | `FIXED_PENDING_VERIFICATION` | V3 partial | The old Ballerina art/mechanic is superseded by the accepted 1024×1024 4×4 mermaid atlas and dedicated three-act full-stage recital; focused, last-full-local, and exact-head remote gates are green. Closure still requires accepted two-aspect capture, M11/child play, and owner identity/style acceptance; the remote diagnostic captures do not fill that evidence |
| `MA-OPERA-006` | P2 | `CONFIRMED_OPEN` | V1/V3 partial | Nursery, Farmer, and Racer received material art-fiction repairs, but the grouped historical claim must be split and re-audited; remaining protected-voice mismatches stay open rather than being inferred fixed |
| `MA-OPERA-007` | P2 | `OWNER_DECISION_REQUIRED` | V1 | Farmer/Doctor above-water setting differs from the other Opera backdrops |
| `MA-AUDIO-001` | P2 | `FIXED_PENDING_VERIFICATION` | V3 partial | Forty-two unique deterministic area cues have complete score/render hashes, 48 kHz stereo OGG delivery, loop/import metadata, loudness/peak/seam measurements, routing ownership, and focused audio/full-branch evidence. The pinned Windows jobs in failed run `31648427712` and successful replacement `31649113587` both verify 42/42; neither fills the human style/two-wrap, voice-over intelligibility/ducking, mono fold-down, music-off transition, or Lenovo Tab M11 start/loop/performance gates |
| `MA-CHANGE-001` | P2 | `VERIFIED_FIXED` | V2/V3 process evidence | Twenty-five stable records, `CHG-001` through `CHG-025`, now cover 70 unique catalog-owned commit references, including the exact current reconciliation merge, focused `af4189a9` CI repair under `CHG-015`, and human scorecard/repository-version snapshot `a3d7580c` under `CHG-025`. Every record names paths, benefit, plausible harm, dependencies, evidence, gates, and rollback class. The planner imports no Git/filesystem mutation API; only CHG-020/021/022/024 can emit guarded stdout scripts, while the other 21 refuse automation. Nineteen unit tests, exact ledger/catalog source parity, clean non-mutation CLI replay, Git-history checks, GAME2D no-regression, and independent adversarial approval are green. Future material changes must append under the stable ID or add the next ID; drift reopens this finding. |
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
| `MA-OPERA-008` | P1 | `VERIFIED_FIXED` | V3 partial: display/forced-2D Canvas branch only | The Canvas Racer finale requested a ride-selection recording for a circle gesture and could leave stale caption/fallback output | `e4528b27`; exact `op_racer_lap_two` pooled recording, hidden caption, quiet fallback, parser/lint, and focused Canvas Opera2D/voice/Opera probes. This closure is bounded to the cue/Canvas finale defect; retained ordinary-headless legacy lobby/kart routing remains open as `MA-OPERA-010` and `MA-2D-002` |

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
| `EV-CI-006` | `MA-RELEASE-001`, `MA-2D-002`, `MA-OPERA-010` | Reconcile the audit history with the newer development runtime without overstating closure | Merge `f3b0de07` (parents `ea6185fd` and `5f58ef0a`); exact Godot 4.7.1 local `scripts/ci.sh` exits 0 after 1437.1 seconds with 64 trusted probes, GAME2D 74 unit tests plus 14 falsification controls, 509 models/509 active, 157 tracked plus 352 generated sidecars, 68 production/77 probe/one scene/one config, and all then-current static/Opera provenance gates green. This is the last full local checkpoint. `EV-CI-008` later supplies exact-head remote evidence only; APK/device/child/owner/listening/strict-2D/authoritative visual evidence remains open, as does the ordinary-headless legacy Opera kart lifecycle. |
| `EV-CI-007` | `MA-RELEASE-001`, `MA-CI-002`, `MA-AUDIO-001`, `MA-CHANGE-001` | Diagnose and narrowly repair the current cross-platform Opera provenance failure without weakening binary integrity | Exact-head run `31648427712` at `bbc817ef`: the pinned Windows area-music job succeeds 42/42; Ubuntu fails only in the static Opera-art gate because generated provenance held the raw CRLF checkout hash of declared text input `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/GENERATION.json` while Linux read LF, so import/analyzer/63 probes never run. Repair `af4189a9` canonicalizes LF only for that declared text source, keeps every binary hash byte-exact, refreshes provenance, and passes 10 focused tests plus Windows and LF-clean Opera checks at 42/42. The failed run remains failed; `EV-CI-008` records its successful replacement. Full local CI at `af4189a9` remains unclaimed. |
| `EV-CI-008` | `MA-RELEASE-001`, `MA-CI-002`, `MA-AUDIO-001` | Verify the newline-stable repair at the exact remote head without promoting diagnostics into acceptance | GitHub run `31649113587` succeeds at exact `af4189a9`. The Ubuntu probes job completes in 35m27s: static gates, import, full analyzer, all current 63 remote trusted probes, boot, Dust/Opera advisory balance, Opera manifest, and five diagnostic capture/upload pairs are green. The pinned Windows job completes in 3m55s with music 42/42. This closes exact-head remote CI only; the captures remain diagnostic, and APK/device/child/owner/listening/strict-2D/authoritative visual/full-local-at-`af4189a9` evidence remains open. |
| `EV-CHANGE-001` | `MA-CHANGE-001` | Make the large audit program reviewable and reversions granular | `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md`, `tools/plan_audit_rollback.py`, and 19 unit tests; CHG-001–025 cover 70 unique catalog-owned commit references, only CHG-020/021/022/024 emit guarded stdout scripts, all other groups refuse automation, CLI execution leaves Git status byte-identical, and independent adversarial review approves the catalog/history/safety contract |
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
| `EV-AUTH-001` | `MA-DOC-001`, `MA-DOC-002` | Reconcile current authority to true 2D while preserving the incomplete-ledger state | `9289dd81`; operational/design authorities updated; exhaustive classification of the current 315 tracked Markdown paths remains open |
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
| Device-only real-3D Opera kart with a headless/probe Canvas bypass | `SUPERSEDED` as design authority; retained source is current debt | Final authority requires one true-Canvas implementation. Exact `f3b0de07` still retains an ordinary-headless legacy lobby/racer route that can attach `scripts/kart.gd`; `MA-OPERA-010`/`MA-2D-002` own its removal, so the forced-2D probe branch cannot be mistaken for global closure |
| `OPERA_MINIGAME_QUALITY_AUDIT_2026-08-09.md`'s 52-phase total and its old Ballerina, generic Boxer, and nested-kart Racer descriptions | `SUPERSEDED` in those scopes | Current shipping table is 13 careers/53 phases/27 modes; latest Ballerina, Boxer, and Canvas Racer authorities control while non-conflicting prop provenance/repairs remain supporting evidence |
| `OPERA_QUALITY_OVERHAUL_2026-08-09.md`'s 52-phase/19-mode/single-`bop` snapshot and requirement to loop every Ballerina row chronologically | `SUPERSEDED` in those scopes | Current Opera has 53 phases/27 modes/no generic `bop`; Ballerina frames are held pose keys because adjacent silhouette jumps are 41.6–47.3%, with only a one-shot curtain call |
| Earlier Ballerina atlas attempts, generic PHRASE/POSE/RIBBON/TWIRL route, or any leg/feet-like candidate | `SUPERSEDED` | `BALLERINA_PARTY_REBUILD_2026-08-09.md` and accepted generation `exec-a4dfa550-5374-43b6-a5e0-16a9d3d4b81c.png` control; prior leg/feet-like candidates remain rejected evidence, and the runtime atlas remains a one-tail mermaid at exact hash `c829784d4085e9cd9765cf0114a0f65bfe3f662ed8acc423223b726a0f003995` |
| Boxer manifest's retained `opera_boxer_outfit.glb`, `opera_boxer_dressing.glb`, and `opera_rival_boxer.glb` as useful runtime resources | `SUPERSEDED` | The Canvas specialist does not require them; while active they remain exact GAME2D transition debt and must retire through the normal tested archive path |
| Music audit's temporary retained `race` cue for an Opera nested kart | `SUPERSEDED` as final direction | The Canvas Racer stays under its Opera career music. A retained legacy headless kart route still exists as implementation debt; its presence does not restore the old music recommendation as current authority |
| Painter-purpose worktree / branch | `UNCOMMITTED_CANDIDATE` | Purpose-focused Painter runtime edits are not part of `f3b0de07`; review, rebase, audit, and commit independently before any authority or shipping claim |
| Arborist career worktree / branch | `UNCOMMITTED_CANDIDATE` | Arborist art, surface, save, lobby, probe, and audit files are not part of `f3b0de07`; it is not a fourteenth current career or base model |
| Boxer V2 branch document | `DOCS_ONLY_CANDIDATE` | `design/BOXING_GAME_V2_2026-08-12.md` exists on a separate branch only; current authority remains the integrated five-phase Boxer until that proposal is independently reviewed and adopted |
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
- **Acceptance:** authoritative two-aspect Mobile capture, one-finger
  target-device comfort/performance and
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
      gates, and all 64 current trusted local probes are green at one integrated
      commit. Historical `a3d3bce1` remains green for its then-current 61-probe
      suite; current merge `f3b0de07` completes the full local gate in 1437.1
      seconds. Historical `dacef140` completes remote run `31457593351` for its
      own SHA. Run `31648427712` at `bbc817ef` proves Windows area music 42/42
      but stops in Ubuntu static checks on the declared-text newline hash; it
      remains a failed run. Replacement `31649113587` succeeds at exact
      `af4189a9` with both required jobs, all 63 remote trusted probes, boot,
      and deterministic music 42/42 green. No full local suite at `af4189a9`
      is claimed. This full matrix must repeat at the eventual release
      candidate, so release satisfaction remains unchecked.
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

1. Keep the dedicated `codex/audit-reconcile-20260812` branch synchronized;
   create the missing complete item records and finish the exhaustive 315-document
   ledger/document-control gate. Authority reconciliation itself is complete at
   `9289dd81`.
2. Continue one tested true-2D gameplay family from the exact 509-model/
   68-production-file inventory until every GAME2D
   category is zero; archive exact resources before active deletion.
3. Implement live fresh-runtime Canvas adapters, beginning with converted
   surfaces and then Fairy/Lagoon; keep every missing capture as a gap.
4. Preserve the verified current Ballerina, Boxer, Candymaker, and 42-cue
   machine evidence; remove and prove the ordinary-headless legacy Opera
   lobby/kart route under `MA-OPERA-010`, repair remaining Opera capture
   coverage, and split the stale grouped Opera art claims.
   Continue with the confirmed Lagoon Canvas-layer defect. Confirm or dismiss
   palette risks only from current state-local evidence.
5. Reconcile protected voice gaps, including Evie's exact Seek tap-tree cue,
   through owner-authorized sources.
6. Rebuild and prove the complete child-visible world graph.
7. Classify all probes and remove only proved obsolete assets/code.
8. Preserve the historical `a3d3bce1`, `ad36ee9f`, and `dacef140` evidence and
   the 1437.1-second exact local gate at `f3b0de07`. Preserve failed run
   `31648427712` as evidence of the CRLF/LF provenance defect, not as a pass;
   replacement `31649113587` is green at exact `af4189a9`. Rerun local and
   remote gates whenever runtime/static content changes and at the eventual
   release candidate, then produce the accepted capture matrix, matching APK,
   target-device U0 pass, audio listening matrix, and child golden path.
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
| 2026-08-10 | `REPAIRING` | Earlier reconciliation preserved the display/forced-2D Canvas Racer with exact `op_racer_lap_two` speech at merge `ad36ee9f`. The later exact `f3b0de07` review narrows this historical claim: an ordinary-headless legacy lobby/kart source path remained and is now explicit `MA-OPERA-010` debt. |
| 2026-08-10 | focused `VERIFYING` | The resolved integration content committed as `ad36ee9f` completes exact Godot 4.7.1 `scripts/ci.sh` in 826.4 seconds with fresh import, all static gates, GAME2D `NO_REGRESSION`, and all 63 then-current trusted local probes green. Remote exact-head CI remains pending; strict 2D, visual, audio-listening, device, child, and owner gates stay open. |
| 2026-08-10 | `REPAIRING` | Exact-head GitHub run `31455723446` at process commit `57bc08d1` fails before import in `prepare_opera_minigame_art.py --check-only`: Linux and Windows reproduce identical RGBA pixels but not identical PNG compression bytes. CHG-015 is widened with an IDAT-only comparison repair and strict chunk/mode/size/scanline/pixel/delivery-hash negative controls; the replacement exact-head run remains pending. |
| 2026-08-10 | focused `VERIFYING` | `fe10ffd2` and exact-head run `31456633826` prove all 39 governed Opera minigame artifacts green on Linux. The same run then exposes a separate missing-FFmpeg integration error before import; music verification is moved, not removed, to a parallel checksum-pinned Windows job matching its recorded render toolchain. Replacement exact-head evidence remains pending. |
| 2026-08-10 | focused `VERIFIED_FIXED` | Workflow/parity repair `dacef140` completes exact-head run `31457593351` successfully in 34m19s. The pinned Windows job verifies 42/42 deterministic music deliveries; Ubuntu passes static gates, import, analyzer, GAME2D 509/68/77 `NO_REGRESSION`/`UNSATISFIED`, all 62 trusted probes, boot, advisory balance, and all five capture/upload pairs. This closes the two CI integration defects only; release, strict-2D, visual, listening, device, child, and owner gates remain open. |
| 2026-08-12 | focused `VERIFYING` | Merge `f3b0de07` reconciles newer `origin/dev` parent `ea6185fd` with audit parent `5f58ef0a`. Exact Godot 4.7.1 local `scripts/ci.sh` exits 0 after 1437.1 seconds with all 64 trusted probes and current static/provenance gates green. GAME2D has 74 unit tests plus 14 falsification controls and remains exact `NO_REGRESSION`/`UNSATISFIED` at 509 models/509 active, 157 tracked plus 352 generated sidecars, 68 production/77 probe/one scene/one config. Visual advisory remains `UNSATISFIED` at 16 FAIL/17 REVIEW_OPEN/2 MANUAL_OPEN/86 COVERAGE_GAP/32 PASS/94 NOT_APPLICABLE. This closes local merge integration only; exact-head remote/APK/device/child/owner/listening/strict-2D/authoritative visual evidence remains open. |
| 2026-08-12 | `CONFIRMING` | Exact source review narrows `MA-OPERA-008` to its display/forced-2D Canvas cue/finale repair. Ordinary headless startup still selects a legacy Opera lobby and may attach `scripts/kart.gd`; new `MA-OPERA-010` keeps that lifecycle and `MA-2D-002` debt open instead of allowing forced-2D probes to certify it away. Current Candymaker is integrated; Painter purpose and Arborist are uncommitted candidates, and Boxer V2 is docs-only on a separate branch. |
| 2026-08-12 | `REPAIRING` / focused `VERIFYING` | Exact-head run `31648427712` at `bbc817ef` passes the pinned Windows area-music job 42/42 but fails only the Ubuntu static Opera-art gate: generated provenance held the raw CRLF checkout hash of declared text `GENERATION.json`, while Linux read LF. Import, analyzer, probes, boot, and captures did not run. Repair `af4189a9` canonicalizes only that declared text hash to LF, leaves binary hashes byte-exact, refreshes provenance, and passes 10 focused tests plus Windows and LF-clean archive checks at 42/42. The failed run stays failed; replacement exact-head remote and a full local suite at `af4189a9` remain pending. |
| 2026-08-12 | focused `VERIFIED_FIXED` | Replacement exact-head run `31649113587` succeeds at `af4189a9`. Ubuntu completes static checks, import, the full analyzer, all current 63 remote trusted probes, boot, Dust/Opera advisory balance, Opera manifest, and five diagnostic capture/upload pairs in 35m27s; pinned Windows music completes 42/42 in 3m55s. This closes exact-head remote CI only. The captures remain diagnostic, the last full local checkpoint remains `f3b0de07`, and APK/device/child/owner/listening/strict-2D/authoritative visual gates remain open. |

No later state is added without its required evidence.
