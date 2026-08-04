# Codex handoff — opera minigame widget art at full ambition (2026-08-03)

**Audience:** Codex — image generation + deterministic promotion.
**Purpose:** regenerate the diegetic art for all ~60 non-combat opera beats at the caliber of the goal props and the career paintings. The engine work is finished and merged; this file and its ledger are the art request.
**Companion ledger:** `OPERA_WIDGET_ART_REQUEST_LEDGER_2026-08-03.csv` — 221 rows, one per file. **The ledger is the authoritative per-file request list.** This document is the grammar; the ledger is the work.
**Conventions by reference:** the weighted acceptance gate, auto-rejection list, STYLE-JOBS / STYLE-HOUSE contracts, P2-09 canonical prop locks, and the staging protocol are as written in `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md` and `CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md`. Everything in those files still binds except where section 9 below explicitly supersedes it.

---

## 1. THE DIRECTION

The owner, on the art:

> "The art style is still very minimal — I want to see ingredients mixing in a bowl, pouring out into a bowl, piping bags in full screen glory."

The owner, on the interaction (`OPERA_INGREDIENT_INTERACTION_DIRECTION_2026-08-03.md`):

> "If we're having this complexity of ingredients, the gameplay should impact it. You should have to crack the eggs, for example, in a visceral motion."

### The caliber target

Not "better widget art." **The widgets must reach the standard already set by the goal props and the career paintings**, which are in this repo and are the only reference that matters:

- `assets/opera/worlds/props/goal_chef.png` — three-tier cake, 512². Every tier has its own crumb texture; the piped rosettes have directional swirl and a specular kick on the outer curl; the cherries have stem, highlight and a cast shadow onto the frosting; the doily plate has painted lace holes. The ink contour is warm dark plum and it *varies* — heavier under the plate, lighter on the lit side.
- `assets/opera/worlds/props/goal_magician.png` — cloud-lamb over a velvet top hat. Velvet reads as velvet: a soft sheen band across the nap, not a flat purple. Sparkles are four-point painted diamonds with pearls between them, not particle dots.
- `assets/opera/worlds/backdrops/world_chef.png`, `world_astronaut.png` — 1024×576 full-bleed painted rooms, forty-plus identifiable objects each, foreground / midground / horizon, soft depth haze.

**That is the bar: warm key light from upper-left, cool bounce from lower-right, painterly modelling, coral / plum / teal / cream / antique gold, pearl-and-shell motif, hand-inked varying contour, no flat fills anywhere.** `world_chef.png` already contains more baking than every chef widget combined. That is the gap being closed.

### Before and after, one line per template

| Template | n | Now | After |
|---|---|---|---|
| **T1 gauge** | 3 | One white card with a navy fan and a mint wedge, a corner prop pasted at 25%, and three byte-identical success blobs (md5 `be61d2f5…`) | The dial is bolted to the machine it measures — oven door, boiler belly plate, kart dash — and a new `_fill` shows the work itself: the cake rising in the tin, fuel climbing the column, turbo lamps stacking |
| **T2 track** | 8 | A prop floated at 22% over a flat lozenge bar, and the mover is a duplicate of the static prop, so two identical objects sit on screen and neither performs the verb | A real ground plane with the sweet spot as a real place on it — light pool, focus mitt, confetti arch — the mover is the *acting* object, and a new `_fill` accumulates what the run produces |
| **T3 pour** | 4 | A second identical bowl fades in while she holds, and a flat `#FFDF95` rounded rectangle grows on the **outside** of a bowl that stays empty | A tipped jug with a stream leaving the lip for exactly as long as her finger is down, and a painted column of batter rising *inside* the bowl with ingredients surfacing as the level passes them |
| **T4 basin** | 2 | Three near-white broken rings (mean RGB 242,250,242) wiping across a sink like fog — and nursery WASH HANDS is the same picture as nursery FEED | A real basin with suds mounding up from the water line, discrete bubbles, hands lathering; two beats that no longer look identical |
| **T5 charge** | 5 | A cream disc that is pixel-for-pixel the ghost-finger hint, plus one mint rounded rectangle 50px wide pinned to the right edge — that rectangle is the entire "progressive reveal" layer | The career's power visibly accumulating: the beam building on the dancer, the splash crown rising out of the puddle, fire climbing the rocket, the hall waking row by row |
| **T6 crank** | 9 | A flat three-ring loading-spinner glyph cross-faded over the scene at alpha=progress, so 50% reads as fog; the painter's mover is an opaque navy box; the racer spins a whole car like a pinwheel | The progress layer becomes a **complete repaint of the same scene finished**, so circling dissolves separated ingredients into smooth batter, a dark hat into a blazing vortex, a bare limb into a decorated cast |
| **T7 trace** | 6 | The identical flat slate polyline in four careers, wiping to the same line in flat `#FCD98A` — for the headline PIPE beat, the thing that grows is a yellow stick | A chalk-ghost of the real thing painted into the backdrop at ~22%, and a painted rope of five-ridge buttercream extruding out of the nozzle as she drags, ending in a cherry-crowned swirl |
| **T8 push** | 4 | 42px of total travel across a 7–9 second beat, a flat yellow arrow, a mover that duplicates the pig already in the backdrop — and boxer DUCK's card paints a *horizontal* track while the code requires DOWN | An empty start and a rewarding destination, a pearl-and-coral bubble chevron, vertical tracks where the gesture is vertical, and a held success image |
| **T9 target** | 8 | The backdrop and the target are the same picture drawn twice at two sizes; every `_mark` across all eight careers is the same generic pip; seven of eight beats have no success image and the eighth is the loading spinner | A scene with a hole in it, one small distinct thing to hit, a mark that is the *placed object* — a cherry, a splat, a rivet plate — and eight finished-job success frames |
| **T10 lanes** | 10 | Three tokens floating at 30% on a white card; the "lit" cell is measurably no brighter than the unlit pad (detective: **−12.2 luma**) | Three full-height bays read from ceiling to floor, the "which one" prompt painted as a real object, and a lit cell that is unmistakably ON |
| **T11 catch** | 1 | An empty white card with three yellow dots on two grey strings; the pillow floor is five flat purple ellipses | A warm lamplit nursery with a real turning mobile, a painted pillow drift with fabric weight and folds, and Roshan's carry-blanket cradle |

