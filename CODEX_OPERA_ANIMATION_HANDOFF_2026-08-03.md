# Codex handoff — minigame animation, feedback and completion art (2026-08-03)

**Audience:** Codex — image generation + deterministic promotion.
**Purpose:** the 2026-08-02 widget delivery made every instruction *nameable*
(a real bowl, a real gauge, real lane tokens). It did not make any
instruction *happen*. 154 widget PNGs are on disk and the card is still a
still photograph while the child's finger is on it, and there is not one
picture anywhere in the game of a job being finished. This file specifies
the art that makes the widgets MOVE and END.

This is the animation sequel to
`CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md`. **Every convention in that
file binds here unchanged** — canvas specs, POT rules, STYLE-JOBS /
STYLE-HOUSE contracts, the green-is-reserved rule, P2-09 canonical prop
locks, content locks, filename grammar, the weighted acceptance gate, the
staging protocol, and the ledger/manifest requirement. Only the deltas are
restated (section 3).

Source audits (three parallel passes over all 88 phases, run 2026-08-03):
hold-and-fill (pour/basin/charge), timing-and-choice (gauge/track/lanes),
motion-and-world (trace/push/crank/target/bop/lens).

Nothing here is blocking. Every file falls through to what exists today.
Deliver in any order; each file upgrades one moment the hour it lands.

---

# 1. THE FINDING

## 1.1 The playtest quote (2026-08-03, the four-year-old, chef career)

> "In the pouring of the bowl in the Baker game, there is no actual bowl
> being poured. No animations. It is simply a bowl. It is not clear what
> the instructions are. Holding a finger down causes it to slowly rise,
> but there is no feedback or animation demonstrating that the game is
> being successfully completed."

Three complaints in one sentence, and they map exactly onto the three
questions this handoff is organised around: **CLARITY** (what do I do),
**FEEDBACK** (is it working), **COMPLETION** (did I win).

## 1.2 The wiring root cause — already found and fixed

The progressive overlays shipped on 2026-08-02
(`_fill` / `_bubbles` / `_full` / `_glow` / `_progress` / `_lit`) were
loaded correctly, registered correctly, and drawn correctly against
`OperaGestureSurface.widget_fill`. `set_fill()` existed on the surface.
**`opera_career_world_2d.gd` never called it.** `widget_fill` stayed 0.0
for the entire life of every phase, so every progressive overlay in the
game rendered empty — including the batter in the chef's bowl. It is now
wired to phase progress (`opera_career_world_2d.gd:1048`, `:1127`).

**This handoff exists to answer: what else is like that, and what is
genuinely missing art rather than missing wiring.** The audits found the
same failure class four more times (section 2, Table A) — art on disk,
drawn on the wrong trigger, at the wrong coordinates, or never reached.
Commissioning art for those would have been wasted money.

## 1.3 Headline numbers

88 phases across 13 careers: 26 bop, 11 hold, 11 timing, 10 swipe, 10
choice, 9 circle, 8 tap, 2 lens, 1 catch. 60 of them are widget-backed
(the 2026-08-02 census), 154 widget PNGs delivered.

87 phases were scored across 40 audit rows (nursery CATCH BABIES was not
audited). Scores are 1–5; 4 = "a four-year-old gets it unaided".

| axis | rows under 4 | beats under 4 | rows scoring 4+ |
|---|---|---|---|
| **CLARITY** | **37 of 40** | **78 of 87** | trace, lens, crank-adjacent, painter REVEAL |
| **FEEDBACK** | **36 of 40** | **44 of 87** | trace 4, crank 4, lens 4, **bop 5** |
| **COMPLETION** | **40 of 40** | **87 of 87** | **none** |

Read that bottom row again. **Not one beat in the game — not one of 87 —
has a legible finish.** The only score of 5 anywhere in the audit is bop
FEEDBACK, and bop is the one beat that plays on the painted stage with
real FX sprites, real pose swaps and real bursts. It is the proof that the
house style already knows how to do this; the widget cards just never got
the same treatment.

Two more measured facts that frame everything below:

- **The chef POUR card stops changing at t = 2.16 s of a 5.0 s hold** and
  sits frozen for 2.84 seconds while the child keeps holding. The `_fill`
  ink occupies y 345→553 of a 608 px canvas but the engine sweeps the
  reveal across the *whole card*, so the ink is fully drawn at 43 %
  progress. That is the playtest complaint, still true after the
  `set_fill` fix, and it is a wiring bug (Table A, W2) — not art.
- **Zero `op_*` voice files exist.** `assets/audio/voices/` holds 293
  files; none of the 88 phase `vo` keys (`op_chef_pour`, `op_chef_bake`, …)
  resolves. The instruction reaches the child only as English text in
  `show_msg()`. See section 5, gap (c) — this is the single most important
  finding in the document.

---

# 2. SPLIT THE WORK HONESTLY

Three tables. **Codex only needs Table B.** A and C are recorded so nobody
commissions art for a code bug, and so the engine work lands in the same
workstream (the P7 no-orphans rule).

## Table A — fixed by WIRING (engine work, no art)

