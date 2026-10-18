# Codex handoff: Sky Lagoon "alive painting" art gaps

Date: 2026-10-18. Author: Claude (written handoff only; Claude builds no images
under the 2026-09-30 owner rule in `CLAUDE.md`). Recipient: Codex.

Status, reported separately:

- `DEMO_IMPLEMENTED`: the standalone demo `scenes/demo/sky_lagoon_alive.tscn`
  exists and is not reachable from `scenes/main.tscn`.
- `MACHINE_VERIFIED`: `scripts/probe_sky_lagoon_alive.gd` passes headless, and
  under Xvfb with the OpenGL compatibility fallback. See the impact record
  `design/audit_impacts/sky-lagoon-alive-demo-20261018.json`.
- `OWNER_REVIEW_PENDING`: nobody has judged the look yet. No Mobile/Vulkan,
  device, child or owner acceptance has been claimed.
- `BRIEF_PUBLISHED`: the art gaps below are specified in words.
  `GENERATION_READY` waits for the owner to review the demo and choose which
  gaps to fund. No item is `DELIVERY_ACCEPTED`.

## Why this exists

The owner said the painted flat scenes feel flat, non-interactive and "like a
pre-rendered JPEG". The demo tests whether the approved Sky Lagoon v5 painting
can feel alive **without redrawing it** (`DL-ASSET-06`, `DL-MED-05`). It uses
only existing approved art, plus runtime motion:

| Layer | What the child sees | Source |
|---|---|---|
| Painting shader | Bushes and the left fir sway in a slow breeze. The lakes shimmer and glint. The cloud sea drifts. A slight depth warp follows camera pans. Taps send ripples. | v5 tiles (unchanged) + `assets/shaders/sky_lagoon_alive_painting.gdshader` |
| Material masks | Computed once at startup on the GPU from the painting's own colours and coarse regions. No mask file exists. | Same shader, `mask_pass` |
| Chimney smoke, meadow motes | Smoke curls from the top cabin. Tapping a cabin makes the chimney puff. Pollen motes drift over the meadow. | `sky_lagoon_smoke_wisp_v2.png`, `CPUParticles2D` |
| Animals | Otter, frog, hare and raccoon idle on their reviewed floor bounds. A tap plays their approved startle frames with a small hop. | `assets/sprites/sky_lagoon/animals/*`, `scripts/arena/sky_lagoon_layout.json` |
| Roshan | Swims along the existing land route to a tapped spot using the swim atlas. Twirls (gesture_a row 3) when tapped. Has a contact shadow. | `assets/characters/roshan_25d/*` |
| Butterflies | Three flutter over the flower beds and flee when tapped. | `assets/fairy/sprites/bug_moth.png` (placeholder, see G4) |
| Water taps | Ripple, splash and ring. A fish-jump splash plays every few seconds. | `assets/sprites/fx_water/*` |

Run it with `godot --path . res://scenes/demo/sky_lagoon_alive.tscn`. Press `M`
to switch all painting motion and camera breathing off and on, to compare
against the untouched painting.

The demo shows how far existing art can go. It also exposes the gaps below,
where the painting cannot supply what a truthful interaction (`DL-INT-02`) or
real parallax needs.

## Source plate (do not modify)

The approved v5 panorama is 6144×2048 master pixels, split into 6 columns × 2
rows of 1024 tiles at `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r{row}_c{col}.png`.
Its source master is `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png`
(SHA-256 `017532ae864e534d9b356472e2e29150855ede6583a7f63f02f0401d28c7be41`).
Tile hashes at baseline `cb203961964f39a25f04434c392bbd5df8cbe080`:

| Tile | SHA-256 |
|---|---|
| r0_c0 | `5addf12c775f697d89b5f7227485155616558c5c2c3c4b29accc89fd9a93fcdb` |
| r0_c1 | `ae962d17088df75e6f3db9fd632a1c2f105d91a902996cd5ac5aba184f82fc1d` |
| r0_c2 | `a5e0dc1e71031ade14059722885bf7905d88f3ea45e9b04e5994cb09ece88850` |
| r0_c3 | `b423c7c320377e15a38d684d4cec4499c81fa9a31e20bdf4d7dbf051d63c1959` |
| r0_c4 | `bb674934980b1b3e70dfe4e2fcb0f866e61f0ac6eefc3414b398a6da654f86ac` |
| r0_c5 | `563cdab3a65bd22518350c441cffd6f0f1173ab51df7d70cf09c11b4c151035c` |
| r1_c0 | `60b2ca6fb0ed517929a7dcdaa19cc9cf13a61cb27d7a7700c396383c85418a3a` |
| r1_c1 | `2fb96fa18f1e9ccec77ba4f1fd162223385fdfaa230f57647f0240de27ca1400` |
| r1_c2 | `2c095349af8d05bb11e43f2115406ce55f583eb885f2abf5b7b4faf7cb8b1e28` |
| r1_c3 | `1f84c75cdfc85923b2a18011e50ac60e78145ed6a9703f7c99ae26592bb6edb7` |
| r1_c4 | `72e54d1d6a1fbfbeba326670c0d0c640d582b0a60f89d95db77ebcec1257e9c4` |
| r1_c5 | `6ef1dd25a1ea4ee998886d6e0c5a824ef915dddb2cff786ffad5520ba0aa2e21` |

