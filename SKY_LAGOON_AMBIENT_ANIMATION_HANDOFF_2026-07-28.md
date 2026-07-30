# Sky Lagoon Ambient Animation — Production Handoff (2026-07-28)

> **SUPERSEDED — do not implement.** This v1 targeted the retired
> `claude/sky-lagoon-pnw-runtime` stage (GLB flora, MultiMesh scatter,
> CPUParticles). The binding document is
> `SKY_LAGOON_LIVING_CARD_ANIMATION_V2_2026-07-28.md`, restated for the
> Sprite3D promenade. Kept for design intent and the art-pipeline rationale.

**For:** codex production branch (branch off `claude/sky-lagoon-pnw-runtime`)
**Goal:** Make the sky lagoon feel alive and playful, reinforce the 2.5D storybook
cutout look, at near-zero tablet cost. Everything below reuses machinery already
shipped on the branch — no new systems, no per-frame GDScript.

---

## Hard constraints

1. **Tablet budget.** Target device already boots at 30–40s and runs warm.
   - No per-frame GDScript loops. All motion is TIME-driven vertex shaders,
     `CPUParticles3D`, or looping Tweens.
   - `CPUParticles3D` only (mobile-safe, established pattern). No GPUParticles.
   - Overdraw is the real tablet killer, not particle count: keep transparent
     billboards small, emitters few. Total NEW particles scene-wide ≤ ~80.
2. **All-sprite vision (owner decision, reaffirmed 2026-07-28).** The world
   is 2D sprite cards in 3D space — "3D sprites" — full stop. No new 3D
   models, and **no animation work targeting GLBs**: the lagoon-kit GLB
   flora still instantiated by `sky_lagoon.gd` (it survived the 2026-07-28
   dead-asset purge because it is still *placed*, not because it is wanted)
   is legacy awaiting card replacement. Do not write mesh-specific shaders,
   material swaps, or sway paths for it — every hour spent animating a GLB
   is thrown away when its card successor lands. Cards are the only
   animation target in this brief.
3. **Quality gate.** Everything except the vertex-sway shaders must respect the
   existing tier check (`m.quality != "speedy"` — see the sun shadow toggle in
   `_build_pearl_castle`). Vertex sway is free and stays on in all tiers.
4. **Chalet tuck clearances.** Build comments in `_build_alpine_*` warn that
   chalet/pine/crag tucks are hand-verified. Keep sway tip displacement ≤ 0.2u
   so no re-verification is needed.
5. Single-mesh `_art35` contract: lagoon kit GLBs are one mesh, one surface.
   Material swaps iterate surfaces anyway (copy the `_gen2_creature` loop).

## Existing machinery to reuse (all on `claude/sky-lagoon-pnw-runtime`)

| Thing | Where | Reuse as |
|---|---|---|
| Tip-pinned sway shader | `assets/shaders/seagrass_sway.gdshader` | template for flora wind + flower cards |
| Body sway w/ `phase`, `excite` uniforms | `assets/shaders/creature_sway.gdshader` | uniform naming + excite-ramp pattern |
| GLB all-surfaces material swap | `_gen2_creature` in `scripts/main.gd` (~L3965) | how to apply wind shader to kit GLBs, preserving baked albedo |
| CPUParticles3D billboard drifter (26 butterflies) | `scripts/arena/sky_lagoon.gd` ~L681 | template for smoke / leaves / seeds |
| Looping Tween (spinning home ring) | `sky_lagoon.gd` ~L675 | template for cloud drift |
| Chalet builder + castle chimney box | `sky_lagoon.gd` ~L1248, ~L1331 | smoke emitter anchor points; `visibility_range_end = 165` precedent |
| Prop/tree/shrub placement | `_lagoon_prop` / `_lagoon_tree` / `_lagoon_shrub` (sky_lagoon.gd L193–216) | hook point to attach wind material + per-instance phase |
| White-bg → alpha cutout tool | `tools/polish_sprite.py` (sprite mode) | stage 1 of the card art pipeline |
| Chroma-key + sheet splitter | `tools/extract_connected_chroma.py` | stage 1 fallback for non-white sources |
| Accepted flat flora art + grammar | `assets_src/concepts/sky_lagoon_pnw_flat/` + `SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md` | card sources + the style rules new art must obey |