| # | beats | what is wrong | the fix |
|---|---|---|---|
| W1 | 5 charge | `widget_charge_<career>_full.png` **is** the filled meter tube (`registration: meter=940..1000,90..540`) and the engine fades the whole tube in at `widget_fill > 0.82`. Measured dead time with an empty meter on screen: 3.28–4.10 s per beat. **The set_fill bug, still live.** | reveal the band `y ∈ [90+(1-fill)·451, 541]` clipped to the declared meter rect |
| W2 | 4 pour, 2 basin, 6 trace | `_draw_progress_overlay` maps the reveal to the 608 px **card**, not to the overlay's ink. pour ink y 345→553 → saturates at fill 0.43. basin ink y 146→463 → dead until 0.24, frozen after 0.76. | lerp the reveal edge across the overlay's opaque bbox; add a `fill_rect` field to the widget set, fed from the ledger |
| W3 | **all 87** | no completion moment exists. `phase_progress >= goal` → `phase_index += 1` → `_show_phase()` → `configure()` zeroes `widget_fill` and swaps textures **before the draw pass runs**. `basin`'s `widget_fill >= 0.96` pop lives ~0.18 s; `target`'s is unreachable by construction. `phase_gap = 1.0` is commented "the between-phase sparkle sting" and **nothing anywhere draws for it.** | `_finish_phase()`: pin `widget_fill = 1.0`, draw the done card + burst, hold 0.9 s, *then* advance |
| W4 | 11 timing | `widget_gauge_*_success.png` and `widget_track_shared_hit.png` are gated on **where the marker is**, not on whether the child tapped. A correct tap changes nothing. | add `hit_flash`, set in `_press` when the tap lands in the zone, decay in `_process`, gate the layer on it |
| W5 | 10 lanes | a **correct** pick calls `queue_redraw()` and draws zero pixels (`choice_flash` is already 0); a **wrong** pick calls `reflash_choice()` and lights up the answer. Feedback is inverted; optimal strategy is to tap wrong on purpose. | `pick_flash` timer + burst on the picked lane; re-arm `choice_flash` on the rotated target |
| W6 | 10 lanes | the `_lit` cell is drawn at `size.y * 0.70`, **44 px below** the painted pads (measured centres x 0.183/0.500/0.816, **y 0.509**), and 124 px against a 90 px pad | `size.y * 0.509`, lanes 0.183/0.500/0.816, box 90 |
| W7 | 3 gauge | `timing_zone` has **zero writes** outside its declaration; every beat runs `Vector2(0.30,0.72)`. Against the painted wedge (−16.0°..+28.7°) that makes **−24.0°..−16.0° a lie band**: needle over the dark dead zone, tap scores, success glow fires. Track is correctly calibrated (0.307..0.712 vs 0.300..0.720 — leave it alone). | `timing_zone = Vector2(0.367, 0.739)` for gauge, or repaint the wedge symmetric (see R9) |
| W8 | 4 push | nursery BEDTIME has **no `"dir"` key** → `swipe_dir` stays RIGHT while the loader picks the **down** arrow and the VO says "down". push travel is `widget_fill * 42.0` px — 11 % of a 392 px card across a 7–9 s beat, sub-perceptual per stroke. | add `"dir": "down"` at `:141`; travel to ≥250 px and track the pointer laterally |
| W9 | 8 target | `_draw_demo_finger` has no `"tap"` case → the idle nudge re-pulses the ghost at card centre while `tap_point` has relocated. `_relocate_tap_point` ±0.26 h with a 142 px mover clips the prop off the top and bottom. | add `"tap": at = tap_point`; tighten relocation to ±0.18 h |
| W10 | 9 crank | `previous_angle` is only written in `_press`/`_drag` and never reset in `configure()`, so during the ghost demo the handle sits frozen at the previous phase's stale angle while a dot orbits it | drive `previous_angle` from `demo_t`; reset it in `configure()` |
| W11 | 2 lens | `lens_demo` is set false on first touch and **never restored**; the 9 s idle nudge calls `restart_demo()` on a surface that is invisible during lens | restore `lens_demo = true` on the idle nudge |
| W12 | 26 bop, 2 lens | `phase_fill` and `phase_label` are children of `action_panel`, which `_apply_panel_layout` hides for bop and lens → **no progress indicator at all** during a 10-goal captain chase | reparent `phase_fill` to `root` |
| W13 | 11 hold | `_bounce_actor` spawns a fresh tween **every frame** of a hold, each capturing a mid-bounce y as "home"; hundreds fight over `position:y`. The one on-stage reaction to holding is a jitter. | gate it behind the existing `score_cool` |
| W14 | 11 hold | a finger already down cannot skip its own `phase_gap = 1.0`; the child holds through a phase boundary and earns nothing for a full second, silently | `if mode == "hold" and surface.held: phase_gap = 0.0` |
| W15 | 60 widget | `_draw()` early-returns the whole `match mode:` block when `widget_backdrop != null`, so the hold ring and the growing white dot — the only elements in the file that respond to `held` — never render. Shipping the lanes art also **silently deleted a working gold flash**. | draw the affordance accents over the widget layers, per the 2026-08-02 layer order |
| W16 | — | dead code and paste damage: `_draw_nursery_context` is unreachable (context is now `track_nursery`), `baby_0/1/2.png` load on every nursery widget phase and are never used, `set_bop_targets()` is never called, `set_fill` is pasted twice at `:1048-1049` and `:1127-1128`, `set_fill(0.0)` twice at `:703`/`:726` | delete / de-duplicate |

## Table B — needs NEW ART (this is Codex's table; specified in section 4)

| # | files | template · beats | why art, not wiring |
|---|---|---|---|
| R1 | 4 | pour · mover | **every pour `_mover` is a 256 px crop of its own backdrop** (`"source": "widget_pour_chef.png"`). chef = the same bowl and whisk again. Drawn while held it renders as two overlapping bowls. There is no jug, no stream, no hand anywhere in the template. |
| R2 | 4 | pour · fill | every `_fill` is a translucent rounded **pill** (1.2 % opaque) sitting on the vessel's *outer front wall*, below the rim. The painter's canvas — the one surface that must fill — never changes. |
| R3 | 2 | basin · bubbles | `_bubbles` are three near-white broken concentric **rings** (mean RGB 242,250,242) on near-white paper. They read as fog wiping across the sink. |
| R4 | 5 | charge · glow | all five `_glow` files are byte-comparable generic cream discs with a navy ring — **pixel-for-pixel the design `_draw_demo_finger` paints for the hint**, at the same centre. "You are charging" and "put your finger here" are the same picture, stacked. |
| R5 | 13 | 6 backdrops depict the **wrong subject** | `charge_farmer` = a strawberry, a raspberry and blueberries (beat: MUD HOP). `basin_nursery` = the swaddled baby, identical to `pour_nursery` — **WASH HANDS and FEED are the same picture**. `pour_painter` = a blank canvas while the VO promises a glowing shape. `pour_nursery` has no bottle. `push_boxer` paints a **horizontal** track for a DOWN-gated swipe. `push_nursery` paints a horizontal track for "swipe the blankets down". Plus 4 alpha/crop defects and 3 duplication defects. |
| R6 | 10 | lanes · lit | the `_lit` cells are **not lit**. Measured mean luma vs the same pad in its own backdrop: popstar −0.9, boxer +1.1, farmer +0.4, detective **−12.2**. In two of four the "on" state is *darker* than "off". |
| R7 | 7 + 8 | target · mover, mark | `widget_target_racer.png` is a checkered flag and `_mover` is **that same flag**. At phase start a 142 px flag is drawn on top of the painted flag. Every `_mark` across all 8 careers is the same generic pip — never a cherry, a splat, a patch. |
| R8 | 9 + 3 | crank · progress, mover | all nine `_progress` files are one generic three-concentric-ring **loading-spinner glyph** in career tints — pixel-identical to `widget_target_boxer_success.png`. `crank_painter_mover` has an **opaque navy square background, no alpha cutout**. `crank_popstar_mover` is an entire proscenium theatre being spun. `crank_racer_mover` is a whole car spun like a pinwheel. |
| R9 | 7 | gauge · needle, success, backdrops | `_shared_needle` is a **symmetric bar with a dot at each end** — no tip, so a non-reader cannot tell which end points at the wedge; it reaches 69 % of the painted radius. The three `_success` files are **byte-identical** (`be61d2f5…`), a 5 %-alpha pale-green glow on a near-white card. The three backdrops are the same abstract dial with a sticker in the corner — BAKE, BOOST and TURBO are indistinguishable. |
| R10 | 6 | track · movers, hit, 2 backdrops | `track_boxer_mover` is the same gloves already painted static above it; `track_nursery_mover` is the same swaddled baby. Two identical objects, one inert and one sliding, and nothing depicts the verb. The mover at 128 px on a 232 px surface **covers the whole green zone at the moment of truth.** `track_shared_hit` and `lanes_shared_pick` are **byte-identical**. `track_detective` ships a raw un-matted crop (hard-edged dark rectangle). |
| R11 | 1 | lens · found clue | a found clue is `draw_circle(spot, 10.0, …)` — a **10-pixel dot on a 1280×720 stage**. No found-clue art exists anywhere. |
| U1 | 2 | **all 87 beats** | no beat has a completion image. `pour` ships no completion asset at all; `push` and `trace` have no `_full`/`_success`/`_lit-done` slot in the loader or on disk; 7 of 8 target `_success` files do not exist. |
| U2 | 5 | **all 60 widget beats** | `_draw_widget_layers` has **no time term** for pour/basin/charge/push/target/lanes, and the surface stops redrawing entirely once the demo ends. Between gesture events the card is a still photograph. |
| U3 | 8 | **all 88 beats** | the instruction channel does not exist for a non-reader (section 5c). |
| BD | 47 | every backdrop | every one of the 60 backdrops carries a **dead gold badge oval** at top-centre (~455,25–575,90) that no code path ever draws into, plus the blank fill pill. Both are visible at rest and read as unfinished art. Mechanical clean re-export. |