---

## 2. ENGINE WORK IS DONE — THIS IS PURELY AN ART REQUEST

Two commits landed before this handoff:

- `192122c2` — *the widget art never filled ("the bowl never pours")*
- `cd624567` — *the feedback bugs the playtest exposed — seven wiring defects*
- `8f10da7d` — *full-ambition widget art concepts + aspect-squash fix*

**No engine change is a precondition for any row in the ledger.** Every layer requested is consumed by code that exists on this branch today. Do not wait on, request, or assume any further engine work.

### What the engine now provides — exploit all six

**1 — Ink-band progressive reveal.** `_draw_progress_overlay()` (`opera_gesture_surface.gd:463`) calls `_ink_bounds()` (`:426`), which scans every row of the PNG for any pixel with `alpha > 0.08` (sampling every 4th column) and caches the result per texture. The reveal edge then sweeps **upward through that measured band**, so 0–100% of the beat maps to 0–100% of *the visible ink* — not of the canvas. Before this fix the pour was fully drawn at fill 0.43 and then sat frozen for 2.84 of chef POUR's 5 seconds. That was the playtest complaint verbatim; it is gone. Drives `pour` `_fill`, `basin` `_bubbles`, `charge` `_full`.

**2 — Aspect-preserving cover fit.** `_cover_rect()` (`:454`) scales by `max(panel.x/tex.x, panel.y/tex.y)` and centres. The backdrop (`:352`) and every progressive overlay (`:483`) go through the same rect, so **backdrop and fill stay pixel-registered to each other at any panel size**, and nothing round is an egg any more (the old plain stretch squashed 1.684 art into a 1.398 panel by ~17%).

**3 — 1:1 rotation movers.** `crank` does `draw_set_transform(center, previous_angle)` (`:534`), where `previous_angle` is the **raw pointer angle from panel centre**. The object turns exactly with her finger, frame by frame, in both directions, through unlimited revolutions. This is the one template where the depicted object already responds directly to the hand.

**4 — Full-canvas cross-fade progress layers.** `crank` draws its overlay as `draw_texture_rect(overlay, panel, modulate = Color(1,1,1,widget_fill))` (`:538`) — a whole-frame dissolve, not a wipe. **This is the most under-used capability in the engine.** It means the progress layer can be a complete repaint of the entire scene in its finished state, and circling continuously dissolves raw → finished across the whole frame. A real, rich, continuous animation from one static PNG.

**5 — Held-only movers.** `pour` draws its mover **only while `held`** (`:516-517`). The pouring is literally her finger being down: the jug tips when she presses and rights itself when she lifts, with no state machine and no frame sequence.

**6 — Completion hold.** On `phase_progress >= goal` (`opera_career_world_2d.gd:1072-1081`) the engine now pins `set_fill(1.0)`, fires `_bop_burst_at()` on the card centre, and forces `phase_gap ≥ 0.9s` before advancing. Terminal states used to live ~0.18s or, for `target`/`basin`, be unreachable at draw time entirely. **`_success` layers are now worth painting** — they are held, celebrated, and seen.

