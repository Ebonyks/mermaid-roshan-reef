# Mermaid Roshan Art Style Audit

_Audit date: 2026-07-13_

_Standard: `ART_STYLE_GUIDE.md`, source-art edition_

## Executive finding

The project has a strong visual heart but an uneven perimeter.

- The protected book art, friend cutouts, app icon, Roshan turnarounds, painted
  terrain, and most GEN2 reef props are clear fits at 4-5.
- The normal reef path is substantially more coherent than the rest of the game
  because it selects GEN2 creatures and props, then adds cel bands and a navy
  outline.
- The weakest visible art is the 2D minigame set, the old aquatic pack when it is
  loaded directly by the kart and Butterfly World, photoreal sky HDRs, and a few
  procedural or generic pack stand-ins.
- The largest problem is consistency between modes, not a lack of good art. The
  same coral role can score 4 in the reef and 2 in the kart because the kart
  bypasses the GEN2 replacement path.
- The painted terrain family is close to the target, but several tiles contain
  baked shells, flowers, pebbles, or leaf clusters. That conflicts with the
  blank-canvas rule because the game also places those objects as 3D props.

The highest-return work is therefore to route every mode through the same asset
selection and rendering path, then replace the small set of 1-2 point art.

## Scope and method

This audit covers all runtime-facing visual asset families currently present in
`assets/`, plus important procedural art built by scripts. It excludes audio,
shader source as code, `.import` metadata, generation variants outside `assets/`,
and maps that are not independently visible. A model's base-color, normal,
roughness, metallic, and emissive maps inherit the model's score unless a map is
called out separately.

Every name in a grouped row receives that row's score. Grouping is used only when
the items share the same source, treatment, and finding.

The audit used:

- all 34 pages of the owner-supplied source PDF;
- the final raster assets and model textures in `assets/`;
- existing creature, craft-creature, and penguin QA renders;
- Roshan and Fairy turnaround sheets;
- runtime path inspection in `main.gd`, `player.gd`, `kart.gd`, `galaxy.gd`, and
  the extracted arena/game scripts;
- prior GEN2 curation notes as provenance, not as final style scores.

No Godot or Blender executable is available in this environment. Model ratings
are based on existing QA renders, approved turnarounds, final albedo atlases, and
the runtime material path. Scene-level judgments should be confirmed with Mobile
renderer screenshots before an art replacement is merged.

## Rating scale

| Score | Meaning | Default action |
|---:|---|---|
| 5 | Canonical fit; directly expresses the source language | Protect and reuse |
| 4 | Strong fit with a small polish or consistency gap | Keep; polish when touched |
| 3 | Mixed fit; works in context but visibly comes from another pipeline | Restyle or improve |
| 2 | Weak fit or obvious placeholder | Replace in a planned pass |
| 1 | Contradicts the guide or fails to depict its role | Replace first |

Scores measure style adherence, not sentimental value, gameplay value, ownership,
or technical correctness. Protected art is never modified solely to improve a
score.

## Core characters and protected 2D art

| Items | Score | Verdict and evidence |
|---|---:|---|
| `assets/book/baby_doll.png`, `baby_doll2.png`, `baby_doll3.png`, `baby_eagle.png`, `chuck_solo.png`, `doll_bunny.png`, `doll_cat.png`, `flower_girl.png`, `friendship_flower.png` | 5 | Direct source-art cutouts with the correct anime/storybook line, warmth, and readable silhouette. |
| `assets/book/gabby_stage.jpg`, `lake_winter.jpg`, `nursery_bg.jpg`, `kareem_shop.jpg` | 5 | Direct source scenes; these are compositional anchors for future environments. |
| `assets/book/hall/glass_mermaid.png`, `p_flower.jpg`, `p_gabby.jpg`, `p_garden.jpg`, `p_seattle.jpg`, `p_slide.jpg`, `p_snowman.jpg`, `p_trampoline.jpg`, `p_xmas.jpg` | 5 | Direct source-page and stained-glass art. Correctly displayed as unshaded pictures. |
| `assets/characters/friends/daddy.webp`, `flower_friend.png`, `gabby.png`, `huluu.png`, `kareem.png`, `mama_baby.png`, `pearl_friend.png`, `two_friends.png`, `wacky_chuck.png` | 5 | Protected character identity and family likeness. These are canonical even where illustration treatment varies between characters. |
| `assets/characters/roshan_sprite.png`, `roshan_0.png`, `roshan_tex_2k.webp` | 5 | Canonical Roshan color, face, hair, rainbow forelock, and tail reference. |
| `assets/characters/skins/fairy_mermaid.png`, `fairy_wing_card.png`, `fairy_fairy_mermaid.png` | 5 | Direct style derivative with the correct rainbow, lavender, and wing language. |
| `assets/characters/stickers/daddy.png`, `flower_friend.png`, `gabby.png`, `huluu.png`, `kareem.png`, `mama_baby.png`, `pearl_friend.png`, `two_friends.png`, `wacky_chuck.png` | 4 | Strong source identity. The thick white rim conflicts with normal-world art rules, but is justified inside the explicitly sticker-book UI. Keep the rim confined to that context. |
| `assets/icon/adaptive_bg_432.png`, `adaptive_fg_432.png`, `icon_192.png` | 5 | Canonical Roshan on a clean lagoon-cyan field; excellent small-screen identity. |