---

## Work item 1 — `lagoon_flora_card.gdshader`: ONE shader for all flora cards

Biggest visual multiplier; zero CPU, zero extra draw calls. This is the
spine of the whole brief: a single card shader, extended from
`seagrass_sway.gdshader`, that every flora card in the lagoon runs — flowers,
shrubs, and (as they land) trees. Wind, gust, brush-past bend, base AO,
scene tint, and distance haze ALL live in this one file, so every later work
item is a uniform on a shader that already exists.

- Base displacement exactly like seagrass: `tip = 1.0 - UV.y`, bottom row
  pinned, tips sway on `sin(TIME * speed + phase)` in X/Z. No mesh-height
  uniforms needed — the art pipeline's bottom-flush anchoring (stage 2)
  makes UV.y the height axis by construction. **The crop IS the rig.**
- Add a smaller higher-frequency flutter term offset by `VERTEX.x` so wide
  cards (trees, big shrubs) shimmer instead of rocking as a rigid poster.
- Per-instance `phase`: `INSTANCE_CUSTOM.x` for MultiMesh scatter,
  `randf() * TAU` shader param for individually placed cards. Without
  desync the meadow moves in lockstep and looks mechanical.
- Sway class comes from the card manifest (stage 3), not hardcoded.

Sway classes (tip displacement, world units — tune from probe shots):

| Card class | amount | speed | notes |
|---|---|---|---|
| Conifer tree cards (fir, cedar, hemlock, spruce, pine, yew) | 0.06–0.09 | 0.7 | barely breathe; stiff |
| Broadleaf tree cards (maple, alder, cottonwood, madrone, oak, dogwood) | 0.12–0.18 | 0.9 | visible rustle |
| Shrub cards (currant, salal, oceanspray, salmonberry, blackberry…) | 0.15–0.20 | 1.1 | liveliest woody layer |
| Flower cards | 0.10–0.15 | 1.2 | gentle nod, not thrash |

Note on the legacy GLB flora: it keeps whatever static materials it has today
and simply gets deleted as card successors land (see scope note below). It
gets NO shader work.

## Work item 2 — Chimney smoke (3 chalets + castle chimney)

Clone the butterfly emitter block (~L681). Per emitter:

- `amount = 7`, `lifetime = 5.0`, low `emission` rate so puffs read as
  **discrete storybook puffs**, not a continuous wisp — this is the style call.
- Upward velocity ~0.8–1.2, slight X/Z spread, `scale_amount` growing
  ~1.0→2.2 over lifetime via scale curve, alpha ramp out in the last 40%.
- Billboard unshaded quad, soft round puff texture (new 2D asset, ~256px,
  soft-edged pale grey — see palette note below).
- **Puff albedo ≤ (0.92, 0.90, 0.88), never pure white.** Pale surfaces clip
  past the tonemap white point and bloom-blow on Android (known arena
  exposure issue). Slight warm-grey also reads cozier.
- Anchor at each chalet roofline (`ALPINE_HOUSE_A/B/C` consts, L21–23; castle
  chimney top at its `_l2_box` position + half height) — eyeball the exact
  roof stack offsets per chalet GLB from a probe shot.
- `visibility_range_end = 165.0` (match the chimney box). Gate behind the
  quality tier.
- Give the initial velocity a small lateral component matching the global
  wind direction (see work item 6) so smoke and trees agree about the wind.

## Work item 3 — The flora card program (flowers → shrubs → trees)

With the all-sprite vision this is no longer a "convert some flowers" side
item — it is the flora replacement program, sequenced smallest-first so the
pipeline and shader are proven before the biggest silhouettes change:

1. **Flower cards** — 3–4 flower clump sprites, new art in the storybook
   cutout style (sample palette from the existing coral/lavender clusters so
   nothing clashes). Meadow volume fill via `MultiMeshInstance3D`, one per
   texture variant, phase in `INSTANCE_CUSTOM.x` — hundreds of flowers, one
   draw call per variant, unshaded fragment path. Hero clumps near paths are
   individually placed cards (bigger, cast shadows — see grounding package).
2. **Shrub cards** — direct from the 12 accepted A/B shrub prototypes in
   `assets_src/concepts/sky_lagoon_pnw_flat/`. These replace the placed
   lagoon-kit shrub GLBs one-for-one at the same `_lagoon_shrub` positions
   and target heights (tables already in the builder).
