# Job minigame weakness register (cycle JC0, 2026-10-31)

- **Status:** `SUPPORTING_CURRENT` analysis for the next-generation job
  handoff. It accepts or rejects no game and cannot redefine a design rule.
  Owner decisions are cited by ID or by their dated words; every "next change"
  is Claude's proposal.
- **Baseline:** dev `a0bb2cf4691631a534e210a5fb60fd227213322f` (2026-10-31).
  The work branch head `511b0690` adds only Day Two documents, so the game code
  is identical.
- **Method:** record first. Every career's phase table, voice keys and the text
  of each recording were read in today's source; branch-only work was read from
  the named commits; dated records are quoted with their date. **[code]** marks
  a fact checked in today's source; **[record, date]** marks a fact quoted from
  a dated record and not re-run. Two large changes post-date most records: the
  Chapter 2 repair `1af25a20` (2026-10-14) and the painted job art (2026-10-19;
  Geologist 2026-10-17 to 31). The gold-star scores, assessed 2026-10-03, are
  therefore stale for every career.
- **Severity:** P0 stops the child; P1 clearly weakens the job; P2 polish.
- **Area:** a input and guidance; b play and agency; c art and staging; d
  voice; e lifecycle, save and tests; g records and governance.
- **Job lens:** six scores per career, 0 (missing), 1 (partial) or 2 (met),
  defined in [SELF_IMPROVEMENT_AUDIT.md](SELF_IMPROVEMENT_AUDIT.md#2-the-job-lens):
  JL1 the job's own skill and feel, JL2 Roshan does the job, JL3 the world is
  the control, JL4 growth rather than repetition, JL5 a job payoff, JL6 story
  truth.

## 1. The careers at a glance

Fifteen careers are live (`ACTIVE_STAR_MASK` `0x3BDEF`, retired bits 4, 9 and
14; `scripts/opera_house.gd:8-15`) **[code]**. Their free-play table has 61
phases with 36 distinct modes, and six shared gestures carry 31 of them: circle
7, hold 6, swipe 6, tap 6, choice 4 and pour 2
(`scripts/opera_career_world_2d.gd:263-355`) **[code]**. Day One locks every
career (`scripts/castle_career_routes.gd:204`). In Part 2 the eight party jobs
run in the fixed order Farmer, Chef, Candy Maker, Painter, Ballerina, Pop Star,
Astronaut, Detective (`scripts/chapter_two_party_plan.gd:8-20`, `GUIDE_ORDER`
`[6, 0, 3, 10, 2, 13, 11, 1]`) **[code]**; only the next job can start while
the story runs, and the other careers open as free play after the lawn
finale (demo audit section D).

Sorted by the JC0 job lens, weakest first:

| Career (save bit) | Where she starts it | Part 2 order | Gold star 10-03 (stale) | Lens JC0 (of 12) | Owner verdict |
|---|---|---|---|---|---|
| Racecar Driver (12) | Movie Lounge card, after the story | – | 15 | 2 | Rejected 2026-10-17 (`ODR-MINIGAME-REBUILD-20261017`); direction contested, see [RACER_VERSIONS.md](RACER_VERSIONS.md) |
| Pop Star (13) | Opera Hall gallery door | 6 | 13 | 2 | Rejected 2026-10-17; the note-memory echo is "a usable mechanic" |
| Ballerina (2) | Opera Hall foyer door; story from the Playroom nook | 5 | 14 | 3 | Rejected 2026-10-17 |
| Candy Maker (3) | Kitchen card | 3 | 10 | 4 | 2026-09-29: "Do not place it in the Kitchen" |
| Painter (10) | Craft Room card | 4 | 11 | 5 | None recorded |
| Detective (1) | Library card; story from the magic book | 8 | 9 | 6 | None recorded |
| Farmer (6) | Dining Room card | 1 | 11 | 6 | None recorded |
| Astronaut Engineer (11) | Mermaid Pool card | 7 | 10 | 6 | None recorded |
| Magician (8) | Opera Hall balcony door | – | 15 | 6 | None recorded |
| Pastry Chef (0) | Kitchen card | 2 | 10 | 7 | Not accepted 2026-10-03 (`ODR-CHEF-VERDICT-20261003`): "Chef pours backwards still", "lots of overdraw" |
| Stuffie Doctor (5) | Playroom card | – | 11 | 7 | None recorded |
| Boxer (7) | Playroom card | – | 16 | 7 | None recorded |
| Geologist (16) | Library card | – | 11 | 7 | None recorded |
| Teacher (17) | Library card | – | 15 | 8 | None recorded |
| Nursery Nurse (15) | Bubble Bath card | – | 14 | 9 | None recorded |
| Arborist Tree Book (practice, own save key) | Book on the Opera foyer floor | – | not catalogued | 7 | Follows the owner's 2026-09-29 corrections |

Every career is rated 1/5 on the gold star only because C1 was 0 at
assessment: "Free-play card appears only after Chapter 2, which cannot finish"
([`MA-PLAY-005`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-005),
since repaired in code but not yet proven on a fresh save). C11 and C12 are 0
everywhere ([gold-star page](../../../design/reference/GOLD_STAR.md)).

## 2. What the gold star does not see

The owner named Pop Star (13 of 24), Ballerina (14) and Racer (15) the weakest
careers on 2026-10-17, while the gold star ranks Detective (9), Astronaut (10),
Candy Maker (10) and Chef (10) lower. The rubric measures generic quality
(reach, true 2D, voice and pointer, input size, no-fail, truthful action, art,
feedback, lifecycle, probes). The owner judged whether the job's fantasy is
there at all: a beat for a performer, speed for a racer, a danced show for a
ballerina. The job lens (section 1 and
[SELF_IMPROVEMENT_AUDIT.md](SELF_IMPROVEMENT_AUDIT.md)) adds that judgement
beside the gold star, and the three owner-rejected careers are its three lowest
scores. That agreement is a fit to the verdict the lens was built from, not
proof; the next owner verdicts test it.

## 3. Register per career

Ordered as the work order treats them: the owner-rejected careers, then the
Part 2 jobs in play order, then the free-play careers.

### 3.1 Racecar Driver (bit 12)

**Today.** TUNE: circle the wrench around the wheel hub. TO THE LINE: swipe
the rear-view kart to the arch. RACE: two laps of about 24 s on a closed curve
over the still `world_racer` painting, where a finger anywhere on a 770×126 bar
drives and steers. The full history of every racing build is in
[RACER_VERSIONS.md](RACER_VERSIONS.md).

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-RACE-1 | P1 | b | Holding any point of the bar drives both laps, and the kart keeps going 2 s after the finger lifts: about 48 s of holding wins | **[code]** `scripts/opera_racer_surface.gd:13`, `:244-251` |
| JW-RACE-2 | P1 | b | Steering moves the kart at most about 19 px from the centre line, invisible at phone size | **[code]** `scripts/opera_racer_surface.gd:12`, `:119`; `scripts/kart_driving.gd:131-141` |
| JW-RACE-3 | P1 | b | The result is fixed: the rival runs at 0.94 of nominal pace with catch-up and only Roshan's finish ends the race; the `DL-INT-14` imp win is not built | **[code]** `scripts/opera_racer_surface.gd:297-314` |
| JW-RACE-4 | P1 | d | The only instruction says "Swipe to steer through the coral gates!": there are no gates and the control is a held bar. `DL-INT-10` names `op_racer_lap_two` ("Loop the loop! Draw big racing circles!"), also wrong | **[code]** `scripts/opera_career_world_2d.gd:334`; recording text in `assets/audio/voices/filler_v1/FILLER_MANIFEST.json`; [`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004) |
| JW-RACE-5 | P2 | c | Roshan is a cropped bust in a kart of at most 150 px; no camera, parallax or sense of speed; the bar, turbo, lap dials and lights are drawn in code | **[record, 2026-10-17]** [rebuild diagnosis §4](../codex_minigame_rebuilds_2026-10-17/DIAGNOSIS.md#4-racer-today) |
| JW-RACE-6 | P1 | g | Two owner directions conflict: the side-scroller (2026-10-18) and "integrate the superior game ... use the tracks that were generated from the various rooms in the castle" (2026-10-22, branch only). The 2026-10-03 priority to convert the existing racing engine is also branch only | [RACER_VERSIONS.md §2](RACER_VERSIONS.md#2-the-owners-words-on-racing) |

**Planned elsewhere.** Generation 1's Reef Grand Prix
([RACER.md](../codex_minigame_rebuilds_2026-10-17/RACER.md)); the parked
castle-room racer `codex/racer-castle-integration-20261022` (`96d6ef9e`); the
imp-contest branch `codex/opera-imp-contests-20260930` (`66420ae7`).

**Next change (proposal).** The combination R1 in
[RACER_VERSIONS.md §6](RACER_VERSIONS.md#6-the-recommended-combination-r1),
after the owner chooses (README Q2); package NG3.

**Lens.** JL1 0 (holding wins), JL2 0 (cropped bust), JL3 0 (a bar widget),
JL4 0 (chores, then two identical laps), JL5 1 (trophy curtain, generic win
line), JL6 1 (the "coral gates" line). Total 2.

### 3.2 Pop Star (bit 13)

**Today.** Opera Hall gallery door. A practice copy of SOUND CHECK, DANCE and
RHYTHM, then a stage of all four: hold the microphone, tap the lit lane, repeat
three code-drawn stars at any tempo, circle for the encore. The story (party
job 6) adds a still Rumi.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-POP-1 | P1 | b | No beat anywhere: the echo accepts any tempo; seven chores, three of them twice; Roshan never sings or plays | **[record, 2026-10-17]** [diagnosis §2](../codex_minigame_rebuilds_2026-10-17/DIAGNOSIS.md#2-pop-star-today); **[code]** `scripts/opera_performance_plan.gd:8-34` |
| JW-POP-2 | P1 | b | DANCE lights the answer lane, and a wrong lane still pays a crumb | **[code]** `scripts/opera_gesture_surface.gd:997-1002` |
| JW-POP-3 | P2 | d | The story's STAGE RUMI step plays the free-play "Tap the glowing dance arrow!"; other actions are silent; the win line is generic | **[code]** `scripts/chapter_two_career_scene_adapter.gd`; recording text |
| JW-POP-4 | P2 | c | Echo stars are code-drawn polygons; a dark ellipse over Rumi; the atlas ribbon reads as a second tail | **[record]** [job-art audit](../codex_job_art_imagegen_2026-10-17/AUDIT.md); [`MA-ROSHAN-005`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-roshan-005) |
| JW-POP-5 | P2 | e | The two-act probes are outside the trusted roster | **[record, 2026-10-03]** `design/reference/games.json` |

**Planned elsewhere.** Generation 1's MR1 (BeatKit) and MR2 (Roshan's Rainbow
Band), an owner-accepted direction (`ODR-POPSTAR-CORE-20261018`,
`ODR-POPSTAR-SONG-20261018`, `ODR-POPSTAR-BAND-20261018`). A foundation is
parked on `codex/popstar-rhythm-rebuild-20261022` (`7eada836`): `beat_kit.gd`,
the band state, an isolated concert preview and their probes; both bass-drum
pilot takes were rejected; its remote CI is pending.

**Next change (proposal).** After promotion, land BeatKit from that branch,
then MR2 (NG4).

**Lens.** JL1 1 (the echo is the one usable mechanic, but untimed), JL2 0,
JL3 0, JL4 0, JL5 0 (a cheer and a digit medal overlay, no finale song), JL6 1.
Total 2.

### 3.3 Ballerina (bit 2)

**Today.** Opera Hall foyer door. A practice copy of the three acts, then the
stage. PEARL MIRROR: an input-blocked demonstration taps the right portrait,
then she taps it. RIBBON TRAIL: trace one fixed curve. GRAND TWIRL: one turn
around a ring. The story (party job 5) is the stuffie version, started from
the Playroom nook.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-BAL-1 | P1 | b | The demonstration taps the answer before she can; the ribbon is fixed; nothing follows the 84 BPM waltz; Roshan holds still pose keys | **[record, 2026-10-17]** [diagnosis §3](../codex_minigame_rebuilds_2026-10-17/DIAGNOSIS.md#3-ballerina-today) |
| JW-BAL-2 | P1 | a | In the story, the stuffie picker opens over the ballet | **[record, 2026-10-31]** [demo audit](../codex_demo_readiness_2026-10-31/AUDIT.md) D2; demo package DR5 |
| JW-BAL-3 | P1 | b | The stage copy races a time-paced imp, against the "not a race" clause of `DL-INT-08`, until the contest lands; every act runs twice | **[code]** `scripts/opera_performance_plan.gd:8-34`; `scripts/opera_career_world_2d.gd:5233-5253` |
| JW-BAL-4 | P1 | d | The first instruction says "Hold still and watch the glowing dance!" and never says to tap; the tap line arrives only as a re-prompt | **[code]** `scripts/opera_career_world_2d.gd:283`; recording text; [`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004) |
| JW-BAL-5 | P2 | d | Story TWIRL and BOW reuse free-play lines ("Trace the ribbon across the floor!", "Draw circles for the grand twirl!") instead of lines about the stuffies and the bow | **[code]** adapter phases; recording text |
| JW-BAL-6 | P2 | c | Code-drawn shells, ribbon and ring; the tail is cut in the portraits; a dimming disc over wrong poses | **[record]** [job-art audit](../codex_job_art_imagegen_2026-10-17/AUDIT.md) |

**Canon.** The Day Two draft records the owner's 2026-09-30 words that the
show has no star until Lamma joins and unlocks it; generation 1's "Lamma's
Music-Box Ballet" fits that.

**Planned elsewhere.** Generation 1's MR3, an owner-accepted concept
(`ODR-BALLET-CONCEPT-20261018`); nothing is built.

**Next change (proposal).** The DR5 picker fix for the demo; after promotion,
MR3 on BeatKit (NG5).

**Lens.** JL1 0 (the demonstration decides), JL2 1, JL3 1, JL4 0 (every act
twice), JL5 0, JL6 1. Total 3.

### 3.4 Farmer (bit 6), Part 2 job 1

**Today.** Dining Room card. PLANT seeds; pull back and TOSS vegetables to a
piglet; HERD with a sweep; set a PICNIC. The story gathers five Sky Lagoon
berries (one button per berry), fills the basket and swipes it to the kitchen.
Painted garden, herd and picnic art landed on 2026-10-19.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-FARM-1 | P1 | a | The first party job is two doors away, and the voice promises a glowing door that never glows | **[record, 2026-10-31]** [demo audit](../codex_demo_readiness_2026-10-31/AUDIT.md) D3; demo package DR5 |
| JW-FARM-2 | P1 | c | The Sky Lagoon crop drops the meadow rows and leaves a horizon seam, so Roshan's path runs through the sky | **[code]** `scripts/opera_world_backdrop_2d.gd:156-169`; **[record, 2026-09-30]** GFX-FARM-01 and GFX-FARM-03 in the [Day Two graphics audit](../../../design/day_two_story_v2/06_GRAPHICS_AUDIT.md) |
| JW-FARM-3 | P2 | c | Picked berries stay behind as faint purple ghosts | **[code]** `scripts/opera_career_world_2d.gd:1050` |
| JW-FARM-4 | P2 | b | HERD and PICNIC are a sweep and a tap; a weak toss loops home and nothing rewards care; no action sounds | **[record, 2026-10-03]** `design/reference/games.json` farmer C5 and C8 |
| JW-FARM-5 | P2 | a | Holes 84 px, seed 92 px, vegetables 86 px | **[record, 2026-10-03]** games.json C4 |
| JW-FARM-6 | P2 | e | No free-play checkpoint | **[record, 2026-10-03]** games.json C9 |

**Planned elsewhere.** Contest FEEDING RACE; the Day Two draft's grove level
(CANDIDATE); DR5 adds the golden marker on the next door.

**Next change (proposal).** DR5's next-door marker is her first Part 2 step;
afterwards the crop seam and the ghost berries (NG7a).

**Lens.** JL1 1 (planting and the lob are farm skills; herd and picnic are
chores), JL2 1, JL3 1, JL4 1, JL5 1, JL6 1 (the glowing-door line). Total 6.

### 3.5 Pastry Chef (bit 0), Part 2 job 2

**Today.** Kitchen card. Roshan walks to the bowl and tips a jug (MIX), stirs
in circles (STIR), takes the cake out with the mitt when it is golden (BAKE),
traces frosting (FROST) and places toppings on sockets (TOP). The story swaps
TOP for STACK on the persistent cake. Painted oven states, tin, batter, piping
bag and toppings landed on 2026-10-19 (`c1429b10`).

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-CHEF-1 | P1 | c, b | The owner has not accepted the Chef: "Chef pours backwards still" and "Chef still looks bad, lots of overdraw". The painted art awaits his look; none is recorded | `ODR-CHEF-VERDICT-20261003`; [`MA-OPERA-001`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-001) |
| JW-CHEF-2 | P1 | a | In the story, each station's pointer is a 5 px pulsing dot under the object | **[code]** `scripts/opera_career_world_2d.gd:1990-1991`; `scripts/opera_world_hotspot_2d.gd:209-213` |
| JW-CHEF-3 | P1 | a | Small targets: frosting start 76×76, topping anchors 46 px | **[record, 2026-10-03]** games.json chef C4 |
| JW-CHEF-4 | P2 | e | No mid-act resume, and a held pour is not released on focus loss | **[record, 2026-10-03]** games.json chef C9 |
| JW-CHEF-5 | P2 | c | Two cakes and two bowls on screen in the story scene | **[record, 2026-09-30]** GFX-CHEF-02, GFX-CHEF-06 and GFX-CHEF-09 in the [Day Two graphics audit](../../../design/day_two_story_v2/06_GRAPHICS_AUDIT.md) |

**Planned elsewhere.** The loop review's Chef package CR0; the contest YUCKY
RECIPE (a defence contest, after the Chef repair); the Day Two draft's J4.

**Next change (proposal).** The owner looks at the painted Chef (it needs no
build) and his verdict is recorded; repairs follow his words (NG6).

**Lens.** JL1 1 (real cooking steps; the owner says the pour runs backwards),
JL2 1 (she walks to each station but holds pose keys), JL3 1 (world objects;
5 px story pointers), JL4 1, JL5 1, JL6 2. Total 7.

### 3.6 Candy Maker (bit 3), Part 2 job 3

**Today.** Kitchen card. SYRUP: tip the painted ladle into the mould, which is
strong and registered to the art (`DL-INT-11`); SORT: drag moving candies into
bins; WRAP: circle; SHARE: tap recipients. The story coats, sorts, glazes and
places five strawberries on the cake.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-CANDY-1 | P1, P0 suspected | a | The story steps take touches through an input surface drawn at alpha 0, while code-drawn berries move with progress. Story SORT asks her to drag an unseen moving candy into unseen bins; the gold-star audit called it "unsolvable", and the probe passes because it knows the coordinates | **[code]** `scripts/opera_career_world_2d.gd:2762-2774`, `:2135-2270`; **[record, 2026-10-03]** games.json candymaker C5; [`MA-OPERA-015`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-015) |
| JW-CANDY-2 | P1 | d | Story SORT says "Sort the strawberries by their matching color!", but all five berries use one texture | **[code]** `scripts/chapter_two_career_scene_adapter.gd:40`; `scripts/opera_career_world_2d.gd:2264-2269` |
| JW-CANDY-3 | P1 | g | On 2026-09-29 the owner ruled: "Candy Maker is reserved for a later section ... Do not place it in the Kitchen". The build keeps it in the Kitchen and as party job 3 | `design/ARBORIST_TREE_BOOK_HANDOFF_2026-09-29.md:8`; **[code]** `scripts/castle_career_routes.gd:21`; `scripts/chapter_two_party_plan.gd:11` |
| JW-CANDY-4 | P1 | a | Moving candy 84×84, bins about 102×79, SHARE anchors 46 px | **[record, 2026-10-03]** games.json C4 |
| JW-CANDY-5 | P2 | c | SORT, WRAP and SHARE are code shapes and the SHARE friends are stick figures; the owner chose "use extra stuffies", not yet built | `ODR-JOBART-SHARE-STUFFIES-20261018`; [job-art audit](../codex_job_art_imagegen_2026-10-17/AUDIT.md) |
| JW-CANDY-6 | P2 | e | No mid-act resume | **[record, 2026-10-03]** games.json C9 |

**Planned elsewhere.** Job-art P7 (local and uncommitted); contest SHARING
RACE; the Day Two draft replaces this job with the Arborist (CANDIDATE).

**Next change (proposal).** Bind the story touches to the drawn berries, tray
and cake, so the visible object is the hit region (pattern GS-05) (NG7b). Its
place in the story waits on the Day Two decision (README Q6).

**Lens.** JL1 1 (the pour is the job; sort, wrap and share are chores), JL2 1,
JL3 0 (invisible story input), JL4 1, JL5 1, JL6 0 (the colour line and the
owner's placement ruling). Total 4.

### 3.7 Painter (bit 10), Part 2 job 4

**Today.** Craft Room card. PAINT: brush a cloudy cover off a fixed sunrise;
STAMPS: place any five stamps; GALLERY: pick the frame lane. The story paints,
stamps and hangs the Main Hall banner.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-PAINT-1 | P1 | b | Nothing she makes is kept: PAINT uncovers a fixed picture, STAMPS pays any five taps so mashing equals play, GALLERY is one lane pick | **[code]** `scripts/opera_career_world_2d.gd:322-326`; **[record, 2026-10-03]** games.json painter C5 and C6 |
| JW-PAINT-2 | P2 | d | Story STAMP plays "Add any five bright finishing stamps!" for "Stamp bright birthday stars on the banner!" | **[code]** adapter phases; recording text |
| JW-PAINT-3 | P2 | c | Story PAINT still shows the sunrise frame and easel, not the Main Hall banner (partly addressed since) | **[record, 2026-09-30]** GFX-PAINT-02 to GFX-PAINT-05 in the [Day Two graphics audit](../../../design/day_two_story_v2/06_GRAPHICS_AUDIT.md) |
| JW-PAINT-4 | P2 | e | No checkpoint; the reveal is checked only along the route | **[record, 2026-10-03]** games.json C9 and C10 |

**Planned elsewhere.** Contest PAINT-OFF; the standalone Painter engine
prototype (`scenes/painter_prototype.tscn`,
`design/PAINTER_ENGINE_PROTOTYPE_2026-09-16.md`, proposed); the Day Two
draft's J5.

**Next change (proposal).** Keep her marks: the prototype's closed-region fill,
or at least her stamps kept on the banner she hangs (NG7c).

**Lens.** JL1 0 (she uncovers a fixed picture), JL2 1, JL3 1, JL4 1, JL5 1,
JL6 1. Total 5.

### 3.8 Astronaut Engineer (bit 11), Part 2 job 7

**Today.** Mermaid Pool card. PIPES: route tiles from the tank to the rocket
over three boards; PATCH: tap the leaks; VALVE: circle; LAUNCH: hold. The
story builds, patches and turns the valve, then parks the rocket unlaunched.
Painted pipes, tank, patches and flames landed on 2026-10-19 (`90508b85`).

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-ASTRO-1 | P1 | e, a | A second finger could lose a pipe tile; the ownership guard exists but every round, cancel and re-entry are unproven | [`MA-OPERA-013`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-013); **[code]** `scripts/opera_gesture_surface.gd:1287-1305` |
| JW-ASTRO-2 | P1 | d | LAUNCH says "Hold through the countdown and launch!", and no countdown exists | **[code]** `scripts/opera_career_world_2d.gd:329`; no countdown in the Astronaut code; [`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004) |
| JW-ASTRO-3 | P2 | d | Story VALVE plays "Draw circles to turn the launch valve!" for "Turn the launch valve, but keep the rocket parked!" | **[code]** adapter phases; recording text |
| JW-ASTRO-4 | P2 | a | Tray tiles 84 px, patch spots 92 px | **[record, 2026-10-03]** games.json astronaut C4 |
| JW-ASTRO-5 | P2 | c | Spotlight wedges are still drawn over the painted room | **[code]** `scripts/opera_world_backdrop_2d.gd:316-317` |
| JW-ASTRO-6 | P2 | g | The Day Two draft gives the Astronaut the invitations (the August ruling, restated 2026-09-30); the build has it building the candle rocket as job 7. Waits on the Day Two decision | `design/day_two_story_v2/01_STORY_BIBLE.md` section 12 (CANDIDATE) |

**Planned elsewhere.** Contest LAUNCH RACE; the Day Two draft's J1
invitations (CANDIDATE).

**Next change (proposal).** A real two-finger probe across every pipe round
with cancel and re-entry, which closes the last recorded soft-lock risk; a
countdown that exists, or a line that does not promise one (NG7d).

**Lens.** JL1 1 (the pipe puzzle is engineering; valve and launch are chores),
JL2 1, JL3 1, JL4 1 (three boards), JL5 1, JL6 1 (the countdown line). Total 6.

### 3.9 Detective (bit 1), Part 2 job 8

**Today.** Library card. SEARCH: sweep a real magnifier to find three clues;
CASE BOARD: match the clues; CROWN: tap the crown chest. The story sweeps the
lens over the storybook, then a tap board, then the unlit candle.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-DET-1 | P1 | b | A timed rival takes finished work away: rival cap 1.0, par 40 s, `timed_retry`; when its reveal ends the phase returns to the finale with zero progress. The gold star scored C5 0 | **[code]** `scripts/opera_competition.gd:21-29`, `:232-234`; `scripts/opera_career_world_2d.gd:3877-3891`, `:4812-4826` |
| JW-DET-2 | P1, P0 suspected | a | The story candle's touch box (x 760 to 916, y 145 to 335) and the drawn candle (art box about x 815 to 987, y 252 to 424, centre about 901, 338) only partly overlap: a tap on the lower half of the candle misses | **[code]** `scripts/opera_career_world_2d.gd:920-942`; `scripts/chapter_two_rainbow_candle_2d.gd:23-25`, `:102-110`; [`MA-OPERA-015`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-015) |
| JW-DET-3 | P1 | a, d | The story board takes taps through an invisible surface and pays any three taps; its recording says "Match each clue to the glowing place!" for "Tap each glowing storybook clue on the board!" | **[code]** `scripts/opera_career_world_2d.gd:2762-2774`; adapter phases; recording text; [`MA-OPERA-015`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-015), [`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004) |
| JW-DET-4 | P1 | b | In story runs the rival race still begins at the last phase, because the story's finale index is clamped to it; a free-play rival line can play | **[code]** `scripts/opera_career_world_2d.gd:3325-3333`, `:2727-2729`; **[record, 2026-10-31]** demo audit D6 |
| JW-DET-5 | P1 | c, b | The "missing" crown is still painted in the scene | [`MA-OPERA-002`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-002) |
| JW-DET-6 | P1 | c | The world painting fills about 28% of the screen, and lens objects were placed for older art | **[record, 2026-09-30]** GFX-SYS-02 and GFX-DET-02 in the [Day Two graphics audit](../../../design/day_two_story_v2/06_GRAPHICS_AUDIT.md) |
| JW-DET-7 | P2 | e | The rival clock keeps running on focus loss (only two-act careers pause it) | **[code]** `scripts/opera_career_world_2d.gd:5137-5145` |

**Planned elsewhere.** Contest SPARKLE RACE retires the timed retry (a W3
pilot, not built); job-art P7 (local); the Day Two draft moves the story level
into the Library (CANDIDATE).

**Next change (proposal).** Remove the timed retry's reset and the rival race
from story runs; fit the candle's touch box to the drawn candle; draw the story
board's targets (NG7e).

**Lens.** JL1 1 (searching with the lens is detective work; the rival takes it
away), JL2 1, JL3 1, JL4 1, JL5 1, JL6 1 (the painted "missing" crown). Total 6.

### 3.10 Magician (bit 8)

**Today.** Opera Hall balcony door. A practice copy of VANISH, TRACK and ROPE,
then the stage of all five: hold the wand to hide Lamba (VANISH), follow the
hat through the shuffle (TRACK), trace the rope (ROPE), pull the cabinet down
(CABINET), circle the portal (PORTAL). Painted hats, rope and portal landed on
2026-10-19.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-MAG-1 | P1 | b | TRACK scores taps during the 1.5 s glide and pays crumbs for wrong hats; the choice press never checks whether the hats are still moving | **[code]** `scripts/opera_gesture_surface.gd:997-1002` |
| JW-MAG-2 | P1 | b | Hall repetition: eight phase runs, practice copies included; the stage race is paced by time, not by her input, and the imp can finish first | **[code]** `scripts/opera_performance_plan.gd:9-14`; `scripts/opera_career_world_2d.gd:5233-5253` |
| JW-MAG-3 | P2 | a | Rope start 76 px; practice cabinet handle about 138×86 | **[record, 2026-10-03]** games.json magician C4 |
| JW-MAG-4 | P2 | c | Encore tokens and medal digits in a code overlay; the tokens have no use anywhere | **[code]** `scripts/opera_performance_overlay.gd` |
| JW-MAG-5 | P2 | d | `MA-ACCESS-002` (the old "bunny-fish" recordings) may be stale for the current route; needs a listening check | [`MA-ACCESS-002`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-002) |
| JW-MAG-6 | P2 | e | Medal and checkpoint probes are outside the trusted roster | **[record, 2026-10-03]** games.json C10 |

**Planned elsewhere.** Contest HAT DUEL, which ignores glide taps (a W3
pilot, not built).

**Next change (proposal).** Ignore TRACK taps while the hats glide and stop
paying crumbs for wrong hats (NG8b).

**Lens.** JL1 1 (tracking the hat is the trick; vanish, rope and portal are
hold, swipe and circle chores), JL2 1, JL3 1, JL4 0 (practice copies), JL5 1,
JL6 2. Total 6.

### 3.11 Stuffie Doctor (bit 5)

**Today.** Playroom card, free play only. WASH: hold at the basin; FIND: pick
the plushy with the glowing ouch; X-RAY: drag the scanner over the sore spots;
CAST: circle; BANDAGE: trace. Painted basin, scanner, patient and bubbles
landed on 2026-10-19 (`9c78f6aa`).

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-DOC-1 | P1 | b | FIND can be mashed (a wrong lane pays a crumb); nothing rewards care | **[code]** `scripts/opera_gesture_surface.gd:997-1002`; **[record, 2026-10-03]** games.json doctor C5 |
| JW-DOC-2 | P1 | a | The X-ray stroke must pass within about 28 px | **[record, 2026-10-03]** games.json doctor C4 |
| JW-DOC-3 | P2 | b | Play happens on a panel beside the station, not on the patient Roshan reached | **[record, 2026-10-03]** games.json doctor C6; [`MA-PLAY-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-004) |
| JW-DOC-4 | P2 | g | The setting (above water) is an open owner decision | [`MA-OPERA-007`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-007) |
| JW-DOC-5 | P2 | e | No mid-job checkpoint; a dead Chapter 2 phase set remains, whose X-RAY recording says "Tap the glowing cracked bone!" | **[code]** `scripts/chapter_two_career_scene_adapter.gd:44-49` |

**Planned elsewhere.** Contest BANDAGE RACE.

**Next change (proposal).** Take the crumb pay out of FIND and let care pay:
the plushy reacts when the right ouch is chosen (NG8c).

**Lens.** JL1 1 (the X-ray and finding the ouch are doctor work; wash, cast and
bandage are chores), JL2 1 (acts on a panel), JL3 1, JL4 1, JL5 1, JL6 2.
Total 7.

### 3.12 Boxer (bit 7)

**Today.** Playroom card. A first-person, two-glove surface where Roshan is
hidden once it opens: push a glove to the mitt (GLOVE GUIDE), jab the glowing
pads (JAB PRACTICE), guard in a bubble (SOFT GUARD), punch when the star opens
against one padded imp (TITLE IMP), punch the belt (BELT). Per-finger
ownership, no loss. Painted gloves landed on 2026-10-19; the surface draws no
primitives.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-BOX-1 | P1 | d | The first instruction is wrong: GLOVE GUIDE plays "Bounce and duck! I'm getting good at this!", and the caption is hidden because the recording exists | **[code]** `scripts/opera_career_world_2d.gd:307`; `scripts/audio_director.gd:561-594`; recording text; [`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004) |
| JW-BOX-2 | P2 | a | A press claims the nearest glove with no distance cutoff | **[record, 2026-10-12]** Luna L17 |
| JW-BOX-3 | P2 | b | Roshan is hidden during play; the targets float at fixed points | **[record, 2026-10-03]** games.json boxer C6 |
| JW-BOX-4 | P2 | e | No mid-run resume; external acceptance pending | [`MA-OPERA-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-009) |

**Planned elsewhere.** Contest TITLE BOUT (first to six; the imp may win).

**Next change (proposal).** A true GLOVE GUIDE instruction: until a new
recording exists after the freeze, play no recording so the caption returns for
the grown-up (NG9a), then record the exact line (NG8a).

**Lens.** JL1 2 (punch when the target opens), JL2 0 (Roshan hidden), JL3 2,
JL4 1, JL5 1, JL6 1 (the first line). Total 7.

### 3.13 Geologist (bit 16)

**Today.** Library card, cooperative with a Field Guide Imp. RIVER: dig a
connected water channel; FOSSIL: brush and assemble a fossil; PAN: swish gravel
back and forth; GEODE: tap five seams and pull it open. Strong engineering:
ownership, checkpoint, award-once. Painted pan, minerals, fossil, river pools,
seams, shell and props landed between 2026-10-17 and 2026-10-31.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-GEO-1 | P1 | d | RIVER, PAN and GEODE each play "A secret grotto! The stones want to play!", which instructs nothing. (FOSSIL's borrowed "Brush it back and forth. Swish, swish!" fits its step) | **[code]** `scripts/opera_career_world_2d.gd:349-354`; recording text; [`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004) |
| JW-GEO-2 | P1 | c | The room is still the code-drawn fallback (no `world_geologist` painting) | **[code]** `scripts/opera_world_backdrop_2d.gd:328-367` |
| JW-GEO-3 | P2 | d | The win caption adds "for the nursery team!", because every cooperative career is treated as the Nursery | **[code]** `scripts/opera_act.gd:159-160`; `scripts/opera_career_world_2d.gd:3985-3988` |
| JW-GEO-4 | P2 | b | Wrong digging gets no explanation; nine pan reversals may tire her; the partner is frozen | **[record, 2026-10-03]** games.json C5; Luna L31 |
| JW-GEO-5 | P2 | e | Its music cue is missing from the build tool's list; its sheet is outside the atlas gate | `tools/build_area_music.py`; `tools/audit_opera_roshan_animation.py:25-39` |

**Planned elsewhere.** Contest GEODE RACE; a painted cave background.

**Next change (proposal).** Play no recording for RIVER, PAN and GEODE until
four exact lines are recorded after the freeze (NG9a, NG8e); fix the win caption.

**Lens.** JL1 2 (dig, brush, wash, crack: the material changes), JL2 1, JL3 2,
JL4 1, JL5 1, JL6 0 (three untrue lines and the nursery caption). Total 7.

### 3.14 Teacher (bit 17)

**Today.** Library card. One adaptive question each for PATTERN, COUNT, ADD
and MATCH, with three difficulty tiers and three clean wins to move up
(`scripts/teacher_lesson_plan.gd:6-58`). Every counted pearl is spoken; help
never inflates mastery; there is a per-phase checkpoint. Painted board, shapes,
pearls and cards landed on 2026-10-19.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-TEACH-1 | P1 | a | Pearls are 72 px circles 88 px apart; the help button is 80 px; a 38 px drift discards the tap | **[code]** `scripts/opera_teacher_surface.gd:156-170`; Luna L18 |
| JW-TEACH-2 | P2 | b | She answers the questions as the pupil; the job's fantasy, teaching, arrives only with the planned IMP'S LESSON contest, where she corrects the imp | **[code]** `PHASES` teacher rows; [imp contest design](../codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md) |
| JW-TEACH-3 | P2 | d | The win line thanks a "learning buddy" who never appears | **[code]** `scripts/opera_house.gd:149`; `scripts/opera_career_world_2d.gd:3357-3363` |
| JW-TEACH-4 | P2 | d | The idle help line is queued and then cleared, so it is never spoken | **[record, 2026-10-03]** games.json teacher C8 |
| JW-TEACH-5 | P2 | e | No Teacher-specific probe; its sheet is outside the atlas gate | **[record, 2026-10-18]** job-art README, P2 |

**Planned elsewhere.** The inverted contest IMP'S LESSON (silly mistakes she
fixes; it cannot be lost).

**Next change (proposal).** Larger pearl hit regions from a layout that does
not overlap them (NG8f).

**Lens.** JL1 1 (a real learning skill, but she is the pupil), JL2 1, JL3 2,
JL4 2 (adaptive tiers), JL5 1, JL6 1 (the absent buddy). Total 8.

### 3.15 Nursery Nurse (bit 15)

**Today.** Bubble Bath card, cooperative with Faron, who speaks in protected
family recordings. Hold the basin (WASH HANDS); slide the cradle under five
falling babies, with pillows and mercy after two misses (CATCH); hold the
bottle (FEED); pat slowly, gated at 0.55 s (BURP); swipe the blankets down
(BEDTIME). Wash and care frames, cradle and pillows were wired on 2026-10-19
(`ODR-JOBART-NURSERY-FRAMES-20261018`).

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-NURSE-1 | P2 | a | Blanket grab about 88×76; held WASH and FEED have no focus-loss cancel | **[record, 2026-10-03]** games.json nursery C4 and C9; **[code]** `scripts/opera_career_world_2d.gd:5137-5145` |
| JW-NURSE-2 | P2 | a | A catch needs a recent press or drag at the moment of contact, so one placement may not count | **[record, 2026-10-12]** Luna L21 |
| JW-NURSE-3 | P2 | b | BURP pays a tap anywhere; Faron is frozen in one pose | **[record, 2026-10-03]** games.json C6 |
| JW-NURSE-4 | P2 | e | No resume; the grouped Nursery subclaims are unsplit | [`MA-OPERA-003`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-003), [`MA-OPERA-006`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-006) |

**Planned elsewhere.** Contest QUIET TIME (a defence contest with plain imps).

**Next change (proposal).** Faron reaction poses and the pat landing on the
baby itself, keeping the strongest cooperative career strong (NG8d).

**Lens.** JL1 2, JL2 1 (care frames for some steps; verify each), JL3 2, JL4 1,
JL5 1, JL6 2. Total 9.

### 3.16 Arborist Tree Book (practice, not a career)

**Today.** From the book on the Opera foyer floor: three book decisions (tree,
diseased leaf, medicine) with four choices each, then hold to spray. No star;
its own save key (`design/OPERA_TREE_BOOK_TEST_2026-09-30.md`). It follows the
owner's 2026-09-29 corrections.

| ID | Sev | Area | Weakness | Evidence |
|---|---|---|---|---|
| JW-ARB-1 | P1 | c | The tree choices have no alpha, so navy boxes give the answer away | **[record, 2026-10-18]** JA-ARB-02 in the [job-art audit](../codex_job_art_imagegen_2026-10-17/AUDIT.md) |
| JW-ARB-2 | P1 | b | Spraying lacks hand contact; the fix is parked on `codex/arborist-spray-20261015` (`941cb76d`) | [`MA-PLAY-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-004); demo README section 4 |
| JW-ARB-3 | P2 | c | An upscaled background, a flat mint screen, one patient, an on-screen text label | **[record, 2026-09-30]** `design/OPERA_TREE_BOOK_TEST_2026-09-30.md` |

**Next change (proposal).** Land the parked spray fix after promotion (NG2),
then alpha on the tree choices (NG8g).

**Lens.** JL1 1, JL2 1, JL3 1, JL4 1, JL5 1, JL6 2. Total 7.

## 4. Weaknesses every career shares

| ID | Weakness | Evidence | Package |
|---|---|---|---|
| JX-1 | **The spoken instruction can be wrong, and then it is the only one.** In the Opera an exact recording hides the caption, so a phase whose recording says something else leaves a non-reader with a wrong instruction: Boxer GLOVE GUIDE, Geologist RIVER, PAN and GEODE, Racer RACE, Ballerina PEARL MIRROR, Astronaut LAUNCH and the story's Detective board | **[code]** `scripts/audio_director.gd:561-594`; phase tables; recording text; [`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004) | NG9a |
| JX-2 | **Invisible story input.** Chapter 2 Candy Maker and Detective take touches through a surface at alpha 0 over props that do not show the targets | **[code]** `scripts/opera_career_world_2d.gd:2762-2774`; [`MA-OPERA-015`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-015) | NG7b, NG7e |
| JX-3 | **One shell for every job.** Six shared gestures carry 31 of 61 phases; in most careers Roshan stands beside a panel instead of acting at the object; the Boxer hides her and the Racer crops her | **[code]** phase table; [`MA-PLAY-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-004); `DL-INT-07` | NG3 to NG8 |
| JX-4 | **The rival pacer.** A wall-clock meter capped below the finish and hidden until the finale; in the room he is a statue. The Detective's is harsh; the Hall careers' runs on time, not input; story runs still start it at the last phase. The owner's imp contests (`DL-INT-14`) are not built | **[code]** `scripts/opera_competition.gd`; `scripts/opera_career_world_2d.gd:2727-2729`, `:3325-3333`; [contest design](../codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md) | NG9c |
| JX-5 | **A generic payoff.** In free play every career's win plays the generic recording "Yay! I did it!" (the two-act careers a pitched yay); in story runs the win line is caption-only, so a non-reader hears nothing; no career's own win line is spoken. The Hall medal overlay shows digits and its tokens have no use | **[code]** `scripts/opera_act.gd:150-176`; recording text of `roshan_win`; `scripts/opera_performance_overlay.gd` | NG9b |
| JX-6 | **Wrong taps pay.** Choice, timing, echo and oven modes pay a crumb for a wrong tap, so mashing makes progress | **[code]** `scripts/opera_gesture_surface.gd:414-419`, `:997-1002` | NG9d |
| JX-7 | **Held input survives focus loss.** The shared surface owns one touch but does not cancel a held one on focus loss; only two-act careers pause the rival | **[code]** `scripts/opera_gesture_surface.gd:1287-1305`; `scripts/opera_career_world_2d.gd:5137-5145` | NG9d |
| JX-8 | **Ten careers restart from the beginning.** Only the Hall careers, Teacher, Geologist and Chapter 2 resume mid-act; the checkpoint validators cap the phase index at 4; the `opera_stars` clamp of 262143 would corrupt every career if an 18th bit were added | **[code]** `scripts/save_state.gd:198`, `:303`, `:629`, `:691`; [takeover audit](../../../audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30.md) | NG9e |
| JX-9 | **Shared art layers.** Spotlight wedges, code halos, ambient doodles above every career, default progress bars; most padded backdrops show the blurred frame | **[record, 2026-10-18]** [job-art audit](../codex_job_art_imagegen_2026-10-17/AUDIT.md) P8; [`MA-VIS-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-008), [`MA-VIS-010`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-010) | Job-art P8 |
| JX-10 | **Tests reach little.** Many trusted probes call internals or the probe gesture; the pacing sensor measures 4 of 15 careers; the Hall mastery and performance probes are outside the trusted roster; no device or child evidence exists for any career | [`MA-CI-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-008); [`MA-CHILD-001`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-child-001); [`MA-PERF-001`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-perf-001) | NG11, NG12 |
| JX-11 | **Records drift from the code.** `DL-INT-07` states 13 careers, 53 phases and 27 modes (the code has 15, 61 and 36); `DL-INT-12` lists 13 careers; `DL-SAVE-06` says 16 slots against 18 bits; owner directions sit unapplied or only on branches (the 2026-09-29 Candy Maker ruling; the 2026-10-03 and 2026-10-22 racing directions); the Job Platform is not built (about 25 files are hand-edited per job) | **[code]** phase table; `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`; [`MA-DOC-006`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-006) | NG10 |

## 5. Records found stale while auditing

Corrected in this change: the ledger row for the rebuild handoff's Pop Star
specification still said it was pending the owner's answers (they were given on
2026-10-18), and the Racer specification's row now notes that its direction is
contested. Left for their owners, with the evidence above: the job-art ledger
row names revision 3 of a revision-4 README; the demo receipt's status note
still calls Q1 to Q8 open; the rebuild handoff's revision 2 has no recorded
remote verification; `MA-ACCESS-002` may be stale for the Magician's current
route; the gold-star C1, C4 and C7 scores predate the Chapter 2 repair and the
painted art.