Protected-size exceptions: seven current images are NPOT and larger than 1024,
including source book scenes, Huluu art, and Roshan source textures. They predate
the new-texture rule and must not be recompressed or resized without owner
approval. Treat them as protected exceptions, not remediation targets.

## 3D characters and skins

| Item | Runtime role | Score | Verdict and evidence |
|---|---|---:|---|
| `assets/characters/roshan_v4.glb` | Default Roshan | 4 | Correct source-derived silhouette, identity colors, rig, two-arm fix, toonification, and latest hair/arm polish. Still needs a Mobile screenshot comparison for face planes, ink weight, and tail-seam continuity before it can be a 5. |
| `assets/characters/roshan_v3.glb` | First fallback | 3 | Strong source palette, but the fused/unrigged left-arm history is a major silhouette and motion mismatch. |
| `assets/characters/roshan_v2.glb` | Second fallback | 3 | Source-derived, but the over-the-shoulder head twist weakens neutral gameplay readability. |
| `assets/characters/roshan.glb` | Legacy fallback | 2 | Plush/flat-relief sculpt conflicts with the guide's clean illustrated 3D translation. Keep only as emergency fallback. |
| `assets/characters/fairy_v2.glb` | Fairy playable skin | 4 | Approved source turnaround, shared rig, strong rainbow/lavender identity. Needs the same in-engine outline and tail-seam confirmation as Roshan V4. |
| `assets/characters/fairy.glb` | Legacy fallback | 2 | Plush-era model and no longer the preferred skin path. |
| `assets/characters/huluu.glb` | Castle throne NPC | 2 | Preserves recognizable color, but is a static plush-like statue with no skeleton. This is one of the clearest character-style mismatches in normal play. Use the protected cutout until a source-faithful 3D model exists. |
| `assets/characters/lamb.glb` | Hide-and-seek Lamb-a' | 3 | Friendly, rounded, and readable, but generic and static compared with the protected paired illustration. |
| `assets/characters/chuck_poodle_rigged.glb` | Fetch-game Chuck | 3 | Correct subject and useful animation, but the dark furry/model-generated treatment is less flat, bright, and inked than the book-art world. |
| `assets/characters/chuck_poodle.glb`, `chuck_poodle_slim.glb` | Non-selected/probe variants | 2 | Legacy sculpts without the final runtime animation treatment. Do not promote them. |

Associated extracted atlases such as `roshan_v2_Baked_BaseColor.jpg`,
`roshan_v3_Baked_BaseColor.jpg`, `roshan_v4_Baked_BaseColor.jpg`,
`fairy_v2_Image_0.jpg`, and the Chuck texture maps inherit their model score.

## Current GEN2 reef art

### Creatures

These are the preferred `assets/props/gen2/*.glb` paths selected by
`CREATURE_GEN2` in the main reef.

