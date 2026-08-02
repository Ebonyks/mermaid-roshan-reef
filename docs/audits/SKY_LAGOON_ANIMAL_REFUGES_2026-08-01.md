# Sky Lagoon animal refuge audit ? 2026-08-01

## Decision

The previous generic startle route failed continuity review because it sent animals toward an off-screen coordinate without proving that the traversed surface remained valid. Sky Lagoon animals now retreat to an authored, visible habitat refuge. Every route is sampled against a support-zone rectangle before it is accepted at runtime; a route that leaves its page or support medium is rejected.

No new animal artwork was generated for this correction. It changes staging, motion, physics, foliage response, and lighting only. The brush-rustle card is a pooled, runtime-generated 96 x 96 image composed in code, so it has no external source asset or additional license entry.

## Authored routes

| Animal | Page | Idle/support medium | Startle destination | Refuge action |
| --- | ---: | --- | --- | --- |
| Otter | 0 | Arrival-shore water, Jolt body | Pond-edge greenery at `(-60.00, 2.72, -5.80)` | Bounded Jolt impulse toward cover, then foliage rustle and concealment |
| Frog | 0 | Arrival-shore water, Jolt body | Pond-edge greenery at `(-60.00, 2.55, -6.10)` | Bounded Jolt impulse toward cover, then foliage rustle and concealment |
| Hare | 1 | West path shoulder ground | West hedge at `(-16.82, -0.55, -4.80)` | Ground run into hedge, foliage rustle, then concealment |
| Squirrel | 2 | Castle path shoulder ground | Existing fir base at `(27.25, -0.68, -7.20)` | Ground run to trunk, climb to `(26.10, 6.10, -7.20)`, canopy rustle, then concealment |
| Raccoon | 2 | Castle path shoulder ground | Bridge-side hedge at `(31.35, -0.58, -7.00)` | Ground run into hedge, foliage rustle, then concealment |

The water refuge is contained by `Rect2(-60.2, 2.0, 3.7, 1.4)`. Ground retreats are contained by the west-path rectangle `Rect2(-21.2, -2.4, 4.5, 0.8)` or castle-path rectangle `Rect2(27.2, -2.4, 4.3, 0.8)`. Route validation samples every waypoint-to-waypoint segment and the final segment into cover. This prevents shortcuts through the lagoon, decorative leaves, unsupported scenery, page boundaries, or off-screen space.

## Animation and physics review

- Otter and frog remain Jolt `RigidBody3D` actors. Startle applies a real central impulse, while the movement controller's target is the authored shoreline refuge rather than an arbitrary off-screen point.
- Hare and raccoon stay on ground support through contact with their hedge. Their cards sink, shrink, and fade only after reaching greenery.
- Squirrel reaches the existing fir trunk before beginning a 6.78-unit vertical climb. Alternating atlas frames preserve the scramble, and the pooled leaf cluster activates in the canopy.
- All five refuge exits record contact, visible foliage response, and completed concealment. The focused probe requires all three conditions.

## Lighting review

The paired Mobile-renderer audit passed all ten day/night captures and all five response comparisons. Night modulation was tuned independently per animal to retain the lagoon's cool aqua/lavender illumination without losing the animal's warm local identity. Water animals retain their waterline treatment; land animals retain contact shadows until entering cover.

Evidence:

- Refuge review sheet: `docs/audits/SKY_LAGOON_ANIMAL_REFUGES_2026-08-01.jpg` (SHA-256 `3e0d4be54dd578eda9ed12bf1c5ed60bb193df436aa02fb35fe090a5a7f3d212`)
- Raw capture manifest: `audit/sky_lagoon_animal_refuges_2026-08-01/candidate_1/capture_manifest.json` (SHA-256 `a9d7a00f04aa202f6665c89e5939ce0b327eaffe50919fb4d0d8f62889d883b0`; ignored review evidence, not shipped)
- Lighting measurements: `docs/audits/SKY_LAGOON_ANIMALS_2026-08-01_LIGHTING.json` (SHA-256 `3326992c7bdc0279b83938d2d139fa637b080f2f65bd1e6e07ae54f2a3917ca0`)
- Lighting review sheet: `docs/audits/SKY_LAGOON_ANIMALS_2026-08-01_LIGHTING.jpg` (SHA-256 `60b0f239f41d20cf46d830d78b4b1d82bd1c24aa9ca7c4fb0ef34660d2c47683`)

## Human review notes

The Mobile captures show each animal remaining within the visible authored environment during the entire response. The refuge contact is readable at child-viewing scale: displaced leaf clusters briefly overshoot and settle around brush entries, while the squirrel's distinct vertical motion reads as a trunk climb rather than a ground escape. No route uses lily pads, floating leaves, open-water crossings by land animals, or an off-screen endpoint.
