# Faerie garden — castle magic restoration prototype

Status: `PROPOSED / CANDIDATE`, isolated playable true-2D scene. Owner commission
2026-09-30. Source baseline `285355eb9e09a29aa4ac53d36874e31419d4674e`.
Implementation and machine checks do not grant visual/device/child/owner acceptance.
Audit impact: [task record](audit_impacts/fairy-restoration-prototype-20260930.json).

## 1. Commission and boundaries

The child wants to help the castle shine again after the Ember King takes the
Rainbow Candle. This prototype develops the faerie/butterfly half of that work:
arborist tree care → fruit harvest → chef fruit preparation → butterfly picnic →
gentle flower shooter → bring faerie magic home. The second world and the full
castle-restoration ending remain outside this commission's implemented scope.
The cake, candle-taking, completed birthday preparations and Ember King's motive
are preserved. No new principal character, antagonist or lost-progress threat.

The [existing Chapter 3 route](FAIRY_CONSERVATORY_CHAPTER3_2026-08-30.md) controls
production geography: Main Hall → Moonflower Door → Rainbow Skyway → Butterfly
House → Butterfly World → Fairy Pond, with symmetric return. Its seven-baby rescue,
`bwdone`, `fairyskin`, `flower`, pearl rewards and legacy access retain their
existing meanings. The isolated review scene compresses travel and does not
replace that route, its rescue, or its downstream spatial presentation.

Delegated detail: a local sick fruit tree, three apple portions and three picnic
friends give familiar verbs connected purpose. No paid service or new raster
generation. All visual art is reused intact; any later raster derivative uses
Aseprite under the owner's 2026-09-30 workflow. Rejected watering-can candidates
are excluded. No cinematic or external animation handoff is commissioned.

## 2. Experience and pacing

Design target: short, forgiving activities with saved stopping points; timing
and enjoyment remain unobserved. A quiet harvest/picnic separates tree care from
the shooter. No health, timer pressure, failed meal, lost fruit or repeat payout.

| Beat | Touch verb and immediate response | Lasting causal result | Exact cue key / assistance | Resume point |
|---|---|---|---|---|
| Castle | Tap visible moonflower door | Enter/resume prototype garden | `enter`; moving hand | All garden work survives return |
| Arborist | Tap a visible tangle; Roshan approaches and applies local magic | Three branches become usable | `arborist`; 136-pixel touch diameter, next-target hand | Each branch mask |
| Water roots | Hold, then rub back and forth at the roots after arrival | Roots receive water; same tree bears three apples | `water`; large root ring shows water amount | Partial water saves on release/Back/focus loss |
| Harvest | Tap each apple; local reach before collection | Those three apples appear on the table | `harvest`; next fruit hand | Each apple mask |
| Chef | Swipe across each apple after Roshan reaches it | Whole fruit separates into two source-image halves | `chef`; no penalty for misses or taps | Each prepared portion mask |
| Picnic host | Tap each butterfly; Roshan approaches it with the snack | Each portion is consumed once; friend gets a sparkle | `picnic`; next friend hand | Each fed friend mask |
| Faerie shooter | Hold and glide in lower flight lane; automatic sparkles | Three buds become full flowers | `shooter`; wide correct lanes, no health or penalty | Each bloom mask |
| Carry home | Tap earned magic beside the bloomed flowers | Castle preview receives faerie glow; second half remains unresolved | `complete`, then `returned` | One permanent return flag |

The nine new OGG cues use the established local Kokoro Roshan settings and live
under `assets/prototypes/fairy_restoration/voices/`. They are additive synthetic
prototype recordings, not edits or substitutes in protected voices. The scene
calls `_say()` at every phase, interrupts the previous line and ducks music.
Listening/intelligibility and final voice acceptance remain pending.

## 3. Continuity and navigation

The tree keeps its approved painted colors, light and contours. Sick state is
shown by removable thorn/tangle overlays; watering unlocks fruit on that same
tree. Hungry butterflies remain kind and present throughout the sequence.
Roshan uses approved farmer/chef pose atlases, with the existing fairy wing card
as temporary support in the faerie-water setting; flight uses the existing fairy
costume. This costume combination is a review candidate, not accepted new canon.

The prototype's castle preview is an isolated launcher/return postcard. Its Back
arrow and Escape leave work immediately, preserve progress and restore this
preview. Returning does not reconstruct the production Main Hall camera because
the production chapter route is not attached. No global menu, save migration,
unlock, reward or freeplay consumer changes.

## 4. Save and causal reconstruction

Only `user://fairy_restoration_prototype.json` is read/written. `reef_save.json`
and all production save keys remain untouched. Fields: `cleared`, `picked`,
`cut`, `fed`, `bloom` are three-bit masks; `water` is a clamped fraction;
`returned` is a boolean. Unknown fields are preserved. Missing fields default
to zero/false. Prerequisite normalization prevents malformed future state from
skipping required work. Writes use a temporary file plus previous `.bak` copy;
malformed primary JSON falls back to the backup.