| Items | Score | Verdict and evidence |
|---|---:|---|
| `turtle.glb`, `stingray.glb` | 5 | Best 3D match in the creature set: friendly silhouette, large decorative color blocks, source-like ornament, pastel palette, and readable movement. |
| `clownfish.glb`, `shark.glb`, `hammerhead.glb`, `squid.glb`, `octopus.glb`, `lobster.glb`, `crab.glb` | 4 | Strong rounded storybook forms and restrained broad color regions. Navy outline and cel runtime bring them close to target. Minor gaps are smooth generated surfaces and inconsistent painted line detail. |
| `dolphin.glb`, `whale.glb`, `penguin.glb` | 3 | Friendly and correctly colored, but too smooth, lightly detailed, or washed in existing QA renders. They need clearer eyes, stronger local-color separation, and a dependable ink contour. |
| `assets/aquatic2/ClownFish.glb`, `Crab.glb`, `Dolphin.glb`, `Hammerhead.glb`, `Lobster.glb`, `Octopus.glb`, `Shark.glb`, `Squid.glb`, `StingRay.glb`, `Turtle.glb`, `Whale.glb` | Same as matching creature | Duplicate/fallback packaging of the same GEN2 creature art. It is not the preferred main-reef path. |

### Reef props

| Items | Score | Verdict and evidence |
|---|---:|---|
| `coral.glb`, `coral1.glb`, `coral2.glb`, `coral3.glb`, `coral4.glb`, `coral5.glb`, `coral6.glb` | 4 | Family-style generated color and rounded silhouettes. Some face-like details are an owner-approved charm choice; keep them sparse so scenery does not become a crowd of characters. |
| `rock.glb`, `rock1.glb`, `rock2.glb`, `rock3.glb`, `rock4.glb`, `rock5.glb`, `rock_largea.glb` | 4 | Broad toy-like masses and pastel planes. The clean round-two sources avoid most prior character/enmeshment problems. |
| `fanshell.glb`, `smallfanshell.glb`, `spiralshell.glb`, `sanddollar.glb`, `starfish.glb`, `sponge_barrel.glb`, `sponge_tubes.glb` | 4 | Clear, oversized, child-readable prop silhouettes with good shell/coral color. |
| `seagrass.png`, `kelp.png` | 5 | Excellent graphic edge, colored line, controlled palette, and readable plant gesture. These should be the reference for new foliage cards. |
| `grasstuft.png`, `clownfish_side.png`, `starfish_decal.png`, `butterfly1.png`, `butterfly2.png` | 4 | Strong functional 2D derivatives. The clownfish and starfish are slightly flatter/simpler than source art but fit at gameplay scale. |

### GEN2 playground and nature models

| Items | Score | Verdict and evidence |
|---|---:|---|
| `play_horse.glb`, `play_merry.glb`, `play_sandbox.glb`, `play_seesaw.glb`, `play_slide.glb`, `play_swing.glb` | 4 | Correct recognizable-playground rule, broad toy forms, generated palette, cel+outline path, and gentle ambient motion. |
| `tree_fall.glb`, `tree_fall2.glb`, `tree_fat.glb`, `tree_palm.glb`, `tree_pineroundf.glb` | 4 | Rounded grouped canopies and readable silhouettes. A dedicated leaf texture would lift these to 5. |
| `craft_kitty_rigged.glb`, `craft_birdie_rigged.glb` | 3 | Cute, readable, animated, and based on her craft creatures, but current QA renders are materially dark and model-like. Verify the live recolor shader; target brighter albedo and cleaner contour. |
| `craft_kitty.glb`, `craft_birdie.glb` | 3 | Same style finding as the rigged versions, with less expressive motion. Keep only as fallback. |

## Cross-mode aquatic regression

The logical reef roles above are not used consistently.

| Context and items | Score | Finding |
|---|---:|---|
| Main reef `Coral`, `Coral1-6`, `Rock`, `Rock1-11`, `FanShell`, `SmallFanShell`, `SpiralShell`, `SandDollar`, `StarFish` | 4 | `AQ_GEN2` redirects them to painted GEN2 models with cel+outline. |
| Main reef `ClownFish`, `Turtle`, `Dolphin`, `Shark`, `Hammerhead`, `Whale`, `StingRay`, `Squid`, `Penguin`, `Octopus`, `Lobster`, `Crab` | 3-5 | `CREATURE_GEN2` redirects them to the scored models above. |
| Kart `Coral`, `SeaWeed`, `Coral1`, `Rock3`, `Coral2`, `SeaWeed1`, `FanShell`, `Coral3`, `Rock7`, `Coral4`, `SeaWeed2`, `SpiralShell`, `Coral5`, `Rock9`, `Coral6`, `SandDollar` | 2 | Loaded directly from `assets/aquatic/` with no GEN2 substitution or `_toonify`. Generic legacy pack geometry/materials visibly break the shared style. |
| Kart `ClownFish`, `Dory`, `Tuna`, `Carp` | 2 | Also loaded directly from the legacy pack. They are animated but not source-style creatures. |
| Kart shell pickup `SpiralShell.glb` | 2 | Direct legacy path even though a stronger GEN2 spiral shell exists. |
| Butterfly World `Coral1-6` and `Rock2` | 3 | Direct legacy models, but `_fit_small()` applies `_toonify` and pastel tint. Better than the kart, still weaker than GEN2 geometry. |

