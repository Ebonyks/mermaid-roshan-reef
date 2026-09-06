# Stage pathfinding inventory

This directory is the machine-readable coverage ledger for the stage-pathfinding
work order. The authoritative inventory is `stage_inventory.json`; it is built
from the live `ReefMain` state names, `CastleCareerRoutes.ROOM_ACT_INDICES`,
`OperaHouse.LIVE_ACT_INDICES`, and the standalone mode roster in
`design/03_TECHNICAL_ARCHITECTURE.md`.

`surface_class` is deliberately one of:

- `avatar_locomotion`: Roshan can walk/swim/drag through a bounded stage and
  must have a walkable route, arrival trigger, and OOB recovery.
- `fixed_minigame`: the surface owns a fixed board/gesture interaction; avatar
  travel is not required inside it, but its entry/exit seam is.
- `spatial_3d_debt`: a reachable spatial mode still uses legacy 3D staging;
  it is inventoried for migration and cannot be claimed pathfinding-complete.

`status` records evidence, not intent. `UNVERIFIED` means no dedicated
arrival/OOB evidence exists yet; `PARTIAL` means the route exists but one or
more arrival, touch, or OOB requirements are open. No entry is marked complete
until a focused arrival and boundary check exists.

The coverage command is `python -B tools/audit_stage_pathfinding.py --check`;
it ends with `COVERAGE_OK` when the parsed catalogs and source paths are
covered. `python -B tools/audit_stage_pathfinding.py --strict` is a separate
logical-geometry gate and must fail while entries remain unresolved. Existing
minigame probes are lifecycle evidence only. The real corrected runtime
reproductions retain their minigame controllers; the Opera Doctor station
fixture is `opera.act.05.stuffie_surgeon`. The review atlas is
[`reproductions/index.html`](reproductions/index.html), with 34 Opera views
and 13 Castle rooms. Geometry and source hashes are recorded in
`opera_geometry.json` and `castle_geometry.json`. These are review
reproductions of the live stages, not accepted replacement art. Diagnostic
line widths do not expand the playable centerlines. Human geometry review
and target-device validation remain open. All 13 Castle rooms now have explicit connected routes. The ten newly authored
layouts have positive floor-foot clearance margins and independent painted
fixture witnesses; Bathroom, Library and Playroom retain their earlier
point-only clearance measurements. Painted Roshan containment at route vertices passes 200 facing/camera samples;
full inter-fixture silhouette and device review remain open.

Room geometry uses floor-footprint clearance in navigation coordinates. Record
each blocker as a footprint or conservative envelope with an explicit floor-foot
radius/standoff; image AABBs, atlas padding and painted extents are inspection
clues, not collision geometry. A pool's water is traversable only when the
stage declares a swim network. Review reproductions must compose the approved
runtime background tiles and live atlas fixture frames at runtime scale and
depth order. Silhouette clearance, depth occlusion, child readability and
target-device review remain separate evidence; a generic walk rectangle does
not pass them.

The implemented Castle networks have focused machine verification, while the
inventory remains PARTIAL until all geometry and external acceptance gates pass. Keep an approach
socket for travel separate from any roleplay/action socket used after arrival,
and retain each existing minigame controller and exact source-stage return
seam. The approach route is not a substitute for the action itself.

Current coverage includes 65 entries after reconciling the new Chapter 2 lawn.
Its rocket approach and battle bounds are recorded separately from still-open
floor/obstacle geometry and King-counter contact. The Castle/Opera atlas does
not claim to reproduce or visually accept that new lawn stage.

The [clearance impact record](../../design/audit_impacts/2026-09-06-stage-pathfinding-clearance.json) records the exact baseline and verification. `castle_clearance_witnesses.json` contains small independently measured solid regions that prevent incorrect runtime blocker metadata from falsely passing a route through furniture. They do not define the complete obstacle boundary.
