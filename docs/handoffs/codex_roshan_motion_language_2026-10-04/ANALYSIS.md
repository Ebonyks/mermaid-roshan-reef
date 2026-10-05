# How Mermaid Roshan should move — analysis (2026-10-04)

**Owner request (2026-10-04):** "Analyze the current approach towards the design
language and artistic direction of roshan's animations ... determing how
mermaid roshan should move, what animations would make her design language
consistent, and what refinements can be offered from the current state of grok
handoffs and aseprite animatinos. Check repo comprehensively." (spelling as
written)

**From:** Claude (analysis and written specification only; no game change, no
images). **To:** the owner, then Codex (every implementation and image) and,
through Codex, Grok. **Status:** `PROPOSED / CANDIDATE`, revision 2.
**Baseline:** `dev` `8a2f30cb0df44ece3b1172ed2dbcb9a55fc5d622`.
**Handoff:** [README.md](README.md). **Finding:** `MA-ROSHAN-006` (P2).
**Numbers:** [`data/motion_measurements.json`](data/motion_measurements.json),
reproducible with [`tools/measure_roshan_motion.py`](tools/measure_roshan_motion.py)
(reads committed atlases and scripts, writes numbers only).

**Revision 2 (2026-10-04, owner answers):** the owner confirmed left/right
orientation, rejected limited animation in favour of a rich, comprehensive
set, chose a slower, more modest swim for the Sky Lagoon, named LTX run
locally by a Codex script with Aseprite into the game as the production
workflow (Grok packets are test documents), and set the goal: a template
for all future Roshan animations. The answers are in the
[README](README.md#owner-answers-2026-10-04); the template is
[TEMPLATE.md](TEMPLATE.md). Sections 9–12 below are updated to match;
sections 1–8 are the revision-1 evidence and still stand.

Rules applied: `DL-MOT-01` to `DL-MOT-16`, `DL-CIN-01` to `DL-CIN-04`,
`DL-CIN-16`, `DL-AGE-07`, `DL-MED-02`, `DL-INT-02`, `DL-INT-04`,
`DL-AUTH-05` to `DL-AUTH-07`. Related findings: `MA-PLAY-004`,
`MA-ROSHAN-003`, `MA-ROSHAN-005`, `MA-VIS-006`, `MA-VIS-008`, `MA-DOC-008`,
`MA-DOC-009`.

## 1. The answer in brief

1. **The acting direction is good; keep it.** The 2026-09-11
   [movement language](../../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md)
   ("notices with her eyes, decides with her hands, and travels with her tail")
   and its two registers (Ribbon Glide everyday, Playful Dolphin for delight)
   fit the character and the owner's later verdicts. None of its pilot studies
   was ever made.
2. **What is missing is a picture of the motion, not more adjectives.** No
   document says which views she swims in, which side her fin curls to, how
   many drawings a stroke has, what her hair and fin do after a move, or
   whether blur is allowed. Every Grok and local trial has been judged against
   prose, and the owner's verdicts (stiff arms, odd hair, unnatural fin bends,
   blurred hands, frozen body) are exactly those missing specifications.
3. **The game shows key poses, not animation.** Every runtime Roshan sheet is
   a set of strong painted keys, and each player hides the gaps differently: the
   castle cross-fades two copies of her, the careers loop unrelated poses at
   4–8 frames per second, gestures spread four keys over up to 6 seconds, and
   the Day One jobs and Sky Lagoon slide a single still cutout. Nine of the
   fourteen gesture rows start with her fin on the other side of her body
   from the idle and swim art, so the tail jumps across her when the Grand
   Puff fight plays `boing`, `point` or `cheer`.
4. **She swims three different ways.** The base-world swim is an upright
   three-quarter breaststroke with an almost still tail; the career "travel"
   rows are a horizontal glide facing left; the Grok swim takes are a
   side-view, tail-driven swim facing right. The owner's last word on gameplay
   swimming (2026-09-16, on an unmerged branch) is "left and right only",
   which the owner confirmed on 2026-10-04.