All other legacy files in `assets/aquatic/` receive 2 as fallback/source-pack
art: `Carp.glb`, `ClownFish.glb`, `Coral.glb`, `Coral1.glb`, `Coral2.glb`,
`Coral3.glb`, `Coral4.glb`, `Coral5.glb`, `Coral6.glb`, `Crab.glb`,
`Dolphin.glb`, `Dory.glb`, `Eel.glb`,
`FanShell.glb`, `Hammerhead.glb`, `Lobster.glb`, `Octopus.glb`,
`Penguin.glb`, `Rock.glb`, `Rock1.glb`, `Rock2.glb`, `Rock3.glb`,
`Rock4.glb`, `Rock5.glb`, `Rock6.glb`, `Rock7.glb`, `Rock8.glb`,
`Rock9.glb`, `Rock10.glb`, `Rock11.glb`,
`SandDollar.glb`, `SeaWeed.glb`, `SeaWeed1.glb`, `SeaWeed2.glb`, `Seal.glb`,
`Shark.glb`, `SmallFanShell.glb`, `SpiralShell.glb`, `Squid.glb`,
`StarFish.glb`, `StingRay.glb`, `Tuna.glb`, `Turtle.glb`, and `Whale.glb`.
Keep them only while a verified gameplay fallback is required; do not use new
direct paths to this family.

## Terrain and surface art

| Items | Score | Verdict and evidence |
|---|---:|---|
| `backdrop_seamounts.jpg` | 5 | Excellent broad silhouette layers, indigo depth, aqua field, and quiet composition. A strong environment reference. |
| `up_cliff_col.jpg` | 5 | Broad illustrated rock planes, colored contours, restrained detail, and no baked prop clutter. |
| `up_marble_col.jpg` | 5 | Soft shell-like shapes and watercolor color variation; directly supports the castle/storybook language. |
| `gen2_water_col.jpg`, `up_water_col.jpg` | 4 | Graphic, bright, and source-compatible. Repetition and high swirl density keep them below 5 on large surfaces. |
| `up_castle_col.jpg`, `up_cliffwall_col.jpg`, `up_cobble_col.jpg`, `up_door_col.jpg`, `up_fabric_col.jpg`, `up_flagstone_col.jpg`, `up_roof_col.jpg`, `up_wood_col.jpg` | 4 | Strong painted family. Each is recognizable, high-key, and materially distinct. Roof uses broad rainbow color, so confine it to focal architecture. |
| `up_dirt_col.jpg`, `up_grass_col.jpg`, `up_sand_col.jpg`, `up_snow_col.jpg` | 3 | Attractive painting, but baked pebbles, leaves, flowers, shells, or decorative clusters conflict with the blank-canvas rule and may reveal repetition. |
| `up_snowsoft_col.jpg` | 3 | Functionally quiet and safe, but too low-information to share the illustrated texture language without supporting props. |
| Missing `up_rainbowroad_col.jpg`; procedural stripe fallback | 3 | Readable and joyful but mechanically uniform and more emissive/gamey than the source. Install a verified painted road tile or improve the fallback. |
| `grass.jpg` | 2 | Generic mottled green texture without the source linework or broad painted shape language. |
| `beachball.png` | 2 inventory / retired | Generic glossy RGB stripe texture remains for provenance but has no runtime consumer. The ball role now uses a matte pastel panel shader, provisionally 4/5. |
| `flower.png`, `flower2.png` | 2 | Flat geometric icons; useful at tiny size but not suitable as world-facing flora art. |
| `leaf.png` | 4 | Replaced by a broad illustrated tropical leaf isolated from the approved Batch 04 family. It retains alpha-safe crossed-card behavior and colored linework. |
| `polyp.png` | 3 | Delicate illustrated repeat, but dense micro-detail can become noise on phone-size coral. |
| `scales.png` | 4 | Clear large graphic repeat that supports mermaid and creature identity. |
| `star_detail.png` | 3 | Decorative radial pattern is usable as a mask/detail, but should not become a visible material focal point. |
| `caustics.png` | 4 | Functional effect mask that produces a source-correct overlay when kept soft and slow. |

