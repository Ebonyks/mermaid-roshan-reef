# OBJECT INVENTORY — Opera career worlds

## 0. READ THIS FIRST: the paintings I was asked to inventory are not the paintings the game draws

Before any of the object findings are usable, two structural facts have to land.

**(a) The runtime backdrop is the 4-tile set, not `world_<career>.png`.**
`C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_world_backdrop_2d.gd` line 98:

```gdscript
var active_tiles: Array[Texture2D] = stage_tiles if stage_mode and stage_tiles.size() == 4 else world_tiles
if active_tiles.size() == 4:
    _draw_tile_set(active_tiles)
    return          # <-- the single painting is never reached
```

All 13 careers have a complete `world_<career>_c{0,1}r{0,1}.png` set (commit `013bfcf7`, "art(opera): deliver remaining Codex regeneration set", Aug 2 20:36, an ancestor of HEAD `d8369f4b`). So `painting` — the file the coordinates in `opera_stage_paths.gd` were derived from — is dead code on every career.

**(b) Seven of twelve careers are now a completely different painting.**

| Same composition (2x re-render) | Entirely new painting |
|---|---|
| chef, detective, ballerina, candymaker, doctor | **farmer, boxer, magician, painter, astronaut, racer, popstar** |

The seven new ones are not variations — they are different places. The magician's three top-hat buildings, bridge, door gallery and moon pool are gone, replaced by three curtained stage booths on a coral seabed. The farmer's green hills, red barn, orchard, picnic blanket and mud pen are replaced by an underwater coral farm with a 3×3 grid of nine empty planting beds. Painter's three paint pots survive but the deck, bridge and splat garden are replaced by three blank easels. Every `landmark` string in `opera_stage_paths.gd` for those seven careers describes furniture that no longer exists, and Roshan walks a route derived from a floorplan that is gone.

**(c) Even on the five that kept their composition, every coordinate is offset.**
The delivered tiles inset the artwork inside a blurred bleed margin. Measured across all 13 careers, sharp content spans **x 0.100 → 0.900** of the composed 2048×1152 frame (y likewise ≈0.10→0.90 where the sky has enough contrast to measure). The draw code maps that whole frame — bleed included — to the full 1280×720 screen. So the mapping from the coordinates in `opera_stage_paths.gd` to where the object actually renders is:

```
screen_u = 0.10 + 0.80 * recorded_u
screen_v = 0.10 + 0.80 * recorded_v
```

Error is zero at screen centre and grows to **±128 px horizontally, ±72 px vertically** at the edges. Evidence image: `C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/c441481e-23f9-41be-93fd-e1ce21bf78fc/scratchpad/out/offset_chef.png` (red = where the code draws the sparkle, green = where the painted object is).

Nothing in this report about "good touch targets" is actionable until the coordinate table is re-derived against the tile composites.

---

## 1. PER-CAREER OBJECT INVENTORY

Coordinates below are **as recorded in `opera_stage_paths.gd`** (i.e. positions in the source painting). Apply the 0.10 + 0.80×  transform to get screen positions.

One general note that applies to all twelve: **station `pos` is a standing spot on the floor, not the object.** `stations_chef.png` shows S1–S5 all landing on bare tile in front of / below the landmark. The pulsing station marker currently pulses over empty pavement. An exploration layer that wants a tappable object needs a second anchor per station, roughly 60–120 px above the standing spot.

### chef — composition intact (same art, inset)
The richest of the five for touch targets.

| Clue | Recorded | What is actually painted there |
|---|---|---|
| C1 | 0.42, 0.095 | **Glowing gold filigree hanging lantern**, suspended from the red curtain valance. Dead-centre hit. |
| C2 | 0.728, 0.12 | **Second glowing hanging lantern**, same design. Dead-centre hit. |
| C3 | 0.483, 0.10 | **Empty violet sky** between the lantern and a distant cherry-topped cake-tower. Dead space. |
| C4 | 0.073, 0.185 | **Gold scallop-shell crest with pearl**, crowning the left entry arch over its purple drapes. |
| C5 | 0.25, 0.30 | The gap between two shelves of the spice etagere; **three glass spice jars** (pink sprinkles, tan sugar, teal sugar) sit ~20 px below-left, covered pots above. |
| C6 | 0.74, 0.23 | **Cluster of small cream-and-yellow flowers** potted on the lip of the big cream urn. |
| C7 | 0.085, 0.815 | **Bowl of dark red cherries with stems**, foreground lower-left ledge. |
| C8 | 0.94, 0.775 | **Canvas piping bag with gold nozzle**, lying beside a swirl of cream and a coil of pink icing. |

