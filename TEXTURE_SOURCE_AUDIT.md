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
8. **Functional maps — no equivalents needed.** caustics.png, ripple
   normals, scales_normal, polyp detail, star_detail are effect/detail
   maps, not art surfaces; retained by design.
9. **Sacred art — out of scope by rule.** assets/book/, family voices,
   friend cutouts are never regenerated.

## Pipeline notes for the next generation batch
- Kenney-family GLBs can lose their palette on glTF import (trop_bigleaf:
  every material came in default grey). bake_nano_wrap.py's FORCE_TINT
  override covers it; check the bake log for `rgb=(0.8, 0.8, 0.8)`.
- White-painted pack pieces (tray) defeat colour classification; use the
  per-model OVERRIDES entry.
- The classifier's wood band reaches down to hue 10 deg so chocolate
  trunks do not fall into fabric; vivid reds are excluded by sat/val.