Normal and roughness partners inherit the score of their color family. Functional
maps such as `polyp_normal.png`, `scales_normal.png`, and `up_water_nrm.jpg`
are appropriate only at subtle strength, as required by the guide.

Two historical texture names still appear in code and documentation,
`Ground054_2K_Color.jpg` and `Rock061_2K_Color.jpg`, but their source images are
not present in the current workspace. Do not treat a local imported cache as a
style-approved asset; either remove the stale dependency or restore a documented
source in a separate functional task.

## Castle, park, furniture, nature, and ship packs

These ratings include the runtime `_toonify`, `_pastel`, and generated triplanar
texture treatment where present.

| Items | Score | Verdict and evidence |
|---|---:|---|
| `assets/castle/bed.glb`, `throne.glb` | 4 | Recognizable oversized furniture with painted fabric/wood sheets. Slightly generic geometry, but strong material integration. |
| `assets/kits/play/merry_go_round.glb`, `sandbox_round_decorated.glb`, `seesaw_large.glb`, `slide_A.glb`, `spring_horse_A.glb`, `swing_A_large.glb` | 4 in main path | `_kit()` redirects these roles to the GEN2 playground models. Raw kit files alone score 3. |
| `assets/kits/castle/flag.glb`, `tower-base.glb`, `tower-square.glb`, `tower-square-base.glb`, `tower-square-mid.glb`, `tower-square-top-roof-high.glb`, `tower-top.glb`, `wall.glb`, `wall-narrow-gate.glb` | 3 | Good toy geometry and strong readability, but shared generic colormaps and limited painted variation make the castle look kit-built. |
| `assets/kits/furniture/bookcase.glb`, `chair.glb`, `table.glb` | 3 | Clear function and safe proportions, but generic unillustrated forms. |
| `assets/kits/park/bench.glb`, `fountain.glb`, `hedge_straight.glb`, `hedge_straight_long.glb` | 3 | Friendly low-poly forms with pastel restyle, but still visibly a separate Tiny Treats material family. |
| `assets/nature/tree_default_fall.glb`, `tree_simple_fall.glb`, `tree_fat.glb`, `tree_palm.glb` | 4 in main path | Redirected to GEN2 trees through `NATURE_GEN2`. Raw Kenney files score 3. |
| `assets/nature/plant_bush.glb`, `grass_leafsLarge.glb` | 3 | Pastel-compatible geometry, but both wear lawn texture as a leaf stand-in. This is the highest-priority nature material gap. |
| `assets/nature/cliff_block_rock.glb`, `cliff_large_rock.glb`, `rock_largeA.glb` | 3 | Broad readable geometry, but generic kit forms unless replaced by GEN2 rock roles. |
| `assets/nature/flower_purpleA.glb`, `flower_redA.glb`, `flower_yellowB.glb`, `mushroom_red.glb`, `mushroom_tanGroup.glb`, `plant_bushLargeTriangle.glb`, `tree_pineRoundF.glb` | 3 | Friendly and readable after pastel tint, but raw pack colors and forms are less illustrated than the source. |
| `assets/ship/barrel.glb`, `chest.glb`, `cliff_cave_rock.glb`, `ship-ghost.glb`, `ship-wreck.glb` | 3 | Excellent silhouette storytelling and toy-scale geometry, but still generic Kenney props with limited source-specific painting. Ship ghost/wreck should avoid dark horror staging. |

## Butterfly World and kart assets

