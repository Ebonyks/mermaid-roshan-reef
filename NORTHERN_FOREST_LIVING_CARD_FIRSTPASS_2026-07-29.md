# Northern Forest Living-Card Stage — First-Run Pass (2026-07-29)

**For:** codex production. **Governing language:**
`SKY_LAGOON_LIVING_CARD_ANIMATION_V3_2026-07-28.md` §1 (living-card
contract), §4 (lighting architecture), §5 (performance budgets), §6 (art
pipeline), §7 (acceptance gates) apply verbatim. This document is the
per-stage part: source-of-truth decisions, phase order, and the northern
motion identity. It is a **first-run pass** — unlike Sky Lagoon, there is no
shipped mural here, so this stage gets to be born correct instead of
retrofitted.

## Owner amendment — preserve the painting, replace the flat item cutouts

This section is binding and supersedes the northern use of the v3 §3
extraction lane wherever that lane would ship pixels cut directly from the
concept painting as an item card.

- The approved concept painting is immutable composition and style authority.
  Preserve the source file byte-for-byte. A crop from it may be used as an
  image-conditioning reference, matte guide, screen-rect guide, or clean-plate
  heal mask, but **must not ship as the final item sprite**.
- Every relevant independent item is regenerated as a **high-resolution
  volumetric sprite**: a transparent raster rendering with an authored,
  three-dimensional turn of form, visible thickness where appropriate,
  rounded storybook construction, baked cel form shading, baked
  self-occlusion, and the concept's navy/plum edge language. It must read as a
  solid toy-diorama object from the locked play-camera view, not as a flat
  paper crop.
- Runtime world art remains an unshaded `Sprite3D` card placed at real scene
  depth. A “3D sprite” in this handoff means volumetric-looking raster art on
  `Sprite3D`; it does **not** authorize `Sprite2D`, `AnimatedSprite2D`,
  `TextureRect`, custom `CanvasItem` drawing, `MeshInstance3D`, GLB models,
  procedural meshes, or runtime shaded art.
- Each item gets a native authoring master with a long edge of at least 2048
  pixels. Generate at that resolution; do not enlarge, interpolate, AI
  upscale, or pad a smaller result and call it compliant. Preserve the master
  under `assets_src/`. Produce a separate POT runtime derivative, normally
  1024 pixels on the long edge. A 2048 POT runtime card is allowed only for a
  measured hero object that cannot meet reference-camera pixel density at
  1024 and still keeps the §5 VRAM and overdraw ledgers green.
- The card camera is fixed per object class and must match the concept
  viewpoint. Regeneration preserves object identity, silhouette family,
  palette, material, apparent scale, facing, root line, and original
  screen-space footprint. It may add form depth and higher-frequency detail;
  it may not move, redesign, multiply, or replace the object.
- Ground shadows are separate unshaded `Sprite3D` contact-shadow cards. Do not
  bake a studio floor, rectangular plate, scene background, or detached cast
  shadow into the item alpha.
- The current 24 runtime touch-item images, which range from roughly
  62×95 to 215×181 pixels, are implementation placeholders. None may be
  promoted as final merely because its `Sprite3D` node, touch reaction, or
  parallax already works.

The clean-plate half of v3 §3 still applies: remove the pixels owned by the
new card only on a new clean-plate version, heal only inside the declared
mask, preserve every approved pixel outside it, then reinsert the regenerated
card so a locked-camera before/after capture is compositionally congruent.

## Source of truth — preserve the approved art

- **The approved scene concept is the autumn enchanted-forest painting**,
  now preserved as
  `assets_src/concepts/northern_forest_concept_2026-07-29.png`
  (1672×941; SHA-256
  `db0cc66cc90551774ffe28809c095658324634ccf8f27c5742b7735da489208d`).
  Record it in `ASSET_LICENSES.md` with its project-generation provenance
  before integration. Contents to preserve:
  red/crimson/gold broadleaf canopies on birch and dark trunks, teal
  stylized pines, red-cap and cream mushrooms, blue/purple/rust fern
  understory, mossy boulders, the turquoise stream with stepping stones,
  glowing cyan crystals, mid-air falling leaves, purple atmospheric
  distance, and the sandy foreground path — which is, conveniently, a
  ready-made walk band.
