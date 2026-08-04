# Widget art concepts at full ambition — 2026-08-03

Owner: see ingredients mixing, pouring, piping bags in full-screen glory.



---

## CONCEPTS: pour-basin-crank

# ART DIRECTION — POUR (4) / BASIN (2) / CRANK (9)
## The "ingredients mixing in a bowl" group

---

# PART 0 — WHAT I LOOKED AT, AND WHAT IS ACTUALLY WRONG

## The bar (what "good" already looks like in this project)

`C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/assets/opera/worlds/props/goal_chef.png` — a three-tier cake, 512², painterly. Every tier has its own crumb texture; the piped rosettes have directional swirl and a specular kick on the outer curl; the cherries have stem, highlight and a cast shadow onto the frosting; the doily plate has a scalloped edge with painted lace holes. Ink contour is a warm dark plum, ~4px, and it *varies* — heavier under the plate, lighter on the lit side.

`goal_magician.png` — a cloud-lamb over a velvet top hat. Velvet reads as velvet (a soft sheen band across the crown, not a flat purple). Sparkles are four-point painted diamonds with pearls between them, not particle dots.

`backdrops/world_chef.png` — 1024×576, and it is dense: a giant mixing bowl with a real whisk, a lit oven with fire inside, tiered cake stands, glass spice jars, a bridge over a syrup canal, piping bags in the foreground corners with actual frosting swirls beside them. There is something to look at in every square inch.

**That is the caliber. Warm upper-left key light, painterly modelling, coral / plum / teal / cream / antique gold, pearl-and-shell motif, no flat fills anywhere.**

## The widgets (what is actually on screen right now)

I read `widget_pour_chef.png`, `widget_pour_chef_fill.png`, `widget_pour_chef_mover.png`, `widget_pour_candymaker.png`, `widget_pour_nursery.png`, `widget_basin_doctor.png`, `widget_crank_chef.png`, `widget_crank_chef_progress.png`, `widget_crank_painter.png`, `widget_crank_racer.png`. All full-panel layers are **1024×608**; all movers are **256×256**.

Precisely what is inadequate:

1. **They are cards, not scenes.** Every backdrop bakes in a rounded white inset panel with a 60px white gutter, a coloured border stroke, and a little coloured ellipse tab floating at the top. The actual subject — a bowl, a sink, a palette — sits alone in the middle of a white void at roughly 45% of the frame. `world_chef.png` has forty painted objects; `widget_pour_chef.png` has one, on a blank card, and the card is *drawn over an already-painted career world*.

2. **`widget_pour_chef_fill.png` is literally a yellow rounded rectangle.** Not stylized — a 320×200 rounded rect of flat `#FFDF95` with a soft white edge glow, and it is positioned on the **outside front of the bowl's belly**, not inside the bowl. When the child holds to pour, a yellow lozenge grows on the outside of a bowl that stays empty. There is no milk, no egg, no level, no liquid. This is the single worst asset in the group.

3. **`widget_pour_candymaker.png` has no syrup in it at all.** It is a smiling wrapped candy sticker, plus two mould plates that are *crudely cropped off at the right edge mid-object*, plus a flat pink rounded rect. The beat is called SYRUP.

4. **`widget_pour_chef_mover.png` is a duplicate of the backdrop's own bowl** — the same bowl-and-whisk sticker at 256². So while she holds to pour, a second identical small bowl fades in on top of the big bowl. Nothing pours. Nothing tips.

5. **`widget_crank_chef_progress.png` is a flat vector ring** — three concentric `#FBD87A` arcs with a notch, on transparency. It is drawn as a full-canvas cross-fade at alpha=progress, so what the child sees is a flat yellow ring materialising over the bowl. `widget_crank_painter.png` and `widget_crank_racer.png` have the same ring *baked into the backdrop*, so a flat yellow/pink circle sits permanently over the palette and the racetrack like a UI mistake.

6. **The art is being squashed.** `opera_career_world_2d.gd:417` sets `surface.size = Vector2(372, 266)` (aspect 1.40) and line 745 sets `Vector2(392, 232)` (aspect 1.69). The backdrop is drawn with `draw_texture_rect(widget_backdrop, panel)` — a stretch, no aspect preservation. 1024×608 art (1.684) shoved into a 1.40 box is compressed ~17% horizontally. Everything round is currently an egg.

---

# PART 1 — THE ENGINE CONTRACT (verbatim from `scripts/opera_gesture_surface.gd`)

Everything below is what the code *actually does*, because the concepts are written to exploit it.

## `pour` — `_draw_widget_layers()` case `"pour"`, lines 502–506
- **backdrop** `widget_pour_<career>.png` → `draw_texture_rect(backdrop, panel)`. Stretched to the panel. Full-bleed, opaque.
- **mover** `widget_pour_<career>_mover.png` → drawn **only while `held`**, as a square of side `138.0` centred at `panel_centre - (0, 18)`. Vanishes the instant the finger lifts.
- **fill** `widget_pour_<career>_fill.png` → `_draw_progress_overlay(overlay, fill, horizontal=false)`.

**The reveal, exactly (lines 451–477):** the code first computes `_ink_bounds()` — it scans every row of the PNG and finds the topmost and bottommost row containing any pixel with `alpha > 0.08`. That painted band is then mapped 0%→100%. The reveal edge sweeps **upward from the bottom of the ink band**, and the visible slab is drawn with `draw_texture_rect_region` at full panel width, pixel-registered to the backdrop.

**Three craft rules fall straight out of that:**
- **(a) The fill PNG must contain ONLY the rising contents.** One stray pixel of steam at the top or a shadow at the bottom stretches the ink band and the level stops short of the rim. The comment at line 417 says exactly this happened before ("the pour saturate at 43% of the hold and then sit frozen — the exact playtest complaint").
- **(b) The cut is a hard horizontal line.** A single painted meniscus ellipse would get sliced in half at every intermediate level. The liquid must be painted so that **every horizontal row already reads as a plausible surface** — i.e. a soft vertically-repeating gloss/foam gradient through the whole body, brightest where the shape narrows. Paint it like a column of liquid, not like a filled shape with a lid.
- **(c) Free animation, exploit it.** Solid objects painted *inside* the liquid body at staggered heights **emerge one at a time** as the cut passes them. This is how we get the owner's "ingredients tumbling in" for zero extra engine cost. Every pour fill layer below has ingredients deliberately stacked at 15% / 35% / 55% / 75% / 92% of the ink band.

## `basin` — case `"basin"`, lines 507–511
- **backdrop** `widget_basin_<career>.png` → full panel.
- **bubbles** `widget_basin_<career>_bubbles.png` → same bottom-up ink-band reveal as pour.
- **shine** `widget_basin_shared_shine.png` → 256², drawn as a 118px sprite at panel centre **only once `fill >= 0.96`**. It is *shared* between doctor and nursery.
- **No mover.** All motion lives in the bubbles reveal. So the water AND the foam AND the hands' lather must all be in that one layer.

## `crank` — case `"crank"`, lines 519–525
- **backdrop** `widget_crank_<career>.png` → full panel.
- **mover** `widget_crank_<career>_mover.png` → `draw_set_transform(centre, previous_angle)`, drawn as a 140×140 square centred on the pivot. `previous_angle` is the **raw pointer angle from panel centre** — this is true 1:1 rotation, the object turns exactly with her finger. Therefore the mover art must be **radially composed with its pivot at the exact image centre**, and must look correct at every one of 360 degrees.
- **progress** `widget_crank_<career>_progress.png` → `draw_texture_rect(overlay, panel, modulate=Color(1,1,1,fill))`. **This is a full-canvas cross-fade, not a wipe.**

**This is the most under-used capability in the whole engine and the crank concepts below are built around it.** The progress layer can be a *complete repaint of the entire scene in its finished state*, pixel-registered to the backdrop. Circling dissolves raw → finished continuously and smoothly across the whole frame. Batter separates → batter smooth. Portal dark → portal blazing. Canvas blank → painting done. That is a real, rich, continuous animation from one static PNG.

**Craft rule:** the progress layer must be a **full opaque repaint at identical composition and camera**, and every region that should NOT change must be painted *identically* in both files. Otherwise the dissolve ghosts instead of transforming.

---

# PART 2 — HOUSE SPEC FOR ALL 15 WIDGETS

- **Canvas: 1024 × 576 for every full-panel layer** (backdrop, fill, bubbles, progress). 16:9 exactly, longest side 1024. This replaces the current 1024×608 and matches a 16:9 panel with zero distortion.
- **Canvas: 512 × 512 for every mover** (up from 256²), pivot dead centre for cranks.
- **Full bleed, fully opaque, edge to edge.** No inset card, no white gutter, no rounded corner, no border stroke, no floating ellipse tab. `_draw()` paints a pale panel and a 4px accent border *underneath* the backdrop (lines 346–347) — an opaque full-bleed backdrop covers both, which is what we want.
- **Composition rule: the hero object occupies 70–85% of the frame and is cropped by at least one edge.** Cropping is what makes it read as a place she is standing in rather than an icon on a card.
- **Every frame carries 6–12 identifiable secondary props** in the corners and margins — the `world_chef.png` density standard. This is the owner's "expand this level of detail".
- Palette: coral `#E4837C`, plum `#7E5A96`, teal `#5FB3AE`, cream `#F5E3C8`, antique gold `#C99A4E`, ink `#3A2450`. Warm key from upper-left, cool bounce from lower-right.
- Line: painterly varying contour, 3–6px, warm dark plum; **never** a uniform vector stroke.
- No flat fills, no gradients-as-UI, no translucent rectangles, no rings drawn over the art.

## Engine changes this direction requires (small, and they are the difference between "card" and "full-screen glory")

| File | Line | Now | Should be | Why |
|---|---|---|---|---|
| `scripts/opera_career_world_2d.gd` | 416–417 | `pos (24,78)`, `size (372,266)` | `pos (64,40)`, `size (1152,648)` | 16:9, near-full-screen, no squash |
| `scripts/opera_career_world_2d.gd` | 744–745 | `pos (24,70)`, `size (392,232)` | same as above | same |
| `scripts/opera_gesture_surface.gd` | 504 | pour mover side `138.0` | `~360.0` | the jug must be a jug, not a thumbnail |
| `scripts/opera_gesture_surface.gd` | 522 | crank mover `Rect2(-70,-70,140,140)` | `Rect2(-180,-180,360,360)` | the whisk must fill the bowl |
| `scripts/opera_gesture_surface.gd` | 511 | basin shine side `118.0` | `~300.0` | success burst should be a burst |
| `scripts/opera_gesture_surface.gd` | 131 | shared basin shine | optional `"%s_shine.png"` per career | one line; lets doctor and nursery differ |

Everything else below plugs into the code **exactly as it stands today**.

---

# PART 3 — THE POUR BEATS (4)

> Layer contract per beat: `widget_pour_<career>.png` 1024×576 opaque painted backdrop · `widget_pour_<career>_mover.png` 512² painted sprite, held-only, appears at centre · `widget_pour_<career>_fill.png` 1024×576 painted layer, **contents only**, revealed bottom-up across its ink band.

---

## 1. `pour_chef` — CHEF / POUR
### *The one the owner named. Get this one right and the direction is proven.*

**THE SCENE.** A cream-glazed mixing bowl so big it runs off the bottom edge of the frame — the coral-and-antique-gold banded belly filling the lower two-thirds, a fat pearl-and-shell boss on its front, the wooden footed base just clipped by the frame's bottom. Its mouth is a wide ellipse crossing the frame at 38% height, tilted toward us so **we are looking down into it** and can see the whole inner wall. The interior is painted in cool shadow with one crescent of light down the far side, so an empty bowl reads unmistakably EMPTY.

Behind it, a warm marble counter running to a bakery window: a torn paper flour sack tipped on its side with a white drift spilling toward camera and a brass scoop half-buried in it; three cracked brown-speckled eggshells, one still rocking; a spill of caster sugar with a measuring spoon lying in it; a glass jug of milk with condensation; a split vanilla pod showing its black seed paste; a half lemon and a fine zester; a folded coral-striped cloth; a stick of butter with the paper peeled back. Flour motes hang in the light beam from the upper left.

**WHAT MOVES AND HOW.**
- `widget_pour_chef_mover.png` — a heavy cream-glazed **milk jug**, gold-banded, tipped ~52° to the left with its lip aimed down into the bowl mouth. An unbroken glassy milk stream falls from the lip, widening slightly, and **runs off the bottom edge of the mover square** so it visually continues into the bowl below. Two fingers of a small hand grip the handle. It appears only while she holds — the pouring is literally her finger being down.
- `widget_pour_chef_fill.png` — the batter body **only**: a column of batter filling the bowl's inner volume, painted with a soft vertically-repeating cream-gold gloss so any horizontal cut reads as a surface. Suspended inside it at staggered heights: two egg yolks low, sugar crystals and a butter curl at a third, a third yolk and a flour swirl at mid, vanilla seeds and a cocoa marble high, a slick of gloss near the rim.

**THE MOMENT OF PROGRESS.**
- **10%** — a shallow pool of milk in the bottom of the bowl with two egg yolks bobbing in it like little suns and one bubble.
- **50%** — level halfway up the inner wall; the cut has passed the sugar and butter, so crystals and a butter curl are now visible; the third yolk has just broken the surface; flour is folding in as a cream streak.
- **100%** — batter to the rim, warm caramel-cream, glossy, vanilla seeds speckled across the top, the whole bowl heavy and full.

**THE SUCCESS IMAGE.** The bowl brim-full of silky batter, a fat gold gloss band riding the surface, three yolks floating like suns, a soft puff of flour rising, a scatter of four-point sparkles and pearls in the upper corners.

**INGREDIENTS/CONTENTS.** Whole milk, three egg yolks, cracked brown-speckled shells, caster sugar crystals, sifted flour and a flour cloud, a curl of butter, split vanilla pod and its seeds, lemon zest shreds, one cocoa marble.

**FILES.**
| File | Size | Type |
|---|---|---|
| `widget_pour_chef.png` | 1024×576 | painted backdrop, opaque full-bleed |
| `widget_pour_chef_mover.png` | 512×512 | painted sprite, held-only; stream must exit the bottom edge |
| `widget_pour_chef_fill.png` | 1024×576 | painted layer, contents only, ink band = empty-line → rim-line |

---

## 2. `pour_candymaker` — CANDYMAKER / SYRUP

**THE SCENE.** A fluted scallop-shell candy mould, cream ceramic with a brass rim, as wide as the frame and cropped at both sides, seen three-quarter from above so the child looks straight into the shell hollow. Its ridged flutes catch the light. Heat shimmer wobbles the air above it.

Behind and around: a copper syrup pan on a brass trivet, still ticking with heat, a wooden spoon across it with a hardened amber drip; four squat glass jars of coloured sugar — raspberry, mint, violet, lemon — each with a little brass scoop; a brass thermometer with a red bead standing in a clip; a marble slab dusted with icing sugar; three cooled candy ribbons curled like shavings in raspberry and mint; a hooked scraper; a bundle of mint-striped twist wrappers; a single dropped candy pearl on the tiles.

**WHAT MOVES AND HOW.**
- `widget_pour_candymaker_mover.png` — a long-handled **copper ladle**, tipped, a thick heavy rope of molten amber sugar falling from its lip with a slow lazy fold and a bright specular line down the rope's spine. The ladle glows faintly from the heat. Exits the bottom edge.
- `widget_pour_candymaker_fill.png` — the molten sugar body in the shell hollow, translucent amber with an internal glow, painted with vertically-repeating gloss. Suspended at staggered heights: two boil bubbles low, a raspberry colour ribbon at a third, a mint ribbon at mid, a violet ribbon high, a fine sugar-crystal sparkle band near the brim.

**THE MOMENT OF PROGRESS.**
- **10%** — a shallow amber puddle glowing at the bottom of the shell, two lazy boil bubbles rising.
- **50%** — half full; raspberry and mint ribbons now marbling visibly through the amber, one bubble breaking the surface.
- **100%** — mould brim-full, a mirror-gloss surface, all three colour ribbons drawn out into a complete spiral marble, sugar sparkle across the top.

**THE SUCCESS IMAGE.** The full shell of jewel-marbled syrup, mirror bright, tiny sugar crystals sparking off the surface, the heat shimmer at its strongest, gold light bouncing off the brass rim.

**INGREDIENTS/CONTENTS.** Molten amber sugar, raspberry / mint / violet colour ribbons, sugar crystals, boil bubbles, heat shimmer, a hardened drip, a stray candy pearl.

**FILES.** `widget_pour_candymaker.png` 1024×576 backdrop · `widget_pour_candymaker_mover.png` 512² held-only sprite · `widget_pour_candymaker_fill.png` 1024×576 contents-only reveal.
*Content reference for the mould flutes and the colour jars:* `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/opera_job_candy_maker_gameplay_mold_plates.png` and `..._gameplay_scoop_and_tongs.png`.

---

## 3. `pour_painter` — PAINTER / FILL

**THE SCENE.** A big footed ceramic paint pot filling the lower two-thirds and cropped by the bottom edge — cream glaze with a plum band, one chip out of the rim, three dried plum drips running down the outside. Its mouth is a wide ellipse at 38% height, tipped toward us so we see the inner wall and the dark empty bottom.

Around it, a paint-spattered canvas drop cloth stiff with old colour: a jar bristling with brushes of five sizes; three smaller pots in coral, teal and cream with crusted rims; a wooden palette with worked mounds of colour and a thumb hole; a rinse jar of murky violet water with a brush standing in it; a crumpled rag; a tube of pigment rolled and squeezed; the easel's wooden leg at the right edge; spatters everywhere, some fresh and wet, some dry and cracked.

**WHAT MOVES AND HOW.**
- `widget_pour_painter_mover.png` — a squat stoneware **pigment jug**, tipped, pouring a heavy opaque plum stream that coils where it lands. Paint clings to the jug's lip in a fat bead about to drop. Exits the bottom edge.
- `widget_pour_painter_fill.png` — the paint body inside the pot: dense plum with a satin (not glassy) surface treatment, vertically repeating. Suspended at staggered heights: a coral pigment pearl not yet dissolved low, a marbled turn at a third, a stray bristle at mid, a teal swirl high, a satin skin near the rim.

**THE MOMENT OF PROGRESS.**
- **10%** — a shallow plum pool, the pigment still separating into visible swirl, one undissolved coral pearl.
- **50%** — half up the pot; the marbled turn and a floating bristle now visible; the plum reading dense and opaque.
- **100%** — pot full to the rim, saturated plum with a satin skin, one teal swirl still unstirred on top.

**THE SUCCESS IMAGE.** Full pot, satin surface, a big round brush laid across the rim already loaded with plum and dripping one bead, sparkles.

**INGREDIENTS/CONTENTS.** Plum pigment, coral and teal swirls, undissolved pigment granules, a floating bristle, wet drips down the outer glaze, spatter.

**FILES.** `widget_pour_painter.png` 1024×576 · `widget_pour_painter_mover.png` 512² · `widget_pour_painter_fill.png` 1024×576.
*Content reference:* `opera_job_painter_gameplay_plum_paint_pot.png`, `..._gameplay_rinse_cup.png`, `..._gameplay_palette.png`.

---

## 4. `pour_nursery` — NURSERY / FEED

**Framing note.** The engine reveal fills bottom-up, so the beat must be *filling the bottle for the baby*, not draining it into the baby. This reads instantly to a 4-year-old ("make the milk for the baby"), uses the mechanic honestly, and gives a warm success image. The current asset — a swaddled baby sticker on a white card with a flat mint rounded rect on its tummy — communicates none of this.

**THE SCENE.** A nursery counter at bottle height, soft peach and mint light. Centre: a tall glass nursery bottle, cropped top and bottom, running from 12% to 92% of frame height, seen dead-on so the milk level is perfectly readable — coral silicone teat, brass screw collar, and **three raised measuring rings on the glass at 25%, 55% and 88%** which act as an honest ruler for progress.

Left: a swaddled baby in a woven moses basket lined with mint muslin, eyes wide and bright, one hand up and reaching toward the bottle, mouth in an expectant O. Right: a warming jug on a shell trivet with steam curling off it; a stack of folded bibs; a wind-up shell rattle; a yellow rubber duck on its side; a soft knitted lamb; a folded hooded towel. A window behind throws a soft bar of light across the counter.

**WHAT MOVES AND HOW.**
- `widget_pour_nursery_mover.png` — a small enamel **warming jug**, tipped, a soft creamy stream falling into the bottle's open neck, a wisp of steam off the jug's rim. Exits the bottom edge.
- `widget_pour_nursery_fill.png` — the milk column inside the glass **only**: warm opaque cream with a vertically-repeating soft froth gradient. Suspended at staggered heights: one bubble low, a fine froth band at each of the three measuring-ring heights so passing a ring is a visible event, and a thick cream froth crown near the top.

**THE MOMENT OF PROGRESS.**
- **10%** — milk just over the first ring, a single bubble climbing.
- **50%** — level at the middle ring, a soft cream froth head sitting on the surface, the glass fogging slightly.
- **100%** — milk at the top ring, warm and full, a proper froth crown, one drop running down the outside of the glass.

**THE SUCCESS IMAGE.** The full bottle glowing warm, the baby's arms **both** up now, hands open, a heart-shaped puff of steam rising between bottle and baby, sparkles and tiny hearts.

