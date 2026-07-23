# Dirty Castle Scene-Resemblance Audit

## Result

**PASS — 41/41 reusable scene-bound dirty skins score 5/5.**

The original concept-generated object drawings did not meet the owner's new
resemblance standard. All 41 sprites that depict a clean castle fixture, toy,
piece of furniture, or storage prop were regenerated from exact transparent
renders of the shipped GLBs. The underlying clean render is preserved
pixel-for-pixel outside the deliberate grime mask.

The other 55 runtime sprites are auxiliary decals, tools, feedback, progress,
or dust-bunny art. They do not replace or impersonate an existing clean scene
object, so clean-object resemblance is not applicable. They remain subject to
the ordinary transparency, padding, readability, palette, and mobile-runtime
checks.

The 36 cinematic frames are narrative illustrations rather than reusable object
skins. They are not included in this skin-resemblance score.

## Source of truth

The audit does not use the earlier generation prompt as a clean reference.

1. `scripts/arena/castle_hall.gd` establishes which room and fixture are live.
2. The referenced GLB under `assets/castle/`,
   `assets/castle/pearl_kit/`, or `assets/art35/castle/` establishes object
   geometry and material blocks.
3. `tools/render_dirty_castle_references.py` renders each live model to an
   orthographic 1024×1024 transparent reference using Blender 4.4.
4. `tools/process_dirty_castle_2d.py` fits that exact render to the 512×512
   runtime canvas and composites only the washable mess layer.

The complete machine-readable object-to-GLB mapping and per-sprite metrics are
in:

- `audit/dirty_castle_2d_2026-07-22/scene_resemblance_ledger.json`
- `audit/dirty_castle_2d_2026-07-22/scene_resemblance_ledger.csv`

## Five-point gate

Every reusable scene-bound skin must pass all five checks:

| Point | Requirement | Final result |
| --- | --- | --- |
| 1 | The clean object comes from the live shipped GLB, not a prose redraw | 41/41 |
| 2 | The exact transparent Blender render is the dirty skin's base layer | 41/41 |
| 3 | Every clean opaque pixel remains represented in the dirty result | 100% silhouette recall on 41/41 |
| 4 | Pixels outside the deliberate grime change mask remain unchanged | Exact on 41/41 |
| 5 | Final output is padded 512×512 RGBA suitable for Godot | 41/41 |

A score below five is a failure. There is no rounding of 4/5 to pass.

## Audit cycles

### Cycle 1 — failure

- Scene-bound sprites inspected: 41.
- Failures: 41.
- Cause: the earlier image-generation pass used runtime captures only as
  stylistic references and redrew fixture geometry. This changed silhouettes,
  trim shapes, shell motifs, proportions, palettes, and—in several cases—the
  kind of object itself.
- Particularly clear failures: bathtub, vanity, toilet, kitchen counter,
  kitchen sink, stove, toy chest, rainbow stacker, bookcase, pantry shelf, and
  undercroft storage.

### Regeneration

- Exact model references rendered: 30.
- Scene-bound outputs rebuilt: 41.
- The image-generation pass was limited to a grime decal; it was not allowed to
  redraw any live object.
- Legacy output filenames were retained so future wiring cannot accidentally
  break, but the ledger records the exact live model behind each file. For
  example, concept-only tea-set/cart/cup drawings are replaced with the live
  shell drum, library table/bookcase, teapot, kettle, and pan-set vocabulary
  already present in the castle.

### Cycle 2 — pass

- Scene-bound skins: 41/41 at 5/5.
- Silhouette recall: 1.0 for every entry.
- Pixels outside the grime mask: unchanged for every entry.
- Transparent padding: at least 24 pixels for every entry.
- Final failures: 0.

## Human visual evidence

- `audit/dirty_castle_2d_2026-07-22/scene_reference_objects.png` — all 30
  exact shipped-model references.
- `audit/dirty_castle_2d_2026-07-22/scene_resemblance_pairs.png` — clean and
  dirty versions side by side for all 41 regenerated skins.
- `audit/dirty_castle_2d_2026-07-22/sprites_contact.png` — complete 96-sprite
  runtime library after regeneration.

## Godot use

For a fixture skin, align the sprite against the matching existing node named
in the ledger. Do not use a dirty sink skin on the vanity, a generic toy skin
on the stacker, or a room vignette as a replacement for geometry.

The sprite may fade away to reveal the live clean GLB, or its grime-only change
mask can be extracted as an overlay. It must never permanently hide or replace
the interactive fixture.