## Table C — DESIGN change (neither wiring nor art alone)

| # | beats | the problem |
|---|---|---|
| D1 | 10 lanes | the target rotates on every correct pick and is never re-shown; the only way to see it is a wrong pick. **The learned strategy is: tap any lane, wait for the mercy flash, tap the flashed lane.** boxer ROUND and popstar DANCE at goal 8.0 = ~16 taps of blind guessing. Either stop rotating within a phase, or re-flash the new target. |
| D2 | 60 widget | `phase_fill` is a default-themed `ProgressBar` with no StyleBox on a `#e6f5ff` card — grey on grey — and it is currently the **only** element that moves smoothly for a whole hold. The least diegetic thing on screen is carrying the entire progress signal. Style it in the StorybookUI language or delete it and let the art carry the load. |
| D3 | ~pre-finale | `competition.note_success()` no-ops before `competition.begin()`, which only runs at `_finale_start()`. On a pre-finale gauge/track/lanes beat the complete response to a correct action is: Roshan hops 14 px on the painted stage, several hundred pixels from the card the child is looking at, and a grey bar moves. |
| D4 | magician CABINET, detective NAME, nursery BURP | the template was applied without adapting the verb. "Tap on the star flashes to open the cabinet" over a top hat on a bar. "Tap when the spotlight shines on the answer" over a grey rectangle. "Tap in the green for gentle burp-pats" over a baby sliding sideways. **Where the template cannot carry the fiction, change the beat's template — do not commission art for it.** These three are excluded from section 4 pending an owner decision. |
| D5 | 2 lens | clues are invisible beyond 118 px, so before the magnifier moves the stage looks empty and "find the glowing clues" has no referent. |

---

# 3. Shared delivery contract — deltas only

Everything in `CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md` §1 binds
unchanged. Additions for animation work:

- **No frame sequences. Zero. Every request in section 4 is a SINGLE
  SPRITE that the engine tweens, masks, scrolls, rotates or swaps.** The
  engine already owns `_draw_progress_overlay` (mask), `draw_set_transform`
  (rotate), `_draw_widget_sprite` (scale/translate) and
  `draw_texture_rect_region` (scroll). Frame sequences would need a new
  loader, a new atlas convention, and a memory budget nobody has costed.
  Where a request needs continuous motion it is served by a **tileable**
  or **radially symmetric** shared FX sprite (section 5b) rather than by
  frames.
- **Scale conversion, use it on every request.** Backdrops are 1024×608;
  the runtime surface is **392×232** (`_apply_panel_layout`), inside a
  440×384 card on a 1280×720 stage. **1 surface px ≈ 2.62 backdrop px.**
  Every "drawn at N px" figure in the engine converts to N × 2.62 in
  authoring space, and every request below gives both.
- **Author for 38 % linear.** The 2026-08-02 contract said "child-readable
  at 50 % scale". The measured runtime is 392/1024 = **38 %**. Tighten to
  that. The gauge needle and the lane lit-states are the two assets that
  failed this test in the last delivery.
- **Mask-friendliness is a content lock.** Any asset the engine reveals
  progressively (`_fill`, `_bubbles`, `_full`, `_lit`, `_progress`) is cut
  by a straight edge at an arbitrary position. Therefore: the ink must be
  **opaque** (alpha ≥ 240 in the body, semi-alpha < 15 % of solid), must be
  **monotonic** along the reveal axis (no floating islands above the cut),
  and must **not** rely on a baked edge treatment at 100 % — the engine
  draws `fx_widget_meniscus.png` at the cut line instead (section 5b).
- **New ledger field, mandatory on every masked overlay:**
  `fill_rect=x0,y0,x1,y1` in 1024×608 backdrop space, the exact opaque
  bbox of the ink. The engine reads it to fix W2. An overlay delivered
  without it cannot be wired and will be rejected at the gate.
- **New manifest `registration` grammar**, extending the accepted forms
  (`crop=bottom_up;registered=1:1`, `meter=940..1000,90..540`,
  `subject_center=512,304`):
  - `fill_rect=350,230,675,352;axis=up` — masked overlays
  - `anchor=168,96;pivot=128,128;sway=±8deg` — movers the engine tilts
  - `emit=568,212` — the point a shared FX sprite is emitted from
  - `hold=0.9s` — done cards
- **Green stays reserved** (house value ≈ RGB 117,240,158): only the baked
  go-zone of gauge/track. **This now explicitly includes the done cards** —
  a finished cake is golden and pink, never green, or the child learns that
  green means two different things.
- **Filenames** extend the existing grammar with exactly one new state
  suffix: **`_done`**. `widget_<template>_<career>_done.png`. And one
  semantic correction: **`_success` from now on means the momentary HIT
  flash** (gauge, target), gated on `hit_flash`; **`_done` means the
  terminal finished-thing card**, held 0.9 s at phase end. The one
  delivered `widget_target_boxer_success.png` is re-authored as
  `widget_target_boxer_done.png` (it is the generic ring spinner today).
- **Paths** follow the existing house split: widget layers →
  `assets/opera/worlds/widgets/`; `fx_widget_*` → `assets/opera/worlds/props/`
  (alongside `fx_telegraph_ring.png`, `fx_slash_arc.png`, `fx_dust_puff.png`);
  `hint_*` → `assets/opera/worlds/ui/` (alongside `magnifier.png`,
  `station_marker.png`, `task_card_frame.png`).
- **Staging** unchanged: `assets_src/concepts/opera_regeneration_2026-08-01/cards/`
  + contact sheets + PROMPTS.md + ledger rows, weighted gate ≥4.5 /
  target ≥4.7, one controlled promotion commit, one `ASSET_LICENSES.md`
  line per accepted asset, QA renders at gameplay scale on the Mobile
  renderer. **Candidates without runtime captures cap at 2/5 and must not
  ship** — and for this delivery a runtime capture means a capture *mid-
  gesture*, not at rest. A still QA render cannot show whether a mover
  reads while it moves.
- **Content locks** unchanged: no words/letters/numerals; no baked Roshan,
  Faron, rivals or imps; P2-09 canonical prop designs bind; species locks
  bind (Lamba is a finned bunny-fish, the doctor's patient is a five-armed
  coral starfish); bubbles never flame; stars only as effects; automatic-
  rejection list applies.

---

# 4. THE ANIMATION REQUESTS

Ordered by template. Each block gives: **file · canvas · how the engine
animates it · what it must depict · registration · the 100 % state.**