Landmarks in master pixels (x right, y down), for orientation:

- Sky: y < ~780.
- Cloud sea: x 480–3450, y 930–1300. The hazy far peaks sit just above it.
- Snow mountain with cabins: x 3700–6144, y 150–950.
  - Cabins at (4790, 500), (4590, 630), (4782, 712) and (3864, 866).
  - The only visible chimney top is at (4794, 428).
- Left pond with rope rail and stepping stones: x 0–420, y 1150–1430.
- Right lake: x 4560–6144, y 1000–1580.
- Tall left fir: x 0–360, y 50–1100.
- Central lawn: x 1400–4100, y 1150–1550.
- Lavender path: runs along roughly y 1550–1670 and climbs the mountain
  at x 3800–4400.
- Foreground flower and large-leaf beds:
  - bottom-left x 0–650, y 1650–2048
  - x 1000–2700, y 1700–2048
  - x 3300–5000, y 1750–2048
  - bottom-right x 5100–6144, y 1450–2048

## Constraints for every item

- Never edit the tiles, the master, `assets/book/`, `assets/audio/voices/` or
  `assets/characters/friends/`. Write derivatives to new paths. Record the
  source hash and the exact edits.
- Sprites are whole drawings (`ODR-SPRITE-WHOLE-UNIT-20261007`). Every animated
  frame is one complete drawing: no part layers, puppet pieces, stacked
  copies or cross-fades. Environment planes in G2 are background layers,
  not character sprites.
- Prefer Aseprite as the editable bridge for sprite cleanup, timing and atlas
  export (`DL-MOT-15`). Keep the editable masters.
- Textures are ≤1024 px on the longest side or power-of-two (`DL-PERF-04`). Data
  masks import lossless (no VRAM compression) and without mipmaps.
- Match the painting: same outline weight and colour, saturation, lighting
  direction (upper left) and soft storybook rendering. No Zelda assets.
- Every new file gets an `ASSET_LICENSES.md` line in the same commit.
- Generate only for a named gap and record prompts, candidates and rejects
  (`DL-ASSET-02`). Rejected candidates stay outside the runtime tree
  (`DL-ASSET-05`).

## Gaps, in recommended order

### G1 (P0): hand-corrected motion masks for the v5 plate

**Why reuse fails:** the demo guesses materials from colour. It cannot know
where a plant is rooted, so a whole bush slides sideways instead of its tips
bending. Dark lake edges and shadowed lawn sometimes register as foliage. The
depth guess is only "lower on screen is nearer", which leans the left fir and
the cabins slightly during pans.

**Deliver:** `assets/flats/sky_lagoon/alive/sky_lagoon_v5_motion_mask.png`,
2048×1024 RGBA, covering the whole 6144×2048 plate (3 master px per mask pixel
across, 2 down). Channels:

- **R, sway weight:** 0 at each plant's base or trunk, rising to 1 at the
  tips. Covers flower stalks, leaves, shrub crowns and the fir's outer
  branches. 0 on rocks, path, lawn, cabins and mountains.
- **G, water:** 1 on open water in both lakes, feathered to 0 over about
  12 master px at the shore. 0 on stones and reflections of stones.
- **B, cloud:** 1 on the cloud sea and the sky clouds only. 0 on snow and
  mountains.
- **A, depth:** 0 = sky, about 0.1 far peaks, about 0.3 the cloud sea and
  mountain, about 0.5 the lakes and lawn, about 0.8 the path, 1.0 the
  foreground beds. Constant across each upright object (the fir trunk, each
  cabin) so pans never shear it. Smooth only where the ground recedes.

**Method:** derive a first pass with a deterministic script from the plate's
colours, then hand-correct in an editor. Save the editable source under
`assets_src/sky_lagoon/alive/`.

**Integration:** the demo already samples `motion_mask` in the shader. Replace
the SubViewport mask pass with this texture and keep the `mask_pass` branch
for comparison.

**Acceptance:**
- In the demo, plant bases stay planted while the tips move.
- Path, rocks, lawn, cabins and mountains show zero displacement. Extend
  `scripts/probe_sky_lagoon_alive.gd` to sample them.
- No upright object leans during a full left-to-right pan.

### G2 (P1): layered depth split of the v5 plate (true parallax)

