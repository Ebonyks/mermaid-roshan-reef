# Royal Kitchen art audit candidate — 2026-07-29

Status: **accepted and runtime-integrated on `codex/kitchen-audit-fridge`**

## Audit findings

- The current room source has two oversized exterior windows.
- Both windows show an ocean/reef vista that is incompatible with the castle
  location.
- No refrigerator or refrigerator source asset exists in the repository.
- The refrigerator needs to be an unobstructed, child-readable touch target
  because it is foundational to the cooking minigame.

## Accepted full-frame result

- Complete regenerated full-room source:
  `room_kitchen_fullframe_v2_1672x941.png`
- Native generated dimensions: `1672×941`
- SHA-256:
  `8faa4e15e60503cb0303434b77461fa559a81c3d021eb6c3165e9ed176bfbf3e`
- Generation method: OpenAI built-in ImageGen, full-scene generation using
  `assets/flats/castle/rooms/room_kitchen.png` as the composition/style
  reference.
- The two ocean-view windows are gone.
- One small, high, opaque shell light inset remains; it does not show an
  exterior view.
- One mint-and-cream refrigerator is fully visible in the back-right work
  zone, with a gold handle, readable door seam, and clear floor approach.
- The established sink, stove/oven, counters, prep table, palette, and open
  central play floor remain.

## Final generation prompt

```text
Use case: precise-object-edit
Asset type: full-frame Royal Kitchen environment master for a preschool touch game
Input image: the current approved Royal Kitchen is the composition, palette, material, and storybook-style reference; regenerate the entire complete flattened scene, preserving its polished 2D cel-shaded storybook illustration quality.
Primary request: correct the kitchen architecture and add the missing gameplay-critical refrigerator.
Scene/backdrop: an interior room deep inside Pearl Castle. Replace BOTH enormous ocean-view windows with continuous lavender castle stone walls, rounded shell-and-pearl architectural trim, warm wall lanterns, and practical kitchen storage. There must be NO ocean view, NO underwater exterior, NO fish, NO visible coral reef beyond glass, and no large exterior windows. At most one very small high opaque stained-glass shell medallion may be used as a decorative light inset, not a view outdoors.
Refrigerator: add one large, unmistakable, freestanding storybook refrigerator in the back-right work zone, fully visible and not hidden by the foreground table. It should be aqua/mint with pearl and cream trim, rounded corners, a clear vertical gold handle, a visible door seam, and a small shell crest. It must read instantly as a refrigerator to a four-year-old, not as a cabinet, oven, pantry, aquarium, or decorative arch. Give it clear empty floor access so it can become a large touch target and so its door can visibly open during the cooking minigame.
Preserve: the wide single-room composition, lavender stone castle walls and arches, mint cabinets, cream shell counters, central stove/oven and copper pans, left shell sink, right preparation counter, foreground round worktable, warm lantern lighting, open central walkable floor, soft aqua/lavender/gold palette, rounded toy-like forms, navy-purple outlines, high polish and child-readable silhouettes.
Composition: wide 16:9 room overview, straight-on storybook game camera, full floor and all key appliances visible, no characters. Keep the refrigerator separated in silhouette from the stove and prep counter.
Constraints: one refrigerator only; refrigerator must be large and usable; maintain an uncluttered central play area; no text, labels, logos, watermark, photorealism, 3D render, UI, characters, exterior seascape, giant windows, glass walls, aquarium, or duplicated appliances.
```

## Runtime gate (historical candidate note)

This candidate is intentionally not copied into `assets/`. Its native
`1672×941` generation does not satisfy the binding minimum of `2048×2048`
native background coverage for one playable screen. Promotion therefore
requires a compliant higher-resolution full-scene source master, then
non-overlapping runtime tiles, depth-card extraction (including the
refrigerator if interactive), import, license/provenance updates, and probe
validation. The currently conflicted rollback branch also contains pre-existing
castle asset changes, so no runtime files were overwritten during this audit.

## Production integration addendum

The historical gate above describes the review-only state before the owner
said to continue. Production integration now uses these rules:

- The accepted full frame is normalized as one complete canvas to the
  1024×576 logical stage; no subject is separately regenerated, translated,
  warped, or composited.
- The clean background is enlarged as one complete canvas to a 4096×2304
  production master. Both dimensions exceed 2048 pixels.
- The background master is split without overlap or scaling into a 3×4 grid
  of twelve 1024×768 runtime cards. Their reconstruction is pixel exact.
- Independently animated exact-pixel Sprite3D cards are extracted for the
  shell sink, oven, four individual copper pans, and refrigerator door.
- The refrigerator owns a subtle, pulsing mint silhouette glow and a
  picture-first menu. The menu reads the saved `opera_pantry`, always offers
  a pearl cake, conditionally offers carrot cake when carrots are present,
  and displays other recognized food inventory.
- Selecting a recipe enters the existing six-gesture cooking minigame.
  Leaving or finishing returns safely to the Royal Kitchen. Recipes do not
  consume inventory, so experimentation cannot lose collected ingredients.