## R1 · `widget_pour_<career>_mover.png` — the vessel actually pouring (4 files)

**Careers:** chef (POUR), candymaker (SYRUP), painter (FILL), nursery (FEED).
**Canvas:** 256×256 RGBA POT, transparent, ≥12 px margin.
**Engine:** SINGLE SPRITE. Drawn only while `held`, at 138 surface px =
**362×362 backdrop px centred (512, 257)**. The engine tilts it ±8° about
its declared pivot and bobs it ±6 px on `elapsed`, and emits
`fx_widget_stream.png` from its declared spout point. No frames.
**Depict:** a **tilted vessel with its lip already tipped past pouring
angle**, mass to viewer-left, spout to the right and pointing down toward
the receiver. Draw the vessel *only* — the falling liquid is the shared
stream sprite, so the mover never contains a baked stream (it would tear
when the engine tilts it).
- **chef** — the batter pitcher from the work counter, tipped, batter
  clinging at the lip. **Not the mixing bowl.** The bowl is the receiver
  and is already in the backdrop.
- **candymaker** — the sparkling syrup bottle, tipped over the mold plates.
- **painter** — the canonical red-handle rainbow-mop brush (P2-09l) loaded
  and dripping, or the coral paint pot tipped. Brush preferred: it is what
  the fiction says.
- **nursery** — the warm milk bottle, tipped to the babies. This subject is
  named in the VO and **does not exist anywhere in the template today**.

**Registration (binding, this is what makes the stream line up):** the
**spout lip at sprite-local (168, 96) ± 8 px**; pivot for the sway at
sprite-local (128, 128). In backdrop space the lip lands at **(568, 212)**,
directly above the receiver interior. Ledger:
`anchor=168,96;pivot=128,128;sway=±8deg;emit=568,212`.
**100 %:** the mover is not the success state — see R2 and U1.

## R2 · `widget_pour_<career>_fill.png` — the liquid (4 files)

**Canvas:** 1024×608 RGBA, registered 1:1 to its backdrop.
**Engine:** SINGLE SPRITE, masked bottom-up **within the declared
`fill_rect`** (W2 fix), with `fx_widget_meniscus.png` drawn at the cut line.
**Depict:** the receiver **full**, painted to the exact silhouette of the
container's interior. Opaque body (alpha ≥ 240), flat broad colour field
per STYLE-JOBS, aqua/lavender shadow at the interior wall, no baked top
edge treatment.
- **chef** — pale sparkling batter filling the bowl interior. Measured
  target interior: roughly **x 350–675, y 230–352**. The delivered pill sits
  at y 345–553 — on the bowl's *outer front wall*. That is the defect.
- **candymaker** — mint/coral syrup filling the mold cavities, monotonic
  upward across the plate.
- **painter** — **the sunrise shape flooding with coral on the canvas.**
  The canvas is the surface that must fill. Nothing else on this card may
  change.
- **nursery** — this one **reverses**: the bottle's milk level *drains* while
  the babies' cheeks rosy up. Author the 100 % state as *empty bottle +
  rosy babies* and declare `axis=down` so the mask runs the other way.

**Registration:** `fill_rect=x0,y0,x1,y1;axis=up` (or `down` for nursery),
measured off the delivered backdrop, in the ledger row. **The vertical span
of `fill_rect` is the entire animation budget for a 4.2–5.0 s hold** — make
it as tall as the fiction honestly allows.
**100 %:** vessel visibly full to the brim with a settled surface.

## R3 · `widget_basin_<career>_bubbles.png` — suds, not fog (2 files)

**Careers:** doctor (WASH), nursery (WASH HANDS).
**Canvas:** 1024×608, registered 1:1. **Engine:** masked bottom-up within
`fill_rect`.
**Depict:** a **mound of suds growing in the basin** — overlapping opaque
lobes, plus 6–10 discrete round bubbles with pearl highlights riding the
top of the mound. Outlines in mid-blue/teal (`#4a4f78` family) so the mass
separates from the `#F0F4FF` paper; the delivered rings (mean RGB
242,250,242) are invisible. **Not concentric rings. Not a spinner.**
**Registration:** `fill_rect` = the basin bowl interior. Measured delivered
ink is y 146→463; the suds should start **at the water line** and grow up,
so the rect must sit on the basin, not float above it.
**100 %:** suds heaped over the rim with bubbles lifting off — and for
nursery, **clean sparkling hands**, which is the thing the beat is named
after and which appears nowhere in the template today.
**Blocked on R5-b:** `widget_basin_nursery.png` is currently the swaddled
baby, identical to `widget_pour_nursery.png`. The backdrop must be rebuilt
before this overlay can register to anything.

## R4 · `widget_charge_<career>_glow.png` — the power visibly gathering (5 files)

**Careers:** ballerina (WATCH), farmer (MUD HOP), magician (VANISH),
astronaut (LAUNCH), popstar (SOUND CHECK).
**Canvas:** 256×256 RGBA POT. **Engine:** SINGLE SPRITE scaled by fill from
108 → 234 surface px (**283 → 613 backdrop px**) at centre (512, 304), with
an added ±4 % pulse on `elapsed`.
**Depict:** the career's power accumulating **on its own subject**, diegetic
and nameable. The delivered files are a cream disc with a navy ring — the
exact shape `_draw_demo_finger` draws for the hint. That collision must not
survive.
- **ballerina** — warm stage light climbing the ribbon-dancer's trail up
  from the floor, mirror-ball motes gathering.
- **farmer** — a mud-splash crown building around the piggy's crouch;
  droplets rising, ground ring widening.
- **magician** — sparkles gathering and thickening into a shroud around
  Lamba (finned bunny-fish, species lock), converging on the canonical
  pearl-tip wand (P2-09k).
- **astronaut** — engine glow building under the rocket, bubble-plume
  widening. **Bubbles never flame.**
- **popstar** — concentric sound rings pulsing out of the canonical
  pearl/shell/coral microphone.

**Registration:** `subject_center=512,304`; the glow must be radially
composed so scaling from the centre never clips the subject.
**100 %:** handled by `widget_charge_<career>_full.png`, which is already
on disk and correct — the filled meter tube at
`meter=940..1000,90..540`. **Do not re-author it. It is a wiring bug (W1),
not an art bug.** This is the clearest case in the whole document of art
that was blamed for a code fault.

## R5 · Backdrops that depict the wrong thing (13 files)

Full 1024×608 repaints, same registration as the file they replace, all
2026-08-02 content locks binding.

