# Aseprite complete-cel repair and reusable source profile

Status: **SOURCE CANDIDATE / NOT OWNER ACCEPTED**. The frozen artwork source is
`full_wave_draft_06`: 41 complete native cels and an editable one-layer master.
Ordered native review found formed connected hands, cuffs and hair contours,
with no lowering-hand smear, old-arm skin strip or fingertip crop. Final RGBA,
normal-speed motion, exact K0 seam, device/runtime and owner evidence remain
separate. Root owns the final matte/export package. This folder is non-runtime
source/evidence, not an external handoff or an accepted performance.

The gap is the blurred/incomplete lowering hand in the native LTX wave. The
41 complete source drawings in `../native640_01/take_01/native_frames/` remain
untouched. Aseprite 1.3.18.4 paints a newly authored connected arm, palm, four
unequal fingers and opposed thumb directly into each complete native cel.
GraphicsContext paths, antialiased contours and authored painted color fields
produce fresh local drawing pixels. No hand/arm appearance template, cropped
part image, rig, part sprite, warp, crossfade or appearance interpolation enters
the repair. Native coordinated whole-body action remains outside the declared
repair/preservation domain. Every master cel is one complete flattened image.

The native workspace is 768×896: the complete 640×896 original is translated 128 px
right onto a neutral field. Planned whole-image delivery maps it uniformly to
240×280 and translates [15,-10] onto 256×256. Original source files are preserved.
Final first/last drawings are exact approved K0 in the derivative package, with
native whole-K0 endpoint provenance there.

The painted bones are constant U 80.2/F 80.2 native throughout frames 1–39, giving
25.0625/25.0625 at the exact 0.3125 export scale. The open-hand design target is
65.651 native with 2.4 px visible-outline fringe compensation. Relaxed hands have
separate filled curved-finger controls, shallow valleys and a warmer lighter
contour, and stay `hand_open:false`. Monotone cubic Hermite interpolates declared
shoulder/angle keys; hand states blend authored control coordinates. Approximate
identity-fit scale 3.2025 in older metadata is registration evidence, not the
exact native-to-delivery scale.

## Executable profile format

`engine_profile.json` declares v2 inputs and reproduces frozen 06.
`recipe_profile.schema.json` lists required fields and their structures. The
profile supplies whole-frame `source_dir`, `source_canvas`, padding, repair
bounds, source-hash-bound head-coordinate masks, `head_protection`, fixture
regions/color predicates/dilations, fixed lengths, pose/shoulder keys, palette,
relaxed-hand controls and whole-image mapping. This wave action remains 41 frames
at 24 fps and 1708 ms; the source recipe does not lower that contract.

`head_protection` exposes seed region, coordinate margin, skin exclusion,
hair-color thresholds, outline/AA dilation and face/upper-head guards.
`fixture_domain` exposes sleeve membership, upper/lower preservation margins,
repair edge and old-skin/shadow erasure. Palette and fresh-fill membership are
configurable together. Regions are [x0,y0,x1,y1] inclusive in un-padded source
coordinates. Difference thresholds use strict `>`; hair maxima use strict `<`.
The source family uses a 2 px cuff/body margin through y439 and 5 px around the lower
outfit, plus bounded warm old-arm shadow erasure below y332. These source-specific
preservation settings require inspection and rebinding for another outfit.

`prepare_full_draft.py` validates the local schema subset using only the Python
standard library, rejects rig/part-appearance input fields, confines source and
output paths, verifies every native SHA256 against the bound coordinate mask,
and refuses an existing output folder. It freezes UTF8LF profile/mask JSON, the
exact recipe, schema, preparation-code snapshot and source/recipe binding. It
does not render pixels.
Legacy v1 profiles retain defaults solely to preserve prior evidence.

Run from the worktree, using a fresh output name:

```powershell
py -3.10 -B assets_src/animation/roshan_wave_repair_20261010/aseprite_paint_trial_01/prepare_full_draft.py --profile engine_profile.json --output new_source_draft
```

Pass the frozen paths to Aseprite 1.3.18.4:

```text
Aseprite.exe -b --script-param root=<absolute-repository-root> --script-param output=<absolute-frozen-output> --script-param config=<frozen-output>/recipe_profile.json --script <frozen-output>/paint_connected.lua
```

The recipe refuses to overwrite a master. `--sample-frame 28` prepares a whole-cel
reproduction/pilot, explicitly separate from a complete performance.
`engine_profile_reproduction_01` proves explicit v2 defaults reproduce frozen 06
cell 28 byte-for-byte and pixel-for-pixel: SHA256
`f062779e0a6881e11bccd288fb73e61896b724955adc247af0b1b7b11333f3b4`, maximum
channel difference 0. Frozen 06 artwork/recipe/source snapshots remain untouched.
The proof also archives its SHA-verified historical preparation helper. Earlier
frozen 06 records the helper hash without a helper copy; its exact rendering Lua,
profile, masks and native inputs are preserved and sufficient to re-render it.

## Review and preservation

Inventory accepted complete sources first. Bind a source profile and review a
small pilot spanning rest, rise, peak and lowering before expansion. Keep failed
native evidence. Inspect every contour, joint attachment and output bound, then
run read-only raster inspection:

```powershell
py -3.10 -B assets_src/animation/roshan_wave_repair_20261010/aseprite_paint_trial_01/inspect_painted_geometry.py --draft new_source_draft
```

Authored shoulder/elbow/wrist/hand targets are not model-measured landmarks.
Raster transverse centers and fitted elbow-axis intersections are separate
estimates; near-straight elbow fits are especially uncertain. Frozen 06 measures
open-hand tips 19.951–20.296 at final scale and hand canvas margin 122 native px.
`full_wave_draft_06/native_review_addendum_v2.json` clarifies current cuff and
relaxed-hand descriptions while preserving all frozen raster measurement arrays.
`engine_profile_reproduction_01/reproduction_proof.json` records the exact cel
comparison. `workflow_freeze_record.json` pins the current reusable workflow.
Numerical evidence does not accept art or motion. Bind matte
to exact frozen source hashes, inspect every RGBA frame on light/dark fields,
play the full loop at normal speed, and inspect K0 neighbors/seam before later
runtime/device/owner gates.

Prototypes 01–03 tested angular/rounded contours and removed waist remnants.
Prototype 04 warranted the full trial without granting acceptance. Full 01/02 had
preservation-mask defects; full 03 improved padding/hair but retained a cuff skin
block. Full 04 fixed that block but retained an old-arm warm shadow and dark
comb-like relaxed fingers. Full 05 removed the shadow; full 06 carries the
independently reviewed filled-hand repair. All rejects remain preserved.

This local paint lane uses no generated API calls, GPU jobs or external monetary
cost. `cleanup_time_ledger.json` records actual first recipe creation and a
conservative contiguous authoring/review/cleanup/wait interval, plus instrumented
pass start/end times and explicit filesystem proxies otherwise. Failed drafts
count; pass seconds are not summed again. Earlier pre-recipe discussion is an
explicit unclocked limit for the parent ledger. Task limits do not reset between
drafts. Immutable PowerShell pilot profiles retain their executed encoding;
current prepared v2 inputs/bindings are UTF8LF.

API documentation: https://aseprite.org/api/graphicscontext and
https://aseprite.org/api/image .