Stations: S1 floor below the giant pink-and-cream **mixing bowl with whisk** (little step stools beside it); S2 at the foot of the **red footbridge**, the **glowing arched hearth oven** up-right; S3 below the **gold étagère of three cakes** (yellow, pink, purple); S4 below the **glass-domed macaron cart on wheels**; S5 on the **red carpet steps** up to the three-tier celebration cake under its curtained proscenium.

Unlisted but excellent nearby: the whisk standing in batter, a small bowl of pink frosting with a spatula, potted palms, rope-and-pearl stanchions, the water inlet under the bridge, distant city domes.

### detective — composition intact (same art, inset)
Night scene, and the only world with painted *narrative* detail.

| Clue | Recorded | What is actually painted there |
|---|---|---|
| C1 | 0.33, 0.08 | **Empty starfield**, just below-right of the crescent moon (moon centre ≈0.318, 0.062). |
| C2 | 0.645, 0.095 | **The giant gold magnifying glass** on the tower — the lens itself. Perfect hit. |
| C3 | 0.92, 0.10 | **A warmly lit arched window** in the distant city facade. |
| C4 | 0.652, 0.31 | **Tall violet stained-glass arched window**, gold-framed, at the magnifier tower's base. |
| C5 | 0.42, 0.40 | **A teal-and-red X-strapped evidence lockbox** on the display shelf (a whole shelf of them). |
| C6 | 0.125, 0.48 | Bare teal walkway tile beside a potted plant. A **glowing purple paw print** sits ~0.135, 0.52. |
| C7 | 0.605, 0.71 | **A cute fish inside a bubble cloud**, lit from above in a display alcove. A painted creature with a face already in the scene. |
| C8 | 0.32, 0.88 | **A purple domed treasure trunk** on a foreground plinth. |

Stations: S1 below the **arched shelf of patterned evidence lockboxes**; S2 the **round pedestal of purple and pink hat-boxes**; S3 the **magnifier tower**; S4 the **three arched dressing mirrors** in the bookshelf wall; S5 the **open treasure chest with pearl tiara** under the domed pavilion.

Two painted features nobody has wired up and should: the **glowing paw-print trail** running the full width of the mid walkway (purple → teal → pink, ~14 prints) and, in the lower alcoves, **a box drawn with motion wiggle-lines** — a shaking box, already painted as "something is in here."

### ballerina — composition intact (same art, inset)

| Clue | Recorded | What is actually painted there |
|---|---|---|
| C1 | 0.17, 0.13 | **Empty sunset sky**, immediately right of a lit lamp-post globe. |
| C2 | 0.07, 0.33 | **Gold pearl-and-shell crest** on the dressing alcove arch. |
| C3 | 0.47, 0.28 | **A floating teal-and-pink ribbon streamer with sparkles**, inside the bandstand dome above the golden treble-clef shell. |
| C4 | 0.72, 0.22 | **A distant pink-domed pavilion** on the far hillside — hazy background scenery, small. |
| C5 | 0.905, 0.26 | **The giant rose bouquet with teal ribbon bow** on the finale dais. |
| C6 | 0.05, 0.81 | Underside of the walkway rim among foreground leaves — a small gold hook, otherwise nothing. |
| C7 | 0.57, 0.83 | **A gold ball finial** on a foreground rope-post, surrounded by hydrangeas. |
| C8 | 0.815, 0.72 | **A giant pink rose blossom**, foreground garden. |

Stations: S1 **gold-framed dressing alcove** with red drapes and teal inner curtains; S2 **teal wave-embroidered practice tuffets** on the mosaic causeway (five of them, in a row — a natural sequence); S3 **pearl-studded bandstand with treble-clef shell stage**; S4 **gold trifold rehearsal mirror**; S5 **rose finale dais**.

### farmer — ART REPLACED. Old inventory void.
`world_farmer.png` (terrestrial: green hills, red barn, apple orchard, hay-bale staircase, mud pen, gingham picnic) is not what renders. Runtime is an **underwater coral farm at sunset**. Contents, in screen-normalized coordinates:

- **Red barn** with round porthole window, big X-braced double doors, brick chimney, **a fish weathervane** on the ridge, starfish stuck to the walls — x 0.10–0.28, y 0.13–0.42.
- **Coral-and-driftwood fence** running left to right, y ≈ 0.35–0.42.
- **Blossom trees** (pink coral-flower canopies) at x ≈ 0.30, 0.42, 0.54, 0.63 — four of them.
- **A flower-covered arch gateway** over the sand path at x ≈ 0.44, y 0.28–0.42.
- **Setting sun with rays**, x ≈ 0.58, y ≈ 0.22.
- **Stack of hay bales** (three big rolls, one with a starfish on it), x 0.77–0.88, y 0.24–0.40.
- **Nine empty dark planting beds** ringed with pebbles and tiny coral, in a clean 3×3 grid: columns x ≈ 0.565 / 0.655 / 0.745, rows y ≈ 0.505 / 0.575 / 0.645.
- **Giant pink clam with a pearl** at 0.14, 0.71; **sea sponges / tube corals** at 0.10–0.20, y 0.55–0.70 and 0.68, 0.78; **orange starfish** on the sand at 0.22, 0.79 and 0.57, 0.79; scattered **bubbles** in the upper water.

The nine beds are the standout: a ready-made nine-slot interaction grid, painted empty and clearly waiting to be filled.

### magician — ART REPLACED. Old inventory void.
No moon, no top-hat buildings, no enchanted-door gallery, no scrying pool. Runtime is **three curtained stage booths on a coral seabed**:

- **Purple booth** (x 0.16–0.33, y 0.20–0.60): shell crest with pearl, swagged purple curtains drawn open, lit empty stage floor, stepped base.
- **Teal booth** (x 0.42–0.60, same band): identical grammar, teal.
- **Coral/red booth** (x 0.68–0.85): identical grammar, coral.
- **Pearl lamp posts** with glowing white globes at x ≈ 0.115/y 0.42, 0.37/0.42, 0.62/0.40, 0.88/0.38 — four of them, plus two more small ones.
- **Two giant open clam shells with pearls**, foreground: 0.16, 0.78 and 0.75, 0.79.
- **Filigree background arches** at x ≈ 0.37, 0.58, 0.68 (y 0.15–0.35), a **starfish** at 0.10, 0.71, **glowing star sparkles** scattered on the sand, and a **winding gold-edged path**.

Three identical booths with drawn curtains and empty lit stages is, structurally, a "which one is it behind" set-piece painted and waiting.

### The other seven, briefly

- **candymaker** (composition intact): C1 = gold shell finial on the red gumball boiler dome with a steam plume; C2 = a purple pipe elbow in the factory plumbing; C3 = empty pipework, the **red/green gauge dial with needle** on the taffy press sits just below; **C4 = a teal round candy with a kawaii face** — one of a row of **seven candy characters with faces** (wrapped candy, heart-eyed drop, red cloud, teal shell, red round, purple star) riding the overhead rail from x 0.55 to 0.93 at y ≈ 0.26; C5 = a distant hazy pipe cupola; C6 = a gold lamp-post finial beside a **candy-bag cottage with a pink bow and arched wooden door** (three such cottages); C7 = a purple candy vat dome with a teal shell finial; C8 = a gold railing post in dark foreground. The seven faced candies are the single best untapped asset in the whole set.
- **doctor** (composition intact): C1 = red-curtained arched window; C2 = gold crest on the teal dome; **C3 = the giant purple stethoscope** on the clinic roof; **C4 = floating soap bubbles** above a shell fountain; C5 = pearl cluster on a plain teal wall arch; **C6 = a red heart medallion** crowning an exam booth (five booths, five hearts, x ≈ 0.58/0.65/0.765/0.86/0.95); C7 = a stone arch over a **waterfall spill**; C8 = empty lawn beside a teal beach parasol. Also painted: **a smiling starfish patient** with a face on a purple cushion at ≈0.05, 0.50, a giant thermometer, a giant bandage on the bridge, and loose props on the exam beds.
- **boxer** — ART REPLACED: three podiums on a pool-blue floor (purple flat dais 0.20/0.62, teal punching cylinder 0.50/0.42, red-and-purple cylinder 0.73/0.42), a **shelf rack of red/purple/teal boxing gloves** (x 0.12–0.22, y 0.24–0.42), **two pairs of gloves hanging from a rail** at 0.33–0.40/y 0.22, a purple pavilion, a small coral chair, starfish on the floor.
- **painter** — ART REPLACED: **three blank white easel canvases** (x ≈ 0.19/0.40/0.80, y 0.20–0.40) — literally empty rectangles waiting for content — **three drip-glazed paint pots** (purple 0.22/0.53, coral 0.50/0.53, cream 0.78/0.53), **two artist palettes with paint blobs** (0.135/0.32 and 0.755/0.35), **a jar of brushes** (0.25/0.33), **a giant rainbow-bristled brush** with rainbow paint streams (0.63/0.25), coral gardens.
- **astronaut** — ART REPLACED: **three glass-domed habitat pods** with star-shaped windows (x ≈ 0.19/0.46/0.58, y 0.13–0.35), **three lab machines on flower-shaped pads** (glass cylinder 0.23/0.47, elbow pipe 0.47/0.44, big ring/torus 0.71/0.45), **three flower-shaped floor hatches** (0.20/0.60, 0.47/0.60, 0.72/0.60), a **control tower with hand-wheel valve and a pearl-shell top** (0.71/0.22), a **red-and-cream rocket** (0.85/0.25), bubble streams, a small Saturn-like planet at 0.30/0.15.
- **racer** — ART REPLACED: an **oval aqua track**, **three pearl-orb trophy pedestals** (teal 0.33/0.55, purple 0.51/0.53, pink 0.65/0.55), **a domed grandstand pavilion** (0.50/0.32), **four pennant flags on poles** (0.24/0.15, 0.32/0.15, 0.64/0.15, 0.76/0.16), **two pearl start arches** (0.14/0.42, 0.83/0.40), a **checkered ribbon with a bow** (0.81/0.55), coral and clams.
- **popstar** — ART REPLACED: **three performance stages** — a giant purple shell stage with **four round speaker cones** and a pearl-garland curtain (x 0.13–0.30), a **coral gazebo with a silver microphone on a shell** (0.42–0.58), a **teal orb stage with a treble clef and music notes** (0.66–0.83) — a **rainbow ribbon road** sweeping behind them, **floating music notes** at 0.12/0.25, 0.30/0.20, 0.60/0.28, 0.68/0.30, 0.78/0.22, 0.88/0.20, and a foreground reef of clams, starfish and pearls.