| file | what is wrong | what it must be |
|---|---|---|
| `widget_charge_farmer.png` | **a strawberry, a raspberry and blueberries.** The beat is MUD HOP. | the piggy in a crouch wind-up beside the mud puddle, spring-squash pose, meter rail clear at x 940–1000 |
| `widget_basin_nursery.png` | the swaddled baby — **identical subject to `widget_pour_nursery.png`.** Two nursery beats are the same picture. | the pearl basin, water line, soap, small hands. Moonlit P3-05 palette. Must be tellable from FEED at 38 % scale. |
| `widget_pour_nursery.png` | no bottle, though the VO says "hold the warm bottle" | three babies + the warm bottle above them, bottle silhouette clear of the mover box (512, 257) |
| `widget_pour_painter.png` | a blank canvas, while the VO promises "the glowing shape" | the canvas with the sunrise shape **outlined and glowing**, ready to flood |
| `widget_push_boxer.png` | a **horizontal** gold capsule track — for a phase gated `"dir": "down"`. **The card teaches the exact gesture the code punishes.** | a **vertical** track: glove swinging overhead at the top, the duck-lane and corner stool at the bottom |
| `widget_push_nursery.png` | a horizontal track under the baby, while a down-arrow is drawn 92 px to its right and the VO says "down" | a **vertical** blanket-pull track: cribs at the top, blankets drawn downward, stars overhead |
| `widget_charge_magician.png` | the lamb sits on an **opaque teal rectangle with hard edges** — an un-cut source card — carrying an off-theme "Eggstra Cute" graphic. No wand. | Lamba under a thickening sparkle shroud, canonical pearl-tip wand at frame edge, full alpha cutout |
| `widget_track_detective.png` | a **hard-edged dark rectangle with a blurry cream smudge inside**, square corners visible on white paper. The worst asset in the delivery. | the lineup shelf of three distinct clue boxes, dim stage, the green zone as a glow floor pool under the centre box |
| `widget_track_magician.png`, `widget_lanes_magician.png` | **white chunks eaten out of the purple hat crowns and brims** — alpha matting damage on all three lane hats and the track hat | re-cut from source with clean alpha |
| `widget_crank_chef.png` | a **static whisk baked into the bowl**, and the rotating `_mover` whisk draws at the same centre — two whisks, one moving, one not | the bowl only, from above, swirl-ready |
| `widget_target_racer.png` | a full-card checkered flag, and `_mover` is **that same flag** | the finish straight in perspective; the flag becomes the small tappable thing (R7) |
| `widget_target_chef.png` | the cake-and-dishes scene, duplicated whole into `_mover` | the cake stand and topping dishes as the *receiving scene*; the cherry becomes the tappable thing (R7) |

## R6 · `widget_lanes_<career>_lit.png` — a lit state that is actually lit (10 files)

**Careers:** detective, ballerina, candymaker, doctor, farmer, boxer,
magician, painter, astronaut, popstar.
**Canvas:** 768×256 POT, three 256×256 cells, lane order left/mid/right.
**Engine:** SINGLE STRIP, one cell drawn per flash at **90 surface px =
236 backdrop px**.
**Depict:** the same lane token, unmistakably **ON** — gold rim light, the
token raised and scaled ~106 %, a sparkle burst behind it, warm bounce onto
the surface below. **Acceptance threshold: the lit cell must measure at
least +40 mean luma against the same pad in its own backdrop, and shift
hue toward gold.** Measured delivered deltas: popstar −0.9, boxer +1.1,
farmer +0.4, detective −12.2. Two of four are *darker* when on.
**Registration (binding — do not move the pads):** the delivered backdrops
paint the pads at **x 187 / 512 / 836, centre y 309, pad width ≈ 234 px**
in 1024×608 space. The engine is being corrected to those exact numbers
(W6). Register each lit cell to its own pad's centre so the correction and
the art agree.
**100 %:** n/a — lanes completion is the `_done` card (U1).

## R7 · `widget_target_<career>_mover.png` + `_mark.png` (7 + 8 files)

