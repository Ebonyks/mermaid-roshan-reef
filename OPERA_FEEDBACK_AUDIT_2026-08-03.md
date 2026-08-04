# Per-game feedback audit — 2026-08-03

Triggered by the human playtest: the bowl never pours, no feedback that holding works.



---

## AUDIT: hold-and-fill

6# AUDIT — pour / basin / charge (11 beats)

Verified against `scripts/opera_gesture_surface.gd`, `scripts/opera_career_world_2d.gd`, the 32 delivered PNGs for these three templates, and `assets_src/concepts/opera_regeneration_2026-08-01/OPERA_CODEX_MANIFEST_2026-08-02.json`. I opened 11 of the PNGs and rendered pixel-accurate simulations of the card at fill = 0.0 / 0.25 / 0.5 / 0.75 / 1.0 by re-implementing `_draw_widget_layers` in PIL, so every claim below about "what the child sees" is measured, not inferred.

**Headline: the `set_fill` fix was necessary but not sufficient. The same bug still exists in `charge` (the meter art is never filled), and the reveal geometry is wrong for `pour` and `basin` so the fill visibly saturates less than half way through the hold. On top of that, most of the delivered art depicts the wrong thing — every `pour` "mover" is a duplicate crop of its own backdrop, and every `pour` "fill" is a translucent rounded rectangle rather than liquid.**

---

## THE ROWS

| Beat | template | goal | CLARITY | FEEDBACK | COMPLETION |
|---|---|---|---|---|---|
| chef **POUR** | pour_chef | 5.0s | **2** | **2** | **1** |
| candymaker **SYRUP** | pour_candymaker | 4.5s | **2** | **2** | **1** |
| painter **FILL** | pour_painter | 4.5s | **1** | **1** | **1** |
| nursery **FEED** | pour_nursery | 4.2s | **1** | **1** | **1** |
| doctor **WASH** | basin_doctor | 4.5s | **3** | **2** | **2** |
| nursery **WASH HANDS** | basin_nursery | 3.6s | **1** | **2** | **2** |
| ballerina **WATCH** | charge_ballerina | 4.0s | **2** | **2** | **2** |
| farmer **MUD HOP** | charge_farmer | 4.0s | **1** | **2** | **2** |
| magician **VANISH** | charge_magician | 4.2s | **2** | **2** | **1** |
| astronaut **LAUNCH** | charge_astronaut | 5.0s | **3** | **2** | **1** |
| popstar **SOUND CHECK** | charge_popstar | 4.5s | **3** | **2** | **2** |

Nothing scores 4. Diagnoses follow, most severe first.

---

## WIRING — art exists, the engine never drives it

### W1. The charge meter is never filled — the exact same bug as `set_fill`, still live in 5 beats
`opera_gesture_surface.gd:466-470`:
```gdscript
"charge":
    if widget_mover != null:
        _draw_widget_sprite(widget_mover, center, 108.0 + widget_fill * 126.0)
    if widget_overlay != null and widget_fill > 0.82:
        draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false, Color(1.0, 1.0, 1.0, widget_fill))
```
`widget_overlay` here is `widget_charge_<career>_full.png`. I opened it: it is **the filled meter tube**, a 61×451 teal/amber capsule at x 940–1001, y 90–541, registered pixel-exactly over the *empty* dark tube painted into the backdrop. The manifest says so explicitly — `"asset_id": "widget_charge_ballerina_full", "registration": "meter=940..1000,90..540"`. It is a meter. The engine never fills it; it fades the whole tube in, at once, during the last 18% of the hold.

Measured dead time with an empty meter on screen: ballerina 3.28s, farmer 3.28s, magician 3.44s, astronaut 4.10s, popstar 3.69s. My simulation of `charge_ballerina` at fill 0.00 / 0.30 / 0.60 shows a byte-identical dark tube in all three.

Missing call: `_draw_progress_overlay(widget_overlay, widget_fill, false)` — but clipped to the declared meter rect, not the card. A whole-card bottom-up wipe would still leave the tube dead until fill 0.11 and full at 0.89. Correct: reveal the band `y ∈ [90 + (1-fill)*451, 541]` of the source, drawn to the matching destination band.

### W2. `_draw_progress_overlay` maps the reveal to the CARD, not to the ink — pour saturates at 43%
`opera_gesture_surface.gd:417-431`:
```gdscript
var source_y := texture_size.y * (1.0 - amount)
var destination_y := size.y * (1.0 - amount)
```
The reveal edge sweeps the full 608px canvas, but every overlay's ink occupies only a band of it:

- **pour `_fill`** ink = y 345→553 (all four careers, identical geometry). Ink starts appearing at fill **0.09** and is **completely drawn at fill 0.43**. My simulation frames at fill 0.43, 0.70 and 1.00 are pixel-identical. Chef POUR: the picture stops changing at t=2.16s of a 5.0s hold and then sits frozen for **2.84 seconds** while the child keeps holding. That is verbatim the playtest complaint, still true after the `set_fill` fix.
- **basin `_bubbles`** ink = y 146→463. Nothing happens for the first 24% of the hold (doctor WASH: 1.07s of blank), motion from 0.24→0.76, then frozen again.

The manifest registers these as `"registration": "crop=bottom_up;registered=1:1"`, so honoring the ink bounds is the engine's job. Fix: give `_draw_progress_overlay` the overlay's opaque bbox (precomputed per template, or a `fill_rect` field on the widget set) and lerp the reveal edge across *that* rect.

### W3. The completion state is destroyed on the frame it appears
`opera_career_world_2d.gd:1069-1071` advances the instant `phase_progress >= goal`, and `_show_phase()` immediately re-configures the surface and calls `surface.set_fill(0.0)` (lines 702-703 and again 726). So `basin`'s success pop —
```gdscript
if widget_fill >= 0.96:
    _draw_widget_sprite(widget_shared, center, 118.0)
```
(`opera_gesture_surface.gd:464-465`) — is on screen for `(1.0 - 0.96) * goal` = **0.18s** at doctor WASH, **0.14s** at nursery WASH HANDS. Roughly 9 frames.

And there is **no per-phase celebration anywhere in the world script**. `confetti` is built only inside `celebrate()` (`opera_career_world_2d.gd:~1231`), which runs once at the end of the entire career. No burst, no sting, no sound, no held "done" frame on any of these 11 beats. The `pour` template does not even have a completion asset to draw — the delivered set is backdrop / `_fill` / `_mover` only.

Missing call: a `_finish_phase()` that pins `widget_fill = 1.0`, fires a burst (`_bop_burst_at` already exists and is reusable), waits ~0.9s, *then* increments `phase_index`.

### W4. Roshan's bounce spawns a fresh tween 60×/second during every hold
`opera_career_world_2d.gd:1679-1680` calls `_on_gesture("hold", delta, 1.0)` every frame while held, and `_on_gesture:1050` unconditionally calls `_bounce_actor(player_actor, ...)`, which does `var home_y := actor.position.y` then `actor.create_tween()`. Each new tween captures a *mid-bounce* y as "home" and none of the old ones are killed — hundreds of tweens fighting over `position:y` across a 5-second hold. The one on-stage reaction to holding is therefore a jitter/drift, not a bounce. The applause is already rate-limited by `score_cool` at line 1034-1039; the bounce needs the same gate.

