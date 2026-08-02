# Reef Redesign Audit — 2026-07-16

## Verdict

The first district redesign failed its visual and navigation goals. It increased
the number of named object families, but the new families were stiff symbolic
assemblies and were placed into an already crowded inner ring. The result had
more objects without more believable ecology, clearer travel, or stronger
geographic separation.

## Measured failures

| Area | Finding | Consequence |
|---|---|---|
| Faron access | Faron spawned about 115 m from the hub; the other friends were 55–85 m away | A preschool player had a uniquely long trip to the dolls game |
| Faron approach | Faron shared the Moon bowl with a 42 m shell arch and two 32–38 m cliff masses | The approach was visually blocked and terrain-heavy |
| District spacing | Minimum center separation was about 96 m | Adjacent biomes occupied the same views |
| Palette spacing | Adjacent tint radii totaled about 150–176 m | Color fields overlapped before a player left either district |
| Macro density | Approximately 34 macro props occupied the reef ring | No negative space or readable threshold between places |
| Generic geology | 40 grove rocks plus 42 scattered boulders | New silhouettes were diluted by the same rock language everywhere |
| Scatter logic | 16% of mass scatter deliberately bridged districts | Habitat boundaries were erased procedurally |
| Kelp assets | Mirrored tubes with identical paddle leaves; upright oval lanterns | Read as a constructed gate and cattails, not underwater growth |
| Moon assets | Mirrored flat fan panels and stacked spheres | Read as furniture/handbag shapes rather than shell erosion |
| Ice assets | Straight cones and flat extruded fins | Read as generic crystals, not water-sculpted ice/current forms |

## Repair criteria

- Minimum authored district-center separation: **125 m**.
- Faron: **75 m or less** from the hub, on a flattened open approach.
- Preserve close, reachable friend gateways while pushing the dense scenic
  bodies outward behind them.
- Narrow palette fields enough to leave neutral sand/water buffers.
- Remove random cross-district scatter.
- Reduce groves from 18 to 14, macro props from roughly 34 to 9, grove rocks
  from roughly 40 to 13, and loose boulders from 42 to 24.
- Rebuild the six existing regional GLBs as asymmetric curved/eroded forms with varied
  thickness, lean, height, and silhouette.
- Add a dedicated organic Wreck ridge if removing the generic cliff slabs leaves
  that district without destination-scale geology.
- Keep every new or rebuilt asset texture-free, Mobile-friendly, and editable
  from the checked-in Blender source.

## Intended world rhythm

The hub and friends form a reachable inner necklace. Each friend stands at a
clear biome gateway, not inside the densest scenery. Past that gateway, each
district grows outward into its own scenic body. Neutral seabed between those
bodies provides the visual pause that the first pass lacked.

## Repaired composition

| Measure | Rejected pass | Repaired pass |
|---|---:|---:|
| Minimum district-center separation | ~96 m | **~129 m** |
| Faron distance from hub | ~115 m | **~72 m** |
| Authored groves | 18 | **14** |
| Macro structures/region props | ~34 | **9** |
| Grove rocks | 40 | **13** |
| Loose perimeter boulders | 42 | **24** |
| Cross-district scatter chance | 16% | **0%** |

Faron now occupies a 30 m flattened nursery clearing before the Moon district,
rather than the Moon bowl itself. His approach is not shared with the shell
arch or cliff enclosure. Friend positions and their guidance-pearl routes use
the same authored gateway coordinates, so the visual path and actual activity
entrance cannot drift apart. Faron also has a more forgiving 12 m discovery
radius and 10 m game-start radius (the standard friends remain 9 m / 8 m), so a
young touch player does not have to hold a narrow position during the countdown.

## Region-by-region identity audit

| Region | Terrain / spatial role | Primary object vocabulary | Separation judgment |
|---|---|---|---|
| Pearl Garden | Broad calm hub and low framing stones | Shell gardens, barrel sponges, pearl-shop ship | Quiet, low, familiar starting area |
| Kelp Cathedral | Long outer ridges and a living threshold | Tapered old-kelp trunks, trailing blades, hanging lantern pods, tall aisles | Strongest vertical/green silhouette; dense body begins beyond Harper |
| Wreck Ravine | Diagonal trench with raised irregular shoulders | Broken ship, treasure debris, two dedicated organic reef ridges | Hard-edged salvage and negative trench distinguish it without generic cliff slabs |
| Moon-shell Grotto | Outer bowl and broken enclosing ring | One eroded shell-rock arch, open pearl nest, anemone bowl | Rounded lavender enclosure is unique; Faron remains in the open gateway before it |
| Rainbow Flats | Two large flattened race clearings | Race gateway, low coral bouquets, starfish flats | Deliberately lowest and most open region, with uninterrupted sightlines |
| Ice Current | Sparse blue-grey outer shelf | Rounded brinicle hummocks, directional frozen-current sheets, penguin floe | Cool palette is reinforced by a flowing horizontal silhouette rather than generic crystals |

Every district has at least three role-specific families and a distinct terrain
profile. Repetition remains inside each habitat as ecological rhythm, but shared
generic rocks have been reduced enough that they no longer define the map.

All interactive gateways and authored macro structures remain inside the 270 m
player boundary. The outermost wreck shoulder is about 237 m from the hub,
leaving a usable margin before the boundary clamp; loose boulders alone dress
the non-interactive cliff rim.

## Asset rebuild audit

The first six Blender assets were rejected twice during repair review. The final
generation removes mirrored gates, stacked spheres, cones, flat fan symbols,
and uniform tubes. Production geometry now uses varying-radius curves,
irregular continuous sweeps, and smoothed tapered ribbons. The checked-in
Blender source and isolated QA renders were regenerated with the GLBs so the
silhouettes remain inspectable and reproducible.

The first in-engine capture then exposed a separate inherited problem: the
generic cliff-block GLBs rendered as enormous rectangular slabs, including one
directly across Faron's approach. All 10 generic slab/spire placements were
removed. Wreck Ravine, the one region that still needed large framing geology,
received a seventh purpose-built asymmetric reef-ridge asset instead.