---

## 2. GOOD TOUCH TARGETS (and what the response should be)

Ranked by how directly a 4-year-old would reach for them.

**Tier 1 — a child will poke these without being told.**

| Object | Where | Response |
|---|---|---|
| Faced candy characters ×7 | candymaker, y≈0.26, x 0.55–0.93 | Squash-and-stretch bounce, blink, a small "boop"; they're already smiling — make them react. |
| Hanging lanterns ×2 | chef C1, C2 | Swing on their hook, brighten, warm glow bloom, soft chime. |
| Fish in the bubble | detective C7 | Fish wiggles, bubbles rise and pop. |
| Smiling starfish patient | doctor ≈0.05/0.50 | Waves an arm, giggle SFX. |
| Soap bubbles | doctor C4 | Pop on touch, one at a time, each a different pitch. |
| Giant magnifying glass | detective C2 | Lens flashes, briefly reveals every hidden sparkle at once. |
| Giant stethoscope | doctor C3 | Thump-thump heartbeat sound, the heart medallions pulse in time. |
| Cherry bowl / piping bag | chef C7, C8 | Cherries jiggle and one rolls; piping bag squeezes out a cream swirl. |
| Rose bouquet, giant rose | ballerina C5, C8 | Petal burst, bloom-open. |
| Nine planting beds | farmer runtime, 3×3 grid | Tap a bed → a coral sprout grows. Nine beds = nine touches = a complete, countable act. |
| Three blank easels | painter runtime | Tap → the canvas fills with a picture. The best "your touch made a thing" beat in the set. |
| Three curtained booths | magician runtime | Tap → curtains sweep open, something appears on the lit stage. |
| Boxing-glove rack + hanging gloves | boxer runtime | Gloves swing and bonk together. |
| Pearl lamp posts ×6 | magician runtime | Light up one by one; light them all → the whole scene brightens. |

**Tier 2 — good, needs the object to be found first.**

Spice jars (chef C5), evidence lockboxes (detective C5 — rattle then pop open), stained-glass and lit windows (detective C3/C4, doctor C1 — glow up), shell crests on every arch (chef C4, ballerina C2, doctor C2 — sparkle and pearl-shine), heart medallions ×5 (doctor C6 — pulse), floor hatches ×3 and star windows ×3 (astronaut), speaker cones ×4 (popstar — pulse to a beat), pennant flags ×4 (racer — flutter), gauge needle (candymaker — swings), waterfall (doctor C7 — splash), flower-arch gateway and fish weathervane (farmer — spin), giant clams with pearls (magician, farmer, racer — open/close, pearl shines).

