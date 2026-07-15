# Art Remediation Batch 04

_Working date: 2026-07-14_

This pass targets every current audit row scored 2/5 or lower. The audit scope
is global across existing game assets and runtime paths. New generated artwork is
then judged separately against a 4/5 quality gate; that gate does not regrade
every existing asset. Protected book art, family/friend cutouts, and child-owned
toys remain excluded from automatic generation.

## 2/5-and-lower inventory

| Score | Existing assets or runtime family | Action |
|---:|---|---|
| 2 | Legacy `roshan.glb`, `fairy.glb`, `huluu.glb`, `chuck_poodle.glb`, `chuck_poodle_slim.glb` | Keep as fallbacks only; preferred Roshan/Fairy paths and protected Huluu cutout are used. No bitmap is treated as a rig replacement. |
| 2 | Kart direct legacy coral, seaweed, shell, rock, sand-dollar, `ClownFish`, `Dory`, `Tuna`, and `Carp` roles | Route through GEN2 props/creatures; legacy files remain fallback-only. |
| 2 | Direct `assets/aquatic/*.glb` fallback family | Do not add consumers; route by role or retire when a verified fallback exists. |
| 2 | `assets/galaxy/butterfly1.glb`, `butterfly2.glb` | Prefer complete GEN2 butterfly cards; legacy GLBs remain missing-file fallback only. |
| 2 | `grass.jpg`, `beachball.png`, world `flower.png`, `flower2.png`, `leaf.png` | New painted raster candidates `001`-`005`. |
| 2 | `assets/vehicles/monstertruck.glb` and `monstertruck_Atlas.png` | Candidate `022` repaints the existing UV atlas; GLB UV/material verification remains open. |
| 2 | Rainbow paint shader | Matte-to-satin code correction: `METALLIC=0.0`, `ROUGHNESS=0.72`, restrained emission. |
| 2 | `fish_body.png`, `fish_fins.png` | New layered candidates `006`, `007`; preserve the existing line-layer contract. |
| 2 | Minigame placeholder family: coal, flowers, bushes, pines, sprouts, stars, sun, trees | New candidates `008`-`013`; direct book carrot, watering can, and friendship flower remain protected. |
| 2 | `orn1.png`-`orn5.png` | New detachable ornament set `014`; Christmas remains one empty tree plus five ornaments. |
| 2 | `rainbow_swatch.png` | New fin-shaped palette swatch `015`. |
| 2 | Visible `lagoon_day_2k.hdr`, `lagoon_dusk_2k.hdr` presentation | Painted sky candidates `016`, `017`; HDRs may remain only as non-visible lighting data. |
| 2 | Procedural glow-tip anemones and urchins | New cards `018`, `019`; first urchin draft rejected for inventing a face, v2 accepted. |
| 2 | Procedural giant fish and slide-arena grass stand-in | New ambient fish card `020`; grass is covered by `005` and the existing GEN2 foliage family. |
| 2 | Kart finish checker, boost strips, generic hazard primitives | New motif sheet `021`; route/implementation still needs material-level integration. |

The score-2 list contains no permission to alter `assets/book/`,
`assets/characters/friends/`, `assets/audio/voices/`, or child-owned toys.

## Generated candidates

| Candidate | Intended role | Review status |
|---|---|---|
| `001_grass_blank_tile` | `assets/terrain/grass.jpg` | 4/5 pass; blank, matte, repeat-oriented ground family |
| `002_beachball_matte` | `assets/terrain/beachball.png` | 4/5 pass; broad matte toy panels |
| `003_flower_coral_card`, `004_flower_lavender_card` | world `flower.png`, `flower2.png` | 4/5 pass; above-water plants kept separate from reef flora |
| `005_leaf_tropical_sheet` | `assets/terrain/leaf.png` and tropical leaf material rebakes | 4/5 pass; four distinct leaf habits, separated for extraction |
| `006_fish_body_layer`, `007_fish_fins_layer` | `assets/mg/fish_body.png`, `fish_fins.png` | 4/5 style pass; registration must be checked with `fish_line.png` before wiring |
| `008_k_bush_round` | `k_bush.png`, `k_bush2.png` | 4/5 pass; readable rounded bush, replaces the cone/flame failure |
| `009_seed_sprout_family` | `seed.png`, `sprout.png`, `k_sprout.png` | 4/5 pass as a growth-stage family sheet |
| `010_coal_pair` | `coal.png` | 4/5 pass; two separate draggable pieces |
| `011_star_reward`, `012_sun_garden_icon` | `star.png`, `sun.png` | 4/5 pass; warm, rounded reward/garden icons |
| `013_tree_family_sheet` | `tree.png`, `xtree.png`, `k_pine.png`, `k_xmastree.png` | 4/5 pass as a family/reference sheet; Christmas use remains an empty tree board plus ornaments |
| `014_ornament_set` | `orn1.png`-`orn5.png` | 4/5 pass; five detachable ornament designs |
| `015_rainbow_swatch_fin` | `rainbow_swatch.png` | 4/5 pass; soft fin-shaped palette control |
| `016_sky_lagoon_day_painted`, `017_sky_lagoon_dusk_painted` | visible sky presentation | 4/5 pass; painted panorama candidates |
| `018_anemone_card` | procedural anemone replacement | 4/5 pass; single base and countable tentacles |
| `019_urchin_card_v2` | procedural urchin replacement | 4/5 pass; non-character marine prop after rejecting the face draft |
| `020_giant_fish_card` | procedural giant fish replacement | 4/5 pass; complete gentle side-profile silhouette |
| `021_kart_motif_sheet` | checker, boost, and hazard motif reference | 4/5 pass as an implementation sheet; split into runtime materials before wiring |
| `022_monstertruck_atlas` | `assets/vehicles/monstertruck_Atlas.png` | 3/5 provisional; palette and surface language pass, but exact UV alignment must be verified on `monstertruck.glb` before use |

The normalized `final/` folder contains 22 generated candidate files: 21 pass
the 4/5 new-art gate, and the monster-truck atlas remains provisional. The
`replacement_candidates/` folder maps exact raster roles without overwriting
runtime assets. All generated files are review-only until approved in context.

## Non-raster replacement status

- Kart ocean decoration, fish, shell pickup, and several hazards now prefer the
  existing GEN2 models/cards through `scripts/kart.gd`.
- Butterfly World coral, pedestal rock, and butterfly decoration now prefer the
  GEN2 family through `scripts/galaxy.gd`.
- The castle throne and Butterfly World avatar use protected Huluu source art;
  the plush-era Huluu GLB is no longer promoted.
- The rainbow shader now uses matte-to-satin response instead of chrome-like
  metallic response.
- The monster truck now has a review-only atlas candidate, but the model still
  needs UV/material verification and Mobile screenshot review. Image generation
  cannot replace geometry, rigging, collision, or animation contracts. Remaining
  fallback GLBs likewise stay open until their preferred runtime paths are
  screenshot-verified.

## Second-pass audit of new generations only

| New candidate | Score | Result |
|---|---:|---|
| `001`-`018`, `020`-`021` | 4 | Passes style gate for the stated raster/card or reference role |
| `022_monstertruck_atlas` | 3 provisional | Style/palette pass; exact UV alignment and in-game material response remain unverified |
| First urchin draft | 2 | Rejected: invented a mascot face and expression |
| `019_urchin_card_v2` | 4 | Passes: species-readable, non-character, broad spine silhouette |

Existing 2/5 and 1/5 assets are not regraded by this table. Their remediation
status is tracked in the inventory above and in `ART_STYLE_AUDIT.md`.
