# CC0 Regen 35 — corrected 2D concept prompt plan

This corrects the earlier ocean-only prompt scope. The two existing accepted
sheets cover eight entries from the numbered Regen 35 plus the three live
seaweed addendum entries. They do **not** cover the full list.

The authoritative workorder table contains 35 paths through the furniture row,
then a separate three-path SeaWeed row. This plan preserves that distinction:

- `01–35`: the owner's Regen 35 coverage contract.
- `F01–F03`: verified-live non-original flora addendum, already represented on
  the Norwegian rock-and-kelp sheet.

No prompt may silently add a replacement role. Context flora and coral are
placement guidance only unless their exact legacy path appears below.

## Numbered coverage manifest

| ID | Legacy path | Family prompt | Status |
|---:|---|---|---|
| 01 | `assets/castle/throne.glb` | A | accepted `regen_01_pearl_shell_throne.png` |
| 02 | `assets/vehicles/gokart.glb` | B | accepted `regen_02_03_vehicles.png` |
| 03 | `assets/vehicles/motorcycle.glb` | B | accepted `regen_02_03_vehicles.png` |
| 04 | `assets/galaxy/crystal1.glb` | C | accepted `regen_04_06_crystal_family.png` |
| 05 | `assets/galaxy/crystal2.glb` | C | accepted `regen_04_06_crystal_family.png` |
| 06 | `assets/galaxy/crystal3.glb` | C | accepted `regen_04_06_crystal_family.png` |
| 07 | `assets/galaxy/crystal_castle.glb` | D | accepted corrected `regen_07_crystal_castle.png` |
| 08 | `assets/galaxy/tray.glb` | E | accepted `regen_08_serving_tray.png` |
| 09 | `assets/galaxy/butterfly1.glb` | F | accepted corrected `regen_09_10_butterflies.png` |
| 10 | `assets/galaxy/butterfly2.glb` | F | accepted corrected `regen_09_10_butterflies.png` |
| 11 | `assets/castle/bed.glb` | G | accepted `regen_11_pearl_castle_bed.png` |
| 12 | `assets/nature/cliff_block_rock.glb` | H | accepted sheet |
| 13 | `assets/nature/cliff_large_rock.glb` | H | accepted sheet |
| 14 | `assets/nature/rock_largeA.glb` | H | accepted sheet |
| 15 | `assets/ship/barrel.glb` | I | accepted sheet |
| 16 | `assets/ship/chest.glb` | I | accepted sheet |
| 17 | `assets/ship/cliff_cave_rock.glb` | I | accepted sheet |
| 18 | `assets/ship/ship-ghost.glb` | I | accepted sheet |
| 19 | `assets/ship/ship-wreck.glb` | I | accepted sheet |
| 20 | `assets/kits/castle/tower-square.glb` | J | accepted `regen_20_22_castle_live_modules.png`; confirmed live |
| 21 | `assets/kits/castle/flag.glb` | J | accepted `regen_20_22_castle_live_modules.png`; confirmed live |
| 22 | `assets/kits/castle/wall.glb` | J | accepted `regen_20_22_castle_live_modules.png`; confirmed live |
| 23 | `assets/kits/castle/tower-base.glb` | J | accepted concept in `regen_23_28_castle_pending_modules.png`; hold 3D commission pending callsite verification |
| 24 | `assets/kits/castle/tower-square-base.glb` | J | accepted concept in `regen_23_28_castle_pending_modules.png`; hold 3D commission pending callsite verification |
| 25 | `assets/kits/castle/tower-square-mid.glb` | J | accepted concept in `regen_23_28_castle_pending_modules.png`; hold 3D commission pending callsite verification |
| 26 | `assets/kits/castle/tower-square-top-roof-high.glb` | J | accepted concept in `regen_23_28_castle_pending_modules.png`; hold 3D commission pending callsite verification |
| 27 | `assets/kits/castle/tower-top.glb` | J | accepted concept in `regen_23_28_castle_pending_modules.png`; hold 3D commission pending callsite verification |
| 28 | `assets/kits/castle/wall-narrow-gate.glb` | J | accepted concept in `regen_23_28_castle_pending_modules.png`; hold 3D commission pending callsite verification |
| 29 | `assets/kits/park/bench.glb` | K | accepted `regen_29_32_park_and_rooted_hedges.png` |
| 30 | `assets/kits/park/fountain.glb` | K | accepted `regen_29_32_park_and_rooted_hedges.png` |
| 31 | `assets/kits/park/hedge_straight.glb` | K | accepted `regen_29_32_park_and_rooted_hedges.png` |
| 32 | `assets/kits/park/hedge_straight_long.glb` | K | accepted `regen_29_32_park_and_rooted_hedges.png` |
| 33 | `assets/kits/furniture/bookcase.glb` | L | accepted `regen_33_35_pearl_furniture.png` |
| 34 | `assets/kits/furniture/chair.glb` | L | accepted `regen_33_35_pearl_furniture.png` |
| 35 | `assets/kits/furniture/table.glb` | L | accepted `regen_33_35_pearl_furniture.png` |
| F01 | `assets/aquatic/SeaWeed.glb` | H | accepted addendum sheet |
| F02 | `assets/aquatic/SeaWeed1.glb` | H | accepted addendum sheet |
| F03 | `assets/aquatic/SeaWeed2.glb` | H | accepted addendum sheet |