**INGREDIENTS/CONTENTS.** Warm milk, cream froth, rising bubbles, three brass measuring rings, condensation on the glass, a run-off drop, steam.

**FILES.** `widget_pour_nursery.png` 1024×576 · `widget_pour_nursery_mover.png` 512² · `widget_pour_nursery_fill.png` 1024×576.
*Note:* `visual_context == "pour_nursery"` is asserted by `scripts/probe_opera_nursery.gd:88` ("feeding uses a bottle hold tableau") — this concept keeps that contract.

---

# PART 4 — THE BASIN BEATS (2)

> Layer contract per beat: `widget_basin_<career>.png` 1024×576 opaque backdrop · `widget_basin_<career>_bubbles.png` 1024×576 revealed bottom-up · `widget_basin_shared_shine.png` 512² success stamp at ≥96%. **No mover** — all motion lives in the bubbles reveal, so the water, the foam and the lather must all be painted into that one layer.

---

## 5. `basin_doctor` — DOCTOR / WASH

**THE SCENE.** A scalloped stone clinic basin so wide it is cropped by both side edges, its fluted bowl filling the lower 60% of the frame, water-darkened and gleaming. A tall brass swan-neck tap rises from the back rim and runs an unbroken glassy ribbon of water down into the bowl, catching a hard white highlight along its edge. **Two small cupped hands come in from the bottom of frame, palms up, held under the stream** — the child's own hands, from her point of view. This is the hero.

Around: a pump bottle of shell-shaped soap with a bead on the nozzle; a folded teal towel on a brass rail with a pearl finial; a mirror behind throwing a bar of daylight across the wet stone; a coral starfish patient peeking over the basin's far edge with a curious face; a brass tray of rounded-tip instruments beyond; wet rings and splash droplets on the stone counter; the clinic's arched window blurred in the mirror.

**WHAT MOVES AND HOW.**
- `widget_basin_doctor_bubbles.png` — one painted layer containing, bottom to top: the rising water level in the basin, then the lather climbing the hands, then the foam meringue above the wrists. Painted with a vertically-repeating foam texture so every cut height reads as a foam line. Suspended at staggered heights: loose bubbles at the wrists low, a foam cap over the drain at a third, rainbow-sheened bubbles at mid, a big soap bubble with a full iridescent film high, a foam crown at the top.
- `widget_basin_shared_shine.png` — redesigned as a proper **sparkle-and-squeak burst**: a painted starburst of four-point gold diamonds, pearls and small radiating light spokes with a warm centre bloom. Career-neutral, so it works for both beats. (If the one-line engine change at `opera_gesture_surface.gd:131` is taken, a per-career `widget_basin_doctor_shine.png` could instead be a gleaming pair of clean hands with a squeak spark.)

**THE MOMENT OF PROGRESS.**
- **10%** — a thin skim of water across the basin floor, a handful of loose bubbles collecting at the wrists.
- **50%** — foam covering both hands to the knuckles, basin half full, a foam cap riding over the drain, rainbow sheen appearing on the larger bubbles.
- **100%** — a full meringue of lather up both wrists and over the fingers, basin brim-full, the biggest bubble carrying a complete iridescent film.

**THE SUCCESS IMAGE.** Hands lifted clear of the water, clean and gleaming with a squeak spark at the fingertip, foam crown still riding the wrists, the starfish giving a tiny approving wave over the rim, sparkle burst.

**INGREDIENTS/CONTENTS.** Running water ribbon, soap lather, iridescent bubbles at four different sizes, droplets on wet stone, the tap's specular glint, shell soap with a bead on the nozzle.

**FILES.** `widget_basin_doctor.png` 1024×576 backdrop · `widget_basin_doctor_bubbles.png` 1024×576 contents-only reveal · `widget_basin_shared_shine.png` 512² (shared, redesign).
*Content reference:* `opera_job_doctor_stage_states_handwashing_basin.png`, `opera_job_doctor_gameplay_starfish_calm.png`.

---

## 6. `basin_nursery` — NURSERY / WASH HANDS

**THE SCENE.** Not a sink — a **baby bath**. A wide oval enamel tub in cream with a peach rolled rim, cropped by both side edges, filling the lower 65% of the frame, warm water in it throwing wobbling light onto the tiles behind. Sitting up in the middle, filling the centre of the frame, a round-cheeked baby with wet hair, a foam hat already slid over one ear, both hands out and laughing.

Around: a mint flannel draped over the rim, dripping; a yellow rubber duck and two floating shell toys with painted faces; a bar of soap on a scallop dish with a bead of water on it; a folded hooded towel on a low stool with a lamb ear on the hood; a rinsing jug; a wooden bath toy boat; wet tiles behind with a low warm sun bar and a run of condensation; a splash arc already frozen at the tub's edge.

**WHAT MOVES AND HOW.**
- `widget_basin_nursery_bubbles.png` — the bath foam rising up the tub and around the baby's body: soft white-pink foam with a vertically-repeating cauliflower texture so every cut is a plausible foam line. Suspended at staggered heights: bubbles round the tummy low, the duck riding the foam at a third, a foam beard forming at mid, a foam epaulette on each shoulder high, a peaked foam crown at the top.
- `widget_basin_shared_shine.png` — the same sparkle burst as above, at ≥96%.

**THE MOMENT OF PROGRESS.**
- **10%** — a scatter of bubbles round the baby's tummy, one on the nose.
- **50%** — foam to the chest, a foam beard forming, the duck riding visibly higher than it was.
- **100%** — foam up to the chin with a proper peaked crown, only a delighted face and two clapping hands above the white.

**THE SUCCESS IMAGE.** The baby enthroned in a mountain of bubbles, both hands mid-clap with foam flying off them, the duck perched on the summit, a burst of sparkles and iridescent bubbles rising out of frame.

**INGREDIENTS/CONTENTS.** Warm bath water, soap foam at three densities, iridescent bubbles, rubber duck, two shell toys, a bar of soap, a splash arc, wet hair curl.

**FILES.** `widget_basin_nursery.png` 1024×576 · `widget_basin_nursery_bubbles.png` 1024×576 · `widget_basin_shared_shine.png` 512² (shared).
*Note:* `scripts/probe_opera_nursery.gd:63` asserts `visual_context == "basin_nursery"` at phase 1 — contract preserved.

---

# PART 5 — THE CRANK BEATS (9)

> Layer contract per beat: `widget_crank_<career>.png` 1024×576 opaque backdrop (the RAW state) · `widget_crank_<career>_mover.png` 512² **radially composed, pivot at exact image centre**, rotates 1:1 with the finger · `widget_crank_<career>_progress.png` 1024×576 **full opaque repaint of the same composition in the FINISHED state**, cross-faded in at alpha=progress. Backdrop and progress must be pixel-registered; regions that shouldn't change must be painted identically in both.

---

## 7. `crank_chef` — CHEF / STIR
### *The owner's "ingredients mixing in a bowl together", literally.*

**THE SCENE.** Looking **straight down** into a wide cream-glazed bowl that fills 85% of the frame, its rim a great circle almost touching all four edges and cropped at top and bottom. The inner glaze catches a crescent of light down the right side. Inside, sitting in **distinct, unmixed islands**: a pale mound of sifted flour with the sieve's mesh marks still pressed into it; a cluster of three intact glossy egg yolks, each with its own highlight; a heap of caster sugar with sharp crystal sparkle; a soft slab of butter with a knife mark in it; a puddle of milk with a skin on it; a drift of cocoa dust on one side; a scatter of black vanilla seeds; a curl of lemon zest.

At the corners, outside the bowl: a cracked shell, a folded coral-striped cloth, a brass measuring cup, a sieve on its side with flour still in it.

**WHAT MOVES AND HOW.**
- `widget_crank_chef_mover.png` — a balloon **whisk seen from directly above**: a rosette of eight steel wires radiating from a centred wooden handle cap, the wires foreshortened into a perfect radial star, batter clinging to the lower ones, a specular kick on each wire. Pivot is the handle cap at the image centre, so it turns cleanly through all 360°.
- `widget_crank_chef_progress.png` — the same bowl, same camera, same corner props painted identically — but the interior is now **one uniform silky caramel batter** with a slow spiral ribbon, a gloss highlight sweeping the surface, the sides scraped clean, a light dusting of flour on the rim. The dissolve from separated islands to smooth batter is the whole animation.

**THE MOMENT OF PROGRESS.**
- **10%** — the islands' edges begin to smear; the first tan streaks bleed between flour and yolk.
- **50%** — a half-marbled swirl: cocoa and cream drawn out into visible spiral arms, lumps still riding the surface, the yolks broken and streaking.
- **100%** — one uniform silky caramel batter, spiral ribbon, glossy, sides clean.

**THE SUCCESS IMAGE.** Perfect batter with a thick ribbon falling off the lifted whisk and folding back on itself, a puff of flour caught in the light, a scatter of gold sparkles.

**INGREDIENTS/CONTENTS.** Sifted flour, three egg yolks, caster sugar, butter slab, milk, cocoa dust, vanilla seeds, lemon zest — **each individually identifiable at 0% and fully gone into one batter at 100%.**

**FILES.** `widget_crank_chef.png` 1024×576 (raw, separated) · `widget_crank_chef_mover.png` 512² (top-down whisk, radial) · `widget_crank_chef_progress.png` 1024×576 (finished batter, pixel-registered).
*Content reference:* `opera_job_pastry_chef_gameplay_bowl_empty.png`, `..._gameplay_bowl_stirring.png`, `..._gameplay_whisk.png`, `..._stage_states_stir_effect.png`.

---

## 8. `crank_ballerina` — BALLERINA / TWIRL

**THE SCENE.** Looking straight down onto a lacquered **stage rose** — a circular parquet floor of pale wood inlaid with a pearl-and-shell compass rose, filling the frame and cropped on all four sides. Dead centre, a pair of satin slippers, ribbon-laced, toes pointed together on the rose's heart. Around the rim: rose petals scattered on the boards, one fallen coral ribbon coiled, chalk rosin dust, the warm ring of footlight glows at the very edge of the frame, and the hard shadow of the raised curtain across one corner.

**WHAT MOVES AND HOW.**
- `widget_crank_ballerina_mover.png` — the dancer **from above**: a disc of layered coral tulle skirt with the pointed slippers and a small pair of raised arms at the exact centre, so rotating the sprite rotates the whole dancer around her own axis. The tulle's outer hem is painted with a slight motion softening.
- `widget_crank_ballerina_progress.png` — the same floor, same props, but blazing: a complete luminous spiral traced onto the boards by the toe, a full ring of airborne petals lifted off the floor, ribbon streamers making a halo, the footlights at full.

**THE MOMENT OF PROGRESS.**
- **10%** — a faint arc of light where the toe has passed, two petals lifted an inch off the boards.
- **50%** — a half-drawn luminous spiral, petals airborne in a partial ring, one ribbon streaming.
- **100%** — a complete radiant spiral of light on the floor, a full ring of airborne petals, streamers haloing the dancer, footlights blazing.

**THE SUCCESS IMAGE.** The spiral held and glowing gold on the boards, petals frozen mid-air in a perfect ring, a burst of pearls and four-point sparkles.

**INGREDIENTS/CONTENTS.** Satin slippers with laced ribbons, coral tulle, rose petals, chalk rosin, pearl-and-shell floor inlay, footlight glow, ribbon streamers.

**FILES.** `widget_crank_ballerina.png` · `widget_crank_ballerina_mover.png` 512² · `widget_crank_ballerina_progress.png`.
*Content reference:* `opera_job_ballerina_gameplay_twirl_ribbon.png`, `..._gameplay_sequence_complete.png`.

---

## 9. `crank_candymaker` — CANDYMAKER / WRAP

**THE SCENE.** A single enormous plum gumdrop at frame centre — glossy, translucent, with a dusting of sugar bloom on its shoulders and light passing right through its edge — nested in a brass wrapping turntable ringed with tiny brass pegs. The turntable fills 70% of the frame.

Around it: a roll of mint-striped waxed paper half unrolled with a torn edge; a reel of coral ribbon; a dish of brass twist-clips; round-tipped scissors; **three already-wrapped bonbons with their ends twisted into crisp fans**, standing as proof of what finished looks like; a scatter of loose sugar; a stick of red sealing wax and a shell seal; the marble slab's edge.

**WHAT MOVES AND HOW.**
- `widget_crank_candymaker_mover.png` — the **wrapping cradle from above**: a brass ring with two waxed-paper flaps standing up on either side and the candy nested at its exact centre. Rotating it winds the paper around the sweet.
- `widget_crank_candymaker_progress.png` — the same turntable and props, but the candy is now a **fully wrapped bonbon**: paper drawn tight over the body, both ends twisted into crisp fans, a coral ribbon knotted at one end, a red wax shell seal pressed on.

**THE MOMENT OF PROGRESS.**
- **10%** — one paper flap has come up over the candy's near side, a single crease.
- **50%** — paper wrapped right around the body, ends still loose and open, the mint stripes now following the candy's curve.
- **100%** — wrapped tight, both ends twisted into fans, ribbon knotted, wax seal on.

**THE SUCCESS IMAGE.** The finished bonbon lifted slightly off the turntable with a gleam running across the paper, sugar sparkles, the three earlier bonbons now joined by a fourth.

**INGREDIENTS/CONTENTS.** Plum gumdrop with sugar bloom, mint-striped waxed paper, coral ribbon, brass twist-clips, red sealing wax, shell seal, loose sugar.

**FILES.** `widget_crank_candymaker.png` · `widget_crank_candymaker_mover.png` 512² · `widget_crank_candymaker_progress.png`.
*Content reference:* `opera_job_candy_maker_gameplay_plum_wrapped_candy.png`, `..._gameplay_coral_round_candy.png`.

---

## 10. `crank_doctor` — DOCTOR / CAST

**THE SCENE.** Close and tender. A starfish patient's arm — a plump coral limb — lies across a folded mint blanket on a padded exam pillow, running diagonally through the lower half of the frame and cropped at the left edge. The limb's centre is the frame's centre. The starfish's face is at the top edge, brave-but-worried, one eye watching.

Around: a rolling tray with a shallow bowl of water going cloudy; a roll of plaster bandage half unwound with the tail trailing; round-tipped scissors; a stethoscope coiled with a pearl chest-piece; a jar of lollipops; a hand-drawn sticker sheet of gold stars with two already peeled off; a pencil; a folded mint towel; the clinic's arched window blurred behind.

**WHAT MOVES AND HOW.**
- `widget_crank_doctor_mover.png` — the **bandage roll seen end-on**: a spiral of cream gauze with a coral thread marker running through it so the rotation is unmistakably legible, a loose tail of gauze coming off one edge. Perfect radial subject.
- `widget_crank_doctor_progress.png` — same limb, same tray, same props, but the limb now wears a **smooth complete white cast** decorated with painted gold stars, a coral heart signature and one peel-off star sticker; the water bowl is cloudier; the bandage roll on the tray is smaller; and the starfish's face at the top edge is now **happy**.

**THE MOMENT OF PROGRESS.**
- **10%** — two turns of gauze around the wrist end, the tail still long.
- **50%** — the limb half-cased, gauze spiralling with visible overlap, the loose tail shorter.
- **100%** — a smooth complete cast, drawn-on stars, coral heart signature, gold star sticker.

**THE SUCCESS IMAGE.** The starfish holding its decorated cast up proudly toward camera, face beaming, a gold "care complete" glow and sparkles.

**INGREDIENTS/CONTENTS.** Plaster gauze roll, coral thread marker, bowl of water, round-tipped scissors, stethoscope, lollipops, star sticker sheet, painted stars, coral heart signature.

**FILES.** `widget_crank_doctor.png` · `widget_crank_doctor_mover.png` 512² · `widget_crank_doctor_progress.png`.
*Content reference:* `opera_job_doctor_gameplay_bandage_roll.png`, `..._gameplay_bandage_wrap.png`, `..._gameplay_starfish_worried.png` → `..._gameplay_starfish_happy.png`, `..._gameplay_care_complete_medallion.png`.

---

## 11. `crank_magician` — MAGICIAN / PORTAL

**THE SCENE.** A vast top hat mouth seen from **directly above** — its black star-flecked interior a deep oval filling the middle of the frame, its purple velvet brim with a coral band and a gold-set pearl shell clasp forming a ring that runs almost to the frame's edge. The velvet reads as velvet: a soft sheen band sweeping across the nap.

On the brim and the cloth beneath: a wand with pearl tips laid across one edge; a fan of playing cards face-down with shell backs; three white dove feathers; a violet silk scarf half-pulled from under the hat; two linked brass rings; a scatter of moon-and-star confetti; the hard shadow of the hat on a dark velvet cloth.

**WHAT MOVES AND HOW.**
- `widget_crank_magician_mover.png` — a **radial rune ring**: a circle of raised gold sigils, moons and stars on a faint violet disc, unlit. Circling literally winds the portal. Perfect radial subject and the most legible "turning" read in the set.
- `widget_crank_magician_progress.png` — the same hat, same brim props, but the interior is now a **blazing violet vortex**: a whirlpool of light spiralling down into the throat, gold light spilling up over the brim onto the velvet, every rune lit, sparkles streaming upward, and the first white fluff of the cloud-lamb rising out of it.

**THE MOMENT OF PROGRESS.**
- **10%** — two runes light amber, a faint violet glow at the hat's throat.
- **50%** — the whole rune ring lit, a clear whirlpool of violet light, sparkles streaming up, a hint of white fluff below the surface.
- **100%** — a full spiral vortex, the portal wide and blazing, gold light spilling over the brim.

**THE SUCCESS IMAGE.** **The cloud-lamb from `goal_magician.png` bursting up out of the portal** with a ring of sparkles and pearls — a direct visual callback to the goal prop, so the beat and the prize are the same picture.

**INGREDIENTS/CONTENTS.** Purple velvet, coral hat band, gold-set pearl shell clasp, gold runes and sigils, violet vortex light, moon-and-star confetti, dove feathers, playing cards, brass linking rings, the cloud-lamb.

**FILES.** `widget_crank_magician.png` · `widget_crank_magician_mover.png` 512² · `widget_crank_magician_progress.png`.
*Content reference:* `assets/opera/worlds/props/goal_magician.png` (the lamb and hat, matched exactly), `opera_job_magician_gameplay_hat_open.png`, `..._gameplay_successful_reveal.png`.

---

## 12. `crank_painter` — PAINTER / STROKES

**THE SCENE.** The canvas, huge and square-on, filling the frame and cropped left and right — a primed off-white ground with visible linen weave, the wooden stretcher bar showing at two corners, one thumbtack. On it, a faint pencil under-drawing of a sunrise over water: a horizon line, a circle for the sun, a few gull ticks.

Around the edges: a laden palette at the bottom-left with fat worked mounds of coral, plum, teal and cream and a dirty mixing patch; three brushes of different widths; a rag with worked colour; the rinse jar of murky violet water; a run of drips along the bottom edge of the canvas; the easel's wood at the sides; a single wet spatter on the floor.

**WHAT MOVES AND HOW.**
- `widget_crank_painter_mover.png` — a loaded round brush **seen from above**: the brass ferrule and a splayed rosette of coral-loaded bristles with a fat wet blob at the centre, radially composed so spinning it reads as working the paint.
- `widget_crank_painter_progress.png` — the same canvas, same easel, same palette position — but the canvas now carries a **complete painterly sunrise**: swirled coral-to-plum sky, teal sea with gold light on the water, a full sun disc with bloom, three clouds, one bird, a lit horizon. And critically: **the palette's colour mounds are visibly depleted** and the rinse jar is dirtier. The world reacts, not just the canvas.

**THE MOMENT OF PROGRESS.**
- **10%** — a few coral swirls in the sky corner, one wet drag mark, the pencil lines still showing through.
- **50%** — sky fully swirled coral-to-plum, sea blocked in teal, sun still a bare disc, edges unresolved.
- **100%** — a complete sunrise, gold on the water, clouds and a bird, paint standing wet and thick.

**THE SUCCESS IMAGE.** The finished sunrise gleaming wet, a gold frame edge glinting in at one corner as if the picture is already being hung, sparkles.

**INGREDIENTS/CONTENTS.** Coral / plum / teal / cream paint mounds, wet brush blob, drips, canvas linen weave, pencil under-drawing, rinse water, rag.

**FILES.** `widget_crank_painter.png` · `widget_crank_painter_mover.png` 512² · `widget_crank_painter_progress.png`.
*Content reference:* `opera_job_painter_gameplay_canvas_blank.png` → `..._gameplay_canvas_finished.png` / `..._gameplay_framed_sunrise.png` — these two cards are literally the before/after this cross-fade needs.

---

## 13. `crank_astronaut` — ASTRONAUT / VALVE

**THE SCENE.** The face of a great brass-and-copper pressure valve filling the frame: a riveted bulkhead plate, weathered and sea-worn, with a many-spoked wheel at the centre and a pearl-set shell boss at its hub. Condensation beads on the cold metal; a green algae bloom in one rivet seam.

Around: two round glass pressure gauges with red needles resting at zero and pearl bezels; a bundle of copper pipes running off the top and right edges with visible rivet seams and a repair patch; a warning plate stamped with a pictogram (an arrow and a bubble — **no text**); a coiled air hose on a hook; three indicator shells, dark; the reef-blue glow of a porthole at the lower-left corner with a fish passing.