**Movers (7):** chef, candymaker, doctor, farmer, painter, astronaut, racer
(boxer's belt is correct as-is).
**Canvas:** 256×256 POT. **Engine:** drawn at 142 surface px =
**372 backdrop px** at `tap_point`, which roams x 205–819, y 146–462 — the
engine is tightening the y amplitude to ±0.18 h (W9).
**Depict: a single small distinct thing to hit** — never the scene. The
backdrop is the scene; the mover is the target.
- chef — **one sparkling cherry** (not the cake and dishes)
- candymaker — one wrapped candy from the canonical 7-candy roster
- doctor — **one glowing cracked bone highlight** (delivered file is an
  x-ray monitor showing a smiling starfish)
- farmer — **one snack** (delivered file is three piggies on a picnic
  blanket — a whole scene)
- painter — one glowing paint blob
- astronaut — **one sparkle-leak bubble jet** for "tap the sparkle leaks to
  patch them" (delivered file is a whole rocket). Bubbles never flame.
- racer — one zoom-strip chevron (P2-09r lock: same teal strip both states)

**Marks (8):** 128×128 POT, drawn at 76 surface px = **199 backdrop px**,
stamped permanently at each hit. **Depict the thing the child placed** —
a cherry sitting on frosting, a candy in a friend's hands, a pearl rivet
patch plate, a coral/plum/cream splat from the exact accepted stamp-set
card, a mended-bone pearl glint, a snack on the blanket, a lit zoom strip.
Every delivered `_mark` is the same generic pip: white dot, navy ring,
tinted halo. The stamps must say "**I put a cherry there**", not "something
happened".
**100 %:** the accumulated marks *are* the progress; the finished picture
is the `_done` card (U1).

## R8 · `widget_crank_<career>_progress.png` + 3 movers (9 + 3 files)

**Progress (9):** chef, ballerina, candymaker, doctor, magician, painter,
astronaut, racer, popstar.
**Canvas:** 1024×608, registered 1:1. **Engine:** SINGLE SPRITE revealed by
a **radial sweep** from −90° (the engine is switching from the uniform
alpha fade, which at 50 % shows a ghost of the finished thing and reads as
fog or a rendering fault).
**Depict: the stirred RESULT, career-specific.** chef — the batter gone
smooth and glossy with a deep swirl. doctor — the cast wrapped around the
starfish arm. candymaker — the wrapper twisted shut. ballerina — the twirl
ribbon completing its circle. magician — the star portal open. painter —
the grand circular rainbow stroke laid down. astronaut — the valve seated
and glowing. racer — the lap line crossed. popstar — the encore sparkle
circle closed. **All nine delivered files are one generic three-ring
loading-spinner glyph in career tints, pixel-identical to
`widget_target_boxer_success.png`.**
**Registration:** the result must be composed **radially about (512, 304)**
so the sweep reveals it like a clock hand, and it must register on the
backdrop's ring subject.
**Movers (3):** 256×256 POT, rotated by the engine at 140 surface px =
**366×366 backdrop px** about the sprite centre, **handle pointing UP as 0°**.
- `widget_crank_painter_mover.png` — **re-cut with transparency.** It has an
  opaque dark-navy square background today; rotating, it shows as a hard
  dark box spinning on the card. The only mover in the set with this defect.
- `widget_crank_popstar_mover.png` — a record/turntable or spotlight ring.
  Currently an **entire proscenium stage with curtains**; rotating a whole
  theatre reads as a glitch.
- `widget_crank_racer_mover.png` — the **steering wheel** (canonical
  two-tone, P2-09o). Currently a whole car spun about its centre like a
  pinwheel. `widget_crank_astronaut_mover.png` (the helm wheel) is exactly
  right — match its approach.

## R9 · gauge: a needle, three dials, three success flashes (7 files)

**`widget_gauge_shared_needle.png`** — 256×256 POT. **Depict a real
pointer**: one fat arrow tip, a weighted hub at the opposite end, clearly
asymmetric so a non-reader can tell which end points at the wedge. The
delivered file is a **symmetric orange bar with a dot at each end**.
Registration: hub at sprite-local bottom-centre, tip at top; the opaque
span must fill ≥92 % of the canvas height (delivered fills 0.03–0.95 of a
box that is itself too small, so the tip reaches only **69 %** of the
painted fan radius and never touches the arc). The engine is growing the
draw box to ~140 surface px; author for a needle that reaches the outer
edge of the green wedge.

**`widget_gauge_<career>.png` ×3** — the dial must be built **into the
career object**, not floated as an abstract fan with a sticker in the
corner. chef: the canonical pink arch-with-shell oven (P2-09a) with the
heat dial **on the oven door**, porthole showing the rising cake. astronaut:
a thrust gauge **on the rocket body** with the three pressure lamps.
racer: a tachometer **on the kart dash** with the canonical two-tone wheel
(P2-09o) at the edges and the turbo button under it. Today all three carry
the identical navy fan and green wedge — identical pixel counts, identical
measured angles — and BAKE, BOOST and TURBO are indistinguishable.
**Geometry lock:** pivot (512, 500); the painted fan must span the needle's
**full ±60°** sweep (delivered spans only −52.6°..+53.5°, so the needle
swings off the dial into blank panel at both extremes); the green wedge
baked **symmetric to the scoring window, −24.0°..+26.4°** (delivered is
−16.0°..+28.7°, which creates an 8° band where the needle sits over the
dead zone and the tap still scores — it teaches a four-year-old that green
means nothing).

**`widget_gauge_<career>_success.png` ×3** — 1024×608, registered 1:1,
now gated on `hit_flash` (W4) so it fires **when the child taps**, not when
the marker passes. The three delivered files are **byte-identical**
(`be61d2f5…`): a 5 %-alpha pale-green radial glow on an already near-white
card — invisible on a tablet in daylight. Author three distinct, high-
chroma, career-specific flashes: chef — the oven door flaring gold with
the cake risen; astronaut — the boosters lit and the pressure lamps
snapping on; racer — speed streaks and a checker flash across the dash.
**Green is reserved** — these flashes must be gold/coral/white.

## R10 · track: movers that depict the verb, and a distinct hit mark (6 files)

**`widget_track_<career>_mover.png` ×3** — 256×256 POT, drawn at **128 → 96
surface px** (the engine is shrinking it; at 128 px on a 232 px surface the
boxer glove spans y 111–194 while the painted bar spans y 138–165, so
**the mover covers essentially the whole green zone at the moment of
truth**). Author the subject to occupy ≤55 % of the canvas height so it
rides clear.
- boxer JAB — **a fist mid-jab**, not the same pair of gloves already
  painted static at the top of the backdrop
- nursery BURP — **a patting hand, or a burp bubble**, not the same
  swaddled baby already painted static
- magician CABINET — a cabinet door with a star flash (**see D4** — this
  beat may change template instead; hold this file pending that decision)

**`widget_track_shared_hit.png`** and **`widget_lanes_shared_pick.png`** —
256×256 POT each. They are **byte-identical today** (`bafd4f0e…`): one
small navy ring on a pale cream halo, doing double duty as "you hit it"
and "this is the answer", both too low-contrast on the `#e6f5ff` card.
Author two visually distinct, high-chroma marks: **hit** = a sharp white/
gold impact star, radial, brief; **pick** = a warm coral/gold selection
ring with an inward pull. Different shape, different hue, tellable apart
at 38 %.

**Track geometry is correct — do not move it.** Measured painted green
spans x 0.354–0.661, implying a zone of 0.307–0.712 against the code's
0.300–0.720. Within 0.008. It is the one calibrated thing in the delivery.

## R11 · `clue_found.png` — lens (1 file)

**Path:** `assets/opera/worlds/ui/clue_found.png`. **Canvas:** 256×256 POT,
drawn permanently at ~90 stage px at each found spot on the 1280×720 stage.
**Depict:** a pinned magnifier badge or a checked evidence tag — something
that says *this one is done* and stays said. A found clue is currently
`draw_circle(spot, 10.0, …)`: a **10-pixel dot on a 1280×720 painted
stage**, with `phase_fill` hidden because `action_panel` is hidden, so
there is no "3 of 5 found" anywhere either (W12).

---

# 5. THE THREE UNIVERSAL GAPS

Each is fixed by a small **shared** set — not per-career — so that one
batch closes the gap on every beat at once. **These 15 files are worth more
than the 78 in section 4.**

## (a) No beat has a distinct success/completion image

**Confirmed on all 87 audited beats. Not a single exception.** `pour`
ships no completion asset. `push` and `trace` have no completion slot in
the loader or on disk. 7 of 8 target `_success` files do not exist, and the
one that does is the generic ring spinner. `basin`'s success pop lives 0.18
seconds. `target`'s is unreachable by construction. The child's only
evidence of success is that the picture abruptly becomes a different
picture.

**The smallest set that fixes it everywhere: 2 files + reuse.**

| file | canvas | engine | depict |
|---|---|---|---|
| `widget_shared_done_burst.png` | 1024×608 RGBA, registered 1:1 | drawn full-frame for the 0.9 s completion hold, scaled 0.85 → 1.05 and faded out over the last 0.25 s | a full-frame celebration burst: gold and coral confetti ribbons, pearl motes, radial streaks from centre. **Centre 40 % must be transparent** so the finished thing shows through. No green. No words. |
| `widget_shared_done_ribbon.png` | 512×512 RGBA POT | stamped at card centre-bottom during the hold, popping in with an overshoot tween | a wordless gold rosette / star-ribbon "finished" stamp, pearl-centred, storybook weight. This is the token the child learns to recognise as *I did it*, identical in all 87 beats. |

**Plus zero-cost reuse:** `assets/opera/worlds/props/goal_<career>.png`
already exists for all 13 careers at 512×512 and **already depicts the
finished thing** — `goal_chef.png` is the completed three-layer cake with
cherries and cream, exactly what a chef beat should end on. The engine
draws it at ~300 surface px at card centre during the hold. **Thirteen
finished-thing images, already on disk, already gate-passed, currently used
only as a stage prop.**

So the completion moment for all 87 beats costs **2 new files**, paired
with the `_finish_phase()` hold (Table A, W3). Neither works alone: the art
without the hold renders for zero frames; the hold without the art holds a
blank.

**Then the upgrade tier:** `widget_<template>_<career>_done.png`, 1024×608,
registered 1:1, **60 files** — the beat-specific finished thing, which is
always better than a generic goal prop because it is the *same object the
child was just working on*: the bowl full and the whisk lifting; the canvas
showing a finished sunrise; the hands clean and sparkling; the rocket
actually leaving the pad; Lamba actually vanished with only sparkles left;
the cake fully topped; the herd inside the pen; the baby covered and
eyes closed; the bandage wrapped and the starfish happy. Ledger
`hold=0.9s`. This is Tier 4 in the priority order — real, but not before
the 2-file version ships and proves the hold.

## (b) No beat animates the actor doing the job

`_draw_widget_layers` has **no time term at all** for pour, basin, charge,
push, target or lanes — only gauge/track ride `timing_position` and only
crank rides `previous_angle`. And `_process` returns early when the demo
ends, so the surface stops redrawing entirely. Between gesture events the
card is a still photograph. Even with W1 and W2 fixed and R1/R2 delivered,
holding a finger on a still picture for five seconds gives a rising level
and nothing else.

**The smallest set that fixes it everywhere: 5 shared FX sprites**, all in
`assets/opera/worlds/props/` alongside the existing `fx_*` family, all
authored **neutral white/cream for per-career `modulate` tinting**, all
single sprites the engine scrolls, tiles, scales or emits.

| file | canvas | engine | depict | serves |
|---|---|---|---|---|
| `fx_widget_stream.png` | 256×512 | UV-scrolled vertically (seamless top↔bottom), emitted from the mover's declared `emit` point down to the mask cut line | a falling liquid ribbon: soft-edged column, brighter core, slight taper, **seamlessly tileable on the vertical axis** — this is what makes the pour *pour* | pour ×4, basin ×2, charge ×5 |
| `fx_widget_meniscus.png` | 512×64 | drawn at the mask cut line every frame, scaled to `fill_rect` width | a liquid-surface ellipse: bright leading highlight, soft shadow under. Solves the mask problem — a baked meniscus only reads at 100 %; this one reads at every level | every masked overlay |
| `fx_widget_splash.png` | 256×256 | popped where the stream lands, on a 0.3 s scale-and-fade | a droplet crown / impact ring, 6–8 beads | pour, basin, target hits |
| `fx_widget_effort_puff.png` | 256×256 | emitted at the trailing edge of each stroke | a soft lavender-white puff, matching `fx_dust_puff.png`'s existing weight | push ×4, crank ×9, trace ×6 |
| `fx_widget_spark.png` | 128×128 | emitted in bursts of 3–8, career-tinted, arced with gravity | a single gold mote with a soft halo | all 60, and the done burst |

With these five the engine can give **every** beat a causal link between
finger and world: the stream visibly leaves the vessel and lands in the
liquid; the level's surface catches the light as it rises; each push stroke
kicks a puff; each crank rotation throws sparks. **That is the difference
between "the number went up" and "I am pouring."**

**The honest caveat:** the *actor* is Roshan, and Roshan is never on the
card — she hops 14 px on the painted stage several hundred pixels away
(D3). A truly actor-animated card needs `roshan_<career>_work.png` ×13
(512×512, matching the existing `roshan_<career>.png` idles, arms working,
same feet-anchor and centroid locks as the imp animation handoff) drawn
small at the card's edge. **That is per-career, so it is out of the shared
set and out of the priority order** — flagged here as the known next
question, pending an owner decision. The FX kit is the shared answer.

## (c) Instruction clarity relies on a spoken line — and the line does not exist

**This is the most important finding in the document, and it is verifiable
in one command.** `assets/audio/voices/` contains 293 files. **Zero begin
with `op_`.** Every one of the 88 phases carries a `vo` key
(`op_chef_pour`, `op_chef_bake`, `op_nursery_wash`, …) and **not one of
them resolves to an audio file.** The line reaches the child through
`show_msg()` as **written English text**: *"Hold to pour the sparkling
batter!"* — to a four-year-old who cannot read.

The 2026-08-02 handoff's entire premise was "the art makes the voice line
TRUE". The voice line never plays. So on every beat in the game the
instruction channel is: a ghost finger that is **extinguished permanently
by `note_input()` on the first touch** (and during a hold cannot return,
because `idle_t` is reset every frame by the hold itself), plus a sentence
the child cannot read. That is the whole of "it is not clear what the
instructions are."

**The smallest set that fixes it everywhere: 8 shared files** in
`assets/opera/worlds/ui/`, wordless, one per input mode, drawn persistently
in the card's lower-right corner for the whole beat — **not** killed by the
first touch.

| file | canvas | depict |
|---|---|---|
| `hint_gesture_hold.png` | 256×256 | a cartoon hand, index finger pressed down, three concentric pressure rings, a small clock-sweep arc |
| `hint_gesture_tap.png` | 256×256 | the same hand, finger descending, one impact ring, two motion ticks above |
| `hint_gesture_swipe_lr.png` | 256×256 | the hand mid-drag with a horizontal trail and a chevron at the leading end |
| `hint_gesture_swipe_down.png` | 256×256 | the same, rotated to a downward trail — **a separate file, not a rotation of the LR one**, because boxer DUCK and nursery BEDTIME are the two beats whose art currently teaches the wrong axis |
| `hint_gesture_circle.png` | 256×256 | the hand tracing a circular trail with an arrowhead on the rim |
| `hint_gesture_choice.png` | 256×256 | three pads, the middle one lit, the hand descending onto it |
| `hint_gesture_timing.png` | 256×256 | a marker over a short bar with a green segment, the hand poised — **the one licensed use of green outside a go-zone**, because it is teaching what green means |
| `hint_hold_ring.png` | 256×256 | a radial-timer ring: a thick gold arc on a dim track, authored as a **full 360° ring** that the engine sweeps by `widget_fill` and re-arms if the finger lifts early |

The hand must match the ghost-finger design already drawn at
`opera_gesture_surface.gd:586` (navy `#382485` ring on a cream disc) so the
child reads corner-pictogram and on-card ghost as **the same hand**.

`hint_hold_ring.png` deserves its own line: it is the answer to *"holding a
finger down causes it to slowly rise, but there is no feedback."* A ring
that closes around the child's own finger, survives contact, and re-opens
the moment the finger lifts early, is the only cue in the design that
answers "am I still doing it right?" while the finger is down.

**And it is 8 files against 88 beats.** Nothing else in this document has
that ratio.

---

# 6. PRIORITY ORDER

Ranked by playtest improvement per asset. Tiers 1–3 are **15 files total**
and between them touch every beat in the game.

### Tier 1 — the instruction kit (8 files) — `hint_gesture_*` ×7 + `hint_hold_ring`
The only instruction channel that works for a non-reader, on a game where
**the voice lines do not exist**. Fixes CLARITY on all 88 beats. `hint_hold_ring`
alone answers the exact sentence in the playtest report. Highest ratio in
the document by an order of magnitude.

### Tier 2 — the completion kit (2 files) — `widget_shared_done_burst` + `_done_ribbon`
Fixes **COMPLETION on 87 of 87 beats** with two files, by reusing the 13
`goal_<career>.png` props already on disk as the finished thing. Ships
paired with `_finish_phase()` (W3) — **neither half works alone.** Second
because completion was the only axis on which nothing scored 4.

### Tier 3 — the motion kit (5 files) — `fx_widget_{stream,meniscus,splash,effort_puff,spark}`
Fixes "nothing moves while I act" on all 60 widget beats. `fx_widget_stream`
is the file that literally makes the bowl pour; `fx_widget_meniscus` is what
makes a masked level read as liquid at every position rather than only at
100 %.

### Tier 4 — POUR (8 files) — `widget_pour_<career>_{mover,fill}` ×4
The beat the child actually played and complained about, and the two assets
no amount of wiring can rescue: a mover that is a duplicate of its own
backdrop, and a fill that is a beige lozenge on the outside of the bowl.
Ship all 8 together — a career with a real jug and a fake fill is worse
than one with neither.

### Tier 5 — LANES `_lit` ×10
The loop currently **rewards deliberate failure** (D1) and the "on" state
is measurably darker than "off" in two of four careers. Ten files convert
the game's largest beat family from blind guessing to a fair recognition task.

### Tier 6 — TARGET movers ×7
Seven beats where the target is a copy of its own backdrop and a 142 px
duplicate is drawn on top of the painted original at phase start. Cheap,
and it is the difference between a tappable game and a double image.

### Tier 7 — the six wrong-subject backdrops
`charge_farmer` (berries for MUD HOP), `basin_nursery` (identical to FEED),
`push_boxer` and `push_nursery` (horizontal art teaching a downward
gesture — ship with W8), `pour_painter`, `pour_nursery`. Six beats where
the card is currently about the wrong thing.

### Tier 8 — CRANK `_progress` ×9 + 3 movers, GAUGE 7, TRACK 6, BASIN 2, CHARGE glows 5
The remaining "generic glyph where career art belongs" work. The crank
`_progress` set is nine copies of one loading spinner; the gauge success
set is three copies of one invisible blob.

### Tier 9 — alpha and crop re-cuts (5 files)
`crank_painter_mover` (opaque navy box), `track_detective` (raw un-matted
crop), `track_magician` + `lanes_magician` (white holes in the hat crowns),
`charge_magician` (uncut source card + off-theme graphic).

### Tier 10 — `_done` ×60
The beat-specific finished thing. Real value, but only after Tier 2 proves
the completion hold on screen. Order by career playtest frequency: chef,
detective, ballerina, candymaker first.

### Tier 11 — the clean re-export (47 backdrops) + `clue_found.png`
Mechanical: strip the dead gold badge oval at top-centre and the blank fill
pill from every backdrop that is not already being repainted. Visible at
rest on all 60 cards today and reads as unfinished art.

**Manifest total:** 15 shared (Tiers 1–3) + 78 replacements (Tiers 4–9) +
60 `_done` (Tier 10) + 47 clean re-exports (Tier 11) ≈ **200 files**, of
which the first **15** close all three universal gaps.

---

# 7. Acceptance gate — additions

The 2026-08-02 weighted gate binds unchanged (≥4.5 pass / ≥4.7 target).
Six programmatic additions for this delivery:

1. **Ink-bbox declared.** Every masked overlay ships `fill_rect` in its
   ledger row, and the measured opaque bbox must match it within 4 px.
   *(The delivered `pour` fills would fail: the declared registration is
   `crop=bottom_up;registered=1:1` with no rect, and the actual ink covers
   1.2 % of the canvas in the wrong place.)*
2. **Mask monotonicity.** Sweeping the declared axis across `fill_rect` in
   200 steps, the revealed opaque pixel count must be non-decreasing and
   must change on ≥85 % of steps. Rejects floating islands and rejects art
   that saturates early.
3. **Duplication check.** md5 and perceptual hash against (a) the asset's
   own backdrop crop and (b) every other file in the delivery. *(Would have
   caught all four `pour` movers, all three gauge `_success` files, the
   identical `track_hit`/`lanes_pick` pair, and the nine crank `_progress`
   glyphs.)*
4. **Lit-state delta.** For any `_lit` / `_success` / `_glow` state, mean
   luma against the same region of its unlit source must differ by ≥40 and
   shift hue. *(Would have caught all ten lane strips.)*
5. **Ghost-finger collision.** No mover or glow may be a cream disc with a
   navy ring at the card centre — perceptual-hash against
   `_draw_demo_finger`'s rendered output. *(Would have caught all five
   charge glows and the basin shine.)*
