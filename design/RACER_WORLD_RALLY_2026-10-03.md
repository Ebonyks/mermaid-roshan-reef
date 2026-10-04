# Racer: connected Castle and Sky Lagoon rally

Status: `CANDIDATE / EXTERNAL_ACCEPTANCE_PENDING`. Baseline is
`4f7181450da4d12497592a963c64422a7bae981a`. The owner selected the fuller
developed racing game after comparing it with the older contained Opera race,
commissioned rebuilt visuals under the master audit, and directed the track
through the game's actual environments.

The previous flat [Canvas port](RACER_EXISTING_ENGINE_2D_PORT_2026-10-03.md)
is superseded as a visual proposal. Its source and machine evidence remain
historical evidence. This rebuild uses the same analytic driving engine and
chase perspective on Canvas. The owner's Racer-only permission to use the
former spatial engine does not require adding spatial resources.

The route follows Movie Lounge → Family Gallery → Main Hall → Mermaid Pool →
Main Hall → Castle front bridge → Sky Lagoon → Castle bridge → Main Hall →
Family Gallery → Movie Lounge. Movie Lounge really belongs to Family Gallery;
Pool connects to Main Hall. Castle and Lagoon use the existing front gate and
stone bridge. The reverse variant follows the same links backwards. Separate
paintings do not create new story portals. Outdoor windows are one path, and
the return bridge stages the existing four-tower Castle and opens its real
front-door footprint.

The simulation owns a level driving aisle, banked turns, eight racers, three
distinct vehicles, eight paints, drift and turbo, drafting, bumps, walls,
items, pearls, hazards, ramps, reverse laps, positive finish and recoverable
rewards. Named hazards are confined to Pool/Lagoon. The Lagoon shortcut now
drives a continuous chord inside that one location; it does not teleport
across Castle rooms. Custom configured courses keep their explicit height
contract. The shared KartDriving source remains unchanged.

Stationary boost-strip drawings retain their source-course coordinates on
reverse laps, matching the original gameplay contacts. Rival portrait lower
edges sit behind each vehicle's authored seat back rather than above it.
Both export presets explicitly include the pose/contact JSON. A separate
isolated Windows resource-pack check verifies packaged metadata and sprites;
it does not establish APK or Android-device acceptance.

The presenter owns road projection, depth ordering, bounded room-tile reuse,
authored seated driving keys, Pool crossing and Castle bridge balustrades,
measured rear-tire pivots, separate jump shadows, physical bumper paint and picture
controls. One visible steering band works with one finger; the child can
release it and tap Turbo. A second finger is optional. Centered deliberate
holding counts as participation, while the demonstration and unattended
auto-cruise award nothing. Pause/focus/teardown clear owned input and restore
the prior world touch state. Emulated mouse events do not steal touch indices.

The [art inventory](../assets_src/racer_chase_20261003/inventory.json),
[native generation prompts](../assets_src/racer_chase_20261003/prompts.json),
[pose/contact contract](../assets_src/racer_chase_20261003/animation.json) and
[impact record](audit_impacts/racer-chase-world-route-20261003.json) preserve
references, named gaps, native hashes, runtime crops and acceptance boundaries.
The built-in image generation tool supplied gameplay cutouts only. Protected
book, voice and friend originals are unchanged. The halo-bearing empty sheets
are rejected and excluded from runtime. Keys are authored held steering and
acceleration poses, not a claimed smooth animation loop or cinematic delivery.

Implementation and machine verification are separate from acceptance.
Evidence is under `audit/racer_chase_20261003/`. Earlier failed captures,
touch ownership failures and runtime errors are preserved with their reasons.
Current exact Godot 4.7.2 checks and captures must refer to the final source;
older green port gates cannot validate this rebuild.
Two failed complete console runs remain archived. The
[engine invocation comparison](../audit/racer_chase_20261003/engine_invocation_comparison.json)
records unchanged controls completing through the same approved 4.7.2 archive's
resolver-selected core executable. The launcher is a working hypothesis;
this comparison does not establish a cause or waive the complete gate.
The [current gameplay direction review](../audit/racer_chase_20261003/current_direction_review.json)
binds the fuller-engine recommendation to these rebuilt visuals and separates
simulated agency, discoverability, contact and progress safety from child review.

The [native route gallery](../audit/racer_chase_20261003/index.html),
[capture manifest](../audit/racer_chase_20261003/manifest.json) and
[verification lanes](../audit/racer_chase_20261003/verification.json) bind
the current review states. These are diagnostic captures; the authoritative
`DL-QA-11` fresh-runtime/challenge adapter remains a `COVERAGE_GAP`.
[CHG-033](../audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md#racer-connected-chase-rally-chg-033)
owns the source change and manual rollback review. Owner review also needs to
resolve the broad head turns and kart/motorcycle rear lamp design.

Outstanding: Lenovo Tab M11 sustained 30 fps, real-device touch/audio, child
comprehension/enjoyment, intermediate steering acting and owner visual/anatomy
acceptance. The reused Hall source retains its recorded native-resolution
shortfall; a normalized production master does not prove native 2K acceptance.
The existing main-game kart entry/callback remains the shipping entry for this
candidate. The older contained Opera implementation and its career/save
lifecycle are unchanged; replacing that adapter is separate integration work.
The [terminal actor review](../audit/racer_chase_20261003/terminal_actor_review.json)
verifies the routed final-action matrix, identifies both actual callers, and
keeps visible driving, conserved kart, finish/park and settled return evidence
separate. The finish pictures stage lap distance and participation; they do
not prove a natural Movie Lounge career playthrough or its final actor action.
No dev integration, release, finding closure or whole-game master satisfaction
is claimed. Global strict-medium satisfaction remains `UNSATISFIED`.