3. **Tree cards** — the 12 accepted tree prototypes, same lane, replacing
   the lagoon-kit tree GLBs at the same `_lagoon_tree` positions/heights.
   Owner reviews the probe sheet before the GLB deletion lands — trees are
   the scene's biggest silhouettes and the riskiest swap.

All cards run `lagoon_flora_card.gdshader` (work item 1). **Every texture
goes through the art pipeline section below — no ad-hoc hand-cropping.**
Crossed quads for shrubs/trees (stable from all angles); flowers may use
single Y-billboards if the crossed X-seam shows at close range — decide per
class on the probe pose, not globally.
Each GLB→card swap deletes the replaced GLB from the placement code in the
same PR — the whole point is that the legacy meshes stop shipping.
- Respect placement rules already in the builder: off the carved river ribbon,
  off paths, use `_lagoon_local()` for terrain height. Cards sit ~0.05u into
  the ground so bases never float on slopes.

**2.5D grounding package (part of this work item — cards without it read as
pasted-on, not standing-in):**

- **Contact shadows, two tiers.** Hero cards/props near paths: enable real
  cast shadows with alpha-scissor in the shadow pass — a cutout casting a
  live *swaying* shadow from `sun2` is the strongest diorama cue available,
  and quads are 4 verts so the shadow-pass cost is trivial. Mass MultiMesh
  fill: NO cast shadows; instead a soft dark ellipse blob quad at each base
  (second quad in the same MultiMesh, one shared texture, unshaded).
  Grounding hundreds of flowers matters more than shadow accuracy.
- **Fake base AO in the card shader.** Darken the bottom ~15% of the card:
  `albedo *= mix(0.85, 1.0, smoothstep(1.0, 0.85, UV.y))` — the base "sits
  into" the grass instead of being sliced onto it. Two lines, do it.
- **`scene_tint` global uniform.** Unshaded cards ignore lights, so at night
  they'd glow daylight-bright while the GLB world dims — instant illusion
  break. One global uniform set when the arena builds (warm cream by day,
  dusky blue-lavender when `m.is_night`), multiplied into every card
  shader's albedo. Without this the card program fails night QA, full stop.
- **Fallback if probe shots still show tonal pop-off:** switch cards from
  unshaded to shaded with normals overridden toward world-up (standard
  billboard-grass trick) so they receive terrain-style lighting from the
  actual sun. Prefer unshaded + tint first — it matches the established
  cutout language and is cheaper.

## Work item 4 — Ambient drift particles (2 emitters, meadow-wide)

- **Falling leaves:** one CPUParticles3D over the deciduous stands. ~14
  particles, lifetime 7s, slight gravity (−0.4), `angular_velocity ±90` for
  tumble, small maple-leaf sprite (2D asset, warm green — NOT autumn red, this
  is a lush summer scene unless owner says otherwise).
- **Seed motes:** ~12 particles, near-zero gravity, tiny soft white dandelion
  motes drifting with the wind direction, meadow box like the butterfly
  emitter. Albedo cap same as smoke.
- Both gated behind quality tier.

## Work item 5 — Cloud drift

Looping Tween per cloud family group (home-ring pattern, ~L675): drift each
cloud 6–10u along wind X over 45–70s, `Tween.TRANS_SINE` ping-pong, staggered
durations so they never sync. If clouds are direct children of terrain-anchored
parents, tween a wrapper node, don't touch the GLB transform math.

## Work item 6 — Global wind coherence (small, but sells everything)

One **global shader uniform** (Godot 4 `global uniform float wind_gust`) driven
by a single slow Tween or the existing `_tick_level2` (one float lerp — this is
the only allowed CPU touch, ~zero cost):

- Base 1.0, gusts to ~1.6 for 2–3s every 15–40s (randomized).
- `lagoon_flora_card` materials multiply sway amplitude by it; smoke
  emitters can read it on gust start to nudge lateral velocity.
- Result: the whole scene occasionally leans together. This single detail is
  what makes wind read as *weather* instead of independent wiggles.
- Pick ONE world-space wind direction constant (suggest +X, matching the
  prevailing camera framing) and use it for smoke lean, seed drift, leaf
  drift, and cloud tween direction.

