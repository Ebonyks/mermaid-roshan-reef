# Ember Fortress forty-asset enrichment audit — 2026-07-22

## Outcome

Forty additional original 2D modeling cards extend the Ember Fortress concept
package from 39 required Blender exports to 79. The request's named Nintendo
world is treated only as a high-level reference for dense spherical volcanic
adventure. No Mario, Bowser, Nintendo, Zelda, branded character, enemy, symbol,
architecture, collectible, or copied silhouette is present.

Every addition is a separate 1024×1024 concept card under
`assets_src/concepts/ember_fortress_claude_2026-07-22/expansion_40/`. Four
1024×768 contact sheets provide review evidence. These are E1 design inputs,
not runtime replacements and not eligible for a numeric runtime art score.
Claude remains the sole Blender modeler in this chain.

## Families

- **Architecture (10):** bridge, route arch, lava aqueduct, balcony, buttress,
  stairs, parapet corner, ash chimney, plaza brazier, lavafall cliff.
- **Terrain (10):** magma rim, basalt columns, ash dune, vent cluster, obsidian
  shards, cooled flow, cave mouth, meteor crater, cinder island, chain anchor.
- **Interactive dressing (10):** anvil, coal cart, urn, drum, bell, lever,
  pressure plate, flame wheel, heat shield, ember bloom.
- **Ambient life and guidance (10):** ash fern, glow moss, cinder fungi, ember
  moths, smoke puffs, spark trail, lava bubbles, shimmer totem, crust slab, and
  comet landing beacon.

The exact row-level contracts are in
`audit/ember_expansion_inventory_2026-07-22.csv` and
`CLAUDE_EXPANSION_40_MANIFEST.csv`.

## Richness without overload

The expansion is a placement library, not a requirement to instantiate all
assets everywhere. Claude must preserve the manifest's per-role placement cap.
Runtime integration must additionally enforce:

- at most 28 expansion instances inside the active camera sector on Speedy;
- no new OmniLights—emission is material-only unless an existing culled light
  is explicitly reused;
- no transparent smoke or shimmer layers on Speedy; use opaque modeled proxies
  or hide them;
- repeated families use shared imported resources and material instances;
- distant architecture and flora receive a cull distance before promotion;
- interactive states remain addressable children, not duplicate full scenes;
- flora, moths, bubbles, smoke, and sparks remain non-colliding visuals;
- bridges, stairs, slabs, islands, and pressure plates retain analytic gameplay
  collision/interaction rather than mass rigid bodies.

## Review findings

The four contact sheets were inspected at original resolution. The cards have
consistent charcoal/plum basalt, lavender/aqua accents, coral emission, cream
modeling backgrounds, rounded toy-playset silhouettes, and usable multi-view
construction. No card visibly resembles a protected franchise asset.

Some generated meter markings are approximate visual aids. The manifest scale
column is authoritative. Generated ornament is not permission to add a logo,
face, eye, mouth, weapon, or unrelated vignette in Blender.

## Completion boundary

This expansion is `concept_ready`. Completion still requires Claude-authored
`.blend` sources and 40 measured GLBs, isolated multi-angle/state renders,
placement integration, Forward Mobile/Speedy runtime captures, exact-head green
CI, and owner review. Nothing in this package is authorized for `dev` by itself.
