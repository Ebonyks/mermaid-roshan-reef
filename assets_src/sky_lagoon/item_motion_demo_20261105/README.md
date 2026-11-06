# Sky Lagoon — gentle ambient motion

Revision4 follows the owner’s November5 feedback: the existing items are okay, but movement, rotation and distortion must be far, far subtler. The camera, artwork, positions, original proportions and fixed roots stay the same.

![Gentle flower movement](flowers-closeup.gif)

[Stationary lagoon capture](fixed-camera-engine.gif) · [Nine individual trials](individual-items.gif) · [Engine recording](sky-lagoon-fixed.mp4)

## Motion direction

Primary sway is8% of the previous pass. Secondary shape deformation is4%, mechanical rotation5%, and window-light intensity12%. The seesaw now moves by only±0.5degree; the gate movement is a small4.1% opening fraction. Flower upper-canopy centroids move roughly one source pixel from rest. The4second/40frame cadence remains; lowering the excursion also lowers movement speed. This is ambient breathing, not exaggerated acting.

Every item stays on its own RGBA layer, including its rest frame. There is no painted-background/animation asset swap. Plants keep their fixed support bands. Every card uses uniform scale and the same source-root anchor. The background remains twelve unchanged native1024px cards from the approved v5 panorama.

## Open the demo

Open `demo_project/project.godot` in Godot4.7.2-stable. **Show still / Show breeze** compares the same items. **See each item / See the lagoon** switches views. A tap restarts the breeze. This is a standalone owner-review demo, with no main-game route or save changes.

## Sources and verification

All source art is reused. `derivation.json` binds source paths/hashes, methods, installed versions, the exact reduced profile and native master hashes. Each action has a job card in `jobs/`. There are no new item designs, generated-image calls or paid animation calls. Prior rejected LTX performances remain excluded; garden identity cutouts remain review-only sources.

Nine editable Aseprite1.3.18.4 masters hold forty complete RGBA cels at100ms each. The runtime uses matching lossless power-of-two atlases; GIFs are palette-limited review previews. Native source paint and protected originals are preserved. Explicit `process/fix_alpha_border=false` prevents automatic import recoloring of painted soft edges.

`evidence/machine-verification.json` checks all360 master/export cels, source hashes, plant root bands, unclipped edges, four-second GIF timing, measured small upper-canopy shifts and faint window-light change. The actual Mobile-renderer checks cover atlas sampling, uniform card proportions, preserved anchors, controls and the fixed camera. Forty lossless engine frames retain626,104 background pixels/frame unchanged. These are machine lanes, not human visual or device acceptance.

Rebuild loops with `python -B build_items.py`. Use Aseprite batch `--script-param packet=<absolute-packet-path> --script build_masters.lua`, followed by `verify_masters.lua`. Verify the current source context with `python -B verify_items.py --production-base a7e1faefc09b3303494a5499cce5fe120cb2dcb2`. Run the demo with `-- --verify`, or capture the stationary view with `-- --capture-fixed`.

## Remaining gates

The new subtle motion still needs owner and human normal-speed/frame-step approval. Production staging/occlusion/lifecycle, target-device timing/memory/overdraw, child and release acceptance remain open. The base atlas/background RGBA estimate is192MiB, not a measured phone budget.

The swing stays unanimated because matching fore/aft surfaces are missing. The door interior is still a flat source gap. Fir is shown only on the item board to preserve the mountain path. No new character acting, 3D asset or runtime adoption is claimed.

## Preserved history

Earlier manifests are retained as `prior_manifest_v1.json`, `prior_manifest_v2.json` and `prior_manifest_v3.json`; original outputs/masters remain at immutable source revisions, including169f6e90. The original scrolling preview remains owner-rejected. Later revisions corrected the window seam and overview proportions before this owner-requested intensity reduction. The unrelated aquarium-test failure at42066798727 attempt1 remains preserved in `evidence/ci-42066798727-attempt1.log`; no aquarium behavior, test, classifier or threshold is changed here.

The frozen `manifest.json` and exact remote-verification receipt define archive completion. `GENERATION_READY` is not applicable because no external generation is requested. `DELIVERY_ACCEPTED`, production runtime, device, child and owner acceptance remain false/pending. No master finding changes lifecycle.