Final concept coverage: `35/35` core entries plus `3/3` live-flora addendum
entries. IDs `23–28` remain concept-only pending the workorder's required
callsite verification.

## Shared production block for every missing-family call

```text
Use case: stylized-concept
Asset type: high-resolution 2D-to-3D model-reference sheet for original replacements of named live non-original game assets
Primary request: depict only the exact numbered Regen roles named in this family prompt; each role must remain a separate reusable model target for Claude's Blender or image-to-3D reconstruction lane
Style/medium: Mermaid Roshan children's Mobile game asset design; original clean flat-color anime cel illustration; rounded toy-playset geometry; mild handmade asymmetry; thin dark-indigo contour; two or three broad value bands; crisp aqua/lavender shadow planes; restrained storybook grain inside color regions only
Composition/framing: orthographic-style front, side, back, top where useful, and three-quarter views; identical proportions and colors across views; generous separation and padding; show natural contact, attachment, or root geometry; no cropping
Lighting/mood: even diffuse studio light; high-key, welcoming and emotionally safe
Constraints: no display plinths, floor discs, contact-shadow ovals, baked ground islands or combined scenic bases; no text, labels, logos, trademarks, watermarks or copyrighted franchise symbols; no photorealism, gritty wear, horror, black shadows, glossy plastic, noisy microdetail, tiny fragile parts or unrequested objects; silhouette and two or three color blocks must read at phone gameplay size; every sheet cell must map to one manifest ID
```

## A — throne (`01`)

```text
Create one original pearl-shell royal throne replacement. Use a broad stable
seat, oversized scallop-shell back, rounded arm rests, low child-readable step,
pearl cream and blush planes, lavender/aqua shadows, and restrained warm-gold
accents. It must read as a throne without a crown logo, character, room, dais,
coral cluster or separate platform. Show front, side, back and three-quarter.
```

## B — vehicles (`02–03`)

```text
Create exactly two separate original preschool-readable racing vehicles: `02`
a low stable go-kart with broad bumper, visible seat, simple steering wheel and
four chunky wheels; `03` a friendly compact motorcycle with two broad wheels,
low saddle, readable handlebars and protected rounded body. Maintain functional
wheel clearances and steering silhouette. Use aqua, coral and lavender color
blocks without branding, faces, weapons, riders, exhaust smoke or racetrack.
```

## C — crystal family (`04–06`)

```text
Create exactly three independent original magical crystal clusters. `04` is a
low three-point cluster, `05` is a tall asymmetric five-point cluster, and `06`
is a broad radial cluster with one dominant center point. Use chunky bevelled
facets, opaque cel-painted turquoise/lavender/rose bands and stable natural
bases. No transparency-dependent design, rainbow overload, rock islands,
particles, faces, jewelry settings or duplicate silhouettes.
```

## D — crystal castle landmark (`07`)

```text
Create one original small landmark crystal castle: a readable central arched
door, broad central tower, two shorter side towers, rounded crystal spires and
a stable continuous foundation integrated into the building. Use pearl cream,
cyan, lavender and restrained coral highlights. No characters, flags, symbols,
floating islands, surrounding crystals, plants, coral or scenic terrain.
```

## E — serving tray (`08`)