**WHAT MOVES AND HOW.**
- `widget_crank_astronaut_mover.png` — the **valve wheel itself**: six brass spokes, a worn grip rim, a pearl-and-shell hub. Radially perfect, and the single most obvious "turn me" object in the whole game.
- `widget_crank_astronaut_progress.png` — same plate, same pipes, same porthole — but the system is **alive**: both gauge needles swung round into the green, warm light running along every pipe seam, all three indicator shells lit gold, a plume of bubbles blasting from the outlet, the condensation flashed off, the whole plate lit warm.

**THE MOMENT OF PROGRESS.**
- **10%** — one indicator shell lights amber, the first gauge needle lifts off zero, a single bubble escapes the outlet.
- **50%** — both needles at half, pipes glowing along their seams, a steady stream of bubbles.
- **100%** — needles pinned in the green, every indicator lit, a full roaring bubble plume, warm light flooding the plate.

**THE SUCCESS IMAGE.** The whole bulkhead lit gold-green, a geyser of bubbles rising out of frame, a ring of sparkles round the pearl hub.

**INGREDIENTS/CONTENTS.** Brass spoked wheel, pearl-and-shell hub, rivets, two glass gauges with red needles, copper pipes with rivet seams and a repair patch, condensation, indicator shells, bubble plume, a passing fish in the porthole.

**FILES.** `widget_crank_astronaut.png` · `widget_crank_astronaut_mover.png` 512² · `widget_crank_astronaut_progress.png`.
*Content reference:* `opera_job_astronaut_engineer_gameplay_valve_wheel.png`, `..._gameplay_valve_spin_bubbles.png`, `..._gameplay_bubble_tank.png`.

---

## 14. `crank_racer` — RACER / LAP TWO

**THE SCENE.** Driver's-eye view. A pearl-rimmed three-spoke **steering wheel** at the centre of the frame with a shell boss, cropped at the bottom by the dash — and beyond it the reef racetrack rushing away: coral-and-cream striped kerbs, a chequered banner strung over the track ahead, a grandstand of packed shell-seats with a cheering crowd, two rival cars ahead on the racing line, and a **lap board on a post showing two shell slots with one filled**.

Dash detail at the bottom: a brass rev dial, a water-temperature gauge, a lucky pearl charm swinging from the mirror, a smear of coral dust across the windscreen edge.

**WHAT MOVES AND HOW.**
- `widget_crank_racer_mover.png` — the **steering wheel face-on**: pearl rim, three spokes, shell boss centre, small hands gripping at ten-and-two. Radially perfect and totally unambiguous.
- `widget_crank_racer_progress.png` — same track, same grandstand, same dash — but transformed: **the two rivals have slid backward and are now behind**, the lap board's second shell is filled, the crowd is on its feet with arms up, speed streaks blur the kerbs, the chequered flag is out and waving, and a bubble boost trail runs off the rear.

**THE MOMENT OF PROGRESS.**
- **10%** — one rival passed, the first speed streaks appearing at the kerbs, board still on one shell.
- **50%** — both rivals behind, streaks strong, the board's second shell half-filled, the crowd rising.
- **100%** — clear track ahead, chequered flag waving, board full, the finish arch in sight, boost trail streaming.

**THE SUCCESS IMAGE.** The chequered flag waving over an empty track, the lap board full, the finish arch overhead, a confetti burst of bubbles and pearls.

**INGREDIENTS/CONTENTS.** Pearl steering wheel with shell boss, coral-striped kerbs, chequered banner and flag, two rival cars, lap board with shell slots, grandstand crowd, rev dial, lucky pearl charm, speed streaks, bubble boost trail.

**FILES.** `widget_crank_racer.png` · `widget_crank_racer_mover.png` 512² · `widget_crank_racer_progress.png`.
*Note:* this replaces the current asset, which is a rainbow-arc track segment with a flat pink ring drawn on top of it and reads as nothing.

---

## 15. `crank_popstar` — POPSTAR / ENCORE

**THE SCENE.** Looking straight down onto a **turntable** on a brass deck: a great pearl-vinyl disc filling most of the frame, its grooves catching an oil-slick iridescence, a coral label at the exact centre with a shell motif. The tone arm swings in from the right with a pearl counterweight and a tiny diamond stylus resting in the groove.

Around the deck: a rack of shell records in their sleeves; a glowing volume dial; a pair of headphones with pearl cups; a scattering of confetti already on the deck from the main set; a coiled cable; and beyond the deck's edge, the dark auditorium — a haze of raised shell-lights in the crowd, unlit.

**WHAT MOVES AND HOW.**
- `widget_crank_popstar_mover.png` — the **record itself**: the pearl-vinyl disc with its coral centre label and a single bright groove-glint so the spin is unmistakable at any angle. Perfectly radial.
- `widget_crank_popstar_progress.png` — the same deck, same tone arm, same crowd — but the encore has landed: the record's grooves lit into a **blazing neon spiral**, three spotlight beams sweeping in across the deck, a downpour of confetti and streamers, and the crowd's shell-lights all raised and burning.

**THE MOMENT OF PROGRESS.**
- **10%** — the record's inner grooves light, one spotlight comes on, the first confetti falls.
- **50%** — half the groove spiral lit, three spotlights sweeping, confetti falling steadily, the crowd's lights coming up.
- **100%** — the whole spiral blazing, every light on, a confetti storm, streamers, the crowd a solid sea of light.

**THE SUCCESS IMAGE.** The disc a complete neon spiral, confetti and streamers filling the frame, a warm gold curtain-call glow flooding in from the frame's edge.

**INGREDIENTS/CONTENTS.** Pearl-vinyl grooves with iridescence, coral centre label, brass tone arm with pearl counterweight and diamond stylus, shell records in sleeves, volume dial, headphones, confetti, streamers, spotlight beams, crowd shell-lights.

**FILES.** `widget_crank_popstar.png` · `widget_crank_popstar_mover.png` 512² · `widget_crank_popstar_progress.png`.
*Content reference:* `opera_job_pop_star_gameplay_microphone_finale.png`, `..._gameplay_dance_complete.png`, `..._gameplay_speaker.png`.

---

# PART 6 — DELIVERABLE MANIFEST (44 files)

All under `assets/opera/worlds/widgets/`.

**POUR — 12 files.** For each of `chef`, `candymaker`, `painter`, `nursery`:
`widget_pour_<c>.png` 1024×576 painted backdrop · `widget_pour_<c>_mover.png` 512×512 held-only pouring vessel, stream exits bottom edge · `widget_pour_<c>_fill.png` 1024×576 contents-only, ink band = empty-line → rim-line, ingredients stacked at 15/35/55/75/92%.

**BASIN — 5 files.**
`widget_basin_doctor.png` · `widget_basin_doctor_bubbles.png` · `widget_basin_nursery.png` · `widget_basin_nursery_bubbles.png` (all 1024×576) · `widget_basin_shared_shine.png` 512×512 painted sparkle burst.

**CRANK — 27 files.** For each of `chef`, `ballerina`, `candymaker`, `doctor`, `magician`, `painter`, `astronaut`, `racer`, `popstar`:
`widget_crank_<c>.png` 1024×576 raw state · `widget_crank_<c>_mover.png` 512×512 radial, pivot at exact image centre, valid at all 360° · `widget_crank_<c>_progress.png` 1024×576 finished state, full opaque repaint, pixel-registered to the backdrop.

**No frame sequences required anywhere in this group.** Every beat animates from painted layers the engine already reveals, rotates or cross-fades.

---

# PART 7 — THE THREE THINGS THAT MUST BE TRUE ON REVIEW

1. **No cards.** Open any of the 15 backdrops and it should look like a still from a film about the job, cropped by the frame edges — not an object floating on a white panel. If there is a rounded rectangle anywhere in the file, it is wrong.
2. **Count the nouns.** Every backdrop must have at least eight identifiable things in it. `widget_pour_chef.png` currently has one. `world_chef.png` has forty. Land between.
3. **Watch the fill rise with the game paused at 10 / 50 / 100.** At 10% something is visibly in the vessel. At 50% something is in it that was NOT there at 10% — a new ingredient the cut has just uncovered. At 100% it is full to the rim and glorious. If any of the three is ambiguous, the fill layer's ink band is wrong.

---

## Files referenced (absolute paths)
- Quality bar: `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/assets/opera/worlds/props/goal_chef.png`, `.../props/goal_magician.png`, `.../backdrops/world_chef.png`
- Current widgets audited: `.../assets/opera/worlds/widgets/widget_pour_chef.png`, `widget_pour_chef_fill.png`, `widget_pour_chef_mover.png`, `widget_pour_candymaker.png`, `widget_pour_nursery.png`, `widget_basin_doctor.png`, `widget_crank_chef.png`, `widget_crank_chef_progress.png`, `widget_crank_painter.png`, `widget_crank_racer.png`
- Engine contract: `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_gesture_surface.gd` (layer loading lines 108–152, layer drawing lines 486–546, ink-band reveal lines 417–477)
- Panel sizing: `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_career_world_2d.gd` lines 416–417 and 744–745
- Content reference cards: `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/assets_src/concepts/opera_jobs_flat_2026-07-21/cards/`

---

## CONCEPTS: trace-target-push

# ART DIRECTION — TRACE (6) · TARGET (8) · PUSH (4)
### Full-screen scene concepts for the opera career-world minigame widgets

---

## PART 0 — WHAT I LOOKED AT, AND THE MEASURED DIAGNOSIS

**The quality bar (read in full):**
- `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/assets/opera/worlds/props/goal_chef.png` — the three-tier cake. Layered sponge with visible crumb, piped pearl beading between tiers, six alternating cream/rose/plum rosettes, two stemmed cherries, a scalloped rose cake-stand with pearl inlays. Painterly, warm rim-light, deep navy line, gold accents.
- `.../props/goal_magician.png` — the cloud-lamb levitating out of a plum top hat, pearl-and-shell hat band, orbiting sparkles and bubbles.
- `.../backdrops/world_chef.png` — an entire undersea pastry district: a giant mixing bowl with a whisk standing in it, spice jars on a rack, a lit oven arch, tiered cake stands, a bell jar, a piping bag with three finished rosettes on the lower-right ledge. **That backdrop already contains more baking than every chef widget combined.**

**The current widgets in my three templates (read: `widget_trace_chef`, `widget_trace_chef_lit`, `widget_trace_painter`, `widget_trace_magician`, `widget_trace_doctor`, `widget_target_chef`, `widget_target_chef_mover`, `widget_target_chef_mark`, `widget_target_painter`, `widget_target_boxer`, `widget_target_boxer_success`, `widget_push_farmer`, `widget_push_farmer_mover`, `widget_push_racer`, `widget_push_nursery`, `widget_push_shared_arrow_lr`).**

### The seven precise failures

1. **The job occupies 6% of the tablet screen.** `scripts/opera_career_world_2d.gd:406-407` — the task card is `420 x 430` at `(430,160)`. `:744-745` — the gesture surface inside it is `392 x 232`. On a 1280x720 base that is **6.3% of the screen**. The 1024x608 art is then downsampled 2.6x. Nothing painted at that size can read as "glory."
2. **Every backdrop bakes in a frosted white card and a slice of its own world.** Look at `widget_trace_chef.png`: a translucent near-white rounded panel covers ~90% of the canvas, and behind its edges you can see a blurred crop of `world_chef.png`. That white wash is why everything reads pale and flat. (The engine *also* draws a white wash + border underneath at `opera_gesture_surface.gd:346-347`, so it is doubled.)
3. **The interactive affordance is raw vector primitives.** The trace guide is a **flat slate-grey polyline** — the same identical polyline in chef, painter, doctor and magician. The push runway is a **yellow stadium outline**. The target zone is a **thin cream rounded rectangle**. The push direction cue is a **flat yellow arrow** (`widget_push_shared_arrow_lr.png`). None of these are painted; none belong to the world.
4. **The guide path does not correspond to the prop.** In `widget_trace_magician.png` the grey polyline crosses *over* the rope at a different angle. In `widget_trace_painter.png` it runs *across a blank canvas* with no drawing on it. In `widget_trace_chef.png` it cuts *through* the piping bag. The child is being asked to trace a line that has nothing to do with the picture.
5. **The progressive layer is a coloured stick.** `widget_trace_chef_lit.png` is the same polyline in flat `#FCD98A` — no frosting, no material, no ridges. For the headline PIPE beat, the thing that grows as she drags is **a yellow stick**.
6. **Movers are duplicate crops of their own backdrop, with matte fringing.** `widget_push_farmer_mover.png` is the identical pig already painted into `widget_push_farmer.png`. `widget_push_racer.png` shows a helmet crop with a visible white halo around the wheels. `widget_trace_doctor.png` is a bandage roll floating with **no patient** — there is nothing to bandage.
7. **Completion has no image.** Only one `_success` file exists in all three templates: `widget_target_boxer_success.png` — and it is **three flat concentric yellow rings**. The other seven target beats and all four push beats simply stop.

### The engine contract I am writing against (verified in `scripts/opera_gesture_surface.gd`)

| template | layers loaded | how they behave |
|---|---|---|
| **trace** (`:139`) | `<prefix>.png` + `<prefix>_lit.png` | `_lit` is wiped **left→right** with a hard vertical edge — source `x: 0 → w·fill`, dest `0 → surface.x·fill` (`:451-459`, `:526-528`). |
| **push** (`:140-144`) | `<prefix>.png` + `<prefix>_mover.png` + shared arrow | mover drawn at `center + swipe_dir · fill · 42px`, size `136px`; arrow at `+92px`, alpha 0.72 (`:529-532`). `swipe_dir` is DOWN for boxer/nursery, RIGHT for farmer/racer (`opera_career_world_2d.gd:705-711`). |
| **target** (`:145-148`) | `<prefix>.png` + `_mover.png` + `_mark.png` + `_success.png` | `_mover` hovers at the roaming `tap_point` (142px); `_mark` stamps at every landed tap (76px); `_success` draws full-canvas at `fill ≥ 0.96` (`:533-538`). `tap_point` roams `center ± 0.30w, ± 0.26h` (`:248-253`). |

**The left→right trace wipe is the single most valuable free animation in this codebase.** A painted ribbon laid out chronologically across the canvas *extrudes itself* as she drags. That is exactly what piping is. It is currently being spent on a yellow stick.

---

## PART 1 — UNIVERSAL RULES FOR THESE 18 BEATS

**R1 — Canvas.** Backdrops and success layers: **1024 x 576** (16:9, ≤1024 longest side, upscales 1.25x to a 1280x720 stage). Movers: **512 x 512** (power of two). Marks: **256 x 256**. Trace `_lit`: **1024 x 576**, matching its backdrop pixel-for-pixel.

**R2 — Full bleed, opaque, no card.** Backdrops and `_success` layers are **fully opaque edge to edge**. No baked white panel, no baked rounded frame, no crop of the career world showing through. The scene *is* the frame. (Engine: delete the white wash at `:346-347` when a backdrop exists.)

**R3 — Extreme close-up.** These are not dioramas on a shelf. The subject is **cropped by the frame edges** — the cake runs off both sides, the piping bag runs off the top-left corner, the whale's belly fills the width. Reference framing: `goal_chef.png` fills 92% of its own canvas.

**R4 — The guide is diegetic.** Kill the slate polyline everywhere. Replace it with a **chalk-ghost of the `_lit` layer painted into the backdrop at ~22% opacity in the identical shape** — powdered-sugar dotting on the cake, a faint pencil contour on the canvas, a dim un-lit footprint on the floor. She traces the ghost; the real thing paints in over it. This is the affordance *and* the beauty in one move.

**R5 — Movers are never duplicates.** If a thing is the mover, it does **not** appear in the backdrop. The backdrop instead paints its **absence**: the empty pen, the hollow in the pillow, the empty gold setting, the crack in the hull.

**R6 — Clean alpha.** Movers, marks and `_lit` layers must be painted on transparency from the start — not cut out of a flat card. The `widget_push_racer_mover` white fringe is disqualifying at full-screen scale.

**R7 — Palette / material.** Cream `#F2E3C6`, coral-rose `#E2857F`, plum `#6B4A86`, teal `#4F8F96`, gold `#C9A25A`, deep-navy line `#1B2A4A`. Underwater physics: no smoke or steam — **bubble plumes**; no dust — **shimmer motes**; liquids are dense and luminous and pour slowly. Warm gold footlight from below-left, cool teal ambient from above.

**R8 — Population.** Every scene carries **at least six named, identifiable objects** beyond the hero prop. This is the owner's ask made checkable: "I want to see ingredients." Sparse = fail.

---

# PART 2 — TRACE (6 beats)
### `widget_trace_<career>.png` + `widget_trace_<career>_lit.png` — drag left→right, `_lit` extrudes

**How to compose a `_lit` layer.** The wipe edge is a straight vertical cut sweeping right. Therefore:
- Lay every element out in **left-to-right chronological order** — the thing that should appear first sits at the far left.
- **Long, roughly-horizontal ribbon forms are ideal**: the vertical cut across a ribbon reads as the fresh, still-emerging end. Use ribbons as the spine of every trace lit layer.
- A **round element gets sliced vertically**. Keep round elements small and frequent (beads, pearls, sparks) so the slice passes in under 3% of the drag — or make them large and deliberately place them at the far right, where "popping in over the last 5%" reads as a finale.
- **The expression trick:** paint a *changed* version of something (a happier face, a smaller bandage roll) into the `_lit` layer at the x-position where it should change. When the wipe passes that x, the new version covers the old. Free state change, zero engine cost.

---

## 1. CHEF — **PIPE** ★ THE HEADLINE

**THE SCENE.** Extreme close-up, the piping bag in full glory. A cream canvas piping bag occupies the **entire left third and rises off the top-left corner of the frame** — so fat with buttercream you can read the pressure bulge in the fabric and the pale stress-sheen where it stretches. Its twisted neck is bound with a plum satin ribbon tied in a two-loop bow, one tail curling loose. Two small cream-gloved mermaid hands grip it: the upper hand squeezing the twist, knuckles dimpled; the lower hand steadying the collar, one finger extended along the barrel. The **brass star nozzle** sits at roughly x=300, y=250, angled down-right, its six-point star mouth catching a hard gold highlight, a single fat bead of rose buttercream already welling at the tip with a wet specular dot on it.

Below and behind, filling the bottom two-thirds and running off **both** frame edges: the top face and upper shoulder of a huge vanilla cake — open crumb, a scatter of loose crumbs on the marble, a faint gold ring where the previous pass of beading was laid. Behind and softly out of focus: the marble counter's chamfered edge, a shallow copper bowl heaped with stemmed cherries, a scallop shell of sanding sugar catching the light, a spatula resting across a jar, a swagged coral curtain edge and two warm gold footlight bulbs. Bubbles drift up the right side.

Painted into the backdrop across the cake's surface: the **chalk-ghost** — a pale, chalky, 22%-opacity version of the exact ribbon shape, like a dusting of icing sugar sifted through a stencil.

**WHAT MOVES AND HOW.**
- `widget_trace_chef_lit.png` (1024x576, painted, alpha) — **the rosette ribbon**. A thick rope of rose buttercream with **five distinct ridges** running lengthwise (star-tip signature), a cream-white highlight along the top ridge and a plum-shadow undercut along the bottom. Ink band spans x=300 (at the nozzle mouth) → x=1000. It runs in three shallow swags; at each crest it curls into a **rosette** — a tight spiral seen three-quarters, the ridges wrapping into the centre. Sugar pearls and a dusting of sanding sugar scatter along it, more densely as it goes. At x≈940 the ribbon rears into a **tall crowning swirl** capped with a candied cherry, its stem arcing left, a bright specular dot on the cherry's shoulder.
- The cut edge of the ribbon at the wipe boundary is painted as a **slightly domed, glossier terminal** for the first 40px of ink — so wherever the wipe stops, it looks like frosting still emerging, not a sliced sausage.
- No mover needed: the bag is baked at the left and the ribbon streams out of the nozzle. **Zero engine change.**

**THE MOMENT OF PROGRESS.**
- **10%** — the bead at the nozzle has slumped forward into two inches of ridged rope. She can see frosting has *come out of the nozzle*.
- **50%** — the ribbon has crossed the cake's centre and completed its first rosette curl; sugar pearls have begun to appear along it; the ridges are unmistakable.
- **100%** — the full swagged border, three rosettes, the crowning swirl and the cherry, sanding sugar glittering along the whole run.

**THE SUCCESS IMAGE.** The fully-revealed `_lit` layer *is* the held picture, so it must be gorgeous at rest: a complete piped border on a real cake, cherry-crowned, matching the beading language of `goal_chef.png` so the child reads "I made the cake's decoration."

**INGREDIENTS / CONTENTS.** Rose buttercream, cream buttercream highlight, candied cherry with stem, sugar pearls, sanding sugar, vanilla cake crumb, loose crumbs, cherries in a copper bowl, plum satin ribbon, brass star nozzle, spatula.

**FILES.**
| file | size | type |
|---|---|---|
| `widget_trace_chef.png` | 1024x576 | painted backdrop, opaque, bag + cake + counter + chalk-ghost |
| `widget_trace_chef_lit.png` | 1024x576 | painted overlay, alpha, ink band x=300→1000 |

---

## 2. DETECTIVE — **TRAIL**