**The already-painted trails nobody is using.** Detective has a glowing paw-print trail across the whole mid walkway; magician has glowing star tiles scattered on the sand; painter has rainbow paint streams. These are painted *sequences* — follow-the-trail is the most contemplative one-finger mechanic available and it needs zero new art.

---

## 3. WHAT CANNOT BE DONE WITHOUT NEW ART

**Coordinates with nothing at them.** chef C3 (open sky); detective C1 (starfield); ballerina C1 (sky beside a lamp), C4 (hazy distant dome), C6 (leaf litter); candymaker C2 (pipe elbow), C5 (hazy distant cupola), C8 (railing post); doctor C5 (blank tiled wall), C8 (empty lawn); magician old C1/C3/C4 and farmer old C2 (all sky). These are not fixable by art placement — they need to be re-pointed at an object (§5).

**Responses that need a sprite that does not exist:**
- **Anything that darts, hops, flies or scuttles out.** There is no fish sprite, no crab, no bird, no butterfly, no bunny in the opera asset set. The nearest things are `assets/art35/cards/gen2/clownfish_side_clownfish_side.png`, `butterfly1_butterfly1.png` and `butterfly2_butterfly2.png` — usable flat 2D pastel cards, reasonably close in tone, but drawn for the reef, not the opera storybook palette.
- **Farm animals.** The old farmer world had a mud pen with no animal in it; the new one has no animal at all. A farm with nothing alive in it is the weakest world in the set.
- **Things to put in things.** The nine farmer beds have no crop sprite. The three painter easels have no picture to fill with. The three magician booths have nothing to reveal. Each of those is one small sprite away from being the best moment in its career.
- **Open/closed pairs.** Curtains, clam shells, evidence lockboxes, barn doors, cottage doors and treasure chests are all painted in exactly one state. "It opens" needs a second frame or an overlay sprite per object.
- **Anything living up to a "release a creature" promise.** Only two creature sprites exist in the whole opera set: `assets/opera/worlds/props/goal_magician.png` (a fluffy white bunny in a top hat, adorable, correct style) and `assets/opera/worlds/props/goal_doctor.png` (a smiling pink starfish). Plus `assets/opera/worlds/nursery/baby_{0,1,2}.png`.

**Roshan's own vocabulary is not the blocker.** `assets/characters/roshan_25d/` holds `roshan_gestures.png`, `roshan_gesture_a..d.png`, `roshan_directional.png`, `roshan_play_a/b.png` and three swim sheets, all unused, and the code still auto-glides her via `_glide_roshan_to`.

---

## 4. THE SHARED-ASSET OPPORTUNITY

The whole exploration layer can be served by **six** reusable sprites plus four existing ones. Per-career art is not needed for the response layer at all.

**Already in the repo — use these, do not re-author:**
- `assets/opera/worlds/props/fx_bop_puff.png` — pink cloud puff, reads as "poof".
- `assets/opera/worlds/props/fx_dust_puff.png` — lavender cloud, softer variant.
- `assets/opera/worlds/props/fx_dizzy_stars.png` — three gold stars on a ring; retimed as an outward burst this is a perfect generic "you found it" flourish.
- `assets/opera/worlds/props/fx_stolen_sparkle.png` — a single fat gold star, 128px.
- `assets/opera/worlds/props/fx_telegraph_ring.png` — gold sunburst ring; the ideal "this is touchable" halo, already authored.
- `assets/opera/worlds/ui/magnifier.png` — the lens.
- `assets/opera/worlds/props/goal_<career>.png` ×13 — one hero object per career, all in the right style. These are the natural reward-reveal payload: tap the last clue, the career's goal object rises out of it.

**Six new shared sprites, and the whole thing is covered:**
1. **Sparkle burst** — 4–6 frame radial twinkle, white-gold, one sheet. Fires on every successful touch, every career.
2. **Soft light-glow overlay** — one radial warm blob, additive. Turns any lantern, window, pearl, lamp post, heart medallion or lit stage into a "lights up" target. Serves ~40 painted objects across the set with one file.
3. **Ripple ring** — one expanding circle, tinted per touch. The universal "touch registered" affordance, works on water, sand, floor, anything.
4. **One generic small creature, ~2 poses + a hop** — a small pastel reef fish is the right call: it is on-world for every career (they are all underwater now), it justifies "release a creature" everywhere, and one sprite covers chef, detective, farmer, magician, boxer, painter, astronaut, racer and popstar. Style-match `goal_magician.png` for line weight and palette; the gen2 clownfish is the fallback if speed matters more than consistency.
5. **A "grown thing" — one sprout/bloom in 3 stages.** Fills the nine farmer beds, doubles as the ballerina petal bloom and the painter's splat garden.
6. **A generic curtain/lid open overlay** — one white shape, tinted at runtime. Serves magician's three booths, chef's domed cake, detective's lockboxes and chest, candymaker's cottage doors, farmer's barn doors.