### W5. Holding through a phase boundary earns nothing for a full second, silently
`_show_phase()` sets `phase_gap = 1.0` (lines 661/663), and `_process:1679` requires `phase_gap <= 0.0` before crediting a hold. The skip in `_on_gesture:1021-1024` only fires on a *new* gesture event — a finger that is already down generates none, so it cannot skip its own gap. The child holds; the new widget sits at fill 0; nothing happens for 1.0s. Fix: `if mode == "hold" and surface.held: phase_gap = 0.0`.

### W6. `surface.set_fill(progress)` is duplicated back-to-back
`opera_career_world_2d.gd:1048-1049` and again `1127-1128`. Harmless, but it is the fingerprint of a double-applied patch and should be cleaned up.

### W7. On any widget-backed beat, the hold affordance is never drawn
`opera_gesture_surface.gd:349-354` early-returns the whole `match mode:` block whenever `widget_backdrop != null`. So the hold ring and the growing white dot (lines 368-371: `draw_circle(center, 24.0 if held else 16.0, Color.WHITE)`) — the only element in the file that visibly responds to `held` — never render on these 11 beats. The sole "press here" cue is the ghost dot, and it is killed permanently by `note_input()` (`_on_gesture:1030`) on the first touch.

---

## ART — the asset does not exist or depicts the wrong thing

### A1. Every `pour` `_mover` is a 256px crop of its own backdrop
Manifest, verbatim: `"asset_id": "widget_pour_chef_mover", ..., "source": "widget_pour_chef.png"`. Confirmed by opening them:
- `widget_pour_chef_mover.png` — **the same mixing bowl and whisk again**
- `widget_pour_painter_mover.png` — the same easel again
- `widget_pour_nursery_mover.png` — the same swaddled baby again
- `widget_pour_candymaker_mover.png` — the same candy and molds again

The code draws it only while held, at `center - Vector2(0, 18)`, 138px (`opera_gesture_surface.gd:456-458`). My chef simulation shows the literal result: **two overlapping bowls**, which reads as a rendering error, not as pouring. There is no jug, no stream, no hand, anywhere in the template.

Each must show a tilted vessel with a visible stream leaving it and landing in the target: chef = a jug tipped over the bowl with batter falling; candymaker = a syrup bottle with a ribbon of syrup into the molds; painter = a loaded brush or paint cup running onto the canvas; nursery = a milk bottle tipped to the baby's mouth. 3-4 stream frames, or a single mover the code sways (see D1).

### A2. Every `pour` `_fill` is a translucent rounded rectangle, not liquid
`widget_pour_chef_fill.png` is a 325×208 semi-transparent pale-yellow **pill** at (350,345)-(675,553) — only 1.2% of the canvas is opaque. It lands on the bowl's **outer front wall, below the rim**; the bowl's interior ellipse is up at roughly y 230-350. So the chef's "batter" is a beige lozenge fading up over the *outside* of the bowl.
- `widget_pour_painter_fill.png` — the same pill, on the easel's **ledge**. The canvas, the one surface that must fill, never changes. The VO says "Hold to fill the glowing shape!"
- `widget_pour_nursery_fill.png` — the same pill, on the baby's swaddle.
- `widget_pour_candymaker_fill.png` — the same pill, mint-tinted.

Each must be the liquid at full level, opaque, painted to the exact silhouette of the container's interior with a meniscus/highlight — and painted across the full vertical sweep the reveal uses, so the level rises for the whole hold.

### A3. `widget_basin_*_bubbles.png` are not bubbles
They are three near-white broken concentric **rings** (mean RGB 242,250,242) at (354,146)-(671,463) — a loading-spinner shape. Against the card's near-white `#F0F4FF` paper they have almost no contrast; in my simulation they read as fog wiping across the sink and washing it out. Must show a mound of suds growing in the basin plus discrete bubbles, in a value that separates from white paper (mid-blue/teal outlines).

### A4. The charge "glow" and the basin "shine" are the same generic dot — and it is the ghost-finger demo
All five `widget_charge_<career>_glow.png` and `widget_basin_shared_shine.png` share identical geometry (256×256, bbox 16-241, 60.6% non-zero alpha, 3.4% opaque, mean RGB 166,154,183): **a cream disc with a navy ring inside a faint halo**. That is pixel-for-pixel the design `_draw_demo_finger` paints for the hint (`opera_gesture_surface.gd:586-587`: `draw_circle(at, 14.5, Color("#382485"))` then `draw_circle(at, 12.0, cream)`), at the same center point. So "you are charging" and "put your finger here" are the same picture, stacked. Neither is diegetic — nothing about a cream dot says ballet, mud, magic, rocket or microphone.

Replace per career with the career's power visibly accumulating: light climbing the ballerina, a mud splash building, sparkles gathering on the wand, engine flame growing, sound rings pulsing out of the mic.

### A5. Wrong subject entirely
- **`widget_charge_farmer.png` depicts a strawberry, a raspberry and blueberries.** The beat is MUD HOP — "Hold to wind up... and make a big mud hop!" There is no mud, no puddle, no hop, no Roshan.
- **`widget_basin_nursery.png` depicts the swaddled baby** (the same subject as `widget_pour_nursery.png`) with a thin peach arc behind it. The beat is WASH HANDS — "Hold the bubbly basin to wash your hands first!" No basin, no water, no hands, no soap. Worse: **WASH HANDS and FEED are the same picture**, so two nursery beats are indistinguishable.
- **`widget_pour_painter.png` is a blank canvas** while the VO promises a glowing shape to fill.
- **`widget_pour_nursery.png` contains no bottle** while the VO says "Hold the warm bottle".

### A6. `widget_charge_magician.png` has an uncut source card baked in
The lamb sits on an opaque **teal rectangle with hard edges** — an un-cut-out card pasted onto the paper — and carries an off-theme "Eggstra Cute" easter-egg graphic on its belly. No wand, despite "Hold the wand to make Lamba vanish!"

### A7. Dead placeholder shapes in every backdrop
Every one of these 32 backdrops carries an **empty badge oval** at top-center (~(455,25)-(575,90)) that no code path ever draws into, plus the blank pill marking the fill zone. Both are visible at rest and read as unfinished art. `widget_charge_ballerina.png` additionally has a clipped stray element cut off at the bottom edge (a thin rule and a half-sphere), and `widget_basin_doctor.png` has white cutout fringing down the left of the purple pedestal.

---

## DESIGN — neither wiring nor art would fix it

### D1. Nothing in a widget beat moves unless `widget_fill` changes
`_draw_widget_layers` has no time term at all for `pour`, `basin` or `charge` — compare `gauge`/`track`, which at least ride `timing_position`. And the surface stops redrawing entirely once the demo ends (`_process:177`, `if not demo_active: return`). So between gesture events the card is a still photograph. Even with W1/W2 and A1/A2 fixed, holding a finger on a still picture for 4-5 seconds gives a 4-year-old a rising level and nothing else. Cheapest honest fix: drive a wobble off `elapsed` — tilt the pour mover ±8° and bob it, jitter the suds, pulse the charge glow — plus a particle stream running from the mover into the fill zone so the *causal link* between finger and level is visible.

### D2. "Hold" is never taught, and the hint dies on contact
`_draw_demo_finger` gives hold `pressing = true` at the card center; every other mode gets a 2.4s press/release cycle at the same center. A tap hint and a hold hint are near-identical, and `note_input()` extinguishes it on the first touch (it only returns after 9s idle, via `_process:1668-1670` — and `idle_t` is reset every frame *by the hold itself*, so during a hold it never returns). A non-reader needs a hold cue that **survives touching**: a ring around the finger that closes as the hold progresses (a radial timer on `widget_fill`), reappearing the instant the finger lifts before the goal.