**THE SCENE.** Top-down onto the prop-library floor. Dark polished planks with a warm grain, a searchlight wedge falling from the upper left. Strewn across it: a coiled velvet rope, an overturned plum hatbox with its lid rocked to one side, a spilled trunk with a cream petticoat frothing out, a dropped opera glove. A **huge brass-and-glass magnifier** occupies the left quarter — barrel running off the frame edge, gloved fingers wrapped round it, the lens a pale convex disc that visibly *magnifies* the plank grain beneath it and throws a caustic ring of light onto the floor. The chalk-ghost trail runs away from under the lens as a line of faint grey prints.

**WHAT MOVES AND HOW.** `widget_trace_detective_lit.png` — **the glowing trail**. Alternating left/right **webbed mer-footprints** in luminous turquoise, each with a soft outward glow and a wet gleam, marching in a curving line from under the lens to the right edge. Dropped evidence punctuates it: a torn plum ribbon at 20%, a single pearl with a bright highlight at 40%, a spray of sequins at 60%, a tuft of cream feather at 80%, and at 92% the **corner of the stolen pearl tiara** protruding from under a curtain hem, gold blazing, three sparkles orbiting it.

**THE MOMENT OF PROGRESS.** **10%** — two prints have lit under the lens. **50%** — the trail is halfway across the floor, the pearl found and gleaming. **100%** — the trail terminates at the tiara, fully lit, unmistakably the thing she was looking for.

**THE SUCCESS IMAGE.** The tiara revealed at the end of a glowing turquoise trail of her own making, evidence laid out along it like a museum case.

**INGREDIENTS / CONTENTS.** Webbed footprints, pearl, torn plum ribbon, sequins, cream feather, pearl tiara, hatbox, velvet rope, opera glove, magnifier.

**FILES.** `widget_trace_detective.png` (1024x576 painted backdrop) · `widget_trace_detective_lit.png` (1024x576 painted overlay, ink band x=180→980).

---

## 3. BALLERINA — **RIBBON**

**THE SCENE.** Stage level, camera low in the wing. Lower-left foreground, large and slightly out of focus: Roshan's pointed foot in a coral satin slipper, ribbons crossed and tied at the ankle. Upper-left: her hand — small, poised, fingers curved — gripping a **pearl-capped ribbon wand** with a gold ferrule. The stage floor is honey-toned wood, waxed, with a bright spotlight pool and the wand's reflection in it. Behind: teal and coral wing curtains with gold rope ties, the mirror-ball rig throwing a scatter of light-dots across the floor and curtain, a music box on a plinth at the right, and a bouquet already waiting on the boards.

**WHAT MOVES AND HOW.** `widget_trace_ballerina_lit.png` — **the satin streamer**. A broad coral-to-cream ribbon looping across the frame in three big S-curves, painted with real satin behaviour: bright sheen bands along the outer face of each curve, deep plum shadow where it twists and shows its underside, a crisp fold at each reversal. Pearl-light sparks trail along the trailing edge. At the far right the ribbon flourishes into a tight **spiral** that frames a burst of coral petals and a shower of light-dots.

**THE MOMENT OF PROGRESS.** **10%** — a short bright flick of satin out of the wand tip. **50%** — two full loops aloft, the light catching a fold, sparks beginning. **100%** — the whole ribbon in the air, ending in a spiral with petals and a shower of pearl light.

**THE SUCCESS IMAGE.** The ribbon frozen at the top of its arc, the stage floor sprinkled with petals, the bouquet lit — a curtain-call photograph.

**INGREDIENTS / CONTENTS.** Coral satin ribbon, pearl-capped wand, satin slipper with ties, coral petals, mirror-ball light-dots, wing curtains, music box, bouquet.

**FILES.** `widget_trace_ballerina.png` · `widget_trace_ballerina_lit.png` (both 1024x576, ink band x=150→990).

---

## 4. DOCTOR — **BANDAGE**

**THE SCENE.** *(Fixes the worst gap in the set: there is currently no patient.)* Close on a cream exam cushion. A **starfish patient** lies across the centre-right of the frame, plump and rounded with a soft dimpled texture, one arm extended toward the left and toward camera. On that arm: a small pink scrape with a bead of shine. Its face is at the upper right — big worried eyes, a wobbly mouth, one arm-tip curled anxiously. At the **left**, held in a small cream-gloved hand, a **roll of cream bandage**, half-unwound, the loose end already tucked under the arm; the roll's spiral edge and the woven texture read clearly. Around them: an enamel tray with a shell thermometer and a coiled stethoscope, a jar of turquoise salve with a gleam on the glass, a folded towel, a paper cup of cotton, a lamp arm coming in from the top left. Faint chalk-ghost spiral bands run along the starfish's arm.

**WHAT MOVES AND HOW.** `widget_trace_doctor_lit.png` — **the wrap**. Cream gauze spiralling around the arm in overlapping diagonal bands, each with a soft shadow where it laps the one before and a slight wrinkle at the inside of the curve, so the wrapping reads as three-dimensional. Two extra elements exploit the wipe:
- At x≈140 (just past 10%), a **smaller bandage roll** is painted in the `_lit` layer over the backdrop's full roll — as the wipe passes, the roll visibly shrinks because she has used it.
- At x≈500 (50%), a **relieved, half-smiling starfish face** is painted over the worried one. The patient cheers up exactly halfway.
At the far right: a neat **bow** with a small scallop pin, and three heart-shaped bubbles rising.

**THE MOMENT OF PROGRESS.** **10%** — one lap of gauze on, the roll gets smaller. **50%** — the arm half-wrapped and the starfish stops looking worried. **100%** — fully wrapped, bow tied, starfish beaming, hearts rising.

**THE SUCCESS IMAGE.** A neatly-bandaged, visibly happier patient. The emotional payoff is the face, not the gauze.

**INGREDIENTS / CONTENTS.** Cream gauze, bandage roll, scallop pin, starfish patient, shell thermometer, stethoscope, turquoise salve jar, folded towel, cotton cup, heart bubbles.

**FILES.** `widget_trace_doctor.png` · `widget_trace_doctor_lit.png` (both 1024x576, ink band x=110→980). Note for the painter: the roll and face swaps must sit at exactly x≈140 and x≈500.

---

## 5. MAGICIAN — **ROPE**

**THE SCENE.** A plum velvet trick table runs across the bottom third, nap catching the light, a fringed gold edge. A single hard spotlight pool sits centre. Behind: a deep indigo curtain with drifting violet motes and the dim shape of the rolling mirror. At the **left**, a plum-gloved mermaid hand holds a **coil of pearl-white rope**, the visible cut end frayed into individual glowing strands. Standing on the velvet at x≈380 and x≈720: two **floating brass rings**, edge-on, each unlit and dull. At the **right**, the top hat — coral band, pearl-and-shell clasp, brim tipped toward camera so its dark mouth is a waiting oval. The chalk-ghost of the rope's path lies across the velvet.

**WHAT MOVES AND HOW.** `widget_trace_magician_lit.png` — **the rope**. A thick, three-strand twisted cord in pearl white with visible strand spiral and a soft violet shimmer that intensifies left-to-right; a scatter of four-point violet sparks along it. Painted at x≈380 and x≈720 in the `_lit` layer: the same brass rings but **lit gold and haloed** — so each ring ignites as the rope threads it. At the right the rope plunges into the hat's mouth in a starburst of violet sparks, and the tips of two **bunny-fish ears** and a pink nose emerge over the brim.

**THE MOMENT OF PROGRESS.** **10%** — a hand-span of twisted rope out of the coil, one spark. **50%** — through the first ring, which now blazes gold. **100%** — through both rings, into the hat, sparks bursting, the bunny-fish appearing.

**THE SUCCESS IMAGE.** Two lit gold rings threaded, sparks, and a creature arriving out of the hat — the trick *worked*. Deliberately rhymes with `goal_magician.png`.

**INGREDIENTS / CONTENTS.** Pearl rope, brass rings, top hat with coral band and shell clasp, bunny-fish, violet sparks, plum velvet, gold fringe, mirror.

**FILES.** `widget_trace_magician.png` · `widget_trace_magician_lit.png` (both 1024x576, ink band x=170→960).

---

## 6. PAINTER — **SKETCH**

**THE SCENE.** A large cream canvas on a shell-crested easel fills roughly 85% of the frame, cropped by the top and both sides — you can read the canvas **weave and tooth**, a faint warm ground, and one soft shadow from the stretcher bar. Only slivers of studio survive at the margins: bottom-left, a wooden palette with wet blobs of coral, plum, teal and cream and a smear where colours were mixed; bottom-right, jars of cloudy turquoise rinse water, a rag draped over a rung, brushes bristle-up in a shell cup; top-right, a corner of the gallery wall and a hanging lamp. At the **left**, a small hand holds a **charcoal-and-pearl drawing stick**, its tip touching the canvas, with a tiny puff of charcoal dust and a smudge of black on the fingertips. A faint pencil chalk-ghost of the drawing is already on the canvas.

**WHAT MOVES AND HOW.** `widget_trace_painter_lit.png` — **the drawing**. A single confident charcoal contour with real pressure variation (thin at the start, swelling on the down-strokes, breaking where the stick skipped over the tooth) that draws a **leaping dolphin**: nose, brow, eye, the long arch of the back, the dorsal fin, the narrowing flank, the tail flick. Beneath it, a curl of wave in three strokes, then five quick hatch marks for spray. At the far right the line thickens into a looping signature flourish, and a **coral paint spatter** flicks across the corner in full colour.

**THE MOMENT OF PROGRESS.** **10%** — a nose and an eye. **50%** — the whole arched back and the dorsal fin: it is now **obviously an animal**, which is the strongest "is it working?" in the whole trace set. **100%** — the complete leaping dolphin with wave, spray, flourish and a splash of colour.

**THE SUCCESS IMAGE.** A finished drawing on a real canvas in a real studio — a picture a 4-year-old will recognise as *a dolphin she drew*.

**INGREDIENTS / CONTENTS.** Charcoal stick, charcoal dust, coral/plum/teal/cream paint blobs, palette, rinse jars, rag, brushes, canvas weave, coral spatter.

**FILES.** `widget_trace_painter.png` · `widget_trace_painter_lit.png` (both 1024x576, ink band x=160→980).

---

# PART 3 — TARGET (8 beats)
### `widget_target_<career>.png` + `_mover.png` + `_mark.png` + `_success.png`

**Role discipline — this is currently inverted and must be fixed.** Today `widget_target_chef_mover.png` is a whole cake-and-plates crop and `widget_target_chef_mark.png` is a **navy dot with a glow**. Correct roles:

- **`_mover` (512x512)** — the **item to be placed**, cradled in a soft pearl-light halo with two or three orbiting sparkles, floating and tilted as if just picked up. It hovers over the next spot. It says *"put this, here."*
- **`_mark` (256x256)** — the **same item, landed and settled**: seated into the surface, deforming what it lands on, with a contact shadow and a small starburst of arrival. It says *"that one's done."*
- **`_success` (1024x576, opaque)** — the finished tableau, held. **Seven of these do not currently exist and the eighth is three flat yellow rings.** This is the largest single gap in the set.

**Backdrop rule:** the backdrop paints the thing **unfinished** — the bare cake, the empty cones, the hollow gold settings, the cracks. Never the finished object (as `widget_target_boxer.png` does today, which leaves nothing to earn).

---

## 1. CHEF — **TOP**

**THE SCENE.** A three-tier cake — the same cake as `goal_chef.png` but **naked**: sponge layers in cream/coral/plum with visible crumb, the pearl beading between tiers already piped, but the **top tier bare**, with only the faint rings of cream where toppings will sit. It fills the frame from the bottom edge to two-thirds up and is cropped left and right by the frame. It stands on the scalloped rose cake-stand. Behind, on a marble counter: a copper bowl of stemmed cherries, a dish of chocolate curls, a shell of gold dragées, a piping bag laid down with a dab of rose frosting still at the nozzle, a sifter, a jar of sanding sugar. Warm oven glow from the right, coral curtain and two footlights behind, bubbles rising.

**WHAT MOVES AND HOW.** `_mover`: a **plump glossy cherry**, deep red with a bright white specular crescent, a green stem curling, cradled in a pearl-light ring with three orbiting sparkles. `_mark`: the same cherry **seated into a cream rosette that squashes and puffs up around its base**, with a soft shadow and four tiny sugar sparks.

**THE MOMENT OF PROGRESS.** **10%** — one cherry on the top tier, everything else bare. **50%** — half the ring placed; the cake now unmistakably reads *being decorated*. **100%** — the ring complete, then the success tableau.

**THE SUCCESS IMAGE.** `widget_target_chef_success.png` — the cake fully crowned: a complete ring of alternating cream/rose/plum rosettes each capped with a cherry, gold dragées scattered across the top, a dusting of sanding sugar mid-fall, three tiny pennant flags on picks, a shower of sugar sparks, footlights blazing. **Silhouette-matched to `goal_chef.png`** so she recognises it as the prize.

**INGREDIENTS / CONTENTS.** Cherries, cream rosettes, chocolate curls, gold dragées, sanding sugar, sponge crumb, pearl beading, pennant flags.

**FILES.** `widget_target_chef.png` 1024x576 · `widget_target_chef_mover.png` 512x512 · `widget_target_chef_mark.png` 256x256 · `widget_target_chef_success.png` 1024x576.

---

## 2. CANDYMAKER — **SHARE**

**THE SCENE.** The parade. A candy cart at the left with a coral-and-cream striped awning, brass wheels, a bell, and glass hoppers heaped with sweets. Along the **bottom edge**, cropped at the chest, a row of upturned delighted faces looking straight up at the camera: two sea-urchin children, a seal pup with its flippers out, a small crab holding a claw aloft, a shy jellyfish at the end. Each holds an **empty striped paper cone**. Behind: the parade arch strung with bunting and shell lanterns, confetti bubbles drifting, a distant crowd blur.

**WHAT MOVES AND HOW.** `_mover`: a **fistful of wrapped candies** — a coral spiral, a teal shell, a cream heart, a plum bow — with twisted cellophane ends catching the light, in a pearl halo. `_mark`: a **cone brimming over** with candies spilling at the rim, one candy tumbling, a heart-puff rising above it, and the child's hands closed happily round it.

**THE MOMENT OF PROGRESS.** **10%** — one cone filled, one delighted face. **50%** — half the row served; the child can *count* who has candy and who is still waiting. **100%** — every cone full.

**THE SUCCESS IMAGE.** `widget_target_candymaker_success.png` — every cone full and raised, all five faces cheering with eyes shut, candies raining down through the frame, confetti bubbles, the cart's awning lanterns lit, the bell mid-swing.

**INGREDIENTS / CONTENTS.** Spiral candy, shell candy, heart candy, bow candy, twisted cellophane wrappers, striped paper cones, glass hoppers, bunting, shell lanterns, confetti.

**FILES.** `widget_target_candymaker.png` · `_mover.png` · `_mark.png` · `_success.png`.

---

## 3. DOCTOR — **X-RAY**

**THE SCENE.** A big friendly whale-shark patient lies across the whole frame, side-on, cropped by both edges — spotted grey-blue back, broad cream belly toward camera, a sleepy half-lidded eye and a gentle smile at the left. A wheeled examination lamp leans in from the top. A trolley at the right holds a gold retrieval tray, tongs and a folded cloth. The belly is painted as a **soft translucent window**, and through it, faint and grey-green like objects underwater, you can just make out **five swallowed things**: a teacup, a boot, a starfish, a comb, a brass key.

**WHAT MOVES AND HOW.** `_mover`: a **shell-framed X-ray paddle** — a scallop-shaped brass frame around a glowing turquoise glass disc, a bright caustic ring thrown below it, held in a halo. Wherever it hovers, the child understands *look here*. `_mark`: the **found object, now fully coloured and outlined in warm gold**, with a bright "found!" starburst and three sparkles — vivid against the grey ghosts of the ones not yet found.

**THE MOMENT OF PROGRESS.** **10%** — one object blazes into full colour among four grey ghosts. **50%** — three colour, two grey; the difference is unmissable. **100%** — all five in colour.

**THE SUCCESS IMAGE.** `widget_target_doctor_success.png` — the five objects lifted **out** and arranged neatly on the gold tray beside the whale, each with a little gleam; the whale now wide awake and beaming with a happy tail-flick blurring the frame edge; a rising column of heart bubbles; the lamp swung back.

**INGREDIENTS / CONTENTS.** Teacup, boot, starfish, comb, brass key, gold tray, tongs, shell X-ray paddle, exam lamp, heart bubbles.

**FILES.** `widget_target_doctor.png` · `_mover.png` · `_mark.png` · `_success.png`.

---

## 4. FARMER — **PICNIC**

**THE SCENE.** A coral-and-cream checkered picnic blanket in perspective, filling the lower two-thirds and running off both frame edges. It is **empty** — just a few crumbs, one folded-back corner, a crease where it was carried. At the left, a wicker hamper stands open, straw and a checked cloth spilling out, a stack of enamel plates and a bundle of napkins inside. Around the blanket's edge sit **five piggies**, each in a different pose of hopeful anticipation: one with its snout lifted sniffing, one with a paw on the blanket edge, one lying flat with its chin on its trotters, one sitting bolt upright, one small one half-hidden behind a hay bale. Behind: fence, barn, orchard, a low warm sunset and drifting glow-plankton.

**WHAT MOVES AND HOW.** `_mover`: a **laden serving board** — a golden pumpkin pie with a lattice top and one slice cut out, a bowl of glossy berries beside it, a sprig of herb — held in a pearl halo, tilted. `_mark`: a **placed dish**, seated on the blanket with a soft shadow and a dent in the cloth, steam-bubbles rising, one berry escaped and rolling.

**THE MOMENT OF PROGRESS.** **10%** — one dish down, one piggy already leaning in. **50%** — the blanket half-laid; the spread has begun to look like a meal. **100%** — laid end to end.

**THE SUCCESS IMAGE.** `widget_target_farmer_success.png` — the blanket fully laid with pie, berries, a stack of corn cobs, a milk jug, a cheese wheel and a bowl of apples; every piggy tucked in with a napkin at its neck, one on its back with its trotters in the air and a leaf on its belly; glow-plankton rising; the sunset gone deep coral behind the barn.

**INGREDIENTS / CONTENTS.** Pumpkin pie, berries, corn cobs, milk jug, cheese wheel, apples, napkins, enamel plates, wicker hamper, straw, hay bale, piggies.

**FILES.** `widget_target_farmer.png` · `_mover.png` · `_mark.png` · `_success.png`.

---

## 5. BOXER — **BELT**

**Reframe required.** `widget_target_boxer.png` currently shows the belt **already finished** — there is nothing to earn, and `_success` is three flat yellow rings. New premise: **she sets the pearls into the champion's belt.**

**THE SCENE.** Ring-corner framing: teal ropes running across the top and down the right, a padded corner post with its coral wrap and a hanging towel, the ring canvas below with the shell logo half-visible. Centre frame, large and in three-quarter view on a **plum velvet cushion** under a hard spotlight: the championship belt — broad teal leather with brass rivets and stitching you can count, a big gold scallop medallion, two square side-plates. Its **five pearl settings are empty** — hollow gold claw-mounts with visible prongs and dark sockets — and the strap is dull and unbuffed. At the right, a jeweller's scallop tray holds a heap of loose pearls, a shell scoop and a soft cloth. Behind: audience pennants and round lamps softly out of focus, imps peeking under the bottom rope at the very bottom edge.

**WHAT MOVES AND HOW.** `_mover`: a **fat luminous pearl** in a shell scoop, glowing from within with a bright specular and a soft pink sub-surface bloom, in a halo. `_mark`: a **pearl set into its claw-mount**, prongs bent over it, gold gleaming, a four-point starburst on its crown.

**THE MOMENT OF PROGRESS.** **10%** — one setting filled, four still dark and hollow. **50%** — three set; the medallion has started to blaze. **100%** — all five, the whole belt alight.

**THE SUCCESS IMAGE.** `widget_target_boxer_success.png` **(replaces the flat yellow rings)** — the finished belt held **aloft**, strap streaming down and out of frame, gold blazing under the spotlight, pearls throwing star-flares, a burst of bubble confetti, pennants snapping, round lamps all lit, the shell trophy on its podium behind, and the imps at the bottom edge bowing with their arms out.

**INGREDIENTS / CONTENTS.** Pearls, gold claw settings, scallop medallion, teal leather, brass rivets, shell scoop, jeweller's tray, polishing cloth, plum velvet cushion, pennants, imps.

**FILES.** `widget_target_boxer.png` (rebuild) · `_mover.png` · `_mark.png` · `_success.png` (replace).

---

## 6. PAINTER — **SPLAT**

**THE SCENE.** A huge blank cream canvas fills nearly the whole frame on a low easel, cropped top and sides, its weave and warm ground clearly readable, one stretcher-bar shadow. Along the bottom edge, in sharp foreground: a row of **open paint pots** — coral, plum, teal, cream — each with paint domed above the rim and a drip down the side, brushes standing in two of them; a rinse cup of cloudy turquoise water with a brush leaning in it; a paint-stained rag; a squeezed tube. A drop cloth beneath, already dotted with old spatters. Faint pale chalk-ghost circles mark where splats should land.

