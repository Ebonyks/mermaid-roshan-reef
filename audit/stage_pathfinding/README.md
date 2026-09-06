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
