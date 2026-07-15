# Mermaid Roshan Full Art Inventory

_Audit date: 2026-07-14_

This is the complete directory-level art audit companion to
`ART_STYLE_AUDIT.md`. It covers 487 visual source files under `assets/`,
excluding audio, `.import` metadata, and generated review trees outside the
runtime asset tree. Grouped rows use one score only when the files share the
same source family, runtime treatment, and finding.

## Folder coverage

| Folder | Visual files | Baseline | Coverage and decision |
|---|---:|---:|---|
| `assets/aquatic/` | 45 | 2 | Legacy pack family. Keep only as a missing-file fallback; route roles to GEN2 or retire. |
| `assets/aquatic2/` | 33 | 3-5 by matching GEN2 creature | Duplicate large creature packaging; not the preferred main-reef path. |
| `assets/book/` | 22 | 5 | Protected source art. Never auto-generate, resize, recompress, or replace. |
| `assets/castle/` | 8 | 4 | Strong painted furniture surfaces; polish only. |
| `assets/characters/` | 50 | 2-5 by role | Protected cutouts and approved models are canonical; legacy models are fallback-only. |
| `assets/galaxy/` | 51 | 2-4 | Butterfly wings are below target; crystal, fruit, beetle, and tropical plant families need future polish. |
| `assets/icon/` | 3 | 5 | Protected product identity art. |
| `assets/kits/` | 41 | 3 raw, 4 in main path | Generic kit models are redirected to GEN2 where available; raw files remain source inputs. |
| `assets/mg/` | 37 | 1-5 by item | Source-derived carrot, watering can, friendship flower, and snowman are protected; placeholder family has Batch 04 replacements. |
| `assets/nature/` | 18 | 3-4 | Main path uses GEN2 trees; lawn-textured plant and leaf stand-ins remain a rebake queue. |
| `assets/portal/` | 1 | 4 | Butterfly gate is a strong focal prop with GEN2 butterfly cards. |
| `assets/props/` | 109 | 3-5 | Preferred GEN2 creatures, props, playground models, cards, masks, and Batch 01 Blender replacements. |
| `assets/ship/` | 5 | 3 | Readable ship-story props; needs a shared painted trim pass. |
| `assets/sky/` | 2 | 2 | HDRs are retained only as possible lighting data; painted visible sky candidates are staged. |
| `assets/terrain/` | 57 | 1-5 by item | Strong painted surfaces plus low-scoring generic/prop-cluttered textures; candidates are staged. |
| `assets/vehicles/` | 5 | 2-4 | Batch 01 monster truck is the provisional preferred route; motorcycle and kart need later livery polish. |

Audio and voice files were intentionally excluded from this art score. The
protected voice rule remains in `AGENTS.md` and is unchanged.

## Technical findings separate from style score

- 39 existing raster maps exceed the 1024px longest-side rule, primarily the
  2048px `assets/aquatic2/` maps and Chuck texture maps. They predate the new
  asset rule and were not resized or recompressed in this audit. New candidates
  in the review trees are normalized to the current limit.
- The runtime reference scan found two genuinely absent historical terrain
  sources: `Ground054_2K_Color.jpg` and the `Rock061_2K_*` set. The rainbow-road
  color texture is also absent, but its code path has a procedural fallback.
  These are dependency findings, not new style candidates.
- Other scan hits such as `up_%s_col.jpg`, `assets/kenney/`, `orn` prefixes,
  `SeaWeed%s.glb`, and `roshan_%s.ogg` are dynamic path templates rather than
  missing files. They should not be scored as individual art assets.

## Complete score bands

### Score 5: protect and reuse

- All direct `assets/book/` pages, characters, props, and backgrounds.
- `assets/characters/friends/` family cutouts and canonical Roshan cutouts.
- `assets/characters/skins/` Fairy source derivative and wing card.
- `assets/icon/` product identity images.
- `assets/mg/snowman.png`, `carrot.png`, `wateringcan.png`, and the book
  `friendship_flower.png` used in the picture games.
- `assets/props/gen2/turtle.glb`, `stingray.glb`, `seagrass.png`, and `kelp.png`.
- `assets/terrain/backdrop_seamounts.jpg`, `up_cliff_col.jpg`, and
  `up_marble_col.jpg`.

### Score 4: keep, polish when touched

- `assets/characters/roshan_v4.glb` and `fairy_v2.glb` pending Mobile screenshot
  comparison against their protected references.
- GEN2 clownfish, shark, hammerhead, squid, octopus, lobster, and crab models.
- GEN2 coral, rock, shell, sand-dollar, starfish, sponge, playground, and tree
  families.
- Castle bed and throne surfaces, portal gate, galaxy tray, and source-compatible
  UI/effect motifs.
- Graphic water, caustics, bubble columns, sparkle bursts, motion rings, and
  pearl objective beacons at restrained opacity.

### Score 3: unify through a future material or model pass

- Roshan V2/V3, Lamb, rigged Chuck, GEN2 dolphin/whale/penguin, and craft
  kitty/birdie families.
- Galaxy crystal, fruit, beetle/ladybug, and tropical plant families.
- Raw kits, raw nature pack models, furniture, park, ship, and vehicle
  motorcycle/kart families where they are not redirected to GEN2.
- Dirt, grass, sand, snow, water, and decorative texture families that are
  attractive but repeat too densely or contain baked props.