| Items | Score | Verdict and evidence |
|---|---:|---|
| `assets/portal/butterfly_gate.glb` with GEN2 butterfly cards | 4 | Painted pearl ring, graphic wings, and recognizable portal silhouette fit the guide well. |
| `assets/galaxy/tray.glb` | 4 | Painted wood texture gives a generic model a convincing storybook surface. |
| `assets/galaxy/crystal1.glb`, `crystal2.glb`, `crystal3.glb`, `crystal_castle.glb` | 3 | Clear magical silhouettes and good tinting, but procedural/glassy material lacks the painted facet language. |
| `assets/galaxy/butterfly1.glb`, `butterfly2.glb` | 2 | One retains photo-like monarch wing texture and both belong to a different model family. Replace wings with the proven GEN2 card art. |
| `assets/galaxy/fruit_apple.glb`, `fruit_banana.glb`, `fruit_melon.glb`, `fruit_orange.glb` | 3 | Readable and friendly at small scale, but raw pack skins are not painted source-style fruit. |
| `assets/galaxy/beetle.glb`, `ladybug.glb` | 3 | Simple and readable after tint, but tiny generic textures and glossy jewel treatment are only a partial fit. |
| `assets/galaxy/trop_palm1.glb`, `trop_palm2.glb`, `trop_monstera.glb`, `trop_bigleaf.glb`, `trop_fern.glb` | 3 | Broad plant silhouettes fit; repeated lawn/wood sheets do not describe leaves correctly and create material sameness. |
| `assets/vehicles/motorcycle.glb`, `gokart.glb` | 3 | Rounded and child-readable, with useful paint customization. Geometry and stock surfaces remain generic rather than Mermaid Roshan-specific. |
| `assets/vehicles/monstertruck.glb` | 2 | Generic rover/monster-truck form and atlas; heavy, mechanical silhouette does not share the rounded illustrated vehicle language. |
| Rainbow paint shader | 2 | `ROUGHNESS=0.15` and `METALLIC=0.5` make the result glossy/metallic, directly conflicting with the matte-to-satin guide. Keep the rainbow but remove the chrome-like response. |

## 2D minigame and craft art

This is the least coherent family. It mixes source cutouts, monochrome generated
line art, flat vector placeholders, shaded spheres, and glossy ornaments.

| Items | Score | Verdict and evidence |
|---|---:|---|
| `bird_body.png`, `bird_accent.png`, `bird_line.png` | 2 | The body/accent are grayscale transformations of protected Baby Eagle and the nominal line layer is blank. Readable, but not a valid three-zone source-art translation. Replacement requires owner-approved separation from the canonical art, not auto-redesign. |
| `cat_body.png`, `cat_accent.png`, `cat_line.png` | 1 | Confirmed owner rejection. Plush-style full render is duplicated across paint zones and the line layer is blank, so it fails both style and customization readability. Hard no for auto-generation: replace only from the child's real toy source. |
| `fish_line.png`, `fish_body.png`, `fish_fins.png` | 4 | Registered illustrated craft composite with independent body and fin colors. This is not core book art: all three layers may be redeveloped together if a stronger complete fish preserves the customization contract. |
| `snowman.png` | 5 | Direct source-art derivative and the strongest picture-game asset. |
| `seed.png` | 3 | Simple, readable, and warm, but visually plain. |
| `carrot.png` | 5 | Direct source-book component. Preserve it; the earlier placeholder classification was incorrect. Source-derived art outranks surface-level stylistic uniformity. |
| `butterfly.png` | 3 | Paired wing-shape animation component, not a standalone butterfly illustration. It is functional but needs an explicit body/wing-layer contract before replacement; do not judge or regenerate it as a single finished sprite. |
| `wateringcan.png` | 5 | Direct book-derived garden prop. Preserve the source art; it is not a replacement candidate even though neighboring minigame icons are weak. |
| `coal.png`, `flower.png`, `flower2.png`, `flower3.png`, `flower4.png`, `k_bush.png`, `k_flower1.png`, `k_flower2.png`, `k_pine.png`, `k_sprout.png`, `k_xmastree.png`, `sprout.png`, `star.png`, `sun.png`, `tree.png`, `xtree.png` | 2 | Functional flat vector placeholders with weak linework and inconsistent proportions. Rebuild as one cel-illustrated icon family, preserving simple silhouettes and animation-layer requirements. Confirmed direct book art is excluded from this replacement group. |
| `k_bush2.png` | 1 | Does not read as a bush; it resembles an orange cone/flame and fails role recognition. Replace first. |
| `orn1.png`, `orn2.png`, `orn3.png`, `orn4.png`, `orn5.png` | 2 | Inconsistent mix of glossy shaded spheres and flat geometric ornaments. Replace as a single painted set. |
| `rainbow_swatch.png` | 4 | Fin-shaped matte spectrum control is now live and displayed without aspect distortion. |

## Sky, UI, effects, and procedural art

