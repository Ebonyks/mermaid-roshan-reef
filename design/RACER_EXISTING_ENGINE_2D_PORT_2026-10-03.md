# Existing Racer engine: Canvas conversion candidate

The owner prioritizes conversion of the already developed `KartGame`/`KartDriving` engine over other racing implementations. Baseline: `30d82725661044de63b682f5b13ba8f19101892b`, isolated branch `codex/racer-existing-engine-2d-20261003`.

## Implementation

`KartGame` is now `Node2D`. `kart_canvas_2d.gd` draws the course, vehicles, contacts, selection, speed cues and result on the Canvas. Original planar route coordinates, scalar road elevation, arclength, signed curvature, banked contact distances and landing timers remain measured simulation data. There are no spatial nodes, cameras, lights, model loads or spatial shaders in the engine subtree.

All 17 features in the [conversion contract](../audit/job_game_refinement_20261003/racer/ENGINE_CONVERSION_CONTRACT.json) are retained: auto-cruise/steering, brake, turbo, drift, drafting, eight-racer pack AI, mass collisions, variable width/banked walls, ramps/landing boosts, four item types, strips, pearls, hazards, shortcut, reverse/theme routes, three rides/eight paints, and lifecycle/save/finish handling. Exact retained methods and the unchanged shared `KartDriving` blob are recorded in [scalar parity](../audit/job_game_refinement_20261003/racer/SCALAR_PARITY.json).

Race rewards still persist at completion, before the podium delay. Only the medal/sticker painting is delayed 0.75 seconds to let the crossing remain visible; the result begins at 0.65 seconds. Other activities retain their existing immediate reward display. The complete pictured ride card is now its native Button target, so a child can tap the artwork.

The existing main-game entry and callback remain intact. `OperaRacerSurface` remains its separately scoped contained adapter; this change does not falsely substitute that partial implementation for the full developed engine or claim that its separate integration is complete.

## Reused art and gaps

Ten kart/motorcycle views are deterministic derivatives of the existing 2026-07-22 source sheet. Crops, source/derivative hashes, dimensions and matte/padding changes are in [provenance](../assets_src/kart_canvas_2d_20261003/provenance.json). Originals and protected book, voice and friend sources are unchanged. No new generation was used.

Truck directional art has no accepted source; the flat Canvas toy silhouette is an explicit development candidate, not accepted final art. The existing raster circuit is 1672×941 and cannot meet native 2K per screen. This candidate uses code-native Canvas course geometry; it makes no upscale/native-resolution claim for that raster. Environment polish, occupied cockpit/driver staging, all directional/view transitions and truck views require visual/owner review.

## Evidence and acceptance

[Port verification](../audit/job_game_refinement_20261003/racer/PORT_VERIFICATION.json) is the machine/capture receipt. The baseline racing probe, original source and original probe are preserved alongside it. Only the old 3D orientation/FOV assertions became equivalent actual 2D orientation/zoom assertions; racing-line, drift, save, full-pack, zero-input and quit gates are retained. The added feature probe checks contact and item/ramp/shortcut/mass behavior without changing the trusted suite's floors.

The first capture attempt was invalid because the startup menu covered the race; its logs are retained as a rejected fixture attempt. Corrected captures use the normal race entry after menu dismissal, isolated user data, actual Vulkan Forward Mobile at 1280×720 and 1280×800. The HUD stage shares the Canvas fit/centering transform; explicit bottom offsets keep the hint and turbo meter in their intended positions. Captures include native ScreenTouch picture selection at both aspect ratios, paint selection, ramp apex, finish approach, crossing and result settle. Screenshots are agent review evidence, not device or child acceptance.

The GAME2D production file inventory shrinks 52→51; models stay zero, probe files remain 61, scene/configuration categories remain one each. `MA-2D-002` stays `IN_PROGRESS`; strict game-wide satisfaction remains `UNSATISFIED`. The historical master snapshot is preserved.

Machine verification passed on exact Godot 4.7.2: final parser/inference, six-script analyzer, deterministic source-art reproduction, focused feature/contact checks, all 82 trusted probes, document authority and exact development coverage. `scripts/ci.sh` exited 0. Its existing visual advisory remains UNSATISFIED; no finding or acceptance closure follows from these green checks.

Implementation, machine checks, agent visual review and external acceptance are separate. No device, child, owner, final art, release, dev integration or master promotion is claimed by this candidate.
