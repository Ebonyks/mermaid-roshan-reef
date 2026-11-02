# One Roshan, interchangeable garment skins

Status: proposed implementation workflow following the owner's2026-11-01 correction. The previous swimming comparison is useful diagnostic footage, but its multi-builder architecture is owner rejected. This document does not claim that the replacement runtime exists, accept the costume artwork, or authorize production integration.

## The missing production stage

The relevant process is **2D skinning and attachment binding**: registered garment pieces receive deformation weights and slot/layer assignments on an existing character rig. Retargeting between different skeletons is not the ordinary outfit workflow.

The source inspection in evidence/architecture_divergence.json finds seven independently implemented character builders, identical14-bone/rest definitions, and four base Body mesh/weight configurations. Matching skeleton definitions and animation timings prove useful compatibility, but do not establish one reusable character implementation. Clothing construction remains entangled with anatomy construction and per-family shaders/code.

Salvage the existing native wardrobe-switch primitive and original/ballet/magician bindings. They already exercise attachment changes on one actor, but their hard-coded garment lists and family-specific setup must become one generic loader with skin data. Reuse suitable painted garment parts from the other studies; do not commission another set of complete characters.

The desired separation is:

- **Character master:** approved face, curls/ponytail, anatomy cutouts, body proportions, scale/pivots, skeleton/rest, common deformation field, semantic sockets and view definitions.
- **Animation library:** one set of bone actions and semantic hand/view states, independent of costume IDs.
- **Skin package:** garment-only RGBA pieces, references to reusable attachment geometry or new garment geometry, weights on known bones, declared coverage/occlusion and view variants. No character builder, skeleton, animator or alternate anatomy.
- **Shared skin controller:** loads validated skin data into semantic attachment slots on the existing live actor. It owns removal, replacement and visibility, with no animation reset.

A comparison may display16 instances of the same character scene with different skin resources. That is valid reuse. The problem is separate character implementations and costume-dependent anatomy, not the number of figures displayed. The live switching proof uses one instance to expose replacement/reset mistakes that separate recordings can hide.

Godot's native Polygon2D skeleton path and bone weights provide the deformation mechanism. The project's shared loader, skin format and authoring/export tools provide the reusable skin system; merely using Skeleton2D does not supply that pipeline automatically. A custom RoshanSkin2D Resource or strict JSON manifest is appropriate. Do not use Godot's3D Skin resource or add a3D fallback.

## Authoring and binding workflow

1. **Lock the master first.** Select one source-only canonical Roshan anatomy/mesh/rest and version it. Remove prior clothes from replacement regions without redrawing her face or proportions. Fix common shoulder/waist support once in the master. A missing common view or anatomical surface is a master change, not15 separate costume repairs. This does not freeze the14-bone study forever: a needed skeleton/hand/view extension is one central version change with explicit skin migrations and revalidation, never a per-outfit rig fork.
2. **Publish a garment template per required view.** Use fixed canvas scale, neutral pose, pivots and neck/shoulder/elbow/wrist/waist/fin landmarks. Define front/back slots and shared join boundaries. Keep face, hair and permanent anatomy outside garment paint ownership.
3. **Create clothing pieces on that template.** Reuse existing suitable clothing art. ImageGen may repair a named garment/view gap using the approved master as registration/style reference, returning isolated garment pieces. Do not ask it to redesign or regenerate a complete costumed Roshan for each skin. Preserve originals, painted edges and provenance; use Aseprite for layered cleanup and exports.
4. **Reuse bindings whenever the shape permits.** A material/color variation references the same garment mesh, UV and weights. A genuinely different silhouette gets a garment-only mesh. Transfer initial weights from the canonical deformation field using registered position/barycentric mapping, then correct shoulders, cuffs, waist and hems manually. Do not modify the anatomical Body mesh to fit each outfit.
5. **Enforce interface joins.** Neck, cuffs and waist use compatible boundary positions, weights and coverage rules across mixable parts. A tiny arbitrary overlap patch cannot certify compatibility. New cloth may extend beyond the base outline; its silhouette is owned by its attachment, while shared seam rules remain fixed.
6. **Assign occlusion and optional parts as data.** Separate back/front cloth where arms or the tail pass through it. Headwear has appropriate hair occlusion. Gloves select canonical hand-pose variants. A skin cannot substitute another face, eye layout, body scale or hair design.
7. **Bind job tools separately.** Hats and rigid tools follow named bone/socket transforms. A sleeve/coat deforms through weighted geometry. GripLeft/GripRight are verified offsets on painted hands, not assumed bone origins; the current RightHand origin probe already shows why that distinction matters. Shared hand poses and front/behind finger layers establish grip/contact. Outfit data must not create a new actor to hold a tool.
8. **Run the unchanged action suite.** Test every affected action/view, extreme, transition and loop. Analyze actual material-visible contours, seams, strain, identity, contacts and original-clothing leakage. Repair the garment art/mesh/weights or shared master according to defect ownership, then rerun affected skins. Different meshes' alpha must not contaminate a mesh's visibility mask.

## The next proof must use one live actor

Use two complete skins first, such as Chef and Magician. Run one continuous swimming action and switch Original → Chef → Magician → Original at mid-stroke. Then repeat during arm bend, blink, tail extreme, entry/exit and pause/resume. Do not substitute recordings of separate actors or restart the action between looks.

Record and assert:

- Actor, Skeleton2D, bone and animator instance IDs remain unchanged.
- Bone count, names, rest transforms, immutable anatomy geometry/weights and identity texture hashes remain unchanged.
- Animation/phase, position, scale and camera remain continuous across equip operations.
- Only intended garment attachment data changes; prior attachments are removed atomically, with no double clothing, leakage, missing required slot or stale prop.
- All attachments bind to the existing skeleton and known semantic slots/views. Incompatible rig versions, unknown bones and invalid weights are rejected before state changes.
- After repeated swaps there is no node/material/texture growth. The actual target device establishes memory and30fps feasibility separately.
- Full sets and every exposed head/body/tail combination pass geometry/outline/contact checks. Unsupported combinations stay unavailable until repaired.

The practical acceptance question is: **Can a new outfit be added with garment art and one skin data file, without editing character/animation code or rebaking her face?**

Only after this two-skin live proof passes should the remaining outfit studies be converted to data-only skins. Their existing art can be salvaged; their independent character builders are reference/diagnostic sources, not the new architecture. The swimming action's current numerical failures remain recorded; this workflow is not acceptance of that performance.

## References and scope

- [Godot Polygon2D API](https://docs.godotengine.org/en/stable/classes/class_polygon2d.html): shared Skeleton2D binding and bone weights. These APIs were exercised by the existing exact4.7.2-stable native captures.
- [Godot2D skeleton tutorial](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html): polygon weighting and deformation; the upstream tutorial itself notes that its4.7 update is incomplete.
- [Spine skins documentation](https://en.esotericsoftware.com/spine-skins): reference for semantic slots/skin placeholders and linked garment meshes. This is an architectural reference, not a software purchase or migration instruction.

Full-speed playback automation stopped because Computer Use could not verify the Windows browser URL. No further UI input was sent. Agent frame/metric review and pixel-exact archives do not replace human normal-speed, phone, child or owner acceptance. The source-only demo freeze and master UNSATISFIED state remain unchanged.

## Operational conversion recipe

The [costume-to-skin conversion guide](../../../design/animation/COSTUME_SKIN_CONVERSION_GUIDE.md) is the repeatable preparation/format recipe. It adds proposed machine-readable schemas and data-only packaging/validation helpers, with the architecture criteria also written directly into the master audit. Helper conformance is not live-actor or visual acceptance.
