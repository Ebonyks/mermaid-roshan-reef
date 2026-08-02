# Northern Kingdom Blender handoff for Claude — 2026-07-20

## Starting point

Continue from content commit `b7ecea03a1b4aa44b5ea7f604aeb4f8c9428e1bd`, which passed
the exact-HEAD gate. The Northern Kingdom audit is complete: all
25 runtime art families are authored Blender exports and score 4.50–4.74/5
under the capped-4.90 rubric. Do not restore any of the removed primitive
Godot substitutes.

Read these sources before changing art:

- `NORTHERN_KINGDOM_QUALITY_AUDIT_2026-07-19.md`
- `audit/northern_quality_ledger_2026-07-19.csv`
- `tools/build_northern_kingdom_kit.py`
- `scripts/arena/northern_kingdom.gd`
- `scripts/probe_northern_art_audit.gd`

The authoritative editable scene is
`assets_src/blender/northern_kingdom_kit.blend`. It contains the 25 source
families exported to `assets/northern/*.glb`. The corresponding isolated
Eevee reviews live in `assets_src/blender/qa_northern_kingdom_kit/`.

## Requested continuation

Produce the next Blender refinement versions of the existing Northern assets,
one independently reviewable family at a time. Preserve each accepted asset's
runtime name, root orientation, footprint and role so existing placements do
not drift. Prioritize the lowest accepted scores first:

1. `northern_peak_a` (4.50)
2. `northern_peak_b` (4.51)
3. `northern_pine_a`, `northern_mushrooms_tan`, and `northern_forge` (4.52)
4. `northern_pine_b`, `northern_house_rose`, `northern_mill_house`, and
   `northern_hall_centerpiece` (4.55)

The full current family list is the `ASSETS` table at the bottom of
`tools/build_northern_kingdom_kit.py`. Prefer stronger silhouette, broad
modeled detail, clean material separation and child-readable landmarks over
microdetail. Keep models texture-free unless a texture is demonstrably better,
Mobile-safe, licensed, and entered in `ASSET_LICENSES.md`.

Use the deterministic builder as the reproducible baseline:

```text
blender --background --python tools/build_northern_kingdom_kit.py
blender --background --python tools/build_northern_kingdom_kit.py -- --only=northern_peak_a
```

If a refinement is modeled interactively, retain an editable Blender source
and a reproducible export path; do not leave the GLB as the only source. Update
the combined `.blend`, GLB, isolated QA render, audit score/evidence and license
entry together.

## Acceptance contract

- Score ceiling: 4.90. Reject anything below 4.50; target 4.60+ for a new
  revision and never regress the current family score.
- Review first in the isolated Eevee render, then in the fixed Godot Mobile
  capture set from `scripts/probe_northern_art_audit.gd`.
- The accepted exact-HEAD evidence is GitHub Actions run `29764110846`, artifact
  `northern-world-review`. `north_22b_hall_bedroom_set.png` is the useful
  bedroom front check; the wider `north_22_hall_bedrooms.png` is partly blocked
  by the bay wall and should not be used alone to grade the model.
- Preserve placement continuity: snowline pines may stand in snow; mushrooms
  belong only on damp forest litter; no tropical plants, palms, cactus, coral,
  kelp, seagrass, anemones or mangroves belong in the Northern biome; structures
  require grounded footprints and water-specific objects require a shore or
  stream relationship.
- Preserve the Speedy-tier budget. Add no physics bodies and no new OmniLights.
- Never modify or substitute `assets/book/`, `assets/audio/voices/`, or
  `assets/characters/friends/` during this art pass.

Before pushing any revision, run the changed-GDScript parser/inference gates
and the full trusted probe workflow. Work from a fresh branch off `origin/dev`;
never commit directly to local `dev` or `master`.
