# Object development guide

**BINDING_DOMAIN** for visual construction and verification of world objects, under the [design language](06_COMPREHENSIVE_DESIGN_LANGUAGE.md#6-2d-canvas-living-card-world-construction). Owner direction, 2026-11-11, asks for five review rounds followed by adoption in the [master audit](../audit/MASTER_AUDIT_2026-08-09.md#development-task-index). Use this guide when planning, adding, replacing, or changing a world object's depth, composition, motion, or interaction.

A world object can read as solid through its silhouette, projected surfaces, contact with the ground, and the order in which it covers other objects. Mermaid Roshan builds those cues with its existing storybook artwork using 2.5D composition on the Godot 2D Canvas. Choose the smallest assembly that preserves the silhouette, required action, and readable overlap.

## What transfers from Cult of the Lamb

Massive Monster describes placing hand-drawn sprites in a spatial scene, adjusting them in the editor, and arranging important objects toward the back because the camera angle was relatively fixed. Their farm-roof breakdown is evidence of deliberately arranged sprite pieces for that example. It leaves the exact render order, offsets, masks and other props' construction unspecified. The useful choices are a controlled projection, common seams, and evaluating objects in context with the camera and actor. A four-course height stack is an independent Roshan experiment. [Massive Monster interview with Unity](https://unity.com/blog/games/recipe-behind-smash-hit-cult-of-the-lamb), [Wilton interview with ACMI](https://www.acmi.net.au/stories-and-ideas/making-games-julian-wilton-massive-monster/), [studio-posted farm breakdown](https://www.reddit.com/r/Unity3D/comments/1joamr1/comment/mktrdls/).

The owner-provided recording supplied visual observations in the earlier study. The approach at 00:47 reads through deck, facing and bank separation. At 05:24 a near canopy frames the active ground. At 08:55 paving and uprights lead the eye to an entrance. These observations establish the screen composition. Construction details come from the studio's accounts and the Roshan tests. Carry over the compositional cues into Roshan's bright painted materials, familiar props and gentle play.

### Evidence from the three Roshan fixtures

| Fixture | What the assembly proved | Defect it exposed |
| --- | --- | --- |
| Stone bridge | One projected deck outline supplies the fascia and return seams. Far and near rails are separate cards around the actor. | The first deck image fell short of the bank even though the motion reached it. Widening the shared outline fixed the visible connection. |
| Harvest bushel | One existing painting supplies the back/interior and the near rim/front. A berry occupies the band between them. | The first settled berry disappeared behind the rim. Raising the socket 27 pixels at the fixture scale made its arrival legible. |
| Trail marker | Four bounded courses and a separate cap show height with a stable ground contact. | A placeholder texture supplied unusable UVs. A real RGBA quad restored the course shape. |

The retained Godot 4.7.2 Forward Mobile captures cover 1280×720 and 1600×720. The pixel check was rerun for this review. Empty bushel reassembly matched the intact source in RGB at both sizes. Inverting the near rail changed 1,008 pixels by more than two RGB code values and left the sampled face region identical. Inverting the bushel rim changed 624 pixels at that threshold. The sampled marker foot was identical at both heights. These numbers describe the exact bench poses and sampled areas. Full-route navigation, alpha across backgrounds, device performance and production acceptance require their own evidence.

## Choose the construction by the job

Start with the approved silhouette at play scale, a ground-contact mark and a sketch of what moves. Add a card only where a separate surface, motion, or overlap changes what the child sees or does. Decorative grain, little bevels and fixed inlays can live in the same painting.

| Object and visible job | Assembly to try first | Review at the point of failure |
| --- | --- | --- |
| Stationary rock, sign or decorative pot | One owned painted card with broad top, front and side values. Put the origin at the ground contact. Use a small fitted contact shadow if the source needs one. | Check whether its foot floats or its silhouette merges into the ground. Add a cut only where a real overlap or separately moving part calls for one. |
| Roof, kiosk or castle shell | Match roof, front and side to one silhouette and shared projected corners. Keep fixed surfaces painted together when the roof does not change visibility. Give an awning or eave its own card when someone passes under it. | Check both travel directions, the eave overlap and door readability. A fixed view with camera panning uses the same projected faces throughout the pan. |
| Bushel, strawberry pot or raised bed | Use the same painted source for back and near lip. Place soil, fruit or the moving item between the appropriate parts. For a planted pot use the soil line as the stem base. A raised bed has a solid floor footprint and clear approach aisles. | At phone size, a fruit or tool should remain recognizable during contact and after settling. The near wall may cover its lower edge. Touch in the aisle must still move Roshan. |
| Bridge, stair or dock | Draw the continuous walk surface from shared projected corners. Use separate face and parapet pieces where they change occlusion. Keep a narrow physical near piece in front during the crossing. | Test both ends against real walkable floor and watch Roshan at entry, midpoint and exit. Check that tapping beyond an inaccessible edge cannot cross it. |
| Door, hinged lid or crank | Separate the fixed housing, moving part, exposed interior, and any near frame needed at contact. Use coherent authored views when turning reveals a new face. Keep the hinge axis and attachment point fixed. | Compare closed, halfway, open and settled. Catch a floating hinge, visible old panel, changed hit target, or an opening state with an unreachable route. |
| Tree, shrub or tall grass | Keep the roots and contact fixed. Separate the canopy, main bough or blade group only where the actor can pass behind it or wind needs an independent response. Place understory along plausible roots and terrain edges. | Watch trunks at the horizon and grass tips near the path. Reject repeated ground stickers, shearing at roots, bright repeated outlines and a foreground branch hiding the child’s next action. |
| Shore, fountain or moving water | Bind the shore and basin to a fixed outline. Stage submerged content behind the surface where it belongs and keep the bank, lip or splash in the right order. Animate local flow or ripples inside the water boundary. | The shore should stay still under camera pan. Check the water/land hit boundary and make sure moving highlights never make it look walkable. |
| Extending marker or short lift | Use a few authored courses only when changing height is visible in play. Give the base a fixed anchor and the cap its own registered face. Use a single painted silhouette for an object with one height and no meaningful interleaving. | Look for duplicate outlines and disappearing overlaps at the shortest and tallest poses. Compare with an authored key-state swap before keeping extra transparent layers. |

The original bridge bench has a fixed route and gives strong evidence for near-rail order. It leaves full route geometry for a live test. The bushel bench answers the single-cavity question. It needs a separate loaded-state design for a raised bed full of leaves or a bushel with several visible fruit. The marker tests fixed footing and changing height. A roof that reveals different faces around a rotating camera needs separate authored views and review.

## Draw and register the parts

1. **Lock the view and draw over the same base.** Draw the whole silhouette at the intended camera pitch and play scale. Mark top and bottom planes, projected corners, contact outline, actor size, and the narrowest safe approach. Store every piece relative to the same ground origin. Crop alpha margins for export and retain the crop offset. A camera pan moves the shared projection together. Only scenery assigned to a background parallax plane moves at a different rate.
2. **Inventory, isolate, or fill one gap.** Record approved source path, hash and acceptance scope. Isolate components from a common RGBA master and save the clean background plate separately. Across tiled scenery, extract a readable seam-spanning object once and heal the joined master before tiling. For a genuine art gap, commission one missing surface or view, with an approved Roshan appearance reference and a separate position-only guide for corners and sockets. Ask for clean alpha, a few broad painted material values, soft plum or warm-brown contours, and the same light direction as adjacent objects. Keep crop bounds, layer or mask master, exact prompts and settings, attempts, rejections, and export hashes. [Art sourcing rules](06_COMPREHENSIVE_DESIGN_LANGUAGE.md#14-art-sourcing-reuse-and-provenance), [Aseprite layers](https://www.aseprite.org/docs/layers/).
3. **Check ownership in the composite.** Adjacent painted faces use shared vertices or the same cut line. An extracted source pixel has one owner. Two soft complementary masks drawn with normal alpha blending can alter edge opacity where both sprites contribute. Check reassembly on light and dark grounds, across tile joins, and under the actual import filter and camera zoom. For a source-preserving cut, retain the source alpha once at each pixel or use a composition that reproduces it. Catch halos, holes, edge bleed, and duplicate outlines in the render.
4. **Publish an object card.** Record its use, source and export paths/hashes, intended viewport and projection, contact origin, visible floor or collision footprint, touch region, action and attachment sockets, draw-order relations by state, rest and moving parts, optional voice/feedback cue, and the evidence needed for each changed state. Include a single assembled view and an exploded view with all parts registered to the shared origin. Link this record from the task's [audit impact](AUDIT_DEVELOPMENT_CONTRACT.md).

## Stage the draw order and touch coordinates

A bushel with a fruit inside has the following local order, from back to front.

```text
ground and fitted shadow
    back wall and interior
        fruit at its settled socket
    near rim and front wall
```

A bridge adds a walkable deck, then its far rail, Roshan on the crossing, and its near rail. The same artwork should also read correctly with Roshan on either bank. A fixed local order applies only to the footprint and poses that require it. For a wide path alongside a prop, test a pass behind, through the opening if there is one, and in front. A global near-layer override can put a railing over Roshan even when she is in front of it. Use sort origins for variable order or an explicit local order constrained to the approach and crossing where it applies.

On the Godot 2D canvas, group pieces that always move and sort together under a grounded origin. Use the projected ground contact for Y sort when actors and props can trade order. Comparable children must share an effective `z_index`. Nested Y sort and inherited `z_index` change the ordering, so inspect the actual scene tree and the rendered crossing. Reserve explicit canvas depths for pieces that require fixed order. Use `CanvasLayer` for genuine screen-space controls. Convert touch positions through the same camera and local transforms used for the art, sockets and footprints. Draw order and input ownership are separate, so inspect the visible candidate selected by a tap when bounds overlap. [Godot CanvasItem ordering](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html#class-canvasitem-property-y-sort-enabled), [Godot canvas layers](https://docs.godotengine.org/en/stable/tutorials/2d/canvas_layers.html).

For a seam-sensitive assembly, freeze the camera, show the projected floor and sockets in a diagnostic capture, and change one part at a time. For a live crossing, sweep both ways past the depth switch, compare the frame just before and after, and check faces, hands, fruit, and any required touch target. Check a pair of overlapping neighboring props as well as the object by itself.

## Author the action and its resting states

Write the visible sequence before implementing it. A usable object has an identifiable resting silhouette, a reachable approach, a contact moment, and a result the child can recognize. Animate the part that changes. Hold the base steady while a door swings, a berry settles behind a lip, or a rooted stem bends. Use coherent keyed states where the action exposes a new surface or a change in contact. Check the action in real time and frame by frame at entry, contact, settle and any loop seam. Apply the existing [interaction rules](06_COMPREHENSIVE_DESIGN_LANGUAGE.md#7-interactions-change-the-world-truthfully) and [animation production protocol](animation/ANIMATION_PRODUCTION_PROTOCOL.md) where the object work includes authored animation.

| Moment | What the child sees and what the route does |
| --- | --- |
| Available | The object reads at phone scale through silhouette and value. A required action has the existing visual and spoken guidance. For required targets, DL-UI-03 calls for a 110×110 base-canvas pixel target or an equally generous projected region, with room for neighboring actions. |
| Requested | A single deliberate tap gives the response under DL-AGE-07, then guides Roshan to the reachable contact pose. The pointer stays on the live target. One touch owns the request. |
| Contact | Show the relevant hand, tool or item meeting its socket. Keep the hinge, floor, rim or other support fixed. If the job grants progress, commit only after the visible action satisfies its existing contract. |
| Settled | The changed object reads on its own. A new visible state and any progress flag agree. Repeat taps cannot collect a second copy, restart a completed step, or charge twice. |
| Interrupted or revisited | Release, focus loss, Back, or a route change cancels the pending action as appropriate. A saved completed state restores consistently. Present a clear exit and a repeatable way back for any newly enterable destination. |

For a bridge, compare idle and in-transit actions. Test both banks from the visible route, blocked input toward the water, and a touch on a nearby fixture. For a closed door, check that its state and decoration communicate the same meaning. An open door's tap, approach, destination, return and re-entry belong in one replay. The current Pearl Castle code already resolves `blocked`, `open`, `bonus`, and `plot` as shared reachability and cue states. Reuse that vocabulary for Pearl Castle door work. [Castle door state model](../scripts/castle_door_language.gd), [promenade doorstep handoff](../scripts/arena/sky_lagoon_promenade.gd).

### Worked example for Enchanted Forest

A later optional farm-to-castle sequence could use the approved raised bed, an existing bushel, Evie's authored help, and a compatible castle display fixture. In the grove, the near bed edge owns the soil line, strawberry crowns stay rooted, and the ripe berries own distinct pickup positions with a clear aisle for Roshan. On one deliberate tap Roshan approaches and picks at the live berry socket. The fruit leaves the plant at contact and settles visibly in a bushel slot behind its lip. The settled state remains readable on the way out. For any commissioned castle payoff, show the result on the destination fixture when Roshan returns and restore it on revisits. Keep the Day One castle entrance independently reachable before the harvest. This example describes a future design. The earlier bench measured one fruit in one bushel.

For a Forest review, label background, midground, mid-foreground and
foreground roles, then record the interaction owner and region separately.
Compare before/after passes with the current Grove terrain and the same
camera, including both crossings of depth boundaries, strawberry-tap cadence,
walkable paths, wet/dry habitat boundaries and dense foliage performance.

## Review and record the evidence

Capture the actual build under Godot 4.7.2-stable with Mobile rendering, at the 1280×720 base and the supported target-device aspects. Preserve the object ID, role, revision, viewport, renderer, camera position, action and state for each capture or replay. A fixture placed directly at a pose can isolate pixels. Entry, gameplay, and progress claims require a replay through real inputs and the normal route. Use the existing `DL-QA-11` fresh-runtime process when making an authoritative visual-runtime claim.

| Review | Compare | A failure the comparison should expose |
| --- | --- | --- |
| Source ownership | Intact source and reassembled rest view when exact reassembly is promised. Also check on a light and dark ground and with one piece disabled. | A doubled painted copy, missing pixels, alpha halo, visible old panel, or a seam at camera extremes. |
| Contact and depth | Assembled and exploded, before/after the depth switch in each reachable direction, plus one wrong-order control for any order-dependent action. Keep pose and camera equal for the control. | A whole-object depth pop, a near rim obscuring the reward, a face hidden by a rail, or a tree canopy sliding off its trunk. |
| Input and state | Tap the visible object, the adjacent floor and any overlap with a second target. Exercise drag/hold where supported, cancellation, rapid repeat, and passive input. Follow the real entry, exit and re-entry route when applicable. | An invisible hit region, an adjacent tap stolen by the prop, remote completion, auto-collection, duplicate progress or an abandoned action that still fires. |
| Restoration | Compare old/default save, pre-contact interruption and completed state on a fresh visit or restart. Exercise the route with optional work untouched. | A formerly visited door that can never be used again, an invisible reward, or a state flag out of sync with the picture. |
| Art and readability | Review full scene and phone scale through normal-speed motion. Include focal separation, shape, palette, foreground, readable silhouettes, readable child action and kind feedback. | A still frame that looks convincing while the action disappears behind a near layer, or painted texture that obscures touch cues. |
| Mobile budget | Compare a representative dense route against its baseline with the same renderer, device, viewport, tier and route. Record visible pieces, texture sizes, overlapping coverage, draw calls and frame pacing before/after. Include the first-use cost for newly loaded or built objects when relevant. | Several overlapping translucent planes or particles stalling the full scene despite an isolated prop looking inexpensive. |

Start the performance comparison with the smallest viable set of cards. Trim empty texture bounds, combine pieces that always share draw order and motion, cull offscreen groups, and reserve overlapping alpha and effects for visible jobs. Keep a cut that preserves an actor crossing, interaction, or clear settle. Use the approved Speedy-tier thresholds in `DL-PERF-02` for normal play on the target device, including P95 ≤33.3 ms, P99 ≤50 ms, no normal-path hitch over 100 ms, and the 30-minute memory/thermal check. Report texture dimensions and import mode under `DL-PERF-04`. Record actual visual and touch outcomes along with machine results. [Godot GPU performance and overdraw](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html), [project performance and QA rules](06_COMPREHENSIVE_DESIGN_LANGUAGE.md).

Keep the disposition of each evidence lane in the impact record. Record desktop checks, author/human visual review, device, observed child and owner outcomes at their actual scope. Match related findings to the failed part, such as [true 2D](../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-2d-002), [card ownership](../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-002), [visual-runtime coverage](../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-006), [overdraw](../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-008), or [route reachability](../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-001). Existing acceptance rules and findings retain their current scope.

## Five review rounds

| Round | Review performed | Resulting correction |
| --- | --- | --- |
| 1. Source and fixture | Read the studio and developer explanations, inspected the assembled/exploded renders, and reran the stored-image verifier at both recorded widths. The rail and rim controls isolate a specific order change. | Scoped the source claims to the farm example and the measurements to their actual pixels and poses. Separated the height-stack experiment from the studio's method. |
| 2. Object families | Walked the first draft through a static pot, roof, container, bridge, moving lid, rooted plant, shore and lift. The three fixtures left the simpler and hinged cases underspecified. | Added a minimum assembly for each family and a concrete failure to look for. |
| 3. Registration and order | Reviewed a translucent cut edge, an object across a tile join, and a traveler both behind and in front of the same prop. Pixel ownership and a pass on both sides catch duplicate alpha and global near-depth overrides. | Added one-owner compositing, crop offsets, projected contact and camera/input transforms, plus local draw-order tests and neighboring objects. |
| 4. Action and state | Checked the front-door regression, a second tap on a harvested berry, and abandoning a requested pickup before contact. The previous draft covered the still and draw order while leaving these outcomes implicit. | Added visible contact, immediate response, one-touch ownership, commit/interrupt/restore checks, and an optional Sky Lagoon progression example. |
| 5. Evidence and cost | Applied the draft to a perfect empty-bushel composite that hides a berry, a visually convincing bridge with a failed floor join, and an inexpensive isolated tree repeated across a dense route. A single favorable still or fixture count misses all three. | Added matched controls, real-route replay, device-scale and dense-route measurements, and evidence status under the existing master audit. |

[Audit impact and evidence references](audit_impacts/object-development-guide-20261111.json).