```text
Create one original ordinary serving tray with a broad shallow oval body, thick
safe rim and two oversized grip handles. Matte pearl cream and muted brass with
one aqua shadow band. Empty tray only: no food, cups, gems, hands, table, coral,
plants or decorative ground.
```

## F — butterflies (`09–10`)

```text
Create exactly two complete species-readable butterfly model turnarounds. `09`
is monarch-like with warm orange cells, deep-brown veins and cream edge spots;
`10` is blue-morpho-like with saturated blue-violet fields and dark margins.
Each has four complete wings, thorax, abdomen, six simplified legs and two
antennae. For each ID show matched open, half-folded and closed wing states at
identical scale and registration. Elegant animals, not mascots: no human faces,
heart/rainbow wings, flowers, leaves, display pins or missing far-side anatomy.
```

## G — pearl-castle bed (`11`)

```text
Create one original child-sized pearl-castle single bed with a broad shell-like
headboard, low rounded frame, thick readable mattress, one pillow and one neatly
folded blanket. Pearl cream, blush, aqua and lavender with restrained warm coral
accent. Show natural feet/contact points. No character, room, canopy, nightstand,
toys, plants, coral or separate rug/base.
```

## H — Norwegian rocks and live flora (`12–14`, `F01–F03`)

Use the exact accepted Norwegian prompt already recorded in `PROMPTS.md`. The
three plants are cold-water macroalgae with believable holdfasts and thick,
countable blades. They are the flora addendum, not extra entries in `01–35`.

## I — Caribbean nautical family (`15–19`)

Use the exact accepted Caribbean prompt already recorded in `PROMPTS.md`.
Biome-context placement may surround these models with the project's existing
original branching, mound, finger, tube and fan coral families plus seagrass,
but those contextual organisms must never be baked into these five meshes.

## J — modular castle kit (`20–28`)

```text
Create exactly nine separate, grid-compatible original toy-castle modules with
one consistent pearl-stone scale and wall thickness: `20` square tower body;
`21` simple cloth flag on a thick safe pole; `22` full wall; `23` round tower
base; `24` square tower base; `25` square tower middle; `26` high square roof;
`27` round tower cap; `28` narrow wall with a broad readable gate opening. Show
connection edges and top views. Pearl cream masonry with broad aqua/lavender
shadow blocks and restrained coral roof/flag accents. No heraldry, characters,
scenes, vines, coral, terrain, damage or assembled fortress. IDs `23–28` are
concept-only until a repo-wide callsite check confirms they remain live.
```

## K — park family and rooted flora (`29–32`)

```text
Create exactly four independent original park assets: `29` rounded bench with
thick slats and stable legs; `30` low child-safe fountain with a broad basin and
simple central shell-water motif represented as solid geometry, not simulated
water; `31` one complete short straight hedge; `32` one complete long straight
hedge at exactly twice the modular length. Each hedge must be a rooted woody
shrub mass with a visible low trunk/branch structure and layered leaf clusters,
not a stretched green cube or detached leaf card. Use spring green, muted mint,
teal shadow and sparse cream blossoms only if leaf structure remains dominant.
No paths, soil islands, pots, coral, shells, benches attached to hedges or scenic
park composition.
```

## L — furniture family (`33–35`)

```text
Create exactly three separate original pearl-castle furniture pieces with one
shared rounded construction language: `33` low broad bookcase with three clear
shelves and a small set of chunky color-blocked books; `34` stable chair with
wide seat and shell-scallop back; `35` four-legged table with thick rounded top
and clear knee space. Honey wood, pearl cream, aqua/lavender shadows and small
coral accents. No room scene, characters, loose props, plants, coral or rug/base.
```

## Ecosystem density and coral rule

The Regen 35 is a file-for-file replacement list, not the full ecosystem roster.
For later Caribbean runtime composition, use many instances and varied rotations
of the project's already-authored original coral families: branching, mound,
soft-finger, tube, fan and anemone-like crowns, plus original seagrass. For the
Norwegian composition, use rooted sugar kelp, finger kelp, bladderwrack-like
clumps and appropriate cold-water vegetation; do not use tropical reef coral.

Those organisms remain independent placement assets. Never bake a mixed coral
garden, sand island, shells, rocks and unrelated species into one reusable prop.
Likewise, do not generate additional coral replacement meshes for the legacy
Group 0 paths: the workorder records that those paths are already unreachable
because original replacements supersede them.