### D3. Completion is invisible by construction
No burst, no sound, no held "done" frame on any beat in scope, and the `pour` template ships no completion asset at all. The child's only evidence of success is that the picture abruptly becomes a different picture. Every beat needs a terminal image the child can name — the bowl full and the whisk lifting, the canvas showing a finished painting, the hands clean and sparkling, the rocket actually leaving, the lamb actually vanishing — held for ~0.9s with a burst and a chime.

### D4. Progress lives in two places that disagree
The diegetic art (frozen for most of the hold) and `phase_fill`, a bare default-themed `ProgressBar` (`opera_career_world_2d.gd:446-451` — no StyleBox, `show_percentage = false`) sitting under the card. The `ProgressBar` is currently the **only** element that moves smoothly for the entire hold, and it is the least legible, least diegetic thing on the screen for a non-reader. Either restyle it as a large diegetic meter or delete it and make the art carry the load.

---

## THE TWO CHANGES THAT BUY THE MOST

1. **W1 + W2** — fill `widget_charge_*_full.png` progressively within its declared `meter=940..1000,90..540` rect, and map `_draw_progress_overlay` to each overlay's ink bbox instead of the card. That alone converts 11 beats from "frozen for 57-82% of the hold" to "moves the whole way", using only art already on disk.
2. **A1 + A2** — the `pour` movers and fills are the assets that make the bowl a bowl being poured into. As delivered they are a duplicate bowl and a beige lozenge; no amount of wiring rescues them.


---

## AUDIT: timing-and-choice

# Opera widget audit — gauge / track / lanes (21 beats)

**Headline: the `set_fill` bug is not the only one of its kind, and for my 21 beats it is not even the relevant one.** None of the gauge, track, or lanes draw branches read `widget_fill` at all, so the `set_fill` fix changes nothing for any of these 21 beats. What I found instead is the *same failure class* three more times — delivered art that the engine draws on the wrong trigger, at the wrong coordinates, or that depicts no state change — plus one structural hole that explains the playtester's exact words ("no feedback or animation demonstrating that the game is being successfully completed") for every beat in the game, not just POUR.

The three biggest are:

1. **No timing beat responds to a tap.** All 11 gauge/track beats gate their "success" art on `timing_position` (where the marker is), never on input. A correct tap changes *nothing* on the widget.
2. **A correct lane pick draws nothing; a wrong pick lights up the answer.** The feedback is exactly inverted, and the child's optimal strategy is to tap wrong on purpose.
3. **There is no completion moment anywhere in the phase loop.** `phase_progress >= goal` silently increments the index and swaps the widget. The `phase_gap` "sparkle sting" the code comments promise is never drawn.

---

## Per-beat scores

### gauge — 3 beats (chef BAKE, astronaut BOOST, racer TURBO)

| Beat | CLARITY | FEEDBACK | COMPLETION |
|---|---|---|---|
| chef BAKE | 2 | 1 | 1 |
| astronaut BOOST | 2 | 1 | 1 |
| racer TURBO | 2 | 1 | 1 |

All three share one backdrop design; only the corner prop and the lamp colour differ. `widget_gauge_{chef,astronaut,racer}_success.png` are **byte-identical** (md5 `be61d2f54a93b5e11d8cf962ee1b63e9`).

### track — 8 beats

| Beat | CLARITY | FEEDBACK | COMPLETION |
|---|---|---|---|
| boxer JAB | 3 | 1 | 1 |
| ballerina DUET | 3 | 1 | 1 |
| candymaker PARADE | 3 | 1 | 1 |
| farmer FEED | 3 | 1 | 1 |
| popstar RHYTHM | 3 | 1 | 1 |
| magician CABINET | 2 | 1 | 1 |
| nursery BURP | 2 | 1 | 1 |
| detective NAME | 1 | 1 | 1 |

Track earns its 3s honestly: its geometry is **correctly calibrated** (see W4). It loses points on the mover covering the green zone and on the prop duplication.

### lanes — 10 choice beats

| Beat | CLARITY | FEEDBACK | COMPLETION |
|---|---|---|---|
| detective MATCH (goal 5) | 2 | 1 | 1 |
| ballerina STEPS (goal 7) | 2 | 1 | 1 |
| candymaker SORT (goal 7) | 2 | 1 | 1 |
| doctor FIND (goal 6) | 2 | 1 | 1 |
| farmer PLANT (goal 6) | 2 | 1 | 1 |
| boxer ROUND (goal 8) | 2 | 1 | 1 |
| magician TRACK (goal 6) | 2 | 1 | 1 |
| astronaut PIPES (goal 6) | 2 | 1 | 1 |
| popstar DANCE (goal 8) | 2 | 1 | 1 |
| painter REVEAL (goal 1) | 4 | 1 | 1 |

painter REVEAL scores 4 on clarity only because `goal: 1.0` means one pick ends it — the ghost finger walks to the answer and it's over before the mechanic can fail.

---

## WIRING — art exists, the engine never drives it (or drives it wrong)

**W1 — No timing beat has any tap feedback. There is no hit state at all.**
`opera_gesture_surface.gd:449` (gauge) and `:454` (track):
```gdscript
if widget_overlay != null and timing_position >= timing_zone.x and timing_position <= timing_zone.y:
    draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
```
Both are gated on **where the marker is**, not on whether the child tapped. `widget_gauge_*_success.png` and `widget_track_shared_hit.png` are therefore continuous "you may tap now" hints that blink on and off as the marker sweeps, whether or not anyone touches the tablet. `_press()` (`:233-237`) emits the gesture and sets no state; the surface has no `hit_flash` variable and `_on_gesture` never calls back into the surface for timing modes. **Fix:** add `var hit_flash := 0.0`, set it in `_press` when the tap lands in the zone, decay it in `_process`, and gate the `_success`/`_hit` layer on `hit_flash > 0.0` instead of on `timing_position`. Right now the entire delivered success layer is wired to the wrong signal — this is the set_fill bug with the wire attached to the wrong terminal instead of unattached.

**W2 — A correct lane pick draws nothing.**
`opera_career_world_2d.gd:1051-1060`:
```gdscript
if mode == "choice":
    if quality >= 0.5:
        choice_target = (choice_target + 1 + (phase_index % 2)) % 3
        surface.target_choice = choice_target
        surface.queue_redraw()
    else:
        surface.reflash_choice()
```
`queue_redraw()` on the correct branch is a no-op visually, because `opera_gesture_surface.gd:492` reads
```gdscript
var show_answer := choice_flash > 0.0 or demo_active
```
and `choice_flash` is 0 by then (`configure()` sets 1.4 once at phase start; nothing re-arms it on success). So the lanes branch draws **zero pixels** and the backdrop redraws identically. Meanwhile the *wrong* branch calls `reflash_choice()` → `choice_flash = 1.2` → the answer lights up. Getting it right is silent; getting it wrong is the light show. **Fix:** the correct branch needs its own response (a `pick_flash` timer drawing a burst on the picked lane), and `choice_flash` must be re-armed for the newly-rotated target.