| Item/family | Score | Verdict and evidence |
|---|---:|---|
| `assets/sky/lagoon_day_2k.hdr`, `lagoon_dusk_2k.hdr` | 2 inventory / retired | The photoreal files remain licensed inventory but no longer drive the visible lagoon. Seamless illustrated day/dusk color bands now serve the runtime role at provisional 4/5. |
| Bubble columns, drifting bubbles, marine snow | 4 | Correct recurring source motif and gentle motion. Keep sparse around faces and touch targets. |
| Caustic plane and surface caustics | 4 | Correct geometry-preserving magic overlay. Existing use matches the guide when opacity remains low. |
| Sparkle bursts and four-point stars | 4 | Correct source punctuation and child-readable success feedback. |
| Wind streaks and water surface rings | 4 | Graphic motion language supports the cel world without replacing local color. |
| Pearl pickups and shell/flower objective beacons | 4 | Warm focal accents and oversized shapes work well for a non-reader. |
| Procedural glow-tip anemones and urchins | 2 | Generic emissive primitives, repeated heavily, and one of the most visible remaining non-source families. Replace with GEN2 painted models/cards. |
| Procedural giant silhouette fish and slide-arena grass bunch | 2 | Functional stand-ins without the source's line, color, or silhouette personality. |
| Box/cylinder castle and arena architecture | 3 | Quiet toy-playset masses and readable layout, but lacks the hand-shaped taper and illustrated surface variation needed for 4-5. |
| HUD panels, labels, touch controls, sticker toast | 3 | High contrast and readable, with useful indigo/plum outlines, but styling is inconsistent between modes and often uses heavy black text outline. A dedicated UI art pass is warranted. |
| Kart finish checker and ramp cue | 4 | Shell-tied checker banner, navy/cream ground checks, matte posts, and an aqua/coral/lavender motion ribbon now serve the live roles. Candidate rock clusters were rejected as hazards because their reward symbols would confuse gameplay. |

## Priority remediation plan

### P0 - Remove the visible 1-2 point breaks

1. Route kart `OCEAN_PROPS`, `OCEAN_FISH`, and shell pickups through the same
   GEN2 role functions used by the main reef.
2. Route Butterfly World coral and rock decoration to GEN2 models instead of
   direct legacy aquatic paths.
3. Replace `assets/mg/k_bush2.png` and rebuild the picture-game vector set as a
   single outlined, softly painted family.
4. Replace the visible photoreal HDR sky presentation with painted sky art.
5. Retire the static plush `huluu.glb` from the throne scene; use her protected
   cutout until a source-faithful, rigged model is approved.
6. Replace procedural anemones, urchins, giant fish, and the grass stand-in with
   generated family-style art.

### P1 - Unify the remaining 3 point families

1. Generate one dedicated tropical leaf/frond sheet and rebake the tropical and
   nature plants currently wearing lawn texture.
2. Replace galaxy butterfly wings with the existing GEN2 butterfly cards.
3. Paint a coherent fruit-skin family and a translucent painted crystal-facet
   material.
4. Restyle the vehicle liveries and change the rainbow shader from metallic/glossy
   to matte-to-satin.
5. Give castle kits, furniture, park props, and ship props a shared painted trim,
   wood, stone, and metal vocabulary rather than generic pack colormaps.
6. Review Roshan V4, Fairy V2, Chuck, kitty, and birdie in Mobile screenshots for
   line weight, face readability, and local-color retention.

### P2 - Polish strong assets

1. Remove baked prop motifs from dirt, grass, sand, and snow tiles where they
   duplicate 3D dressing.
2. Tune water tiles to reduce obvious repetition over large surfaces.
3. Standardize dark ink to indigo/plum/brown instead of black across UI and 2D art.
4. Keep rainbow surfaces concentrated on identity and reward beats.
5. Add an art-screenshot probe for each major mode so style regressions are caught
   when a direct legacy path is introduced.

## Acceptance target

The next audit should meet all of these conditions:

- no runtime-facing item scores 1;
- no direct legacy aquatic model is visible in kart or Butterfly World;
- every major mode has a screenshot-reviewed median score of at least 4;
- Roshan, Fairy Roshan, Huluu, and Chuck are compared against protected references
  at gameplay distance under the Mobile renderer;
- all minigame art belongs to one outlined, softly painted icon family;
- no terrain tile duplicates a prop that is also placed in 3D;
- all new art is documented in `ASSET_LICENSES.md` and passes the project probes.
## 2026-07-14 remediation pass