6. **Runtime capture mid-gesture.** The Mobile-renderer QA render must be
   taken **while the gesture is in progress** at fill 0.25 / 0.50 / 0.75,
   not at rest. A still capture cannot show whether a mover reads in
   motion or whether a level is still rising. Rest-only captures cap at
   2/5 and must not ship.

Plus the standing checks: canvas and POT conformance, semi-alpha < 15 % of
solid, no solid pixels within 2 px of a canvas edge on movers, no
words/letters/numerals, green only in gauge/track go-zones and
`hint_gesture_timing`, P2-09 canonical designs and species locks intact.

---

# 8. Delivery and scope

- Files → `assets/opera/worlds/widgets/` (widget layers),
  `assets/opera/worlds/props/` (`fx_widget_*`), `assets/opera/worlds/ui/`
  (`hint_*`, `clue_found`).
- Staging, contact sheets, PROMPTS.md, ledger rows and manifest entries per
  the 2026-08-02 protocol; one `ASSET_LICENSES.md` row per accepted asset
  **in the same commit**; one controlled promotion commit.
- **Ledger rows must carry the new registration fields** (`fill_rect`,
  `anchor`/`pivot`/`sway`, `emit`, `hold`). The engine mapping is data, not
  guesswork — that rule is why W2 is a one-line fix instead of a rewrite.
