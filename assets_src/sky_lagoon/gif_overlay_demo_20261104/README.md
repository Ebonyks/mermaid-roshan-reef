# Sky Lagoon animated overlay demo

Owner commission, November 4, 2026. Review candidate under the [master audit](../../../audit/MASTER_AUDIT_2026-08-09.md) and [impact record](../../../design/audit_impacts/sky-lagoon-gif-overlay-demo-20261104.json).

Open `demo_project/project.godot` with Godot 4.7.2-stable and run. Drag horizontally with one finger or the mouse to explore the painting. A tap recentres the view. Press M on desktop to compare motion with the source painting.

The fir crown, meadow leaves, lakeside lupines and open water are crops of the approved v5 panorama. Four fresh four-second loops use 32 frames at eight frames per second, with different playback phases. The background retains all twelve native 1024 cards. Every moving patch stays in the same master coordinates throughout playback.

The loops are declared ambient raster deformation. No new item or appearance drawing was generated. The source identity, source flowers and leaf arrangement stay intact. The October rejected object performances are excluded. This pilot tests breeze and ripples, and supplies no authored playground action or Roshan performance.

The local patch contains matching scenery around the object, with a stationary transparent guard at the outer border. Its moving interior covers the corresponding original pixels, avoiding two visible versions of a leaf. Bases, paths and unselected pixels stay fixed. The patches retain local scenery around each item and belong at their recorded background coordinates. They must sit behind actors. Foreground overlap needs a reviewed silhouette matte and matching hidden background, as described in the earlier G2 handoff. That source and occlusion work remains open. The meadow trial locks the top 96 rows, including the paving between stems, and animates the lower leaves. The earlier broader mask is preserved under `prior_meadow_mask` as a rejected scope diagnostic. The source and motion-weight PNGs expose the complete edit region. GIF previews use a single palette per loop. The demo uses the same frames as lossless PNGs to retain the original paint at the joins.

`build_demo.py` reproduces the source crops, loops, masks and frame hashes. `build_masters.lua` puts those exact flattened RGBA frames into four one-layer Aseprite masters. `manifest.json` records source hashes, coordinates, methods, cadence, fixed-pixel checks and acceptance limits. The `evidence` folder retains strict-test failures and later verification separately.

The current full-residency estimate is 97.31 MiB of base RGBA texture data, including the panorama. This excludes driver overhead, render targets and other game assets. Byte-identical cels share a texture resource. The demo culls drawing outside the camera view. Target-tablet residency, frame time, overdraw and thermal behaviour still require measurement.

## Rebuild sequence

1. Run `python -B assets_src/sky_lagoon/gif_overlay_demo_20261104/build_demo.py` from the repository root.
2. Run Aseprite in batch mode with `--script-param packet=<absolute packet directory> --script <packet>/build_masters.lua`.
3. Import the nested project with the approved engine. Run it with `-- --verify` for the desktop pixel/playback/pan check, or `-- --capture-tour` for a deterministic camera tour.

## Next work using the existing plan

1. Review the four loops in the scene and at native size. Record any contour stretching, plant contact, visible border, unwanted motion and loop-seam failures against exact hashes.
2. Trim and pack the selected loops, retain their master registration and measure the existing Speedy-tier texture, overdraw and frame-time budgets on the Lenovo M11. Expand only the source regions that meet those checks.
3. Reuse this continuous-overlay path for other already-authored background items after source inventory and a bounded trial. Existing cloud and chimney art are candidates for that inventory. The prior handoff's G1 motion regions and G2 depth needs remain distinct tasks.
4. Wire accepted loops into the promenade's matching background Canvas layers, with lifecycle and scene-reentry checks. Add foreground placement only after the silhouette, revealed background and actor-occlusion checks pass. Preserve route, animal-floor and save behaviour during that later integration.
5. Keep the existing playground and gate work scoped to their real geometry and authored states. Missing fore-and-aft surfaces, hidden background or valid motion keys remain source gaps. This source-only commission supplies no replacement designs.

Human visual and full-speed motion review, physical-device performance, child and owner acceptance remain open. The standalone project is excluded from the shipping game by `.gdignore`. No master finding is closed.

The final [verification receipt](evidence/verification_summary.json) binds the static-gate chain, normal guarded import and all 82 trusted probes. The initial boss process exit 127 is retained beside the unchanged native retry that exits 0. Both 1280×720 and 1280×800 desktop Mobile checks pass, and Aseprite verifies all 128 complete cels. Source rest RGB is exact; rendered comparison permits one 8-bit colour step of texture sampling. These checks grant no owner, child or physical-device acceptance.