**W3 — The lanes "lit" overlay is drawn 44px below the pad it highlights, and 38% oversized.**
`opera_gesture_surface.gd:494-497`:
```gdscript
var lane_point := Vector2(size.x * (float(target_choice) + 0.5) / float(choice_count), size.y * 0.70)
...
draw_texture_rect_region(widget_mover, Rect2(lane_point - Vector2(62.0, 62.0), Vector2(124.0, 124.0)), source)
```
Measured painted pad centres across popstar/magician/boxer/farmer: **x = 0.183 / 0.500 / 0.816, y = 0.509**, pad width **0.229w**. Code uses x = 0.167/0.500/0.833 and **y = 0.700**. On the 392×232 surface set by `_apply_panel_layout` that is **44px too low** — the 124px overlay spans y 100..224 while the pad spans y ~69..167, so the highlight hangs off the bottom of the pad into the card's lower border. Width 124px vs a 90px pad. **Fix:** `size.y * 0.509`, lane fractions `0.183/0.500/0.816`, draw box `90.0`.

**W4 — `timing_zone` is never assigned by the driver, and the gauge art disagrees with the default.**
`grep -rn "timing_zone"` returns **zero writes** outside `opera_gesture_surface.gd:17` — every timing beat in all 13 careers runs the hardcoded `Vector2(0.30, 0.72)`.

Track is fine: measured painted green spans x 0.354..0.661 in every track backdrop, which under the code's own `lerpf(size.x * 0.12, size.x * 0.88, timing_position)` implies a zone of **0.307..0.712** vs the code's 0.300..0.720. Within 0.008 — correctly calibrated.

Gauge is not. Measured about the code's own pivot `(0.50, 0.82)`:
- painted green wedge: **−16.0° .. +28.7°** (identical in all three files; asymmetric, skewed right)
- code scoring window: `deg_to_rad(lerpf(-60.0, 60.0, timing_position))` over 0.30..0.72 → **−24.0° .. +26.4°**

Two lie-bands:
- **−24.0° to −16.0°** (8°, 6.7% of the whole sweep): needle sits over the **dark dead zone** and the tap **scores**, and the success glow fires.
- **+26.4° to +28.7°**: needle sits **on the green** and the tap **misses**.

The first band is the damaging one — it teaches a 4-year-old that the green wedge means nothing. **Fix:** set `timing_zone = Vector2(0.367, 0.739)` for the gauge template (or repaint the wedge symmetric to 0.30..0.72).

Two more gauge geometry errors from the same measurement pass:
- The painted fan spans **−52.6° .. +53.5°**; the needle sweeps **−60° .. +60°**, so at both extremes the needle **swings off the dial** into blank white panel.
- The needle's visible length is **81px** against a painted fan radius of **117px** on the surface — the tip reaches only **69%** of the dial and never touches the arc or the outer edge of the green wedge.

**W5 — `widget_fill` is dead for all 21 beats.** `_draw_widget_layers` (`:440-497`) reads `widget_fill` only in the `pour`/`basin`/`charge`/`crank`/`trace`/`push`/`target` branches. `gauge`, `track` and `lanes` never touch it. The `set_fill(progress)` calls added at `opera_career_world_2d.gd:1048` have no effect here. If these templates are meant to show accumulating work (they should — see D1), they need a progress layer of their own.

**W6 — The nursery BURP diegetic scene is unreachable dead code.** `opera_gesture_surface.gd:508-554` `_draw_nursery_context()` has a `"nursery_burp"` branch that draws the baby, a patting hand, and the timing bar. It can never run: `opera_career_world_2d.gd:701` always builds `var context := "%s_%s" % [template, career_id]`, so BURP's context is `"track_nursery"`, and `_draw()` early-returns at `:354` the moment `widget_backdrop != null`. All four `nursery_*` branches are dead. Relatedly `configure()` (`:82-87`) loads `baby_0/1/2.png` on every nursery widget phase and nothing ever uses them.

**W7 — The gauge ghost-finger teaches the wrong gesture.** `_draw_demo_finger()` `:572-575` places the demo dot at `Vector2(lerpf(size.x * 0.12, size.x * 0.88, timing_position), center.y + 58)` — a **horizontal slide** — for `mode == "timing"`. On track that's correct and lands ~21px under the marker. On gauge the marker is a **rotating needle** and the demo dot slides across the middle of the dial, actively demonstrating a swipe on a rotary control.

**W8 — cosmetic sloppiness from the fill fix.** `surface.set_fill(progress)` is duplicated on consecutive lines at `:1048-1049` and `:1127-1128`; `surface.set_fill(0.0)` is duplicated at `:703` and `:726`.

---

## ART — the asset does not exist, or depicts the wrong thing

**A1 — `widget_gauge_{chef,astronaut,racer}_success.png` is one invisible blob, shipped three times.** All three are byte-identical (`be61d2f5…`): a ~5%-alpha pale-green radial glow, drawn full-panel over an already near-white `#e6f5ff` card. On a tablet in daylight this is nothing. **Needs:** three distinct, career-specific success cards — chef: the cake risen and golden through the open oven door; astronaut: the boosters flaring; racer: the shell-car with speed streaks and a checker flash.

