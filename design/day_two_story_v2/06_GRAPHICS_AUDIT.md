# 06 — Graphics audit

Part of the [Day Two story draft v2](README.md). Status: `CANDIDATE` audit,
2026-09-30, at repository head `b3d168f9` (art and scripts unchanged since
`e7899cc0`). Nothing here is owner, device or child acceptance.

This audit covers every picture a child sees in Day Two, from the Day Two
card to the lawn finale. It also covers the Opera career worlds that host each
job's practice, and the character and prop art Day Two reuses. Each flaw has
an ID, a severity, its evidence, and a written fix.

## How to read it

**Evidence labels.** Each finding says how it was established:

| Label | Meaning |
|---|---|
| **V** | Viewed: I opened the asset or an engine capture and looked at it |
| **H** | A historical engine capture whose art and script are unchanged since it was taken (the Opera baseline of 2026-09-05; the lawn scale-v2 captures of 2026-09-06) |
| **M** | Measured with a pixel script (sizes, alpha, edge detail) |
| **C** | Read in code, with file and line |
| **R** | A reconstruction from source pixels and script coordinates, made by a research pass. It is not an engine capture: take a capture before fixing |

**Severity.**

- **P0:** breaks the scene for a four-year-old. It is unreadable,
  misleading, hides the key object, looks broken, or contradicts the story at
  its key moment.
- **P1:** a clearly visible flaw that weakens story, identity or quality.
- **P2:** polish.

**Disposition.** Draft v2 moves each job's second level into the game world
and keeps the Opera career worlds for Level 1 practice and freeplay. So some
flaws are worth fixing now and some disappear when their scene is replaced:

- **Fix now:** affects freeplay, the Level 1 practice, the finale, or a
  child's ability to finish today.
- **With WP-nn:** fixed as part of the named work package in
  [07](07_WORK_PACKAGES.md).
- **Retire:** the scene is replaced by the v2 rebuild; do not spend art time
  on it, but carry the lesson into the new level.
- **Owner:** needs an owner decision first.

**Rules for every fix.**

- Protected art is never edited: `assets/book/`, `assets/audio/voices/` and
  `assets/characters/friends/`. Fixes use staging, overlays, or
  owner-approved derivatives saved as new files, with the originals untouched.
- Approved identities are not redesigned: Roshan (`roshan_25d`), the Ember
  King (V4 and the owner reference), the Ember Prince (identity card), Grand
  Puff and the rainbow friend, and Baby Eagle.
- Rumi is on IP hold: she gets no new frames, no regeneration and no voice.
- Derivatives get source hashes, a provenance note and an
  `ASSET_LICENSES.md` line. New textures are at most 1024 px on the longest
  side, or power-of-two.
- Everything stays 2D Canvas under the Mobile renderer: no 3D, no lights.
- No fix may add words a child must read.
- Every fix is checked with before and after captures at 16:9 and 20:9.

## The fixes that matter most