5. **Effort has gone into methods for one gesture.** The local LTX/Aseprite
   work has produced three study packets of the same wave and zero accepted
   seconds. The motions the child sees all the time — swim, turn, stop,
   work — have no accepted source, while 26 returned Grok files (18 audition takes and 8 hero cuts of
   the eight swimming auditions, 2026-09-22) and the last two core-loop takes
   (2026-09-19) have never been reviewed.

The proposal: ten motion locks (section 9), a fourteen-clip canonical set
(section 10), and refinements for Grok, the local pipeline, the runtime and
governance (section 11), in an order that starts with what already exists.

## 2. Sources and method

Read in full or in the relevant parts: the master-audit planning entry and
task index; design 06 sections 4–6, 9 and 11; `AGENTS.md` animation and Day
One sections; the movement language, production protocol, workflow options,
character template, job card and animation branch README; the atlas contract
and 4× generation provenance; the active findings named above; the owner
decision register; the Day One selected-cut edit map; and these unmerged
branches: `grok/roshan-4way-basic-swim-20260914` (`056e668f`),
`codex/roshan-swim-start-loop-stop-20260914` (`2952d2d5`),
`grok/day-one-cinema-takes-20260922` (`138d3b1a`),
`codex/job-art-review-v2-20261001` (`cfcadc96`) and
`codex/animation-engine-benchmark-20261003` (`e2ebf8ff`). The LTX wave and
retake studies are on `dev`.

Code read: `scripts/player.gd`, `scripts/roshan_sprite_loop.gd`,
`scripts/sprite_transition_2d.gd`, `scripts/roshan_sprite_frames.gd`,
`scripts/opera_roshan_actor.gd`, `scripts/day_one_contact_action_2d.gd`,
`scripts/arena/castle_rooms_25d.gd`, `scripts/arena/sky_lagoon_promenade.gd`
and `scripts/games/dust_boss.gd`.

Images: every base-world atlas and two career atlases were opened and viewed;
two existing Codex review boards (LTX wave phases; Grok slow swim A004) were
viewed from their branches. No image was made or edited and no video frame
was extracted. Measurements are numbers from the tool above.

## 3. What the current approach gets right

| Strength | Where | Why it matters for the motion language |
|---|---|---|
| A clear acting thesis and two registers | `design/animation/ROSHAN_MOVEMENT_LANGUAGE.md` | Eyes lead, hands decide, tail travels; delight is an accent, not constant busyness. The owner's later critiques all agree with it. |
| Contact, cancellation and reward ownership | `design/animation/ANIMATION_PRODUCTION_PROTOCOL.md`, `DL-MOT-12` | Animation reports events; gameplay commits once. The Pool's gold-star reference patterns (`GS-01`, `GS-02`) are built on it. |
| Clip contracts exist as a format | `design/animation/grand_puff_encounter_clips_v1.json` | One versioned record per clip with anchors, loop, exit and interruption. Roshan needs the same for her own clips. |
| Identity canon is settled | `ODR-ROSHAN-IDENTITY`, `ODR-ROSHAN-IRIDESCENT`, `ODR-ROSHAN-Q12` to `Q16` | `roshan_base.png` is the anchor; the tail is iridescent; the tiara stays outside costumes. Motion work can bind these instead of rediscovering them. |
| Method permission and cost caps | `ODR-ANIMATION-*-20261003`, `DL-MOT-14` to `DL-MOT-16` | Video, keyed 2D and Aseprite cleanup are all allowed, with two takes per brief and a task cap. |
| Disciplined Aseprite masters | `assets_src/cinematics/ltx_registered_wave_20261004/`, `ltx_retake_repair_20261004/` | Every native frame round-trips through an editable master with hashes. The bridge itself works. |
| Owner verdicts are specific | sections 6 and 7 | "Stiff arms", "abnormal hair", "fin bends unnaturally", "less motion blur", "shoulder, torso, dress/bodice and hair must respond together" are usable specifications. |

## 4. What Roshan actually does on screen today