**A2 — `widget_gauge_shared_needle.png` is not a needle.** It is a symmetric orange bar with a dot at each end — there is no tip, so a non-reader cannot tell which end points at the wedge. **Needs:** a real pointer with one fat arrow tip and a hub at the pivot end, drawn long enough to reach the painted arc (117px on-surface, i.e. the sprite's opaque span must fill the `Rect2(-48,-84,96,96)` box rather than 0.03..0.95 of it, and the box should grow to ~140px).

**A3 — the three gauge backdrops are the same abstract dial with a sticker in the corner.** `widget_gauge_chef.png`, `_astronaut.png`, `_racer.png` all carry the identical navy fan + green wedge (identical pixel counts, identical measured angles); only a small inert prop in the upper-left and the lamp colour change. The racer's prop is a pearl-domed disc that reads as neither car nor speedometer. BAKE, BOOST and TURBO are visually indistinguishable to the child. **Needs:** the dial built *into* the career object — an oven door with a heat dial on it, a thrust gauge on the rocket body, a tachometer on the car dash.

**A4 — `widget_track_shared_hit.png` and `widget_lanes_shared_pick.png` are byte-identical** (md5 `bafd4f0ebefbde0cb5cde7f9b92f9c99`): one small navy ring on a pale cream halo, doing double duty as "you hit it" and "this is the answer". It is far too low-contrast on the `#e6f5ff` card, and on track it is drawn at 82px *on top of* the 128px mover, so it lands on a mid-tone glove. **Needs:** two separate, high-chroma marks.

**A5 — the `_lit` lane atlases are not lit.** Measured mean luma of a lit cell vs the same pad in its own backdrop:

| career | backdrop pad | lit cell | delta |
|---|---|---|---|
| popstar | 136.7 | 135.8 | **−0.9** |
| boxer | 133.7 | 134.9 | **+1.1** |
| farmer | 145.7 | 146.2 | **+0.4** |
| detective | 134.8 | 122.6 | **−12.2** |

The lit cell is the *same pad art* plus a barely-visible pale halo — in two of four cases it is darker than the unlit pad. This matters more than it looks: `_draw()`'s early return at `opera_gesture_surface.gd:354` skips the fallback `match mode:` block, whose `"choice"` branch drew a strong gold ring and white core (`Color(1.0, 0.86, 0.32)`, `:394-398`). Shipping the lanes art **silently deleted a working gold flash and replaced it with nothing visible** — the same regression shape as the set_fill bug. **Needs:** an unmistakable ON state per cell — gold rim, raised value, sparkle burst; at least +40 luma and a distinct hue from the unlit pad.

**A6 — `widget_track_detective.png` ships a raw un-matted crop.** The static prop is a **hard-edged dark rectangle with a blurry cream smudge inside it**, square corners plainly visible against the white panel. For a beat whose line is "Tap when the spotlight shines on the answer!" the child sees a grey box. This is the single worst asset in my set and the reason detective NAME scores CLARITY 1.

**A7 — `widget_lanes_magician.png` and `widget_track_magician.png` have alpha-matting damage.** White chunks are eaten out of the purple hat crowns and brims on all three lane hats and on the track hat. Re-cut from source.

**A8 — the track movers duplicate the static backdrop prop.** `widget_track_boxer_mover.png` is the same pair of gloves already painted static at the top of `widget_track_boxer.png`; `widget_track_nursery_mover.png` is the same swaddled baby already painted static in `widget_track_nursery.png`. So the child sees **two identical objects**, one inert and one sliding, and nothing depicts the verb — the gloves never punch, the baby is never patted or burped. **Needs:** the mover should be the *acting* object and visually distinct from the static prop — a fist mid-jab for JAB, a patting hand (or a burp bubble) for BURP, a cabinet door with a star flash for CABINET.

**A9 — the track mover physically hides the answer.** `_draw_widget_sprite(widget_mover, run_point, 128.0)` (`:453`) puts a 128px sprite on a 232px-tall surface. The boxer glove's opaque span is 0.05..0.95 × 0.17..0.82 of its canvas → 115×83px on-surface, spanning y 111..194. The painted bar spans y ~138..165 (27px tall) and the green zone is 120px wide. **When the marker is centred in the green, the mover covers essentially the whole green zone** — exactly at the moment of truth. Either shrink the mover to ~72px or move it to ride *above* the bar rather than on it.

**A10 — no completion asset exists for any of these 21 beats.** There is no `widget_gauge_*_done`, no `widget_track_*_done`, no lanes finished state. Every COMPLETION score of 1 is partly this.

---

## DESIGN — neither wiring nor art; the beat itself doesn't communicate

**D1 — There is no completion moment in the entire phase loop.** `opera_career_world_2d.gd:1069-1071`:
```gdscript
if phase_progress >= goal:
    phase_index += 1
    _show_phase()
```
No burst, no tween, no sound, no "finished thing". `_show_phase` sets `phase_gap = 1.0` (`:661`, `:663`) and `_on_gesture:1021-1024` calls it *"the between-phase sparkle sting"* — **but nothing anywhere draws for `phase_gap`.** It is one second of dead input during which the widget has already been replaced. The child's last correct tap is answered by the puzzle vanishing. This is the general form of the playtester's complaint and it affects all 21 beats plus every other beat in the game. **Fix:** hold the finished widget on screen for the gap, swap it to a `_done` card, fire a burst (the `_bop_burst_at` confetti at `:1097-1109` already exists and could be reused), and let the gap be the celebration it claims to be.

**D2 — `phase_fill` is an unstyled default `ProgressBar` and it is the only accumulating signal these 21 beats have.** `opera_career_world_2d.gd:446-451` creates `ProgressBar.new()` with no theme override, sitting on a `#e6f5ff` card — Godot's default grey-on-grey. A non-reader will not connect a UI bar to "the cake is getting made". Style it in the StorybookUI language, or better, give gauge/track/lanes a diegetic fill layer (this is where a real `widget_fill` hookup would pay off — see W5).

**D3 — lanes degenerates into blind 1-in-3 guessing, and rewards deliberate failure.** `choice_target` rotates on every correct pick (`:1054`) and is never re-shown, so after the first pick the answer is invisible. The only way to see it is `reflash_choice()`, which fires **only on a wrong pick**. The learned strategy for a 4-year-old is: tap any lane, wait for the mercy flash, tap the flashed lane. With boxer ROUND and popstar DANCE at `goal: 8.0` (+1.0 per correct pick) that is ~8 blind guesses per beat and roughly 16 taps. The stated intent — *"the pick uses recognition memory instead of tap-the-highlight"* (`:37-38`) — is not achievable when the thing to be recognised moves in secret. **Fix:** either stop rotating the target within a phase, or re-flash briefly on the new target after each correct pick so the memory task is fair.

**D4 — `competition.note_success()` does nothing before the finale.** `opera_competition.gd:183-185`:
```gdscript
func note_success(points: int = 12) -> void:
    if active:
        player_score += maxi(points, 0)
```
`competition.begin()` is only called at `_finale_start()` (`:653-654`), which is phase 4 or 5. So for every pre-finale beat — including chef BAKE, astronaut BOOST, all the lanes beats, and most track beats — a correct action increments nothing at all. Combined with W1/W2, the complete response to a correct action on a pre-finale gauge/track/lanes beat is: `_bounce_actor(player_actor, 14.0)` — Roshan hops 14 pixels on the painted stage, several hundred pixels away from the card the child is looking at — and a grey progress bar moves.

**D5 — the fictions and the widgets don't match.** magician CABINET says *"Tap on the star flashes to open the cabinet!"* over a top hat on a bar (no cabinet, no star). nursery BURP says *"Tap in the green for gentle burp-pats!"* over a baby sliding sideways (no patting). detective NAME says *"Tap when the spotlight shines on the answer!"* over an un-matted grey rectangle (no spotlight, no answer). The template was applied to the careers without adapting the verb. Where the template genuinely can't carry the fiction (CABINET, NAME), the beat should change template rather than get new art.

---

## Ranked fix order

1. **W1** — hit state for all 11 timing beats. One `hit_flash` variable; the art already exists. Biggest feedback win per line changed.
2. **W2 + A5** — correct-pick response for the 10 lanes beats, and repaint the `_lit` atlases so the flash is visible. Currently the loop rewards failure.
3. **D1** — a real completion beat. Fixes all 21 rows' COMPLETION column *and* every other beat in the game.
4. **W4** — gauge `timing_zone = Vector2(0.367, 0.739)`, needle sweep to ±53°, needle length to 117px. Stops the dial lying to the child.
5. **W3** — lanes overlay y 0.700 → 0.509, size 124 → 90.
6. **A6 / A7** — re-cut `widget_track_detective.png` and the magician hats.
7. **A9** — shrink the track mover so it stops covering the green zone.
8. **A1 / A2 / A3 / A8** — real career-specific gauge dials, a real needle, real success cards, movers that depict the verb.
9. **D2** — style `phase_fill`.
10. **W6 / W8** — delete `_draw_nursery_context` and the unused baby loads; drop the duplicated `set_fill` lines.

---

## AUDIT: motion-and-world

# OPERA BEAT AUDIT — trace / push / crank / target / bop / lens

Files audited (all absolute):
- `C:\Users\Peter\Documents\mermaid-roshan-reef\.worktrees\codex-opera-art-regeneration\scripts\opera_gesture_surface.gd`
- `C:\Users\Peter\Documents\mermaid-roshan-reef\.worktrees\codex-opera-art-regeneration\scripts\opera_career_world_2d.gd`
- `C:\Users\Peter\Documents\mermaid-roshan-reef\.worktrees\codex-opera-art-regeneration\assets\opera\worlds\widgets\` (all 4 templates fully enumerated)

---

## HEADLINE: THE SET_FILL BUG HAS A TWIN, AND IT IS WORSE

`set_fill` is now wired (`opera_career_world_2d.gd:1048`), so the *progressive* overlays move. But **every terminal "success" state in the widget system is unreachable by construction.** In `_on_gesture`:

```gdscript
surface.set_fill(progress)        # line 1048 — widget_fill = 1.0, queue_redraw()
...
if phase_progress >= goal:
    phase_index += 1
    _show_phase()                 # line 1071 → surface.configure() → widget_fill = 0.0, new textures
```

`queue_redraw()` only marks the node dirty; the draw pass runs at end of frame. By then `configure()` (`opera_gesture_surface.gd:80`) has already zeroed `widget_fill` and swapped the texture set to the *next* phase. Therefore these branches in `_draw_widget_layers` **can never be true at draw time**:

- `"target"`: `if widget_overlay != null and widget_fill >= 0.96:` (line 489)
- `"basin"`: `if widget_fill >= 0.96:` (line 464)

The child never sees a finished thing. Not once, in any career. `phase_gap = 1.0` does *not* help — it only gates input in `_on_gesture`; the card has already been repainted with the next beat's art.

**THE SINGLE HIGHEST-VALUE FIX IN THIS AUDIT:** add a completion hold. Something like `_finish_phase()` that sets `surface.set_fill(1.0)`, sets a `complete_hold = 0.9` timer, plays the success layer + a chime, and only then calls `_show_phase()`. One change unblocks target, basin, charge and gauge completion across all 13 careers.

Also flagging as evidence of a hasty patch: `surface.set_fill(progress)` is **pasted twice** at lines 1048–1049 and 1127–1128, and `surface.set_fill(0.0)` twice at 703 and 726. Harmless, but clean it up.

---

## SCORECARD

| Beat (template) | Phases | CLARITY | FEEDBACK | COMPLETION |
|---|---|---|---|---|
| **trace** (swipe) | chef PIPE, detective TRAIL, ballerina RIBBON, doctor BANDAGE, magician ROPE, painter SKETCH | 4 | 4 | **2** |
| **push** — lr (swipe) | farmer HERD, racer STEER | **3** | **2** | **1** |
| **push** — boxer DUCK | boxer DUCK | **1** | **2** | **1** |
| **push** — nursery BEDTIME | nursery BEDTIME | **1** | **2** | **1** |
| **crank** (circle) | 9 phases (chef STIR, ballerina TWIRL, candymaker WRAP, doctor CAST, magician PORTAL, painter STROKES, astronaut VALVE, racer LAP TWO, popstar ENCORE) | **3** | 4 | **2** |
| **target** (tap) | 8 phases (chef TOP, candymaker SHARE, doctor X-RAY, farmer PICNIC, boxer BELT, painter SPLAT, astronaut PATCH, racer FINISH) | **2** | **3** | **1** |
| **bop** (world combat) | 26 phases (2 per career) | **3** | 5 | **2** |
| **lens** (magnifier) | detective LENS, detective SEARCH | 4 | 4 | **2** |

---

## TRACE — 4 / 4 / 2

**What the art literally is.** `widget_trace_chef.png` (1024×608) is a lovely painted piping bag over a frosting swirl — with a **flat dark slate-purple zigzag polyline baked into the illustration**, running left→right across the middle, drawn straight over the piping bag. `widget_trace_chef_lit.png` (3 KB, 25 643 non-transparent px) is that same zigzag in flat gold, nothing else. So the mechanic is: dark guide path → wipes gold as you swipe. All 6 careers ship base + `_lit`; asset coverage is complete.

**Why it works.** `_draw_progress_overlay(widget_overlay, widget_fill, true)` (line 480) does a genuine horizontal wipe. Now that `set_fill` is called, this is the *only* template in my set with honest, legible, continuous feedback. The `_draw_demo_finger` `"swipe"` branch (line 563) sweeps the ghost dot left→right along the same axis. Clarity and feedback are basically fine.

**COMPLETION = 2 — ART.** No `widget_trace_*_full/_success/_lit-done` file exists (verified: zero matches). The terminal state is "the zigzag is now yellow." Combined with the instant phase advance, even the fully-gold line is on screen for zero frames. A four-year-old piping frosting should end with **frosting on a cake**, not a coloured line.
Needed: `widget_trace_<career>_done.png` — chef: the swirl now piped onto a finished cake; doctor: the bandage wrapped around the limb; painter: the sketch filled in as a sunrise.

**Minor (FEEDBACK deduction).** The wipe tracks *cumulative* `phase_progress`, not finger position, so scrubbing backwards still advances it, and the piping bag itself never moves. Consider driving the mover prop along the path by `widget_fill`.

---

## PUSH — 3 / 2 / 1 (lr), 1 / 2 / 1 (DUCK and BEDTIME)

Assets are complete-by-name: `widget_push_{boxer,farmer,nursery,racer}.png` + `_mover.png`, plus `widget_push_shared_arrow_down.png` and `_arrow_lr.png` (plain flat gold arrows, no career flavour). The movers are correct isolated props — racer = a coral racing pod with bubbles, boxer = a pair of boxing gloves.

### FEEDBACK = 2 — DESIGN (this IS the playtest complaint, in swipe form)

```gdscript
"push":
    var mover_point := center + swipe_dir * widget_fill * 42.0
    _draw_widget_sprite(widget_mover, mover_point, 136.0)
```
(`opera_gesture_surface.gd:482`)

**42 pixels of total travel across an entire 7–9 second beat**, on a 392 px-wide surface. That is 11 % of the card, spread over dozens of swipes — sub-perceptual per stroke. And the prop never follows the finger; it only creeps with cumulative progress. The child swipes and the world does not move.
Fix: make the prop track the pointer laterally *plus* travel the full usable width with `widget_fill` (≥ 250 px), and give each stroke a visible kick (a scale/tilt pulse or a wake puff at the trailing edge).

### COMPLETION = 1 — ART

`_load_widget_set` `"push"` (line 140) loads **only** `_mover` and the shared arrow. There is no `_full`, `_success` or `_lit` in the push branch and no such file on disk. Verified: zero matches for `push_.*(_full|_success|_lit)`. Push has no ending at all.
Needed: `widget_push_<career>_done.png` — nursery: the baby **actually covered by the blanket, eyes closed**; farmer: the herd inside the pen; racer: the pod through the gate; boxer: the counter-punch whiffing overhead.

### boxer DUCK, CLARITY = 1 — ART contradicts the gate

`widget_push_boxer.png` paints a **horizontal** gold capsule track across the middle of the card. The phase is `{"name": "DUCK", "mode": "swipe", "dir": "down"}` (`opera_career_world_2d.gd:94`), so `swipe_require_dir = true` and `swipe_dir = Vector2.DOWN`. A child who follows the painted track sideways hits:

```gdscript
if aligned >= 0.35: gesture.emit("swipe", travel, 1.0)
else:               gesture.emit("swipe", travel * 0.2, 0.4)   # → competition.note_miss()
```

**The card teaches the exact gesture the code punishes.** Also `_draw_widget_sprite(widget_shared, center + swipe_dir * 92.0, 92.0)` puts the down-arrow at y = 208 on a 232-tall surface — the bottom ~22 px hangs off the card onto the progress bar.
Fix: repaint `widget_push_boxer.png` with a **vertical** track (glove above, duck-lane below), and clamp the shared-arrow anchor to `center + swipe_dir * 70.0` so it stays inside the surface.

### nursery BEDTIME, CLARITY = 1 — WIRING, a three-way contradiction

- Phase dict (`opera_career_world_2d.gd:141`) has **no `"dir"` key** → `swipe_dir` stays `Vector2.RIGHT`, `swipe_require_dir` stays `false`.
- `_load_widget_set` picks the **down** arrow: `var down := visual_context.ends_with("_boxer") or visual_context.ends_with("_nursery")` (line 142).
- The VO says *"Swipe the blankets **down**"*.
- `widget_push_nursery.png` paints a **horizontal** capsule track under a swaddled baby.

Result: a down-pointing arrow is drawn 92 px to the **right** of the baby while the baby creeps **rightward**, under a horizontal track, while the voice says "down."
Exact fix (WIRING): add `"dir": "down"` to the nursery BEDTIME phase dict at `opera_career_world_2d.gd:141`, and repaint `widget_push_nursery.png` with a vertical blanket-pull track.

---

## CRANK — 3 / 4 / 2

Asset coverage is complete: 9 careers × (base + `_mover` + `_progress`), matching all 9 circle phases exactly.

**FEEDBACK = 4 (genuinely good).** `draw_set_transform(center, previous_angle)` (line 473) means the whisk/wheel really does spin under the finger, frame by frame, driven by `_drag`. This is the one template where the object visibly responds to the hand. Deduct one for: the **first** angular step after every press pays nothing, because `if absf(change) <= 0.9 and signf(change) == signf(_last_spin) and absf(_last_spin) > 0.0001` (line 299) is false while `_last_spin == 0.0` — set on press at line 217.

### CLARITY = 3 — WIRING: the crank is dead during the ghost-finger demo

`_draw_demo_finger`'s `"circle"` branch (line 565) walks the ghost dot around a ring, but the crank mover rotates by `previous_angle`, which is **only ever written inside `_press` and `_drag`**. `configure()` does not reset it either (`previous_angle` appears at lines 21, 215, 296, 302, 473 — never in `configure`). So the handle sits frozen at whatever stale angle the *previous* circle phase left it at, while a dot orbits around it. The demo shows the motion but not the consequence.
Exact fix: in `_process`, when `demo_active and mode == "circle"`, drive `previous_angle = -2.7 + fmod(demo_t, 2.4) * 2.0` (matching the demo dot), and reset `previous_angle = 0.0` in `configure()`.

### COMPLETION = 2 — ART

`widget_crank_chef_progress.png` (7 KB) is **not chef art**. It is a generic three-concentric-gold-rings loading-spinner glyph, centred on an otherwise empty 1024×608 canvas — and it is pixel-for-pixel the same picture as `widget_target_boxer_success.png` (identical 37 029 non-transparent px, identical 7 KB). All 9 `_progress` files are this same glyph in career tints.

Worse, it is drawn as a **uniform alpha fade of the finished ring set**:
```gdscript
draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false, Color(1.0, 1.0, 1.0, widget_fill))
```
At 50 % the child sees a *ghost of the complete thing*, which reads as fog or a rendering fault, not as half-done.
Two fixes: (a) ART — `widget_crank_<career>_progress.png` should be the **stirred result** (chef: batter gone smooth and glossy; doctor: the cast wrapped; candymaker: the wrapper twisted shut), not an abstract ring; (b) WIRING — if a ring gauge is wanted, draw it as a **radial sweep** (`draw_arc(center, r, -PI/2, -PI/2 + TAU*widget_fill, ...)`) so partial progress looks partial.

### CRANK ART DEFECTS (name these files)

- **`widget_crank_painter_mover.png` — has an opaque dark-navy square background, no alpha cutout.** It is the only mover in the set like this. Drawn at `Rect2(-70,-70,140,140)` and rotating, it will show as a hard dark box spinning on the painter's card. Must be re-cut with transparency.
- `widget_crank_popstar_mover.png` is an entire **proscenium stage with curtains**. Rotating a whole theatre for ENCORE reads as a glitch. Should be a record/turntable or a spotlight ring.
- `widget_crank_racer_mover.png` is a **whole car**, spun about its centre like a pinwheel. Should be the steering wheel (the astronaut's helm-wheel mover is exactly right — copy that approach).
- `widget_crank_chef.png` already has a **static whisk baked into the bowl**, and the rotating `_mover` whisk is drawn at the same centre — so the child sees two whisks, one moving and one not. Repaint the base with the bowl only.

---

## TARGET — 2 / 3 / 1 (the weakest beat in my set)

8 tap phases, and the asset set is base + `_mark` + `_mover` for all 8 — but `_success` exists for **boxer only** (`widget_target_boxer_success.png`; verified, one file).

### CLARITY = 2 — ART: the backdrop and the target are the same picture

`widget_target_racer.png` is a full-card painted **checkered flag**. `widget_target_racer_mover.png` is that **same checkered flag**, isolated. `widget_target_chef.png` is a cake-on-a-plate with two topping dishes; `widget_target_chef_mover.png` is that same cake-and-dishes scene shrunk to 256². The draw code:

```gdscript
"target":
    for mark: Vector2 in tap_marks:
        _draw_widget_sprite(widget_stamp, mark, 76.0)
    _draw_widget_sprite(widget_mover, tap_point, 142.0)