Also fixed and relevant: the charge meter fills progressively instead of fading in whole over the last 18% (W1); the hold affordance draws again on widget-backed beats (W7); a finger already down clears its own phase gap (W5); the on-stage bounce is rate-limited instead of spawning a tween 60×/second (W4); the duplicated `set_fill` is gone (W6).

### Author to today's numbers

The panel has **not** been resized to full screen. Compose for what the engine draws now, and the art will only improve if the panel grows later.

| Layer | Drawn at | Anchor |
|---|---|---|
| backdrop / `_success` / `_progress` | cover-fit to panel | full bleed |
| `gauge` `_needle` | `Rect2(-48,-84,96,96)`, ±60° | pivot `(0.5w, 0.82h)` |
| `track` `_mover` / `_hit` | 128px / 82px | `x = lerp(0.12w, 0.88w, t)`, `y = 0.66h`; zone `t ∈ [0.30, 0.72]` |
| `pour` `_mover` | 138px, **held only** | `centre − (0,18)` |
| `basin` shine | 118px, at `fill ≥ 0.96` | centre |
| `charge` `_glow` | 108px → 234px with fill | centre |
| `crank` `_mover` | `Rect2(-70,-70,140,140)`, rotated | image centre = pivot |
| `push` `_mover` / arrow | 136px, travel 42px / 92px at 0.72α | centre + `swipe_dir` |
| `target` `_mover` / `_mark` | 142px / 76px | roaming `tap_point`, ±0.30w ±0.26h |
| `lanes` `_lit` cell | 124px from a 256px source cell | `x = (i+0.5)/3 · w`, `y = 0.70h` |

**The crop rule.** Author 1024×576 (16:9). The panel is 372×266 (1.398) on entry and 392×232 (1.690) in play, and cover-fit crops the *width* in both cases — up to **10.7% off each side** at the narrower panel. Height is never cropped, so vertical fill registration is always exact. Therefore: **paint full bleed to all four edges, but keep the hero, every readable secondary prop and all fill ink inside x 110–914** (the centre 78%).

**Two hard exceptions.** The `lanes` `_lit` strip must be **exactly 768×256** — the engine slices `Rect2(lane·256, 0, 256, 256)` out of it, and any other size shears the cells. And `opera_nursery_catch.gd:230` still plain-stretches its backdrop and strokes a 5px teal border over it (`:233`), so the **catch backdrop is the one file that must be composed tolerant of both a stretch and an engine-drawn frame** — keep it low-contrast at the extreme edges.

---

## 3. THE LAYER GRAMMAR

These rules are derived from the reveal implementation, not from taste. They apply to every beat in the ledger.

**G1 — A fill layer contains ONLY the rising contents.** Not the vessel, not the steam above it, not the shadow beneath it. `_ink_bounds()` measures the *whole* painted extent of the file; one stray pixel of steam at the top or a soft shadow at the bottom stretches the band, and the level stops short of the rim while the child is still holding. Everything else on that canvas must be fully transparent.

**G2 — Every horizontal row must read as a plausible surface.** The reveal edge is a hard horizontal line. A single painted meniscus ellipse gets sliced in half at every intermediate level. Paint the fill as a **column of liquid**, not as a filled shape with a lid: a soft vertically-repeating gloss/foam gradient through the whole body, brightest where the shape narrows. The same rule generalises — a rising stack of bales, lamps lighting from the floor up, a crowd filling a hall from the front rows back, the splash crown rising out of the puddle. **If a slice of it would read as "cut in half" rather than "partly done," it is composed wrong.**

**G3 — Ingredients stacked at staggered heights emerge one at a time as the cut passes them.** This is free animation and it is how the owner's "ingredients tumbling in" is delivered at zero engine cost. Solid objects painted *inside* the liquid body at **15% / 35% / 55% / 75% / 92% of the ink band** surface in sequence across the hold. Chef POUR: two yolks low, sugar crystals and a butter curl at a third, a third yolk and a flour swirl at mid, vanilla seeds and a cocoa marble high, a slick of gloss near the rim. Declare the stack positions in the ledger row.

**G4 — Rotation movers pivot at the exact image centre and must read at all 360°.** `previous_angle` is the raw pointer angle, so the sprite will be seen upside-down, sideways and everywhere between. Compose **radially**: a whisk seen from directly above as a rosette of eight foreshortened wires; a bandage roll end-on with a coral thread marker running through it so the turning is legible; a rune ring. **A whole car, a proscenium stage with curtains, or anything with a "correct way up" is disqualifying** — those are today's defects (`widget_crank_racer_mover.png`, `widget_crank_popstar_mover.png`).