| Where the child sees her | Art | How it moves | Code |
|---|---|---|---|
| Castle rooms (Day One and later rooms) | Directional frame 0 idle; `roshan_swim_front.png` for every travel direction, mirrored for left | Idle: a 1.8 px breath plus a whole-sprite rock between −0.012 and +0.012 rad, 0.85 s each way. Swim: 16 frames at 8–12 fps, each change cross-faded so two half-transparent copies are drawn for 67% of every frame interval | `scripts/arena/castle_rooms_25d.gd:1349-1356`, `:2746`, `:2803`; `scripts/roshan_sprite_loop.gd:22-27`, `:186-195`, `:270-279`; `scripts/sprite_transition_2d.gd:151-184` |
| Day One jobs (contact action, Pool skimmer, toilet) | One still cutout: directional frame 1 | The still cutout slides to the work point at 440 px/s; soap bubbles circle the hand during 0.42 s of contact | `scripts/day_one_contact_action_2d.gd:32`, `:100`, `:106`; `scripts/games/pool_skimmer_activity.gd:517`; `scripts/games/day_one_bathroom_toilet.gd:60` |
| Sky Lagoon promenade | One still cutout: directional frame 2 (left profile), declared medium `land` | Slides along the route; a 26 px hop over 0.32 s; mirrored by direction | `scripts/arena/sky_lagoon_promenade.gd:991-997`; `scripts/arena/sky_lagoon_layout.json` |
| Grand Puff fight, toys, collections, trophy, idle (legacy player, a 3D billboard that is migration debt) | Full base-world family | Swim cycle by phase; gestures spread their 4 keys evenly over 0.8–6.0 s (0.2–1.5 s per key); idle picks one of 8 headings and breathes by scaling; `twirl` mirrors the whole sprite halfway through; `carry` alternates two frames forever; a random idle gesture after 12 s | `scripts/player.gd:79-121`, `:401-456`, `:458-473`, `:918-930`; `scripts/games/dust_boss.gd:465`, `:665`, `:1040` |
| Opera careers (15 costume atlases) | Career atlas rows idle, travel, work, cheer | Each row of four pose keys loops at 4, 8, 7 and 6 fps; Ballerina, Geologist and Teacher hold single poses instead | `scripts/opera_roshan_actor.gd:17-35`, `:178-206` |
| Menus, cards, kart roster, intro | `roshan_base.png` | Still | `scripts/main.gd:708`, `scripts/intro_overlay.gd:144` |
| Day One story clips | Owner-selected Grok footage (`DL-CIN-16`) | Full-motion video; may not be edited | `assets/cinematics/day_one_story/story_clips.json` |

## 5. Measured problems in the runtime motion

### 5.1 Gestures flip her tail to the other side of her body

The legacy player draws idle headings unflipped and draws gesture rows with
the same view flip as the swim cycle (`scripts/player.gd:406`, `:455-456`).
The sheets were generated separately (2026-07-26, `PROMPTS_4X.md`) and their
fins curl opposite ways:

| Art | Fin side (viewer) | Ponytail side (viewer) |
|---|---|---|
| `roshan_base.png`, directional front and front-left, all 32 swim frames | left | right (swim front: streaming back to the left; swim back: centred) |
| Gesture rows `wave`, `cheer`, `twirl`, `sleep`, `point`, `collect`, `boing`, `hum`, `flop` (first frame) | right | right |
| `clap`, `giggle`, `hairtwirl`, `carry` | slightly right (under the 0.06 threshold) | right |
| `look` | left | right |

So 9 of 14 gesture rows begin with the fin on the other side from the idle
and swim art, in both facings (`gesture_entry_fin_side` in the data). The
Grand Puff fight plays three of them (`boing`, `point`, `cheer`). Mirroring
the gesture is not a fix: it moves the fin but also moves the ponytail to the
other side of her head. This is a pose snap under `DL-MOT-01` and the
movement language's "a fin may trail a turn but cannot ... switch side
without a readable transition". `MA-ROSHAN-005` covers single bad frames
(RV-07, RV-08), not this cross-sheet mismatch.

### 5.2 Every frame is a key; nothing is in between

Silhouette change between neighbouring frames (1 − overlap of the alpha
masks; "aligned" first matches the centroids, so it measures shape change
only):