- At 1672×941 the painting is **reference-only** under the AGENTS.md
  per-screen 2048 rule — it is the composition and style authority; the
  native master is regenerated from it, never upscaled.
- **Palette decision for Phase 0:** the approved *kit* art
  (`northern_kingdom_quality_2026-07-19.png` + the
  `qa_northern_kingdom_kit/*.png` renders — cottages, mill + wheel, docks,
  snow arches, purple castle) is winter-toned. Owner picks the
  reconciliation: (a) all-autumn stage with kit structures recolored to
  autumn, or (b) a progression — autumn forest screens rising to a
  snowline and winter castle (the kit art used as-is on the later
  screens). Both keep the art-reuse-before-generation policy: kit renders
  condition any structure that appears.
- The current runtime northern kingdom (720u GLB strip, forest → town →
  castle) is legacy under the all-sprite vision. This stage replaces it;
  no animation or art work targets the GLBs.

## Phase 0 — Composition reference (owner gate before any native art)

Extend the approved single-frame concept into the three-screen panorama at
reference scale (~2172×724, ratio 3.0, Sky Lagoon precedent). The concept
frame becomes one screen essentially as-is — its composition is approved,
preserve it. Suggested layout, owner to confirm along with the palette
decision: **deep forest** (the concept frame: path, mushrooms, ferns) →
**stream crossing** (the stepping-stone crossing widened into the screen's
centerpiece, crystals flanking) → **destination** (village-and-mill or
castle approach per the palette decision). Continuous path from edge to
destination door for the walk band, one landmark silhouette per screen.
**Owner approves this composition before Phase 1 spends anything on native
resolution.** Iterate here — it's the cheap phase.

## Phase 1 — Native master, neutral-lit from birth

- Generate the approved composition at **6144×2048 native** (ratio 3.0
  preserved, ≥2048² per screen), image-conditioned on the Phase 0 reference
  + kit renders.
- **Apply v3 §4 at generation time, not as a retrofit:** the master is
  generated as a neutral plate — no directional sun, no cast shadows, no
  time-of-day color cast, full form shading kept. The concept's autumn
  palette and purple atmospheric distance are *local color and aerial
  perspective* — keep them; its warm ambient cast and the cyan crystal
  glow are *lighting* — the cast is neutralized and the glow moves to the
  emissive layer. This is the entire reason the first-run pass is cheaper
  than the Sky Lagoon retrofit: relight decomposition costs one prompt
  clause now versus a v7 master later.
