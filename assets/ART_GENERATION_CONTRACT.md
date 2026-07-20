# Art Generation Contract — read this before generating any asset

Audience: the code-generation agent (Codex) producing the next art pass.
This file is self-contained; authoritative long-form sources are
`ART_STYLE_GUIDE.md`, `ART_SCORING_GOVERNANCE_2026-07-18.md`, and
`ART_GAP_WORKORDER_2026-07-18.md` at the repo root.

**Active work order:** if you are iterating on the full-texture-regen
candidate pack, `CODEX_IMPROVEMENT_AUDIT_2026-07-18.md` at the repo root is
the current prioritized directive list (P0 QA fixes → P1 promotion → P2
rework → P3 coverage). Close P0 before generating anything new.

**Audit memory:** read `assets/OBJECT_GENERATION_AUDIT_LOG.md` before creating
a generation prompt or Blender generator. It evaluates the source audits,
assigns stable rule IDs, records family-specific failures, and defines the
required per-role generation packet. Append new audit findings there before
changing a batch prompt so rejected patterns do not re-enter later runs.

## Scoring standard (owner decision 2026-07-18)

- **5/5** = the asset survived the stress-test loop AND the owner accepted
  the shipped views. There is no automatic score for any provenance,
  including book fidelity. The book is identity reference, not the
  aesthetic ceiling — you are expected to iterate toward a look that
  renders BETTER in engine than the book's static paintings.
- The loop (reference example: Northern Kingdom rebuild, 2026-07-17):
  1. Generate deterministically from a Python/Blender script in `tools/`.
  2. Capture near, mid, and gameplay-distance views on the **Mobile
     renderer** via the CI capture probes.
  3. Visually review; reject on silhouette, material, scale, composition,
     repetition, occlusion, or bloom/exposure clipping.
  4. Regenerate until clean. Two or three rejected iterations is normal.
- Generated candidates without runtime captures cap at 2/5. Focal objects
  built from engine primitives cap at 1/5. Do not ship either.

## Two pipelines — know which one you are

| | World / environment assets (YOU, Codex) | Book-derived characters & story objects (NOT you) |
|---|---|---|
| Method | Deterministic Blender code, flat multi-material geometry | Meshy image-to-3D from book art |
| Quality source | Stress-test iteration | Book painting fidelity, preserved by construction |

Never generate replacements for book-derived characters, faces, family
voices, or friend cutouts. Protected, untouchable zones: `assets/book/`,
`assets/audio/voices/`, `assets/characters/friends/`. Roshan identity
anchors (for scenes she appears in, never regenerate her): chestnut hair,
front-LEFT rainbow forelock, lavender clothing, green-right/pink-left tail.

## The look (digest of ART_STYLE_GUIDE.md)

- Pastel toy playset in a cel-shaded, storybook diorama: rounded, slightly
  asymmetrical masses; broad color fields; oversized child-readable
  features; nothing gritty, noisy, or threatening.
- **Materials**: texture-free, flat `baseColorFactor` slots (the current
  corpus averages ~5 materials/model — the palette IS the material list).
  Matte-to-satin roughness (0.65–0.90 stone/cloth/plant), metallic 0
  unless visibly metal. Navy/purple inverted-hull outline shells:
  `#4a4f78`, `#1a1238`, `#090d1a`.
- **Palette anchors**: coral `#ffa399`, lavender `#a87dd6`, gold
  `#f5b838`, aqua `#45c4c7`, mint `#80d48f`, cream `#f5ebd1`, slate
  `#6b7aa3`; foam white `#E4F5F6`, ocean blue `#4087B0`, ink indigo
  `#222E44`, tail pink `#E88FB9`, reef green `#79C982`.
- Shadows are aqua/blue-grey/lavender, never black. High-key: no baked
  spotlights, crushed AO, or vignettes. Rainbow is a reward accent, never
  a universal fill.
- **Motif fidelity**: butterflies get 4 wings + body + antennae; beetles
  get head/thorax/wing-case + six legs; pines keep trunk + tiered
  silhouette; snow is rounded caps with blue-grey undersides. No invented
  faces on ordinary props (coral, rocks, food, plants).
- **Ground-plant completeness**: one detached leaf is never a complete plant
  growing from terrain. Every placed ground plant needs a believable root or
  attachment point and a full growth habit: baby rosette, multi-leaf clump,
  reed bed, shrub, flowering plant, or mature tree. Single leaves are allowed
  only as litter, collectibles, or attached parts of a larger plant.
- **Functional separation** where play needs it: detachable pieces are
  separate meshes/files (music bars, ornaments, star bells, gates the
  player swims through).

## Hard technical rules

- Mobile renderer on every platform; must read correctly there, not just
  in Blender renders.
- Textures (if unavoidable — prefer none): ≤1024 px longest side OR
  power-of-two. Prefer embedded flat materials; zero new texture memory is
  the norm (the 17-piece Northern kit adds none).
- Low-poly budgets: props ~800–2,500 verts; hero/one-instance pieces may
  reach ~12k tris (Northern castle: 12,816). Merge by material — never
  ship 18-material un-merged exports (see `bathroom_sink.glb` defect).
- No new OmniLights without a cull path. Restrained emissive instead.
- Every asset ships in the same commit with: generator script in
  `tools/`, editable source in `assets_src/blender/`, QA renders, and a
  row in `ASSET_LICENSES.md` (project-generated, © Mermaid Roshan LLC).
- Every generated asset must be PLACED by runtime code in the same
  workstream. Unplaced output is an orphan (11 exist already — do not add
  more).
- Trusted probes (`scripts/ci.sh`) must stay green; placement must respect
  the ecosystem rules in `OBJECT_PLACEMENT_AUDIT_2026-07-17.md` (habitat
  filters, reserved gameplay footprints, believable support surfaces).

## What to build next (from ART_GAP_WORKORDER_2026-07-18.md, by lift)

1. **Wire existing assets first, no modeling**: `art35/kart/soft_barrier.glb`
   (kart track edges), `art35/arena/treasure_chest.glb` (castle back room),
   `art35/landmarks/dream_star.glb` (lagoon star platforms),
   `galaxy/crystal1-3.glb` (kart rainbow deco). Delete the 10 orphaned
   GLBs and the 2 retired HDR skies.
2. **Sky Lagoon train set** — engine, tender, coach, gondola, caboose,
   station, track kit (currently 100% primitives, courtyard_train.gd).
   Plus fairy-castle exterior kit and chalet/alpine crag kit.
3. **Castle architecture kit** — fluted columns with capitals, archways,
   doorframes, balustrades, cornices, chandeliers, painted banners, stair
   kit, stained-glass windows; per-room floor canvases (throne medallion,
   library parquet, toy-room mat, midnight rug).
4. **Reef hub** — painted backdrop panorama (replaces photo seamounts),
   cliff/reef-wall rim kit, pastel seabed canvases, hero portal-shell,
   five friend-gateway markers, softer caustics sheet.
5. **Kart world** — grandstands + crowd + pit garage (absent entirely),
   road trim-sheet, boost pads, starting-lights gantry.
6. **Butterfly World** — painted planet-surface canvas, crystal wall
   panels, orrery planets.
7. **Clutter/loot** — treasure gems/coin/pearl piles, basement
   barrels/crates/jars, shop cans/tanks/shelves, toy blocks/chest,
   easel/paints, rubber duck, cradle/keepsakes; slide chute segments;
   fetch snowfield canvas; dungeon impact-VFX sheets.

Northern Kingdom is complete — do not regenerate it; it awaits owner
review only.