| Art | Neighbouring-frame change, aligned (min / median / max) |
|---|---|
| Base swim front, 16-frame cycle | 7.0 / 24.1 / 51.4 % |
| Base swim back, 16-frame cycle | 8.5 / 24.2 / 40.2 % |
| Base gesture rows (`gesture_a` to `c`) | medians 17.1, 24.9, 24.0 % |
| Base play rows (`play_a`, `play_b`) | medians 45.0, 40.1 % |
| All 15 career atlases, 240 pairs including the loop wrap | 0.9 / 24.5 / 53.9 % |

Stored as drawn (what the Opera player shows, since it applies no anchor
offsets), 25 of the 60 career rows have a neighbouring change of 40% or more
and 53 of 60 have 25% or more. Ballerina's rows were taken off looping in
August for 41.6–47.3% jumps (`DL-MOT-09`); that measurement's exact formula is
not recorded, so these figures are comparable only roughly. A smooth painted
cycle at 8–12 fps would need far smaller steps between drawings. The 4×
expansion asked for "four chronological keyframes: anticipation, transition,
peak action, and settle/return" per row, and that is what it produced:
keys, not motion.

### 5.3 Each player hides the gaps a different way

| Trick | Where | Effect on the child's view |
|---|---|---|
| Cross-fade between frames (`SMOOTHNESS_MULTIPLIER` 3) | Castle swim and idle | Two half-transparent Roshans overlap for 0.083 s of each 0.125 s frame at 8 fps (0.056 of 0.083 s at 12 fps): ghosted limbs, the opposite of the owner's 2026-10-04 "crisp contours", and two draws instead of one |
| Loop four pose keys at 4–8 fps | 12 Opera careers | Pose snapping, the defect `DL-MOT-09` already names for Ballerina |
| Spread four keys evenly over a long verb | Legacy player gestures | A slideshow: `sleep` holds each key 1.5 s, `boing` 0.2 s; equal key durations contradict "do not give every key equal duration merely because the atlas is a grid" |
| Slide one still cutout | Day One jobs, Sky Lagoon | Truthful contact (`MA-PLAY-004`) but a moving sticker (`DL-MOT-07`) |
| Rotate or mirror the whole sprite | Castle idle wobble; `twirl` mirror swap | Idle noise; an unreviewed mirror swap mid-gesture |

### 5.4 Three swim grammars

| Source | View | Propulsion | Arms |
|---|---|---|---|
| Base-world swim cycles (runtime, castle and legacy player) | Upright three-quarter, facing right; back view | Almost still tail (fin side constant, small change) | Symmetric reach-and-sweep breaststroke |
| Career travel rows (runtime, Opera) | Horizontal, facing left | Tail held behind | Both arms forward |
| Grok swim takes (reference only) | Side view, horizontal, facing right | Tail-driven: the fin rises and falls through the stroke | Small sculling near the chest |