## Work item 7 — Player-reactive flora (brush-past bend)

Flowers, shrubs, and grass-layer cards bend away as Roshan swims past and
spring back behind her. This is the highest-value playfulness item in the
package — the world responding to *her* is worth more than all the ambient
motion combined. It is also nearly free if built the right way:

- **Primary approach — stateless shader bend, no proximity loops.** Declare a
  `global uniform vec3 player_world_pos`, updated once per frame from the
  existing player tick (one `RenderingServer.global_shader_parameter_set`
  call — this is the only CPU cost, scene-wide). `lagoon_flora_card.gdshader`
  then computes each card's reaction per vertex:
  - card origin via `NODE_POSITION_WORLD` for placed cards, or the instance
    origin from `MODEL_MATRIX` for MultiMesh scatter.
  - `push = normalize(world_pos.xz - player_world_pos.xz)`
  - `strength = 1.0 - smoothstep(bend_r * 0.4, bend_r, dist)` with
    `bend_r ≈ 2.5u` for shrub cards, `≈ 1.8u` for flower cards.
  - Displace tips by `push * strength * bend_amount * tip_weight` (same
    height/UV tip weighting as the wind term; base stays pinned).
  - Because bend derives from live distance, spring-back needs **no state**:
    she leaves, `strength` falls, the plant returns. Smooth by construction.
  - Fake the playful overshoot wobble with a stateless term:
    `sin(TIME * 9.0) * strength * (1.0 - strength) * 0.3 * bend_amount` —
    peaks at the bend boundary, silent when idle and when fully bent.
- `bend_amount`: cards/shrubs ~0.35u at tips (bold — this should be clearly
  readable, it's a toy), GLB clusters ~0.2u, trees **0.0** (a swimmer does
  not bend a fir; trees opt out via uniform default).
- Vertical range matters: scale `strength` by proximity in Y too (she can be
  well above the meadow — flowers shouldn't bend when she flies 6u overhead;
  fade the effect out over ~2u of height difference).
- **Fallback for anything that can't share the shader** (e.g. a hero prop
  with bespoke material): per-material `excite` uniform ramped from the
  existing crafted-creature proximity pass in `_tick_crafted` — same cadence,
  no new scans. Use only where the global-uniform path genuinely can't reach.
- Not gated by quality tier (it's vertex math, same cost class as the wind
  sway), but the `player_world_pos` update should no-op cleanly when the
  lagoon arena isn't active.

## Work item 8 — Aerial perspective + backdrop silhouette rings

The scene-scale 2.5D move: near = saturated/warm, far = lighter/cooler/
flatter, like paper-theater backdrops. Two parts, both cheap:

- **Distance tint in the flora shaders** (both `flora_wind` and the card
  shader — one `mix()` in fragment): lerp albedo toward a pastel haze color
  (pale lavender-aqua from the established palette) by camera distance,
  starting ~45u, maxing ~40% at ~120u. This is cheaper and more controllable
  than environment volumetric fog on the mobile renderer — do NOT reach for
  fog. Tune the haze color in-game, not from probes (AgX washout gotcha).
- **Silhouette backdrop rings.** 2–3 concentric arcs of flat tree-line
  silhouette cards at the island rim, each ring progressively lighter and
  bluer. Flat art IS the correct technology for backdrops — this is where
  the PNG baseline is an advantage. Prior exploration exists on
  `codex/sky-lagoon-silhouette-tiles`; review it before authoring new art.
  Rings are static (no sway — distant motion at that scale reads as
  shimmer/noise), unshaded, `scene_tint`-multiplied, no shadows, huge
  `visibility_range`. A handful of large quads total.