- **The engine work in Table A ships in the same workstream** (P7
  no-orphans). Specifically, Tier 2 art is inert without `_finish_phase()`
  (W3), Tier 3 is inert without a time term in `_draw_widget_layers` and a
  redraw that survives demo-end (U2/W15), and R4's companion `_full` files
  need only W1 — no art at all.
- Never touch `assets/book/`, `assets/audio/voices/`,
  `assets/characters/friends/`, and never regenerate Roshan.

## Out of scope — do not start without an owner decision

- **`roshan_<career>_work.png` ×13.** The actor-on-the-card question
  (section 5b). Per-career, and it interacts with the stage layout.
- **magician CABINET, detective NAME, nursery BURP** (D4). The template
  cannot carry the fiction; these should change template rather than get
  new art. `widget_track_magician_mover.png` is held pending that call.
- **bop (26 phases).** Already the best-served beat in the game
  (FEEDBACK 5) and already covered by
  `CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md`. Its only gaps are wiring
  (W12: no progress indicator; the last imp's 0.62 s fade cut off
  mid-flight).
- **`op_*` voice recordings.** 88 lines. Out of scope for image
  generation, but this document's central finding is that they do not
  exist, and the Tier 1 pictogram kit is explicitly the mitigation rather
  than the fix. Someone should decide whether the lines get recorded.

---

**Files referenced (absolute):**
`C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md`,
`.../CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md`,
`.../OPERA_WIDGET_INPUT_AUDIT_2026-08-02.md`,
`.../scripts/opera_gesture_surface.gd`,
`.../scripts/opera_career_world_2d.gd`,
`.../scripts/opera_nursery_catch.gd`,
`.../scripts/audio_director.gd`,
`.../assets/opera/worlds/widgets/` (154 PNGs),
`.../assets/opera/worlds/props/goal_<career>.png` (13),
`.../assets/opera/worlds/actors/roshan_<career>.png` (13),
`.../assets/audio/voices/` (293 files, zero `op_*`),
`.../assets_src/concepts/opera_regeneration_2026-08-01/OPERA_CODEX_MANIFEST_2026-08-02.json`,
`.../assets_src/concepts/opera_regeneration_2026-08-01/OPERA_WIDGET_LEDGER_2026-08-02.csv`.