**G5 — A cross-fade progress layer is the finished scene repainted.** Same composition, same camera, same crop, pixel-registered to the backdrop, fully opaque. **Every region that should not change must be painted identically in both files** — the corner props, the counter edge, the window behind — or the dissolve ghosts instead of transforming. Only the region that is *doing the work* differs: separated ingredient islands → one silky batter; a dark hat mouth → a blazing violet vortex; a bare limb → a smooth decorated cast. This is not an overlay. It is the second half of a two-frame film.

**G6 — Horizontal (`trace`) layers are laid out chronologically left to right.** The wipe edge is a straight vertical cut sweeping right, so the thing that should appear first sits at the far left. Long, roughly-horizontal **ribbon forms are ideal** — the vertical cut across a ribbon reads as the fresh, still-emerging end. Paint the first ~40px of ink at the wipe boundary as a slightly domed, glossier terminal so wherever the wipe stops it looks like frosting still emerging, not a sliced sausage. Round elements get sliced vertically: keep them small and frequent (beads, pearls, sparks) so the slice passes in under 3% of the drag, or make them large and place them at the far right where popping in over the last 5% reads as a finale. **The expression trick:** paint a *changed* version of something — a happier face, a smaller bandage roll — into the `_lit` layer at the x-position where it should change. When the wipe passes that x, the new version covers the old. Free state change, zero engine cost.

**G7 — A mover is never a duplicate of its own backdrop.** If a thing is the mover, it does not appear in the backdrop; the backdrop paints its **absence** — the empty pen, the hollow in the pillow, the empty gold setting, the crack in the hull. Every current `pour` mover, both `track` movers and most `target` movers violate this and read as a rendering error.

**G8 — Full bleed, opaque, no card.** No baked white inset panel, no rounded corners, no border stroke, no floating ellipse tab, no crop of the career world showing through. Every current backdrop carries a dead badge oval at ~(455,25)-(575,90) that no code path ever draws into; it is visible at rest and reads as unfinished art. **The hero occupies 70–85% of the frame and is cropped by at least one edge** — cropping is what makes it a place she is standing in rather than an icon on a card. **Every frame carries at least six, ideally 8–12, identifiable secondary props** in the corners and margins.

**G9 — Clean alpha from the start.** Movers, marks and `_lit` layers are painted on transparency, never cut out of a flat card. White matte fringing and un-cut-out source rectangles are disqualifying at any scale (today: `widget_crank_painter_mover.png` has an opaque navy square, `widget_charge_magician.png` has an uncut teal card baked in, the magician hats have alpha damage eaten out of the crowns).

**G10 — Green is reserved.** The success-zone green (≈ RGB 117,240,158) appears ONLY in the baked go-zone of T1 gauge and T2 track. It is the one channel that tells a pre-reader "wait for THIS." Aqua fuel, teal palette and mint props must stay clearly distinct from it in hue and value.

**G11 — Content locks.** No words, letters or numerals anywhere. No baked Roshan, Faron, rivals or imps — they are runtime sprites. Creature subjects that ARE the task (piggies, plushy starfish patients, babies, the bunny-fish) are allowed as props and patients. **Hands are allowed and encouraged** — small cream-gloved mermaid hands gripping the piping bag, steadying the jug, lathering in the basin. Every P2-09 canonical prop design binds where its prop appears; bubbles never flame; stars only as effects; the automatic-rejection list applies. Underwater physics: no smoke or steam — **bubble plumes**; no dust — **shimmer motes**; liquids are dense, luminous and pour slowly.

---

## 4. THE INGREDIENT-STATE REQUIREMENT

The interaction direction changes what "one beat's art" means. Until now every beat has been *a gesture mode with a skin on it*: the beat is `hold`, the art behind it is a bowl, and the finger acts on the surface while the picture reacts in the abstract. The direction is **direct manipulation of the depicted objects** — each ingredient is a thing on screen with its own state, and the motion that changes it is the motion you would really make.

> "Visceral is the operative word: the crack should be a *snap*, with a shell that splits, a yolk that drops and lands. Not a meter filling."

**What this means for the request: every ingredient the art depicts now needs its STATES, not just its presence.** This is more art per beat than "backdrop + fill overlay," but it is the same painted-layer economy — states are layers the engine swaps or reveals, never frame sequences.

### Delivery format

State sets ship as a **horizontal strip of 256px cells on transparency, cells left→right in state order**, named `widget_<template>_<career>_state_<object>.png` (N × 256 by 256). This follows the existing `lanes` `_lit` precedent, which the engine already slices by 256px source rect.

**Sequencing note:** the ingredient surface mode that hit-tests these per object is the next engine pass, not this one. Author the strips now anyway — until that mode lands, **the same cells are the source material the `_fill`, `_progress` and `_success` layers are composed from**, so nothing painted here is wasted, and when the mode ships the art is already on disk.

