# Sky Lagoon animal support, pathing, and lighting re-audit

Date: 2026-08-01

Target: 1280x720 expanded canvas, Godot Mobile renderer, Speedy tier

Status: corrected implementation; prior five-species acceptance withdrawn

## Rejection addressed

The earlier automated audit confused coordinate clearance with believable
support. All five species failed human review: the otter and frog were simply
translated cards over the pond, while the hare, squirrel, and raccoon appeared
to run on painted leaf masses. This re-audit makes support a runtime contract
and treats the Mobile-renderer composite as the final authority.

## Support and pathing plan

Only one animal card, one constrained `RigidBody3D`, one contact shadow, and one
waterline card are pooled across the five-species roster.

| Page | Species | Allowed support | Authored patrol | No-go continuity zones | Activation exit |
|---|---|---|---|---|---|
| Arrival pond | River otter, Pacific tree frog | Jolt water volume at y 2.72 / 2.55, behind the rope line | x -59.8 to -56.8 | Touch-control edge, stepping stones, player route, page seam, dry lawn | West, into pond-bank cover, via a real Jolt impulse |
| West promenade | Snowshoe hare, Douglas squirrel | Non-foliage stone/grass shoulder; foot y about -2.10 | x -20.7 to -17.2 | Shrub canopy, player centerline, slide, swing, seesaw, page seams | West along the ground shoulder |
| Castle promenade | Raccoon | Non-foliage stone/grass shoulder; foot y about -2.07 | x 27.4 to 29.9 | Shrub canopy, seesaw, water, bridge, drawbridge, door, page seam | West along the ground shoulder |

The explicit support rectangles are checked at every authored waypoint. Land
waypoints are evaluated at the animal's foot, not its card center. The shoulder
keeps at least 1.25 world units from the painted player-route centerline; the
animals have no collision layer and cannot obstruct Roshan. Every waypoint is
also rejected if it enters the slide, swing, seesaw, drawbridge/door, or page
seam rectangles. Shore fauna remains suppressed until the pearl plane has
departed.

## Jolt water behavior

The pond species use the project's configured `Jolt Physics` engine. The pooled
body is constrained in depth and rotation, then Jolt integrates horizontal
patrol drive, gravity-countering buoyancy, vertical damping, mass, wave response,
and the activation impulse. No gameplay tick writes the water animal's position
directly.

The blocking probe observed 49–50 solver steps before capture, vertical spans of
0.0564 world units for the otter and 0.0704 for the frog, active non-frozen
bodies, and water-surface error below 0.24 world units. Activation must set the
real escape-impulse marker and clear the viewport before the roster advances.
A generated low-overdraw ellipse follows the fixed water surface to communicate
submersion and wake; land shadows are disabled in water.

## Painted-ground result

The three land routes were moved from the nominal shrub edge to the first
continuous, load-bearing band immediately above the promenade. Mobile captures
show all feet and contact shadows on the stone/grass shoulder. The shrub pixels
remain behind the animal silhouettes; no route uses leaves as a support surface.
Idle bob is local to the card, so it does not change the audited body/foot support
point.

## In-game lighting result

Each species remains unshaded to match the flattened storybook mural, with
species-specific day/night modulation. Water fauna use a pond waterline rather
than a dry-land shadow. The night water profiles were neutralized after the
first re-audit attempt produced an overly saturated blue cast; the squirrel was
lifted slightly at night to retain its child-readable outline.

The paired Mobile-renderer audit passed all ten day/night composites and all
five response comparisons:

- mean silhouette luminance change: 0.0628–0.1939;
- night/day animal luminance ratio: 0.4157–0.5288 (accepted 0.25–0.72);
- maximum foreground saturation: 0.8178, below the 0.85 ceiling;
- minimum dark-outline fraction: 0.0571, above the 0.025 floor;
- every species dims and becomes cooler relative to its local background at night;
- every capture is inside its declared support rectangle and has the correct
  waterline/contact-shadow state;
- every water capture reports an active Jolt body and measurable solver motion.

The compact review sheet is
`SKY_LAGOON_ANIMALS_2026-08-01_LIGHTING.jpg`; exact metrics, support checks, and
capture hashes are in `SKY_LAGOON_ANIMALS_2026-08-01_LIGHTING.json`. The final
raw manifest SHA-256 is
`cdeb46baf3a23065a65d0a8d007044c0cbc6a3e0b27622ac9211139920a5a837`.

## Blocking regression coverage

`scripts/probe_sky_lagoon_animals.gd` now fails for an absent/incorrect support
zone, a land foot outside its shoulder, an unfrozen land body, a dry shadow in
water, an absent waterline, a non-Jolt or frozen water body, insufficient solver
steps, absent vertical motion, missing escape impulse, invalid page roster,
premature shore spawn, prop/seam overlap, or incomplete off-screen exit.

`tools/audit_sky_lagoon_animal_lighting.py` now joins the pixel lighting checks
with the captured support and physics contract. Reproduction requires a real
Mobile-renderer window with `LAGOON_ANIMAL_SHOT_OUT` set to ignored review
storage, followed by the audit tool with `--json-out` and `--sheet-out`.
