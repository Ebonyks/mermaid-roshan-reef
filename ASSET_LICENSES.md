# Asset license ledger

All third-party assets in this project are CC0 / royalty-free and free to redistribute.

## Audio
- chuck_bark.ogg / chuck.ogg — 'Free Dog Bark' by DRAGON-STUDIO via Pixabay (Pixabay Content License, royalty-free, no attribution required). Source: pixabay.com, file dragon-studio-free-dog-bark-419014.mp3. Trimmed + normalized.

## Terrain / surface textures (`assets/terrain/up_*`)
PBR sets (color + normal + roughness), CC0 1.0 Public Domain.

| Texture set | Used for | Source | License |
|---|---|---|---|
| up_cliff_* | dry land cliffs (Sky Lagoon, treasure arena, winter shore) | Poly Haven | CC0 1.0 |
| up_grass_*, up_dirt_*, up_sand_*, up_water_* | lagoon ground, reef seabed, water | Poly Haven | CC0 1.0 |
| up_snow_* | winter (fetch) minigame — Poly Haven snow_02 | Poly Haven | CC0 1.0 |
| up_wood_*, up_castle_*, up_cobble_*, up_flagstone_*, up_marble_*, up_roof_* | ships/props, castle interior | Poly Haven | CC0 1.0 |
| **up_reefrock_*** | **Level 1 reef — wet rock formations (overworld cliff/rock models)** | **ambientCG "Rock030"** | **CC0 1.0** |
| **up_seastone_*** | **Level 1 reef — submerged boulders, grove rocks, treasure cavern** | **ambientCG "Rock035"** | **CC0 1.0** |

The `up_reefrock_*` (Rock030, a wet coastal rock) and `up_seastone_*` (Rock035, a
layered sea stone) sets were added in the Level 1 reef texture audit so the
underwater rocks read as submerged stone rather than the dry-land cliff texture
previously reused there. Both originate from ambientCG.com (Lennart Demes),
released under CC0 1.0 — free for any use, no attribution required. They were
obtained from public GitHub-hosted CC0 mirrors of the ambientCG library.

## Reef coral & sea-plant textures (`assets/terrain/up_coral_*`, `up_algae_*`)
Original, procedurally-authored seamless PBR sets (color + normal + roughness,
1024px) created for this project — released as CC0 1.0 (own work). Generator:
`tools/gen_reef_textures.py` (numpy/Pillow). No third-party source.

| Texture set | Used for |
|---|---|
| up_coral_* | living coral colonies + shells/starfish (`_aq_mat`, tinted per species) |
| up_algae_* | swaying seaweed / sea plants (`_aq_mat` SeaWeed) |

These replace the older low-res `polyp.png` / `leaf.png` detail maps on the reef
flora so coral and sea plants gain real surface relief (normal map) at higher
resolution. CC0 coral/sea-plant PBR sets were not obtainable from the reachable
asset sources (the dedicated CC0 CDNs are blocked by network policy and the
GitHub matches were git-LFS pointers or non-CC0 asset-store packs), so these were
authored from scratch instead.