### Tier A — full per-object state sets (the recipe beats)

These are the beats whose fiction is genuinely a short recipe — *crack two eggs → tip the milk → stir it smooth* — three small satisfying actions rather than one long abstract hold. Order is forgiving: any object can be handled at any time, and the beat completes when all are done.

| Beat | Object | States |
|---|---|---|
| **chef POUR** | egg (×2) | whole → cracking (shell split, seam open) → yolk falling → empty shell resting |
| | milk jug | upright → tipping → streaming → empty |
| | flour scoop | heaped → dusting → emptied |
| | butter | block → knifed curl → melted in |
| | bowl contents | empty → streaky → mixed |
| **chef STIR** | batter | streaky islands → combining (marbled spiral arms) → smooth |
| | yolks (×3) | intact and glossy → broken and streaking → gone |
| | whisk | clean → batter-clung → lifting a falling ribbon |
| **chef PIPE** | piping bag | full and pressure-bulged → squeezing with ribbon emerging → slack and done |
| | nozzle bead | welling → streaming → cut clean |
| | cherry | in the copper bowl → crowning the final swirl |
| **candymaker SYRUP** | syrup bottle | upright → tipped → streaming → empty |
| | mould | dry → filling → set → turned out |
| **painter FILL** | paint pot | full → dipped → spent |
| | brush | loaded → dripping → dry |
| | sunrise shape | outlined → flooding → filled |
| **nursery FEED** | bottle | full → tipped → empty |
| | baby (×3) | hungry → feeding → content, cheeks rosy |

### Tier B — state pairs and triples inside existing layers

These beats do not need a full object list, but every named object below must be painted in at least two distinguishable states, delivered inside the beat's `_fill` / `_progress` / `_success` layers per G3, G5 and G6.

| Beat | Object → states |
|---|---|
| doctor **WASH** / nursery **WASH HANDS** | tap off → running · soap dry → lathering → worn thin · hands grubby → soapy → clean · towel folded → used |
| doctor **CAST** | bandage roll fat → half → spent · limb bare → half-cased → cast and decorated · starfish face worried → brave → beaming (**use the G6 expression trick**) |
| doctor **BANDAGE** | same three faces, swapped by the wipe at the x where the bandage completes |
| candymaker **WRAP** | paper flat → creased over → wrapped → twisted and wax-sealed · three finished bonbons on the bench become four |
| nursery **BEDTIME** | blanket folded → half-drawn → tucked · baby awake → drowsy → asleep |
| chef **TOP** | each canonical topping (cherry / cream / chocolate) unplaced → placed; the `_mark` **is** the placed topping |
| painter **SPLAT** | pot full → blob in flight → splat landed; the `_mark` is the splat, rotating coral / plum / cream |
| astronaut **PATCH** | leak spurting bubbles → plate laid → riveted; the `_mark` is the pearl rivet plate |
| farmer **HERD** | pen empty → piggies entering → herd inside, gate closed |
| magician **VANISH** | bunny solid → translucent → almost pure light → gone, hat alone with one pearl spinning |

**The general rule for every other beat:** the object named in the voice line must look **different at 0%, 50% and 100%**. If it cannot, the beat's layer set is under-specified — say so in the ledger row rather than shipping a static prop.

---

## 5. HOW TO USE THE LEDGER

`OPERA_WIDGET_ART_REQUEST_LEDGER_2026-08-03.csv` — **221 rows, one row per file.** It supersedes and reconciles the three per-section manifests inside the concepts document (44 / 46 / 118), which overlap and disagree on canvas sizes. **Where this document, the concepts document and the ledger disagree, the ledger wins.** If a row is wrong, fix the row — do not diverge in the file.

Do not re-derive the request from the prose. Read the ledger, generate row by row.

| Column | What it carries |
|---|---|
| `asset_id` | Stable id, matching the filename stem. The join key to `ASSET_LICENSES.md` and the promotion commit |
| `path` | Final runtime path — `assets/opera/worlds/widgets/<file>.png` for all but the catch layers |
| `beat` | The career + PHASE the file serves (e.g. `chef POUR`) — the voice line this art must make TRUE |
| `template` | One of the eleven: gauge / track / pour / basin / charge / crank / trace / push / target / lanes / catch. Determines which engine branch consumes the file and therefore which grammar rule binds |
| `career` | The career id, for the palette and prop locks |
| `layer_role` | `backdrop` / `mover` / `fill` / `progress` / `full` / `lit` / `mark` / `needle` / `glow` / `hit` / `success` / `state` / `shared`. **This is the rule selector** — a `fill` obeys G1-G3, a `progress` obeys G5, a `lit` obeys G6, a `mover` obeys G4 and G7 |
| `canvas` | Exact authored dimensions. 1024×576 for all full-panel layers, 512×512 for movers, 256×256 for marks and shared sprites, **768×256 (hard) for lanes `_lit`**, 1024×128 for the catch pillow band, N×256 for state strips |
| **`depicts`** | **The generation line.** See below |
| `registration` | The engine-anchored geometry this file must honour — ink band bounds in source pixels, pivot, lane centres, track y, fill-region bounds. Recorded so the engine mapping is data, not guesswork |
| `refs` | Content-reference cards under `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/`, plus the caliber refs |
| `priority` | `P1` or the batch number from section 7 |
| `status` / `score` | Filled on delivery: `staged` → `accepted` / `rejected` with the weighted gate score, per the house protocol |