- Same-generation side products, per the §4b layer stack: the cast-shadow
  pass (transparency), the emissive pass (crystal glow, lit windows and
  the mill lantern if structures appear), and **sky/canopy-light
  variants** — day / golden dusk (autumn's home key) / night, with
  **night-with-aurora** if the winter-destination palette option is
  chosen.
- Evidence: master SHA, ratio check, changed-nothing diff against the
  Phase 0 composition (structural), per Sky Lagoon precedent.

## Phase 2 — Slice + stage skeleton

- 6×2 grid of 1024² tiles, 115px overscan procedure, seam ratio gate ≤2.0,
  evidence JSON — identical tooling to the lagoon.
- Stage class cloned from `SkyLagoonPromenade` architecture: backdrop grid,
  walk band, depth planes (same constants unless measured otherwise),
  `_add_ambient_card`/tick, contact shadows, probe with node-type
  inventory. The promenade class is the template; northern-specific
  choreography only.

## Phase 3 — Volumetric Sprite3D regeneration table (closed)

The replacement list is closed so “make it more 3D” cannot become an
unbounded repaint. Pin each concept-owned object to its exact master-space
box and screen rect before generation. The old crop is a reference and matte
guide only; the accepted output is a new high-resolution volumetric sprite.

### 3a. Structural and hero living cards

| Class | expected count | depth | native master | runtime target | purpose |
|---|---:|---|---|---|---|
| Foreground fern/mushroom clusters at bottom corners and center | 3–5 | NEAR_Z | ≥2048px long edge each | 1024 POT each | player occlusion, sway, brush-past |
| Red-cap mushroom cluster at the large trunk base | 1 | NEAR_Z | ≥2048px | 1024 POT | hero silhouette, squash-and-wobble |
| Near birch + red canopy | 1–2 | DRESS_Z | ≥2048px | 1024 POT, or lossless shared-root tiles if justified | parallax and broadleaf sway |
| Cyan crystal groups | 2–3 | DRESS_Z / NEAR_Z | ≥2048px each | 512–1024 POT | solid crystal body plus separate emissive pulse |
| Stream surface band | 1 per stream composition | DRESS_Z | exact-ratio ≥2048px long edge | lossless ≤1024 tiles at one shared depth | dominant shimmer without moving the stream bed |
| Mill wheel and destination door/structure sockets | as authored | PLAY_Z / LANDMARK_Z | ≥2048px each | 1024 POT each | readable authored interaction |

Stepping stones, the stable walk path, stream bed, and other route-defining
ground stay in the clean plate unless they become independently interactive.
Ground that moves reads as broken. Static distant foliage may also stay
painted. The goal is stronger depth and object solidity, not maximum card
count.

### 3b. Current touch-item replacement inventory

The following 24 placeholder crops are all in scope. The file stems identify
interaction sockets and may remain stable so touch/save wiring does not
change, but final runtime paths should point to new derived files rather than
overwrite the preserved placeholders.

| Panel | Regenerate as volumetric sprites |
|---|---|
| Forest trail | red mushroom cluster; tan mushroom cluster; stream wisp |
| Forest stream | left mushroom cluster; right mushroom cluster; stream wisp |
| Spirit grove | left spirit totem; center spirit totem; right spirit totem |
| Forest bridge | bridge mushroom cluster; guide wisp; storybook lantern |
| Village mill | blue cottage door; village lantern; waterwheel |
| Village street | forge fire; market stall; purple cottage door |
| Castle forecourt | fountain; gate crystal; right lantern |
| Castle grand hall | hall fountain; left lantern; right lantern |

Solid items use one transparent RGBA card. Wisps and forge fire use a small
POT sprite sheet or a bounded set of `Sprite3D` cards, with identical
per-frame canvas, root/pivot, camera, palette, and apparent volume. Animation
is advanced by the stage's bounded tick; no `AnimatedSprite2D` is introduced.
Doors remain independent cards in front of structure clean plates so their
invitation motion and touch socket stay readable.

### 3c. Generation and finishing contract

1. Inventory the existing library first. Direct reuse is allowed only when an
   asset already matches the required object identity, camera, volumetric
   construction, palette, resolution, licensing, and touch silhouette. Record
   the match. A merely similar low-resolution flat does not qualify.
2. Condition each new asset on its exact approved concept crop and, where
   relevant, the project-owned northern kit render. Use an orthographic or
   very-long-lens object render matched to the concept camera: neutral
   top/front light, rounded toy-diorama volume, baked warm-light/cool-shadow
   cel planes, navy/plum edges, no perspective mismatch, no character, text,
   UI, floor, or scene background.
3. Generate the authoring master natively at ≥2048px long edge on a removable
   flat chroma background when transparent output is unreliable. Extract and
   hand-check alpha, decontaminate the fringe over light and dark swatches,
   keep the root bottom-flush, and preserve the full master.
4. Produce the POT runtime derivative without overwriting the master or the
   old placeholder. Record source/master/runtime dimensions and hashes,
   content bounds, pivot, world height, pixels per meter, aspect ratio,
   animation frames, depth plane, motion class, contact shadow, and touch
   footprint.
5. Heal only the old object's declared clean-plate mask. Reinsert the new card
   at real Z with perspective compensation. At the reference camera its base,
   screen rect, silhouette weight, and negative space must remain congruent;
   on pan it must show measured parallax and correct occlusion.

New ornaments remain narrowly scoped: falling-leaf cards reproduce the
concept's leaf families; crystal glints, chimney smoke, and window/lantern
emissives are separate low-coverage cards only where the panel calls for
them.

## Phase 4 — Northern motion identity

Same three layers, autumn personality — the concept's own weather:

- **Ambient:** broadleaf canopy sway (the lively class, 0.12–0.18u — this
  forest *rustles*, unlike the lagoon conifers); teal pines stay stiff
  (0.06–0.09u) for contrast. **Falling leaves** are the stage's signature
  ambient: 4–6 leaf cards per screen on slow tumble-drift tweens
  (reproducing the concept's painted leaf shapes; deterministic paths,
  counted as ONE quiet loop per screen). Fern understory at the shrub
  class.
- **Reactive:** brush-past bend on NEAR_Z ferns; **mushroom wobble** (a
  squash-and-wobble tween when brushed — mushrooms are rigid, they rock,
  not bend); one-shot **leaf-shake** — first brush of a near tree per
  visit drops one leaf card from its canopy (deterministic trigger).
- **Authored / dominants per screen:** deep forest — falling leaves +
  crystal glow pulse; stream crossing — the **stream shimmer** (scrolling
  sparkle band) with leaves occasionally landing on the water and drifting
  off-screen; destination screen — mill wheel turning or castle-door
  invitation per the palette decision.
- Time-of-day: full §4b/§5 runtime grading applies from day one — the
  stage is *born* gradeable. Golden dusk is autumn's home key; the
  emotional-staging beat is the crystals and windows coming alive as the
  canopy grades toward evening (aurora reserved for the winter-destination
  option).

## Budgets, gates, order

- All v3 §5 budgets and §7 gates (1–20) apply unchanged; the probe
  inventory table is created in Phase 2 and updated every card PR.
- Build order: Phase 0 → owner gate → Phase 1 → gates 12/13/17–20 →
  Phase 2 → existing-library audit → Phase 3 pilot (the forest-trail red
  mushroom cluster end-to-end) → owner gate → remaining structural and
  touch-item batch → Phase 4.
- First-run rule of thumb from the lagoon numbers: target ≈40–55 total
  `Sprite3D` nodes for the three-screen first-run target, ≈40 visible per
  framing, and no more than 6–8 large transparent cards or 150% cumulative
  transparent-card coverage in one framing. For the extended promenade,
  distance-cull panel-local cards so only the current and adjacent panels
  contribute. Resolution may not be reduced to hide an overdraw problem.

The card batch is not accepted on visual review alone. Required handoff
evidence includes:

- a node-type inventory showing all world items on unshaded `Sprite3D` and
  zero nonconforming world-art node types;
- a path inventory proving none of the 24 low-resolution placeholder crops is
  wired as final runtime art;
- native-master and runtime-derivative dimensions, hashes, prompts,
  references, alpha/fringe checks, and license/provenance records;
- locked-camera before/after congruency captures plus max-pan parallax,
  player/item occlusion order, pixels-per-meter, and aspect-ratio checks;
- touch-hit projection and reaction checks after every card replacement,
  including animation-frame pivot stability for wisps and fire;
- Speedy-tier visibility, VRAM, transparent-overdraw, and 30 fps evidence;
- the established five-part art audit at **≥4.5/5 for every panel and seam**.
  A lower score is a rejection: preserve the candidate for evidence,
  regenerate only the failing object, and repeat its structural and runtime
  gates.
