# Sky Lagoon ambient-animal implementation audit

> **Superseded after failed human review (5/5).** This audit accepted route
> coordinates without proving the painted support surface. The result placed
> the land animals over collapsible foliage and treated the water animals as
> animated cards rather than Jolt-supported water bodies. Its acceptance and
> performance conclusions are withdrawn. The corrected blocking audit is
> `SKY_LAGOON_ANIMAL_SUPPORT_2026-08-01.md`.

Date: 2026-08-01
Target: 1280x720 expanded canvas, Godot Mobile renderer, Speedy tier

## What failed in the first implementation

The first animal pass was asset-complete but not scene-complete. It registered all five animals and gave each a generic horizontal corridor, then kept all five `Sprite3D` cards and all five shadows alive at once. Its probe verified names, atlases, and a state change, but did not verify projected placement, gameplay continuity, habitat logic, day/night integration, or the animal actually leaving the screen.

That branch was also never integrated into `dev`: its real Lagoon probe was red. The added cards raised the audited world-art count from 34 to 44 sprites, contact shadows to 11, visible cards to 37, and depth layers to 15. In visual captures the hare crossed Roshan's pink route, the frog occupied the seesaw lane, the raccoon sat on the castle approach, and the arrival animals entered the left touch-control matte.

## Existing art-direction audit

The Lagoon is a polished 2D storybook mural presented as a shallow diorama. It is not physically lit 3D scenery, so the animals must read as painted inhabitants rather than newly lit models.

- **Color temperature:** daylight is cool and high-key: cyan sky, aqua water, blue distant mountains, and blue-green foliage. Warm color is localized to the pink/lavender route, flowers, shells, skin, and coral accents. Night is a deliberate blue-violet grade with retained aqua highlights.
- **Iconography:** shells, pearls, stepping stones, rope rails, shell-capped playground equipment, rounded castle towers, stained glass, lupine-like flowers, conifers, clouds, and oversized glossy leaves. Shapes are rounded, readable, and non-threatening.
- **Line and surface language:** deep navy/plum outlines, painterly internal texture, soft graphic shadows, controlled specular-like highlights painted into the image, and no realistic cast-light gradients on cutout cards.
- **Depth and continuity:** the walk route and interaction props are the visual priority. Ambient life belongs at habitat edges and must never compete with the route, screen seams, playground silhouettes, drawbridge, or door.

The generated animal art follows that language: rounded silhouettes, deep plum contours, painted highlights, readable faces, and a cute surprise rather than distress. A deer fawn was deliberately excluded. Its height and visual importance would turn an ambient edge interaction into a landmark, and its escape route would either cross Roshan's path or require implausible hiding space.

## Implemented habitat plan

Only one pooled animal card and one pooled contact shadow can be visible. Moving between pages rebinds that pool to the page's roster; tapping and completing an exit advances the roster.

| Page | Habitat | Animals | Authored path | May be present | Must never be present | Safe activation exit |
|---|---|---|---|---|---|---|
| 1 | Arrival shore | River otter, Pacific tree frog | Pond edge, x -62.0 to -57.8 | After the pearl plane has departed; behind the rope/waterline and left of Roshan's route | Touch-control matte, stepping route, screen seam, playground | West into the pond-bank/tree cover |
| 2 | West meadow edge | Snowshoe hare, Douglas squirrel | Shrub edge, x -20.7 to -17.2 | Behind the navigation lane and west of the slide | Pink route, slide footprint, swing, seesaw, either seam | West into dense shrub cover |
| 3 | Castle shrub edge | Raccoon | Shrub edge, x 29.0 to 34.0 | West of the castle and above the route | Seesaw, bridge, water approach, drawbridge, castle door, screen seam | West into hillside shrubs |

The path validator enforces a 3.2-world-unit clearance from every segment of the painted player route. It also rejects waypoints inside explicit rectangles for both page seams, slide, swing, seesaw, and drawbridge/door. Exit direction is authored per habitat rather than chosen from the animal's instantaneous screen position.

Idle motion uses each species' three-point path, dwell time, speed, bob amplitude, and locomotion cadence. The activation sequence is alert (0.24 s), squash (0.18 s), hop (0.24 s), then a two-frame run/hop until the projected card clears the screen by 96 pixels. The animal is non-physical, cannot block Roshan, and has no objective or save-state consequence.

## In-game lighting audit

Animals remain unshaded because the background is flattened painted art. Integration is instead handled with per-species day/night modulation and habitat-colored contact shadows. Day profiles neutralize overly warm or dark source cards; night profiles dim and cool the same cards with the mural instead of applying one generic tint.

The audit probe captured each species twice per lighting state with the Mobile renderer: once visible and once hidden at the exact habitat location. `tools/audit_sky_lagoon_animal_lighting.py` isolates changed pixels, hashes both captures, and measures the final composite rather than the source atlas.

All ten composites pass:

- mean silhouette luminance change: 0.046 to 0.182 (minimum 0.012);
- night/day animal luminance ratio: 0.353 to 0.552 (accepted 0.25 to 0.72);
- every species' relative warm/cool value decreases at night;
- mean foreground saturation remains at or below 0.824 and never increases by more than 0.08 at night;
- dark outline retention exceeds the 0.025 minimum in every capture;
- per-habitat shadows use cooler, lower-opacity values at night and remain attached to the pooled actor.

The exact metrics and SHA-256 capture hashes are in `SKY_LAGOON_ANIMALS_2026-08-01_LIGHTING.json`. The review sheet is `SKY_LAGOON_ANIMALS_2026-08-01_LIGHTING.jpg`.

To reproduce the evidence, run `scripts/probe_sky_lagoon_animals.gd` in a real 1280x720 Mobile-renderer window with `LAGOON_ANIMAL_SHOT_OUT` set to an ignored `audit/` directory, then pass that directory to `tools/audit_sky_lagoon_animal_lighting.py` with `--json-out` and `--sheet-out`. Raw full-frame captures stay under ignored review storage; the compact sheet, metrics, and hashes are the tracked evidence.

## Performance and continuity result

The corrected implementation brings the audited scene back to 36 world-art sprites, 7 contact shadows, 29 visible cards, and 11 depth layers while retaining all five species. Only one animal and one animal shadow process at a time. The living-card stress probe remains below its 1 ms update budget.

Continuity is now enforced by tests that fail if an animal path approaches the player route or enters a no-go rectangle, if shore fauna appears before the plane leaves, if more than one animal card/shadow exists, if the four activation poses do not occur in order, if the exit uses the wrong edge, or if page rosters fail to advance.
