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
and target-device validation remain open. Generic Castle layouts outside the
three explicitly authored rooms still require fixture-by-fixture review.