```

`configure()` sets `tap_point = size * 0.5`, so **at phase start a 142 px flag is drawn exactly on top of the painted flag** — a double image. After the first tap the small one jumps elsewhere and two flags coexist, only one of which is tappable. A non-reader cannot tell which.
Fix (ART): `widget_target_<career>.png` must be the **scene/context** (the cake stand, the finish straight, the ward), and `_mover` must be a **small distinct thing to hit** (a single cherry, a single zoom-strip chevron, a single crack on the bone).

Two movers are also semantically wrong for their VO line:
- `widget_target_astronaut_mover.png` is a **whole rocket**, for *"Tap the sparkle leaks to patch them!"* — needs a leak/bubble-spurt sprite.
- `widget_target_doctor_mover.png` is an **X-ray monitor showing a smiling starfish**, for *"Tap the glowing cracked bone!"* — needs a cracked-bone highlight.
- `widget_target_farmer_mover.png` is **three piggies on a picnic blanket** (a whole scene), for *"Tap a snack for every happy piggy"* — needs a single snack.
- Correct as-is: boxer (championship belt), candymaker (wrapped candy), racer (flag, if the backdrop changes).

### CLARITY = 2 — WIRING: `_draw_demo_finger` has no `"tap"` case

`_draw_demo_finger` (line 561) matches only `swipe`, `circle`, `choice`, `timing`, `bop`, `hold`. `"tap"` falls through to the default `at = center`. That is coincidentally right on the very first demo (because `tap_point` starts at centre) — but `restart_demo()` fires from the 9-second idle nudge (`opera_career_world_2d.gd:1670`) mid-phase, at which point `tap_point` has relocated via `_relocate_tap_point()` and **the ghost finger pulses at the middle of the card, pointing at nothing.** A stalled child is actively misdirected.
Exact fix: add `"tap": at = tap_point` to the match in `_draw_demo_finger`.

### FEEDBACK = 3

Real: each hit appends to `tap_marks` and stamps persistently, and the target relocates. Deductions:
- **ART** — every `_mark.png` across all 8 careers is the **same generic pip**: a white dot inside a navy ring with a faint career-tinted halo. Not a topping, not a paint splatter, not a bandage. The stamps say "something happened" but never "I put a cherry there."
- **DESIGN/WIRING** — a *miss* draws nothing on the card. `_press` line 226 emits `gesture.emit("tap", _miss_pay(), 0.4)` with no visual. Compare stray taps in combat, which get `_bop_burst_at(to, true)`. To a four-year-old an unresponsive tap reads as a broken game. Add a fizzle burst at the miss point.
- **Layout bug** — `_relocate_tap_point()` puts `tap_point.y` in [56, 176] and the mover is 142 px, so its half-height 71 pushes it to y ∈ [-15, 247] on a 232-tall surface: **the target prop is clipped off the top and bottom of the card at extreme positions.** Tighten the relocation amplitude to ~0.18 of `size.y`.

### COMPLETION = 1 — ART **and** WIRING, compounding

- **ART:** `widget_target_{chef,candymaker,doctor,farmer,painter,astronaut,racer}_success.png` **do not exist** → `widget_overlay` is null for 7 of 8 careers → the branch is skipped outright.
- **ART:** boxer's one `_success` file is the **generic three-ring loading spinner** (identical to the crank progress glyph), not a picture of winning the belt.
- **WIRING:** even a correct file would never render — see the HEADLINE section. `widget_fill >= 0.96` is unreachable at draw time.

So: `widget_target_<career>_success.png` must be authored (8 files, showing the **finished job**: the cake fully topped, the bone healed and glowing, the finish line crossed with confetti, the belt raised) **and** the completion-hold must be added. Either fix alone accomplishes nothing.

---

## BOP (world combat) — 3 / 5 / 2

**FEEDBACK = 5. This is the best-served beat in the entire game and should be the model for the others.** `_bop_burst_at` puff + confetti; `_apply_imp_pose` gives every AI pose its own squash/tilt/lift/tint; the full per-costume state set is delivered on disk — `rival_<career>_{windup,charge,slash,recover,guard,taunt,flee,stagger,bopped,bow,hop_a,hop_b}.png` for all 12 competitive careers, plus `imp_mischief_*` and `imp_captain_*`; `_draw_combat_fx` renders telegraph rings, "!" bangs, dust, slash arcs, dizzy stars and an orbiting stolen sparkle from real textures; death is a spin-and-fade tween; contact shoves Roshan. Misses fizzle. Nothing here is unwired.

### CLARITY = 3 — WIRING: bop's ghost-finger demo is dead code

`_draw_demo_finger`'s `"bop"` branch (line 577) iterates `bop_targets`. **`set_bop_targets()` is never called anywhere in `opera_career_world_2d.gd`** (grep confirms: only definition + internal uses in `opera_gesture_surface.gd`). Combat moved to `combat_layer`, and `_apply_panel_layout` sets `action_panel.visible = false` for bop, so the surface is hidden anyway. There is therefore **no first-touch pointer for the very first thing a child does in every career.** The roaming imps carry it — but a one-time ghost hand tapping the nearest imp on `combat_layer` would close the gap. (`opera_gesture_surface.gd` lines 24–29, 186–196, 256–272 and the `"bop"` demo branch are all dead in the current architecture — either delete or re-point at `combat_imps`.)

### COMPLETION = 2 — WIRING

`phase_fill` and `phase_label` are **children of `action_panel`**, and `_apply_panel_layout` (line 734) hides the whole panel for bop and lens:
```gdscript
if mode == "bop" or mode == "lens":
    action_panel.visible = false
    return
