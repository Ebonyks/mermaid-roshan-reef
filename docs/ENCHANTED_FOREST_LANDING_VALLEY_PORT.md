# Landing Valley production port

The reviewed standalone Landing Valley has ten layered firs, granite and understory on dry ground, and a route into Reed Cove. This topic ports its passive scenery assembly. The production Sky Lagoon route still enters the predecessor promenade. The dormant host adds the reviewed terrain, crossing, and Cove. ReefMain exposes an explicit entry for a supplied actor. The normal launch paths still enter the promenade and Castle.

## Mounting the component

A future Forest route can instantiate [the Canvas component](../scripts/arena/enchanted_forest_landing_valley.gd), call build with its Y-sorted ground and a placement predicate, and tick it with the actor’s ground-local contact position. The predicate needs the reviewed Valley terrain footprint, wet/dry rules, and trail clearance in that same space. The route owns the actor, camera, terrain, and input. Call teardown when leaving the route. The component frees only its scenery.

## Dormant route host

The [Canvas host](../scripts/arena/enchanted_forest_route.gd) owns the floor, scenery, camera, route travel, Cove interactions, and two-shell bridge. It accepts a caller-owned actor and an optional wildlife hit callback. It emits world-space objective targets and completed progress events. On teardown it detaches the actor and frees the route. If the route still owns the viewport, it restores the previous camera.

The [ReefMain session adapter](../scripts/arena/enchanted_forest_route_session.gd) uses the current world-input gate and SaveState writer. It stores the bridge bitmask and Cove charm under the additive `enchanted_forest_route` key and preserves unknown fields. It supplies `forest_bridge_shells` and `forest_cove_valve` events with pointer positions. The explicit entry uses the existing touch dispatcher, overlay gate, focus and app lifecycle. It restores the prior promenade position on exit. Normal activation and production cue registration remain open.

The Grove source is the sealed standalone snapshot. The host advances the bridge clock. Cove decompresses the existing shell texture before reading the CPU touch silhouette on Mobile. The Valley component is byte-identical to the independently reviewed staged code. The [host impact record](../design/audit_impacts/enchanted-forest-route-host-20261113.json) covers the additional work.

## Production seams still open

| Seam | Required production connection and evidence |
| --- | --- |
| Entry and return | The explicit Forest entry accepts a caller-supplied actor from the promenade outside active Day One. The fixture verifies return to the prior promenade position and teardown at the existing Castle entry. The route has no player-facing entry or Forest Castle target. |
| Touch | Deliver production touch and drag events through the existing input gates and one world-to-screen transform. Cancel pending travel and actions on overlay, focus loss, and route exit. Test the visible Cove waymark, valve, frog and shell at 1280×720 and 1600×720. |
| Guidance | Use production voice and pointer ownership. The author’s retained demo record identifies the exact Kokoro bridge cue. Production needs its license and objective-audio record, playback review and a matching cue for the Cove valve, or the documented diegetic exception in DL-SND-13. Check that Cove takes over on arrival and bridge guidance returns on deliberate departure. |
| Save and teardown | Keep the production reef_save.json recovery path. The host provides scoped Cove and bridge defaults. Production still needs to verify the route lifecycle and explicitly map any shared objectives. The demo’s separate CFG is outside production save authority. Verify old and fresh saves, interrupted contact, completed progress, restart and re-entry. Release route camera, audio, gesture ownership and scene nodes on exit. |
| Character | The reviewed standalone uses atlas playback. New Forest gameplay needs the exact Rigby2D source, export and acting evidence in DL-MED-02 and DL-MOT-17. The scenery topic introduces no character playback. |

## Source and verification

The reviewed standalone manifest has SHA-256 6e36c6fa142a933a25764e1503191ebce3e2dccda2b58b5cf8bd92e669568c2f. It binds 310 files, including the corrected habitat script 7dce2da090fd6157cbe9c830f83569431fb7ae0417457c257a7e74e1069210bf. Independent desktop Mobile tests verified the full fish silhouettes stayed in the water and the standalone touch route passed at both widths. The active Ecosystems patch remains separate.

This component preserves the six cutouts and foliage shader from that snapshot. It uses the existing project contact shadow. The only assembly changes are caller-owned placement and cleanup. The [source digest list](../assets_src/enchanted_forest/landing_valley_20261113/reviewed-source-sha256.txt), [art provenance](../assets_src/enchanted_forest/landing_valley_20261113/landing-art-provenance.json), [asset license ledger](../ASSET_LICENSES.md), and [impact record](../design/audit_impacts/landing-valley-canvas-component-20261113.json) bind the retained sources and validation scope.

Independent production route, occlusion and touch review, exact candidate CI, physical Android, child and owner review remain open.