**WHAT MOVES AND HOW.** `_mover`: a **fat loaded brush** — bristles bulging with coral paint, a heavy bead hanging off the tip about to fall, the ferrule crusted with dried colour — tilted as if cocked for a flick, in a halo. `_mark`: a genuinely **painterly splat** — irregular lobed edge, four or five radiating tendrils of different lengths, three flung satellite droplets, a glossy wet highlight across the middle and one drip beginning to run down from the bottom lobe.

**THE MOMENT OF PROGRESS.** **10%** — one bold splat on an intimidating blank canvas: instantly satisfying. **50%** — five splats, the canvas visibly *hers*. **100%** — the canvas covered.

**THE SUCCESS IMAGE.** `widget_target_painter_success.png` — the canvas as a joyful abstract of overlapping splats in all four colours, drips running to the bottom edge, a few flung arcs across the top — now **framed in carved gold, hung on the gallery wall** with a small brass plaque and a picture light, a velvet rope in front and a scatter of applause bubbles.

**INGREDIENTS / CONTENTS.** Coral/plum/teal/cream paint, loaded brush, drips, flung droplets, wet highlights, paint pots, rinse cup, rag, drop cloth, gold frame, brass plaque.

**FILES.** `widget_target_painter.png` · `_mover.png` · `_mark.png` · `_success.png`.

---

## 7. ASTRONAUT — **PATCH**

**THE SCENE.** Extreme close-up on the bubble-ship's hull, filling the entire frame: overlapping riveted brass plates with real material — patina in the seams, polish on the crowns, condensation beading, a painted shell crest across two plates. At the left, a **porthole** with a friendly little fish pressed against the glass, cheeks squashed, looking out with wide worried eyes. Across the plates, **five cracks** — jagged dark navy lines with a pale stress halo, each **venting a thin stream of bubbles** that curves up out of frame. Bottom right, a tool caddy: a rivet gun, a coil of gasket cord, a spanner. Through a gap between plates at the top right: the star-field and the reef far below.

**WHAT MOVES AND HOW.** `_mover`: a **shell-shaped brass patch** with a rubber gasket lip and four pre-set rivets, its edges glowing warm, in a halo with the rivet gun ghosted beside it. `_mark`: a patch **sealed flush** over a crack, four rivets bright and struck, the gasket squeezed out slightly at the rim, the bubble leak replaced by a small clean gleam.

**THE MOMENT OF PROGRESS.** **10%** — one leak stopped, four still streaming — the bubble count is the score. **50%** — half the streams gone; the frame gets visibly calmer. **100%** — no bubbles anywhere.

**THE SUCCESS IMAGE.** `widget_target_astronaut_success.png` — the whole hull sealed and gleaming, every rivet catching a highlight, the porthole fish now cheering with its fins up, the engine bells below lighting a warm coral plume, and the ship beginning to rise past a ring of bubbles with the star-field wheeling behind.

**INGREDIENTS / CONTENTS.** Brass patches, rivets, gasket cord, rivet gun, spanner, escaping bubbles, porthole, porthole fish, hull plates, star-field.

**FILES.** `widget_target_astronaut.png` · `_mover.png` · `_mark.png` · `_success.png`.

---

## 8. RACER — **FINISH**

**Reframe:** give the finish something to *build*. She clips the checkered banner into place across the track, then the kart bursts through it.

**THE SCENE.** Low camera on the track surface, looking up the straight. The **finish arch** straddles the frame — coral-and-gold pillars cropped by both edges, shell finials, a bank of round lamps. Slung between them, a **checkered ribbon sagging loose**, with five **empty brass clasps** hanging open along its length and one end trailing to the ground. The track below is banked coral with a painted racing line, bubble-turbo strips glowing faintly, padded shell barriers along both sides. In the middle distance, small under the arch: **the kart**, headlamps on, engine bubbles trailing, waiting. Behind: grandstands packed with cheering fans, bunting, flags, a haze of confetti bubbles.

**WHAT MOVES AND HOW.** `_mover`: a **checkered pennant square** with a brass clasp, corner lifted as if caught by a current, in a halo. `_mark`: a **clasped pennant** — taut, fluttering, casting a hard shadow on the ribbon, its clasp snapped shut with a bright gleam.

**THE MOMENT OF PROGRESS.** **10%** — one pennant clipped, the ribbon still sagging. **50%** — three clipped, the ribbon lifting and straightening. **100%** — the full checkered banner taut across the arch.

**THE SUCCESS IMAGE.** `widget_target_racer_success.png` — the kart **bursting through** the finished banner in a spray of bubbles, ribbon halves flying back on either side, confetti everywhere, speed streaks blurring the barriers, the round lamps all lit, the shell trophy raised in the grandstand and every flag snapping.

**INGREDIENTS / CONTENTS.** Checkered pennants, brass clasps, finish arch with shell finials, round lamps, bunting, confetti, turbo strips, shell barriers, kart, shell trophy.

**FILES.** `widget_target_racer.png` · `_mover.png` · `_mark.png` · `_success.png`.

---

# PART 4 — PUSH (4 beats)
### `widget_push_<career>.png` + `_mover.png` + shared arrow

**Composition rules for push.** The backdrop must contain three things, and currently contains none of them:
1. A **visible runway** along `swipe_dir` — a lane, a chute, a slope, a shaft of light — painted diegetically. Not a yellow pill outline.
2. An **empty START hollow** at the near end where the mover sits at 0% — a rutted patch of mud, a dent in a pillow, a shadow pool. The mover must *belong* there without being duplicated in the backdrop.
3. A **rewarding DESTINATION** at the far end — an open gate with light spilling out, a turned-back bed, an apex with the racing line. The child must be able to see where the thing is going before she moves it.

The mover carries its own **motion cues baked in** (dust puff, spray, trailing bubbles, streaming hair) so it reads as moving even when the engine has it static.

---

## 1. FARMER — **HERD** *(swipe right)*

**THE SCENE.** A meadow lane in three-quarter view sweeping left to right across the frame. **Left third:** a churned muddy yard — rutted, glossy, scattered with straw, a puddle reflecting the sky, a mess of trotter-prints, a tipped bucket. This is the empty start hollow. **Middle:** the lane itself, hemmed by a weathered rail fence with knot-holes, wildflowers and long grass leaning over it, a stray hen and a butterfly. **Right third:** the **barn gate standing wide open**, warm amber lantern light spilling out across the lane and up the fence posts; inside you can see a trough heaped with carrots, corn and apples, a hay bale, a coiled rope, and a cat sitting on the gatepost with its tail curled. Behind: orchard rows, a windmill, a deep coral sunset with backlit clouds and drifting glow-plankton.

**WHAT MOVES AND HOW.** `widget_push_farmer_mover.png` (512x512) — **a huddle of three piggies trotting together**: the leader with its snout thrust forward and ears blown back, a second mid-hop with a trotter kicking a splash of mud, a small one scampering behind with its tail a blur. A mud-and-dust puff trails beneath them and three specks fly up behind. They read as *moving* at rest.

**THE MOMENT OF PROGRESS.** **10%** — they've left the mud, one trotter on the lane, dust puff behind. **50%** — level with the puddle, the gate's lantern light now warming their backs. **100%** — at the gate mouth, silhouetted against the golden interior, tails up.

**THE SUCCESS IMAGE.** `widget_push_farmer_success.png` *(Tier 2 — see engine notes)* — all three piggies inside at the trough, one with a carrot crosswise in its mouth, one with its front trotters up on the rim, the gate swinging shut, the cat stretching, lantern blazing, the sunset gone crimson.

**INGREDIENTS / CONTENTS.** Piggies, mud and splash, straw, carrots/corn/apples in the trough, hay bale, bucket, lantern, fence posts, wildflowers, hen, cat, windmill.

**FILES.** `widget_push_farmer.png` 1024x576 · `widget_push_farmer_mover.png` 512x512 · *(opt.)* `widget_push_farmer_success.png` 1024x576.

---

## 2. BOXER — **DUCK** *(swipe down)*

**THE SCENE.** Ring's-eye view. **Top third:** a huge coral training bag swinging in from the upper right, cropped by the frame, its stitched seams and worn leather clearly readable, chain and swivel above, a hard shadow it throws across the canvas below — the shadow tells her exactly where the danger is. **Bottom two-thirds:** the ring canvas, cream with a painted shell logo, taut ropes running across the left and right edges with turnbuckles; a corner stool with a folded towel and a shell flask; three imps peeking under the bottom rope with wide eyes; audience pennants and the round-progress lamps glowing behind. Painted at the bottom centre: a **pool of deep shadow with a scuffed ring in the canvas** — the safe hollow, the place to get to.

**WHAT MOVES AND HOW.** `widget_push_boxer_mover.png` (512x512) — Roshan front-on in a mid-duck: knees bent, chin tucked, both gloves up beside her face, eyes turned up at the bag and **grinning**, hair and tail-fin blown up by the drop, with two arcing bubble-trails above her head showing where her head just was.

**THE MOMENT OF PROGRESS.** **10%** — she's dipped slightly, the first motion arc appears. **50%** — properly crouched, the bag's shadow sliding across her shoulders. **100%** — down in the shadow pool, the bag sailing over her, a pop of bubbles in its wake.

**THE SUCCESS IMAGE.** `widget_push_boxer_success.png` *(Tier 2)* — she springs back up with both gloves punched to the sky, the bag swinging harmlessly away at the frame edge, imps applauding with their arms over the rope, bubble confetti bursting, all the round lamps lit.

**INGREDIENTS / CONTENTS.** Training bag with chain and swivel, boxing gloves, ropes and turnbuckles, corner stool, towel, shell flask, imps, pennants, round lamps.

**FILES.** `widget_push_boxer.png` · `widget_push_boxer_mover.png` · *(opt.)* `widget_push_boxer_success.png`.

---

## 3. RACER — **STEER** *(swipe right)*

**THE SCENE.** Chase camera, low and close behind. The banked coral track sweeps up from the bottom of the frame into a **hard bend at the upper right**, the banking clearly angled so you feel the lean before anything moves. Along the outside: padded shell barriers in coral and cream, course flags on poles leaning with the wind, a run-off strip of pale sand. Along the inside of the apex: **bubble-turbo strips** glowing dim teal, and a **racing line painted in pale gold dashes** curving through the gap between two barriers — the destination, unmistakable. Beyond the bend: grandstands packed and blurred, bunting, a haze of confetti, the arch in the far distance. Bottom of frame: the track surface streaking past with motion smear.

**WHAT MOVES AND HOW.** `widget_push_racer_mover.png` (512x512) — the opera kart from three-quarter rear, **leaning hard into the turn**: the inside wheel lifting clear of the track, the body rolled, the driver's ponytail and tail-fin streaming sideways, a fan of bubble spray blasting off the rear wheels, and heat-shimmer over the exhaust shells. The lean *is* the steering.

**THE MOMENT OF PROGRESS.** **10%** — kart barely angled, wheels near-straight, small spray. **50%** — leaning hard, spray fanning wide, inside wheel clear of the ground. **100%** — on the gold racing line at the apex, through the barrier gap, the turbo strip beneath it now blazing.

**THE SUCCESS IMAGE.** `widget_push_racer_success.png` *(Tier 2)* — the kart rocketing out of the bend onto the straight, turbo trail blazing coral behind it, flags snapping, the crowd a joyful blur, speed streaks radiating from the vanishing point.

**INGREDIENTS / CONTENTS.** Opera kart, bubble spray, shell barriers, course flags, turbo strips, gold racing line, grandstand crowd, bunting, confetti.

**FILES.** `widget_push_racer.png` · `widget_push_racer_mover.png` · *(opt.)* `widget_push_racer_success.png`.

---

## 4. NURSERY — **BEDTIME** *(swipe down)*

**Note:** `widget_push_nursery.png` currently uses a **thin-line, coloring-book human baby** — completely off-model for this painterly mer-world. Must be repainted as a merbaby.

**THE SCENE.** A nursery at night, warm and quiet. **Lower half:** a **scallop-shell cradle**, large and front-on, cropped by the bottom edge — its ridged shell in cream and blush, gold-rimmed, rocking on a curved base. The bedding is **turned back and waiting**: a coral quilt folded to a neat triangle, a pearl-white pillow with a soft dent already pressed into it, a knitted seaweed blanket hanging over the side, a plush octopus tucked into the far corner with one arm draped out. **Upper half:** a mobile of little glowing jellyfish and gold stars hanging on threads, softly turning; a shelf holding a milk bottle, a folded stack of muslins tied with ribbon, a shell nightlight; a round porthole window with moonlight coming through it and a slow drift of bubbles. Walls in soft plum shading to teal. A shaft of moonlight runs down the frame — the runway.

**WHAT MOVES AND HOW.** `widget_push_nursery_mover.png` (512x512) — a **sleepy merbaby swaddled in a coral wrap**, held in two cupped mermaid hands: eyes heavy and nearly closed, one tiny fist escaped and curled by its cheek, a wisp of hair, a small iridescent tail-fin peeking from the bottom of the swaddle, and three dream-bubbles rising above its head.

**THE MOMENT OF PROGRESS.** **10%** — the hands begin to lower, one dream-bubble drifts up. **50%** — the baby is directly over the cradle, its soft glow warming the pillow, eyes down to slits. **100%** — settled into the dent in the pillow, hands beginning to withdraw, the quilt ready to fold over.

**THE SUCCESS IMAGE.** `widget_push_nursery_success.png` *(Tier 2)* — the baby fast asleep with the coral quilt drawn up under its chin, thumb near its mouth, the plush octopus tucked in beside it with an arm over the blanket, a soft row of "z" bubbles rising, the jellyfish mobile dimmed to a nightlight glow, moonlight lying in a bar across the cradle. Utterly still and warm.

**INGREDIENTS / CONTENTS.** Merbaby, coral swaddle, coral quilt, pearl pillow, knitted seaweed blanket, plush octopus, milk bottle, folded muslins, jellyfish-and-star mobile, shell nightlight, porthole moonlight, dream bubbles.

**FILES.** `widget_push_nursery.png` · `widget_push_nursery_mover.png` · *(opt.)* `widget_push_nursery_success.png`.

---

# PART 5 — SHARED FILES

**`widget_push_shared_arrow_lr.png` / `widget_push_shared_arrow_down.png`** (256x256 each — replace the flat yellow arrows). A **triple chevron built from pearl-and-coral bubbles**, largest and brightest at the leading tip, fading back into a soft gold streak; soft-edged, no hard vector silhouette, painted with the same rim-light as everything else. The engine already draws these at 0.72 alpha (`opera_gesture_surface.gd:532`), so paint them at full opacity and let the engine soften them. Two files, four beats — the cheapest quality win in the set.

---

# PART 6 — ENGINE CHANGES (exact locations)

**Tier 1 — required for any of this to read as "full screen". All literal-number edits.**

| file:line | now | change to |
|---|---|---|
| `scripts/opera_career_world_2d.gd:406-407` | `action_panel` at `(430,160)`, `420x430` | full stage, e.g. `(50,28)`, `1180x664` |
| `scripts/opera_career_world_2d.gd:744-745` | `surface` at `(24,70)`, `392x232` | `(0,72)`, `1180x560` (16:9-ish, leaves the label ribbon on top) |
| `scripts/opera_gesture_surface.gd:346-347` | white wash `rgba(.94,.97,1,.96)` + 4px border drawn under everything | skip both when `widget_backdrop != null` (new backdrops are opaque full-bleed) |
| `:531` | push mover `136.0` | `420.0` |
| `:530` | push travel `42.0` | `300.0` |
| `:536` | target mover `142.0` | `300.0` |
| `:535` | target mark `76.0` | `190.0` |
| `:220` | tap hit radius `92.0` (fixed px) | `size.x * 0.12` — at 1180 wide the fixed 92px becomes a proportionally much smaller target for a 4-year-old |

**Tier 2 — small adds that unlock concepts flagged above.**
- **push completion** (~3 lines): in `_load_widget_set` `"push"` case add `widget_overlay = _load_widget_texture("%s_success.png" % prefix)`; in `_draw_widget_layers` `"push"` case add `if widget_overlay != null and widget_fill >= 0.96: draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)`. Identical to the existing `target` pattern at `:537-538`. This gives all four push beats a held success image; the audit's completion score can't move without it.
- **travelling piping bag** (~4 lines, optional): in the `"trace"` case load `%s_mover.png` and draw it at `Vector2(lerpf(x0, x1, widget_fill), y_path(widget_fill))`. Only worth doing if the Tier-1 chef PIPE concept (bag baked at the left, ribbon extruding out of it) tests as not dynamic enough. **The Tier-1 version already delivers the owner's ask with zero engine risk — build that first.**

---

# PART 7 — FILE MANIFEST & PRODUCTION ORDER

**Total: 46 painted files.** All under `assets/opera/worlds/widgets/`.

- **trace** — 12 files: 6 x `widget_trace_<career>.png` (1024x576) + 6 x `_lit.png` (1024x576). Careers: chef, detective, ballerina, doctor, magician, painter.
- **target** — 32 files: 8 x backdrop (1024x576) + 8 x `_mover.png` (512x512) + 8 x `_mark.png` (256x256) + 8 x `_success.png` (1024x576). Careers: chef, candymaker, doctor, farmer, boxer, painter, astronaut, racer. *(7 of the 8 `_success` files do not exist today; the boxer one must be replaced.)*
- **push** — 8 files: 4 x backdrop (1024x576) + 4 x `_mover.png` (512x512), plus 4 optional `_success.png` (Tier 2). Careers: farmer, boxer, racer, nursery.
- **shared** — 2 files: `widget_push_shared_arrow_lr.png`, `widget_push_shared_arrow_down.png` (256x256).

**Build order (highest owner-visible impact first):**
1. **chef PIPE** trace pair — the named headline. Prove the extruding-ribbon technique on one beat before committing the other five.
2. **chef TOP** target quad — proves the mover/mark/success role split and rhymes directly with `goal_chef.png`.
3. **farmer HERD** push pair + the two shared arrows — proves the empty-start/rewarding-destination composition and kills the yellow arrow across all four push beats at once.
4. Remaining 5 trace pairs.
5. Remaining 7 target quads (**boxer BELT** early — it currently has the worst success image in the project).
6. Remaining 3 push pairs (**nursery BEDTIME** early — it is the only off-model art in the set).

**Content references to hand the painter**, all under `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/`:
`opera_job_pastry_chef_gameplay_piping_ribbon.png` (bag + ribbon material — already close to the right idea, just needs to fill a screen), `..._stage_states_frosting_ribbon.png` (ribbon sheen and flow), `..._gameplay_cherry_topping.png`, `..._gameplay_topping_targets.png`, `..._gameplay_finished_cake.png`; `opera_job_doctor_gameplay_bandage_unrolled/_wrap.png`, `..._gameplay_starfish_worried/_calm/_happy.png` (the three faces the wipe-swap trick needs); `opera_job_magician_gameplay_pearl_wand.png`, `..._gameplay_hat_open.png`, `..._gameplay_bunny_fish_reveal.png`; `opera_job_painter_gameplay_splat_stamp_set.png`, `..._gameplay_palette.png`, `..._gameplay_canvas_blank/_finished.png`, `..._gameplay_rinse_cup.png`; `opera_job_boxer_gameplay_championship_belt.png`, `..._gameplay_training_bag.png`, `..._gameplay_imp_peek.png`; `opera_job_farmer_gameplay_piggy_trot_a/_b.png`, `..._gameplay_piggy_hop.png`, `..._gameplay_mud_splash.png`, `..._gameplay_vegetable_basket.png`, `..._stage_states_picnic_blanket.png`; `opera_job_astronaut_engineer_gameplay_bubble_tank.png`, `..._gameplay_rocket_side.png`; `opera_job_racecar_driver_gameplay_opera_kart_rear.png`, `..._gameplay_finish_ribbon.png`, `..._gameplay_bubble_turbo_trail.png`; `opera_job_candy_maker_gameplay_*_candy.png` (eight wrapped candy shapes), `..._stage_states_parade_arch.png`; `opera_job_detective_gameplay_magnifier.png`, `..._gameplay_pearl_tiara.png`, `..._gameplay_paw_clue.png`, `..._gameplay_feather_clue.png`; `opera_job_ballerina_gameplay_twirl_ribbon.png`.

**The one-line acceptance test for every file:** stand back six feet from the tablet. If you cannot name three ingredients in the scene, it is not finished.

---

## CONCEPTS: gauge-track-lanes-charge-catch

# RICH WIDGET CONCEPTS — gauge (3), track (8), lanes (10), charge (5), catch (1)
## 27 beats. Art-director briefs, written against the verified engine contract.

---

# PART 0 — WHAT I LOOKED AT, AND WHAT IS ACTUALLY WRONG

## The caliber bar (verified by reading the files)

`assets/opera/worlds/props/goal_chef.png` — a three-tier layered cake, 512², painterly: sponge with visible crumb texture, a coral and a plum layer, piped cream pearls running the seam of every tier, six rosettes on top in three colours, two cherries on a shared stem, a scalloped doily plate with pierced holes. It has weight, bounce light, and a hand-inked outline that never goes mechanical.

`assets/opera/worlds/props/goal_magician.png` — a cloud-fluffy bunny-fish hovering over a plum top hat with a coral band and a gold-set pearl shell clasp; the sparkle language is four-point stars plus loose pearls, scattered asymmetrically.