The movement language asks for the third ("travels with her tail", "avoid
permanently mirrored paddling") and the owner's 2026-09-16 direction is
"left and right only". The runtime implements neither.

### 5.5 She has no way to move on land

The Sky Lagoon declares `"medium": "land"` and shows a still left-profile
card because "the former 16-frame swim cycle had no feet/ground contract and
made the card visibly airborne" (`scripts/arena/sky_lagoon_promenade.gd:991`).
The movement language forbids inventing hovering or legs without an owner
decision, so this mode needs one (Q5). Answered 2026-10-04: she still swims there, with a
slower, more modest animation than in the sea.

## 6. The Grok handoffs: what they established

| Date | Branch / location | What happened |
|---|---|---|
| 2026-09-12 | `dev`: `assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/` | Eight swimming auditions RSW-01..08 (glide, delighted departure, distracted explorer, bank, bored→eager, arrival, two cruise loops). The local `swim-scull-v6` prototype is recorded as owner-rated "3.5/5 at best: technically adequate, extremely stiff, without enough personality". |
| 2026-09-13 | same, video-first revision | One RSW-01 video before any batch; no still-board substitute. |
| 2026-09-14/15 | `grok/roshan-4way-basic-swim-20260914` | Front/right/back/left basic swims on navy plates. Owner inspection: hair and tail colour corrections outstanding; navy plates cannot give clean hair alpha. |
| 2026-09-16 | same, `056e668f` | Owner: "only using 2 view now, left and right, no front/back standard swim animations". Right (full stroke, "strongest clip") and left (tail only) remain candidates. |
| 2026-09-15..19 | `codex/roshan-swim-start-loop-stop-20260914` | RSW-FLOW-01 (owner 4.25) with owner defects: arms and upper body held near-straight, abnormal hair motion, fin bends unnaturally. Then slow (A001–A005) and dash (A001–A006) takes. Review: "neither short coordinated whole-body loop/seam is established"; dash added unrequested hand-water effects. Target cadence 0.8–1.2 s (slow) and 0.4–0.6 s (dash) per stroke. The last returns (slow A005, dash A006, 2026-09-19) were never reviewed. |
| 2026-09-22 | `grok/day-one-cinema-takes-20260922` | All eight auditions returned: 18 takes (RSW-01 four, the others two each) and 8 hero cuts, "editorial reference only". No review record exists on any branch. |
| 2026-09-20/23 | `dev`: Day One selected cut | The owner's chosen Grok footage plays between scenes (`DL-CIN-16`); one shot was replaced because of a forked tail. |

Owner workflow rule recorded with FLOW-01: "Written instructions produce
improved Grok performances. Initial video audit FIRST; failed source goes
directly back to Grok, never into Aseprite. Only a passing source is eligible
for conversion." The 2026-10-03 policy later made Aseprite the cleanup bridge
for results; the two fit together (clean passing results, never salvage
failures).

Recurring Grok failure modes, from the review records: identity drift (hair
toward auburn, rainbow ponytail weakened, a forked tail in the Day One
footage), backgrounds that prevent clean alpha, long strokes with about a
second of upright settling instead of short loops, unrequested effects, and
camera or framing changes. What Grok does well, from the same records and the
A004 board: a readable side-view swim in which the tail drives, the arms stay
near the chest and the hair streams behind — the grammar the movement
language asks for.

## 7. The Aseprite and local-model work

| Date | Study | Result |
|---|---|---|
| 2026-10-03/04 | Engine benchmark (`codex/animation-engine-benchmark-20261003`, unmerged) | Recommends Aseprite pose and socket preflight → LTX-Video 2B pose-guided → Aseprite isolation and export. Best Roshan take keeps one tail but changes body, head and hands; guides were not registered (crown centroid moved about 82 px between keys). |
| 2026-10-04 | Registered wave (`dev`) | Owner asked for less motion blur, then rejected the sharp limb-only correction: the shoulder, torso, dress/bodice and hair must respond together. Whole-figure takes keep the figure coherent but smear the hand while lowering. |
| 2026-10-04 | 8 GB retake repair (`dev`) | Temporal retake runs at 448×256 but ghosts the raised arm; rejected. |

Every study is the same 1.7–3.4 s wave from `roshan_gesture_a.png` row 0.
Accepted production seconds: zero. What the studies proved is useful: the
editable-master discipline works; registration to a waist landmark keeps the
figure coherent; generated in-betweens of a fast hand arc smear, and stronger
guides, prompts or retakes have not fixed that.

## 8. Diagnosis

1. **No visual motion specification.** The movement language is written as
   acting; the production protocol as process. Nothing fixes views, fin side,
   drawings per stroke, secondary motion, blur or the hold-and-snap policy, so
   each method is judged against adjectives and each owner verdict arrives as
   a surprise.
2. **Keys are presented as motion.** The approved art is a strong library of
   painted keys. The runtime tries to make keys move with fades, loops,
   slideshows and slides. Each trick fails a motion rule (`DL-MOT-01`,
   `DL-MOT-03` or `DL-MOT-07`).
3. **Method before clip.** Three local study packets tested one rare gesture.
   Meanwhile no swim, turn, stop or work clip has an accepted source, and the
   biggest pile of existing evidence (26 Grok returns) is unreviewed.
4. **Decisions are scattered.** The two-view swim (2026-09-16) and the shared
   final-action sequence (2026-10-03, `codex/job-art-review-v2-20261001`
   `audit/job_final_action_consistency_v1_20261003/OWNER_DIRECTION.json`:
   "Use the same final-action sequence everywhere, with Roshan visibly
   finishing each task") exist only on unmerged branches and are not in the
   owner decision register.

## 9. How Roshan should move: ten motion locks

These extend the movement language with a checkable picture. Numbers are
pilot starting points to tune with recorded evidence, as in v1. Revision 2
updates M1, M5, M7 and M10 to the owner's answers; TEMPLATE.md section 6
holds the current wording.

| Lock | Rule | Evidence behind it | Check |
|---|---|---|---|
| M1 Orientation | Left and right only: sprites have no up or down orientation. Author facing right and mirror the whole sprite for left; moving up or down the screen keeps the current horizontal facing. | Owner 2026-09-16, confirmed 2026-10-04; Grok swim strongest in side view; mirroring already used in the castle | Clip card names its facing and mirror rule |
| M2 Propulsion | The tail drives: one connected wave from hip to fin, fin root continuous, broad lobes, gentle membrane curve. Arms scull or balance near the chest; a two-arm sweep is never the propulsion. Shoulders, torso, bodice and hair answer each stroke. | v1 "travels with her tail"; owner FIN-01, BODY-01; owner 2026-10-04 whole-figure rule | Per-frame fin-tip and tail-root positions; no frame with both arms fully extended during cruise |
| M3 Home pose and fin side | Each view has one home pose with a fixed fin side and ponytail side. Every clip in that view starts and ends within tolerance of its home pose. The fin changes side only through a drawn swish or turn. | Section 5.1; v1 fin rule | Tool's `fin_side` at clip entry and exit equals the home pose side |
| M4 Follow-through | Ponytail and curls trail the head and settle with a buoyant curl; the fin tip trails the tail root; the tiara is rigid; sleeves settle within the action. The ponytail's ribbon arc is her signature on turns. | Owner HAIR-01; "Ribbon Glide" | Frame-by-frame review of head, ponytail tip and fin tip |
| M5 Rich motion | Full, smooth motion: keep the native generated frame sequence (24 fps in the current runner) and choose each clip's playback rate from review and the device budget. No limited-animation style and no frame-thinning to hide defects. | Owner 2026-10-04: "a rich, comprehensive set of animations"; core-loop stroke targets 0.8–1.2 s (slow) and 0.4–0.6 s (dash) | Measured stroke length; frame count kept from the native take |
| M6 Crisp contours | No motion blur, smear or cross-fade between frames unless a brief declares it. A smeared frame is repaired (Aseprite repaint or a temporal retake window), not blended or removed. | Owner 2026-10-04 "less motion blur"; section 5.3 | No frame with two semi-transparent copies; native-frame review of hands |
| M7 Listening idle | Idle is attentive and alive: authored breath, hair and fin motion on the home pose. No whole-sprite rotation or squash. Glances only when they do not compete with an instruction. | v1 "idle is a listening state"; `DL-MOT-03` | Idle displacement at most about 1% of body height |
| M8 One action shape | Every action: notice → reach or travel → contact → finish → settle → show result → celebrate once. Work verbs have their own contact key with a measured hand socket. | Owner 2026-10-03 shared final-action sequence; `DL-MOT-03`, `DL-MOT-12`; `GS-01`, `GS-02` | Clip contract events; probe that progress waits for contact |
| M9 Delight is rare | Playful Dolphin (two short pulses, one lift) only for a real discovery, greeting or earned success, once per event. | v1 registers; `DL-MOT-05` | No celebration on a timer or zero input |
| M10 One Roshan, context variants | Cinematics, gameplay and careers share M1–M8; tempo follows context. Water: standard swim. Sky Lagoon: swimming, slower and more modest travel. Castle rooms: owner question (README Q7). Career costumes change props and verbs, not the swim. Identity colours come from `roshan_base.png` (brown hair, tied rainbow ponytail, tiara). | Section 5.4; identity canon; owner 2026-10-04 Sky Lagoon answer | Same swim grammar in base and career travel; Sky Lagoon stroke measurably slower than the water swim |

## 10. The canonical clip set

Revision 2: these fourteen clips are the seed backlog. The template's
room-by-room pass (Phase B) extends them toward the rich, comprehensive set
the owner asked for, and the Sky Lagoon row now follows the owner's answer
(a slower, more modest swim, card `RAC-SKY-LAGOON-SWIM-GENTLE`).

What the child needs, ordered by how often she sees it. "Source" means
existing approved drawings that can serve as keys; "gap" is what must be
made.

| # | Clip | View | Use | Existing source | Gap | Priority |
|---|---|---|---|---|---|---|
| 1 | Swim, slow (loop) | side | All travel | None in the base family; Grok A004/A005 and RSW-01/07 as reference | Two side-view keys, then the whole cycle from LTX | First |
| 2 | Start and stop | side | Leaving and reaching a point | None | Short clips joined to clip 1's phases | First |
| 3 | Turn left/right | side → three-quarter → side | Reversal | Directional headings 6, 7, 0, 1, 2 as keys | 2 breakdowns; fin swish | First |
| 4 | Listening idle | three-quarter | Waiting, voice lines | `roshan_base.png`, directional 0 | Authored breath, hair and fin motion | First |
| 5 | Work contact: scrub/wipe | three-quarter | Day One bath, craft, toilet | None (still frame plus bubbles today) | Contact keys with a hand socket, then the stroke from LTX | Second |
| 6 | Work contact: scoop/carry/place | three-quarter or side | Pool, eagle, deliveries | `gesture_d` row 1 (carry), `gesture_c` row 0 (collect) | Socket table; fin side per M3 | Second |
| 7 | Notice/look | three-quarter | Attention before action | `gesture_b` row 0 (fin side already matches) | Repair RV-08 frame | Second |
| 8 | Greet/wave | three-quarter | Friends | `gesture_a` row 0; LTX wave studies | Fin side; one breakdown per arc | Third |
| 9 | Celebrate once | three-quarter | Earned success | `gesture_a` row 1 | Fin side | Third |
| 10 | Bump/recover | three-quarter | Boss contact, retry | `gesture_c` row 1 | Fin side | Third |
| 11 | Swim, dash (loop) | side | Fast travel | Grok A005/A006 as reference | Whole cycle, 0.4–0.6 s per stroke | Third |
| 12 | Point/reach | three-quarter | Boss counter, choices | `gesture_b` row 3 | Fin side | Third |
| 13 | Sleep and rare idles | three-quarter | Night, long idle | `gesture_b` row 2, `gesture_c` rows 2–3 | Fin side | Later |
| 14 | Sky Lagoon travel | side | Sky Lagoon | Variant of clip 1 | Slower, more modest swim (owner 2026-10-04) | First, after clip 1 |

Careers inherit 1–4 as costume overlays or costume-specific redraws later;
until then their pose keys hold (section 11.3).

## 11. Refinements

### 11.1 Grok handoffs

Revision 2: the owner calls Grok packets test documents to be digested for the
workflow; production runs through LTX locally (TEMPLATE.md section 4).

| ID | Refinement |
|---|---|
| G1 | Review what already exists before new spend: the 18 audition takes and 8 hero cuts (2026-09-22) and core-loop A005/A006 (2026-09-19), with the audition README's own protocol (neutral labels, normal speed, timestamps). Pick a timing spine for clip 1 and fragments for 2, 3 and 9. |
| G2 | Use Grok tests for performances (entries, exits, turns, delight beats) and timing reference. Do not ask them for seamless short loops: the core-loop reviews found repeated takes give long strokes with about a second of upright settling. Loops are cut in Aseprite from a clean stretch of a local LTX take. |
| G3 | Make future swim jobs extraction-ready: a flat background colour absent from Roshan's palette and tested with the cleanup path that produced the approved atlases, instead of navy. Pilot once before adopting. |
| G4 | Bind `roshan_base.png` (or the directional side profile) as identity in every Roshan job and name brown hair, tied rainbow ponytail and tiara in the action-first prompt; add M2/M4 wording (connected fin root, curl follow-through, arms near chest) and "no water or sparkle effects". |
| G5 | Every Roshan swim job states M1 (right-facing side view; the game mirrors for left). |
| G6 | Answered by the [shot-card audit](SHOT_CARD_AUDIT.md): V2 is the better template; `CLAUDE.md` and `AGENTS.md` change from V1 only on the owner's word (README Q8). |

### 11.2 Aseprite and local pipeline

| ID | Refinement |
|---|---|
| A1 | Keep the full native sequence (rich motion, owner 2026-10-04) and repair smeared frames with an Aseprite repaint or a temporal retake window; never thin frames to hide smear. Keep every native frame for provenance. |
| A2 | Write the timing (phases in seconds and guide frame indices) in the card before generating; guides come from it. |
| A3 | Register every source to its home pose and check fin and ponytail side (M3) before generation, as the waist-landmark registration already does for position. |
| A4 | Build a hand and socket reference per view (open hand, grip, pinch, two-hand hold, point, wave) from existing frames, used when Codex draws whole-figure contact keys, never as a limb pasted on a still body. |
| A5 | Move the pilot from the wave to the T1 water swim: the child sees travel all the time and the Grok test evidence already exists. |
| A6 | Stop the wave line unless a new method is chosen; record it as the reference that showed hand smear. |

### 11.3 Runtime playback (Codex)

| ID | Refinement |
|---|---|
| R1 | Stop the tail jumping on gestures: in gesture contexts use a home pose from the gesture family (fin right; for example `gesture_a` frame 0 or `gesture_c` row 2 frame 0) or add an authored two- or three-drawing fin swish between the directional home pose and the gesture. Choose after a side-by-side review; no mirroring trick. |
| R2 | Replace the castle cross-fade with authored breakdowns once clip 1 exists; meanwhile measure its cost with the overdraw meter and show the owner the swim with and without it. |
| R3 | Moved to the Phase B census: each career's loops are judged there and replaced with rich clips. |
| R4 | Remove the `twirl` mid-spin mirror swap now; authored holds wait for the rich gesture clips. |
| R5 | Replace the whole-sprite rotation wobble and scale breath with the M7 authored breath when it exists. |
| R6 | When clips 1–3 exist, make Day One jobs and the Sky Lagoon travel with them instead of sliding a still cutout. |

### 11.4 Governance

| ID | Refinement |
|---|---|
| D1 | Record the owner's 2026-10-04 answers in the owner decision register (done in revision 2); record the shared final-action sequence after README Q2. |
| D2 | Adopt the template's style rules as revision 2 of the movement language after the Phase A tests (README RM4). |
| D3 | Add one clip contract per canonical clip (Grand Puff format) under `design/animation/`. |

## 12. Owner questions

Answered on 2026-10-04 (verbatim in the
[README](README.md#owner-answers-2026-10-04)): Q1 yes, sprites need left and
right only; Q3 audit V2 (done: [SHOT_CARD_AUDIT.md](SHOT_CARD_AUDIT.md)) and
production runs through LTX locally by a Codex script with Aseprite into the
game; Q4 no, make a rich, comprehensive set; Q5 swimming, slower and more
modest; Q6 the uncommitted note is a work-in-progress rule. Q2 was unclear and
is re-asked in plain words with two new questions in
[README section 3](README.md#3-questions).

## 13. Evidence limits

- No runtime capture, device run or child session was made; the runtime
  descriptions come from code and committed images.
- Grok video was judged only through existing review records and one
  existing Codex board; the 26 unreviewed returns were not watched.
- The fin and ponytail measures are heuristics with stated thresholds;
  borderline rows are reported as such. The silhouette measure counts
  shape change and is not a judgement of appeal.
- The legacy player is migration debt; its gesture code is described because
  the Day One boss fight still uses it.
- Numbers come from `tools/measure_roshan_motion.py` at the baseline above;
  rerun it after any atlas or playback change.
