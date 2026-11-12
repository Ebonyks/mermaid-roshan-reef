# Sky Lagoon layering and style handoff

Sky Lagoon should read as a walkable storybook set. The route is the quiet ground plane, each toy occupies a real patch of lawn, Roshan and wildlife have distinct points of contact, and the scenery frames the next action. Use Cult of the Lamb as a reference for how a scene is assembled and how it leads the eye. Use the approved Sky Lagoon v5 painting, existing silhouettes, and high-key Reef palette for the visual identity.

## What the reference build does

The local Windows Unity build identifies Massive Monster and Unity `2021.3.16f1`. ILSpyCmd `9.1.0.7988` produced 2,718 C# files from `Cult Of The Lamb_Data/Managed/Assembly-CSharp.dll`, SHA-256 `eecbae2542f2b3ce6d063a71678d9693864882557d4454cdd316486a9a112685`. The companion `Assembly-CSharp-firstpass.dll` produced 391 C# files and has SHA-256 `90383325ef46e2a2c78a15e857643721e19016ab053cfd193113ccf1a1f2cae4`. The study also read the serialized project settings in `globalgamemanagers` with UnityPy `1.23.0`. That file’s SHA-256 is `c63606b95b88c929cd475b2ea6f08472063beaf16e2c75deb769039d5df372fb`. The GitHub handoff contains Reef implementation and independent observations.

| Evidence | Observation | Sky Lagoon application |
| --- | --- | --- |
| Serialized `TagManager` | Depth FX, island and ground passes precede terrain, decoration, paths and tiles. Shadows and ground UI have named layers before the default subject layer. Lighting, VFX, foreground and screen UI follow. Alternate level bands repeat the separation. | Give terrain, supported objects, effects and UI named jobs. Reserve an uninterrupted ground band and keep transparent overlays sparse. |
| `GenerateRoom`, `IslandPiece`, `SetSortingLayer` | Room fill, island and encounter ground are configured independently. The same source shows deliberate order overrides for particular states. | Hold landmarks and structural supports in mural space. Give movable or actionable parts their own transforms and explicit order. |
| `ChildPlacementHelper`, `EnemyDropper`, `UIMenuBase` | Placement has an explicit depth axis. The dropper shadow is driven separately from the actor. Menus maintain a separate canvas order. | Use the stable floor contact for grounded depth and shadow. Give supported action poses and cues explicit order. Keep HUD in its screen-space canvas. |
| Serialized `GraphicsSettings` | The project stores orthographic transparency sorting (mode `2`) and a separate axis value of `(0, -1, 0)`. The bootstrap scene camera is orthographic. Gameplay camera overrides and individual renderer pivots remain outside this sample. | Use a Reef-specific Canvas contact-Y rule. Test actual overlapping pixels per prop and direction. |
| Settlement and Anchordeep examples | Tall architecture and dense plant masses sit at the edges or back. Objects on the play plane have compact silhouettes and visible bases. The exposed ground gives the player and the active event room to read. | Carry the same hierarchy through the runway, playground and castle. Concentrate contrast and motion around the active object. Keep the route open. |

