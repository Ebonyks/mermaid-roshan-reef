# Pearl Castle dust-bunny spawn guide — 2026-07-29

## Outcome

The Main Hall now spawns exactly three distinct dust bunnies as unshaded Sprite3D cards at real scene depth:

1. one sleeping static bunny;
2. one static bunny hiding beneath a shell;
3. one bunny running a deterministic patrol.

Roshan does not tap a UI hotspot to remove them. When her live in-world foot position touches a bunny's contact area once, that bunny bursts into twelve star Sprite3D cards, scales/fades out, is removed from the interaction registry, and cannot trigger a second time during that castle visit. There is no fail state, timer, text dependency, score requirement, or lost progress.

## Resolution correction

The Main Hall's `3344×941` logical art space and `1672×941` camera view are placement/navigation coordinates only. They are not background pixel dimensions and do not establish resolution compliance.

The current two screen plates are provisional:

| Screen | Current master | Dimensions | SHA-256 | Status |
| --- | --- | ---: | --- | --- |
| A | `assets/flats/castle/main_hall_2screen/main_hall_screen_a_room_led_master.png` | 2048×1153 | `ae84f4f79a8183312b5ba26b6999f26b69c8a538424b5383a7d6623cc2f275e9` | below native 2048×2048 per-screen coverage |
| B | `assets/flats/castle/main_hall_2screen/main_hall_screen_b_room_led_master.png` | 2048×1153 | `c333bdbd3243b2cfcd61e9475e7e5449d7165d03ff8413f860535d5ccb811454` | below native 2048×2048 per-screen coverage |

The background-resolution remediation remains separate and pending. It must preserve the approved aspect ratio, composition, camera, lane, sockets, silhouettes, and depth boundaries while supplying at least 2048×2048 native coverage for each playable screen. The normalized spawn layout below remains valid when compliant background masters replace the provisional plates.

## Spawn table

Coordinates are in Main Hall logical art space. `center` positions the visual card; `contact foot` is the floor-space point used for collision. All cards have depth testing enabled and use the castle perspective Camera3D.

| ID | Character direction | Asset | Center | Contact foot | Contact ellipse radius | z | Scale | Motion |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `sleepy_bunny` | sleeping | `dust_bunny_sleepy.png` | `(720,790)` | `(720,864)` | `(132,92)` | `2.65` | `0.34` | static |
| `shell_bunny` | hiding beneath shell | `dust_bunny_shell_hide.png` | `(1140,790)` | `(1140,864)` | `(132,92)` | `3.05` | `0.32` | static |
| `runner_bunny` | running | `dust_bunny_hop.png` | `(1820,790)` at start | live center + `(0,74)` | `(142,98)` | `2.85` | `0.32` | triangle patrol from x `1820` to `2580` at `220` logical pixels/second, with a 14-pixel hop |

Normalized against the full 3344×941 logical hall, the centers are approximately `(0.2153,0.8395)`, `(0.3409,0.8395)`, and `(0.5443,0.8395)` at runner start. The initial Roshan foot point `(380,835)` does not overlap any spawn.

## Approved asset inventory

No new artwork was generated. These three existing protected runtime derivatives are reused without pixel modification:

| Asset | Dimensions | SHA-256 |
| --- | ---: | --- |
| `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_sleepy.png` | 512×512 RGBA | `02c37b1d84a78da7c750308cbf708b98636808c855e9811bf82dcdccfc26ec90` |
| `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_shell_hide.png` | 512×512 RGBA | `b3fbe139d79ba9567213afeb70a25bd986d90230052be7a9b320802a65613293` |
| `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_hop.png` | 512×512 RGBA | `677cda8c5de1d3aaf1d8960b089d48fab27106429bc221b4c26c14775b382752` |
| `assets/mg/star.png` (transient burst reuse) | 1024×1008 RGBA | `3cc5d5cbc5d6e0df0540cdc00ef557b0c7ed6e566331035c4e75d5d971ef3b98` |

The old dust-bunny-family door marker was replaced by the existing star marker, so the navigable hall depicts exactly three dust bunnies rather than three targets plus a misleading fourth family image.

## Runtime node and interaction contract

Steady-state additions to `CastleItemVisualLayer`:

| Node type | Count | Shaded | Billboard | Depth test | Input role |
| --- | ---: | --- | --- | --- | --- |
| Sprite3D dust-bunny cards | 3 | no | disabled | enabled | analytic player-contact target |
| Button/Control bunny hotspots | 0 | n/a | n/a | n/a | none |

Each removal creates twelve unshaded Sprite3D star motes in `CastleItemEffectLayer`; they fade and free themselves after 0.72 seconds. The bunny card itself expands, rotates, fades, and frees itself after 0.24 seconds.

Touch movement uses the castle camera's projected stage mapping. During a walk tween, Roshan's `current_stage_foot` is updated continuously. Collision is evaluated in logical hall floor space with an ellipse test, so camera travel and perspective projection cannot separate the touch destination from the world object. Bunnies intentionally have no invisible Button node. The probe projects a ray through each card's visible center, verifies that it intersects that Sprite3D position, reverses the screen point into logical hall space, and confirms the resulting destination lies inside the bunny's contact ellipse.

Main-owned visit state:

- `castle_dust_bunnies_cleared`: dictionary keyed by the three spawn IDs; written before effects begin, preventing duplicate activation.
- `castle_dust_bunny_runner_time`: deterministic patrol clock.

Changing castle rooms rebuilds the Main Hall without respawning cleared bunnies. Closing the castle clears visit-scoped state, so a later castle visit can replay the child-safe cleaning interaction.

## Acceptance probes

`scripts/probe_castle_pearl_art.gd` verifies:

- exactly three distinct, unshaded, depth-tested Sprite3D bunny cards and zero bunny hotspots;
- correct semantic roles and spawn-guide IDs;
- camera-ray intersection and reverse screen-to-hall mapping land inside every contact ellipse;
- two cards remain fixed while the third changes position;
- every bunny clears after one contact, produces twelve effects, and records its cleared ID;
- a second explosion request has no effect;
- cleared bunnies remain absent after leaving and returning to the Main Hall;
- no spawn intersects either fixed elevator region;
- Sprite3D-only world art, depth layering, camera travel, and mobile visible-card budget remain intact.

`scripts/probe_crown.gd` verifies the Main Hall inventory as seven ordinary touch props plus three dust bunnies (ten item Sprite3D cards total) and only seven UI hotspots. It also blocks on an honest castle background status: all current 2048×1152/1153 plates are marked provisional until native 2048×2048-per-screen coverage exists.
