# Game-Wide Art Audit and Pass-35 Rebuild

## Result

This pass replaces the former file-presence audit with runtime visual evidence.
It captures 69 representative views in Godot's Mobile renderer and preserves
all 88 roles from `audit/human_art_ledger_2026-07-16.csv` in the superseding
`audit/game_art_ledger_pass35_2026-07-16.csv`.

The pass generated or rebuilt **110 active assets**: 96 Blender GLBs and 14
OpenAI-generated 2D sprites. It also changed composition and placement in the
reef, Sky Lagoon, Northern Kingdom, castle, arenas, galaxy, dungeon, picture
games, and kart presentation.

Provisional post-pass distribution:

| Score | Roles | Meaning |
|---:|---:|---|
| 1 | 1 | Protected manual-only cat parts; automatic generation remains forbidden. |
| 2 | 2 | Unmerged Alpine review and legacy generated-source integrity follow-up. |
| 2.5 | 5 | Whole-world composition or broad terrain still below production. |
| 3 | 14 | Coherent but visibly sparse, generic, or overexposed runtime role. |
| 3.5 | 12 | Replacement candidate works, but repetition/composition still misses the 4 gate. |
| 4 candidate | 52 | Passes this capture matrix; owner review is still required for promotion. |
| 5 | 2 | Source-locked book carrot and watering can, unchanged. |

No 4/5 candidate is presented as owner-approved. The detailed CSV uses
`4_candidate_owner_review` explicitly.

## Evidence

- Capture probe: `scripts/probe_art_audit_35.gd`
- Runtime PNGs: `audit/runtime_shots_2026-07-16/pass_35/`
- Labeled contact sheets: `audit/runtime_shots_2026-07-16/pass_35/contact_sheets/`
- Blender QA: `assets_src/blender/qa_art_pass35/`
- 2D chroma sources: `assets_src/imagegen/pass35_2026-07-16/chroma/`
- Rebuild source: `assets_src/blender/art_pass35.blend`
- Reversible originals: `backups/art_pre_pass35_2026-07-16/`

The 69-view matrix covers 11 reef views including three anatomy closeups,
seven Sky Lagoon views, seven collection/Northern views, 14 castle views,
eight arena views, five Butterfly World views, all ten dungeon rooms, four
picture-game states, and three kart states.

## Strong Candidates

The clearest 4/5 candidates are the castle facade and tower silhouette, cloud
family, dream/crown/chamber stars, complete butterfly gates, bathroom fixtures,
royal and dream beds, kitchen prop family, theater, seek meadow, dungeon kit,
anatomically coherent clownfish/octopus/shrimp/jellyfish, and the rebuilt 2D
sun/tree/coal/star/fish/butterfly/Christmas interaction set.

Specific owner feedback is enforced:

- Carrot and watering can are preserved as 5/5 book assets.
- Stuffed animals and cat parts were not generated or transformed.
- Butterfly meshes/cards have complete paired forewings and hindwings.
- Coral is undersea-only and split into non-repeating modeled clumps.
- Shrimp, octopus, and jellyfish use corrected anatomy.
- Christmas trees remain bare where ornaments are interactive.
- The hermit crab remains untouched as the owner-approved 5/5 success.

## Residuals Below 4

Thirty-three roles remain visibly below the production gate after integration.
These are not hidden by the number of generated files.

| Area | Residual roles | Current finding |
|---|---:|---|
| Reef | 8 | Modeled flora and creatures improved, but the hub is still overexposed; cliff blocks, caustics, backdrop, and portal composition remain generic or intrusive. |
| Sky Lagoon | 6 | Castle/cloud focal assets improved strongly; world terrain, rainbow route, snow breakup, train, paintings, and repeated palms remain uneven. |
| Castle | 8 | Kitchen, bath, beds, and stars improved; hall walls, stairs, columns, doors, throne scaffold, and several large rooms remain sparse modular blockouts. |
| Butterfly World | 2 | Gates pass; the tiny planet's broad surface and world-wide composition remain sparse and noisy. |
| Kart | 5 | Plinths, barriers, and finish arch improved; world composition, vehicle material integration, boost language, and coral sightlines need another pass. |
| Development/Pipeline | 4 | Alpine interiors still require representative captures; Northern additions remain 3/5; old corrupt provenance files need separate quarantine work. |

The Northern Kingdom is the largest new-wing residual. Authored houses, gate,
mountains, and keep are integrated, but distant views still read as washed-out
walls and sparse roofs. The next pass should rebuild the curtain-wall kit and
compose closer child-height landmark approaches before adding more assets.

The castle's crown star itself now reads, but its surrounding cage/scaffold is
still a 2-3/5 primitive assembly. The music room and dreaming/toy floors need
larger authored room kits, not additional small props.

## Replacement Families

The Blender library includes modeled coral and rocks, kelp and seagrass,
clouds, three star landmarks, butterfly gates, kart furniture, Northern
landmarks, castle kitchen/music/bedroom sets, winter route dressing, fairy pond
flora and creatures, treasure/shop/slide dressing, galaxy furniture and gates,
corrected reef anatomy, and the dungeon pepper/ice projectiles.

Runtime placement changes reduce crossed-card density, mixed-habitat coral,
duplicate finish banners, unadorned shop walls, blocked objective sightlines,
and random clutter near the treasure chest. The ice gate and treasure chest
were recaptured after clearing their approach occluders.

## Known Audit-Harness Noise

The rapid capture probe intentionally destroys and rebuilds gameplay states in
far less time than normal play. Godot reports freed tween targets and an
already-scheduled `SlideRaceGame` lambda after teardown. All 69 captures finish,
but this noise is not accepted as gameplay validation; the trusted probes and
full analyzer remain the release gate.

## Next Art Order

1. Northern curtain walls, town grouping, and child-height approach cameras.
2. Castle hall architecture, crown scaffold, music room, toy room, and dreaming floor.
3. Reef cliff/terrain silhouette kit plus lower-energy portal and caustic composition.
4. Butterfly planet terrain patches and garden paths.
5. Kart vehicle materials and track-wide coral/boost composition.
6. Alpine interior capture matrix and corrupt legacy provenance quarantine.