[Massive Monster lead programmer interview and source images](https://unity.com/blog/games/recipe-behind-smash-hit-cult-of-the-lamb) · [Unity sprite sorting](https://docs.unity3d.com/2022.3/Documentation/Manual/sprites-sort.html) · [ILSpy](https://github.com/icsharpcode/ILSpy)

## Build guidelines

1. **Compose the scene around the route.** Hold the horizon and camera scale steady as Roshan walks. Work in 6144×2048 master coordinates on the existing 6×2 tile grid. Establish the runway, playground and castle at wide view first. At phone size, preserve a clear route through each screen and a distinct resting silhouette for each of the slide, swing and seesaw. Put large landmark masses back from the walking line and leave gaps between silhouettes.
2. **Give each visual a physical job.** Keep distant paint and local floor surfaces registered at factor 1.0. Use the existing rear atmosphere at 0.82 and sparse near effects at 1.06. The art file owns a physical object once. If a painted plant needs to move or cast an occlusion, isolate that exact feature and heal its source area before reinsertion. Inspect the border at rest and during camera travel.
3. **Build from the contact point.** Mark a foot, pedestal, pivot or support edge before aligning the image. In the playground, a toy and a walker share the same ground-depth band. Use the resting floor position through toy rotation, swing motion and actor hops. The character’s face and the object a child can tap must remain recognizable through any overlap.
4. **Keep silhouette and material contrast deliberate.** Use the approved lagoon's indigo, plum and warm-brown contours and broad painted value bands. Let the floor carry low-contrast texture. Put sharper shapes and contrast at touchable edges, faces and hands. Group vegetation into broad masses and leave clear gaps around props and destination markers. Use the existing palette in day and night and keep contact readable in both.
5. **Keep motion attached to the thing that moves.** Pin the roots of ambient art and the bolts of equipment. The swing needs a supported fore-and-aft performance, with the ropes, seat and rider moving together and changing visible surfaces. The slide needs contact with the bed and an exit that returns to ground. The seesaw needs weight at its pivot and seated contact through the cycle. Preserve the rest pose, the end of the action and the handback to walking. The existing authored poses are the first integration context. Approve new motion through the separate production and review gates.
6. **Put cues above the world and on the object.** Keep the existing attached tip and one active cue. Inspect it with the normal HUD at phone scale. Keep the actor, prop, cue and touch target in agreement across approach, play, cancellation and return. Keep near foliage and night effects out of the face and pointer during those beats.

## First implementation

The promenade now sorts the slide, swing, seesaw, Roshan and pooled wildlife by ground contact in a shared Canvas band. Contact shadows use a lower band. Roshan's supported ride pose and settle draw above grounded subjects until control returns. Focus cues draw above the ride band. Scenery and parallax keep their existing holders. The change uses the existing artwork, approved floor and route, touch targets, authored sockets and save behavior.

The existing walking route passes in front of the playground fixtures. The focused probe samples both sides of the live slide contact to exercise the ordering rule. New walk-behind paths or stronger fixture occlusion require a painted-ground and face-visibility review for each prop. Any future front rail needs a source-owned split, a matching rest composite and separate evidence that the face and touch target stay legible.

For the next art pass, work in this order.

1. Use the playground overview to check ground contact at the slide ladder and chute exit, the four swing feet, and the seesaw pivot. The slide is beside the left shrub edge and the seesaw sits against the right planting mass. Use a quieter value under those supports and enough contrast to read each complete silhouette.
2. Check the day and night views together. Match the independent cloud's edge softness and day-to-night value response to the painted cloud family so its motion reads as atmosphere. Retain an open band behind Roshan and each cue.
3. Build and review per-fixture front and rear ownership at the same master scale. Use the existing slide rail and swing frame as the first candidates. Capture the assembled rest artwork and the entry, overlap and exit in each direction before widening the walking route.

| Review | Pass condition |
| --- | --- |
| Runway to castle and return | Walk in both directions. Show no tile seam, doubled object or parallax drift at a grounded landmark. Confirm normal exits and re-entry. |
| Playground overview and each action | Inspect slide, swing and seesaw at rest, focus, first contact, mid-action, settle and exit. Check the contact shadow below grounded art, the rider at the authored support and the pointer attached to the live prop. |
| Wildlife, day and night | Patrol and startle stay on their approved floor envelopes. The lifted sprite stays registered to its floor shadow and retains ground order. Confirm that wildlife does not obscure Roshan's face during a touch-dependent action. |
| Mobile device and child use | Review with HUD on at phone size and on the Lenovo Tab M11. Verify stable 30 fps on Speedy, useful touch targets and a child-readable route. Obtain owner review of the in-context result. |

## Independent cross-review request

Compare the published topic against its base, `f070a61e0ffdd84c1cca17ea2c368aa0382d981f`, and against the current Dev head before integration. Inspect the effective depth order with Roshan in front of and behind the same contact. Repeat a ride, cancel a ride, and confirm the ground order and shadow return on settle and re-entry.

Cross-check the Reed Cove puzzle and biome or ecosystem candidates at their exact available revisions. Confirm that the visible support and occupied floor agree, near scenery leaves Roshan and the selected touch cue readable, and overlap changes preserve each area's existing interaction path. The separate Grove demo was based on the same Dev revision and had no edits to this topic's runtime, probe or visual-audit spec at inspection. Include its visible contact and occlusion in the combined review. Record each candidate revision and the renderer used.

[Impact and validation record](../../../design/audit_impacts/sky-lagoon-layering-20261111.json) · [Current design language](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md) · [Original painted feature survey](../../../assets_src/sky_lagoon/original_art_motion_20261105/SOURCE_LAYER_SURVEY.md)