Arrival/time alone cannot water, cut or fire. Intentional tap jobs complete only
after local arrival and visible work. Second fingers cannot take ownership of an
active gesture. Focus loss cancels input/work/audio and saves existing progress;
focus return requires fresh input. Repeat, wrong and passive input earn no new
completion. Every milestone survives Back, teardown and scene re-entry.

## 5. Strategic asset shortlist

Search scope: runtime/source fairy V2/V4/V5 families, conservatory source masters
and tile manifests, MG garden assets, story fruit/leaf props, GEN2 butterflies,
castle furniture, approved Roshan atlases and existing voices/music. Searches
included current consumers in `scripts/games/fairy.gd`, `galaxy.gd`,
`picture_games.gd`, `story_art.gd` and the central license ledger. Assets with
dynamic consumers are not described as unused merely from a search miss.

Exact selected paths, source SHA-256, dimensions, protection and roles:
[art reuse manifest](../assets_src/prototypes/fairy_restoration_2026-09-30/ART_REUSE_MANIFEST.json).

| Family | Authority / consumers | Player benefit and readiness | Decision |
|---|---|---|---|
| Conservatory lily-pad panorama | Existing project-generated native 3640×2048 master; eight 910×1024 runtime cards; current skyway consumer | Complete single-screen coverage, open play area, established fairy palette; reused tile order without healing or regeneration | Use as temporary garden backdrop; final interior geography needs owner review |
| `assets/mg/tree.png` + story apples | Existing project-generated cards used by garden/story families | Recognizable same tree before/after; clear tree → ingredient consequence | Use; sick state is overlay prototype, no authored sick-tree state claimed |
| Fairy thorn, bud/bloom, leaf and lily cards | Existing project-generated V2/V4/V5 runtime art; Fairy Pond consumers | Coherent state family makes meaningful care and bloom possible cheaply | Use intact as Canvas cards |
| GEN2 complete butterfly | Project-generated RGBA card; `galaxy.gd` and garden consumers | Friendly, oversized picnic targets; identity retained | Use; no new character biography |
| Pearl dining table | Existing project-original castle furniture; dining-room consumers | Keeps chef work in the castle's toy-playset vocabulary | Reuse intact for garden picnic station |
| Farmer/chef atlases and fairy skin/wings | Current approved career/base art families; accepted source cells, new use remains contextual candidate | Actual work/travel/attention poses, stable Roshan identity | Use; exact pruning/watering/cutting tool/contact poses remain art gaps |
| Legacy watering can | Book-derived rough crop; style35 flat silhouette; later generated candidates rejected for checkerboard | Weak quality and rejected derivatives cannot become the new world's tool | Exclude; use local water-spell gesture; reserve Aseprite derivative only after selecting a suitable source |
| Castle tiles, moonflower doorway and glow | Existing route/hall art; source resolution is inherited existing debt for this review postcard | Gives a recognizable entry and earned return context | Use in isolated preview only; do not claim new native-2K castle repair |
| `picture_garden.ogg` | Existing garden score, not a newly composed cue | Quiet familiar activity bed, ducked under voice | Reuse; new cue ownership ends with scene teardown |

New authored raster-art count: zero; native review screenshots are evidence.
The same licensed story-prop family also contains `fruit_orange.png`,
`fruit_melon.png` and `fruit_banana.png`. These are ingredient-variety candidates
for a later pass; the orange was visually inspected and keeps the apple family's
painted outline and palette. This first prototype uses three apples so the
tree-to-table consequence can be reviewed before adding more choices. Whole-fruit
reuse does not resolve the separately identified cut-face art gap.
Source originals are unchanged. Sprite region cropping
for split apples is a temporary runtime state visualization, not raster asset
editing or a cinematic technique. Cut faces, sick-tree/healthy-tree action states,
hand-tool poses and final setting composition are named future art gaps; suitable
source reuse must be exhausted before any new generation.

## 6. Implementation and dependency plan

Run `scenes/fairy_restoration_prototype.tscn` in exact Godot 4.7.2-stable (open the
scene in the editor and use F6). The scene
is a self-contained `Control`/`Node2D`/`Sprite2D` prototype with fixed 1280×720
composition, uniform aspect fitting and no new spatial node/resource. It is not
in the production launch menu. Source: `scripts/fairy_restoration_prototype.gd`.
Focused probe: `scripts/probe_fairy_restoration.gd`, using live routed touch events.
Disk-fixture runs require APPDATA and LOCALAPPDATA below
`tmp/fairy_restoration_review/<profile>/`; the probe refuses another profile
before writing fixtures. This guard prevents a manual run from touching family
data. Adding `-- --capture` records the real Mobile render and its source hashes.