`assets/opera/worlds/backdrops/world_chef.png` (1024×576) and `world_astronaut.png` (1024×576) — full-bleed painted rooms with foreground, midground and horizon; forty-plus identifiable objects each (whisk in a batter bowl, spice jars on a rack, a lit oven arch, a tiered cake stand under a glass cloche, piping bags with rosettes on the near counter); consistent pearl/coral/teal/plum palette, warm rim light, soft depth haze.

## What the current widgets in my five templates actually are

- `widget_gauge_chef.png` (1024×608) — a **white rounded card** with a navy outline, a flat mint-green pie wedge on a flat navy pie, a yellow ellipse floating at the top, and a cropped oven prop pasted in the corner at 25% scale. Zero relationship to baking. `widget_gauge_racer.png` is the identical card with the identical wedge and a cropped dashboard-lamp prop. **The two "gauges" differ only by the pasted-in prop and the colour of one ellipse.**
- `widget_track_boxer.png` — the same white card, a pair of gloves floated at 22% scale in the middle of nothing, and a **flat lozenge progress bar** with a mint segment. `widget_track_candymaker.png` is worse: the parade cart is pasted in as an **un-alpha'd 190px square with a dark navy background box** still attached — a literal rectangle of the wrong colour sitting in the middle of the frame.
- `widget_charge_ballerina_full.png` — the entire "progressive reveal" layer is **one mint rounded rectangle, 50px wide, pinned to the right edge**. Nothing else is on the canvas. All five charge `_full` layers are this bar. This is the layer that is supposed to carry the feeling of a thing filling.
- `widget_lanes_detective.png` — three treasure boxes, decently painted, floating on the white card at 30% scale with no table, no room, no light. `widget_lanes_farmer_lit.png` (768×256) has genuinely good art (a hopping piglet, a munching piglet, a hay bale) — but the engine draws each cell at **124px, only during the 1.4s flash**, so the best painting in the whole set is on screen for a second and a half at postage-stamp size.
- `widget_catch_nursery_pillows.png` — **five flat purple ellipses with a 3px outline.** `widget_catch_nursery.png` is an empty white card with three yellow dots on two grey strings.

## The two structural problems behind all of it

**1. The widget is 10.7% of the screen.** `scripts/opera_career_world_2d.gd:417` sets `surface.size = Vector2(372, 266)`; line 745 sets `Vector2(392, 232)`; the parent `action_panel` is 420×430 at (430,160). On a 1280×720 stage that is 98,952 of 921,600 pixels. You cannot put "piping bags in full screen glory" into it.

**2. Everything painted is being squashed 17%.** All widget backdrops are authored at 1024×608 (aspect 1.684) and drawn with `draw_texture_rect(widget_backdrop, panel)` into a 372×266 panel (aspect 1.398). Every circle in every widget is currently an ellipse on the tablet.

Plus: `_draw()` paints `Color(0.94,0.97,1.0,0.96)` over the whole panel and strokes a 4px accent border **before** the backdrop. That white card and its navy outline are baked into the engine, not the art.

---

# PART 1 — THE SHARED SPEC (applies to all 27 concepts)

## Canvas standard — new

| Layer | Canvas | Kind |
|---|---|---|
| `widget_<tpl>_<career>.png` | **1024×576** | painted, opaque, full-bleed. No card, no border, no white inset, no rounded corners. |
| `..._fill.png` (new) | **1024×576** | painted RGBA, progressive bottom-up reveal |
| `..._full.png` (charge) | **1024×576** | painted RGBA, progressive bottom-up reveal |
| `..._success.png` | **1024×576** | painted RGBA, held celebration frame |
| `..._mover.png` / `_glow.png` / `_needle.png` / `_hit.png` / `_cradle.png` | **256×256** | painted RGBA sprite, transparent, ~8px alpha padding, no background box |
| `..._lit.png` (lanes) | **768×256** | three 256² cells, left→right = lane 0,1,2 |
| `widget_catch_nursery_pillows.png` | **1024×128** | painted RGBA band |

1024 is the longest side everywhere — inside the mobile-renderer limit. 1024×576 is exactly 16:9, so a full-screen 1280×720 panel shows it undistorted.

## Five cheap engine changes these concepts assume

1. **Grow the surface to full-screen.** `surface.size = Vector2(1280, 720)` at position (0,0); the career backdrop sits behind and the task card frame becomes a thin top ribbon. This is the change the owner is actually asking for.
2. **Skip the paper rect and the border when `widget_backdrop != null`** (`opera_gesture_surface.gd:_draw()` lines 337-339). The painted scene is the frame.
3. **Add a progressive `_fill` layer to gauge, track and lanes.** `widget_fill` is already driven with real beat progress (`opera_career_world_2d.gd:1049`, `1137`) and `_draw_progress_overlay()` already exists. One line per template in `_draw_widget_layers()`. **This is the single highest-value change** — today those three templates have no "is it working?" signal at all.
4. **Per-career `_needle` (gauge) and `_hit` (track)** loaded with a fallback to the shared file. One `_load_widget_texture` line each.
5. **Draw lanes `_lit` cells at ~320px instead of 124px, and hold them ~0.6s after a correct pick** (`opera_gesture_surface.gd:540-543`). The lane art already exists and is good; it is just being shown too small for too short a time.

## The painter's rule for every progressive layer

`_draw_progress_overlay(..., horizontal=false)` computes the layer's **ink band** (the first and last rows containing any alpha > 0.08) and sweeps the reveal edge **upward** through that band. So:

> **A progressive layer must be bottom-stackable.** Any horizontal slice of it, revealed from the bottom, must be a truthful picture of "partly done." Liquid levels, rising columns, stacking bales, lamps lighting from the floor up, a crowd filling a room from the front rows back — all good. A single centred object that would appear sliced in half — bad. Paint the layer as a **vertical strip** and keep everything else on that canvas fully transparent, so the ink band is exactly the strip.

## Track geometry (all eight track beats, exact)

The runner travels `x = lerp(0.12w, 0.88w, t)` at `y = 0.66h`; the scoring zone is `t ∈ [0.30, 0.72]`. On a 1024×576 canvas:

> **The painted sweet-spot patch must sit at x 356–683, centred on y 380. The runner's path is y 380, x 123 → 901.** Paint the whole path as a real ground plane (table, deck, canvas, street, floor) and the sweet spot as a real place on it — a light pool, a trough, an arch, a mitt-target, a doorway — with the runner's cast shadow travelling on it.

## Lanes geometry (all ten lanes beats, exact)

Hit-testing is `lane = int(x / w * 3)` over the **full panel height**. So:

> **Each vertical third — x 0–341, 341–683, 683–1024 — must read as a self-contained bay from ceiling to floor**: a plinth with a tall banner behind it, a full-height shelf bay, a furrow running away, a lit column. The choosable object is centred at x = 171 / 512 / 853, sized large (≥ 260px tall). The "which one" prompt is painted into the top of the backdrop as a real object — a case card on a corkboard, a music-box cylinder, a stage monitor, a pictogram cabinet.
>
> **The lanes `_fill.png` ink band is standardised as the bottom strip: full width, y 390–570** — a growing row/pile of the collected thing along the front of the scene. It never collides with the lane columns.

---

# PART 2 — GAUGE (3 beats)

*Engine: `_needle` sprite pivots at (0.5w, 0.82h) through −60°→+60° driven by `timing_position`; `_success` is drawn full-panel only while the needle is inside the zone; child taps in the zone. So the dial bezel is a real object bolted at bottom-centre of the scene, and the needle points up into the action.*

---

## GAUGE / CHEF — **BAKE**

**THE SCENE.** We are crouched at the open mouth of the great pearl-and-copper oven, its door swung down toward us so its inside face ramps into the bottom of the frame. Two-thirds of the screen is the oven cavity: firebrick the colour of warm apricot, coral embers banked and breathing at the back, and on the middle rack a round tin of batter, domed and just beginning to split, its top turning from wet cream to gold. Heat shimmer bends the brick behind it. Bolted to the door at bottom-centre is the **thermometer** — a fat brass bezel with a scalloped shell rim and bevelled glass, 340px across, its face painted as an arc: cool pearl-blue at the left, a wide glowing amber "just right" band in the middle stamped with a tiny cake silhouette, scorched red-brown at the right with a painted crack. A tea towel hangs off the door handle; along the very bottom edge, out of focus and warm, the counter with a flour sack, three brown eggs in a wire basket, a milk jug, a block of butter, a vanilla pod and a sugar bowl. Steam curls up the left wall.

**WHAT MOVES AND HOW.**
- `widget_gauge_chef_needle.png` (256²) — a copper spoon-handle pointer with a pearl boss and its own soft cast shadow, so it floats above the dial glass. Rotates.
- `widget_gauge_chef_fill.png` (1024×576, ink band **x 380–700, y 150–430**) — the cake **rising and browning inside the tin**. Bottom of the band: a pale slumped puddle with one bubble. Top of the band: a tall domed golden sponge with a split crown and a wisp of steam.
- `widget_gauge_chef_success.png` — the in-zone flash: embers flare, three gold heat-shimmer rings ripple off the tin, four sparkle motes.

**THE MOMENT OF PROGRESS.** 10% flat batter, one bubble. 50% risen to the tin rim, edges set, top still pale and wet. 100% domed proud above the rim, cracked golden crown, steam curling.

**THE SUCCESS IMAGE.** The cake lifted clear on a shell trivet, deep gold, steaming, a knob of butter sliding down its flank, the oven glowing behind. Held 2s.

**INGREDIENTS.** Eggs, milk, flour, butter, sugar, vanilla pod, batter, cake tin, embers, tea towel, wire basket.

**FILES.** `widget_gauge_chef.png` 1024×576 painted · `_needle.png` 256² rotating sprite · `_fill.png` 1024×576 painted progressive · `_success.png` 1024×576 painted overlay.
**REF.** `opera_job_pastry_chef_gameplay_oven_open.png`, `_bowl_empty.png`, `_stage_states_oven_alcove.png`, `_oven_success.png`.

---

## GAUGE / ASTRONAUT — **BOOST**

**THE SCENE.** Inside the bubble-rocket's engine bay. Filling the frame is a fat vertical **pressure column** — hand-blown glass in a riveted brass cage, running from the floor plate up out of the top of frame, part-full of luminous aqua fuel with bubbles rolling through it. Around it: coiled copper pipes beaded with condensation, a coral-and-cream valve wheel to the right, three shell-lamps in a row, a wrench hanging on a hook. Through a porthole at upper-left, the purple bubble-city and a distant moon straight out of `world_astronaut.png`. Bolted to the boiler's belly plate at bottom-centre, the **pressure gauge**: a shell-rimmed brass dial, pearl-white at the left, an aqua-green GO band in the middle stamped with a tiny rocket, hot coral at the right with a painted crack and a bead of steam escaping.

**WHAT MOVES AND HOW.**
- `widget_gauge_astronaut_needle.png` (256²) — a brass arrow with a pearl counterweight and a glass reflection streak. Rotates.
- `widget_gauge_astronaut_fill.png` (ink band **x 430–620, y 60–470**) — the fuel column climbing: bubbles streaming, a bright trembling meniscus, the brass cage catching the glow more as it rises.
- `widget_gauge_astronaut_success.png` — aqua flare rings around the column plus white steam jets popping from every pipe joint.

**THE MOMENT OF PROGRESS.** 10% a shallow puddle in the tube, one lazy bubble. 50% half up, bubbles streaming, the pipes beginning to glow from within. 100% full to the top, meniscus trembling, every joint venting a puff.

**THE SUCCESS IMAGE.** The bubble-rocket on the pad, engine cone blazing aqua, lifting off a ring of bubbles — the boiler behind it drained and content.

**INGREDIENTS.** Aqua fuel, bubbles, rivets, copper pipes, condensation drips, valve wheel, shell lamps, wrench, gauge glass, steam.

**FILES.** `widget_gauge_astronaut.png` 1024×576 · `_needle.png` 256² rotating · `_fill.png` 1024×576 progressive · `_success.png` 1024×576 overlay.
**REF.** `opera_job_astronaut_engineer_stage_states_pressure_lamps.png`, `_pipe_wall.png`, `gameplay_valve_wheel.png`, `gameplay_bubble_tank.png`.

---

## GAUGE / RACER — **TURBO**

**THE SCENE.** First person over the seahorse-kart's dashboard. The bottom third is the dash: brass with pearl inlay, a wooden steering yoke with two grips reaching into the bottom corners, a good-luck shell charm swinging on a cord. Bolted centre-dash, the **turbo dial** — a shell-bezel gauge, its face pearl at the left, a hot coral GO band in the middle stamped with a little flame, dark at the right. Beyond the dash the reef racetrack streaks past: coral chicanes, kelp banners strung between posts, checkered shell flags, a curtain of bubble spray thrown up by the kart ahead, motion-smeared. Up the right pillar of the frame, a vertical rack of **five round shell turbo-lamps**, currently dark pearl.

**WHAT MOVES AND HOW.**
- `widget_gauge_racer_needle.png` (256²) — a red-tipped speed pointer with a chrome hub. Rotates.
- `widget_gauge_racer_fill.png` (ink band **x 850–980, y 90–470**) — the five stacked turbo lamps lighting **bottom to top**, each gaining a bloom and a coral corona as it fires.
- `widget_gauge_racer_success.png` — white speed streaks raked across the whole frame plus a burst of bubbles off the nose.

**THE MOMENT OF PROGRESS.** 10% the bottom lamp glowing dim amber. 50% three lamps lit, the dash washed warm. 100% all five blazing coral, the entire dashboard lit from the side, streaks everywhere.

**THE SUCCESS IMAGE.** The kart bursting through a curtain of bubbles under a checkered shell arch, turbo plume streaming behind it, kelp banners whipping.

**INGREDIENTS.** Dashboard brass, pearl inlay, steering yoke, shell charm, turbo lamps, coral chicanes, kelp banners, checker flags, bubble spray.

**FILES.** `widget_gauge_racer.png` 1024×576 · `_needle.png` 256² rotating · `_fill.png` 1024×576 progressive · `_success.png` 1024×576 overlay.

---

# PART 3 — TRACK (8 beats)

*Engine: `_mover` (256²) travels the path; `_hit` flashes over it inside the zone. Geometry per Part 1. All eight get a new `_fill.png` and `_success.png`.*

---

## TRACK / DETECTIVE — **NAME**

**THE SCENE.** The detective's search table in the prop library. The back wall is a floor-to-ceiling shelf of theatre props, painted like the concept cards: a pearl tiara on a velvet stand, a plum hatbox, a coral mystery box, a stack of scripts, a feather boa spilling off a hook, a single sock, a rubber fish, a brass lantern. Across the middle at eye level runs the long **green-baize search table**, edge-lit, with a folded velvet runner. Sitting on it dead centre in a soft ellipse of searchlight is **the clue**: a single pearl-white ribbon curled on a saucer, glowing faintly, three gold sparks hovering. Everything outside that pool sits in cool shadow. Bottom edge: a notebook, a spyglass, a shell magnet, a spill of red string.

**WHAT MOVES AND HOW.**
- `widget_track_detective_mover.png` (256²) — the brass shell-handled magnifying glass, tilted 20°, its lens a real convex glass with a specular streak and a faint enlarging warp painted inside it, a soft ground shadow beneath.
- `widget_track_detective_hit.png` (256², per-career) — a gold FOUND starburst ringed with tiny pearls.
- `widget_track_detective_fill.png` (ink band **x 40–300, y 90–470**) — the **case board** on the left wall filling bottom-up with pinned clue cards, red string lacing between them.

**THE MOMENT OF PROGRESS.** 10% an empty corkboard with one lonely pin. 50% three clue cards pinned — ribbon, paw print, feather — string beginning to cross. 100% board full, a gold rosette in the middle.

**THE SUCCESS IMAGE.** The pearl tiara lifted into the searchlight on a velvet cushion, the completed case board glowing behind, a confetti of tiny pearls.

**INGREDIENTS.** Tiara, hatbox, mystery box, feather, ribbon, paw print, sock, rubber fish, notebook, magnifier, red string, pins, lantern.

**FILES.** `widget_track_detective.png` 1024×576 · `_mover.png` 256² tweened sprite · `_hit.png` 256² sprite · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_detective_gameplay_magnifier.png`, `_ribbon_clue.png`, `_pearl_tiara.png`, `_stage_states_case_board_empty.png` / `_case_board_complete.png`, `_searchlight_pool.png`, `_six_box_display.png`.

---

## TRACK / BALLERINA — **DUET**

**THE SCENE.** The recital stage from the front row. Coral and teal wing curtains sweep in from both sides, gathered with pearl ropes and gold tassels. Overhead a mirror ball scatters lozenges of light across a polished floor that holds a soft upside-down reflection of everything. At centre stage, the meeting point, a warm oval spotlight with the floor's shell-inlay rosette inside it. Roshan waits stage-left in her tutu, arm raised in fourth. Upstage: a practice barre with two pairs of pointe shoes hanging by their ribbons, and a bank of mirror panels replaying the whole scene smaller. Along the bottom, the orchestra pit glittering with brass bells and an open music box.

**WHAT MOVES AND HOW.**
- `widget_track_ballerina_mover.png` (256²) — the partner: a coral-tailed merboy dancer in a pearl sash, in a travelling arabesque, two ribbons trailing behind him with real cloth curl.
- `widget_track_ballerina_hit.png` (256²) — hands meeting: a burst of teal and cream petals plus a soft ring of light.
- `widget_track_ballerina_fill.png` (ink band **x 30–210, y 80–500**) — a **ribbon banner spiralling up the left proscenium column**, plum/teal/coral, bottom-up, finishing in a big bow at the top.

**THE MOMENT OF PROGRESS.** 10% one ribbon tail at the column base. 50% wound halfway, all three colours in play. 100% a full spiral to the capital with a fat bow and a rain of petals.

**THE SUCCESS IMAGE.** The two dancers in a held lift inside the spotlight, petals falling through the beam, the mirror ball throwing light, a bouquet resting at their feet.

**INGREDIENTS.** Tutu, pointe shoes, ribbons, petals, mirror ball, barre, brass bells, music box, bouquet, pearl ropes, tassels.

**FILES.** `widget_track_ballerina.png` 1024×576 · `_mover.png` 256² · `_hit.png` 256² · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_ballerina_stage_states_spotlight_pool.png`, `_mirror_ball_rig.png`, `_dance_floor.png`, `_curtain_call_bouquet.png`, `gameplay_twirl_ribbon.png`.

---

## TRACK / CANDYMAKER — **PARADE**

**THE SCENE.** The candy-town parade street at dusk. A wide avenue of pink and cream cobbles runs across the frame; on both sides a crowd of happy sea-creature silhouettes holding glowing lanterns and waving flags. Spanning the centre is the **parade arch** — a great hoop of twisted barley-sugar wrapped in bunting and hung with wrapped sweets, its opening a warm lit gap exactly where the cart must be. Streamers hang mid-air. Behind, sugar-spun buildings with piped-icing rooflines and shop windows full of gobstopper jars. Along the bottom, a spill of loose candies on the cobbles: spirals, hearts, shells, bows.