- **Value-separation rule** (the flat-prototype audit called out "poor value
  separation" as a rejection cause — treat this as a gate): foreground
  flora darkest/warmest, midground full chroma, backdrop rings lightest.
  Check on the wide probe pose in greyscale — the three layers must
  separate with color removed.

---

## Art pipeline — flat source image → animated runtime card

The accepted flat flora set (24 cards, `assets_src/concepts/sky_lagoon_pnw_flat/`,
per `SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md`) and all new Gemini art
are **opaque flat images** — reference paintings, not runtime assets. A flat
image cannot take motion; a processed card can. Every card asset (flowers,
shrubs, smoke puffs, leaves, seeds — and eventually trees, see trajectory note)
goes through this lane. The critical insight: **the sway shader pins the base by
UV.y, so the crop and anchor decisions in this pipeline ARE the animation rig.**
Sloppy cropping = broken motion, no shader fix possible.

### Stage 0 — Source acquisition / generation spec

- Existing accepted sources: the 24 PNW flat cards (RGB PNG, opaque bg).
- New sources (flowers, puffs, leaves, seeds): generate per the audit's visual
  grammar — single readable silhouette at phone scale, 2–5 primary masses,
  broad cel planes, established palette (mint/aqua/sage/lavender/coral/cream/
  muted-gold/warm-wood/navy-purple), one oversized story cue.
- **Generation constraints for clean processing** (put these in the prompt):
  - plain near-white background (`polish_sprite.py` floods ≥235,235,235);
  - full subject in frame, silhouette nowhere touching the image edge;
  - the plant's ground-contact line visible (root flare / stem bases) —
    a card with an ambiguous bottom cannot be anchored;
  - no cast shadow reaching the image border (it survives the flood fill);
  - neutral, slightly top-down painted lighting — no strong side light. The
    card is unshaded in-engine and visible from both sides; a hard painted
    light direction will contradict the scene sun from half the angles.
- **Baked shading conventions** (the PNG does the lighting engine's job —
  these carry the entire cel read, spell them out in every art prompt):
  - soft dark ink outline baked into every card, matching the `next_pass`
    outline the GLB props already wear — one consistent contour language is
    what makes mixed cutout+mesh scenes read as a single world;
  - warm-light / cool-shadow cel planes: painted shadow tones shift toward
    the palette's navy-purple, never toward gray or black;
  - painted root shading — slight darkening at the plant base, which stacks
    with the shader base-AO and blob shadow (work item 3) to seat the card.
- New generations land in `/Downloads` (project convention) with Gemini-hash
  names; copy to `assets_src/concepts/` with the final asset name BEFORE
  processing, so provenance survives.

### Stage 1 — Cutout (RGB → RGBA)

- Primary tool: `python3 tools/polish_sprite.py sprite <in> <out.png>` —
  border flood-fill (interior whites survive), 1px mask feather, autocontrast,
  tight crop. Already shipped and proven on the GEN2 sprites.
- Non-white backgrounds: `tools/extract_connected_chroma.py` (chroma key +
  optional grid split for multi-item sheets).
- **Fringe check (mandatory):** flood-fill cutouts keep a 1–2px pale fringe
  from anti-aliased edges. It's invisible on white review pages and glaring
  against dark meadow grass. Inspect every card composited over a dark navy
  swatch; if fringe shows, add an edge-decontamination pass (bleed interior
  colors outward under the alpha ramp) to the tool rather than hand-fixing.

### Stage 2 — Anchor authoring (the step that makes motion work)

The runtime quad maps the texture 1:1; `seagrass_sway` weights displacement by
`(1.0 - UV.y)` — bottom row pinned, top row max sway. Therefore, per card:

1. **Bottom-flush root line.** The visual ground-contact row must sit exactly
   at the bottom canvas edge — zero bottom padding. NOTE: `polish_sprite.py`
   crops with margin on ALL sides; the card lane needs a variant/flag that
   forces bottom-flush. For multi-stem shrubs the root line is the lowest
   ground-contact pixel, not the lowest leaf (drooping foliage may hang below
   stem bases in the painting — if so, repaint or lift it: foliage below the
   pin line would sway *through the ground*).
2. **Centered stem.** The stem/trunk center of mass sits on the horizontal
   canvas midline. The quad pivot is bottom-center; placement code positions
   that pivot on terrain via `_lagoon_local()`. An off-center card visibly
   orbits its pivot when the wind-lean term moves it.
3. **Tight top crop.** Transparent headroom above the plant inflates the
   apparent sway (tip weight peaks in empty pixels) and wastes texels. Crop
   to the alpha bbox top + 2–3px.
4. **Measured content fractions, not eyeballed.** Record content-height
   fraction and aspect from the alpha bbox with a script. This burned us
   before: the mg2d garden plants were scaled by eyeballed fractions and
   came out wrong (see mg2d content-fraction fix). World quad height =
   `target_height / content_height_fraction`.

### Stage 3 — Card manifest (single source of truth)

One const table in the builder (pattern: `LAGOON_TREE_SOURCE_HEIGHT`) or a
generated `.json` in `assets_src/`, one entry per card:

```
"lagoon_card_flower_coral_a": {
  "tex": "res://assets/props/lagoon_cards/flower_coral_a.png",
  "aspect": 0.82,            # measured, stage 2
  "content_h": 0.97,         # measured, stage 2
  "target_h": 0.9,           # world units, design choice
  "sway_amount": 0.15, "sway_speed": 1.2,   # motion class, work item 1 table
  "bend_amount": 0.35,       # work item 7; 0.0 = opts out
  "quads": "crossed"         # crossed | single-billboard (puffs/leaves)
}
```

A small tool (`tools/build_lagoon_cards.py`, new) runs stages 1–3: cutout →
anchor-check → measure → emit manifest entries. Hand-editing measured fields
is a review flag. Puffs/leaves/seeds use the same lane minus stage 2's root
line (they're center-pivot, `quads: single-billboard`).

### Stage 4 — Godot import settings (per card texture)

- PNG with straight alpha; **Fix Alpha Border ON** (kills the dark mipmap
  halo at distance), mipmaps ON, filter linear.
- VRAM-compress (mobile) — flat-color storybook art compresses well, but
  check banding on the broad color planes; bump to lossless only if a card
  visibly bands on the tablet, not preemptively (boot-time audit: lossless
  textures are a measured boot-cost lever, don't add more by default).
- Size budget: shrubs ≤1024px tall, flowers ≤512, puffs/leaves/seeds ≤256.

### Stage 5 — Validation gate (before any mass scatter)

New probe pose set in `probe_sky_lagoon_art.gd`: each new card rendered
in-scene (a) against grass and against snow, (b) day and night, (c) at 3m /
12m / 40m. Checks:

1. no pale fringe against dark backdrops, no dark halo at 40m (mipmaps);
2. base pinned: two captures 1s apart — root-line pixels must not move while
   tips do (this directly verifies stage 2 wasn't skipped);
3. silhouette reads at the 40m/phone-scale shot (audit criterion);
4. crossed-quad intersection isn't visibly X-shaped from the main play angles;
5. owner review of the composited probe sheet — the audit precedent applies:
   card acceptance means *runtime asset accepted*, a higher bar than the
   "modeling reference accepted" the 24 flat cards currently hold.

### Trajectory note — trees

Runtime trees are currently lagoon-kit GLBs and work item 1 animates them as
meshes. Under the 2D-sprites-only direction (owner decision 2026-07-26) those
GLBs are slated for eventual replacement; the 24 flat tree/shrub cards +
this pipeline are exactly how their card successors get built. Sequence
deliberately: flowers/shrub-fill cards first (this handoff), tree cards as a
separate owner-approved pass later — the wind shader work is NOT wasted, the
same shader drives the cards via the seagrass UV.y path.

---

## Additional feel polish (recommended, in priority order)

1. **Butterfly scatter.** When she enters the hero butterflies' hover radius,
   briefly boost their flap speed/altitude (uniforms already exist in
   `butterfly_flap.gdshader`); the drifting CPUParticles cloud can stay
   oblivious. Piggyback on the same `_tick_crafted` proximity cadence.
2. **Night windows + smoke.** `m.is_night` already exists: at night, warm up
   chalet window emissive (pulse ±10% over ~4s, Tween) and slow smoke by
   ~30%. Cozy hearth read for free.
3. **River sparkle.** The lavender footing stones already use animated
   emission (see comment ~L2546). A sparse sparkle-mote emitter (8 particles)
   over the two river ribbons, or a scrolling-UV glint strip, makes the water
   read as moving. Keep it subtle — water is background here.
4. **Occasional bluebird flyover.** `lagoon_bluebird.glb` exists as a
   collectible. A single bird on a long looping Tween arc between chalet
   rooftops every ~90s (sway shader mode 1 for wing undulation) adds a
   storybook vignette moment. Skip if over budget — nice-to-have.
5. **Emissive micro-accents.** Tiny low-energy emissive dots — flower
   centers, currant berries, chalet windows — under the existing
   `glow_bloom 0.05` environment give jewel-like "toy world" sparkle.
   Sparse: a dozen glints scene-wide, not a field. Keep energies below the
   tonemap clip (Android bloom-blowout recipe applies).
6. **Audio layer.** `assets/audio/ambience_lagoon.ogg` is already wired.
   Add: (a) a soft wind-gust swell one-shot triggered off the `wind_gust`
   ramp, (b) sparse songbird chirps (2–3 one-shots, randomized 20–60s
   timer), (c) faint crackle loop within ~6u of a lit chalet at night.
   Audio is the cheapest "alive" signal there is — three one-shots outperform
   another particle system.

## Explicitly out of scope / do not do

- No GPUParticles, no skeletal animation, no new GLB/3D assets.
- No dappled-light projectors or moving light shadows (tablet cost).
- No motion on the mountain, terrain, castle structure, or path stones —
  ground that moves reads as broken, not alive.
- Don't animate anything with collision the player relies on.

## QA / validation

1. **Probe shots:** `scripts/probe_sky_lagoon_art.gd` is the established
   screenshot probe. Add a probe pose per chalet chimney and one wide meadow
   pose. Remember the QA-render tonemap gotcha: probe captures wash out under
   AgX vs. in-game — judge color in-game or with matching tonemap, judge
   *motion/placement* from probes.
2. **Windows CI:** `ci.sh` needs the APPDATA isolation shim on Windows
   (established pattern) — don't let probe runs touch the real user save.
3. **Perf gate:** before/after frame time on the tablet (or the speedy-tier
   desktop proxy): the whole package must cost < 1ms/frame. If it doesn't,
   the particle emitters are the suspects — halve amounts before touching
   the shaders (shaders are effectively free; if perf moved, something else
   is wrong).
4. **Lockstep check:** wide probe shot at t=0s and t=2s — no two adjacent
   trees may be at an identical sway phase.
5. **Bloom check on Android profile:** smoke/seed whites must not bloom-clip
   (arena exposure recipe: glow_bloom 0.05 environment).
6. **Brush-past check (work item 7):** swim Roshan through the meadow at
   ground level — flowers/shrubs on her path must visibly part and settle
   behind her. Then fly the same path 6u up — nothing below may react.
   Verify trees never bend. Confirm `player_world_pos` updates stop when
   leaving the lagoon arena (no stale-position bending on re-entry).
7. **Night congruence (work item 3 `scene_tint`):** capture the meadow probe
   pose with `is_night` on — cards must sit in the same tonal family as the
   lit GLB props, not glow daylight-bright. This check is a hard gate.
8. **Grounding check:** every hero card's cast shadow moves with its sway;
   every MultiMesh instance has a blob shadow under it; zoom a card at 3m —
   base darkening visible, no card looks "sliced onto" the grass.
9. **Layer separation (work item 8):** wide probe pose converted to
   greyscale — foreground / midground / backdrop rings must still separate
   as three distinct value bands.

## Suggested build order

1. Work item 1 (flora wind) + work item 2 (smoke) — transforms the scene, ~1 day.
2. Work items 6 + 7 (global gust, brush-past bend) — both live in the same
   shaders as item 1; do them while the shader files are open. Item 7 is the
   playfulness centerpiece — do not let it slip to a later pass.
3. **Art pipeline bring-up** — write `tools/build_lagoon_cards.py` (stages
   1–3), prove it end-to-end on ONE card (a currant shrub is a good pilot:
   multi-stem, tests the root-line rule), run the stage-5 probe gate on it.
   Only then batch the rest. Smoke/leaf/seed sprites (work items 2 and 4)
   use this lane too, so it unblocks three work items at once.
4. Work item 3 (flower cards, including the 2.5D grounding package) — batch
   through the proven pipeline; advances the 2.5D goal most, and inherits
   the brush-past bend for free once the card shader has it. Do the
   `scene_tint` uniform and distance tint (work item 8's shader half) here
   too — same shader files, and night QA needs the tint from day one.
5. Work item 8's backdrop rings — after the card lane is proven (rings are
   just big static cards), reviewing `codex/sky-lagoon-silhouette-tiles`
   first.
6. Work items 4, 5, then polish items 1–6 (butterfly scatter, night,
   emissive accents, audio).
