# Measured Interface Sheet — Fable 5 constructor workstream, 2026-07-19

Source of truth: `scripts/arena/courtyard_train.gd` at 75af34d (verbatim
constants and build code), `scripts/main.gd` `_build_meadows`/`_scatter_field`/
`_art35_static_mesh`, and Blender bbox probes (`tools/probe_glb_bounds.py`) of
the active runtime assets. All numbers are game units, Godot Y-up. Train car
space: origin ON the railhead at the bogie midpoint, +Z = direction of travel.

## Track (from `_build_track` / `_ring_ribbon`)

| Quantity | Value | Source |
|---|---|---|
| Ring radius | 191.5 nominal, variable (west tuck to ~151.5) | `RING_R`, `_ring_r()` |
| Ring circumference | TAU x 191.5 = 1203.2 | derived |
| Rail centerlines | x = ±1.55 | `_ring_ribbon(o, ±1.55, ...)` |
| Rail width / top / skirt | 0.34 wide, top y +0.30, skirt drop 0.6 | half_w 0.17, y_off 0.30 |
| Tie size | 4.6 x 0.2 x 1.1, tie top y −0.18 | tie BoxMesh, y −0.28 center |
| Tie count / spacing | 240 around ring = 5.013 apart | `tie_n` |
| Deck ribbon | 5.4 wide, top y −0.45, skirt 1.2 | first `_ring_ribbon` |
| Railhead above terrain | 0.55 | `RAIL_LIFT` |

**Authored straight segment**: length 5.013 (one current tie spacing), so 240
instances tile the ring exactly where the 240 ties sit today. Chord-vs-arc
sagitta at r191.5, L5.013 is L²/8r = 0.016 — invisible; straight pieces ARE
the correct ring tiling. Ends flush (no toy connector nubs at runtime), rails
full length, 4 ties per piece at 1.2533 spacing (4x today's tie density,
matching the approved sheet's rhythm).

**Quarter-curve**: the live ring's variable radius (191.5 with a smoothstep
tuck) cannot be tiled by any fixed-radius curve piece; straight chords tile it
with 0.016 error. The curve kit piece is therefore built at r = 12.0 (tangent
ends, same rail/tie section and gauge) for spur/display/future small-loop use,
and this decision is the recorded constructor answer to the audit's
"radius derived from the active ring" requirement.

## Locomotive (from `_build_engine` / `_car_base` / `_build_train`)

Runtime KEEPS: wheels/axles (z −1.9 / 0.2 / 2.3, wheel r 1.3, width 0.5,
centers x ±2.4, gold crank pin r 0.22 at x ±2.7, axle height y 1.6), side rods
(0.22 x 0.3 x 5.2 at x ±2.75, animated), smoke particles, colliders, seats.
The authored GLB is the BODY SHELL ONLY.

| Part | Measured geometry |
|---|---|
| Chassis | 4.4 x 0.7 x 9.0 box at y 2.0 |
| Boiler | cylinder r 1.9, z −1.2..4.0, center y 3.8 |
| Smokebox ring | r 2.05, w 0.6 at z 4.2 |
| Headlamp | sphere r 0.55 at (0, 3.8, 4.6), emissive |
| Boiler bands | r 1.98, w 0.3 at z 0.0 and 2.6, gold |
| Funnel | cone r1.0 -> 0.55, h 1.7 at (0, 6.4, 3.2); top y 7.25 |
| Steam dome | sphere r 0.8 at (0, 5.9, 0.8), gold |
| Cab | 4.4 x 3.8 x 2.8 at (0, 4.6, −2.9); roof 5.0 x 0.5 x 3.4 at y 6.75 |
| Cab windows | 1.5 x 1.5 at x ±2.25, y 5.1, emissive cream |
| Cowcatcher | cone rb 2.1, h 1.9 at (0, 1.3, 5.1), z-scale 0.55 |
| Envelope | width ≤ 5.0, height ≤ 7.5, z −4.3..6.05; keep y < 0.6 clear between wheel wells |
| Colors | teal (0.35,0.75,0.78), navy (0.22,0.22,0.40), gold (0.95,0.80,0.40) |

Wheel/rail note (existing visual, preserved): wheel discs ride at x ±2.4,
OUTSIDE the ±1.55 visual rails — this is the shipped look, not an error.

## Station (from `_build_station` + bbox probe)

Existing authored station GLB (`lagoon_train_station.glb`): 6.3 x 12.2
footprint, 7.5 tall, placed at ring bearing 2.1, radial offset +6.5, ground
height, NON-SOLID (owner: nothing at the station may pinch). Bench at +2.2 x.

**Platform piece**: deck 12.0 long x 5.2 wide, deck top y 1.1 (low — boarding
is a 9.0-radius proximity plop, not a climb; coach floor 2.7 is above it),
steps on the side away from the track. Placed with its rail-side edge ≥ 3.4
from track centerline (car half-width 2.3 + margin; CAR_SOLID_R 3.1 is the
collider, and the platform stays non-solid regardless).

**Shelter piece**: 4 posts + open roof, own origin at ground; roof underside
6.3 (= deck 1.1 + 5.2 clearance, comfortably above seated-Roshan head height
~+3.5 over a 4.5 seat). Posts inset so the boarding face and train face stay
fully open.

## Reef flora (from `_build_meadows` + bbox probes)

`_art35_static_mesh` uses ONLY the first MeshInstance3D and ignores its node
transform -> flora GLBs must be a SINGLE mesh, identity transform, origin at
the burial point, +Y up. Scatter applies scale 0.55..2.45 with y x0.8..1.6.

| Reference | Measured |
|---|---|
| kelp_0.glb | 1.0 x 1.0 footprint, 3.54 tall |
| kelp_1.glb | 1.5 x 1.4 footprint, 3.54 tall |
| gen2 coral1/3 | 1.4 x 1.2 footprint, 1.82 tall |
| roshan_v4.glb | 2.0 tall model |

**Authored kelp (r004)**: single mesh, ~3.5 tall, ≤1.6 footprint, 6 stems,
volumetric ribbon blades, stems taper to direct burial at origin, foot −0.1.
**Authored coral (r003)**: single mesh, ~2.6 tall x ~2.1 wide, bare antler
branching, no pedestal, buried foot extending to −0.15 below origin.