Movement follows [Roshan's profile](animation/ROSHAN_MOVEMENT_LANGUAGE.md):
notice → travel → local hand effect → persistent result → settle. Candidate clip
contract V1: atlas frame 4 is travel, frame 8 is local reach, frame 9 is roots
attention/work; hand magic socket `(-77, -20)` in the 256-pixel source cell;
arrival is within two logical pixels of target + `(85, 20)`; local tap work holds
0.55 seconds. These are provisional semantic poses, not newly accepted temporal
animation. Gesture progress requires actual valid input after arrival. Focus,
Back and teardown cancel all pending work. Required art/contact study and human
review remain open; no final pruning/cutting animation is claimed.

Next production step, after prototype review: adapt the existing chapter route
and shared saved state without replacing the seven-baby rescue or any existing
reward. Convert downstream Butterfly/Fairy spatial presentation in separate,
bounded tested work. This prototype does not satisfy `MA-2D-002` or close
game-wide embodied-job finding `MA-PLAY-004`.

## 7. Acceptance matrix

| Claim | Evidence / command | Result and limits |
|---|---|---|
| Source/authority/coverage | Parser, inference lint, exact 4.7.2 analyzer; document/development gates | Recorded in task impact after verification |
| Intentional/negative/input/lifecycle/save | `--headless --script scripts/probe_fairy_restoration.gd`, isolated APPDATA profile | Recorded in task impact; live-input tests, not child observations |
| Runtime composition | Same focused probe with `-- --capture`, measured 1280×720 Mobile | Eleven unchanged live captures, source/probe hashes and focused log in [review receipt](../assets_src/prototypes/fairy_restoration_2026-09-30/review/VERIFICATION.json); no accepted visual/device result is inferred |
| Surrounding production regressions | Exact 4.7.2 local gate stages and branch CI before integration | All local stages pass, including 77/77 trusted probes. [Split-run receipt and logs](../assets_src/prototypes/fairy_restoration_2026-09-30/review/LOCAL_GATE_RECEIPT.json) preserve the initial cross-drive fixture failure, corrected TEMP/TMP environment, exact original CI suffix and final presentation recheck. Exact-head branch CI is required before integration |
| Voice and meaning | Nine exact new synthetic cues, known music, cue-state binding | Listening, phone intelligibility and one-finger comprehension pending |
| Device/child/owner | Lenovo Tab M11/target phone: touch, 30 fps, memory, comprehension, pacing, art/canon | Pending; no fabricated human observations or game-wide satisfaction |

## 8. Decision and learning log

2026-09-30: Owner commissioned faerie/butterfly world prototype with arborist →
chef → happy butterflies causality and existing art reuse. Existing high-quality
fairy state families make a playable candidate possible without new raster art.
Rough watering art is a specific gap, not a reason to redesign the world.
Previous unfinished Battle of Bands/Aseprite work was preserved untouched on
`rescue/peter-2026-09-30` before branching from fresh `origin/dev`.
The prototype's compressed route, work poses, magical watering and half-magic
return are agent-authored implementation choices within this commission;
production geography and full ending are not implicitly replaced. Final source
review separates the split-apple regions visibly and names the flower-flight
objective accurately; eleven fresh source-bound Mobile captures verify those
presentation corrections. Child review must still check the water/chef gesture
timing after Roshan arrives, alongside pacing and instruction comprehension.

Integration regression: incoming dev b52fc32a fails the unchanged Opera Racer
exact-instruction test. A direct baseline proves the stale Chapter Two route
retains the speech channel. The shared AudioDirector repair permits an exact
Opera/Chapter Two activity objective to supersede that obsolete route/phase cue;
generic talk/win/pearl and Day One required FIFO keep their priorities. No
recording or prototype artwork changes. Source-bound baseline and sibling
checks are in the task impact. Final code `33a2c8e3` passes all local gate stages
using the permitted probe-by-probe path and the [GitHub Probe suite](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/36785254581). All 82 original native probes pass; the fixed-frame combat tutorial uses the official 60-fps clock while its code and 1.75-second charge threshold remain unchanged. Bash/native process failures and the initial uncapped tutorial assertion failure remain honestly archived. The review packet preserves raw attempts, the success-log composition, runner and receipts. The newer
job-game audit at dev 83d7e1ed is preserved. Its interim recipe uses the delegated
standalone-prototype extension path here; no permanent career, star bit or
takeover-playbook implementation is added.

Latest reconciliation preserves dev `ce033173` phase-owned Opera voice clearing
and its forced-overlap regression. The direct activity-priority guard and phase
owner pass the voice, Day One FIFO, Chapter Two and Opera checks together; the
new combined code requires its own full CI before integration. The incoming Job
Platform architecture is a proposal, with no runtime implementation here.
Official Windows headless processes can abort or access-violate locally; raw
failures and successful probe-by-probe evidence remain separately recorded.
