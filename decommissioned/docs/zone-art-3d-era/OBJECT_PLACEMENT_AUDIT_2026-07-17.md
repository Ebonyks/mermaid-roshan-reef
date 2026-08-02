# Object Placement Continuity Audit — 2026-07-17

This repeat audit extends the earlier plant/substrate check into a general rule:
generated objects must match their ecosystem, stand on a believable supporting
surface, preserve authored routes and landmarks, and avoid reserved gameplay
footprints. Authored story props are reviewed in context rather than rejected by
generic biome rules.

## Audited ecosystems

| Ecosystem | Valid support and contents | Excluded or reserved placement | Enforcement |
| --- | --- | --- | --- |
| Open reef districts | Species-appropriate seabed district; cold-water sponge, shell, and coral remain valid in the Ice district | Wrong district, central calm hub, friend gateways, rainbow portal lane, world rim | `ReefDistricts.habitat_point_allowed` and retrying family/scatter placement |
| Open-water reef | Free swimmers above local seabed and below the surface | Terrain intersections and breaches above the water | `ReefMain._aquatic_patrol_height`, with body-size clearance |
| Sky Lagoon meadow | Temperate trees, bushes, flowers, and fungi on ordinary grass | Rivers, pond, castle/moat, main path, Dream Star platforms, fountain, gatehouse, chalets, Alpine mountain body, island rim | `SkyLagoon._lagoon_ground_object_allowed` plus climate/substrate filtering |
| Sky Lagoon snow | Pine trees on open snow | Mushrooms, tropical trees, chalet interiors, mountain geometry | `SkyLagoon._lagoon_plant_allowed` |
| Butterfly World | Tropical trees, flowers, feeding trays, and bounce flowers on meadow | Both maintained sandy path bands | `_garden_fixture_allowed`; fixed fixtures are moved to the nearest meadow edge |
| Northern grassland | Pines and temperate fungi on forest grass | Fjord water, cobble road, town houses, castle, world rim | `NorthernKingdom._north_flora_allowed` |
| Northern snow belt | Pines on open snow | Mushrooms and mountain solid cores | `NorthernKingdom._north_flora_allowed` |
| Lamb meadow | Temperate trees, bushes, mushrooms, grass, and flowers | Tropical palm, hiding-bush interaction clearances, arena edge | `_lamb_meadow_placement_allowed` |
| Penguin slide gateway | Ice floe supported by the water surface; penguin above the floe | Submerged “floating” floe | Portal/floe height tied to `WATER_TOP` |
| Fetch snow arena | Snow pines, frozen lake floes, shoreline rocks and dock | No mismatch found in repeat audit | Existing authored placement retained |

## Resources removed or relocated

- Removed the tropical palm from Lamb Meadow's generated tree pool.
- Suppressed any generated flora candidate that lands on an incompatible
  substrate or reserved authored footprint.
- Relocated saved crafted friends away from Sky Lagoon water, paths, structures,
  and landmark platforms using deterministic retries.
- Relocated Butterfly World feeding trays and bounce pads from sandy walking
  paths to the closest meadow edge.
- Raised the Penguin Slide floe from deep underwater to the water surface.
- Extended Northern Kingdom dock posts into the fjord and added supporting masts
  beneath its pennants.
- Clamped reef creature patrol height to local terrain and body clearance.

## Deliberate continuities retained

- Pine trees remain valid on open snow.
- Mushrooms remain valid in the Northern Kingdom's grassy forest; the kingdom is
  not globally snow-covered just because its mountains have snow caps.
- Cold-water sponges, shells, and coral remain valid in the underwater Ice
  district.
- Castle gates and route markers may intentionally meet paths; this exception is
  explicit and is not applied to generic flora or play fixtures.

The trusted probes now exercise each reusable rule so later layout expansion
cannot silently reintroduce the audited mismatches.
