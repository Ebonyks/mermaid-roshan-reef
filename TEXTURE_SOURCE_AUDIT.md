# Texture Source Audit — nano-banana coverage after the full swap
2026-07-12 · companion to the bake_nano_wrap.py pass (Blender pipeline,
build_npc_rig.py family) that dressed the remaining traditional pack GLBs
in the generated sheets.

## What is now nano-banana
- **Terrain/level bases**: seabed sand, reef rocks (gen2 sculpts + cliff
  tile fallback), snow (chute, snowball, ice floe, fetch arena), courtyard
  grass/cobble/dirt/flagstone, castle walls/roof/door/marble, moat +
  toon-water albedo, Butterfly World meadow + paths + dome mullions +
  dance rug.
- **Baked by this pass (11 GLBs, in place)**: trop_palm1/2, trop_monstera,
  trop_fern, trop_bigleaf, tray, plant_bush, grass_leafsLarge, Rock2,
  throne, bed. Method: box-projected NanoUV + per-material colour
  classification -> sheet, original part colour multiplied into an
  embedded copy (gold stays gold, red cushion stays red).
- **Props/creatures**: all gen2 Meshy models carry their own generated art.

## Update — defaults-removal pass (2026-07-12, same day)
The procedural/default reef layer is now HER art too: the 2,520-blade
meadow + kelp fields wear the gen2 seagrass/kelp sprites (same wind sway),
the 240 scatter starfish are painted decals rendered from the gen2
starfish model (the model itself was also re-baked to lie flat - it stood
on edge like a coin), the six ambient fish schools are painted clownfish
side-sprites (softly tinted per school), and the Butterfly Gate portal is
rebuilt: painted pearl ring + two fluttering gen2 butterfly cards
replacing the white procedural wings.

## Update — reef geography pass (2026-07-13)
Owner: "very same-y... larger hills, more geography... walls have no
details." Two NEW nano-banana generations: up_cliffwall_col (terraced
cliff face with coral shelves) and backdrop_seamounts (layered silhouette
panorama). The seabed gained a landmark swell (real hills + basins, capped
under the fixed-height POIs), the rim is scalloped cliff bays crested at
84 units, the terrain shader blends sand->cliff-wall by slope, a painted
seamount ring surrounds the world, and the three tallest hills carry mega
rock + kelp-grove crowns. NOTE: the flat-sand sheet remains ambientCG
Ground054 (a deliberate readability exception - the painted sand read as
cracked dirt).

## Rule added — surface textures are BLANK canvases (owner 2026-07-13)
Rock/wall/ground sheets must contain NOTHING that also exists as a 3D
prop: no baked corals, moss, flowers, shells or pebble clusters - the
game dresses those surfaces with real gen2 props, and painted twins clash
with them. up_cliffwall_col and up_cliff_col were regenerated bare (the
first cliffwall had coral shelves; the old up_cliff had moss + flowers -
the 'camo' look on the rock pedestals). Rock2 re-baked from the pack
original with the bare sheet. Scenery PAINTINGS (the seamount backdrop)
are exempt - they are backdrops, not surfaces.

## Weaknesses of source-art availability (the gaps)
Ranked by how visible the stand-in or hold-back is in play:

1. **Foliage/leaf sheet — MISSING (stand-in used).** No painted leaf-vein
   / frond close-up exists in the suite, so every plant baked here wears
   `up_grass_col` (a lawn texture). Reads pastel-consistent but has lawn
   grain, not leaf veins. Highest-value next generation: one "painted
   tropical leaf" sheet + rebake 6 plants.
2. **Crystal/gem — MISSING (held back).** crystal1-3, crystal_castle and
   the Star Hall amethyst panels keep procedural translucency; no painted
   facet sheet exists, and opaque tiling would kill their glassiness.
   Needs a dedicated translucent-friendly facet sheet (or leave as-is by
   design — the glass look is intentional).
3. **Fruit skins — MISSING (held back).** fruit_orange/melon/banana (the
   butterfly feeding trays) keep pack colours; no orange-peel/melon-rind/
   banana-skin sheets. Small on screen; low priority.
4. **Flower petals + mushroom caps — MISSING (held back).** flower_*,
   mushroom_red, mushroom_tanGroup keep pack colours under the runtime
   pastel tint. A petal sheet would finish the flower beds.
5. **Painted metal — MISSING (worked around).** The bed's metal trim was
   routed to fabric, gold trims lean on marble x gold tint. A soft painted
   metal sheet would serve throne/gate/lantern hardware.
6. **Galaxy butterfly GLBs — partial.** Sprite butterflies use gen2 art
   (butterfly1/2.png); the two CC GLB butterflies in the Butterfly World
   still carry pack wings (tinted). Candidate for the card-wing rebuild
   used on fairy Roshan.
7. **Vehicle liveries — out of this pass.** Kart/motorcycle/monstertruck
   belong to the kart workstream (nano road tiles already exist there).
8. **Still procedural, no source art**: anemones and urchins in the
   scatter field (glow-tip meshes), the giant ambient silhouette fish
   (_fish_mesh(14)), and one grass bunch in the slide arena. Candidates
   for the next Gemini batch (anemone + urchin especially - 560
   instances on the seabed).
9. **Functional maps — no equivalents needed.** caustics.png, ripple
   normals, scales_normal, polyp detail, star_detail are effect/detail
   maps, not art surfaces; retained by design.
10. **Sacred art — out of scope by rule.** assets/book/, family voices,
   friend cutouts are never regenerated.

## Pipeline notes for the next generation batch
- Kenney-family GLBs can lose their palette on glTF import (trop_bigleaf:
  every material came in default grey). bake_nano_wrap.py's FORCE_TINT
  override covers it; check the bake log for `rgb=(0.8, 0.8, 0.8)`.
- White-painted pack pieces (tray) defeat colour classification; use the
  per-model OVERRIDES entry.
- The classifier's wood band reaches down to hue 10 deg so chocolate
  trunks do not fall into fabric; vivid reds are excluded by sat/val.
