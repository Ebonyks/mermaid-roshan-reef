ROSHAN — SHARED NATIVE GODOT SWIM / TWO-SKIN SOURCE PROTOTYPE
Owner review draft, 2026-11-01. No production integration or acceptance.

MASTER AUDIT HOLD
The owner's latest instruction is: "Test before adding to master audit, do not
do so until permission is specifically given". The master audit, finding
lifecycles and canonical audit index are unchanged. Test evidence and this
source guide do not grant permission to write back or close a finding.

WATCH / TRY
review/live_swaps.mp4 is the primary test: five swaps during one swimming
sequence, with native animation phase and actor identity displayed.
review/ballet.mp4 and review/magician.mp4 show the same actor captured
sequentially in each costume; review/two_costumes.png compares them.
The grid is QA instrumentation derived from the actual recorded native root.
The character is native Godot RGBA, never a Python-painted character.

Launch this folder's project.godot using exactly Godot 4.7.2-stable. The source
fixture uses Mobile rendering and never loads the game or its saves.
Click Ballet / Magician or press B / M. Space pauses/resumes. The costume
switch only updates five persistent garment nodes. It never calls play,
seek or stop, recreates bones, or changes the actor's position/velocity.

STRUCTURE
shared_actor.gd creates ONE Node2D actor, ONE Skeleton2D (19 Bone2D nodes)
and ONE AnimationPlayer. It reads one canonical rest/anatomy contract.
The animation has a 7.6s entry/propel/brake/settle sequence and 1.9s cycle.
Head, rainbow ponytail, bare arms, neck/shoulder insert and fin are common.
No default pink shirt or original violet tail is drawn under the costumes.
The generated original shirt/tail pieces supply registration references only.
Each skin owns the actual drawn bodice, tail cover, two sleeves and headwear.

The common fin interpolates three authored views on ONE fin node. The shared
material blends signed contours and source pigment, without the rejected
gradient UV projection. It is declared 2D pose interpolation, not proof of
physically accurate swimming. Its appearance still needs exact human review.
The simple travel model uses actual pelvis/tail/fin skeletal tip motion. The
ablation freezes Hips, TailA-D and Fin bones plus fin view controls; other
upper-body tracks continue. This is a qualitative causal prototype, not fluid
simulation. There are no per-costume motion curves or character builders.

FORMAT AND CURRENT LIMITS
rig/rig_binding.json: roshan.rig-binding/1, roshan.canvas.shared.swim 0.1.0.
skins/{ballet,magician}.json: roshan.skin/1, pinned to the exact same rig hash.
Five required slots: body_front, tail_cover, sleeve_left, sleeve_right,
headwear_front. Layers and required coverage come from the canonical rig.
Native loader subset: weighted attachments only, one swim_right_quarter view,
and garment-owned PNG paths. A rigid-looking hat/sleeve uses weight 1 on its
named bone. The general Python schema/helper also describes rigid packages;
that does NOT mean the native prototype implements them.
Cached assets are immutable for a session. Rebuild and relaunch after changing
a file; this prototype does not implement on-disk asset hot reload.
Renderer program files are outside the data-only rig/skin asset contract.
The anatomy JSON pins numeric fin fields, verified by the native core.
Native run and publication manifests pin the actual renderer program bytes.

Stable existing Fashion Designer head/body/tail IDs are recorded in
skins/catalog.json. Only Ballet and Magician have been translated here.
This does not establish compatibility for the other costumes, other facings,
new actions, facial acting, grips, transparent/revealing clothes or objects.
Grip socket names are authoring placeholders, not accepted prop contacts.
There is no Android export or actual Lenovo Tab M11 performance evidence.

COSTUME TRANSLATION / OBJECT BINDING GUIDE
1. Inventory the current Fashion Designer masters and approved identity.
   Preserve originals and their rights/hashes. Existing upright complete
   portraits are design references, not attachable skin payloads.
2. Separate garment objects in native Aseprite, preserving painted contours
   and antialiasing. A payload must contain clothes only: no face, hair,
   hands, replacement anatomy or baked whole character. If a suitable action
   view is missing, request that named GARMENT-ONLY view using common rig
   part proportions and the original costume design; never request a new
   costumed Roshan. Record input roles, prompts, calls, rejected results,
   source scope and cleanup. Approval of a reference does not accept output.
3. Register neckline/waist, shoulder openings, tail-root/chain/tip and headwear
   anchors against the same canonical rest pose. Begin with uniform fits;
   inspect the intermediate chain, not just the end points. If the garment's
   perspective/shape cannot fit naturally, repair that source view. Do not
   stretch a portrait, clip to the old costume's alpha or shift the skeleton.
