# Reef of Light — Flora & Asset Identity (with licensing record)

Decision (per project direction): **marine-first flora with magic accents**. The land-garden
(mushrooms/flowers) from the legacy build is retired. Every reef element is sea-native;
the "fairy tale" reads through bioluminescence and hero spirit-lights, not land plants.

## Flora roster (in the build now)

| Element | Form | Source | License |
|---|---|---|---|
| Seagrass meadows (3,200) | crossed swaying blades, baked leaf texture (vein/serration) | procedural + own baked texture | original (project) |
| Kelp columns (800) | tall swaying ribbons, glow tips | procedural | original (project) |
| Anemones (520 + giant grove crowns) | 9-tentacle curved crowns, glowing tips | procedural mesh | original (project) |
| Starfish (340) | 5-arm flat star, tip glow | procedural mesh | original (project) |
| Sea urchins (300) | spiked balls, needle glow | procedural mesh | original (project) |
| Coral fans (600) | upright sail fans | procedural | original (project) |
| Reef rock outcrops | grove hearts, PBR stone | geometry procedural; texture **Rock061, ambientCG** | **CC0** |
| Seabed | splat sand w/ ripples | **Ground054, ambientCG** | **CC0** |
| Caustics + plankton + god rays | shader/particles | procedural | original (project) |

> ⚠️ **LICENSING ACTION REQUIRED (2026-06-25).** The corals/seaweed/shells/rocks below — and the
> rigged fauna in the next table — are the Riley *Aquatic Animal Models* pack (rkuhlf-assets.itch.io),
> licensed **"free use, NO redistribution."** Shipping them in a public repo *is* redistribution, so
> they must be swapped for CC0 equivalents. The swap is currently **network-blocked** (every free-asset
> CDN returns egress-policy 403; only github.com is reachable). Full audit, blocker evidence, and a
> ready-to-run replacement manifest: see **`ASSET_AUDIT.md`**.

Pending **replacement** (download blocked — see `ASSET_AUDIT.md` §3): **7 coral variations + 3 seaweeds,
11 rocks, shells** from *Aquatic Animal Models* (Riley / rkuhlf-assets.itch.io). To be replaced with
Quaternius CC0 equivalents once the egress allow-list opens.

## Fauna roster

| Element | Source | License |
|---|---|---|
| 6 glowing fish schools, 3 mantas, 1 whale, 2 turtles | procedural meshes + shaders | original (project) |
| Shark, hammerhead, squid, octopus, eel, stingray, turtle, seal, crab + 4 fish (rigged/animated) | *Aquatic Animal Models* (itch.io) — ⚠️ **NO-REDISTRIBUTION; replace with CC0, see `ASSET_AUDIT.md`** | free use, no redistribution |

## Characters & hero set pieces (preserved)

| Element | Source | License |
|---|---|---|
| Roshan (inflated art mesh, 26-bone rig, **new 2K texture from source art**) | book illustration (project IP) | project-owned |
| 5 friends (book art sprites): Evie & Lamb-a', Harper & Fiona, Faron, Friendship Flower, Wacky & Chuck | book illustrations (project IP) | project-owned |
| Shipwreck, ghost ship, chest, barrel | **Kenney Pirate Kit** | **CC0** |
| Chuck (fetch game dog), plush dolls (bunny, cat), nursery backdrop, flower-girl art | book illustrations, cut out from gemini_originals_backup pages | project-owned |
| Wood/plank PBR (ship) | **Planks023B, ambientCG** | **CC0** |
| Voice clip ("Yay!") | floraphonic via **Pixabay** | Pixabay Content License (free use) |
| 6 music loops | synthesized for project | original (project) |

## Engine base

| Component | Source | License |
|---|---|---|
| Godot 4.4 | godotengine.org | MIT |
| FFT ocean surface, buoyancy, underwater post (addon + example scene at `example/Example.tscn`) | **godot4-oceanfft** (tessarakkt, GitHub) | **MIT** |
| Kenney Nature/Pirate kits (rocks, dressing fallback) | kenney.nl | **CC0** |
| Sky Lagoon decoration: trees, flowers, mushrooms, bushes, cliffs (level 2) | **Kenney Nature Kit** (kenney.nl) | **CC0** |
| Stage-2 minigame plant/flower/tree sprites (garden, xmas) | **Kenney Foliage Pack** (kenney.nl) | **CC0** |

Project is non-commercial (IP-encumbered); all sources above are compatible.