- HUD panels, labels, touch controls, sticker toast, and box/cylinder arena
  architecture where the functional design is sound but the treatment varies.

### Score 2 or lower: replacement institution

| Score | Complete source family | New-art or runtime institution | 3D conversion status |
|---:|---|---|---|
| 2 | Legacy character models: `roshan.glb`, `fairy.glb`, `huluu.glb`, `chuck_poodle.glb`, `chuck_poodle_slim.glb` | Do not promote. Roshan V4, Fairy V2, rigged Chuck, or protected Huluu cutout are the preferred paths. | Retire/fallback policy. Huluu requires an explicitly approved source-faithful model, not auto-generation. |
| 2 | Entire direct `assets/aquatic/*.glb` fallback family, including coral, seaweed, shells, rocks, fish, and invertebrates | No new direct consumers. Kart, Butterfly World, and main-reef role aliases prefer GEN2 replacements. | Existing GEN2 meshes are the replacement family; remaining legacy files are deprecation inputs. |
| 2 | `assets/galaxy/butterfly1.glb`, `butterfly2.glb` | Prefer complete `butterfly_story.glb`; cards and legacy GLBs remain fallbacks. | Batch 01 paired-wing mesh is wired and pending Mobile QA. |
| 2 | `assets/terrain/grass.jpg`, `beachball.png`, `flower.png`, `flower2.png`, `leaf.png` | Batch 04 candidates `001`-`005`, exact-role copies staged review-only. | Leaf and flowers are mesh/card-ready; grass remains a repeat-safe tile. |
| 2 | `assets/vehicles/monstertruck.glb` and `monstertruck_Atlas.png` | Prefer the Blender-authored `monstertruck_story.glb`; retain old rover only as fallback. | Batch 01 rounded matte mesh is wired and pending Mobile paint/orientation/collision QA. |
| 2 | Rainbow paint shader | Code correction to matte-to-satin response: zero metallic, high roughness, restrained emission. | Shader institution, no mesh conversion. |
| 2 | `assets/mg/fish_body.png`, `fish_fins.png` | Batch 04 candidates `006`, `007`; preserve `fish_line.png` registration. | Ready for a layered low-poly fish mesh or cutout rig after registration check. |
| 2 | Minigame placeholders: `coal.png`, `flower*.png`, `k_bush.png`, `k_flower*.png`, `k_pine.png`, `k_sprout.png`, `star.png`, `sun.png`, `tree.png`, `xtree.png`, `sprout.png` | Batch 04 candidates `008`-`013`; source book carrot, watering can, friendship flower, and snowman stay protected. | Family sheet is the modeling reference; split items before runtime or mesh conversion. |
| 1 | `assets/mg/k_bush2.png` | Replaced by the rounded bush candidate in Batch 04. | Ready as a simple low-poly bush card or mesh. |
| 2 | `assets/mg/orn1.png`-`orn5.png` | Batch 04 candidate `014`; five detachable designs, one empty tree board. | Each ornament is a separate mesh-ready concept; do not model the sheet as one object. |
| 2 | `assets/mg/rainbow_swatch.png` | Batch 04 candidate `015`; fin-shaped, matte palette control. | UI-only; no mesh conversion. |
| 2 | Visible `assets/sky/lagoon_day_2k.hdr`, `lagoon_dusk_2k.hdr` | Batch 04 candidates `016`, `017` replace visible presentation; HDR can remain non-visible lighting data. | Panorama reference only; not a mesh target. |
| 2 | Procedural glow-tip anemones and urchins | Prefer `anemone_story.glb` and `urchin_story.glb`; procedural geometry remains fallback-only. | Batch 01 joined Mobile meshes are wired and pending gameplay screenshot QA. |
| 2 | Procedural giant fish and slide-arena grass stand-in | Prefer `giant_fish_story.glb`; foliage remains covered by leaf/grass family references. | Batch 01 animated whale is wired; foliage card/clump conversion remains. |
| 2 | Kart finish checker, boost strips, and generic hazards | Batch 04 candidate `021`; split into separate runtime motifs. | Convert shell/hazard clusters into simple modular meshes only after material split. |

## Replacement rules now in force

1. Every score-2-or-lower visual gets one of four explicit dispositions:
   protected source, retire/fallback, routed to an existing stronger mesh, or
   staged new artwork with a named owner and conversion gate.
2. A generated 2D image is never counted as a finished 3D replacement. It must
   retain a role name, anatomy check, silhouette check, palette check, and
   collision/animation note before mesh work begins.
3. Multi-item sheets are references only until each item is split and named.
   Christmas remains an empty tree board plus five detachable ornaments.
4. Props stay non-character unless the source art explicitly gives them a
   face. Coral, anemones, urchins, rocks, and hazards must not gain invented
   expressions during generation.
5. All future mesh candidates use the 3D conversion manifest and must pass a
   Mobile-render screenshot review at gameplay distance before promotion.

## Open work after institution

The <=2/5 inventory is now covered by a replacement or disposition, but several
items still need implementation work: splitting and wiring of multi-item sheets,
terrain and sky presentation, source-faithful protected-character modeling, and
Mobile screenshot review of the five Batch 01 meshes.
These are deliberately tracked as conversion gates rather than silently marked
complete by the presence of a generated PNG.
