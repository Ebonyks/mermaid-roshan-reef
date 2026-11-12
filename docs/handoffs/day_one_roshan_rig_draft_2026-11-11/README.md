# Day One: Mermaid Roshan action audit, art direction and rig draft

2026-11-11. Rough draft by Claude at the owner's request. It reviews the Rigby2D work Codex has already done, uses the bathroom cleanup study as the model, audits every Roshan action in Day One against it, sets an acting direction for Roshan, and adds a first set of Day One clips to the rig.

Status: **rough draft; design accepted by the owner on 2026-11-11** ("This is now accepted design"), and the project rules now allow a 2D skinned cutout rig for Roshan's gameplay acting. Nothing here changes the game yet, closes a finding or supplies visual, device or child acceptance. Claude has not watched any of these clips; the draft is animation data checked by geometry only. Codex renders and reviews.

## 1. What is in this folder

| File | What it is |
|---|---|
| [`rig/roshan_day_one_draft.rigby`](rig/roshan_day_one_draft.rigby) | The bathroom rig (`roshan_arm_rebound.rigby`) with 44 new animations named `D1 …`. Open in Rigby2D 0.4.3. Bones, slots, skins, weights and all nine textures are byte-identical to the source. |
| [`rig/day_one_clips.json`](rig/day_one_clips.json) | The clip catalogue: intended keys, the strength the current rig can deliver, markers, props and the rig change each clip needs. |
| [`rig/joint_envelope.json`](rig/joint_envelope.json) | How far each joint can turn before the painted mesh leaves the 0.80–1.20 strain floor. |
| [`rig/strain_verification.json`](rig/strain_verification.json) | 30 fps check of every new clip in Original, Ballet and Magician. |
| [`tools/`](tools/) | The scripts that produced the above ([rebuild steps](#9-rebuild)). |

## 2. Codex's existing work, as reviewed

| Stage | Where | What it established |
|---|---|---|
| Rigby2D Godot trial, 11-05 | worktree `.worktrees/rigby-roshan-trial-20261105`, `assets_src/animation/rigby_roshan_trial_20261105/` | The Rigby GDExtension plays a skinned Roshan in Godot 4.7.2 Mobile with live costume swaps. Windows x64 binary only. No navigation or gameplay. |
| Original-art rig, revisions 01–08, 11-07/08 | worktree `.worktrees/rigby-original-art-20261107`, `assets_src/animation/rigby_original_art_20261107/` | One 17-bone actor bound to the approved swim atlas cell. Two repaints were owner-rejected for drift (revisions 03–04); revision 08 uses registered donor paint. Original, Ballet and Magician share the skeleton. |
| Bathroom scene and acting, 11-09 | same worktree, `bathroom_scene_20261109`, `bathroom_acting_20261109` | Brush on a palm socket, three fixtures, blink patches, hair lag, earned completion. |
| Two views, motion, arm scrub, swim arms, arm rebind, 11-10 | same worktree, `bathroom_two_views…` to `bathroom_arm_review_20261110` | Authored left head, tail-driven travel, arm-led scrubbing (body moves 4–19 px for 45–109 px of brush travel), elbow-correct swim arms, forearm weight repair. |
| Published packet, 11-10 | branch `codex/claude-bathroom-action-audit-20261110` | The hash-bound packet of the last build. |
| Claude secondary review and Codex work order, 11-11 | branch `origin/ccr-68aec945-iossk2`, `docs/handoffs/claude_bathroom_action_review_2026-11-11/` and `codex_bathroom_scene_revision_2026-11-11/` | Issues C-01 to C-12, work orders WO-A1 to WO-A8, and the proposed "scene acting rig pattern" in the master audit. |

Open items carried from those notes, all still true for Day One:

- The left/right view swap moves the fluke 120–126 px in one frame. A front crossover view is needed (WO-A7).
- The brush trails backward on leftward carries (WO-A3, WO-A4).
- Back-and-forth rubbing never finishes the round fixtures (WO-A1).
- The hand is one painted silhouette. Codex's own notes ask for an open hand, a closed grip and a supported scrub posture.
- No revision folder for the 11-11 work order was found on this machine, so Phase A appears not to have started.

**None of this is in the game.** The rig exists only in the browser study and the Godot trial. The two bathroom branches and the two rig worktrees are unmerged, and the worktree material is uncommitted.

## 3. What the current rig can and cannot do

The rig is one continuous painted figure. Arms, head and ponytail are not separate pieces, so every joint stretches the paint around it. Measured single-joint limits, all three looks:

| Joint | Safe range | Joint | Safe range |
|---|---|---|---|
| Head | ±3° | Abdomen | −16.5° to +15° |
| Ponytail base / tip | ±2° / ±2.5° | Chest | ±6° (the Ballet bodice limits it) |
| Trailing upper arm | ±10° | Tail root, mid, distal | about ±15° each |
| Leading upper arm | −11° to +11.5° | Tail peduncle | −19.5° to +17.5° |
| Forearms | −19.5° to +17° and −26° to +30° | Fluke | −16° to +14.5° |
| Hands | about ±17° and ±22.5° | | |

Consequence: the rig is good at swimming, scrubbing at waist height, small nods and tail acting. It cannot raise an arm, turn or shake the head, wave, point, hug, clap or reach a shelf. A wave needs the upper arm near 85–95°; the rig allows 11.5°.

Result for the 44 draft clips ([per-clip numbers](rig/day_one_clips.json)):

| Result | Count | Clips |
|---|---|---|
| Runs at full strength now | 8 | `idle_breathe`, `idle_tail_sway`, `idle_glance_at_child`, `idle_hum_sway`, `talk_beat_a`, `talk_beat_b`, `travel_commit`, `work_wipe_side` |
| Runs at 58–91% strength now | 10 | `idle_fin_flick`, `react_tap_giggle`, `react_tap_tail`, `notice_look`, `listen_nod`, `travel_brake_settle`, `turn_gather_t1`, `room_arrive_look_around`, `react_uh_oh_dusty`, `celebrate_small_admire` |
| Needs the rig upgrade (under 58%) | 26 | Every wave, point, reach, carry, tug, scoop, clap, hug, surprise, sneeze and the big celebration |

In the draft rig each clip is stored at the strength the mesh allows, so all 44 play without tearing. The 26 upgrade clips are placeholders at 8–53% of the intended pose; the full keys are in the catalogue for use after the upgrade.

## 4. Day One, beat by beat

Read from `origin/dev` at `f070a61e`. Room order is bathroom, pool, playroom, art room. "Static cutout" means one atlas cell sliding with no pose change.

| Beat | What Roshan does today | What she should do | Clips |
|---|---|---|---|
| Start menu | Painted splash only | Out of scope (splash art) | — |
| Sky Lagoon travel | Static left-profile cell slides; instant mirror to turn | Tail-driven swim; T0–T4 turn | bathroom motor, `travel_commit`, `travel_brake_settle`, `turn_gather_t1` |
| Castle door, hall doors | Slide to the door, then a cut | Notice the door, push through | `notice_look`, `door_enter` |
| Room arrival | Teleports to room centre, front idle | Glide in, look around, react | `room_arrive_look_around`, `react_uh_oh_dusty` in the dusty hall |
| Waiting anywhere | 1.8 px breath and a rotation wobble | The idle system in section 6 | `idle_*` |
| Child idle 5 s / 12 s | Ghost-hand button and voice only | Roshan herself looks at, then points at, the target | `notice_look`, `guide_point_at_target`, `guide_beckon` |
| Any spoken line | Caption and voice; no acting | Small beat with the line, mouth patch | `talk_beat_a`, `talk_beat_b`, `listen_nod` |
| Child taps Roshan | No handler exists | Always answers | `react_tap_giggle`, `react_tap_wave`, `react_tap_tail` |
| Bathroom basket | Stands still while tools pop in | Reach and take the tool | bathroom study grasp |
| Sink, tub | **Roshan is not involved.** The sponge and brush follow the finger alone | The bathroom study: carry, hover, arm-led scrub, lift | bathroom study |
| Tub bunny "NO!" | No reaction | Startle, then a look at the child | `react_surprise`, `idle_glance_at_child` |
| Toilet | Static cutout; only the brush rotates | Bathroom study | bathroom study |
| Fixture done / room done | Three sparkles | Admire hold per fixture; one bigger accent per room | `celebrate_small_admire`, `celebrate_clap`, `celebrate_big_dolphin` |
| Pool skimmer | Static cutout; whole card rocks ±3° | Two-hand scoop and lift | `work_skim_scoop` |
| Waterfall | Static cutout follows the finger | Downward swipe per stroke | `work_swipe_down` |
| Seahorse | Static cutout; the trash rotates | Brace with the tail and tug; recoil when it pops free | `work_tug_pull`, `work_tug_release` |
| Rumi (story clip, later tap-greet) | No response | Wave back | `greet_wave` |
| Playroom dust bunnies | Swim cycle only; the bunny pops by itself | Shoo with a hand and tail flick at contact | `work_shoo_bump` |
| Baby Eagle freed, adopted, following | No response; rigid follower card | Greet; pet or hug on adoption; pet on a tap | `greet_wave`, `companion_pet`, `companion_hug` |
| Art supplies | Static cutout; the supply snaps to her hand | Reach down, grasp, carry, place | `work_pick_up`, `work_carry_hold`, `work_place_stow` |
| Art counters | Static cutout dragged along; the brush jiggles | Side-to-side wipe | `work_wipe_side` |
| Colour customizer | Roshan absent | Roshan beside the panel, reacting to each pick | `listen_nod`, `celebrate_small_admire` |
| Grand Puff appears | No Roshan in the splash | Startle | `react_surprise` |
| Dodge, dash | Static billboard cell slides | Tuck and thrust | `react_dodge_dash` |
| Sneezed on | Old `boing` atlas verb | Recoil and shake the dust off | `react_sneezed_on` |
| Tickle star / soap clean | Old `point` verb plus a code-drawn beam | Aim the wand; the beam starts at the prop tip | `work_aim_bubble_wand` |
| Befriended; rainbow bunny follows | Old `cheer` verb | Big celebration, then pet the new friend | `celebrate_big_dolphin`, `companion_pet` |
| Day Two card | Card only | Wave goodbye to the child | `day_end_wave_goodbye` |

The largest gaps against `DL-INT-02` and `DL-MOT-07`: the production sink and tub do not use Roshan at all, every other job is a sliding cutout, and nothing in Day One answers a tap on her. The old atlas has unused verbs (wave, clap, look, giggle, carry, collect); they are useful as pose references for Codex.

Not found in dev: any towel beat. Branch `codex/bathroom-floor-towels-20261110` exists with no commits of its own.

## 5. Art direction for Mermaid Roshan

The movement language's sentence stays the rule: she **notices with her eyes, decides with her hands, and travels with her tail**. For Day One that becomes:

1. **She is the child's hands.** Every job happens at her palm or tool, at the moment the child's finger asks for it. A prop never moves by itself.
2. **She always knows the child is there.** A tap on her gets a reaction on the next frame. After a win she glances out at the child before moving on. When the child is stuck she looks at the target, then points.
3. **Eyes first.** Each action opens with a 0.2–0.6 s look at its target. At room scale the head direction reads more than a blink, so the head needs real range.
4. **One clear pose per verb.** A four-year-old should be able to name the action from the silhouette: scoop, tug, wipe, wave. Arms must leave the torso outline to read.
5. **Tail and hair finish last.** The body settles, then the fluke and ponytail resolve once. Hair is never a metronome.
6. **Calm by default, joy on real events.** Ribbon Glide for everyday work. One small acknowledgment per fixture. One Playful Dolphin accent per room and at the befriending. No cheering while idle.
7. **A curious helper, never scared.** Dust bunnies and Grand Puff get surprise and then interest. No fear poses, no fail poses.
8. **Painted, not rubbery.** Broad shapes, clean contours, no visible stretch. Where the paint would tear, the answer is a new piece of art, not a wider bend.

Face: the rig has only half and closed lids. Day One needs seven small patches on the quarter-right face: wide eyes, smiling closed eyes, eyes toward the camera, worried brows, mouth open (talk), mouth open wide (yawn, cheer) and mouth closed smile.

Hands: four hand shapes per arm instead of one: relaxed, open palm, closed grip and pointing.

## 6. Idle and life system

The movement language says idle is listening: sparse glances, about 1% of body height, no idle celebration. Lifelike comes from layering and from answering the child, not from constant motion.

| Layer | Behaviour | Clips |
|---|---|---|
| Base, always on | Breath, slow tail drift, hair drift | `idle_breathe` blended with `idle_tail_sway` |
| Blink | Every 3–6 s, only in quiet phases, never during a contact | lid patches |
| Fidget, one at a time | First after 6–9 s of quiet, then every 7–12 s, never the same twice running | `idle_fin_flick`, `idle_glance_at_child`, `idle_look_up_bubble`, `idle_hum_sway` (one 2.4 s phrase), `idle_hair_twirl`, `idle_stretch` |
| Guidance | Replaces the fidget when an objective is waiting: look at 5 s, point at 12 s, beckon at 25 s | `notice_look`, `guide_point_at_target`, `guide_beckon` |
| Touch | Tap on head or body, arm side, or tail. Interrupts any idle within 2 frames | `react_tap_giggle`, `react_tap_wave`, `react_tap_tail` |
| Companion | Follower within reach and quiet for 20 s: Roshan pets it once | `companion_pet` |
| Long idle | After 45 s with no input: one yawn, then base only | `idle_yawn_sleepy` |

Rules: any input cancels a fidget at once. Fidgets never play during work, travel or a voice line. Nothing here awards progress.

## 7. Rig upgrade needed for Day One

| ID | Change | Unlocks | Art needed |
|---|---|---|---|
| R1 | **Separate both arms** into upper arm, forearm and hand pieces with rounded joint overlaps and a shoulder underlay under each. Per-look sleeve pieces for Ballet and Magician | Wave, point, reach, carry, scoop, tug, clap, hug, stretch. Nearly all of the 26 blocked clips | Arm pieces cut from the approved quarter-right paint; shoulder and underarm fill. The wardrobe shoulder patch already exists |
| R2 | **Separate the head** (face, tiara, hair mass) on a neck underlay; ponytail as its own two-bone piece | Head turns of ±15–20°, look up, head shake, real hair follow-through | Neck fill; ponytail root fill |
| R3 | **Hand set**: relaxed, open palm, closed grip, pointing, per arm, swapped as attachments | Readable wave, grasp and point | 6 new small hand paintings |
| R4 | **Face patch set** from section 5, feathered like the existing lids | Surprise, smile, talk, yawn, gaze at the child | 7 small patches |
| R5 | **Front crossover view and same-scale left view** (bathroom C-05, WO-A7) | Turns without the 120 px fluke jump | Front seed exists in the shared contract; left head re-registered at 1.0 scale |
| R6 | **Sockets**: second palm, two-hand grip pair, chest-carry point, hair-touch point, companion contact point, prop-tip (beam origin) | Skimmer, seahorse tug, carried supplies, wand beam, petting | None |
| R7 | **Aim and look-at controls**: head toward a target within its range; leading arm aims at a point | Pointing at the real door, the wand on Grand Puff's star | None |
| R8 | **Clip contract** (`DL-MOT-12`): each clip carries its markers (`grasp_attach`, `release_detach`, `contact_*`, `blink`, face-patch events), an interrupt rule and a return-to-idle blend | Props attach at the visible grasp; taps interrupt cleanly | None |
| R9 | **Runtime**: Rigby GDExtension builds for Android arm64, or the converter to Godot `Skeleton2D`/`Polygon2D` (WO-B2), and a device cost measurement | Anything in the actual game | None |

R1 and R2 are the upgrade that matters. They turn the continuous mesh into a cutout puppet at the shoulders and neck, while the torso and tail keep the smooth mesh that already works. Every new piece of Roshan art is a named gap under `DL-MOT-14` to `DL-MOT-16` and needs owner approval before generation.

## 8. Suggested order for Codex

1. **Render the draft.** Open the draft rig, capture the 18 clips that run at 58% or more in all three looks, and review them at room scale and enlarged. Retime or re-key what reads wrong. Claude's keys are untested by eye.
2. **Idle and touch layer in the bathroom study.** Add the section 6 scheduler and the three tap reactions to the existing browser scene. This needs no new art.
3. **Bathroom work order Phase A** (WO-A1 to A5), unchanged.
4. **R1 arm separation pilot** on the leading arm only. Accept on `greet_wave` and `guide_point_at_target` at full strength inside the strain floor in all three looks. Then the trailing arm, then R2.
5. **One scene profile per room**, in Day One order, reusing the bathroom pattern: pool (skimmer, waterfall, seahorse), playroom (shoo, greet, adopt), art room (pick up, carry, place, wipe).
6. **Grand Puff** last: the arena still stages Roshan as a 3D billboard, so it needs Canvas staging before the rig applies.

## 9. Rebuild

Extract `raw/renderer`, `raw/scene/visible_triangles.json` and `raw/rig/project.json` from the packet on `codex/claude-bathroom-action-audit-20261110` into a work folder as `renderer/`, `scene/` and `rig/`. Copy `renderer/src` to `node_modules/@rigby/src` with a `package.json` of `{"name":"@rigby","type":"module"}`. Copy `tools/*` beside them. Then:

```
node envelope.mjs                      # joint limits
node fit.mjs                           # per-clip strength the mesh allows -> fit.json
node export.mjs                        # day_one_clips.json + animations.json
python -B build.py roshan_arm_rebound.rigby animations.json roshan_day_one_draft.rigby
node verify.mjs <project.json from the new archive> scene/visible_triangles.json strain_verification.json
```

Recorded results: source rig SHA-256 `db65e8fc…ff3ad2` (matches the packet); draft rig SHA-256 `71f46479…411e48`; 44 animations, 6,432 samples across three looks, strain 0.828–1.171, zero flips. Clip edits go in `tools/clips.mjs`.

## 10. Questions checked against the master audit, and what stays open

| Question | Answer found | Effect on this draft |
|---|---|---|
| Is a rigged Roshan allowed? | Yes, since the owner decision of 2026-11-11: `CLAUDE.md`, `AGENTS.md`, `DL-MED-02`, the movement language and the atlas contract now accept a 2D skinned cutout rig over approved art for gameplay acting. 3D models stay excluded | OD-1 is answered. Claude reads the decision as also making this 17-bone rig the working skeleton (OD-2); the shared-contract adapter is still to be written |
| Is the rig pattern in this branch's master audit? | No. It is on `origin/ccr-68aec945-iossk2`, unmerged, as are the review and the work order | That branch should be integrated or this draft rebased onto it before commit |
| May Claude make the clips? | Claude writes and does not build images. This draft is key data and measurements; it contains no rendered or edited image | Codex produces every picture |
| How lively may idles be? | Movement language: idle is listening, sparse glances, about 1% excursion, no idle celebration, blinks in quiet windows only | Section 6 follows it. **If the owner wants busier idles than this, the movement language needs an owner amendment** |
| Related findings | `MA-ROSHAN-006` (static Roshan playback) and `MA-PLAY-004` (Roshan visibly performs each job) are open | No lifecycle change claimed |
| New Roshan art | The accepted design includes the R1–R5 pieces. Each generated piece still needs a job card, the `DL-MOT-16` caps and owner review of the result | Codex may start the R1 pilot |
| Rumi | IP hold; do not regenerate | Only Roshan's reply is drafted |
| Baby Eagle and Grand Puff reactions | Outside this draft | `companion_pet` and `companion_hug` need matching companion clips |

Not done: visual review, timing by eye, the left and front views (all 44 clips are quarter-right only), device cost, and child acceptance.
