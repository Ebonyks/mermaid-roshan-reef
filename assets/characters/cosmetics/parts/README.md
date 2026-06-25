# Cosmetic parts library

One GLB per socket cosmetic, referenced by `assets/characters/cosmetics/catalog.json`.

Rules:
- **One mesh per file**, authored at the **origin** in its socket bone's local
  space (the runtime attaches it to the bone, so origin = the bone).
- Export **glTF Binary (.glb), +Y up**, no animation, keep it small.
- Filename matches the catalog `asset` entry (e.g. `wings_fairy.glb`,
  `crown_pearl.glb`).
- Validate: `python3 ../../../../tools/glb_check.py wings_fairy.glb`

Socket bones these parts attach to (added to Roshan's rig when re-rigging):
`headTop, backL, backR, earL, earR, tailTip, handHold` — see
`tools/build_roshan_cosmetics.py` and `CHARACTER_CUSTOMIZATION.md §8`.

Material/texture cosmetics (hair recolour, sparkle tail) and morph cosmetics
(fairy ears) are **not** parts — they live entirely in the catalog + runtime and
need no file here.

> Empty for now: no part art exists yet. The runtime skips missing parts safely,
> so the catalog can list them before the art lands.