### `depicts` is the generation line

**`depicts` is the field that goes to the image generator.** It is written to be self-sufficient: a full scene description with the hero, its crop, the named secondary props, the light, the material read, and — for progressive layers — what is at the bottom of the ink band and what is at the top. It already carries the concept document's prose distilled to one generation-ready line per file. The concepts document is that line's **provenance and rationale, not a competing spec** — read it when you need to understand *why* a row asks for what it asks for, never to override the row.

Three fields must be reconciled before generating, every time: `depicts` says what to paint, `canvas` says how big, `registration` says where the ink must land. **A beautiful file that misses its registration is a rejected file.**

---

## 6. SHARED ASSETS

Files that serve many beats at once. These are the cheapest quality wins in the whole set — paint them first within their batch.

| File | Canvas | Serves | Request |
|---|---|---|---|
| `widget_push_shared_arrow_lr.png` | 256² | 2 beats | A **triple chevron built from pearl-and-coral bubbles**, largest and brightest at the leading tip, fading back into a soft gold streak. Soft-edged, no hard vector silhouette. The engine draws it at 0.72 alpha, so paint at full opacity and let the engine soften it |
| `widget_push_shared_arrow_down.png` | 256² | 2 beats | Same language, rotated to lead downward. Replaces the flat yellow arrow |
| `widget_basin_shared_shine.png` | 512² | 2 beats | A painted sparkle burst — four-point diamonds with loose pearls between them, per the `goal_magician.png` sparkle language. Today it is the ghost-finger cream dot, so "you succeeded" and "put your finger here" are currently the same picture |
| `widget_lanes_shared_pick.png` | 256² | 10 beats | A high-chroma pick burst. **Must not be byte-identical to `widget_track_shared_hit.png`** — today both are md5 `bafd4f0e…`, one mark doing double duty as "you hit it" and "this is the answer," at almost no contrast on the pale card |
| `widget_track_shared_hit.png` | 256² | 8 beats | The timing-hit mark, distinct in hue and shape from the lanes pick. Fallback behind any per-career `_hit` |
| `widget_gauge_shared_needle.png` | 256² | 3 beats | Fallback behind the per-career `_needle`. A **real pointer** — one fat arrow tip and a hub at the pivot end — not today's symmetric orange bar with a dot at each end, which gives a non-reader no way to tell which end points at the wedge |

### Shared not-a-file

These bind every row and are not restated per beat: the palette (coral `#E4837C` / `#E2857F`, plum `#7E5A96` / `#6B4A86`, teal `#5FB3AE` / `#4F8F96`, cream `#F5E3C8` / `#F2E3C6`, antique gold `#C99A4E`, ink `#3A2450` / `#1B2A4A` — **never black**); warm key from upper-left, cool bounce from lower-right; painterly varying contour 3–6px, never a uniform vector stroke; the four-point-star-plus-loose-pearls sparkle language; the underwater physics substitutions (bubble plumes, shimmer motes, slow dense liquids); and the caliber references `goal_chef.png`, `goal_magician.png`, `world_chef.png`, `world_astronaut.png`.

---

## 7. PRIORITY AND BATCHES

**Deliver whole beats, never whole layer types.** A beat is only reviewable as a set — a backdrop without its fill proves nothing. Do not paint 60 backdrops and then 60 fills.

### P1 — the style proof: chef POUR, chef STIR, chef PIPE

**The owner's three named beats — "ingredients mixing in a bowl, pouring out into a bowl, piping bags in full screen glory" — are literally these three.** Eight files:

- `widget_pour_chef.png` / `_mover.png` / `_fill.png`
- `widget_crank_chef.png` / `_mover.png` / `_progress.png`
- `widget_trace_chef.png` / `_lit.png`

They are P1 for a reason beyond the owner naming them: **between them they exercise all three animation mechanisms.** POUR proves the bottom-up ink-band reveal with staggered ingredients (G1-G3). STIR proves the full-canvas cross-fade repaint (G5). PIPE proves the left-to-right chronological wipe (G6). If these three are right, the grammar is proven and the remaining 213 rows are execution. If any of them is wrong, the rule that broke is wrong for a third of the set.