```
So during a 10-goal captain chase there is **no progress indicator anywhere on screen**. Worse, the captain reserve silently freezes progress:
```gdscript
if amount < 5.0 and (captain_pending or _live_captain_hp() > 0):
    var reserve := 2.0 if captain_pending else float(_live_captain_hp())
    phase_progress = minf(phase_progress, goal - reserve)
```
— bops stop counting with zero on-screen explanation. And when the last imp pops the phase advances instantly, cutting the 0.62 s bopped-fade tween off mid-flight via `_clear_stage_combat()`. No "you cleared them" moment.
Exact fix: reparent `phase_fill` (or add a stage-level twin) to `root` so it survives `action_panel.visible = false`, and route the completion hold through the same `_finish_phase()` so the last imp's fade + a cheer actually play.

---

## LENS (detective LENS + SEARCH) — 4 / 4 / 2

**CLARITY = 4.** `_tick_lens` drifts the magnifier on a sine path across the whole stage while `lens_demo` is true, using the real painted `assets/opera/worlds/ui/magnifier.png`. That is a proper ghost demo and it is wired. Deduct one: clues are invisible beyond 118 px, so before the lens moves the stage looks empty and the VO's "find the glowing clues" has no referent.

**FEEDBACK = 4.** Proximity reveal `reveal = clampf(1.0 - d / 118.0, ...)` plus a twinkle, plus a real dwell meter:
```gdscript
lens_layer.draw_arc(lens_pos, 100.0, -PI * 0.5, -PI * 0.5 + TAU * clampf(lens_dwell / 0.45, 0.0, 1.0), 40, Color(1.0, 0.9, 0.4), 6.0)
```
That ring visibly filling is exactly the "it's working" signal the playtester said was missing elsewhere.

**Deduct one — WIRING:** `lens_demo` is set `false` on the first touch (lines 1586/1589/1592/1595) and **never restored**. The 9-second idle nudge calls `surface.restart_demo()`, which does nothing because the surface is invisible during lens. A stuck child gets a repeated voice line and no visual help, forever.
Exact fix: at `opera_career_world_2d.gd:1669`, when the current phase mode is `"lens"`, also set `lens_demo = true`.

**COMPLETION = 2 — ART + WIRING.** A found clue becomes:
```gdscript
lens_layer.draw_circle(spot, 10.0, Color(1.0, 0.9, 0.5, 0.9))
```
A **10-pixel dot on a 1280×720 painted stage.** There is no found-clue art anywhere — `assets/opera/worlds/ui/` contains only `magnifier.png`, `station_marker.png`, `task_card_frame.png`; `props/` contains only `fx_*` and `goal_*`. And because `action_panel` is hidden, `phase_fill` is hidden, so there is **no "3 of 5 found" counter** either. The beat just ends.
Needed (ART): `assets/opera/worlds/ui/clue_found.png` — a big pinned magnifier-badge or a checked evidence tag, ~90 px, drawn permanently at each found spot; plus a stage-level found counter (five sockets that light up), which the reparented `phase_fill` from the bop fix would also serve.

---

## PRIORITY ORDER

1. **Completion hold** in `_on_gesture` / `_show_phase` — unblocks every terminal state in the game. WIRING, one place.
2. **Author the 8 `widget_target_<career>_success.png`** and re-cut the 7 target `_mover` sprites so the target is not a copy of its own backdrop. ART, biggest clarity win.
3. **`"dir": "down"` on nursery BEDTIME** + repaint `widget_push_boxer.png` / `widget_push_nursery.png` with vertical tracks. WIRING + ART, fixes two beats that teach the wrong gesture.
4. **Push travel 42 px → full card width** and make the prop follow the finger. DESIGN, this is literally the reported complaint.
5. **Reparent `phase_fill` out of `action_panel`** so bop and lens have progress. WIRING.
6. **Add `"tap"` to `_draw_demo_finger`; drive `previous_angle` during the crank demo; restore `lens_demo` on idle.** Three small WIRING fixes to the ghost-finger system.
7. **Re-cut `widget_crank_painter_mover.png` with alpha** (opaque navy box today) and replace the 9 generic ring-spinner `_progress` glyphs with real stirred-result art. ART.