Everything else per career is *tint and scale* on those six. The one place per-career art genuinely pays for itself is the three painter easel pictures — and even those can be the existing `goal_<career>.png` sprites dropped into the frames.

---

## 5. THE COORDINATE PROBLEM

**Every clue spot and station in `opera_stage_paths.gd` is wrong on screen today**, in two independent ways.

**(a) The 0.80 inset, affecting all 13 careers.** Correction is `screen = 0.10 + 0.80 * recorded`. The lens catches within 96 px (`opera_career_world_2d.gd:1651`) and reveals within 118 px, so the offset is silently survivable near centre and fatal at the edges. Measured, on the five careers whose composition survived:

| Career | Spots landing >96 px off (lens can never catch the painted object) |
|---|---|
| chef | **C4** (118 px, lands in the blurred bleed), **C7** (116, bleed), **C8** (119, bleed) |
| detective | **C3** (122, bleed), **C6** (96, on the boundary) |
| ballerina | **C1** (100), **C2** (113), **C5** (109), **C6** (124) |
| candymaker | **C2** (124), **C5** (106), **C7** (102), **C8** (126) |
| doctor | **C1** (121), **C8** (121) |

Only 10 of those 40 spots land within 60 px of their object. Fifteen land more than 96 px away, most of them out in the blurred bleed margin where there is no painting at all — a child sweeping the lens there finds a sparkle floating on a smear. Station markers carry the identical offset, so the pulsing "stand here" marker is up to 128 px off its landmark, and the walk route itself is shifted.

**(b) Seven careers point at a painting that no longer exists.** For farmer, boxer, magician, painter, astronaut, racer and popstar, no offset correction helps — the objects are gone. Their 40 clue spots and 35 stations need re-deriving from scratch against the tile composites. Spot-checking the worst: farmer's C1 "shell crest on the entry gate arch" now lands on bare coral; C7 "fence rail" lands in sand between planting beds; C8 "stone planter urn" lands in the bleed border. Magician's C1/C3/C4 pointed at a moon and floating lanterns in a night sky that has been replaced by daylit water; C5 and C6 pointed at top-hat buildings that are gone.

**Sky, water and dead space specifically** (these would feel broken even with the offset fixed, on the five intact careers): chef C3 (open sky); detective C1 (starfield — the moon is 40 px away and is a fine target); ballerina C1 (sky) and C6 (foreground leaf clutter under the walkway lip); candymaker C5 (hazy distant skyline) and C8 (dark railing); doctor C5 (blank tiled retaining wall) and C8 (empty lawn / half off-canvas at u=0.963).

**The cheapest correct fix, in order:**
1. Decide which art is canon. If the tiles are canon, delete the dead `painting` branch in `opera_world_backdrop_2d.gd` so nobody re-derives against the wrong file again.
2. Either re-slice the tiles without the 10% bleed, or apply the `0.10 + 0.80×` transform inside `OperaStagePaths` helpers — one place, fixes all 13 careers and both clue spots and stations at once.
3. Re-derive the seven replaced careers' stations, clue spots and walk routes against the tile composites.
4. While re-deriving, move every clue spot off sky/water onto a named object, and record the object name alongside the coordinate so the next art regeneration breaks loudly instead of silently. Add a second `object_pos` per station so the pulse lands on the landmark rather than the pavement in front of it.

---

**Evidence files** (scratchpad, all under `C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/c441481e-23f9-41be-93fd-e1ce21bf78fc/scratchpad/out/`): `annot_<career>.png` (clue + station overlay on the source painting), `clues_<career>.png` / `stations_<career>.png` (3× zoom crop sheets), `grid_<career>.png` (runtime tile composite with a screen-normalized tenths grid), `compare_0.png` / `compare_1.png` (source painting vs runtime tiles, all 12), `offset_chef.png` / `offset_farmer.png` (code position vs true object position), `fx_sheet.png` / `goal_sheet.png` / `gen2_sheet.png` (available response sprites).