**Stop after P1.** Stage them, capture QA renders at gameplay scale on the Mobile renderer at fill 0.0 / 0.5 / 1.0, and get owner sign-off on the style before generating anything else. Do not batch P1 with anything.

### Batches

| Batch | Content | Why here |
|---|---|---|
| **B2** | pour ×3 remaining (candymaker SYRUP, painter FILL, nursery FEED) + basin ×2 + shared shine | Chef's direct siblings — same grammar, immediately after the proof, while it is fresh. Also kills the two worst-scoring beats in the audit (painter FILL and nursery FEED both score 1/1/1) and stops nursery WASH HANDS being the same picture as nursery FEED |
| **B3** | crank ×8 remaining | Largest single grammar (G5) after the proof, and `crank` already has the best feedback in the game (4/5) — the art is the only thing holding it back. Retires nine copies of the loading-spinner glyph |
| **B4** | charge ×5 | Biggest visible gain per file in the set: five mint rectangles become five painted scenes filling from the floor up. Also kills the cream-dot glow that is pixel-identical to the ghost-finger hint |
| **B5** | trace ×5 remaining + push ×4 + the two shared arrows | The arrows fix all four push beats at once. Push carries the two beats whose art teaches the gesture the code punishes — repaint boxer DUCK and nursery BEDTIME with **vertical** tracks |
| **B6** | target ×8 (backdrop + mover + mark + success each) | The weakest beat in the audit (2/3/1). Seven of eight have no success image and the eighth is the loading spinner. Do **boxer BELT** first — it currently has the worst success image in the project |
| **B7** | gauge ×3 + track ×8 | Both need their new `_fill` layers, which is where the "is it working?" signal comes from. Do **detective NAME** early — its backdrop ships a raw un-matted crop and it is the single worst asset in the timing set |
| **B8** | lanes ×10 + catch ×1 | Largest count, and the lit-state repaint is the whole job (today's lit cells measure up to −12.2 luma against their own unlit pads). Catch last, so the nursery room can borrow finished props from the track/BURP and push/BEDTIME scenes |

Exact row counts per batch are in the ledger's `priority` column; treat that as authoritative over any count implied here.

---

## 8. ACCEPTANCE

### The house gate (unchanged, by reference)

Staging into `assets_src/concepts/opera_regeneration_2026-08-01/cards/` with contact sheets, `PROMPTS.md` entries and ledger rows; weighted acceptance gate **pass ≥ 4.5, target ≥ 4.7**; the auto-rejection list; STYLE-JOBS / STYLE-HOUSE contracts; P2-09 canonical prop locks; **QA renders at gameplay scale on the Mobile renderer — a candidate without a runtime capture caps at 2/5 and must not ship**; one controlled promotion commit; one `ASSET_LICENSES.md` line per accepted asset.

### The new criteria

**N1 — THE 50% TEST (new, and it is the gate that matters).** Capture every progressive beat at **0%, 50% and 100%**. **At 50% the scene must be visibly different from both 0% and 100%.** Name the difference in the ledger row — "the third yolk has just broken the surface," "three of five turbo lamps lit," "the cocoa has drawn out into spiral arms." This is the criterion the whole regeneration exists to satisfy: the delivered pour was fully drawn at 43% and then frozen for 2.84 seconds, and the delivered crank progress was a uniform alpha ghost of the finished thing, which at 50% reads as fog or a rendering fault rather than as half-done. If 50% is indistinguishable from 100%, the contents are stacked too low in the ink band; if indistinguishable from 0%, too high. Either way, reject and restack.

**N2 — INK DISCIPLINE (new).** **No fill, bubbles, full or progressive layer may carry a single pixel with `alpha > 0.08` outside its intended band.** Verify by running the engine's own measurement — scan every row for any pixel above 0.08 alpha, sampling every 4th column — and compare the measured band against the row's declared `registration`. Any mismatch is an automatic rejection, not a note. This is not pedantry: the band the engine measures *is* the animation, so a stray shadow below the vessel or a wisp of steam above it silently shortens the fill and the level stops short of the rim while the child is still holding.

**N3 — The crank diff test.** Diff `<beat>.png` against `<beat>_progress.png`. Every pixel that changes outside the region that is doing the work is a ghost. Corner props, counter edges, window frames and crops must be **byte-comparable**.

**N4 — The 360° test.** Rotate every `crank` mover through twelve positions. If any reads upside-down, off-pivot, or as an object with a correct way up, reject.

**N5 — The crop test.** Mask the outer 11% of each side of every backdrop. If anything load-bearing is lost, recompose to the centre 78%.

**N6 — No duplicates.** No two files in the set may be byte-identical. Today `widget_gauge_{chef,astronaut,racer}_success.png` are one file shipped three times (`be61d2f5…`), `widget_track_shared_hit.png` and `widget_lanes_shared_pick.png` are one file doing two jobs (`bafd4f0e…`), and `widget_crank_*_progress.png` and `widget_target_boxer_success.png` are the same 37,029-pixel loading spinner. Check hashes before staging.

### The three review tests from the concepts, retained verbatim

1. **No cards.** Open any backdrop: it should look like a still from a film about the job, cropped by the frame edges — not an object floating on a white panel. **If there is a rounded rectangle anywhere in the file, it is wrong.**
2. **Count the nouns.** At least eight identifiable things per backdrop. `widget_pour_chef.png` currently has one; `world_chef.png` has forty. Land between.
3. **The six-foot test.** Stand back six feet from the tablet. **If you cannot name three ingredients in the scene, it is not finished.**

---

## 9. RECONCILIATIONS — where this file supersedes earlier documents

- **Canvas.** All full-panel layers are **1024×576** (16:9), not the 1024×608 in `CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md`. Cover-fit makes 16:9 safe and undistorted at every panel size.
- **Movers.** Author at **512×512** where the concepts say 512 and where a mover is a hero object (pour, crank, push, target); 256×256 for marks, needles, hits, glows and shared sprites. The engine scales the texture into its draw rect either way; the larger canvas survives the panel resize when it comes.
- **`lanes` `_lit` is 768×256, exactly.** Non-negotiable — the engine slices fixed 256px cells.
- **Baked characters vs. the success images.** Several concept success lines describe Roshan on screen (popstar SOUND CHECK: "Roshan at the mic"). **The content lock wins: no baked Roshan.** Paint the moment around him — the hall a wall of light, the mic live, confetti falling, glow-sticks raised — and let the runtime sprite occupy the space. Hands, crew fish, piglets, plushy patients and babies remain allowed.
- **Green vs. aqua.** The gauge concepts specify an "aqua-green GO band" and the astronaut fuel is "luminous aqua." Both are legitimate, but the go-zone green (≈ RGB 117,240,158) must stay unique to the T1/T2 go-zone: keep the astronaut's fuel and every teal prop clearly separated from it in hue *and* value.
- **Engine changes listed in the concepts are NOT preconditions.** The concepts propose panel resizes and draw-size bumps (pour mover 138→360, crank 140→360, push travel 42→300, target mover 142→300, lanes cell 124→320). Those are a future engine pass. **Nothing in the ledger waits on them.** Compose for section 2's table; the art improves automatically if and when the panel grows.
- **The catch beat is the one unfixed registration.** `opera_nursery_catch.gd:230` still plain-stretches its backdrop and strokes a 5px teal border over it at `:233`. Compose `widget_catch_nursery.png` tolerant of both.

---

## Files referenced (absolute)

**This handoff and its ledger**
- `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/CODEX_OPERA_WIDGET_ART_REGENERATION_HANDOFF_2026-08-03.md`
- `.../OPERA_WIDGET_ART_REQUEST_LEDGER_2026-08-03.csv` — 221 rows, authoritative

**Direction and evidence**
- `.../OPERA_WIDGET_ART_CONCEPTS_2026-08-03.md` — the full art direction, all ~60 beats (provenance for `depicts`)
- `.../OPERA_INGREDIENT_INTERACTION_DIRECTION_2026-08-03.md` — the ingredient-state direction
- `.../OPERA_FEEDBACK_AUDIT_2026-08-03.md` — the measured audit every "Now" column above is quoted from
- `.../CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md` — house conventions, phase census, prop locks
- `.../OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md` — the gate, the rejection list, the staging protocol

**Engine contract (read-only; no changes requested)**
- `.../scripts/opera_gesture_surface.gd` — `_ink_bounds()` `:426`, `_cover_rect()` `:454`, `_draw_progress_overlay()` `:463`, `_draw_widget_layers()` `:499`
- `.../scripts/opera_career_world_2d.gd` — panel sizing `:406-417` and `:741-745`, completion hold `:1072-1081`
- `.../scripts/opera_nursery_catch.gd` — catch geometry `:224-296`

**Caliber and content references**
- `.../assets/opera/worlds/props/goal_chef.png`, `goal_magician.png`
- `.../assets/opera/worlds/backdrops/world_chef.png`, `world_astronaut.png`
- `.../assets_src/concepts/opera_jobs_flat_2026-07-21/cards/`
- Target runtime path: `.../assets/opera/worlds/widgets/`
- Staging: `.../assets_src/concepts/opera_regeneration_2026-08-01/cards/`