4. Give each object its own canonical-canvas UV mesh and normalized known
   bone weights. Use the SAME canonical weight fields across costumes.
   The curved tail uses smooth neighbourhood-blended arc coordinates: hard
   nearest-segment switching produced a real visible strain crease.
   A sleeve/hat can be effectively rigid with one bone. Keep anatomy, the
   common fin, animation and object sockets owned by the actor.
5. Build a data-only recipe using the root skin_binding schemas/templates.
   Preserve rig ID/version/hash, supported view, exact required coverage,
   source/edit/license provenance and current wardrobe IDs. The preparation
   helper packages an already-authored fit; it does not automatically segment
   art, infer perspective, generate weights or certify pixels. The validator
   checks structure/references/weights, not whether a picture is garment-only.
6. Apply on the SAME live actor at mixed phases, roots and velocities and
   while paused. Record actor/skeleton/bone/animator/anatomy/slot/material IDs,
   rest/pose hashes, native phase and root state before/after. Test exact
   restoration and invalid rig/view/slot/code/hash/path/anatomy controls.
7. Render complete entry, steady stroke, braking, settle and loop seam for
   each skin. Inspect each material's own source alpha and native bone
   matrices: unchanged strain floor [0.8,1.2], zero flipped triangles,
   angular speed <=140deg/s, acceleration <=650deg/s2. Measure fin-view
   controls separately. Test all visible texel centres, not a few points or
   a whole-character alpha union. A successful encode or smooth bone metric
   cannot accept a bad material/view transition.
8. Audit native output outlines: no clipped edges or detached visible parts;
   identify intended holes (for example the Ballet tiara arch) explicitly.
   Compare live-swap pixels with standalone output at the SAME pose, phase,
   root and camera, including the FIRST drawable frame. Never normalize each
   costume with a separate camera to conceal registration differences.
9. Review full speed and frame-step at every view/contact/occlusion/swap and
   seam. Check face/anatomy/fin count, original clothes bleeding through,
   cuffs/neck/shoulders, sliding joints, line weight, occlusion, colour, pauses,
   body-supported motion and readable endpoints. The geometric floor alone
   does not establish natural motion or identity/style acceptance.
10. Keep implementation, machine results, exact human review, actual-device
    playback/performance, child and owner acceptance separate. For a new
    facing/action/slot/occlusion requirement, revise a versioned common
    contract and recompile/retest every skin. Do not hide unsupported pose
    selectors or a custom character builder in a v1 package. Opaque clothes
    currently provide body/tail surfaces; a new opening needs an appropriate
    shared anatomical underfill, never an old outfit or per-costume anatomy.

REPRODUCTION (from repository root)
Run python assets_src/animation/roshan_shared_swim_20261101/tools/run_native.py
with --mode import/check/pose/verify/capture (choose one mode). Supply
--godot <exact-approved-executable> if the local Windows default differs.
Source asset rebuilding uses this folder's tools/build_assets.py, then
tools/prepare_fin_views.py; the
latter updates common fin data and repins both skins. Both use native
Aseprite 1.3.18.4 for bitmap isolation/registration; originals are preserved.
Then run the root validate_costume_skin.py for EACH actual package, the
native fixture, audit_native_geometry.py, audit_swap_pixels.py and
make_review.py. The latter records exact RGBA round trips for all native
frames in masters/*_native_rgba.mkv (RGB track 0, alpha track 1).
The helper defaults to this workstation's FFmpeg 8.1.2 path.

EVIDENCE / ACCEPTANCE
evidence/native_capture_receipt.json pins actual executed source inputs and
fresh process completion; native_capture_complete.json records all three
full 229-frame captures and five live before/after swap snapshots.
native_swap_tests.json is actual Godot evidence, not a simulated pose counter.
native_geometry_audit.json, swap_pixel_audit.json, media_roundtrip.json and
the review sheets supply separate measurements. result_summary.json records
current status. Failed technical stages and rejected motion are retained
under evidence/history with explicit roles; they are never runtime fallbacks.
Framing diagnostics are stored as explicit lossless RGB/alpha XOR video
frames against named paired-track bases; pack_diagnostic.py verifies every
reconstructed frame. Opaque high-compression ZIP transport was rejected by
the unchanged 2D-only gate and replaced after all decoded data matched.
The format-metadata preflight uses the final identical pixel archive, with
all frame hashes explicitly compared after revalidation.

Four built-in ImageGen calls filled named shared-view, Ballet, Magician and
neck gaps; one take each, no paid API jobs and no per-frame campaign. Model
revision, seed and monetary usage were not exposed. Aseprite masters preserve
editable source parts and three common fin keys. Godot source owns timing
and weights. Source PNGs/references above 1024px remain source-only; active
runtime image textures meet the project's size rule.

Publication is a source REVIEW packet, not game integration, device approval,
creative acceptance or finding closure. Master-audit writeback remains held
until the owner specifically approves the tested results.