**Why reuse fails:** a single plate can only fake depth by warping, which
stretches pixels. Real parallax needs separate planes with the hidden parts
painted in.

**Deliver** four 6144×2048 planes, each cut into 1024 tiles like the current
plate, under `assets/flats/sky_lagoon/alive/layers/`:

1. **Sky.** Gradient plus sky clouds, with the mountain silhouettes removed
   and the sky continued behind them.
2. **Far.** Distant peaks and the cloud sea, transparent above.
3. **Mid.** Snow mountain with cabins and path, both lakes, lawn, central
   bushes and the path.
4. **Near.** Only the foreground flower and leaf beds and the tall left fir,
   transparent elsewhere.

Wherever a nearer plane is removed, the plane behind it needs a believable,
targeted inpainted continuation: lawn or path continues under the
foreground beds, sky continues behind the fir. This is local inpainting,
not a redraw (same rule family as `DL-ASSET-08`). Stacking all four planes
must reproduce the original plate within compression noise. Prove it with a
per-pixel difference report, not by eye.

**Integration:** four `Parallax2D` layers. Suggested scroll scales are 0.85
(sky), 0.92 (far), 1.0 (mid) and 1.08 (near). Then set the shader's
`parallax_px` to 0.

**Acceptance:**
- Stacked planes match the source.
- No visible seam or halo at layer edges at gameplay zoom.
- Overdraw stays within budget: measure the Speedy tier on the phone,
  because the near plane is mostly transparent (`DL-PERF-03`).

### G3 (P1): tap-responsive foreground flower clusters

**Why reuse fails:** flowers in the plate can only wobble as part of the
painted bed. A truthful tap (`DL-INT-02`) should make that particular flower
cluster bend and spring back.

**Deliver** three whole-drawing clusters, isolated from the plate's own
foreground lupines and foxgloves where possible:

- tall purple lupines near (5900, 1650)
- yellow lupines near (5760, 1700)
- the pink foxglove near (1350, 1830)

Each cluster is a 2×2 atlas of 4 whole frames: rest, lean left, lean right,
spring-back overshoot. Pivot at the base. Each cell ≤512 px. The pixels
under each cluster in the G2 near plane are inpainted, so the cluster is
not drawn twice.

**Acceptance:**
- At rest, frame 1 matches the plate pixels at that spot.
- The base never moves.
- Silhouette and colour stay within the painting's palette.

### G4 (P2): Sky Lagoon daytime butterfly

**Why reuse fails:** the demo borrows the Fairy chapter's night moth
(`bug_moth.png`, a dark navy wing pattern). It reads as a stranger in the
bright meadow, and its flap is a cheap horizontal squash, not authored
frames (`DL-MOT-07`).

**Deliver** `assets/sprites/sky_lagoon/sky_lagoon_butterfly_atlas.png`: a 2×2
atlas of 256 px cells with 4 whole flap frames. Wings open, half, closed,
half, seen from slightly above. Pastel coral or lavender wings with cream
spots, navy outline matching the plate, small enough to read at about 90
master px wide.

### G5 (P2): lake fish jump

**Why reuse fails:** a splash that appears with nothing jumping reads as
random water popping.

**Deliver** a 4×2 atlas of 8 whole frames (256 px cells) of a small round
storybook fish leaping out and back in. It should match `fx_water_splash_small_atlas.png`
for timing and scale, with the fish about 110 master px long. Water contact
is at the bottom centre of every cell.

### G6 (P3, optional): cabin response states

**Why reuse fails:** tapping a cabin can only puff smoke. A truthful answer is
the cabin itself changing: the door opens or a window lights.

**Deliver**, for the cabins at (4790, 500) and (4782, 712): small overlay
patches cut from the plate at exact plate alignment, with 2 states each
(closed/dark is the plate itself; open or lit is an edited patch). Record
patch rectangles in master pixels.

## Out of scope

- Redrawing the Sky Lagoon scene, or a pixel-art restyle.
- A rigged, puppet or part-layer Roshan, which is ruled out by
  `DL-MED-02` and `ODR-SPRITE-WHOLE-UNIT-20261007`.
- Main-game integration.
- Any change to the shipping promenade.

## Questions for the owner (to answer after trying the demo)

1. Is the motion strength right? Breeze, water and cloud strength, and
   camera breathing, are single numbers in the shader and script. The owner
   previously rejected transformed source art as a *replacement for authored
   object animation* (`design/audit_impacts/sky-lagoon-motion-owner-qc-20260930.json`).
   This demo uses that kind of motion only as ambient breeze and water. Is
   that acceptable here?
2. Which gaps should be funded first? The recommendation is G1 alone, then
   decide on G2.
3. Should the demo's tap answers (ripples, rustles, startles) become the
   pattern for other painted flats?
