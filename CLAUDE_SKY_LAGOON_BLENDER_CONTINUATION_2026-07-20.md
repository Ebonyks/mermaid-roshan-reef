# Sky Lagoon Blender continuation for Claude — updated 2026-07-21

## Binding production baseline

Continue from `assets_src/blender/sky_lagoon_pnw_woody_plants.blend` and
`tools/build_sky_lagoon_pnw_woody_plants.py`. These are the editable and
deterministic Blender sources for the accepted Seattle-area woody-plant family.
The non-woody environment remains in
`assets_src/blender/sky_lagoon_quality_kit.blend`.

The prior GEN5 tree family, its eight runtime GLBs, its concept, its QA renders,
and `tools/build_sky_lagoon_tree_gen5.py` were explicitly rejected by the owner
and removed. Do not restore them, the four generic GEN2 anchors, the meadow
shrub, or palette variants of any of those models to Sky Lagoon.

The binding runtime tree roster is exactly these twelve independently modeled
species:

1. coastal Douglas-fir (`Pseudotsuga menziesii`)
2. western redcedar (`Thuja plicata`)
3. western hemlock (`Tsuga heterophylla`)
4. Sitka spruce (`Picea sitchensis`)
5. shore pine (`Pinus contorta var. contorta`)
6. Pacific yew (`Taxus brevifolia`)
7. bigleaf maple (`Acer macrophyllum`)
8. red alder (`Alnus rubra`)
9. black cottonwood (`Populus trichocarpa`)
10. Pacific madrone (`Arbutus menziesii`)
11. Garry oak (`Quercus garryana`)
12. Pacific dogwood (`Cornus nuttallii`)

The binding shrub roster is exactly six species: salal, low Oregon grape,
red-flowering currant, oceanspray, salmonberry, and evergreen huckleberry.

Each GLB contains `role`, `species_common`, `species_latin`, `habitat`, and
`style_gate=sky_lagoon_pnw_woody_gen1` extras. Preserve those values and the
runtime filenames. All models are texture-free and use embedded matte
materials. The isolated Mobile limits are 7,500 triangles and eight materials
for a tree, 6,500 triangles and eight materials for a shrub. No new light or
physics body belongs in these assets.

## Art and placement contract

The family must remain cohesive in deep jade, mint, aqua-shadow, lavender,
coral, warm bark, and butter-gold, but silhouette is the primary identity.
Conifers must differ through leader, bough, spray, skirt, and density. Broadleaf
trees must differ through crown topology and diagnostic leaves rather than a
shared sphere crown. Shrubs must retain their diagnostic habit plus flowers or
fruit. A recolor, uniform scale, whole-tree warp, or repeated crown template is
not a new design.

Runtime ecology is encoded in `scripts/arena/sky_lagoon.gd`:

- red alder, black cottonwood, and salmonberry stay within 42 units of a water
  edge;
- moist-forest species stay within 82 units of a water edge;
- madrone, Garry oak, shore pine, Oregon grape, currant, and oceanspray stay at
  least 20 units from water;
- only the five PNW conifers may enter painted snow;
- no mushroom, tropical palm, isolated leaf, or broadleaf tree may enter snow;
- all plants remain off river channels, the pond disc, moat/castle, paths,
  playground, houses, train corridor, and island rim.

Do not loosen those rules to make a screenshot pass. If a guaranteed specimen
cannot be placed, fix its candidate position or habitat logic while retaining
the ecological rule.

The Mermaid Roshan stained glass at `assets/book/hall/glass_mermaid.png` is
protected and must remain a separate unchanged image plane. Expected SHA-256:
`94952B4C13455F7A3966DB32D7FC49F652DD5B933325AD9C3D37DE9B93C3D4A0`.

The Ember Fortress gateway remains code-native for now. If continuing its
Blender conversion, preserve the vertical plum/coral ring, gold inner lip,
three-lobe flame crest, planted lavender/aqua stones, role
`lagoon_ember_gateway`, and the accepted local placement `(72, -150)`.

## Rebuild and reject/regenerate workflow

Use Blender 4.4.3:

```text
blender --background --python tools/build_sky_lagoon_pnw_woody_plants.py
blender --background --python tools/render_glb_turntable_batch.py -- GLB OUT_DIR STEM [...]
python tools/build_pnw_woody_contact_sheets.py
python tools/audit_sky_lagoon_kit.py
```

Isolated reviews are under
`assets_src/blender/qa_sky_lagoon_pnw_woody_plants/` at 0°, 45°, and 135°.
After any changed asset passes those three angles, run the fixed Godot Mobile
review in `scripts/probe_sky_lagoon_art.gd`; it contains one framed scene view
for every tree and shrub plus numerous whole-scene perspectives and the stained
glass check. Reject and rebuild any item below 4.5/5 in either isolated or
runtime review. The automatic ceiling is 4.9/5.

Update `ASSET_LICENSES.md`,
`SKY_LAGOON_PNW_WOODY_PLANT_AUDIT_2026-07-21.md`, and
`audit/sky_lagoon_pnw_woody_plant_ledger_2026-07-21.csv` after an accepted
revision. Require parser/inference gates and exact-branch green CI before
integrating into `dev`.