**WHAT MOVES AND HOW.**
- `widget_track_candymaker_mover.png` (256², **replace the current un-alpha'd square crop**) — the parade cart: pink-canopied, gold-spoked wheels, heaped with pastel gumballs, a pennant on top, one wheel painted mid-turn with a motion smear, full alpha cut-out.
- `widget_track_candymaker_hit.png` (256²) — an arch burst: confetti, two streamer curls, a shower of wrapped sweets.
- `widget_track_candymaker_fill.png` (ink band **x 800–1000, y 100–500**) — the **seven-slot candy shelf** at the right filling bottom-up, tier by tier, with wrapped candies.

**THE MOMENT OF PROGRESS.** 10% one candy on the bottom shelf. 50% shelves half full, ribbons hanging off the edges. 100% every slot filled, a rosette bow crowning the top.

**THE SUCCESS IMAGE.** The cart under the arch under a shower of confetti, every lantern in the crowd lit, the full candy shelf glowing beside it.

**INGREDIENTS.** Gumballs, spiral candies, shell candies, heart candies, bow candies, wrapped sweets, bunting, streamers, confetti, lanterns, cobbles.

**FILES.** `widget_track_candymaker.png` 1024×576 · `_mover.png` 256² · `_hit.png` 256² · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_candy_maker_stage_states_parade_arch.png`, `_parade_cart.png`, `_parade_tableau.png`, `_seven_slot_shelf.png`, `gameplay_teal_spiral_candy.png` and siblings.

---

## TRACK / FARMER — **FEED**

**THE SCENE.** The meadow pen at golden hour. A split-rail fence runs the middle distance with sunflowers nodding through it; beyond, the red barn, an orchard and soft parallax hills. The near ground is churned earth and clover. Dead centre, a chunky **wooden trough** — planks, iron bands, a shell end-plate — half full of chopped carrot, corn kernels and berries, a wooden scoop resting in it, a fat pumpkin propped against its side. Right of frame, a wicker basket overflowing with carrots, corn, apples and a spill of berries. Straw everywhere. Two piglets doze in the straw at the left, one with a trotter over its eyes.

**WHAT MOVES AND HOW.**
- `widget_track_farmer_mover.png` (256²) — the trotting piglet: pink, green kerchief, ears flapping, one front trotter lifted, little dust puffs painted at its heels.
- `widget_track_farmer_hit.png` (256²) — the munch burst: carrot tops flying, three heart puffs, a scatter of crumbs.
- `widget_track_farmer_fill.png` (ink band **x 790–1000, y 120–500**) — the **hay stack** building bottom-up, bale on bale, with a pitchfork stuck in the side.

**THE MOMENT OF PROGRESS.** 10% one bale. 50% four bales and the pitchfork. 100% a tall stack with a rooster crowing on the peak.

**THE SUCCESS IMAGE.** Five round-bellied piglets asleep in a heap around the empty trough, straw drifted over them, long sunset light.

**INGREDIENTS.** Carrots, corn, apples, berries, pumpkin, hay bales, straw, trough, scoop, wicker basket, fence, barn, sunflowers.

**FILES.** `widget_track_farmer.png` 1024×576 · `_mover.png` 256² · `_hit.png` 256² · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_farmer_gameplay_piggy_trot_a.png` / `_b.png`, `_piggy_munch.png`, `_vegetable_basket.png`, `_carrot.png` / `_corn.png` / `_berries.png` / `_pumpkin.png`, `_stage_states_hay_stack.png`, `_fence_segment.png`.

---

## TRACK / BOXER — **JAB**

**THE SCENE.** Ringside, from just off Roshan's shoulder. Three thick coral-wrapped ropes with brass turnbuckles run across the top; behind them the crowd is a warm blur of pennants and bubble-lanterns. The canvas floor fills the bottom, painted with a shell crest and scuffed with chalk. Across the middle at mitt height, chalked onto the canvas, is the **strike pocket** — a bullseye ring of cream and coral with a faint glow. Bottom-left, a corner stool with a folded towel and a flask; bottom-right corner, Roshan's own laced gloves waiting in frame. A shell bell on a stand upper-right.

**WHAT MOVES AND HOW.**
- `widget_track_boxer_mover.png` (256², **replace the floating glove pair**) — the focus mitt: a big round quilted pad with a cream bullseye, dented from use, held in a teal-sleeved forearm with a wrist wrap, motion smear on the trailing edge so it reads as swung by a person.
- `widget_track_boxer_hit.png` (256²) — impact: a white shockwave ring, four bubble-puffs, three cartoon speed wedges.
- `widget_track_boxer_fill.png` (ink band **x 40–220, y 90–500**) — the **round-lamp tower** on the left post: five round shell lamps lighting bottom to top, each with a bloom.

**THE MOMENT OF PROGRESS.** 10% one lamp warm. 50% three lamps lit, the crowd's pennants brighter. 100% all five blazing, the shell bell swinging with motion arcs.

**THE SUCCESS IMAGE.** The championship belt held up on a velvet cushion at the centre of the ring under a hot white light, gloves resting either side, confetti coming down.

**INGREDIENTS.** Focus mitt, padded gloves, ropes, turnbuckles, towel, flask, shell bell, pennants, chalk, championship belt.

**FILES.** `widget_track_boxer.png` 1024×576 · `_mover.png` 256² · `_hit.png` 256² · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_boxer_gameplay_focus_mitt.png`, `_padded_gloves.png`, `_ring_post_ropes.png`, `_towel_and_flask.png`, `_shell_bell.png`, `_stage_states_round_progress_lights.png`, `_belt_reward.png`.

---

## TRACK / MAGICIAN — **CABINET**

**THE SCENE.** The magic stage. Deep plum wing curtains with gold tassels; a polished black-lacquer floor throwing soft reflections. Centre stage, a pool of warm cream light with visible dust motes drifting in a beam that rakes down from the top-left corner. Upstage, a trick table draped in star-print velvet holding a pearl wand, a stack of three top hats and a bell jar with a single bubble inside. A rolling mirror panel stands stage-right, doubling the light. Purple four-point sparkles drift throughout, the exact sparkle language of `goal_magician.png`.

**WHAT MOVES AND HOW.**
- `widget_track_magician_mover.png` (256²) — the trick cabinet: a tall narrow lacquered box on brass castors, plum with gold shell-motif corners, its door ajar by a crack with a curious slice of light inside and a little curtain fluttering out. Castors painted mid-roll.
- `widget_track_magician_hit.png` (256²) — a puff of star-shot smoke with the bunny-fish's ears popping out of the door.
- `widget_track_magician_fill.png` (ink band **x 810–990, y 70–500**) — the **conjuring column** behind the right curtain: violet sparkles, star-shapes and floating pearls, dense at the bottom, thinning upward.

**THE MOMENT OF PROGRESS.** 10% three lonely sparkles near the floor. 50% a knee-high swirl of stars, pearls beginning to float. 100% a full column reaching the flies, the curtain lifting in its draft.

**THE SUCCESS IMAGE.** The cloud-fluffy bunny-fish — literally `goal_magician.png` — hovering above an open top hat in the spotlight, pearls and sparkles ringing it, the cabinet doors thrown wide behind.

**INGREDIENTS.** Top hats, pearl wand, bell jar, star-velvet cloth, castors, curtains, tassels, sparkles, pearls, smoke puffs, bunny-fish.

**FILES.** `widget_track_magician.png` 1024×576 · `_mover.png` 256² · `_hit.png` 256² · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_magician_stage_states_trick_cabinet.png`, `_trick_table.png`, `_spotlight_pool.png`, `_rolling_mirror.png`, `gameplay_hat_open.png`, `_pearl_wand.png`, `_bunny_fish_reveal.png`.

---

## TRACK / POPSTAR — **RHYTHM**

**THE SCENE.** The concert stage from just over the crowd's shoulder. A rainbow backdrop of soft banded light behind a pearl-lit proscenium frame; two speaker stacks flank it, cones visible through grille cloth, cabinet catches and handles painted. Sweeping across the middle of the screen at runner height is the **rainbow rhythm ribbon** — a wide satin band, red through violet, twisting so it catches highlight, laid over the stage like a ribbon of road. Where it crosses centre-frame it threads through a glowing pearl ring: the beat gate. Below, the catwalk edge and a rail of raised glow-sticks held by silhouetted fans. Above, a truss of shell-shaped par-cans throwing beams through haze. A chrome mic stand at the left with its cable coiled on the deck.

**WHAT MOVES AND HOW.**
- `widget_track_popstar_mover.png` (256²) — the beat: a plump luminous pearl note with a soft comet tail and three concentric shock rings, riding the ribbon.
- `widget_track_popstar_hit.png` (256²) — a sound burst: concentric ripple rings, four tiny hearts, a spray of gold notes.
- `widget_track_popstar_fill.png` (ink band **x 830–1000, y 80–500**) — the **applause ladder** on the right speaker stack: a vertical VU column of round shell lamps in rainbow order lighting bottom-up, glow-sticks rising alongside it.

**THE MOMENT OF PROGRESS.** 10% two lamps warm. 50% lit up to the yellow, glow-sticks half raised. 100% the whole rainbow ladder blazing, every glow-stick up, confetti starting to fall.

**THE SUCCESS IMAGE.** Roshan at the mic mid-note under a crossfire of beams, confetti falling, the crowd's glow-sticks a solid field of light.

**INGREDIENTS.** Microphone, mic stand, cable, speaker stacks, par-cans, glow-sticks, confetti, rainbow ribbon, shell tambourine on the deck.

**FILES.** `widget_track_popstar.png` 1024×576 · `_mover.png` 256² · `_hit.png` 256² · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_pop_star_gameplay_rainbow_rhythm_ribbon.png`, `_beat_pulse.png`, `_speaker.png`, `_microphone_stand.png`, `_stage_states_glow_stick_rail.png`, `_speaker_stacks.png`, `_rainbow_backdrop.png`.

---

## TRACK / NURSERY — **BURP**

**THE SCENE.** The nursery in lamplight. Close on Roshan's shoulder from behind and to the side: the baby is up on her shoulder, cheek squashed, one fist curled into her collar, a soft muslin cloth draped underneath — this fills the upper-left half of the frame. Beyond: the arm of a rocking chair, a low shelf with a bottle warmer, folded nappies, three tiny bonnets in a stack, a night-lamp casting a warm pool, and a mobile of felt fish turning overhead. On the wall a painted moon-and-shell frieze. Everything soft, low contrast, sleepy. Between the baby's shoulder blades, a warm glowing oval — **the patting spot** — ringed by three drifting sleep-bubbles.

**WHAT MOVES AND HOW.**
- `widget_track_nursery_mover.png` (256²) — Roshan's cupped hand: palm hollowed, fingers together, two soft motion arcs trailing it.
- `widget_track_nursery_hit.png` (256²) — the burp puff: one big soft bubble with two smaller ones and a tiny heart, cream and mint.
- `widget_track_nursery_fill.png` (ink band **x 820–1000, y 120–500**) — the **sleep column** rising out of the night-lamp: drowsy stars and half-moons stacking bottom-up, ending in a big crescent moon.

**THE MOMENT OF PROGRESS.** 10% one small star above the lamp. 50% a half-column of stars, the baby's eyes gone half-lidded. 100% a full column with a crescent moon at the top, the baby's eyes closed.

**THE SUCCESS IMAGE.** The baby laid in the cradle, arms up over its head, fast asleep, muslin tucked; the mobile turning; the lamp low; one bubble drifting.

**INGREDIENTS.** Baby, muslin cloth, bottle warmer, bonnets, nappies, night-lamp, felt-fish mobile, cradle, rocking chair, bubbles, stars.

**FILES.** `widget_track_nursery.png` 1024×576 · `_mover.png` 256² · `_hit.png` 256² · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
*Note: this beat currently falls through to `_draw_nursery_context()`'s vector rectangles (`opera_gesture_surface.gd:585`). Once the widget set exists the backdrop branch takes over and that fallback becomes dead code.*

---

# PART 4 — LANES (10 beats)

*Engine: three full-height columns; `_lit.png` is a 768×256 three-cell sheet. Geometry and the standardised bottom-strip `_fill` band per Part 1. All ten get a new `_fill.png` and `_success.png`.*

---

## LANES / DETECTIVE — **MATCH**

**THE SCENE.** The prop library head-on. Three plinths evenly spaced, each in its own pool of light with its own tall velvet banner behind it so each third reads as a bay. Left: a coral quilted mystery box with a brass shell clasp. Centre: a cream trunk laced with cord. Right: a plum hatbox with a ribbon bow. Every box big and chunky at plinth scale — catchlights on the brass, dust settled on the lids. Pinned to a corkboard across the top of the frame, lit by a swinging lantern, the **case card**: a photograph-style card showing the wanted box. Bottom edge, the search table with a magnifier, a notebook and a spill of red string.

**WHAT MOVES.** `_lit.png` cells — each box **open**, lid tilted back, warm gold light pouring out, the pearl tiara glinting inside, a ring of gold sparks. `_fill.png` ink band **y 390–570 full width** — a row of pinned clue cards and red string lacing along the table edge, growing left to right and upward.

**PROGRESS.** 10% one clue card. 50% three cards and crossing string. 100% a full row of six with a gold rosette.

**SUCCESS.** The pearl tiara on a velvet cushion in the middle spotlight, all three boxes open and empty, the evidence row complete.

**INGREDIENTS.** Mystery box, trunk, hatbox, tiara, magnifier, notebook, red string, pins, lanterns, dust.

**FILES.** `widget_lanes_detective.png` 1024×576 · `_lit.png` 768×256 sheet · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_detective_gameplay_coral_mystery_box.png`, `_cream_trunk.png`, `_plum_hatbox.png`, `_chest_open.png`, `_pearl_tiara.png`, `_stage_states_six_box_display.png`.

---

## LANES / BALLERINA — **STEPS**

**THE SCENE.** Looking down and forward at the dance floor. Three great inlaid floor tiles fill the frame, one per third: coral with a shell rosette, teal with a wave scroll, plum with a ribbon knot. Not flat shapes — polished stone with grout lines, a soft mirror-ball reflection sliding across each, a faint scuff of rosin. Around them: the barre along the top with two pairs of pointe shoes hanging by their ribbons, wing curtains at the edges, the mirror ball overhead. Top edge, the **music box** with its lid open and a little dancer turning — the tile to copy is shown on its spinning cylinder.

**WHAT MOVES.** `_lit.png` cells — that tile **pressed**: sunk a few pixels with a ripple ring of light spreading out of it and petals puffing from its corners. `_fill.png` bottom strip — ribbon rosettes blooming along the front edge of the stage with petals rising behind them.

**PROGRESS.** 10% one rosette. 50% three rosettes and a scatter of petals. 100% a full garland with petals in the air.

**SUCCESS.** Roshan in a held arabesque on the last tile, all three tiles glowing, petals raining, a bouquet at the stage edge.

**INGREDIENTS.** Floor tiles, rosin, pointe shoes, ribbons, barre, mirror ball, petals, music box, bouquet.

**FILES.** `widget_lanes_ballerina.png` 1024×576 · `_lit.png` 768×256 · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_ballerina_gameplay_coral_shell_tile.png`, `_teal_wave_tile.png`, `_plum_ribbon_tile.png`, `_pressed_tile_ripple.png`, `_music_box.png`, `_four_tile_floor.png`.

---

## LANES / CANDYMAKER — **SORT**

**THE SCENE.** The candy workshop bench, close and warm. Three heavy brass mould plates lie side by side, one per third: a shell mould, a heart mould, a spiral mould — deep-cut cavities, sugar dust in the corners, a smear of syrup on one edge. Behind them a copper syrup kettle with a tap, a jar of coloured sanding sugar, a pair of tongs, and a marble slab dusted with icing. Suspended above centre frame in the tongs is **the candy to sort** — a fat glossy teal spiral — spotlit, its soft shadow falling onto the correct plate.

**WHAT MOVES.** `_lit.png` cells — that mould **filled**: molten candy poured into the cavity, a glossy meniscus, a curl of steam, a sugar sparkle. `_fill.png` bottom strip — a growing line of wrapped, twisted-end sweets along the front of the bench.

**PROGRESS.** 10% one wrapped sweet. 50% four. 100% a row of eight in a paper tray with a ribbon tied round it.

**SUCCESS.** The tray of finished candies lifted into the light, every shape represented, ribbon tied, sugar glinting.

**INGREDIENTS.** Shell/heart/spiral moulds, molten sugar, sanding sugar, tongs, copper kettle, marble slab, icing dust, wrappers.

**FILES.** `widget_lanes_candymaker.png` 1024×576 · `_lit.png` 768×256 · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_candy_maker_gameplay_mold_plates.png`, `_scoop_and_tongs.png`, `_teal_shell_candy.png`, `_cream_heart_candy.png`, `_teal_spiral_candy.png`, `_wrapped_candy_reward.png`.

---

## LANES / DOCTOR — **FIND**

**THE SCENE.** The reef clinic. A long padded exam bench runs across the frame — cream vinyl with brass studs, a paper roll pulled across it. Sitting on it, one per third, three starfish patients with unmistakably different faces: left, happy and pink; centre, worried with a wobbly mouth and a tear; right, sleepy with heavy lids. Behind, a tool trolley with a stethoscope, a thermometer, a bandage roll and a kidney dish; a privacy curtain half drawn; a jar of lollipops. Across the top, the **pictogram cabinet** — a lit shell-panel showing the symptom to look for.

**WHAT MOVES.** `_lit.png` cells — that starfish **being cared for**: the stethoscope disc on its chest, a heart-ripple ring spreading, a kiss-puff, its mouth turning up into a smile. `_fill.png` bottom strip — a row of care tokens filling along the trolley shelf: a plaster, a heart sticker, a thermometer, a folded bandage, a lollipop.

**PROGRESS.** 10% one plaster. 50% three tokens. 100% a full shelf with a gold care medallion at the end.

**SUCCESS.** Three recovered starfish in a row, all beaming, one waving, hearts floating up, the medallion glowing.

**INGREDIENTS.** Starfish patients, stethoscope, thermometer, bandage roll, plasters, kidney dish, lollipops, paper roll, privacy curtain.

**FILES.** `widget_lanes_doctor.png` 1024×576 · `_lit.png` 768×256 · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_doctor_gameplay_starfish_worried.png` / `_calm.png` / `_happy.png`, `_stethoscope.png`, `_heartbeat_ripple.png`, `_kiss_heart_puff.png`, `_checkup_tray.png`, `_stage_states_pictogram_cabinet.png`, `_tool_trolley.png`.

---

## LANES / FARMER — **PLANT**

**THE SCENE.** Looking down the vegetable patch. Three ploughed furrows run away from us, one per third — dark crumbly earth with a hand-painted marker stake at the head of each: a carrot board, a corn board, a pumpkin board, each with the actual vegetable painted on it. Between the furrows, trodden grass and a scatter of stones. Along the bottom, a watering can, a trowel and an open seed packet spilling seeds. Beyond: the fence, the barn, sunflowers, a wheelbarrow. Held above centre frame in a gloved hand, **the seed** — plump and striped, softly glowing, its shadow pointing at its furrow.

**WHAT MOVES.** `_lit.png` cells — that furrow **sprouting**: the earth parting, a bright green shoot with two seed-leaves pushing up, a puff of soil, a worm waving. `_fill.png` bottom strip — the harvest basket filling along the front with carrots, corn, apples, berries and a pumpkin.

**PROGRESS.** 10% a single carrot in the basket. 50% basket half full. 100% overflowing, a pumpkin balanced on top.

**SUCCESS.** Three full-grown rows — feathery carrot tops, tall corn, a fat pumpkin — a scarecrow waving, the basket brimming.

**INGREDIENTS.** Carrot, corn, pumpkin, apples, berries, seeds, watering can, trowel, soil, worm, fence, barn, sunflowers, wheelbarrow.

**FILES.** `widget_lanes_farmer.png` 1024×576 · `_lit.png` 768×256 · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_farmer_gameplay_carrot.png` / `_corn.png` / `_pumpkin.png` / `_berries.png` / `_apple.png`, `_vegetable_basket.png`, `_stage_states_orchard_parallax.png`.

---

## LANES / BOXER — **ROUND**

**THE SCENE.** The ring from above and behind. Three corner posts stand across the frame, each wrapped in a different cord — coral, teal, cream — each with a padded stool and a bucket beneath it and a round lamp hanging above. The canvas floor sweeps toward us, chalk-scuffed, a shell crest at its centre. Behind, the crowd's pennants and bubble-lanterns. From **one** corner a mischief imp peeks around the post with a cheeky grin and a curl of tail showing — the tell. Bottom edge: the corner stool with a towel, a flask and Roshan's gloves resting on it.

**WHAT MOVES.** `_lit.png` cells — that corner **lit**: a hot white spot, the imp bopped into a bubble-puff with stars round its head, a bonk ring. `_fill.png` bottom strip — the apron round-lamps lighting up along the ring edge with confetti drifting up above them (lamps at the base of the band, confetti at the top, so it stacks truthfully).

**PROGRESS.** 10% one apron lamp lit. 50% three lit and a few confetti. 100% all lit, confetti thick, the shell bell swinging.

**SUCCESS.** The championship belt raised on a velvet cushion at the centre of the ring, imps bowing in a row along the ropes, confetti coming down.

**INGREDIENTS.** Corner posts, cords, stools, buckets, towels, flask, gloves, shell bell, pennants, imps, championship belt, confetti.

**FILES.** `widget_lanes_boxer.png` 1024×576 · `_lit.png` 768×256 · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_boxer_gameplay_ring_corner.png`, `_imp_peek.png`, `_imp_bopped.png`, `_bubble_puff_impact.png`, `_round_lamps.png`, `_stage_states_coral_corner_stool.png` / `_teal_corner_stool.png`, `_belt_reward.png`.

---

## LANES / MAGICIAN — **TRACK**

**THE SCENE.** The magic stage head-on. Three top hats sit in a row on a mirror-polished rail, one per third, each with a different band — coral, cream, teal — brims catching a rim of light, a soft reflection pooled under each. Behind them a plum star-velvet drape and a rolling mirror panel; above, a spotlight pool; in the foreground the trick table with a pearl wand lying across it and a scatter of sparkles. Faint looping glitter trails run between the hats — the ghost of the shuffle. Purple four-point sparkle motes throughout, matching `goal_magician.png`.

**WHAT MOVES.** `_lit.png` cells — that hat **tipped open** with the cloud-fluffy bunny-fish rising out of it in a burst of stars and pearls, one cell per band colour. `_fill.png` bottom strip — a string of pearls and stars accumulating along the rail with a rising glitter haze above it.

**PROGRESS.** 10% two pearls on the rail. 50% a half-string of pearls and stars. 100% a full pearl string with big stars and a glitter mist.

**SUCCESS.** The bunny-fish hovering above the middle hat exactly as in `goal_magician.png`, all three hats tipped, pearls and sparkles everywhere.

**INGREDIENTS.** Top hats, coloured hat bands, pearl wand, star-velvet, mirror panel, sparkles, pearls, smoke, bunny-fish.

**FILES.** `widget_lanes_magician.png` 1024×576 · `_lit.png` 768×256 · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_magician_gameplay_coral_band_hat.png` / `_cream_band_hat.png` / `_teal_band_hat.png`, `_hat_open.png`, `_bunny_fish_reveal.png`, `_swap_trail.png`, `_stage_states_hat_pedestal_rail.png`.

---

## LANES / PAINTER — **REVEAL**

**THE SCENE.** The gallery. Three easels stand across the frame, one per third, each holding a big canvas under a draped dust cloth — folds painted with real weight and shadow, one corner lifted on the left one showing a glimpse of coral underneath. The floor is a paint-spattered drop cloth. Along the bottom edge: a palette loaded with plum, coral, cream and teal, three loaded brushes, a rinse cup of cloudy water, open paint pots. On the back wall, the **colour order board** showing the swatch to look for. A skylight above with motes drifting in its beam.

**WHAT MOVES.** `_lit.png` cells — that cloth **whipped off** mid-air, billowing, with the painting revealed beneath: a framed sunrise over the reef, glowing. `_fill.png` bottom strip — a row of finished small canvases leaning against the wall along the floor, accumulating.

**PROGRESS.** 10% one small canvas leaning. 50% four leaning. 100% a full row with a gold-framed one in the centre.

**SUCCESS.** The big framed sunrise on the gallery wall under a picture light, the dust cloth pooled on the floor, palette and brushes at rest.

**INGREDIENTS.** Canvases, dust cloths, easels, palette, brushes, paint pots (plum/coral/cream/teal), rinse cup, drop cloth, frames.

**FILES.** `widget_lanes_painter.png` 1024×576 · `_lit.png` 768×256 · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_painter_gameplay_canvas_blank.png`, `_canvas_finished.png`, `_framed_sunrise.png`, `_palette.png`, `_coral_paint_pot.png`, `_color_order_board.png`, `_stage_states_gallery_reveal.png`, `_drop_cloth.png`.

---

## LANES / ASTRONAUT — **PIPES**

**THE SCENE.** The engine room pipe wall. A great brass-and-glass pipe run climbs the back wall with **one obvious gap** dead centre-top — a missing segment, its two open flanges bolted and waiting, a wisp of steam escaping, a coral shell-lamp blinking beside it. Below, on a workbench running across the frame, lie three candidate pieces, one per third: a straight length, a 90° elbow, a ring coupler — each a real object with brass flanges, rivets and a glass window showing aqua fuel, a wrench lying beside them. Bubbles drift upward. Through a porthole at the right, the purple bubble-city.

**WHAT MOVES.** `_lit.png` cells — that piece **fitted** into the gap: flanges clamped, aqua fuel surging through its glass window, a ring of light and three bubbles. `_fill.png` bottom strip — the pressure lamp bank along the bench front lighting up with a rising bubble stream above it.

**PROGRESS.** 10% one lamp, a few bubbles. 50% half the bank, steady bubbles. 100% the whole bank aqua-bright, bubbles streaming.

**SUCCESS.** The pipe run complete and glowing end to end, fuel racing through every glass window, the rocket lit and ready beyond the porthole.

**INGREDIENTS.** Straight/elbow/ring pipe segments, flanges, rivets, wrench, glass windows, aqua fuel, bubbles, shell lamps, porthole.

**FILES.** `widget_lanes_astronaut.png` 1024×576 · `_lit.png` 768×256 · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_astronaut_engineer_gameplay_straight_pipe.png` / `_elbow_pipe.png` / `_ring_pipe.png`, `_straight_fitted.png` / `_elbow_fitted.png` / `_ring_fitted.png`, `_*_ghost_slot.png`, `_stage_states_pipe_wall.png`, `_pipes_complete.png`, `_pressure_lamps.png`.

---

## LANES / POPSTAR — **DANCE**

**THE SCENE.** The concert catwalk from above and in front. Three big illuminated dance pads fill the frame, one per third — thick pearl-rimmed plates with a coloured arrow inlaid under glass: left arrow, up arrow, right arrow, chunky and rounded, each with a soft under-glow and a scuff of stage dust. Around them the catwalk deck with cable runs taped down and a coiled mic cable; the glow-stick rail below. Behind, the rainbow backdrop and two speaker stacks; above, a truss of par-cans throwing coloured beams through haze. At the top of the frame a **stage monitor** displays the arrow to copy, big and bright.

**WHAT MOVES.** `_lit.png` cells — that pad **stomped**: the glass blazing, a shockwave ring of light spreading across the deck, four notes and two hearts popping out, dust jumping. `_fill.png` bottom strip — the glow-stick rail rising: a field of glow-sticks lifting into the air, confetti beginning above them.

**PROGRESS.** 10% a handful of glow-sticks up. 50% half the rail up, confetti starting. 100% every glow-stick up, confetti thick, beams crossing overhead.

**SUCCESS.** Roshan mid-pose on the centre pad, all three pads blazing, confetti falling, the crowd's lights a solid field.

**INGREDIENTS.** Arrow pads, glow-sticks, confetti, speaker stacks, par-cans, mic cable, stage monitor, shell tambourine, rainbow backdrop.

**FILES.** `widget_lanes_popstar.png` 1024×576 · `_lit.png` 768×256 · `_fill.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_pop_star_gameplay_left_arrow.png` / `_up_arrow.png` / `_right_arrow.png`, `_pressed_arrow.png`, `_stage_monitor.png`, `_dance_sequence.png`, `_stage_states_arrow_lane.png`, `_glow_stick_rail.png`, `_catwalk.png`.

---

# PART 5 — CHARGE (5 beats)

*Engine: `_glow` (256²) is drawn **centred** and scales 108→234px as `widget_fill` grows; `_full` (1024×576) is revealed **bottom-up** across its ink band. Two hard rules follow: **the thing that charges must be at the exact centre of the backdrop**, and **`_full` must be a vertical, bottom-stackable strip**. All five need `_full.png` replaced — today every one of them is a single mint rounded rectangle pinned to the right edge.*

---

## CHARGE / BALLERINA — **WATCH**

**THE SCENE.** The stage from the wings — we are watching, not dancing. Dead centre, in a beam that comes down from the top of the frame, the prima teacher is caught mid-demonstration: a coral-tailed dancer in a pearl tutu, arms in fifth, one foot pointed, ribbons floating. Around her, the floor's shell rosette. Behind, mirror panels reflecting her three times over, a barre with pointe shoes hanging by their ribbons, and coral and teal wing curtains. Dust motes drift in the beam. Along the bottom, the front edge of the stage with the orchestra's brass bells and an open music box. **In the backdrop everything is dim** — the beam faint, the mirrors dull, the curtains in shadow.

**WHAT MOVES AND HOW.** `_glow.png` (256²) — a soft cream-and-rose radiance: concentric petal-shaped light blades with a lens bloom and a few floating petals, alpha-feathered to nothing at the edge; grows around the dancer as attention builds. `_full.png` (ink band **x 300–740, y 40–560**) — the **full beam**: a column of warm light from the flies down onto her, dust motes and petals suspended in it, the floor rosette blazing at the bottom. Bottom-up reveal reads as the light pool forming on the floor first, then the column climbing to its source.

**PROGRESS.** 10% a faint pool of light around her feet. 50% the column half-built, petals visible inside it, her tutu catching the edge light. 100% the beam complete floor to flies, mirrors ablaze with reflections, petals falling through it.

**SUCCESS.** The teacher in a held penché inside a full spotlight, petals raining — and the three mirror panels doing it too, so it's a wall of dancers.

**INGREDIENTS.** Tutu, pointe shoes, ribbons, petals, dust motes, mirror panels, barre, brass bells, music box, wing curtains.

**FILES.** `widget_charge_ballerina.png` 1024×576 · `_glow.png` 256² scaling sprite · `_full.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_ballerina_stage_states_spotlight_pool.png`, `_watch_state.png`, `_mirror_panels.png`, `_practice_barre_unit.png`.

---

## CHARGE / FARMER — **MUD HOP**

**THE SCENE.** A great mud puddle fills the lower two-thirds of the frame — glossy chocolate-brown, reflecting the sky and the barn upside down, with ripple rings and a few floating straws. Standing dead centre at its rim, coiled and grinning, a piglet mid-crouch: back legs bunched, tail wound into a spring, shadow pooled tight under it, three mud freckles already on its snout. Around: churned earth and boot prints, clover, a dropped welly on its side, a fence post with a coil of rope, the red barn and sunflowers behind, a washing line with two aprons flapping.

**WHAT MOVES AND HOW.** `_glow.png` (256²) — a mud-splat charge: a ring of brown droplets and motion arcs over a warm gold anticipation halo. `_full.png` (ink band **x 130–900, y 200–560**) — the **splash crown** rising out of the puddle: a low ripple at the bottom of the band, a rising rim, then a full crown of mud with droplets arcing off it and a thin rainbow caught in the spray at the top.

**PROGRESS.** 10% one ripple ring and two droplets. 50% a knee-high mud crown, droplets in the air, the piglet lifting off its heels. 100% a splash crown taller than the piglet, droplets everywhere, the piglet airborne at its peak.

**SUCCESS.** The piglet at the apex of a magnificent muddy splash, all four trotters out, freckled head to tail, three other piglets cheering from the fence rail.

**INGREDIENTS.** Mud, puddle, ripples, droplets, straw, clover, welly boot, boot prints, fence, rope, barn, sunflowers, aprons, piglets.

**FILES.** `widget_charge_farmer.png` 1024×576 · `_glow.png` 256² scaling · `_full.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_farmer_gameplay_mud_splash.png`, `_piggy_hop.png`, `_stage_states_mud_puddle.png`, `_fed_piggy_hop.png`.

---

## CHARGE / MAGICIAN — **VANISH**

**THE SCENE.** Centre stage on a star-velvet trick table sits a single top hat, brim toward us, mouth open like a dark well — and hovering just above it, the cloud-fluffy bunny-fish, ears up, about to disappear. Hat and bunny occupy the exact centre. Around them: plum wing curtains with gold tassels, a pearl wand lying on the table, a bell jar with one bubble in it, a rolling mirror panel, and a lacquer floor throwing a soft double of everything. Sparkle motes and small purple stars drift — sparse and dim to start.

**WHAT MOVES AND HOW.** `_glow.png` (256²) — a violet conjuring aura: a many-pointed star-flare with a soft pearl core and a ring of tiny four-point sparkles, alpha-feathered. `_full.png` (ink band **x 260–780, y 30–560**) — the **vanishing column**: a vortex of star-shot smoke wrapping the hat, thick and swirling at the bottom with a ring of light where it meets the brim, thinning into a spray of stars and floating pearls at the top.

**PROGRESS.** 10% a curl of smoke around the brim, three stars. 50% the vortex up to the bunny's shoulders, pearls orbiting, its edges going translucent. 100% a full column of stars to the top of frame, the bunny almost pure light.

**SUCCESS.** The hat alone on the table, one last star settling into it and a single pearl spinning on the brim — and the bunny-fish popping up from behind the curtain, delighted, in a TA-DA starburst.

**INGREDIENTS.** Top hat, bunny-fish, pearl wand, star-velvet cloth, bell jar, smoke, stars, pearls, curtains, tassels, mirror panel.

**FILES.** `widget_charge_magician.png` 1024×576 · `_glow.png` 256² scaling · `_full.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `goal_magician.png` (the bunny is already painted — reuse it), `opera_job_magician_gameplay_hat_open.png`, `_decoy_bubble_puff.png`, `_stage_states_final_reveal.png`, `_trick_table.png`.

---

## CHARGE / ASTRONAUT — **LAUNCH**

**THE SCENE.** The launch pad from ground level, low and heroic. Dead centre, the bubble-rocket on its pad: cream hull, coral fins, brass bands, a pearl-ringed porthole with a small helmeted face at it, engine bell aimed down at us — dark and cold, with frost on the lower hull. Around it: the gantry with a walkway and a ladder, coiled fuel hoses running to the pad, a bank of shell-lamps, drifting bubbles, and the purple bubble-city and moons on the horizon. Two crew fish in helmets wave from the gantry rail.

**WHAT MOVES AND HOW.** `_glow.png` (256²) — an ignition bloom: a hot white core, aqua corona, six radiating light spikes and a spray of bubbles. `_full.png` (ink band **x 330–700, y 120–560**) — the **fire climbing the rocket**, painted so it stacks correctly bottom-up: at the base of the band a boiling cushion of aqua fire and bubble-smoke on the blast deflector; through the middle, the fire climbing and wrapping the fins in glow; at the top, the hull lit from below, porthole blazing, frost burning off.

**PROGRESS.** 10% a smoulder of aqua sparks on the deflector, two bubbles. 50% a rolling cushion of fire and bubble-smoke up to the fins, fins glowing, hoses whipping. 100% fire filling the pad, whole hull lit, porthole blazing, frost gone, every gantry lamp aqua.

**SUCCESS.** The rocket clear of the pad on a pillar of aqua fire and bubbles, the gantry falling away, the crew fish cheering, moons behind it.

**INGREDIENTS.** Rocket, engine bell, fins, porthole, gantry, ladder, fuel hoses, shell lamps, bubbles, frost, blast deflector, crew fish, moons.

**FILES.** `widget_charge_astronaut.png` 1024×576 · `_glow.png` 256² scaling · `_full.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_astronaut_engineer_gameplay_rocket_front.png` / `_rocket_side.png`, `_bubble_launch.png`, `_stage_states_launch_pad.png`, `_prelaunch_glow.png`, `_mobile_gantry.png`, `world_astronaut.png` (horizon).

---

## CHARGE / POPSTAR — **SOUND CHECK**

**THE SCENE.** The empty hall, seen from the stage. Dead centre and close, a big chrome-and-pearl **microphone** on a stand, head-on, its shell-shaped grille catching a hot rim of light, cable coiling down to the deck. Behind it, in cool blue half-light, the venue: two speaker stacks flanking, a truss of unlit par-cans, the rainbow backdrop dull grey-violet, rows of empty seats, the glow-stick rail dark. A stool at the left with a shell tambourine and a water bottle. Dust hanging in the air.

**WHAT MOVES AND HOW.** `_glow.png` (256²) — a rose-gold sound bloom: nested ripple rings with a pearl core and a scatter of musical shell-notes. `_full.png` (ink band **x 60–980, y 60–560**) — the **hall waking**, bottom-up: at the base, the glow-stick rail lighting along the floor and the front rows filling with silhouetted fans; through the middle, the speaker cones pulsing with visible ripple rings and confetti cannons priming; at the top, the par-can truss igniting and the rainbow backdrop blazing with beams and haze.

**PROGRESS.** 10% a few glow-sticks along the floor, one lamp warm. 50% front rows full, speakers rippling, half the truss lit. 100% the whole hall packed with light, every beam on, the backdrop a full rainbow, confetti in the air.

**SUCCESS.** Roshan at the mic, mouth open on a big note, the hall a wall of light and raised glow-sticks, confetti falling, notes streaming out of the speaker stacks.

**INGREDIENTS.** Microphone, mic stand, cable, speaker stacks, par-cans, glow-sticks, confetti, shell tambourine, water bottle, stage monitor, seats.

**FILES.** `widget_charge_popstar.png` 1024×576 · `_glow.png` 256² scaling · `_full.png` 1024×576 progressive · `_success.png` 1024×576.
**REF.** `opera_job_pop_star_gameplay_microphone_idle.png` / `_active.png` / `_finale.png`, `_microphone_stand.png`, `_speaker.png`, `_stage_states_speaker_stacks.png`, `_pearl_light_frame.png`, `_rainbow_backdrop.png`, `_glow_stick_rail.png`.

---

# PART 6 — CATCH (1 beat)

*Engine (`scripts/opera_nursery_catch.gd`): backdrop stretched to the panel; `_pillows` drawn into `Rect2(0, 0.78h, w, 0.22h)`; `_cradle` (256²) drawn ~116px wide with its rect top at `catch_point.y − 1.55r` — so the cradle art's bowl must sit in the **lower ~65% of the cell** with hands reaching to the top corners; babies fall from the top at up to 86px; caught babies settle at 0.89h beside the cradle; missed babies rest on the pillows at 0.82h and are gently returned.*

---

## CATCH / NURSERY — **CATCH BABIES**

**THE SCENE.** The nursery at bedtime, seen as a tall warm room. Across the top, a wide ceiling **mobile** — a carved wooden hoop hung on ribbons with felt fish, a moon and three little stars turning beneath it — painted as a real object so the babies have a place to come from. The walls are papered in a soft shell-and-star pattern. A high window at the right shows deep blue evening and one big moon, its light falling in a warm shaft across the room. Left wall: a tall painted dresser with a stack of folded muslins, a bottle warmer with a glowing element, three tiny bonnets on pegs, a shelf of picture books, a wind-up music box. Right: a rocking chair with a knitted blanket over the arm and a basket of soft toys — a plush octopus, a rag seahorse, a knitted crab. The floor is a big round rag rug in coral and cream. Everything is lamplit, warm-pooled, long-shadowed, and unmistakably **safe** — padded, rounded, nothing sharp anywhere.

Along the whole bottom of the room, filling the floor edge, is a heaped bank of **pillows** — not five ellipses but a proper drift: fat cotton pillows with piping and buttons, a folded quilt, two rolled bolsters, a knitted blanket spilling over, tassels, a scatter of soft felt stars. Painted with real fabric weight, folds, and contact shadow.

**WHAT MOVES AND HOW.**
- `widget_catch_nursery_cradle.png` (256², **replace**) — Roshan's arms and carry-blanket: two forearms in coral sleeves curving up into a broad open cradle, a cream muslin slung between them like a hammock and pinned with a shell brooch, hands open at the ends. Bowl in the lower 65% of the cell, hands to the top corners, a gentle blue-white safe-glow beneath so the catch zone reads against the rag rug. Follows the finger.
- `widget_catch_nursery_pillows.png` (**1024×128**, replace the five flat ellipses) — the painted pillow drift above, alpha feathering into the room at its top edge.
- `widget_catch_nursery_babies.png` (768×256, three cells — **optional upgrade** to the existing `nursery/baby_0..2.png`) — the three babies painted to read as *falling and delighted*: arms up, one giggling, one blowing a bubble, one clutching a knitted crab; each with a small muslin fluttering above like a parachute and a trail of two soft bubbles.
- `widget_catch_nursery_fill.png` (1024×576 progressive, ink band **x 30–250, y 120–500**) — the **cradle shelf** on the left wall filling bottom-up: moses baskets, each with a tucked blanket, a sleeping baby, and a small star hanging above it. *(Needs one `_draw_progress_overlay()` call added to `opera_nursery_catch.gd:_draw()`.)*
- Cheap motion: give the mobile a ±3° sway tween about its hanger point. One tween, no new art.

**THE MOMENT OF PROGRESS.** 10% one baby asleep in a basket on the bottom shelf. 50% three baskets filled, the shelf half lit, two stars hung. 100% five baskets, every one starred, the whole shelf glowing warm.

**THE SUCCESS IMAGE.** All five babies asleep in a row of moses baskets on the shelf, blankets tucked, the mobile turning above, the moon in the window, one bubble drifting up — and Roshan's arms empty and folded, resting. Held.

**INGREDIENTS.** Babies, muslins, moses baskets, blankets, bonnets, bottle warmer, plush octopus / knitted crab / rag seahorse, mobile with felt fish and moon, rag rug, rocking chair, pillows, bolsters, quilt, music box, picture books, night-lamp, bubbles, stars.

**FILES.** `widget_catch_nursery.png` 1024×576 painted · `_cradle.png` 256² finger-tracked sprite · `_pillows.png` 1024×128 painted band · `_fill.png` 1024×576 painted progressive · `_success.png` 1024×576 painted · `_babies.png` 768×256 three-cell sheet (optional).

---

# PART 7 — PRODUCTION ORDER

**Batch 1 — prove the format on one beat, end to end.** `chef BAKE`. It's the owner's own reference career, it exercises every new piece (full-screen backdrop, per-career needle, progressive `_fill`, `_success`), and the cake in the tin rising is the most direct answer to "I want to see ingredients in a bowl." Ship it, look at it on the tablet, then commit to the rest.

**Batch 2 — charge (5).** Biggest visible gain per file: five mint rectangles become five painted scenes filling from the floor up, and no new engine code is needed beyond the panel resize.

**Batch 3 — track (8) and gauge (2 remaining).** Needs the one-line `_fill` addition per template plus the per-career `_needle`/`_hit` loads.

**Batch 4 — lanes (10).** Largest count and needs the `_lit` draw size bumped from 124px to ~320px with a short hold after a correct pick, otherwise the best art in the batch stays invisible.

**Batch 5 — catch (1).** Standalone script; do it last so the room can borrow finished nursery props from the track/BURP scene.

**Total new/replaced files in my group: 27 backdrops, 27 `_fill`/`_full` progressive layers, 27 `_success` layers, 8 track movers, 8 track hits, 3 gauge needles, 5 charge glows, 10 lane sheets, 3 catch layers — 118 PNGs, every one ≤ 1024px on its longest side.**

## Key file paths

- Engine contract: `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_gesture_surface.gd` (`_load_widget_set()` ~line 110, `_draw_widget_layers()` ~line 486, `_draw_progress_overlay()` ~line 440, `_ink_bounds()` ~line 415)
- Panel sizing: `.../scripts/opera_career_world_2d.gd:406-417` and `:741-745`
- Catch: `.../scripts/opera_nursery_catch.gd:225-296`
- Target folder: `.../assets/opera/worlds/widgets/`
- Caliber refs: `.../assets/opera/worlds/props/goal_chef.png`, `goal_magician.png`; `.../assets/opera/worlds/backdrops/world_chef.png`, `world_astronaut.png`
- Content refs: `.../assets_src/concepts/opera_jobs_flat_2026-07-21/cards/opera_job_<career>_gameplay_*.png` and `_stage_states_*.png`