| Order | ID | Why first |
|---|---|---|
| 1 | [GFX-DET-03](#gfx-det-03) | The Detective's candle touch area misses the candle, so the job may be unfinishable by touch. A one-line fix |
| 2 | [GFX-SYS-13](#gfx-sys-13), GFX-ROOM-06, [GFX-LAWN-19](#gfx-lawn-19) | The pointers fail: 19 of 29 job steps show none (build audit B1), no castle door lights for the next job, and the lawn's hand lands 55 px right of and 85 px below every target |
| 3 | [GFX-SYS-01](#gfx-sys-01) | A blurred frame surrounds every career world, freeplay included. Fixable with no new art |
| 4 | [GFX-SYS-02](#gfx-sys-02) | The Detective world is a postage stamp, and every lens target sits off the painting |
| 5 | [GFX-LAWN-01](#gfx-lawn-01) | Code-drawn party hats cover friends' faces, including a protected family portrait |
| 6 | [GFX-LAWN-07](#gfx-lawn-07) | The day's payoff, lighting the candle, is a 7 px dot and a 20 px flame |
| 7 | [GFX-CHAR-KING-01](#gfx-char-king-01) | The King never moves; demand, battle and theft all use one static pose |
| 8 | [GFX-LAWN-08](#gfx-lawn-08) | The stomp warning is a faint orange ellipse on yellow-green grass |
| 9 | [GFX-SYS-12](#gfx-sys-12) | Words stand in for pictures: "DAY TWO!", "Happy Birthday, Roshan!", screenplay captions |
| 10 | [GFX-LAMMA-01](#gfx-lamma-01) | Lamma has two different designs; settle one before she is staged anywhere |
| 11 | [GFX-SYS-03](#gfx-sys-03) | A see-through stripe runs down Roshan's tail in all eight costume sheets |
| 12 | [GFX-PROP-CAKE-01](#gfx-prop-cake-01) | The cake reads as five tiers, and its five strawberries are too small to count |
| 13 | [GFX-HALL-07](#gfx-hall-07) | The Main Hall party table is glued to the screen and slides across the doors as the hall scrolls |
| 14 | [GFX-HALL-08](#gfx-hall-08) | In the Main Hall the cake hides the candle the whole day is about |

## 1. Cross-cutting flaws

<a id="gfx-sys-01"></a>
**GFX-SYS-01 — Blurred frame around every career world.** P0. Evidence V,
H, M, C. Fix now.

- **Where:** `assets/opera/worlds/backdrops/world_{chef,candymaker,painter,popstar,astronaut}_c{0,1}r{0,1}.png`,
  drawn by `scripts/opera_world_backdrop_2d.gd` (`_draw_tile_set`).
- **What is wrong:** the 2048 px "masters" are a 1672×941 native painting
  padded with a smeared blur ("ImageGen native + non-subject edge
  continuation" in
  `assets_src/concepts/opera_regeneration_2026-08-01/OPERA_CODEX_MANIFEST_2026-08-02.json`;
  the native rectangle is recorded in code for Racer at
  `opera_world_backdrop_2d.gd:188-190`).
  - At runtime the sharp painting covers only about 1045×588 of the 1280×720
    screen (66%): exactly 1672×941 at the tiles' 0.625 scale.
  - Around it runs a blurred band, about 120 px at each side and 66 px at top
    and bottom, ending at a hard seam. The Chef world's top valance is cut
    in a straight line.
  - Measured edge detail in the outer band is five to ten times lower than
    in the centre, in all six worlds measured (the Detective's included).
  - The Opera baseline captures (`chef_01_pourt.png`, `painter_01_paint_reveal.png`,
    `astronaut_01_pipe.png`, `popstar_03_echo.png`) look like a letterboxed
    video with a blurred pillarbox, not a storybook world.
  - Roshan, props, panels and the pause button are often staged over the
    blur.
- **Fix:**
  1. Draw only the native painting rectangle, full-bleed, for every career.
     Generalise the path Racer driving already uses (`_draw_racer_circuit`,
     `opera_world_backdrop_2d.gd:187-198`), reading each career's native
     rectangle from the promotion manifest. 1672×941 to 1280×720 is a 0.77×
     reduction, so it stays crisp.
  2. Set `StagePaths.BLEED` to `[0, 1]`. Re-measure every station, path and
     clue spot once, on both axes, with `tools/measure_opera_bleed.py`. The
     current remap corrects x only, although the band is also on y.
  3. Keep the padded tiles only as provenance. No new pixels, no relighting.
- **Acceptance:** a probe fails if more than 5% of a career frame has low
  edge detail; captures at 16:9 and 20:9.

<a id="gfx-sys-02"></a>
**GFX-SYS-02 — The Detective world is a postage stamp.** P0. Evidence V, H,
C. Fix now.

- **Where:** `world_detective_c{0,1}r{0,1}.png`, replaced on 2026-08-29
  (`a89599c8`).
- **What is wrong:** the painting fills about 657×390 px (28% of the
  screen), nested inside a blur halo, flat navy bands and a second blurred
  pillarbox: a triple frame. `StagePaths.BLEED["detective"]` and
  `DETECTIVE_ROOM_OBJECTS` were measured against the old full-frame art, so
  every lens target and station now sits on the padding. In the baseline
  capture Roshan floats in the blur at the left.
- **Fix:** restore the tiles from before `a89599c8`, or draw only the native
  painting full-screen (about 1.2× enlargement). Then re-derive the bleed,
  paths and lens objects from that frame. In v2 the Detective's second level
  moves to the Royal Library ([03 J8](03_LEVEL_DESIGN.md)), but this world
  stays for freeplay and the J8 practice.

<a id="gfx-sys-03"></a>
**GFX-SYS-03 — See-through stripe down Roshan's tail in eight costume
sheets.** P1. Evidence M, V. Fix now.

- **Where:** `assets/opera/worlds/actors/animation/roshan_{farmer,chef,candymaker,painter,ballerina,popstar,astronaut,detective}_sheet_a.png`.
- **What is wrong:** each sheet has 7,500 to 10,000 half-transparent pixels
  inside the silhouette; the Teacher sheet has 767. Mapped out, they form a
  vertical stripe along the green band of the rainbow tail in every cell:
  green-screen keying damage. Over light floors it shows as a dark seam; over
  dark floors the background shows through the tail.
- **Fix:** make derivative sheets. Set alpha to fully opaque for pixels
  enclosed by the silhouette on the tail band, keeping true openings (the
  magnifier glass, the helmet visor, the sheer Pop Star skirt). Pull the
  green spill in the 1-2 px edge band toward the outline colour. Keep the
  same cells and pivots so no code changes. Run the existing Roshan clipping
  and ghost gate, which checks cell edges but not this.

<a id="gfx-sys-04"></a>
**GFX-SYS-04 — Costume sheets drift from Roshan's approved look.** P1.
Evidence V. Owner ([decision 10](README.md#owner-decisions)).

- **What is wrong:** the approved Roshan (`assets/characters/roshan_25d/roshan_base.png`)
  has shoulder-length wavy hair, a small rainbow streak, a lilac sparkle tail
  with a pastel rainbow fin, and a light line. All eight Chapter 2 costume
  sheets give her a fully rainbow-banded tail, waist-length hair with a
  flag-sized streak, and heavier dark contours. The Teacher sheet shows the
  look can be matched. This matters more in v2, because Roshan does each job
  inside the castle rooms, next to the approved cutout.
- **Fix, two options:**
  - (a) Identity-matched derivative sheets for each career, locked to
    `roshan_base.png` and the Teacher sheet. This is an owner call, because
    `DL-MED-02` lists the sheets as accepted art.
  - (b) Recommended for the in-world levels: keep the approved Roshan and add
    a small costume overlay per job: chef hat and apron, farmer straw hat,
    painter beret and smock, ballet tiara and tutu, pop star headset,
    astronaut helmet, detective cap and magnifier, arborist sun hat and satchel.
    Eight cutouts at 512 px or less, navy or plum contour, pinned to her head
    and waist anchors. She stays one Roshan in every room.

**GFX-SYS-05 — Code-drawn shapes stand in for story objects.** P0 and P1.
Evidence V, H, R, C.

| Object | Where | What the child sees | Disposition |
|---|---|---|---|
| Candy Maker activity panels | `opera_career_world_2d.gd:2048-2191` | Cream and lilac boxes, a purple rectangle "pitcher", a yellow line "stream", a circle "crank" | Retire (the Arborist replaces the Candy Maker in Day Two) |
| Detective storybook board | `opera_career_world_2d.gd:2193-2207` | A lilac rounded box with dots, like a domino | Retire; the J8 level uses the Library's painted magic book |
| Chef BAKE oven | Gauge widget | Brown boxes and a dial beside the world's own painted hearth oven | Fix now for freeplay and practice: use the painted oven as the BAKE object |
| Astronaut pipe board | Pipe widget | A grey grid with tan boxes and black dots over the painted rocket | Fix now: a painted pipe-tile kit (new art) |
| Farmer basket | `opera_world_backdrop_2d.gd:151-152` | A brown disc with a gold arc, like a pie | Retire with J2; the grove level uses a painted basket that fills from one to five |
| Pop Star echo | Rhythm widget | Three flat vector stars | Fix now: painted star-note pads (new art) |
| Shared widgets | `widget_pour_chef_fill.png`, `widget_crank_*_progress.png`, `widget_trace_*_lit.png`, `widget_gauge_shared_needle.png`, `widget_charge_popstar_*.png` | A tan blob, thin rings, a thin zigzag, flat bars | Fix now, replacing one at a time |
| Activity darkening | `_draw_activity_focus` (`opera_career_world_2d.gd:2007`) | A dark ellipse over the painting behind every activity | Fix now: remove, or use a soft light halo |

**GFX-SYS-06 — Old job art leaks into the birthday story.** P1. Evidence V,
C. Disposition: the in-world levels must never reuse it (WP-07 to WP-14). The
Opera practice may keep freeplay art, because it is the show, but never the
old cherry cake on Day Two.

| Story step | What the child hears | What the child sees |
|---|---|---|
| Farmer DELIVER (`chapter_two_career_scene_adapter.gd:53`) | "Swipe the full basket all the way to the kitchen!" | A lying pig (`widget_push_farmer_mover.png`) |
| Astronaut READY PARK (`:66`) | "Park the repaired rocket…" | A race kart (`widget_push_racer_mover.png`) |
| Chef STACK | "Stack the rainbow tiers" | Cherries, a cream swirl and a brown swirl that reads as poop (`widget_target_chef_piece_2.png`) on a plain sponge |
| Chef BAKE success and invitation | The rainbow cake | The old three-layer cherry cake (`goal_chef.png`, `widget_gauge_chef_success.png`) |
| Painter PAINT | The birthday banner | A framed sunrise painting (`goal_painter.png`) |
| Painter STAMP and HANG | Birthday stars; the Main Hall spot | Red paint splats; three tiny easel icons; no Main Hall |
| Detective cheer | The candle is found | Roshan cheering with a blue gem (cell 3,2 of the Detective sheet) |
| Farmer work loop | Picking strawberries | Pouch, digging and a carrot |

**GFX-SYS-07 — Story props float and appear twice.** P1. Evidence R, H.
Retire with the in-world levels, but carry the rule "one grounded object per
story object" into every new level.

- The persistent cake node at (790, 200) floats over the Chef world's
  étagère with only a faint 332×22 ellipse, and sits beside the world's own
  painted cherry cake: two cakes, three during FROST with the code rectangle.
- Two mixing bowls during MIX and STIR; the action happens at the painted
  bowl at x≈410 while the batter appears at x≈827-1113.
- The Astronaut world paints one rocket; the curtain-call prop
  (`goal_astronaut.png`) is a different rocket.
- The Candy Maker cake node draws over its own activity panel, hiding the
  pitcher and three of the five strawberries.

**GFX-SYS-08 — Always-on spotlight wedges.** P2. Evidence C, H. Fix now.
When a career world is drawn from its four tiles, `_draw()` always adds
`_draw_spotlights()` (`opera_world_backdrop_2d.gd:236-239`): two tinted wedges
at 8-13% opacity, pulsing. The single-painting branch a few lines below skips
them outside stage mode, with the comment that over a painted district they
"fight the art's own light sources". Apply the same rule to the tile branch.

**GFX-SYS-09 — Wide phones get a double letterbox.** P1. Evidence C. Fix
now. The stage is frozen at 1280×720 and the leftover width is flat navy
(`#16214d`). On a 20:9 phone the sharp painting covers about 53% of the
screen; the Detective about 22%. After SYS-01 and SYS-02, fill the side bars
with painted curtain panels (a derivative of the `stage/finale_stage_*`
curtain edges) or an extended painting edge, never flat navy.

**GFX-SYS-10 — Scene names promise art that does not exist.** P1. Evidence
C. `chapter2_chef_cake`, `strawberry_cake_workshop`,
`main_hall_birthday_banner`, `chapter2_astronaut_rocket`,
`chapter2_popstar_rumi` and `magic_storybook` all fall back to the generic
career worlds. Meanwhile `chapter2_scene_specific_2d` is set to true whenever
a variant name is given, whether or not its art exists
(`opera_world_backdrop_2d.gd:53`). The Painter's "Main Hall
banner" never shows the Main Hall; the Detective's "magic storybook" never
shows a book. Fix now: stop tagging these as scene-specific, so probes do
not count them as done. v2 answers the rest by moving these levels into the
real rooms.

**GFX-SYS-11 — Nothing touches the ground.** P1. Evidence V, C. None of the
lawn guests, stuffies, table, rocket, microphone, music box, King or Prince
has a contact shadow, and props float in the job scenes. Fix: one shared soft
lavender contact-shadow sprite, the castle's existing style, under every
standing figure and prop, sized to 70-90% of its base width. Seat objects on
painted surfaces: a table, a counter, a blanket, a pad.

<a id="gfx-sys-12"></a>
**GFX-SYS-12 — Words stand in for pictures.** P0. Evidence V, C. With WP-03,
WP-16, WP-17.

- The Day Two card says "A NEW DAY", "DAY TWO!" and "NEW ADVENTURES".
- The lawn shows "Happy Birthday, Roshan!" as a 42 px label in the sky for
  the whole finale, including the theft (`chapter_two_lawn_finale_2d.gd:226-232`).
- Lawn captions are screenplay lines at the top, 27 px, often two speakers
  in one line: "Prince: You made that?  Roshan: All of us did."
  (`chapter_two_lawn_finale_2d.gd:233-239`). Every line, the King's
  included, plays in Roshan's synthetic voice (`_say("roshan", …)`, line 294).
- 16 of 29 job steps have no voice line, so their caption is the only
  instruction (build audit B5).
- **Fix:** carry every meaning with a picture and a voice.
  - On the card: a picture of the birthday (see GFX-CARD-01).
  - On the lawn: a painted garland instead of the title (GFX-LAWN-02).
  - Captions: one short line for the adult reader, no speaker labels, never
    over a face, with a small face icon of the speaker. Each speaker is
    voiced and visibly acts while talking.

<a id="gfx-sys-13"></a>
**GFX-SYS-13 — Steps with no pointer.** P0. Evidence C. Cross-discipline;
fix now. 19 of the 29 Chapter 2 job steps have no `PHASE_STATIONS` entry, so
no station is armed, no hotspot is shown, and real touches cannot open the
step (build audit [B1](05_BUILD_AUDIT.md)). That is the missing half of the
hard rule that every objective has a voice and a visual pointer. Fix with the
B1 repair, then confirm with a real-touch run.

## 2. The Opera House venue

Venue art: `assets/flats/castle/opera_house_venue_2d/` and
`scripts/opera_house_venue_2d.gd`. In v2 each practice launches from its job's
room card by default ([decision 2](README.md#owner-decisions)). The venue is
still the stage for freeplay, and the front door if the owner chooses Opera
Hall launches.

| ID | Sev | Evidence | Flaw | Fix |
|---|---|---|---|---|
| GFX-VEN-01 | P0 | C, R | All doors look alike, with generic 40 px medallions and no career picture. In Chapter 2 party mode the pointer is hidden (`guide_pointer.visible = chapter2_tutorial_mode`, line 365), and the "glow" tints a fully transparent button (lines 368-379), so there is no visible cue. Only the next job's door responds; other doors ignore taps silently | A painted plaque over each active door showing the job (the costume idle cell, or a Day Two crest, in a door-top frame derivative). Keep the pointer in every Chapter 2 mode. Other doors answer gently: the curtain wiggles and a voice says the show is later |
| GFX-VEN-02 | P1 | C | A finished door looks the same as an open one | A painted "curtain closed, gold star" state |
| GFX-VEN-03 | P1 | V | A third rendering style: semi-realistic, very detailed, mid-value salmon, no contour lines. It sits between the castle's flat pastel Opera Hall and the painted career worlds | No restyle here. The owner-commissioned native venue in `design/VISUAL_REPAIR_PLAN_2026-09-26.md` is the fix |
| GFX-VEN-04 | P2 | C | The tiles are a 1024×576 master enlarged 3.55× and then shrunk 2.84× at runtime: soft, with no added detail, and about 22-30 MB of video memory for eight odd-sized tiles | Draw the 1024×576 source directly until the commissioned venue lands |
| GFX-VEN-05 | P2 | C, R | Roshan slides between doors as a still card about 100 px tall; the floor "footlight" is a flat 696×5 bar at y=666 that reads as an underline; the act-13 touch area sits 20-40 px off its door | A swim cycle from the `roshan_25d` swim sheets; a soft glow sprite for the footlight; realign the area |

## 3. The job scenes as built today

Today every Day Two job runs inside its Opera career world with Chapter 2
overlays. v2 keeps each world for the practice (Level 1) and builds Level 2
in the real room ([03](03_LEVEL_DESIGN.md)). Scene scores are the research
pass's ratings out of five.

### Farmer (scene 1.5/5)

| ID | Sev | Evidence | Flaw | Fix | Disposition |
|---|---|---|---|---|---|
| GFX-FARM-01 | P0 | R, C | The Sky Lagoon backdrop is cropped row by row (`_draw_sky_lagoon_farmer`, `Rect2(0, 224, 1024, 576)` per row), which drops 448 source rows (the bushes and lupines: the actual meadow) and leaves a straight horizon seam at screen y=360 | Crop one continuous window across both rows (about y 448-1600 of the 2048-tall column pair), drawn as one rectangle | Reuse the fixed crop for the J2 grove level |
| GFX-FARM-02 | P1 | R | The five strawberries hover in the sky above the seam, evenly spaced like a menu row | Seat each berry on a painted strawberry plant (new small art, three variants) in the meadow band | With WP-08 |
| GFX-FARM-03 | P0 | R | Roshan starts in the sky on the seam, following the Farmer world's path | A path on the lilac walk | With WP-08 |
| GFX-FARM-04 | P1 | C | Code basket (brown disc and gold arc) | A painted basket derivative that fills from one to five berries | With WP-08 |
| GFX-FARM-05 | P1 | R | Picked berries stay where they were as grey-purple ghosts (tinted, 38% opacity); nothing goes into a basket | Each picked berry flies into the basket | With WP-08 |
| GFX-FARM-06 | P1 | C | DELIVER uses the pig (SYS-06) | The full basket is the thing she swipes | With WP-08 |
| GFX-FARM-07 | P2 | C | The work loop shows digging and a carrot | Hold a neutral work cell, or a strawberry-holding derivative | Fix now |

### Chef (scene 2/5)

| ID | Sev | Evidence | Flaw | Fix | Disposition |
|---|---|---|---|---|---|
| GFX-CHEF-01 | P0 | H | Blurred frame (SYS-01) | SYS-01 | Fix now |
| GFX-CHEF-02 | P1 | R, H | Two cakes on screen (the story cake and the painted cherry cake on the dais), three during FROST; two mixing bowls during MIX and STIR | One cake, placed on the dais where it hides the painted one | Retire; the J3 level is in the Royal Kitchen |
| GFX-CHEF-03 | P0 | H | Code-drawn oven box beside the painted hearth oven | Use the painted oven as the BAKE object | Fix now (freeplay and practice) |
| GFX-CHEF-04 | P1 | V, C | The old cherry cake is the BAKE success and the room invitation | Suppress it on Day Two | Fix now |
| GFX-CHEF-05 | P1 | V | STACK pieces are cherries, cream and a brown swirl on a plain sponge | Six rainbow tier pieces cut from `chapter2_chef_baked_tiers_unstacked.png` as separate derivatives | With WP-09 |
| GFX-CHEF-06 | P1 | H | A beige batter oval and a flat cream rectangle cake sit next to the rainbow bowl and stack | Remove them when the story art is on screen | Retire |
| GFX-CHEF-07 | P2 | R | The cake jumps in size between steps: 207×296, then 166×237 (20% smaller), then 194×276 | One fixed on-screen height for all cake stages | With WP-09 |
| GFX-CHEF-08 | P2 | V | Roshan's work row holds a pink bowl of beige batter, not the lavender shell bowl of rainbow batter | Hold a neutral cell during story steps | Fix now |
| GFX-CHEF-09 | P1 | C | Before MIX, `ChapterTwoGiantCake2D._draw()` paints a code tray and an orange capsule "bowl" (lines 463-467) behind five tiny berries, then swaps to the painted bowl: a style jump and a bowl that changes shape. The same code tray shows on the Main Hall party table after the Farmer | Draw the painted bowl from the start, or nothing | With WP-09 |

### Candy Maker (scene 1.5/5; leaving Day Two)

The Arborist replaces the Candy Maker in Day Two, and the strawberry topping
moves to the Chef ([Arborist handoff](../ARBORIST_TREE_DOCTOR_HANDOFF_2026-09-30.md)).
Its Chapter 2 flaws retire with it: all four activities are code panels
(K2); the cake hides the panel's pitcher and three berries (K3); berries fly
to the panel edge while the cake sits elsewhere (K4); ten strawberries are
visible in a "five" lesson (K5); berry textures are stretched 16% (K6).
**Keep** `chapter2_candied_strawberries_tray.png` for the Chef's topping
step: its weak "candied" look, a flaw for the Candy Maker, suits fresh berries
(see [GFX-PROP-BERRY-02](#gfx-prop-berry-02)).

### Painter (scene 2/5)

| ID | Sev | Evidence | Flaw | Fix | Disposition |
|---|---|---|---|---|---|
| GFX-PAINT-01 | P0 | H | Blurred frame (SYS-01) | SYS-01 | Fix now |
| GFX-PAINT-02 | P1 | H, C | PAINT reveals the sunrise painting on a flat cream rectangle floating over the easel | The banner states in [GFX-PROP-BANNER-01](#gfx-prop-banner-01) | With WP-10 |
| GFX-PAINT-03 | P1 | C | STAMP stamps paint splats for "stars"; HANG shows easel icons; the Main Hall never appears | Star stamps; the J4 level hangs the banner in the real room | With WP-10 |
| GFX-PAINT-04 | P1 | R | The curtain-call banner (110×220) floats over a coral pot, its pale wash vanishes on the sand, and it shows nothing the child painted | Show the finished banner state, grounded | With WP-10 |
| GFX-PAINT-05 | P2 | C | The party table remembers the Painter's job as the sunrise painting (`goal_painter.png` at (54, 502), `chapter_two_party_table_2d.gd`) | Show the banner | With WP-16 |

### Ballerina (scene 2.5/5)

| ID | Sev | Evidence | Flaw | Fix | Disposition |
|---|---|---|---|---|---|
| GFX-BALLET-01 | P1 | R, C | The Stuffie Room backdrop is the empty playroom shell (bricks, balcony, two shelves, bare floor); the nook and toys are separate castle cards not drawn here | The J5 level runs in the Playroom's own art with its item cards | Retire |
| GFX-BALLET-02 | P1 | R | Stations point at a blank brick wall (`trifold_mirror` at (475, 205)) and a floor edge (`wave_tuffets`) | Point stations at the drawn toys | Retire |
| GFX-BALLET-03 | P1 | V, M | Kitty and Bunny are damaged protected book crops ([GFX-CHAR-DOLLS-01](#gfx-char-dolls-01)) | See that finding | Owner |
| GFX-BALLET-04 | P2 | R | The dolls' thin-line watercolour style against the painted room, with no shadows, about 700 px from the Roshan they are meant to mirror | Stage them within about 300 px of Roshan, with contact shadows | With WP-11 |

### Pop Star (scene 3/5, the best of the eight)

| ID | Sev | Evidence | Flaw | Fix | Disposition |
|---|---|---|---|---|---|
| GFX-POP-01 | P0 | H | Blurred frame (SYS-01) | SYS-01 | Fix now |
| GFX-POP-02 | P2 | R | Rumi is about 156 px tall against Roshan's 200 px, so the older friend reads younger; no contact shadow on the dome steps | Scale Rumi to at least Roshan's height; add a shadow. No new Rumi frames | With WP-12 |
| GFX-POP-03 | P1 | H | The rhythm echo draws three flat stars and a dark ellipse over Rumi | Painted star-note pads placed clear of Rumi | Fix now |
| GFX-POP-04 | P2 | V | STAGE RUMI shows abstract arrow tiles, not Rumi being staged | In J6, Rumi herself is the choice target | With WP-12 |

### Astronaut (scene 2/5)

| ID | Sev | Evidence | Flaw | Fix | Disposition |
|---|---|---|---|---|---|
| GFX-ASTRO-01 | P0 | H | Blurred frame (SYS-01) | SYS-01 | Fix now |
| GFX-ASTRO-02 | P0 | H | BUILD ROCKET covers the right half, painted rocket included, with the code pipe grid; the "rocket parts" never appear | A painted pipe-tile kit (new art) laid beside the rocket, not over it | Fix now |
| GFX-ASTRO-03 | P1 | V | PATCH pastes flat vector badges on the painted rocket | Painted patch pieces in the rocket's style | Fix now |
| GFX-ASTRO-04 | P1 | C | READY PARK uses the race kart | The party rocket (`goal_astronaut.png`) as the thing she parks | With WP-13 |
| GFX-ASTRO-05 | P1 | R | The curtain-call rocket (coral fins, porthole) is not the painted rocket (red nose, star window, door) | One rocket design everywhere: `goal_astronaut.png`, which is already the party rocket | With WP-13 |

### Detective (scene 1/5)

| ID | Sev | Evidence | Flaw | Fix | Disposition |
|---|---|---|---|---|---|
| GFX-DET-01 | P0 | V, H | Postage-stamp painting (SYS-02) | SYS-02 | Fix now |
| GFX-DET-02 | P0 | R, C | Every lens object and station was placed for the old full-frame art and now sits on the padding | Re-derive them after SYS-02 | Fix now |
| <a id="gfx-det-03"></a>GFX-DET-03 | P0 | C, M | The candle touch area misses the candle. The invisible button is at (760, 145), 156×190 (`opera_career_world_2d.gd:902-905`). The candle is drawn at about (874-927, 313-419), from its sprite at local (75, 119) scaled 0.20 inside a node at (838, 238) scaled 0.84 (`chapter_two_rainbow_candle_2d.gd:106-110`). They overlap by about 42×22 px, so a tap on the candle's centre, about (900, 366), misses | Size the button from the candle's drawn bounds plus at least 30 px of padding (at least 120×160), or make the candle node itself the touch target | Fix now |
| GFX-DET-04 | P0 | R, C | The "magic storybook" board is a code domino card; the candle overlaps its left edge during the reveal | Retire; J8 uses the Library's painted magic book | Retire |
| GFX-DET-05 | P1 | H | A night detective district with evidence boxes; no storybook anywhere, although the job starts at the Library's magic book | J8 runs in the Royal Library | Retire |
| GFX-DET-06 | P2 | H | Dark navy night palette; the brightest objects are the evidence boxes, not the goal | Keep for freeplay; J8 is in the bright Library | Retire |
| GFX-DET-07 | P2 | V | The cheer cell holds a blue gem | Hold a cell without the gem | Fix now |
| GFX-DET-08 | P1 | V | The Library's magic book item (`room_library_item_magic_book.png`, 137×169) has a cream background smear behind the book and stray fragments along its top edge; the opening-book sheet has a mottled grey cover and blank pages | Clean alpha derivative; J8 paints the candle clue onto the pages as a derivative | With WP-14 |

### Arborist (not yet in the repository)

**GFX-ARB-01 — The Arborist art is not committed.** P0 for J1. The owner
says the art exists; it was not found in the repository or on Drive. It must
be committed from the owner's local worktree (`codex/arborist-tree-doctor`)
before J1 can be audited or built ([Arborist handoff](../ARBORIST_TREE_DOCTOR_HANDOFF_2026-09-30.md),
Step 0). When it lands, check it against this audit's rules: one Roshan
identity, painted objects rather than code shapes, redundant colour, shape and
icon cues for every sickness and medicine, and a clean alpha on every cutout.

## 4. The Day Two card

`scripts/day_two_transition_2d.gd`: night turning to dawn over the castle, "✦
A NEW DAY ✦ / DAY TWO!", a "NEW ADVENTURES" tray with Opera, Craft and
Kitchen medallions, and the voice "The second day is here! Visit castle jobs
and the Opera House!"

| ID | Sev | Evidence | Flaw | Fix |
|---|---|---|---|---|
| GFX-CARD-01 | P0 | C, R | Nothing says birthday: no cake, balloons or candle, and no Roshan, Baby Eagle or rainbow friend. The tray advertises jobs, and the voice never mentions the birthday | Keep the dawn animation. Add the three friends waking (cutouts), a picture of the birthday (the cake silhouette or balloons), and a pointer toward the first place. New voice: "It's Roshan's birthday!" ([03 D2-OPEN-1](03_LEVEL_DESIGN.md)) |
| GFX-CARD-02 | P1 | C | Its words ("A NEW DAY", "DAY TWO!", "NEW ADVENTURES") are the message | Keep words only as decoration for the adult; the picture must tell the story alone |
| GFX-CARD-03 | P2 | V | The Opera medallion (`assets/ui/castle_room_buttons_v2/room_opera_hall.png`) pairs a smiling mask with a frowning black one: a sad face on the birthday card, and again over the Main Hall's Opera door | A Day Two variant medallion (a smiling mask with a star, or a curtain and microphone) as a derivative |
| GFX-CARD-04 | P2 | R, C | The castle is placed at (160, 128), 748×590 (lines 229-230), so its wooden ramp runs past the card's rounded frame at the bottom. The castle floats on nothing, and the dimmed, tinted cloud bank behind it reads as grey smog rather than a cloud island | Scale the castle to about 0.92 and raise it so the ramp ends inside the frame; seat it on a bright cloud island in front of the bank |
| GFX-CARD-05 | P2 | C | The sky gradient is built by assigning three colours to a new two-point `Gradient` (lines 97-100) without setting three offsets, so the night colour may never show; the code-drawn moon, a cream disc with a sky-coloured "cutout" disc, can then read as two circles. The sun also stays faintly visible beside the moon at night | Set three offsets explicitly before the colours; confirm in a capture; hide the sun until dawn. Better, use a painted moon cutout. The colours are also reassigned every frame (line 387), which rebuilds a 1280×720 gradient texture on the CPU for 4.18 s: use a 1×256 texture or a shader to avoid a hitch on the phone |
| GFX-CARD-06 | P2 | C | Stars are text glyphs ("✦" and "·") in a label: the dots are two or three pixels on a phone, and "✦" depends on the phone's font and may show as an empty box | Painted star sprites (the existing `castle_banner_motif_star.png` works) |
| GFX-CARD-07 | P2 | V | The medallions are enlarged from small door signs (about 106-126 px) and look soft; the Kitchen medallion carries a grey rectangle from its source plate at the top | Re-cut them from larger sources, or show them at their native size |

## 5. The Main Hall party table and the castle rooms

### 5.1 The party table

`scripts/chapter_two_party_table_2d.gd`. In v2, Daddy's Party Plan board
replaces the table as the day's progress picture ([03 D2-OPEN-2](03_LEVEL_DESIGN.md)).
The table remains the place the finished pieces gather before the party.

<a id="gfx-hall-07"></a>
**GFX-HALL-07 — The party table is glued to the screen.** P0. Evidence C.
Fix now; WP-03 builds on it.

- **What is wrong:** the Main Hall is twice the screen's width, and its world
  scrolls with Roshan (`castle_rooms_25d.gd:5081-5088` moves
  `castle_room_world_root`). The party table belongs to `ChapterTwoRoomPlot`,
  which is added to the stage itself at position zero (`main.gd:6299-6301`,
  `chapter_two_room_plot.gd:26`), so it never scrolls. When Roshan swims
  right, the table, cake, banner and props stay put on screen and slide
  across the other doors. The table's touch area stays at fixed screen
  coordinates too. Because the plot layer sits above the whole world, its
  props also draw over Roshan: behind the table's panel she disappears, and
  in the Library the found candle covers her body when she reaches the book.
- **Fix:** parent the table and the other plot props to the scrolling world
  at their room positions, sorted by depth with Roshan, and move the touch
  area with them.

<a id="gfx-hall-08"></a>
**GFX-HALL-08 — The candle is drawn behind the cake.** P0. Evidence C, M.
Fix now.

- **What is wrong:** the cake's picture is a child sprite with
  `z_index = 4` inside the cake node (`chapter_two_giant_cake_2d.gd:655-659`),
  so it draws above the candle node's `z_index = 3`
  (`chapter_two_party_table_2d.gd`, `_build_story_centerpieces`). The unlit
  candle, drawn at about x 619-660, y 118-200, sits almost entirely inside
  the cake's top tier and crest (the cake is drawn at about x 542-738,
  y 116-394). Only its tip shows; lit, only the flame shows. The object the
  whole chapter is about is barely visible.
- **Fix:** draw the candle above the cake, standing in a holder on the top
  tier ([GFX-PROP-CAKE-04](#gfx-prop-cake-04)).

| ID | Sev | Evidence | Flaw | Fix |
|---|---|---|---|---|
| GFX-HALL-01 | P1 | C, R | The table stands inside a 710×238 rounded UI panel (`PartyTableGlow`, lines 364-368) that turns bright yellow when the party is ready (lines 103-108). It reads as a menu card on the floor | Remove the panel. Show readiness with a soft painted glow under the table and sparkles on the pieces |
| GFX-HALL-02 | P1 | C, R | The banner is the tall pennant (`castle_banner_rainbow.png`, 256×512) squeezed into a 396×118 slot (lines 352-353). It shows as a pennant about 59 px wide, parked behind the top of the cake, with an empty medallion | A horizontal garland derivative of the painted banner, hung above the table |
| GFX-HALL-03 | P1 | C | Two rockets: the candle-lighting rocket (112×112 at (815, 235)) and the Astronaut's 76 px summary icon at (1150, 502) | Drop the summary icon; the lighting rocket is the Astronaut's piece |
| GFX-HALL-04 | P1 | C | The other summary pieces are 76 px stickers at the screen edges (music box, sunrise painting, microphone). Unearned ones show as purple ghosts at 16% opacity, like disabled buttons | Put each piece on or beside the table at readable size; show unearned pieces as empty spots on the Party Plan board, not ghosts |
| GFX-HALL-05 | P1 | R, C | In the reconstruction the cake floats 25-45 px above the table top with its shadow on the panel's edge. The cake is also about 1.45 times Roshan's height here, against about 1.1 on the lawn | Take a capture; seat the cake stand on the tabletop; use one cake-to-Roshan ratio everywhere |
| GFX-HALL-09 | P1 | C | The approved table (`dining_table.png`, 292×223) is fitted into a 620×206 box with its aspect kept, so it draws only about 270×206 in the middle of the 710 px panel: a small table under a cake twice its height | Size the table from its own aspect so it can hold the cake and pieces; drop the panel (GFX-HALL-01) |
| GFX-HALL-10 | P1 | C, R | The lighting rocket (112 px, tilted) floats in mid-air in front of the Opera arch's curtains and sign | Stand it on the floor or a small pad beside the table |
| GFX-HALL-11 | P1 | C | The castle caption panel (820×112 at (230, 112), `castle_rooms_25d.gd:1091-1092`, nearly opaque) covers the cake's top tiers, the candle and the Opera door sign while its line talks about the party | Captions go to a band clear of the story objects (bottom-left for the adult), never over the thing being described |
| GFX-HALL-06 | P2 | C | Dead code: code-drawn flame shapes with dot eyes for an "Ember scout", "Ember King" and "son" (lines 212-285 and 448-535). Nothing calls them | Delete them, so the only King and Prince are the approved ones |

### 5.2 The castle rooms on Day Two

From the room art, the follower code and reconstructions of each room with
Roshan and her two followers. In v2 each job's practice still launches from
its room card, and several levels happen in these rooms.

| ID | Sev | Evidence | Flaw | Fix |
|---|---|---|---|---|
| GFX-ROOM-01 | P1 | C, R | Roshan and her followers merge into one blob. The rainbow friend (a 165 px box at the foot offset (-104, -78)) is drawn in front of Roshan and covers her tail; Baby Eagle (a 195 px box at (+108, -100)) covers her hand and fin. Neither has a shadow, and the rainbow friend's saturated gradient reads as a sticker against the pastel rooms. The followers do not scale with depth: Roshan scales from 0.72 to 1.05, the followers stay fixed, so at the back of a room Baby Eagle is as tall as Roshan | Spread the offsets so the three silhouettes do not overlap at phone size (about 40 px clear on each side), scale the followers with Roshan's depth, draw them behind her front plane, and add contact shadows. Do not recolour the approved rainbow friend |
| GFX-ROOM-02 | P1 | V, R | Career cards are near-white rounded squares that cover painted details: in the Kitchen, two cards hide the range hood and copper pans; in the Dining Room the Farmer card overlaps the chandelier. At about 112 px the Chef and Candy Maker costumes look alike, and each crest's symbol is about 25 px wide | One card per room in v2 (the Arborist takes the Candy Maker's slot). Place cards in quiet wall space, use painted frames instead of white panels, and show the job's key object large (GFX-PROP-CREST-01) |
| GFX-ROOM-03 | P1 | V | The Dining Room backdrop (`assets/flats/castle/rooms/room_dining_room_background.png`, 1024×576) is a flat vector placeholder: plain lavender bricks, a featureless teal arch, a pastel checkerboard floor with harsh navy perspective lines, and a flat purple ceiling band. The painterly hutch, table and stools float on it without shadows. Its teal arch is the Farmer's "berry doorway", with no berry in sight | A painted Dining Room plate in the castle style, commissioned as a named replacement; until then, dress the arch with strawberry vines and baskets as cutouts so the doorway says "berries" |
| GFX-ROOM-04 | P2 | R | The Dream House Wing's Family Gallery and the Movie Lounge also use flat vector backdrops, with blank cream circles above the gallery arches. The gallery is on the Farmer's route (Main Hall, Dream House Wing, Dining Room) | Named replacements after the Dining Room; fill the blank circles with each doorway's picture |
| GFX-ROOM-06 | P0 | C | On Day Two no door is lit for the next job. `door_state()` falls back to the free-play resolver once Day One ends, and `active_door_highlight_id()` only ever lights the Royal Hall event (`castle_rooms_25d.gd:1686-1702`). With the objective card also hidden in the castle (build audit B6), the only guide to the next job is a caption and, sometimes, a voice | Light the next job's door with the Day One golden-door language, and point the hand at it; after v2's Party Plan, the glowing frame on the board and the lit door name the same job |
| GFX-ROOM-05 | P2 | C, R | In the Library the found candle is small (about 40×75 px at (588, 200), scale 0.7) and overlaps the magic book; when Roshan reaches the book, the rainbow friend covers the pedestal | Show the candle larger when found, standing clear above the book, and keep followers beside Roshan, not in front of the goal |

## 6. The lawn finale

`scripts/chapter_two_lawn_finale_2d.gd`, from the eleven engine captures of
2026-09-06 (`assets_src/cinematics/chapter2_lawn_scale_v2_2026-09-06/runtime/`)
and zoomed crops of them. [04](04_FINALE_PARTY_CHAPTER.md) is the story these
fixes serve.

<a id="gfx-lawn-01"></a>
**GFX-LAWN-01 — Code party hats cover faces and miss heads.** P0. Evidence
V, C. With WP-16.

- **What is wrong:**
  - Each hat is a `Polygon2D` triangle, 44×46 px at full size, in one of four
    flat pastels, with a 3 px navy line and a cream stripe (`_add_hat`, lines
    202-223).
  - Hats are placed at fixed points inside each guest's 118×140 box (lines
    161-169). The portrait is fitted and centred inside that box, so the
    points do not match where heads are.
  - In the captures:
    - Faron's lavender hat covers her whole face: a protected family portrait
      with the face hidden.
    - The baby's small hat floats in the air beside her.
    - Huluu's yellow hat covers her helmet and eyes.
    - Harper's and Fiona's hats cover both sisters' faces.
    - Daddy's hat floats high above the crown he already wears.
    - Evie's and Flower Friend's hats float above their heads, not touching.
  - The flat geometry clashes with the painted portraits, and a row of
    triangles pointing down at every guest reads like tap markers.
- **Fix:**
  1. Paint a small party-hat set (new art): a cone with a pom-pom, in four
     colours and two sizes, with a navy or plum contour and soft painted light
     from the upper left. 256 px or less, with alpha.
  2. Measure each portrait's head from its alpha: top centre, width and tilt.
     Store it as a per-guest table in the lawn script, in portrait
     coordinates, not box coordinates.
  3. Scale each hat to 55-70% of the head's width, tilt it with the head, and
     sit the brim on the hairline, never below the eyebrows.
  4. Give Faron's baby a hat only if the baby's head is visible. Give Rumi
     and Roshan hats as well ([GFX-LAWN-16](#gfx-lawn-16)).
  5. Add a probe: no hat may overlap any face rectangle from the table.
  6. On each stomp (F4), hats wobble with a short tilt of about 6°.
- The portraits stay untouched; hats remain overlays
  (`protected_source_unchanged` stays true).

**GFX-LAWN-02 — A text title in the sky.** P0. Evidence V, C. With WP-16.
"Happy Birthday, Roshan!" is a 42 px label at (175, 115) (lines 226-232) that
floats over the mountains and stays up through the theft and the sad beat.

- **Fix:** remove the label.
  - Hang a painted birthday garland between the party tree and a pole: a
    derivative of the finished banner and its star stamps, showing the cake
    and candle, and Roshan's initial or her age if the owner wishes.
  - Voices say "Happy birthday, Roshan!" in F1 and F2.
  - In F6 and F7 the garland stays, but the warm light drains, as the
    story does.

**GFX-LAWN-03 — Screenplay captions, all in Roshan's voice.** P0. Evidence
V, C. With WP-16 and WP-17. See GFX-SYS-12. Each line gets its own speaker's
voice and a short caption with no speaker label. The speaker bobs or squashes
while talking.

**GFX-LAWN-04 — The party has no view of home.** P1. Evidence V, C. With
WP-16.

- **What is wrong:** the lawn uses columns 2-3 of the approved Sky Lagoon
  panorama (`flat_sky_lagoon_main_panorama_v5`, lines 128-134). That crop
  shows snowy peaks, a cloud sea and a hillside cabin. It shows neither the
  castle, where everything was made, nor water. The cabin is an unexplained
  landmark, someone else's house at Roshan's party. F3's moonflower glow and
  F8's walk home both need the castle in view.
- **Fix:** keep the approved painting; do not restyle it.
  - Place the existing castle cutout (`assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png`)
    small on the horizon behind the party tree.
  - Let the healed party tree cover the cabin.
  - If the panorama has a crop with the lagoon, prefer it.

<a id="gfx-lawn-05"></a>
**GFX-LAWN-05 — Guests squeezed into identical boxes in one corner.** P1.
Evidence V, C. With WP-16.

- **What is wrong:**
  - Every protected portrait is fitted into the same 118×140 box (lines
    150-158). The two sisters, a mother with a baby, a boy in an armchair and
    Daddy all get roughly the same size, whatever their real size.
  - Daddy, the planner and the one who hugs her, is small and far back at
    (520, 280), behind the cake.
  - Eight guests, Rumi, the stuffies, the cake, the rocket and three props
    crowd x 40-690. The right half holds only Roshan until the royals
    arrive.
  - No guest has a shadow, and several stand on their tail tips on the
    grass. Kareem's armchair, part of his portrait, stands on the lawn.
  - The stuffies sit on the stone path at the bottom edge (y 620-688).
- **Fix:**
  1. Three depth bands (back y≈330, middle y≈450, front y≈560) in a shallow
     arc around the table, facing the path the royals will use.
  2. Size each portrait from a height table (adult 1.0, teen 0.9, child 0.75,
     baby carried), keeping aspect, instead of one box for all.
  3. Daddy front-left, near Roshan's start.
  4. A picnic blanket with cushions, so the merfolk rest on something and
     Kareem's armchair stands at the blanket's edge. New small art, or
     cushions reused from the castle playroom.
  5. Contact shadows for everyone (GFX-SYS-11).
  6. Keep the open lawn (about x 700-1100) clear for the King's rounds.

**GFX-LAWN-06 — The cake, rocket and props crowd and float.** P1. Evidence
V, C. With WP-16. The rocket (140×145 at (480, 422)) stands in front of the
table, overlapping it and hiding guests. The microphone (64×75 at (630, 440))
and the music box (70×68 at (205, 460)) float with nothing under them. Fix:
the rocket on its own small painted launch pad beside the table, tilted toward
the candle; the microphone on Rumi's little shell stage; the music box on the
stuffie blanket.

<a id="gfx-lawn-07"></a>
**GFX-LAWN-07 — Lighting the candle is too small to see.** P0. Evidence V,
C. With WP-16.

- **What is wrong:**
  - In the ignition capture Roshan's hand is on the rocket, about 200 px
    from the candle, so nothing connects her to the flame.
  - The spark is a 7 px dot that travels for 0.6 s (`_draw_foreground`,
    lines 604-611).
  - The lit flame is about 20 px tall.
  - Nothing glows, and no guest reacts: every pose matches the unlit capture.
  - This is the payoff of the whole day.
- **Fix:**
  1. The rocket points at the candle (GFX-LAWN-06).
  2. The spark becomes a painted sparkle trail, at least 24 px, travelling
     1.0-1.2 s in an arc. Reuse existing sparkle art.
  3. At ignition the camera moves in about 1.15× on the cake for 1.5 s
     (`Camera2D`), so the flame reads at 60 px or more.
  4. A warm radial glow sprite behind the cake at low opacity: a 2D effect,
     not a relight of the painted art.
  5. Guests react with whole-card bobs and squashes, the only motion
     allowed on protected portraits, and hats wobble.
  6. Hold the lit candle for at least 2.4 s.

<a id="gfx-lawn-08"></a>
**GFX-LAWN-08 — The stomp warning barely shows.** P0. Evidence V, C. With
WP-16.

- **What is wrong:** the warning is a flat orange ellipse at 34% opacity with
  a 6 px outline. The safe spot is an unfilled mint circle with a 24 px radius
  and a 4 px line (lines 579-599). Both have little contrast on yellow-green
  grass: the orange fill over green reads as a brown mud puddle, drawn under
  the characters. They sit in empty lawn rather than near the friends, and
  the King does not lift a foot first.
- **Fix:**
  - Reuse the painted gold telegraph ring
    (`assets/opera/worlds/props/fx_telegraph_ring.png`, thick, with a navy
    outline) under a warm ember-crack decal with a dark plum rim.
  - The safe spot becomes a sparkling lily pad at least 96 px across, with the
    moving hand on it. This is new small art; no lily pad exists.
  - Each landing puffs `fx_dust_puff.png`.
  - The King's foot lift comes from [GFX-CHAR-KING-01](#gfx-char-king-01).

**GFX-LAWN-09 — The shelter is three thin lines.** P1. Evidence V, C. With
WP-16.

- **What is wrong:** each finished round adds a 7 px pastel arc centred at
  (343, 530) with a radius of 260-280 (lines 572-574). The arcs are outlines
  only; guests at the far left sit half outside them. They stay up after the
  theft and to the end.
- **Fix:** the three friend layers from F5.
  1. A dust bunny wall: five to seven existing dust bunny cutouts
     (`assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_family.png`,
     `dust_bunny_curl_ears.png`) standing shoulder to shoulder in front of the
     guests.
  2. Baby Eagle holding a horizontal banner canopy over them.
  3. A painted rainbow dome (new effect art: seven soft bands with a gentle
     inner glow, at 40-55% opacity) sized over all guests and the cake. That
     needs the tighter guest arc from GFX-LAWN-05.
  - The dome softly pops into sparkles at the start of F7.

**GFX-LAWN-10 — The royals never act.** P0. Evidence V, C. With WP-16.
Arrival, demand, battle, theft and departure all show the same two still
images. The candle jumps into the King's upturned palm with no reach, and the
two never walk in or out. See [GFX-CHAR-KING-01](#gfx-char-king-01) and
[GFX-CHAR-PRINCE-01](#gfx-char-prince-01).

**GFX-LAWN-11 — After the theft, nothing changes.** P1. Evidence V. With
WP-16. The "hope" capture matches the party capture: same poses, same hats,
the title still up, the rainbow arcs still there. Nobody moves toward Roshan,
who stands alone facing the camera.

- The candle's absence is not marked: nothing shows where it stood, so a
  child may not notice what was taken.
- **Fix:** F7 staging.
  - The empty candle holder ([GFX-PROP-CAKE-04](#gfx-prop-cake-04)) shows
    what is missing.
  - The warm tint drains and the music stops.
  - Guests turn and lean toward Roshan (whole-card flips and tilts).
  - Lamma bounces over with the hat.
  - Daddy moves beside Roshan and they do a squash "hug" with a heart
    sparkle. A real hug pose is an art gap: record it rather than borrowing
    frames from the Day One clip, which must not be edited (`DL-CIN-16`).

**GFX-LAWN-12 — A tiny banner hangs from nothing.** P1. Evidence V, C. With
WP-10 and WP-16. The banner is 90×145 at (50, 118), with five 20 px star stamps
(lines 135-147), top left in the sky. It reads as a rank ribbon. Fix: the
finished banner garland in the party tree, at least 420×140 on screen, stars
at least 36 px.

**GFX-LAWN-13 — Damaged doll edges on screen.** P1. Evidence V. Owner. The
book dolls sit at the frame's bottom edge, where their crop damage shows: the
hole in Kitty's nose, the straight cuts along her left and bottom edges, and
Bunny's face cut at the right. Fix: [GFX-CHAR-DOLLS-01](#gfx-char-dolls-01).
Until then, tuck their damaged edges behind a fold of the picnic blanket and
never place them at the screen edge.

**GFX-LAWN-14 — A white patch in the Wacky and Chuck portrait.** P2.
Evidence V. Owner. Inside the curl of the merman's tail an unremoved white
background shape, with speed lines from the jumping dog, shows as a white hole
against the green bushes. The portrait is protected. Fix: stage it where the
curl is covered by a foreground plant or sits against a pale cloud; or, with
the owner's approval, an alpha-only mask in a new file with no repainting.

**GFX-LAWN-15 — A tiny opening target.** P1. Evidence C. With WP-16. The
counter opening is a 9 px yellow ring of radius 110 around the King's centre
with four dots (lines 615-622). It is not the gold star the child learned on
Day One. Fix: show the Day One gold star (`assets/opera/worlds/props/fx_stolen_sparkle.png`,
`DustBossLesson2D.STAR`) large on his crown crest, and add
`fx_dizzy_stars.png` for the dizzy beat.

**GFX-LAWN-17 — Grey bars on wide phones.** P1. Evidence V, C. With WP-16.
The lawn draws nothing outside its 1280×720 canvas, so the renderer's default
grey shows at both sides: visible in every capture, and about 140 px a side on
a 19.5:9 phone. The castle rooms use a violet backdrop. Fix: extend the
panorama (it is 6144 px wide) or give the lawn a matching backdrop colour.

**GFX-LAWN-18 — The nearest guests are the smallest.** P1. Evidence V, C.
With WP-16. Kareem, Huluu and Flower Friend stand nearest the camera (y
550-700) but draw smaller than Roshan in the middle distance (foot 560),
because every guest uses the same box. Depth reads backwards. Fix: the height
table and depth bands in [GFX-LAWN-05](#gfx-lawn-05).

<a id="gfx-lawn-19"></a>
**GFX-LAWN-19 — The guide hand misses every target.** P0. Evidence C, M, V.
With WP-16, but fix now. The hand is an 88×88 picture placed at the target
plus (18, 8) (`chapter_two_lawn_finale_2d.gd:425`), and its fingertip sits at
about (37, 77) inside the picture. So the fingertip lands about 55 px right
of and 85 px below every target: in the captures it points at the rocket's
fins, not its brass button, and below the forward button, partly off the
canvas. Fix: place the hand so its fingertip, not its corner, is on the
target; add a probe that the fingertip lies inside each target's rectangle.

**GFX-LAWN-20 — Roshan's face never changes.** P1. Evidence V, C. With
WP-16. She keeps the base cutout's happy smile through the demand, the theft
and the loss. The approved gesture sheet
(`assets/characters/roshan_25d/roshan_gestures.png`, 16 poses) goes unused on
the lawn. Fix with no new art: surprised hands-up at the stomps, hands
clasped for "He's so big…", pointing for her invitation, the self-hug for the
theft, eyes-closed clasped hands for "We'll find our light together", cheers
for the ignition, and the holding pose for the hat. A sad pose is an art gap.

**GFX-LAWN-21 — The Prince stands with Roshan.** P1. Evidence V, C. With
WP-16. The Prince's box (x 848-958) sits shoulder to shoulder with Roshan,
so he reads as her ally rather than his father's son. Fix: keep him half a
step behind the King and apart from Roshan until he helps in round 2.

**GFX-LAWN-22 — The grass outshouts the characters.** P1. Evidence M. With
WP-16. Measured on the party capture, the open grass is more saturated (0.77)
than every character (0.33-0.60), and the dark King (value 0.33) stands
against the dark hedge (0.42). Fix without restyling the approved painting:
stage the King where the lighter cloud and sky band is behind him, add a soft
2D rim-glow sprite behind dark figures, and ask the owner before any colour
grade on the panorama.

<a id="gfx-lawn-16"></a>
**GFX-LAWN-16 — The birthday girl has no hat.** P1. Evidence V. With WP-16.
Roshan wears no hat at her own party. She uses one still cutout except while
reaching, and stands in the empty right half facing the camera. Fix: Daddy
puts a painted hat on her in F1 (the hat set from GFX-LAWN-01). It tumbles off
in F4 and Lamma brings it back in F7. Add her swim and reach states from the
`roshan_25d` family as she moves.

**GFX-CIN-01 — The finale shot board shows one frame nine times.** P1.
Evidence V. With WP-20. `assets_src/cinematics/chapter2_lawn_scale_v2_2026-09-06/SHOT_BOARD.png`
repeats the same locked wide runtime frame for all nine beats, HUD included
(Back, forward button, caption, title, grey bars), with no close or medium
shots for the ignition, the demand, the apology or the theft. It is honestly
labelled as a draft reference. Fix: WP-20's revised cards use clean first
frames without HUD, with a shot choice per beat.

## 7. Characters

| ID | Sev | Evidence | Flaw | Fix |
|---|---|---|---|---|
| <a id="gfx-char-king-01"></a>GFX-CHAR-KING-01 | P0 | V, M, C | One still cutout (`assets/chapter2/ember_alpha/king_v4_cutout.png`, 747×817) for every beat. Its palm-up gesture reads as welcoming, not demanding. Its edge has no soft pixels at all (hard alpha) and a thin white keyline runs round the whole silhouette, so it stair-steps at 0.36 scale and looks like a sticker | Now, with no new art: whole-card acting (a squash and heavy drop for each stomp, a tilt for the wobble, a spin with `fx_dizzy_stars.png`, a flip to turn away, a slide to walk), with `fx_dust_puff.png` on each step. Next: isolate the views the approved sheets already show, as the V4 gameplay cutout was isolated: the owner reference (`assets_src/cinematics/chapter2_lawn_scale_v2_2026-09-06/characters/ember_king_owner_reference.jpg`) has a side view for walking in and out, a back view (with the glowing shell seams) for leaving, and four head expressions. Then a pose set (point, foot up, foot down, wobble, reach, hold the candle), with soft antialiased edges. It is an approved identity: poses only, never a redesign |
| GFX-CHAR-KING-02 | P2 | V | For a four-year-old the design has sharp cues: horns, lower tusks, claws, spiked cuffs, a chain | Do not redesign. Keep the menace comic through acting (big wobbles, dizzy stars), distance (never looming over the guests), and a theatrical rather than scary voice |
| <a id="gfx-char-prince-01"></a>GFX-CHAR-PRINCE-01 | P0 | C | Runtime uses one idle frame (`prince_idle.png`, region 144×301). The V2 motion package (`idle_glance`, a 16-frame `sleek_walk`, `cinderstep`) is described in `ember_prince_ANIMATION_DELIVERY.txt`, but its atlas files are not in this tree; the record cites commit `671b8b4a` | Recover and commit the V2 package from history, then use `sleek_walk` in and out and `idle_glance` in dialogue. The identity sheet (`ember_prince_identity.png`) has front, side and back views and four heads, including a sad face for "I'm sorry": isolate those. New poses are an art gap: the "Over here!" point, one clap, the look back |
| GFX-CHAR-PRINCE-02 | P2 | V | Father and son do not read as family: a chunky, big-headed King and a lanky Prince with realistic proportions and different skin rendering | Both are approved; do not repaint either. Stage the bond: they enter together, the Prince mirrors his father's first pose, both leave the same ember-dust footsteps |
| <a id="gfx-lamma-01"></a>GFX-LAMMA-01 | P0 for Day Two | V, M | Two Lamma designs. The companion card (`assets/sprites/stuffie_studio/lamma.png`) is an egg-shaped plush in flat cel shading, grey-white shaded blue-grey, legless, holding a lavender Easter egg, matching the protected identity source (`assets/characters/lamb_0.png`). The Seek sheet (`assets/minigames/seek/lamma_animation.png`) is a bright fluffy lamb with little feet and no egg. Evie's protected portrait shows a third look: a round, fluffy, pale-blue lamb. The identity source itself is opaque, on a teal ground, with brand-like lettering on the egg, so it cannot be used as a cutout | Make the identity-source design canonical: egg shape, no legs, the lavender egg. Derive the moments Day Two needs from it as new files: peek, hide, bounce away, sniff, hug the egg, dance, hat offer. Keep the Seek sheet as provenance. Owner art review |
| <a id="gfx-lamma-02"></a>GFX-LAMMA-02 | P1 | V, C | Two Lammas at the party: Evie's protected portrait (`pearl_friend.png`) already shows Evie hugging her, so any separate Lamma on the stuffie blanket makes two | At the party, stage Evie with her Seek sheet (`assets/minigames/seek/evie_animation.png`: idle, point, giggle, clap, cheer), which has no lamb and also gives her reactions. Or the owner decides otherwise ([decision 9](README.md#owner-decisions)) |
| GFX-CHAR-EAGLE-01 | P1 | V, C | Baby Eagle is one still pose (`assets/characters/companions/baby_eagle.png`), follows only in castle rooms, and is absent from the Sky Lagoon and the lawn | Extend the follower to the Sky Lagoon and lawn. Poses Day Two needs: chirp on a branch (J1, F2), carry the banner (F5), hop along. The Book One page 20 art (`eagle_inviting.png`, on the book branch) is a source for a walking pose, with owner approval |
| GFX-CHAR-PUFF-01 | P1 | V, C | The rainbow friend (Grand Puff restored) is one still 132 px card (`rainbow_friend.png`), castle only, with no tap. He has no wings | Now: a whole-card hop (squash and stretch) and a tap reaction. Next: presence on the Sky Lagoon and lawn, and the rainbow dome effect. He always hops, never flies |
| GFX-CHAR-BUNNY-01 | P2 | V | Good dust bunny art exists (curl ears, family, hop, shell hide, sleepy, swimming), but not the helpful poses Day Two needs | New small poses from the same family: carrying a strawberry, rolling (for the wall), saying sorry (the book's `bunny_apology_canvas.png` is a source, with owner approval). On Day Two the Main Hall's three pop-for-a-pearl bunnies also return on every castle visit, under the party table; in v2 they are the playful helpers, not targets |
| <a id="gfx-char-dolls-01"></a>GFX-CHAR-DOLLS-01 | P1 | V, M | Kitty (`assets/book/doll_cat.png`, 220×205) has a hole in her nose, a see-through speckled belly, straight cuts along her left and bottom edges and a stray fragment. Bunny (`doll_bunny.png`, 220×159) is cut off at the right edge through the face, with a ragged bottom and stray line fragments | Protected, so never edit these files. Ask the owner to authorise re-isolations from the full book source pages, saved as new files with provenance ([decision 11](README.md#owner-decisions)). Until then, never enlarge them above their native size, and hide the damaged edges |
| GFX-CHAR-GUESTS-01 | P1 | V, C | The guest portraits mix styles and sizes, and hats hide faces (GFX-LAWN-01, GFX-LAWN-05) | Staging only: sizes, bands, shadows, hats, as in those findings |
| GFX-CHAR-GUESTS-02 | P2 | M, V | Several portraits carry a pale halo along their edges (a white rim measured on Flower Friend, Faron, Evie, Harper and Fiona, and Wacky and Chuck), which shows as a light outline on the green lawn. Huluu's portrait is 640×1039, above the 1024 px texture rule | Protected: no edits. Stage them against mid-value backgrounds; alpha-erode derivatives only with the owner's approval ([decision 11](README.md#owner-decisions)) |
| GFX-CHAR-RUMI-01 | P2 | V | Rumi's sheet (`rumi_eight_pose_runtime.png`) is in a realistic teen style unlike chibi Roshan, with a faint greenish edge fringe; two cells touch their left edges; frame 0 is clean | Use frame 0 and the wave cells only. No new frames (IP hold) |
| GFX-CHAR-DADDY-01 | P1 | V | Daddy has no pose beyond his still portrait, and Day Two makes him the planner, the coach and the hug | Whole-card motion for now. Pointing at the Party Plan, tying the apron and the hug are art gaps. Day One clip frames are not borrowed (`DL-CIN-16`) |

## 8. Props

| ID | Sev | Evidence | Flaw | Fix |
|---|---|---|---|---|
| <a id="gfx-prop-cake-01"></a>GFX-PROP-CAKE-01 | P1 | V, M | In the frosted and final cakes the blue and violet tiers share one cylinder: the blue swag drapes across the colour change, with no pearl ledge between. A child counts five tiers and a purple skirt. In the unstacked-to-stacked art the violet base is no wider than blue, although the baked rounds grow strictly from red to violet | A derivative with a violet ledge wider than blue and a pearl rim between them, in the stacked, frosted and final states |
| GFX-PROP-CAKE-02 | P1 | V, M, C | The final cake's five strawberries are about 60 px in the texture and about 10-18 px on screen (the lawn draws the cake 210 px wide; the table and job scenes about 0.30 scale). "Five strawberries" cannot be counted on a phone | Enlarge the berries in a derivative to at least 45 px on screen, or show a close-up when the Chef places them |
| GFX-PROP-CAKE-03 | P2 | M | The final cake art is about 6% smaller than the frosted art, so the cake shrinks when it is finished | Normalise the on-screen height |
| <a id="gfx-prop-cake-04"></a>GFX-PROP-CAKE-04 | P1 | V, C | The shell crest on top is not a candle holder. On the lawn the candle stands on the crest, which reappears when the candle is taken; in the Main Hall the cake hides the candle ([GFX-HALL-08](#gfx-hall-08)) | A small shell candle-holder derivative on the top tier (the candle node's code fallback already draws one), drawn above the cake |
| GFX-PROP-CAKE-05 | P2 | C | The superseded ten-strawberry cake (`chapter2_grand_candied_strawberry_cake.png`) still ships in the build | Move it to `assets_src/` with its provenance |
| GFX-PROP-CANDLE-01 | P2 | V | Good art: the unlit and lit candles line up exactly. The glitter turns to noise at 44-53 px (the Library and Detective sizes). The unlit candle's wick is dark and twisted, like one already burned | Show it larger when it is found. Optionally a pale wick on the unlit derivative |
| GFX-PROP-BERRY-01 | P2 | V | The field strawberries (`sky_lagoon_strawberry_single.png`, `…_cluster.png`) are sticker-style with thick navy outlines. The tray and cake berries are painterly, with no outline and a different stem. The child may not see them as the same berries. The cluster shows three berries in a five-berry job | Keep the field berries as the model. Match the tray and cake berries' outline and calyx in the derivatives above. Use five single berries, not the cluster, for "five" |
| <a id="gfx-prop-berry-02"></a>GFX-PROP-BERRY-02 | P2 | V | The candied tray's five berries touch, so they are hard to count | 6-8 px gaps in a derivative. Reused for the Chef's topping step, the berries are fresh, so no glaze is needed |
| <a id="gfx-prop-banner-01"></a>GFX-PROP-BANNER-01 | P1 | V, C | The only banner (`assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png`, 256×512) is a near-white pennant with an empty medallion. Nothing on it says birthday, it vanishes on sand and pale walls, and it has one state, so painting and stamping never change it | Non-destructive derivative states: painted (a cake and candle in the medallion, using the Craft Room colour Roshan chose on Day One), stamped (five gold stars), hung (on a hook with a shadow), and a horizontal garland version for the party. Leave the approved template untouched |
| GFX-PROP-ROCKET-01 | P1 | V, C | `goal_astronaut.png` is good art, but three rockets exist: the Astronaut world's painted rocket, this prop, and a second copy on the party table | One rocket everywhere: this prop (GFX-ASTRO-05, GFX-HALL-03) |
| GFX-PROP-MIC-01 | P2 | V | The shell microphone is good art, but floats on the lawn | On Rumi's small stage (GFX-LAWN-06) |
| GFX-PROP-BOX-01 | P2 | V | The music box (`goal_ballerina.png`) is good art, but floats beside Faron | On the stuffie blanket (GFX-LAWN-06) |
| GFX-PROP-CREST-01 | P2 | V | The Opera crests on the room cards are embossed, with ornate frames that leave the symbol about 25 px wide at runtime. The Chef, Farmer and Candy crests show a layer cake, vegetables and a wrapped sweet | Symbol-only small variants; Day Two variants (rainbow cake, strawberry) as derivatives |

## 9. New art the draft needs

Everything else reuses existing art. Each item below is new, small, and in
the navy-and-plum-contour storybook style.

| Art | For | Notes |
|---|---|---|
| Arborist job art | J1 | Exists with the owner; commit it (GFX-ARB-01) |
| Party hat set (4 colours, 2 sizes) | F1-F8 | GFX-LAWN-01 |
| Picnic blanket and cushions | Finale | GFX-LAWN-05; or reuse castle cushions |
| Rainbow dome effect | F5 | GFX-LAWN-09 |
| Lily pad safe spot | F5 | GFX-LAWN-08 |
| Launch pad for the rocket | F3 | GFX-LAWN-06 |
| Party Plan board and its empty-frame state | D2-OPEN-2 | 03 |
| Strawberry plants (3) and a basket that fills 1-5 | J2 | GFX-FARM-02, GFX-FARM-04 |
| Pipe-tile kit; star-note pads; patch pieces | Practice and freeplay | GFX-SYS-05, GFX-ASTRO-02, GFX-ASTRO-03 |
| Costume overlays for Roshan (8) | In-world levels | GFX-SYS-04 option (b) |
| King pose set | F4-F6 | GFX-CHAR-KING-01 |
| Prince poses: point, clap, apology, look back | F4-F6 | GFX-CHAR-PRINCE-01 |
| Lamma poses in the canonical design | LAMMA-*, F7 | GFX-LAMMA-01 |
| Baby Eagle: branch chirp, banner carry, hop | J1, F2, F5 | GFX-CHAR-EAGLE-01 |
| Dust bunnies: strawberry carry, roll, sorry | J2, J3, F5 | GFX-CHAR-BUNNY-01 |
| Daddy: point, apron, hug | D2-OPEN, J3, F7 | GFX-CHAR-DADDY-01 |
| A painted Dining Room plate (then the Family Gallery and Movie Lounge) | The Farmer's launch room | GFX-ROOM-03, GFX-ROOM-04 |
| Derivatives: cake ledge and berries, banner states, tray gaps, candle holder, costume alpha repair, venue plaques, Day Two medallion | Various | Sections 1-8 |

## 10. Fix order and work packages

| Step | Fixes | Package |
|---|---|---|
| Now: can the child finish, and does it look broken? | GFX-DET-03, GFX-SYS-13, GFX-HALL-07, GFX-HALL-08, GFX-ROOM-06, GFX-LAWN-19 | WP-18, with the B1 repair from 05 |
| Now: fixes with no new art | GFX-SYS-01, -02, -08, -09, -10; GFX-DET-02; GFX-CHEF-04; GFX-FARM-07; GFX-DET-07; GFX-HALL-06, -09, -10, -11; GFX-LAWN-17, -20; GFX-ROOM-01; GFX-CARD-04 to -07; GFX-PROP-CAKE-05 | WP-18 |
| Now: derivative repairs | GFX-SYS-03; GFX-PROP-CAKE-01 to -04; GFX-PROP-BANNER-01; GFX-PROP-BERRY-01, -02 | WP-18 |
| Owner decisions | GFX-SYS-04 (decision 10); GFX-LAMMA-02 (decision 9); GFX-CHAR-DOLLS-01, GFX-LAWN-14, GFX-CHAR-GUESTS-02 (decision 11) | WP-00 |
| Opening and the Main Hall picture | GFX-CARD-01 to -03; GFX-HALL-01 to -05 | WP-03 |
| Friends in the challenges | GFX-ROOM-01; GFX-CHAR-EAGLE-01, GFX-CHAR-PUFF-01, GFX-CHAR-BUNNY-01, GFX-CHAR-DADDY-01 | WP-06 |
| The in-world levels | GFX-FARM-*, GFX-CHEF-05/-07/-09, GFX-PAINT-*, GFX-BALLET-04, GFX-POP-02/-04, GFX-ASTRO-04/-05, GFX-DET-08, GFX-ROOM-02 to -05 | WP-05, WP-07 to WP-14 |
| Lamma | GFX-LAMMA-01, -02 | WP-15 |
| The finale | GFX-LAWN-* (except -17, -19, -20), GFX-CHAR-KING-*, GFX-CHAR-PRINCE-*, GFX-CHAR-GUESTS-01, GFX-CHAR-RUMI-01 | WP-16 |
| Cinematic cards | GFX-CIN-01 | WP-20 |
| Venue | GFX-VEN-* | WP-18 (VEN-03 waits for the commissioned venue) |
| Arborist | GFX-ARB-01 | WP-07 (Step 0 of the Arborist handoff) |

## 11. Keep: the strongest art

- The career world paintings themselves (Chef's palace kitchen, the candy
  factory, the Painter's coral garden, the Pop Star shell stage, the
  Astronaut dome lab). Only their framing is broken.
- The cake progression art: clear rainbow order, baked rounds growing from
  red to violet, the same bowl and spoon from mixing to stirring (the
  batter-coated spoon is a lovely causal detail), and a final cake with
  exactly five berries and no candle baked in.
- The rainbow candle pair: identical body in both states, a strong
  silhouette, true to the story.
- The single Sky Lagoon strawberry: the cleanest navy-outlined cutout here.
- The costume design language: each hat and prop names its job at a glance.
- The painted props: pitcher, whisk, pearl microphone, magnifier, shell
  microphone, music box, the party rocket, and the four painted effects
  (telegraph ring, dust puff, dizzy stars, gold star).
- The dust bunny family and the rainbow friend's art.
- Evie's Seek sheet: clean, and useful for reactions at the party.
- The architecture: one persistent cake, the candle as its own layer, and
  a frozen 1280×720 stage with correct touch mapping.
- The scale-v2 lawn numbers: the King, Prince, Roshan, candle and stuffie
  sizes are much better than the earlier staging; keep them.
- Roshan's approved gesture sheet: sixteen poses ready for acting.