The full below-4 inventory and replacement ledger are maintained in
`ART_REMEDIATION_BATCH_03.md`. The audit contains no 0/5 rows. The two 1/5
raster breaks, `assets/terrain/leaf.png` and `assets/mg/k_bush2.png`, now have
normalized review candidates. All raster-capable families below 4 also have
review candidates or exact-role reused candidates in
`assets_src/style_review_batch_03/replacement_candidates/`.

That review-only statement is superseded for the promoted families by
`ART_3D_BATCH_01.md`, `ART_3D_BATCH_02.md`, and
`ART_RUNTIME_REMEDIATION_BATCH_03.md`. Unpromoted candidates remain review art,
and no candidate is counted as fixed merely because a PNG exists.

## 2026-07-14 score-2-and-lower remediation pass

The global score-2-and-lower inventory and candidate ledger are maintained in
`ART_REMEDIATION_BATCH_04.md`. Batch 04 contains 22 generated finals, with 21
passing the new-art 4/5 gate and one provisional atlas candidate, including
raster candidates for terrain, minigame icons, layered fish art,
ornaments, sky presentation, procedural marine cards, kart motifs, and a
monster-truck atlas candidate. The
first urchin draft was rejected for inventing a face and was replaced by the
non-character `019_urchin_card_v2` candidate.

Approved candidates are promoted only through the model, layer-registration,
and gameplay-role gates recorded below. Protected book art, family cutouts, and
child-owned toys remain unchanged. Kart and Butterfly World prefer the GEN2
family, Huluu remains the protected source cutout, and rainbow paint is matte.
Unpromoted multi-item sheets remain reference art rather than runtime assets.

## 2026-07-14 full-art inventory closure

The complete directory-level coverage is now recorded in
`ART_FULL_INVENTORY.md`: 487 visual source files across the runtime art tree,
excluding audio and import metadata. Every score-2-or-lower family has an
explicit disposition: protected source art, retire/fallback, routed stronger
mesh, staged replacement candidate, or a named shader/material correction.

Future conversion of those candidates into meshes is tracked in
`ART_3D_CONVERSION_MANIFEST.md`. The manifest deliberately separates a 2D
concept from a finished model and records anatomy, silhouette, UV, rig,
collision, animation, Mobile screenshot, and licensing gates. No generated
concept is silently treated as a replacement for a model contract.

## 2026-07-14 Blender production Batch 01

`ART_3D_BATCH_01.md` records the first five local-Blender production meshes:
anemone, urchin, complete paired-wing butterfly, animated giant whale, and
rounded monster truck. Preferred runtime routes now use these models while the
old score-2 geometry remains missing-file fallback only. The whale explicitly
uses paired pectoral fins, one dorsal fin, and horizontal flukes; the butterfly
uses paired fore/hind wings and independent flap pivots.

The Blender QA renders pass a provisional 4/5 visual review, and structural
checks confirm 12,232 total triangles with no embedded raster images. Final
promotion remains gated on Godot Mobile import and gameplay screenshots because
no Godot binary is available in this environment. Protected book art, legacy
character models, family cutouts, and child-owned toys were not modified.

## 2026-07-14 Blender production Batch 02

`ART_3D_BATCH_02.md` records 21 editable Blender models rendered into 23
power-of-two picture-game sprites. This replaces the score-1/2 coal,
seed/sprout, flower, bush, tree, sun, star, and detachable ornament family
without changing any touch, growth-stage, or placement code.

The former 1/5 `k_bush2.png` now reads as a flowering shrub. The Christmas
tree no longer contains baked bulbs or a star before play begins: five separate
ornaments are placed by the child, followed by the protected friendship-flower
topper. Blender contact review scores the family provisionally at 4/5. Book
carrot, watering can, friendship flower, characters, cutouts, and child-owned
toys were not transformed.

## 2026-07-14 runtime remediation Batch 03

`ART_RUNTIME_REMEDIATION_BATCH_03.md` records the active-runtime continuation.
The broadleaf card, fin-shaped rainbow control, and registered fish body/fin
layers are now live. The glossy beach-ball texture and photoreal lagoon HDRs no
longer have runtime consumers; Mobile-safe matte panels and seamless illustrated
sky bands serve those roles. Kart uses the shell-tied finish banner and flowing
ramp ribbon. The candidate rock clusters were rejected as hazards because their
stars and shells already communicate rewards. The continuation audit also found
procedural manta geometry serving both ray and turtle roles; normal play now
routes those movers to the 5/5 GEN2 stingray and turtle models.
