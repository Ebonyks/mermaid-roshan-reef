# Asset license ledger (Phase 8 — complete table)

> **Project is freeware.** Strict CC0 is not required; any free-to-use asset is
> acceptable (owner direction, 2026-06-25). Book art, family photos and family
> voice recordings are **Original work © Mermaid Roshan LLC, all rights
> reserved** — never redistribute outside this project.
>
> Historical per-group audit + the CC0 swap manifest live in `ASSET_AUDIT.md`.
> Voice pipeline details live in `assets/audio/voices/VOICE_MANIFEST.md`.

| Path | Source | License | URL | Modifications |
|---|---|---|---|---|
| scripts/landmark_art.gd | Original project code-native artwork | project original | — | Runtime low-poly Dream Stars, Crown Star, Butterfly Gate, and storybook clouds; no external visual assets or protected book art used |
| backups/art_pre_landmarks_2026-07-15/** | Archival copies of previously licensed project assets | same licenses as live originals | — | Unmodified rollback copies; not loaded at runtime |
| assets/book/** (incl. hall/) | Mermaid Roshan storybook scans | **Original work © Mermaid Roshan LLC, all rights reserved** | — | cropped/resized for in-game frames |
| assets/characters/friends/* | book character art (family) | **© Mermaid Roshan LLC, all rights reserved** | — | background removal only — SACRED, never restyle |
| assets/characters/huluu.glb, lamb.glb | plushie meshes generated from the book art (tools/build_plushie.py) | derivative of © book art — all rights reserved | — | silhouette-extruded, rigged |
| assets/characters/roshan_sprite.png, roshan_tex_2k.webp, lamb_0.png, skins/* | book-art derivatives | © Mermaid Roshan LLC, all rights reserved | — | palette/skin variants |
| assets/ui/boot_splash_mermaid_roshan.png | OpenAI built-in image generation using project-owned Mermaid Roshan character references and approved project environment/style art | **Project-generated derivative of (c) Mermaid Roshan LLC - all rights reserved** | assets_src/imagegen/boot_splash_2026-08-01/PROMPTS.md | Selected Rainbow Bridge candidate; native 1672x941 full frame normalized as one whole canvas to 1024x576 PNG; no protected original modified or overwritten; generated 2026-08-01 |
| assets_src/imagegen/boot_splash_2026-08-01/** | OpenAI built-in image-generation candidates plus non-destructive project-reference boards and derived review contact sheet | **Project-generated review/source art; protected character sources remain (c) Mermaid Roshan LLC - all rights reserved** | assets_src/imagegen/boot_splash_2026-08-01/README.md; assets_src/imagegen/boot_splash_2026-08-01/PROMPTS.md | Three native full-frame candidates, selected/rejection audit, exact prompts, hashes, and reference layouts; review/source only under assets_src; no protected original changed; generated 2026-08-01 |
| assets/audio/voices/daddy1-3.ogg, chuck*.ogg | family recordings (+ Pixabay dog bark, see below) | **© family / Pixabay Content License** | pixabay.com | trim + loudnorm — SACRED |
| assets/audio/voices/voice_yay.mp3 | floraphonic via Pixabay | Pixabay Content License | pixabay.com | none — SACRED |
| assets/audio/voices/* (all other lines) | Kokoro-82M neural TTS (Apache-2.0 model), lines written for this project | synthesized output, owned by project | huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX | pitch/tempo/loudnorm per VOICE_MANIFEST.md |
| assets/audio/voices/chuck_whimper.ogg | original numpy synthesis | project original | — | -16 LUFS |
| assets/audio/music/world, world_night, level2, hall, home (.ogg) | Juhani Junkala JRPG Packs 1/2/4 | **CC0** | opengameart.org/content/jrpg-pack-1-exploration (+pack-2-towns, +pack-4-calm) | -18 LUFS loudnorm |
| assets/audio/music/* (finale + minigame stingers) | synthesized for this project | project original | — | — |
| assets/audio/music/castle_{opera_hall,kitchen,library,playroom,craft_room,mermaid_pool,bubble_bath,dining_room,royal_bedroom,sleepover_bedroom,movie_lounge,family_gallery}.ogg; assets/audio/music/opera_*.ogg; assets/audio/music/{northern,galaxy,ember,dungeon_ice,dungeon_ember,combat_ice,combat_fire,combat_tutorial,stuffie_battle,picture_snowman,picture_garden,picture_trampoline,picture_xmas}.ogg | `assets_src/audio/music/area_music_scores.json` + deterministic project renderer `tools/build_area_music.py`; provenance in `assets/audio/music/area_music_manifest.json` | **project-owned original composition and synthesis** | — | 42 unique 24–40 s integer-bar loops; 48 kHz stereo; -18 LUFS; managed Vorbis 96k target / 80k floor; sample-exact loop, BPM, meter, and cue tags; no samples, soundfonts, downloads, network services, protected voices, or protected art used |
| assets/audio/ambience_*.ogg, ui_tap.ogg | original numpy synthesis | project original (CC0-equivalent) | — | seamless loops |
| assets/audio/buy, buzz, chime, fart (.ogg) | synthesized for this project | project original | — | — |
| assets/audio/hop_boing.ogg | original numpy synthesis (pitch-wobbled decaying twang) | project original | — | 0.5s one-shot, quiet-normalized for per-hop playback |
| assets/aquatic/*.glb | Riley *Aquatic Animal Models* (itch.io) | **"free use, no redistribution"** — see OPEN QUESTION below | itch.io | integrated as-is; Rock2 re-textured with project nano-banana sheets (tools/bake_nano_wrap.py, 2026-07-12) |
| assets/terrain/up_*_rgh.jpg (roughness maps only) | ambientCG | **CC0** | ambientcg.com | resized ≤1K |
| assets/terrain/up_*_col.jpg (all 13 roles) | GEN2 pipeline: family-style painted tiles (Gemini; audit picks; castle re-generated r3 as a proper wall) | © Mermaid Roshan LLC — generated for this project | gen2/generated/terrain_up_*/ | 2048→1024 POT, JPEG q88; matching _nrm.jpg flattened to neutral 64px |
| assets/terrain/caustics.png, scales*, polyp*, flower*, leaf, beachball, star_detail (.png) | painted/generated for this project | project original | — | — |
| assets/terrain/castle_floor_col.jpg, assets/terrain/castle_carpet_col.jpg | OpenAI ChatGPT image generation guided by `ART_STYLE_GUIDE.md` and the Level 2 castle audit | **Project-generated art** | - | seamless quiet lavender stone and deep berry woven runner; 1254 to 1024 POT, JPEG q90; generated 2026-07-15 |
| assets/terrain/kitchen_floor_col.jpg, assets/terrain/kitchen_wood_col.jpg, assets/terrain/kitchen_counter_col.jpg | OpenAI ChatGPT image generation guided by `ART_STYLE_GUIDE.md` and the Royal Kitchen screenshot | **Project-generated art** | - | seamless pastel ceramic tile, painted honey wood, and shell-terrazzo surfaces; periodic 1254 to 1024 POT resample, JPEG q92; generated 2026-07-15 |
| gen2/generated/kitchen_counter/concept.jpg, gen2/generated/kitchen_sink/concept.jpg, gen2/generated/kitchen_stove/concept.jpg | OpenAI ChatGPT image generation guided by the Royal Kitchen screenshot and the approved kitchen wood/shell-terrazzo surfaces | **Project-generated art** | - | isolated orthographic-like modeling references; normalized to at most 1024px, JPEG q90; generated 2026-07-15 |
| assets/castle/kitchen_counter.glb, assets/castle/kitchen_sink.glb, assets/castle/kitchen_stove.glb | Project-authored Blender 4.4.3 geometry based on the approved image-generated kitchen concepts | **Project-generated art** | gen2/generated/kitchen_counter/concept.jpg, gen2/generated/kitchen_sink/concept.jpg, gen2/generated/kitchen_stove/concept.jpg | exact-size static meshes; 4,316 triangles total; named shared-material rig; no armature, animation, light, or physics body; generated 2026-07-15 |
| assets_src/blender/kitchen_props.blend, assets_src/blender/qa_kitchen_props/kitchen_counter.png, assets_src/blender/qa_kitchen_props/kitchen_sink.png, assets_src/blender/qa_kitchen_props/kitchen_stove.png | Project-authored Blender source and Workbench QA renders for the Royal Kitchen appliance set | **Project-generated source/review art** | tools/build_kitchen_props.py | editable source scene plus 900x700 material/bounds review renders; generated 2026-07-15 |
| assets/terrain/bathroom_tile_col.jpg | OpenAI ChatGPT image generation guided by `ART_STYLE_GUIDE.md`, the Royal Kitchen screenshot, and the approved shell-terrazzo fixture language | **Project-generated art** | - | seamless pastel rounded ceramic tiles with bubble/shell motifs; 1254 to 1024 POT resample, JPEG q92, VRAM-compressed with mipmaps; generated 2026-07-16 |
| gen2/generated/bathroom_bathtub/concept.jpg, gen2/generated/bathroom_sink/concept.jpg, gen2/generated/bathroom_toilet/concept.jpg, assets_src/blender/references/bathroom_bathtub_turnaround.png, assets_src/blender/references/bathroom_sink_turnaround.png, assets_src/blender/references/bathroom_toilet_art_turnaround.png | OpenAI ChatGPT image generation guided by the Royal Kitchen screenshot, approved fixture concepts, and the owner's earlier toilet artwork (used as reference but not redistributed) | **Project-generated art** | - | isolated concepts plus consistent multi-view modeling turnarounds; normalized to at most 1024px; generated 2026-07-16 |
| assets/castle/bathroom_bathtub.glb, assets/castle/bathroom_sink.glb, assets/castle/bathroom_toilet.glb | Project-authored Blender 4.4.3 geometry converted from the approved image-generated concepts and turnarounds | **Project-generated art** | assets_src/blender/references/bathroom_*_turnaround.png | exact-size static meshes; 27,995 triangles and 43 consolidated material-role nodes total; toilet rear skirt and molded S-trap corrected 2026-07-18; bespoke embedded surfaces with no kitchen texture reuse; zero near-degenerate faces at the Godot audit threshold; no armature, animation, light, or physics body |
| assets_src/blender/bathroom_bathtub_v2.blend, assets_src/blender/bathroom_sink_v2.blend, assets_src/blender/bathroom_toilet_v2.blend, assets_src/blender/qa_bathroom_props/*.png | Project-authored Blender sources, Eevee review renders, and in-game QA captures for the Royal Bathroom fixture set | **Project-generated source/review art** | tools/build_bathroom_props.py, tools/build_bathroom_bathtub_v2.py, tools/build_bathroom_sink_v2.py, tools/build_bathroom_toilet_v2.py, scripts/probe_bathroom_integration.gd | editable per-fixture source scenes, polished material renders, and live Level 2 placement captures; generated 2026-07-16; toilet source and isolated render revised 2026-07-18 |
| assets/castle/pearl_kit/*.glb | Project-authored Blender 4.4.3 pearl-castle architecture and furnishing kit guided by the source-book style guide and consolidated human/AI audits | **Project-generated art** | tools/build_pearl_castle_kit.py; CASTLE_PEARL_ART_AUDIT_2026-07-18.md | fifty-eight exact-size, texture-free Mobile props covering architecture, water and Opera thresholds, lighting, seating, non-plush toys, library, royal bedroom, seven playable music keys, varied provisions/storage, a remodeled pantry, craft, bath, non-plush keepsakes, and an opaque modeled Opera vista; one runtime mesh each; 560-5,768 triangles; generated and expanded 2026-07-18 |
| assets_src/blender/pearl_castle_kit.blend, assets_src/blender/qa_pearl_castle_kit/*.png, assets_src/blender/qa_pearl_castle_kit/runtime_*/*.png | Editable Blender source, isolated Eevee QA renders, and labeled Mobile runtime review evidence for the pearl-castle kit | **Project-generated source/review art** | tools/build_pearl_castle_kit.py; scripts/probe_castle_pearl_art.gd | complete deterministic source scene plus one 780x660 render per runtime GLB; rejected runtime captures retained outside runtime loading for comparison; generated 2026-07-18 |
| backups/art_pre_castle_pearl_2026-07-18/** | Byte-exact pre-pass toilet, source, QA render, hall script, and builder archive | **Same license as each archived source** | Git commit 9943f16; backups/art_pre_castle_pearl_2026-07-18/README.md | reversible ZIP with repository-relative paths and SHA-256 manifest; created 2026-07-18 |
| backups/art_pre_castle_visibility_2026-07-18/** | Rejected pearl-castle material-visibility source/runtime snapshot retained for direct rollback and review comparison | **Project-generated archive** | Git commit 50b1907; backups/art_pre_castle_visibility_2026-07-18/README.md | SHA-256 recorded full forty-nine-asset/source/code ZIP plus fifteen extracted prior runtime GLBs whose nested dark outline shells were superseded after Mobile review; excluded from runtime loading by backup path; archived 2026-07-18 |
| backups/art_pre_castle_opera_2026-07-18/** | Rejected primitive Opera gate source reference retained for direct visual rollback | **Project-generated archive** | Git commit 2227031; backups/art_pre_castle_opera_2026-07-18/README.md | documents the gold-box/crimson-panel/Label3D blockout superseded by the authored shell-theatre gate; excluded from runtime loading by backup path; archived 2026-07-18 |
| backups/art_pre_castle_final_polish_2026-07-18/** | Rejected `affb617` wardrobe and pantry runtime GLBs retained for direct rollback and review comparison | **Project-generated archive** | Git commit affb617; backups/art_pre_castle_final_polish_2026-07-18/README.md | SHA-256 recorded two superseded GLBs whose isolated renders were valid but failed runtime role/readability review; excluded from runtime loading by backup path; archived 2026-07-18 |
| assets/nature/*.glb | Kenney Nature Kit | **CC0** | kenney.nl | pastel-restyled at load (_toonify); plant_bush + grass_leafsLarge re-textured with project nano-banana sheets (tools/bake_nano_wrap.py, 2026-07-12) |
| assets/ship/*.glb | Kenney Pirate Kit | **CC0** | kenney.nl | pastel-restyled at load |
| assets/kits/castle/*.glb | Kenney Castle Kit | **CC0** | kenney.nl/assets/castle-kit | colormap embedded per piece (Blender re-export) |
| assets/kits/play/*.glb | Tiny Treats: Fun Playground (Isa Lousberg) | **CC0** | tinytreats.itch.io/fun-playground | gltf→glb (Blender) |
| assets/kits/park/*.glb | Tiny Treats: Pretty Park (Isa Lousberg) | **CC0** | tinytreats.itch.io/pretty-park | gltf→glb (Blender) |
| assets/kits/furniture/*.glb | Quaternius Ultimate Furniture | **CC0** | quaternius.com/packs/ultimatefurniture.html | FBX→glb (Blender) |
| assets/sky/lagoon_day_2k.hdr | "Qwantani (Pure Sky)", Poly Haven | **CC0** | polyhaven.com/a/qwantani_puresky | none (2K) |
| assets/sky/lagoon_dusk_2k.hdr | "Qwantani Dusk 2 (Pure Sky)", Poly Haven | **CC0** | polyhaven.com/a/qwantani_dusk_2_puresky | none (2K) |
| assets/shaders/toon_water.gdshader | based on "Toon Water" (godotshaders) | **CC0** base; project additions | godotshaders.com/shader/toon-water/ | pastel bands, sparkle, scrolling normals, Speedy toggle |
| assets/shaders/cel.gdshader, cel_post.gdshader, outline.gdshader | written for this project | project original | — | — |
| assets/characters/stickers/*.png | die-cut sticker bakes generated from the friend cutouts (tools, PIL) | derivative of (c) book art — all rights reserved | — | white vinyl rim + navy drop shadow; originals untouched |
| gen2/npc_src/*.png | Meshy submit sources derived from the friend cutouts (tools/prep_npc_sources.py, PIL) | derivative of (c) book art — all rights reserved | NPC_3D_WORKORDER_2026-07-19.md | alpha trimmed, white-carded, ≤1024; not imported (gen2 .gdignore) |
| assets/mg/*.png | drawn/generated for this project (PIL) from book-art motifs | © Mermaid Roshan LLC derivatives / project original | — | craft zone masks, minigame art |
| assets/sprites/stuffie_studio/display_shelf.png, assets/sprites/stuffie_studio/worktable.png, assets/sprites/stuffie_studio/toy_chest.png | OpenAI built-in image generation guided by the project's 2D storybook castle style | **Project-generated art** | — | isolated pearl-shell furniture cutouts for the six-slot display, care/upgrade table, and active-friend toy chest; chroma-key removed with the bundled ImageGen helper, edge-contracted once, and normalized to ≤1024px; generated 2026-07-28 |
| assets/sprites/stuffie_studio/lamma.png | OpenAI built-in image edit of the project-owned `assets/characters/lamb_0.png` design | **© Mermaid Roshan LLC derivative / project-generated edit** | assets/characters/lamb_0.png | faithful front-facing 2D runtime cutout replacing Lamb-a's retired GLB use; source left untouched, egg lettering removed, chroma-key removed, and normalized to 949×1024; generated 2026-07-28 |
| assets/props/gen2/*.glb | GEN2 pipeline: family-style art (Gemini, audited) → 3D (Meshy image-to-3D) | © Mermaid Roshan LLC — generated for this project | gen2/ (workorder, audit) | tools/shrink_glb.py: textures ≤1024, speculars stripped, shadow lift, albedo posterized to 8 flat PNG fills (WW look) |
| assets/props/gen2/*.png | GEN2 pipeline sprites (Gemini, audited), alpha-cut via tools/polish_sprite.py | © Mermaid Roshan LLC — generated for this project | gen2/ | white bg → alpha, tight crop |
| assets/props/gen2/seagrass.png | GEN2 pipeline: family-style sea grass sprite (Gemini, aquatic_seaweed2 v1, audit 9/10 clean) | © Mermaid Roshan LLC — generated for this project | gen2/generated/aquatic_seaweed2/ | polish_sprite.py alpha cutout, 892×735 |
| assets/props/gen2/starfish_decal.png | derived: top render of assets/props/gen2/starfish.glb (project Gemini+Meshy art) | project-owned | — | flat decal for the seabed scatter field |
| assets/props/gen2/clownfish_side.png | derived: side render of assets/props/gen2/clownfish.glb (project Gemini+Meshy art) | project-owned | — | sprite for the ambient school quads |
| assets/props/gen2/craft_kitty.glb | craft-studio kitty: HER book art (Gemini, doll_cat) → luma-neutralized source → Meshy image-to-3D + texture | © Mermaid Roshan LLC — generated for this project | Downloads/Meshy_AI_Whiskercorn_* | tools/import_craft_creature.py: decimate 309k→9k, textures ≤1024, normal/MR stripped; recolored in-game by the craft sway shader |
| assets/props/gen2/craft_birdie.glb | craft-studio birdie: HER book art (Gemini, baby_eagle) → luma-neutralized source → Meshy image-to-3D + texture | © Mermaid Roshan LLC — generated for this project | Downloads/Meshy_AI_Pufflet_* | tools/import_craft_creature.py: decimate 541k→9k, textures ≤1024, normal/MR stripped; recolored in-game by the craft sway shader |
| assets/props/gen2/craft_kitty_rigged.glb | craft kitty rigged: the kitty mesh on Chuck's 20-bone quadruped rig with idle/walk/run/happy clips | © Mermaid Roshan LLC — generated for this project | Downloads/Meshy_AI_Whiskercorn_* | tools/build_chuck_rig.py (rig) + tools/animate_kitty.py (clips), texture ≤1024, maps stripped; recolored in-game by the sway shader (sway_amount 0) |
| assets/props/gen2/craft_birdie_rigged.glb | craft birdie rigged: its own 12-bone standing-bird skeleton (two-bone legs + wing chains) with idle/walk/run/happy clips | © Mermaid Roshan LLC — generated for this project | Downloads/Meshy_AI_Pufflet_* | tools/rig_birdie.py (rig+clips, penguin-pipeline weights), texture ≤1024, maps stripped; recolored in-game by the sway shader (sway_amount 0) |
| assets/props/gen2/craft_kitty_mask.png, craft_birdie_mask.png | paint-zone masks baked from the rigged meshes (tools/bake_zone_mask.py) | project-owned | — | R/G/B = body/accent/detail. Baby Eagle uses named rig joints plus the embedded authored albedo to make whole wing/crest/breast cutouts; black = fixed features (horn, feet, beak). |
| assets/audio/penguin_giggle.ogg | synthesized squeak giggle (numpy, tools history 2026-07-12) | project-owned | — | baby penguin voice: escape burst, catch, portal greet |
| assets/terrain/up_cliffwall_col.jpg | nano-banana generation (gemini-3-pro-image, 2026-07-13, bare-stone regen same day) | project-owned | — | painted cliff-wall tile: terrain steep-slope blend; BARE stone by rule - 3D coral props decorate surfaces |
| assets/terrain/backdrop_seamounts.jpg | nano-banana generation (gemini-3-pro-image, 2026-07-13) | project-owned | — | seamount silhouette panorama: world-edge backdrop ring |
| assets/audio/purr.wav | synthesized cat purr (numpy: 55/110/165 Hz body, 25 Hz AM pulse, seamless 2s loop) | project-owned | — | craft kitty nuzzle loop; WAV not OGG (no vorbis encoder available in build env); loop set in code |

> **Retired provenance (owner decision 2026-08-09):** the Roshan GLB rows
> below are historical license records, not active asset paths or shipping
> recommendations. The exact v3/v4 models, raw Meshy bundles, textures,
> importer records, rig tools, and QA renders are preserved with checksum
> manifests on `codex/deprecated-resources-roshan-20260809` at `8d9c69b6`.
> Mermaid Roshan is 2D-only in the active game; restoring a model requires a
> new explicit owner decision.

| assets/characters/roshan_v4.glb | ROSHAN V5 replacement sculpt: owner-supplied Meshy rainbow mermaid generation → in-house 57-bone game rig | © Mermaid Roshan LLC — generated for this project | `Downloads/Meshy_AI_Rainbow_Mermaid_Princ_0716022221_texture.glb` (source SHA-256 `aeca483bd15d84b1c957ebfddd6ce8f55d3d8e27e44c593d169b93bd6baeefa`) | Source has both complete native hands and cohesive visible arm sculpts; `tools/shrink_glb.py` + `tools/_decimate_keep.py` reduce 409,082→39,999 triangles and both embedded maps to 1024²; `tools/fit_roshan_rig.py` fits/symmetrizes the 57-bone rig with analytic region weights and five topology-smoothing passes; `tools/rebuild_roshan_arm_surfaces.mjs` preserves every visible triangle and adds 728 narrow hidden safety triangles spanning torso→shoulder→elbow→wrist→palm; `tools/rebuild_roshan_hair_physics.mjs` replaces the temporary static-hair bind with eight monotonic three-bone chains weighted only to 7,745 texture-verified disconnected hair-lock vertices (no geometry or texture changes); `tools/smooth_shoulder_weights.py` harmonically re-solves the chest↔armU blend band (252 crease vertices, weights only — no geometry, joints, or textures) after the 2026-07-18 human review flagged shoulder stretching: worst arm-verb edge opening 0.073→0.056. Shipping total: 40,727 triangles; SHA-256 `bb758b98c1720615951131046598f87d1146ed473fd3a520222eaac9bcc47a5e` |
| assets/characters/roshan_v2.glb | ROSHAN V2: owner-spec turnarounds (Gemini) → Meshy multi-image i23d → weight transfer onto her original 26-bone rig | © Mermaid Roshan LLC — generated for this project | gen2/turnarounds/roshan_v2/, gen2/ROSHAN_V2_WORKORDER.md | shrink pass ≤1024, tools/roshan_v2_retarget.py |
| assets/characters/chuck_poodle_rigged.glb | CHUCK 3D: Meshy image-to-3D poodle → in-house 20-bone quadruped rig + 5 clips (sit_idle/sit_excited/run/pickup/wag), built headless in Blender (reef2/tools/build_chuck_rig.py + animate_chuck.py) | © Mermaid Roshan LLC — generated for this project | reef2/tools/, reef2/tools/out/chuck_rig.blend | glTF-Transform weld+simplify 603k→72k tris; proxy-bind weight transfer; 2048 POT textures |
| assets/characters/skins/fairy_wing_card.png | FAIRY V2 wing plate, cut from the Gemini turnaround back view | © Mermaid Roshan LLC — generated for this project | gen2/turnarounds/fairy_v2/back.png | polish_sprite alpha cut, largest-component + geometric cleanup |
| assets/terrain/up_door_col.jpg | GEN2 pipeline: storybook castle-door tile (Gemini; audit follow-up — wood read as the road on the door) | © Mermaid Roshan LLC — generated for this project | gen2/generated/terrain_up_door_col/ | 1024 POT JPEG q88; flat _nrm |
| assets/terrain/gen2_water_col.jpg | GEN2 pipeline: family-style painted water tile (Gemini, role terrain_up_water_col v1) | © Mermaid Roshan LLC — generated for this project | gen2/generated/terrain_up_water_col/ | downscaled 2048→1024 POT, JPEG q88 |
| assets/portal/butterfly_gate.glb | modeled in Blender for this project | project original | — | — |
| assets/castle/bed.glb | "Bed Single" by Kenney | **CC0** | poly.pizza/m/sn8az3odMR | re-textured with project nano-banana painted sheets (tools/bake_nano_wrap.py, 2026-07-12); geometry unchanged |
| assets/castle/throne.glb | "Throne" by Poly by Google | **CC-BY 3.0** (attribution: Poly by Google) | poly.pizza/m/bpFCWQSs-aT | re-textured with project nano-banana painted sheets (tools/bake_nano_wrap.py, 2026-07-12); geometry unchanged |
| assets/vehicles/motorcycle.glb | "Cartoony Purple Motorcycle" by AliceCassie | **CC0** | poly.pizza/m/j20srJUjpB | — |
| assets/vehicles/gokart.glb | "Go kart" by Poly by Google | **CC-BY 3.0** (attribution: Google/Poly) | poly.pizza/m/3hkutVs0AAV | — |
| assets/vehicles/monstertruck.glb | "Rover" by Quaternius | **CC0** | poly.pizza/m/WRd1piJOfh | used as Monster Truck |
| assets/galaxy/crystal1-3.glb | "Crystal" by iPoly3D | **CC0** | poly.pizza/m/3saqXqoOti +2 | — |
| assets/galaxy/butterfly1.glb, butterfly2.glb | "Butterfly" by Poly by Google | **CC-BY 3.0** | poly.pizza/m/e9NAQQrCbLu, /m/2ZwYwkTVnfG | — |
| assets/galaxy/fruit_apple.glb | "Apple" by jeremy | **CC-BY 3.0** | poly.pizza/m/4tOmpD9-xsV | — |
| assets/galaxy/fruit_banana.glb | "Banana" by Poly by Google | **CC-BY 3.0** | poly.pizza/m/ahOO6wz8sV0 | — |
| assets/galaxy/fruit_melon.glb | "Watermelon Half" by S. Paul Michael | **CC-BY 3.0** | poly.pizza/m/1exBmBVJHjj | — |
| assets/galaxy/fruit_orange.glb | "An Orange" by Ivan Kraft | **CC-BY 3.0** | poly.pizza/m/abyCKYOa770 | — |
| assets/galaxy/tray.glb | "Plate Oval" by MilkAndBanana | **CC0** | poly.pizza/m/06WhCScuAF | re-textured with project nano-banana painted sheets (tools/bake_nano_wrap.py, 2026-07-12); geometry unchanged |
| assets/galaxy/beetle.glb, ladybug.glb | by Poly by Google | **CC-BY 3.0** | poly.pizza/m/4yufxgZ1QQ2, /m/4K7V5f9ntfu | — |
| assets/galaxy/crystal_castle.glb | "Castle" by CreativeTrio | **CC0** | poly.pizza/m/4360GdbxRe | — |
| assets/galaxy/trop_palm1.glb | "Palm tree" by jeremy | **CC-BY 3.0** | poly.pizza/m/bjGeBbKhAVN | re-textured with project nano-banana painted sheets (tools/bake_nano_wrap.py, 2026-07-12); geometry unchanged |
| assets/galaxy/trop_palm2.glb | "Coconut palm tree" by Poly by Google | **CC-BY 3.0** | poly.pizza/m/bXUTyfiwqBb | re-textured with project nano-banana painted sheets (tools/bake_nano_wrap.py, 2026-07-12); geometry unchanged |
| assets/galaxy/trop_fern.glb | "Fern" by Quaternius | **CC0** | poly.pizza/m/jqcanvH7D6 | re-textured with project nano-banana painted sheets (tools/bake_nano_wrap.py, 2026-07-12); geometry unchanged |
| assets/galaxy/trop_monstera.glb | "Large Monstera Plant" by Isa Lousberg | **CC0** | poly.pizza/m/kZQ2WmnJFI | re-textured with project nano-banana painted sheets (tools/bake_nano_wrap.py, 2026-07-12); geometry unchanged |
| assets/galaxy/trop_bigleaf.glb | "Big Leaf Plant" by reyshapes | **CC0** | poly.pizza/m/aKIm5k6l5F | re-textured with project nano-banana painted sheets (tools/bake_nano_wrap.py, 2026-07-12); geometry unchanged |
| disabled_addons/tessarakkt.oceanfft | OceanFFT addon (disabled, .gdignore) | **MIT** | github.com/tessarakkt/godot4-oceanfft | dead code removed Phase 0 |

| assets_src/style_review_batch_02/** | OpenAI ChatGPT image generation, guided by `ART_STYLE_GUIDE.md` and book motif analysis | **Project-generated review art** | - | chroma-key removed; normalized to <=1024px; review-only, generated 2026-07-13 |
| assets_src/style_review_batch_03/** | OpenAI ChatGPT image generation and approved Batch 02 candidates, guided by `ART_STYLE_GUIDE.md` and the full below-4 audit | **Project-generated review art** | - | chroma-key removed where applicable; normalized to <=1024px; review-only, generated 2026-07-14 |
| assets_src/style_review_batch_04/** | OpenAI ChatGPT image generation and approved project references, guided by `ART_STYLE_GUIDE.md` and the score-2-and-lower audit | **Project-generated review art** | - | chroma-key removed where applicable; normalized to <=1024px; review-only, generated 2026-07-14 |
| assets/props/gen2/anemone_story.glb | Project-authored Blender 4.4.3 geometry based on the approved Batch 04 anemone concept | **Project-generated art** | - | rooted ten-tentacle mesh; joined and Mobile-decimated; embedded matte palette materials; generated 2026-07-14 |
| assets/props/gen2/urchin_story.glb | Project-authored Blender 4.4.3 geometry based on the approved Batch 04 urchin concept | **Project-generated art** | - | radial non-character mesh; joined and Mobile-decimated; embedded matte palette materials; generated 2026-07-14 |
| assets/props/gen2/butterfly_story.glb | Project-authored Blender 4.4.3 geometry based on approved complete-butterfly references | **Project-generated art** | - | complete paired fore/hind wings, antennae, and two flap pivots; embedded matte palette materials; generated 2026-07-14 |
| assets/props/gen2/giant_fish_story.glb | Project-authored Blender 4.4.3 geometry based on the approved Batch 04 giant-fish concept | **Project-generated art** | - | anatomical whale silhouette with paired pectoral fins, dorsal fin, horizontal flukes, and tail action; generated 2026-07-14 |
| assets/vehicles/monstertruck_story.glb | Project-authored Blender 4.4.3 geometry based on the approved style guide and monster-truck role | **Project-generated art** | - | rounded toy body, oversized wheels, matte embedded palette, no stock logos; generated 2026-07-14 |
| assets_src/blender/low_score_batch_01.blend | Project-authored Blender source for 3D Replacement Batch 01 | **Project-generated source art** | - | editable source scene for five production GLBs; generated 2026-07-14 |
| assets_src/blender/qa_low_score_batch_01/anemone_story.png | Blender Workbench QA render of project-authored Batch 01 geometry | **Project-generated review art** | - | transparent 900x700 visual QA render; generated 2026-07-14 |
| assets_src/blender/qa_low_score_batch_01/urchin_story.png | Blender Workbench QA render of project-authored Batch 01 geometry | **Project-generated review art** | - | transparent 900x700 visual QA render; generated 2026-07-14 |
| assets_src/blender/qa_low_score_batch_01/butterfly_story.png | Blender Workbench QA render of project-authored Batch 01 geometry | **Project-generated review art** | - | transparent 900x700 visual QA render; generated 2026-07-14 |
| assets_src/blender/qa_low_score_batch_01/giant_fish_story.png | Blender Workbench QA render of project-authored Batch 01 geometry | **Project-generated review art** | - | transparent 900x700 visual QA render; generated 2026-07-14 |
| assets_src/blender/qa_low_score_batch_01/monstertruck_story.png | Blender Workbench QA render of project-authored Batch 01 geometry | **Project-generated review art** | - | transparent 900x700 visual QA render; generated 2026-07-14 |
| assets/mg/coal.png, sprout.png, k_sprout.png, flower.png, flower2.png, flower3.png, flower4.png, k_flower1.png, k_flower2.png, k_bush.png, k_bush2.png, tree.png, k_pine.png, xtree.png, k_xmastree.png, sun.png, star.png, orn1.png, orn2.png, orn3.png, orn4.png, orn5.png | Project-authored Blender 4.4.3 models and orthographic renders guided by the approved Batch 04 concepts and `ART_STYLE_GUIDE.md` | **Project-generated art** | - | 512x512 RGBA; matte materials; navy Freestyle contours; existing runtime paths replaced in place; generated 2026-07-14 |
| assets_src/blender/low_score_batch_02.blend | Project-authored Blender source for 3D Replacement Batch 02 | **Project-generated source art** | - | 21 editable minigame models producing 23 runtime PNGs; generated 2026-07-14 |
| assets/terrain/leaf.png, grass.jpg, beachball.png, flower.png, flower2.png; assets/mg/rainbow_swatch.png, fish_body.png, fish_fins.png | Approved OpenAI ChatGPT Batch 04 review art promoted by project tooling | **Project-generated art** | assets_src/style_review_batch_04/final/ | normalized to at most 1024px; registered craft layers and source-style terrain inventory; generated/promoted 2026-07-14 to 2026-07-15 |
| assets/kart/finish_banner.png, boost_ribbon.png | Approved OpenAI ChatGPT Batch 04 kart motif sheet, split by project tooling | **Project-generated art** | assets_src/style_review_batch_04/final/021_kart_motif_sheet.png | isolated semantic finish/ramp motifs; 1024x256 RGBA; generated/promoted 2026-07-14 |
| backups/art_pre_remediation_2026-07-15/** | Byte-identical snapshots of repository art from `origin/master` at commit `61e80dd5` | **Same license as each original mirrored asset** | original repository paths and this ledger | reversal archive only; manifest includes source and current SHA-256 values; created 2026-07-15 |
| assets_src/style_review_score3/** | OpenAI ChatGPT image generation plus approved project review sources, guided by `ART_STYLE_GUIDE.md` and the game-wide 3/5 audit | **Project-generated review art** | - | chroma sources, rejected snow candidate, split sources, and final candidates; generated 2026-07-15 |
| assets/terrain/up_dirt_col.jpg, up_grass_col.jpg, up_sand_col.jpg, up_snow_col.jpg, up_snowsoft_col.jpg | Approved OpenAI ChatGPT score-3 terrain rebuild | **Project-generated art** | assets_src/style_review_score3/terrain_*_blank.png | blank low-frequency painted canvases; 1024px; previous files archived; promoted 2026-07-15 |
| assets/terrain/up_crystal_col.png, up_shipwood_col.png | OpenAI ChatGPT score-3 material rebuild | **Project-generated art** | assets_src/style_review_score3/crystal_facet.png, shipwood.png | matte triplanar crystal facets and painted nautical planks; 1024px; generated 2026-07-15 |
| assets/props/story/leaf_broad.png, leaf_spear.png, leaf_fern.png, leaf_palmfan.png, flower_coral.png, flower_lavender.png | Approved OpenAI ChatGPT Batch 04 tropical and flower sheets, split by project tooling | **Project-generated art** | assets_src/style_review_batch_04/final/003_flower_coral_card.png, 004_flower_lavender_card.png, 005_leaf_tropical_sheet.png | isolated transparent world cards; promoted 2026-07-15 |
| assets/props/story/mushroom_red.png, mushroom_tan_cluster.png, fruit_apple.png, fruit_banana.png, fruit_orange.png, fruit_melon.png, beetle.png, ladybug.png | OpenAI ChatGPT score-3 object and insect rebuild | **Project-generated art** | assets_src/style_review_score3/ | border-connected chroma removal; complete role-separated cards; <=1024px; generated 2026-07-15 |
| assets/mg/seed.png | OpenAI ChatGPT score-3 garden icon rebuild | **Project-generated art** | assets_src/style_review_score3/seed.png | 512px transparent seed icon; previous file archived; generated 2026-07-15 |
| assets/mg/butterfly.png | Approved project-generated complete butterfly card, adapted from the GEN2 butterfly family | **Project-generated art** | assets/props/gen2/butterfly1.png | resized to 512px for garden-minigame use; previous wing-only file archived; promoted 2026-07-15 |
| backups/art_pre_score3_2026-07-15/** | Snapshots of every runtime raster overwritten by the score-3 rebuild | **Same license as each original mirrored asset** | original repository paths and this ledger | reversal archive plus restore script; created 2026-07-15 |
| assets/props/alpine/alpine_fish_aquarium.glb | Project-authored Blender 4.4.3 Alpine chalet collectible: storybook fish in a pale glass aquarium | **Project-generated art** | - | Original low-poly geometry; separate `Cage` and `Collectible` nodes; embedded matte materials; generated 2026-07-15 |
| assets/props/alpine/alpine_beetle_terrarium.glb | Project-authored Blender 4.4.3 Alpine chalet collectible: oversized beetle in a ventilated glass terrarium | **Project-generated art** | - | Original low-poly geometry; separate `Cage` and `Collectible` nodes; embedded matte materials; generated 2026-07-15 |
| assets/props/alpine/alpine_bird_cage.glb | Project-authored Blender 4.4.3 Alpine chalet collectible: pastel bird in a thin-bar golden perch cage | **Project-generated art** | - | Original low-poly geometry; separate `Cage` and `Collectible` nodes; embedded matte materials; generated 2026-07-15 |
| assets_src/blender/alpine_chalet_creatures.blend | Editable Blender source scene for the three Alpine chalet creature habitats | **Project-generated source art** | - | Deterministic source for all three runtime GLBs and QA renders; generated 2026-07-15 |
| assets_src/blender/qa_alpine_chalet_creatures/alpine_fish_habitat.png | Blender Eevee QA render of the Alpine fish aquarium | **Project-generated review art** | assets_src/blender/alpine_chalet_creatures.blend | 700x700 visual QA render; generated 2026-07-15 |
| assets_src/blender/qa_alpine_chalet_creatures/alpine_beetle_habitat.png | Blender Eevee QA render of the Alpine beetle terrarium | **Project-generated review art** | assets_src/blender/alpine_chalet_creatures.blend | 700x700 visual QA render; generated 2026-07-15 |
| assets_src/blender/qa_alpine_chalet_creatures/alpine_bird_habitat.png | Blender Eevee QA render of the Alpine bird cage | **Project-generated review art** | assets_src/blender/alpine_chalet_creatures.blend | 700x700 visual QA render; generated 2026-07-15 |
| assets/collectibles/*.glb | Eighteen Critter Book species plus the storybook catch net, modeled and palette-skinned in Blender 4.4.3 for this project | **Project-generated art** | tools/build_collection_critters.py | Rounded low-poly primitives; embedded matte materials only; no external textures or source meshes; Mobile-safe exports; generated 2026-07-15 |
| assets_src/blender/collection_critters.blend | Editable Blender source scene for all Critter Book species and the catch net | **Project-generated source art** | tools/build_collection_critters.py | Contains fish, seahorse, insect and bird anatomy families with distinct per-species material skins; generated 2026-07-15 |
| assets_src/blender/qa_collection_critters.png | Blender Eevee overview render of the complete Critter Book asset family | **Project-generated review art** | assets_src/blender/collection_critters.blend | Visual QA only; transparent 1200x700 render; generated 2026-07-15 |
| assets/reef_regions/wreck_ravine_shoulders.glb, kelp_cathedral_arch.glb, kelp_lantern_cluster.glb, moon_shell_arch.glb, moon_pearl_totem.glb, ice_crystal_cluster.glb, ice_current_fan.glb | Project-authored Blender 4.4.3 regional reef kit | **Project-generated art** | assets_src/blender/reef_region_kit.blend | rebuilt 2026-07-16 as asymmetric wreck ridges, tapered kelp, eroded shell masses, rounded brinicle hummocks, and flowing current sheets; texture-free embedded matte materials |
| assets_src/blender/reef_region_kit.blend | Project-authored Blender source for the regional reef kit | **Project-generated source art** | - | editable source scene for seven production GLBs; rebuilt 2026-07-16 |
| assets_src/blender/qa_reef_region_kit/*.png | Blender Eevee QA renders of the regional reef kit | **Project-generated review art** | assets_src/blender/reef_region_kit.blend | isolated visual QA renders regenerated 2026-07-16 |
| assets/dungeon/*.glb | Project-authored Blender 4.4.3 dungeon geometry guided by `ART_STYLE_GUIDE.md` and the 2026-07-16 human art audit | **Project-generated art** | assets_src/blender/dungeon_art_v2.blend | ten Mobile-friendly models replacing primitive arena, door, enemy, boss, basket, pedestal, lantern, statue, stepping-stone, and pictogram roles; embedded matte storybook palette; generated 2026-07-16 |
| assets_src/blender/dungeon_art_v2.blend | Editable source for the authored Dungeon Art V2 kit | **Project-generated source art** | tools/build_dungeon_art_v2.py | complete editable source scene for all ten runtime GLBs; generated 2026-07-16 |
| assets_src/blender/qa_dungeon_art_v2/*.png | Blender Workbench QA renders of Dungeon Art V2 | **Project-generated review art** | assets_src/blender/dungeon_art_v2.blend | transparent 900x700 model review renders; generated 2026-07-16 |
| backups/art_pre_dungeon_v2_2026-07-16/** | Byte-identical pre-integration dungeon builder scripts | **Same license as original project code** | scripts/combat_arena.gd; scripts/dungeon_puzzle_room.gd | reversal archive with SHA-256 manifest; created 2026-07-16 |
| assets/northern/*.glb | Project-authored Blender 4.4 Northern Kingdom kit guided by `ART_STYLE_GUIDE.md` and the capped 4.9 computer-audit rubric | **Project-generated art** | tools/build_northern_kingdom_kit.py | twenty-five texture-free, Mobile-friendly models for pass, mountain, forest, town, bridge, mill, forge, dock, castle, hall, bedroom and wisp roles; all original geometry and embedded matte pastel materials; regenerated 2026-07-20 |
| assets_src/blender/northern_kingdom_kit.blend | Editable source for the Northern Kingdom art kit | **Project-generated source art** | tools/build_northern_kingdom_kit.py | complete editable source scene for all twenty-five runtime GLBs; regenerated 2026-07-20 |
| assets_src/blender/qa_northern_kingdom_kit/*.png | Blender Eevee QA renders of the Northern Kingdom art kit | **Project-generated review art** | assets_src/blender/northern_kingdom_kit.blend | isolated 780x660 asset-review renders used for deterministic reject/regenerate review; regenerated 2026-07-20 |
| assets_src/concepts/northern_kingdom_quality_2026-07-19.png | OpenAI ChatGPT built-in image generation; original Northern Kingdom modular-kit concept sheet | **Project-generated source art** | prompt recorded in `NORTHERN_KINGDOM_QUALITY_AUDIT_2026-07-19.md` | Wide 1536x1024 style-and-shape reference for the deterministic Blender rebuild; no external or protected project art embedded in the runtime; generated 2026-07-19 |
| assets_src/concepts/northern_bedroom_quality_2026-07-20.png | OpenAI ChatGPT built-in image generation; original Northern royal-bedroom concept sheet | **Project-generated source art** | prompt recorded in `NORTHERN_KINGDOM_QUALITY_AUDIT_2026-07-19.md` | 1536x1024 shape-and-material reference for the authored bedroom GLB; no external or protected project art embedded in the runtime; generated 2026-07-20 |
| assets/art35/landmarks/dream_star.glb, crown_star.glb, chamber_star.glb, butterfly_gate.glb, star_observatory.glb | Project-authored Blender 4.4.3 landmark geometry | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Rounded Mobile-safe star, butterfly-gate, and observatory families; embedded matte palette; generated 2026-07-16. |
| assets/art35/landmarks/cloud_0.glb, cloud_1.glb, cloud_2.glb | Project-authored Sky Lagoon cloud family guided by `ART_STYLE_GUIDE.md` | **Project-generated art** | `tools/build_sky_lagoon_quality_kit.py` | Three texture-free, broad-lobed, smooth-normal cloud variants with pearl highlights and blue-lavender undersides; core glTF binaries are Blender-importable; regenerated 2026-07-20; previous binaries retained in `backups/art_pre_sky_lagoon_5of5_2026-07-19/`. |
| assets/sky_lagoon/lagoon_kit/*.glb | Project-authored Sky Lagoon quality kit guided by `ART_STYLE_GUIDE.md`, the runtime audit, and the accepted 2026-07-21 flat PNW prototype cards | **Project-generated art** | `tools/build_sky_lagoon_quality_kit.py`; `tools/build_sky_lagoon_pnw_woody_plants.py`; corresponding `.blend` sources in `assets_src/blender/` | Sixty-one Mobile-friendly models covering complete plants, twelve Seattle-area PNW trees and six native shrub species in two accepted structural variants each (GEN2 flat-card grammar: two to five primary volumes, oversized botanical ornaments, planted bases), paths and gates, park and playground, five-car train and station, pearl castle/bridge, and Alpine village/cave props. All woody plants are original deterministic texture-free geometry; regenerated 2026-07-21. |
| assets_src/blender/sky_lagoon_quality_kit.blend, assets_src/blender/sky_lagoon_pnw_woody_plants.blend | Editable Blender sources for the complete Sky Lagoon quality kit | **Project-generated source art** | `tools/build_sky_lagoon_quality_kit.py`; `tools/build_sky_lagoon_pnw_woody_plants.py` | Editable modeling pieces for all Lagoon runtime GLBs plus three cloud GLBs, exported as Mobile-safe GLBs. The rejected GEN5 tree source and the rejected GEN1 procedural PNW family were removed and replaced by the flat-card GEN2 woody family on 2026-07-21. |
| assets_src/blender/qa_sky_lagoon_quality_kit/*, assets_src/blender/qa_sky_lagoon_pnw_woody_plants/* | Deterministic isolated QA renders for the Sky Lagoon environment and woody-plant family | **Project-generated review art** | Sky Lagoon Blender builders; `tools/render_glb_turntable_batch.py`; `tools/build_pnw_woody_contact_sheets.py` | Non-woody kit reviews plus fixed 0°, 45°, and 135° reviews and uncropped contact sheets for all twelve trees and twelve shrub variants; iteration gate only, with final acceptance based on Mobile-render Godot captures; regenerated 2026-07-21. |
| assets_src/concepts/sky_lagoon_quality_2026-07-20.png | OpenAI built-in image generation; comprehensive Sky Lagoon modular-kit concept sheet | **Project-generated source art** | prompt recorded in `SKY_LAGOON_QUALITY_AUDIT_2026-07-20.md` | Style, palette, and shape-language reference for the deterministic Blender rebuild; no protected project illustration is embedded; generated 2026-07-20. |
| assets_src/concepts/sky_lagoon_tree_family_gen5_2026-07-20.png | OpenAI built-in image generation guided by the four approved GEN2 tree renders | **Project-generated source art** | prompt recorded in `SKY_LAGOON_QUALITY_AUDIT_2026-07-20.md` | Eight-extension GEN5 silhouette and botanical-graph reference; no runtime texture use; generated 2026-07-20. |
| assets_src/concepts/sky_lagoon_pnw_tree_prototypes_flat_2026-07-21.png, assets_src/concepts/sky_lagoon_pnw_shrub_variants_flat_2026-07-21.png | OpenAI built-in image generation guided by the approved in-repository Sky Lagoon quality, tree-family, and first-pass shrub concept sheets | **Project-generated source/model-reference art** | prompts and comparison audit recorded in `SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md` | Flat, review-only PNW prototype sheets for twelve trees and two structural variants of six shrubs; tree revision replaces oversized leaf badges with species-appropriate maple samaras, cottonwood catkin/seed ornaments, and Garry oak acorns; repository copies normalized to a 1024px longest side; no external or protected art embedded; generated and revised 2026-07-21. |
| assets_src/concepts/sky_lagoon_pnw_flat/*.png | Deterministic crops from the two accepted flat PNW prototype sheets | **Project-generated source/model-reference art** | `tools/slice_sky_lagoon_pnw_prototypes.py`; `SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md` | Twenty-four named review cards for later Blender translation; review-only under `assets_src/.gdignore`; not runtime textures; generated 2026-07-21. |
| assets_src/sky_lagoon/runtime_rejected_1e2412a/* | Rejected Godot 4.4 Mobile-render Sky Lagoon review set | **Project-generated review evidence** | `scripts/probe_sky_lagoon_art.gd`; GitHub Actions run `29711050812` | Fourteen runtime views plus contact sheet retained after human rejection for inward face winding, opaque Butterfly gate, oversized station text, and weak review framing; captured 2026-07-19. |
| assets_src/sky_lagoon/runtime_rejected_9da8457/* | Rejected Godot 4.4 Mobile-render Sky Lagoon review set | **Project-generated review evidence** | `scripts/probe_sky_lagoon_art.gd`; GitHub Actions run `29712024169` | Fourteen runtime views plus contact sheet retained after human rejection for a buried Fairy Pond, washed palette, castle-occluding cloud, and invalid Alpine review camera; captured 2026-07-19. |
| assets_src/sky_lagoon/runtime_rejected_584d3a0/* | Rejected Godot 4.4 Mobile-render Sky Lagoon review set | **Project-generated review evidence** | `scripts/probe_sky_lagoon_art.gd`; GitHub Actions run `29712933709` | Fourteen runtime views plus contact sheet retained after human rejection because the persistent reef sun stacked with Lagoon daylight and clipped the world palette toward white; captured 2026-07-19. |
| assets_src/sky_lagoon/runtime_candidate_046fbcf/* | Godot 4.4 Mobile-render Sky Lagoon owner-review candidate | **Project-generated review evidence** | `scripts/probe_sky_lagoon_art.gd`; GitHub Actions run `29714300033` | Fourteen Speedy views, three Sparkly comparisons, and a contact sheet retained after technical gates and agent visual review passed; candidate remains below owner-awarded 5/5; captured 2026-07-19. |
| backups/art_pre_sky_lagoon_5of5_2026-07-19/** | Byte-identical pre-pass Sky Lagoon cloud binaries and integration scripts | **Same licenses as the original files** | matching repository-relative runtime paths | Reversal archive with documented cloud SHA-256 hashes; protected book art is excluded because it was not modified; created 2026-07-19. |
| assets/art35/reef/seagrass_0.glb, seagrass_1.glb, kelp_0.glb, kelp_1.glb | Project-authored Blender 4.4.3 reef foliage | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Low-overdraw modeled tuft and ribbon families replacing repeated cards; generated 2026-07-16. |
| assets/art35/kart/showcase_plinth.glb, soft_barrier.glb, finish_arch.glb | Project-authored Blender 4.4.3 kart geometry | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Rounded toy showcase, barrier, and finish landmark; generated 2026-07-16. |
| assets/art35/northern/northern_gate.glb, northern_mountain.glb, northern_house_0.glb, northern_house_1.glb, northern_house_2.glb, northern_castle.glb | Project-authored Blender 4.4.3 Northern Kingdom kit | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Original snow-gate, mountain, house, and keep silhouettes; generated 2026-07-16. |
| assets/art35/castle/kitchen_kettle.glb, kitchen_teapot.glb, kitchen_pan_set.glb, kitchen_soup_pot.glb, kitchen_table_set.glb | Project-authored Blender 4.4.3 castle kitchen props | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Rounded shell-accented kitchen set; generated 2026-07-16. |
| assets/art35/castle/music_rail.glb, music_bar_0.glb, music_bar_1.glb, music_bar_2.glb, music_bar_3.glb, music_bar_4.glb, music_bar_5.glb, music_bar_6.glb, music_song_star.glb, music_wall_panel.glb | Project-authored Blender 4.4.3 castle music-room kit | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Independent playable bars plus physical staff, notes, rail, and song-star silhouettes; generated 2026-07-16. |
| assets/art35/castle/royal_bed.glb, royal_nightstand.glb, royal_bookcase.glb, dream_bed_0.glb, dream_bed_1.glb, dream_bed_2.glb, dream_bed_3.glb, dream_bed_4.glb, dungeon_gate.glb | Project-authored Blender 4.4.3 castle room kit | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Original royal/dream furniture and ten-pearl undercroft gate; generated 2026-07-16. |
| assets/art35/arena/meadow_bush_0.glb, meadow_bush_1.glb, meadow_bush_2.glb, meadow_bush_3.glb, winter_tree_0.glb, winter_tree_1.glb, winter_tree_2.glb, winter_shore_0.glb, winter_shore_1.glb | Project-authored Blender 4.4.3 arena foliage | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Four bush, three winter-tree, and two winter-shore variants; generated 2026-07-16. |
| assets/art35/arena/treasure_chest.glb, treasure_dais.glb, treasure_cluster_0.glb, treasure_cluster_1.glb, treasure_cluster_2.glb, shop_interior.glb, slide_snowbank_0.glb, slide_snowbank_1.glb, slide_finish_arch.glb | Project-authored Blender 4.4.3 arena landmarks | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Treasure, shop, and slide families with objective-readable silhouettes; generated 2026-07-16. |
| assets/art35/arena/fairy_lily_cluster.glb, fairy_flower_gate.glb, fairy_shadow_beetle.glb, fairy_bank_0.glb, fairy_bank_1.glb, fairy_shadow_jellyfish.glb, fairy_shadow_eel.glb | Project-authored Blender 4.4.3 fairy-pond kit | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Habitat-specific lilies, banks, six-legged beetle, jellyfish, eel, and flower gate; generated 2026-07-16. |
| assets/art35/galaxy/wish_fountain.glb, star_bell_0.glb, star_bell_1.glb, star_bell_2.glb, ice_gate.glb, shell_throne.glb | Project-authored Blender 4.4.3 galaxy furniture and landmarks | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Original walk-through arch, independent bells, fountain, and shell throne; generated 2026-07-16. |
| assets/props/gen2/coral.glb, coral1.glb, coral2.glb, coral3.glb, coral4.glb, coral5.glb, coral6.glb | Project-authored Blender 4.4.3 coral family | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Seven undersea-only clumps replacing mixed-habitat and repeated-card forms; old GLBs mirrored in `backups/art_pre_pass35_2026-07-16/`; generated 2026-07-16. |
| assets/props/gen2/rock.glb, rock1.glb, rock2.glb, rock3.glb, rock4.glb, rock5.glb, rock_largea.glb | Project-authored Blender 4.4.3 rock family | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Seven low-poly toon variants; old GLBs mirrored in `backups/art_pre_pass35_2026-07-16/`; generated 2026-07-16. |
| assets/props/gen2/clownfish.glb, octopus.glb, jellyfish.glb, shrimp.glb | Project-authored Blender 4.4.3 creature anatomy | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Complete fish fins, eight octopus arms, jellyfish bell/oral arms/tentacles, and ten-legged shrimp; generated 2026-07-16. |
| assets/dungeon/pepper_projectile.glb, ice_berry_projectile.glb | Project-authored Blender 4.4.3 dungeon projectile pair | **Project-generated art** | `tools/build_art_pass35.py`; `assets_src/blender/art_pass35.blend` | Readable curved chili and faceted berry replace transient glowing spheres; generated 2026-07-16. |
| assets/mg/sun.png, tree.png, coal.png, star.png, butterfly.png, fish_body.png, fish_fins.png, k_bush2.png, xtree.png, orn1.png, orn2.png, orn3.png, orn4.png, orn5.png | OpenAI ChatGPT built-in image generation guided by `ART_STYLE_GUIDE.md` and the source-book motif analysis | **Project-generated art** | `assets_src/imagegen/pass35_2026-07-16/chroma/`; `ART_PASS35_PROMPTS.md` | Separate chroma generations; corner-sampled green/magenta alpha removal, despill, tight crop, normalized to at most 1024 px; previous files mirrored in `backups/art_pre_pass35_2026-07-16/`; generated 2026-07-16. |
| assets_src/imagegen/pass35_2026-07-16/chroma/*.png | OpenAI ChatGPT built-in image generation | **Project-generated source art** | `ART_PASS35_PROMPTS.md` | Original flat green/magenta sources retained for reproducibility; generated 2026-07-16. |
| assets_src/blender/art_pass35.blend, assets_src/blender/qa_art_pass35/*.png | Project-authored Blender source and QA renders for the pass-35 library | **Project-generated source/review art** | `tools/build_art_pass35.py` | Editable deterministic source plus one isolated render per GLB; generated 2026-07-16. |
| assets/ship/Textures/colormap.png | Byte-identical project texture restored from `assets/terrain/up_shipwood_col.png` | **Project-generated derivative** | `assets/terrain/up_shipwood_col.png` | Restores a missing ship material dependency without modifying protected book art; restored 2026-07-16. |
| backups/art_pre_pass35_2026-07-16/** | Byte-identical pre-pass runtime art and script snapshots from `origin/master` `021e235f` | **Same license as each mirrored source** | original repository paths; `backups/art_pre_pass35_2026-07-16/MANIFEST.md` | Reversal archive for every overwritten sprite, coral/rock/creature GLB, and affected art-routing script; created 2026-07-16. |
| assets_src/fairy_v2/concepts/*.png | Original Fairy Pond V2 background, shadow-bug, leaf-shield, and five-state Fairy Flower masters generated with the built-in OpenAI image tool from `ART_STYLE_GUIDE.md` direction | **Project-generated art** | assets_src/fairy_v2/GENERATED_ART.md | twelve orthographic top-down masters; normalized to 1024px; V2 background concepts retained as history after the V3 runtime replacement; no protected book, family voice, or friend source modified; generated 2026-07-16 |
| assets_src/fairy_v2/runtime_textures/*.png | Fairy Pond V2 transparent relief-build textures derived from the registered subject concepts | **Project-generated art** | assets_src/fairy_v2/concepts/ | nine export-excluded RGBA masters; connected chroma removal, soft matte, despill, centered transparent padding; 1024x1024; generated 2026-07-16 |
| assets_src/fairy_v5/concepts/*.png | Fairy Pond V5 panorama and ornament source art generated with the built-in OpenAI image tool | **Project-generated art** | assets_src/fairy_v5/GENERATED_ART.md | one uninterrupted top-down pond canvas plus one two-ornament chroma sheet; dramatic mint/aqua→cobalt→indigo/purple flow; no protected source modified; generated 2026-07-27 |
| assets/fairy/pond_panorama.png | Fairy Pond V5 single-canvas runtime background | **Project-generated art** | assets_src/fairy_v5/concepts/fairy_pond_panorama_raw.png; tools/process_fairy_panorama.py | one RGB 4096x1024 power-of-two panorama; a single resample only, with no stitched plates, tiles, mirrored bridges, or generated join bands; published 2026-07-27 |
| assets/fairy/sprites/{bug_jewel,bug_moth,bug_firefly,boss_leaf,boss_seed,boss_sprout,boss_bud,boss_opening,boss_bloom}.png | Fairy Pond V2 illustrated subjects converted from export-excluded transparent masters to runtime Sprite3D cards | **Project-generated art** | assets_src/fairy_v2/runtime_textures/*.png; tools/process_fairy_readability_art.py | nine RGBA 1024x1024 2D sprite cards with transparent padding; former GLB reliefs retired; published 2026-07-27 |
| assets_src/fairy_v4/**; assets/fairy/sprites/{helpful_flower_gate,danger_thorn_halo}.png | Original Fairy Pond V4 nonverbal readability cues generated with the built-in OpenAI image tool | **Project-generated art** | assets_src/fairy_v4/GENERATED_ART.md; tools/process_fairy_readability_art.py | mint/gold rounded helpful ring and coral/plum pointed danger ring; flat chroma sources retained, locally alpha-extracted, centered and normalized to 1024x1024 runtime Sprite3D cards; generated 2026-07-27 |
| assets_src/fairy_v5/runtime_textures/*.png; assets/fairy/sprites/{ornament_lily_cluster,ornament_lavender_reeds}.png | Fairy Pond V5 ornamental Sprite3D cards generated with the built-in OpenAI image tool | **Project-generated art** | assets_src/fairy_v5/GENERATED_ART.md; tools/process_fairy_panorama.py; tools/process_fairy_readability_art.py | two matching 1024x1024 RGBA cards—a mint lily cluster and lavender reed tuft—red-key extracted and placed along the background banks as noninteractive Sprite3D ornaments; generated 2026-07-27 |
| assets/full_texture_regen_2026-07-18/models/*.glb | Project-authored deterministic Blender geometry guided by `ART_STYLE_GUIDE.md` and the game-wide full-regeneration audit | **Project-generated art** | `tools/build_full_texture_regen.py`; `assets_src/blender/full_texture_regen_2026-07-18/full_texture_regen.blend` | 137 isolated, texture-free Mobile candidates with embedded matte materials; no runtime paths replaced; generated 2026-07-18 |
| assets/full_texture_regen_2026-07-18/textures/*.png | OpenAI ChatGPT built-in image generation guided by the source-book style analysis and full-regeneration prompt contract | **Project-generated art** | `assets/full_texture_regen_2026-07-18/source_generations/accepted/`; `assets/full_texture_regen_2026-07-18/PROMPTS.md` | 30 reviewed isolated candidates plus one unscored R044 calm-ground development texture, all normalized to at most 1024 px; alpha cleanup, despill, and seam processing; no runtime paths replaced; generated and iterated 2026-07-18 |
| assets/full_texture_regen_2026-07-18/source_generations/** | Original accepted and rejected OpenAI ChatGPT image-generation outputs | **Project-generated source/review art** | `assets/full_texture_regen_2026-07-18/PROMPTS.md` | 28 reviewed accepted sources, 1 accepted unscored R044 development source, and 1 rejected source retained for provenance; excluded from Godot import; generated and iterated 2026-07-18 |
| assets/full_texture_regen_2026-07-18/textures/R044_BUTTERFLY_WORLD_PLANET_SURFACE__butterfly_meadow_ground_calm.png and source_generations/accepted/R044_BUTTERFLY_WORLD_PLANET_SURFACE__calm_ground_source.png | OpenAI ChatGPT built-in image-generation edit of the project-authored R044 meadow source | **Project-generated art** | `assets/full_texture_regen_2026-07-18/PROMPTS.md` iteration-2 R044 prompt | Cooler low-flower mass-placement base requested by Claude's iteration-2 critique; raw source 1254x1254, candidate resized to 1024x1024 and seam-pinned on both axes with the project normalization functions; unscored and not wired to runtime; created 2026-07-18 |
| assets_src/blender/full_texture_regen_2026-07-18/** | Editable Blender source and deterministic model manifest for the full-regeneration candidate pack | **Project-generated source art** | `tools/build_full_texture_regen.py` | Source for all 137 isolated GLBs; excluded from Godot import; generated 2026-07-18 |
| audit/full_regen_2026-07-18/** | Derived Blender Eevee renders, contact sheets, repetition sheets, ledgers, and stress-test reports | **Project-generated review art** | `assets/full_texture_regen_2026-07-18/`; `tools/render_full_texture_regen.py`; `tools/build_full_regen_galleries.py` | Visual QA only; excluded from Godot import; generated 2026-07-18 |
| gen2/generated/r003_coral_branch_bare/*.png; gen2/generated/r004_volumetric_kelp_tall_canopy_a/*.png; gen2/generated/r021_locomotive_identity/*.png; gen2/generated/r021_track_straight/*.png; gen2/generated/r021_track_quarter_curve/*.png; gen2/generated/r021_station_platform_low/*.png; gen2/generated/r021_station_shelter_open/*.png | OpenAI built-in image-generation prototype sheets guided by the 2026-07-18 Codex improvement and object-generation audits | **Project-generated review art** | `gen2/CODEX_IMPROVEMENT_PROTOTYPE_BATCH_2026-07-18.md` | Isolated review-only concept turnarounds; original 1254 px provenance files plus 1024 px review copies; no external source art; no runtime promotion or APK export; generated and iterated 2026-07-18 |
| assets_src/sky_lagoon/cohesion_pass_2026-07-19/** | OpenAI built-in image-generation model-reference sheets guided by `ART_STYLE_GUIDE.md` and the in-frame Sky Lagoon cohesion audit | **Project-generated review art** | `SKY_LAGOON_STYLE_COHESION_AUDIT_2026-07-19.md`; `CLAUDE_SKY_LAGOON_DESIGN_HANDOFF_2026-07-19.md`; batch `PROMPTS.md` | Eight selected 1024px design references, untouched raw masters, one rejected square-recess castle iteration, hashes, and contact sheet; review-only under `assets_src/.gdignore`; no runtime asset replaced; generated 2026-07-19. |
| gen2/ui_prototypes_2026-07-19/*.png | OpenAI built-in image-generation and editing prototypes guided by the project's UI, non-reader-accessibility, Mobile-readability, and art-direction audits | **Project-generated review art** | `gen2/UI_PROTOTYPE_REVISIONS_2026-07-19.md`; `gen2/ui_prototypes_2026-07-19/PROMPTS.md`; project-authored successful reef capture artifact from Actions run `29674202837` | Review-only exploration, pause, craft, and intro interface mockups; 1672x941 provenance files plus 1024x576 review copies; the HUD/pause background derives from project runtime capture evidence; protected source assets untouched; no Godot wiring or APK export; generated and iterated 2026-07-19 |

| assets_src/concepts/opera_house_flat/*.png; assets_src/concepts/opera_house_flat/cards/*.png | Original Pearl Opera House flat prototypes generated with OpenAI built-in image generation under project art direction | **Project-generated review art** | `assets_src/concepts/opera_house_flat/PROMPTS.md`; `OPERA_HOUSE_FLAT_ART_AUDIT_2026-07-21.md`; `tools/slice_opera_house_prototypes.py` | Thirteen accepted sheets and 172 derived cards; normalized to at most 1024 px; review/model-reference only, no runtime path replaced; generated and iterated 2026-07-21. |
| assets_src/concepts/opera_jobs_flat_2026-07-21/*.png; assets_src/concepts/opera_jobs_flat_2026-07-21/cards/*.png; audit/opera_job_flat_contact_sheet_2026-07-21.png | Original Opera House Roshan outfit, subgame-prop, and stage/state prototypes generated with OpenAI built-in image generation from project-owned Roshan and Opera House visual references | **Project-generated review/model-reference art** | `assets_src/concepts/opera_jobs_flat_2026-07-21/PROMPTS.md`; `OPERA_JOB_FLAT_ART_AUDIT_2026-07-21.md`; `tools/slice_opera_job_prototypes.py` | Thirty-six accepted 1024px sheets, 576 deterministic 1024x1024 individual card renders, and one derived audit contact sheet for twelve non-boss jobs; individual cards preserve the accepted sheet cells without a new generative reinterpretation; three failed drafts were regenerated and retained only in external provenance cache; review/model-reference only, no protected or runtime art replaced; generated and iterated 2026-07-21. |
| assets_src/concepts/opera_nursery_2026-08-01/*.png | Original Nursery Nurse Roshan, Nurse Faron, and three-baby source generations made with OpenAI built-in image generation from project-owned/protected identity references | **Project-generated source art** | `assets_src/concepts/opera_nursery_2026-08-01/GENERATED_ART.md`; `SHA256SUMS` | Three accepted complete isolated storybook generations plus non-destructive alpha masters; protected Roshan/Faron/baby references were read-only and no protected pixels were copied into delivery; generated and accepted 2026-08-01. |
| assets/opera/worlds/actors/roshan_nursery.png; assets/opera/worlds/actors/faron_nursery.png; assets/opera/worlds/nursery/baby_0.png through baby_2.png | Deterministic lossless-alpha runtime derivatives of the accepted OpenAI nursery sources | **Project-generated art** | `tools/prepare_opera_nursery_art.py`; `assets_src/concepts/opera_nursery_2026-08-01/GENERATED_ART.md` | Whole-subject fits and deliberate equal-lane baby splits only; 512×512 actors and 320×320 baby cards, transparent-corner and chroma-residue audited; created 2026-08-01. |
| assets_src/concepts/ocean_kingdoms_2026-07-22/**/*.png | Original Caribbean and Norwegian ocean-kingdom environment and fauna reference sheets generated with OpenAI built-in image generation under project art direction | **Project-generated review/model-reference art** | `assets_src/concepts/ocean_kingdoms_2026-07-22/PROMPTS.md`; `assets_src/concepts/ocean_kingdoms_2026-07-22/README.md` | Four accepted and one quarantined 1536x1024 source sheet for Claude's modular low-poly 3D reconstruction lane; first Caribbean fauna draft rejected for an Indo-Pacific regal-tang pattern, accepted revision uses adult Atlantic blue tang identity; no external reference art; reference-only under `assets_src/.gdignore`; no runtime or protected asset replaced; generated 2026-07-22. |

+| assets/ember_fortress/ember_planet.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_tower_a.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_tower_b.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_tower_c.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_tower_d.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_rampart.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_flag.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_great_gate.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_gate_veil.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_sentry.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_king.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_lantern.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_flame.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_beacon.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_geyser.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_crag_a.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_crystal_a.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_crag_b.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_crystal_b.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_crag_c.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_crystal_c.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_ash_moon.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_home_ring.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_arena.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_door.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_imp.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_boss.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_basket.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_fire_projectile.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_ice_projectile.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_pedestal.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_dungeon_lantern.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_statue.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_stepping_stone.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_pictograms.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_clue_plaque.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_direction_beak.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_completion_spark.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets/ember_fortress/ember_pearl_target.glb | Project-authored deterministic Blender 4.5 geometry | **Project-generated art** | `tools/build_ember_fortress_kit.py`; `assets_src/blender/ember_fortress_kit.blend` | Texture-free Ember Fortress runtime role; generated 2026-07-21. |
| assets_src/blender/ember_fortress_kit.blend | Editable deterministic source for the complete Ember Fortress kit | **Project-generated source art** | `tools/build_ember_fortress_kit.py` | Source for 39 texture-free runtime GLBs; generated 2026-07-21. |
| assets_src/blender/qa_ember_fortress_kit/** | Deterministic isolated QA renders, contact sheets, and parsed geometry metrics | **Project-generated review art** | `tools/build_ember_fortress_kit.py`; `EMBER_FORTRESS_GRAPHICS_AUDIT_2026-07-21.md` | Review-only evidence; final acceptance uses Mobile runtime captures; generated 2026-07-21. |
| audit/ember_runtime_2026-07-21/** | Godot 4.4.1 Forward Mobile Ember Fortress runtime evidence | **Project-generated review art** | `scripts/probe_ember_art.gd` | Ten representative Speedy frames and one contact sheet; captured 2026-07-21. |
| assets_src/concepts/ember_fortress_claude_2026-07-22/*.png | Original Ember Fortress Blender modeling boards generated with OpenAI built-in image generation from the project-authored 42-role audit and scale contracts; no input image or external source art | **Project-generated review/model-reference art** | `assets_src/concepts/ember_fortress_claude_2026-07-22/PROMPTS.md`; `EMBER_FORTRESS_2D_CONCEPT_AUDIT_2026-07-22.md`; `CLAUDE_EMBER_FORTRESS_BLENDER_HANDOFF_2026-07-22.md` | Six selected boards normalized to a 1024px longest edge plus one derived 1024px contact sheet; raw masters retained only in local provenance cache; review/model-reference input for Claude's Blender work; no runtime asset replaced or APK-exported; generated 2026-07-22. |
| assets_src/concepts/ember_fortress_claude_2026-07-22/expansion_40/*.png | Forty original individual Ember Fortress enrichment cards generated with OpenAI built-in image generation using the project-generated Ember contact sheet as style reference only | **Project-generated review/model-reference art** | `assets_src/concepts/ember_fortress_claude_2026-07-22/expansion_40/PROMPTS.md`; `EMBER_FORTRESS_EXPANSION_40_AUDIT_2026-07-22.md`; `CLAUDE_EXPANSION_40_MANIFEST.csv` | Forty 1024px individual modeling cards plus four derived 1024×768 contact sheets; original generic volcanic fantasy designs; no external or protected source art; review/model-reference only, no runtime replacement or APK export; generated 2026-07-22. |
| assets/castle/day_one_pool/*.png; assets_src/imagegen/day_one_pool_2026-08-22/*.png; assets_src/imagegen/day_one_pool_2026-08-22/rejected/*.png | OpenAI built-in image generation using the approved project-owned Mermaid Pool plate, separated fixtures, and Roshan cutout as style/identity references | **Project-generated derivative of © Mermaid Roshan LLC — all rights reserved** | `assets_src/imagegen/day_one_pool_2026-08-22/PROVENANCE.md` | Five selected transparent source masters: pool algae/trash, waterfall growth, rim grime, the corrected clogged seahorse fountain with a soggy wrapper visibly lodged in its mouth/nozzle, and the new distinct Rumi character. The superseded wrong-identity seahorse is retained under the source `rejected/` evidence folder and is never a runtime fallback. Runtime copies normalized non-destructively with FFmpeg 8.1.2 to a maximum 1024px edge with RGBA preserved; protected references and clean runtime originals remain unchanged; generated and corrected 2026-08-22. |

## Individual credits (detail)
- **chuck_bark.ogg / chuck.ogg** — 'Free Dog Bark' by DRAGON-STUDIO via Pixabay
  (Pixabay Content License, royalty-free, no attribution required), file
  dragon-studio-free-dog-bark-419014.mp3. Trimmed + normalized.

## OPEN QUESTION (owner decision needed)
- **assets/aquatic/*.glb** — "free use, no redistribution" license vs this PUBLIC
  repository (public git hosting arguably redistributes the files). Options:
  (a) accept as-is for a personal freeware project, (b) make the repo private,
  (c) swap to the CC0 replacements manifest parked in ASSET_AUDIT.md §5.
  Awaiting your call; nothing changed pending it.

## CC-BY attribution block (ship this text with any public build)
Contains models by Poly by Google, jeremy, S. Paul Michael, Ivan Kraft
(CC-BY 3.0, via poly.pizza). Music by Juhani Junkala (CC0). World assets by
Kenney, Kay Lousberg, Isa Lousberg (Tiny Treats), Quaternius, Poly Haven,
ambientCG (all CC0).

### Archived castle differentiation texture candidates (2026-07-17)
- Files: `art_library/candidates/castle_differentiation_2026-07-17/*.jpg`
- Source: project-authored texture studies recovered from the local
  `castle-differentiation` worktree
- License: project original; not for external redistribution
- Modifications: none; archived byte-for-byte and excluded from Godot imports
- Status: unintegrated candidates retained for visual review
- assets/opera/jobs/pastry_chef/opera_pastry_chef_layer_vanilla.glb — original work (this project), CC0-equivalent. Built programmatically (assets_src/blender/build_opera_pastry_chef.py, Blender 5.0 bpy) as a 3D interpretation of the project's own accepted flat cards in assets_src/concepts/opera_jobs_flat_2026-07-21/. No external assets. Modifications: n/a (new).
- assets/opera/jobs/pastry_chef/opera_pastry_chef_layer_coral.glb — same source/license as above.
- assets/opera/jobs/pastry_chef/opera_pastry_chef_layer_plum.glb — same source/license as above.
- assets/opera/jobs/pastry_chef/opera_pastry_chef_bowl.glb — same source/license as above.
- assets/opera/jobs/pastry_chef/opera_pastry_chef_oven.glb — same source/license as above.
- assets_src/blender/opera_pastry_chef_2026-07-22.blend — Blender source for the above, original work.
- assets/opera/jobs/ballerina/opera_ballerina_tile_{0,1,2,3}.glb — original work (this project), CC0-equivalent. Built programmatically (assets_src/blender/build_opera_batch2.py + opera_shared.py, Blender 5.0 bpy) from the project's accepted flat cards. Modifications: n/a (new).
- assets/opera/jobs/pastry_chef/opera_pastry_chef_outfit.glb — original work, same source/tooling as above (chef toque + whisk outfit kit).
- assets_src/blender/opera_batch2_2026-07-22.blend — Blender source for the above, original work.
- assets/opera/jobs/detective/opera_detective_box_{0..5}.glb, opera_detective_chest.glb — original work (this project), CC0-equivalent. Built programmatically (assets_src/blender/build_opera_detective.py + opera_shared.py, Blender 5.0 bpy) from the project's accepted flat cards. Modifications: n/a (new).
- assets_src/blender/opera_detective_2026-07-22.blend — Blender source for the above, original work.
- assets/opera/jobs/candymaker/opera_candymaker_press.glb, opera_candymaker_candy_{0..6}.glb — original work (this project), CC0-equivalent. Built programmatically (assets_src/blender/build_opera_candymaker.py + opera_shared.py, Blender 5.0 bpy) from the project's accepted flat cards. Modifications: n/a (new).
- assets_src/blender/opera_candymaker_2026-07-22.blend — Blender source for the above, original work.
- assets/opera/jobs/{ballerina,detective,candymaker}/opera_*_outfit.glb — original work (this project), CC0-equivalent. Built programmatically (assets_src/blender/build_opera_outfits_floor1.py + opera_shared.py, Blender 5.0 bpy) from the project's accepted outfit cards. Modifications: n/a (new).
- assets_src/blender/opera_outfits_floor1_2026-07-22.blend — Blender source for the above, original work.
- assets/opera/jobs/doctor/opera_doctor_{patient,scope,thermo,bandage}.glb — original work (this project), CC0-equivalent. Built programmatically (assets_src/blender/build_opera_doctor.py + opera_shared.py, Blender 5.0 bpy) from the project's accepted flat cards. Modifications: n/a (new).
- assets_src/blender/opera_doctor_2026-07-22.blend — Blender source for the above, original work.
- assets/opera/jobs/magician/opera_magician_hat_{0,1,2}.glb, opera_magician_bunnyfish.glb — original work (this project), CC0-equivalent. Built programmatically (assets_src/blender/build_opera_magician.py + opera_shared.py, Blender 5.0 bpy) from the project's accepted flat cards. Modifications: n/a (new).
- assets_src/blender/opera_magician_2026-07-22.blend — Blender source for the above, original work.
- assets/opera/jobs/boxer/opera_boxer_dressing.glb — original work (this project), CC0-equivalent. Built programmatically (assets_src/blender/build_opera_boxer.py + opera_shared.py, Blender 5.0 bpy) from the project's accepted flat cards. Modifications: n/a (new).
- assets_src/blender/opera_boxer_2026-07-22.blend — Blender source for the above, original work.
- assets/opera/jobs/painter/opera_painter_pot_{0,1,2}.glb, opera_painter_easel.glb — original work (this project), CC0-equivalent. Built programmatically (assets_src/blender/build_opera_floor3.py + opera_shared.py, Blender 5.0 bpy) from the project's accepted flat cards. Modifications: n/a (new).
- assets/opera/jobs/astronaut/opera_astronaut_{tank,rocket,valve}.glb — original work, same source/tooling as above.
- assets_src/blender/opera_floor3_2026-07-22.blend — Blender source for the above, original work.
- assets/opera/jobs/{painter,astronaut,racer,popstar}/opera_*_outfit.glb, assets/opera/jobs/popstar/opera_popstar_microphone.glb — original work (this project), CC0-equivalent. Built programmatically (assets_src/blender/build_opera_outfits_floor3.py + opera_shared.py, Blender 5.0 bpy) from the project's accepted flat cards. Modifications: n/a (new).
- assets_src/blender/opera_outfits_floor3_2026-07-22.blend — Blender source for the above, original work.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/{caribbean_nautical_live_replacements.png,norwegian_rock_kelp_live_replacements.png,rejected/caribbean_nautical_plinth_v1.png} — original project-generated review/model-reference art made with OpenAI built-in image generation; exact prompts and initial rejection history in `PROMPTS.md`; no external or protected reference images, runtime replacement, or legacy deletion; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_01_pearl_shell_throne.png — original project-generated 1536x1024 item-01 model-reference turnaround made with OpenAI built-in image generation; prompt family A in `REGEN_35_PROMPT_PLAN.md`; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_02_03_vehicles.png — original project-generated 1536x1024 items-02–03 go-kart/motorcycle model-reference sheet made with OpenAI built-in image generation; prompt family B in `REGEN_35_PROMPT_PLAN.md`; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_04_06_crystal_family.png — original project-generated 1536x1024 items-04–06 crystal-family model-reference sheet made with OpenAI built-in image generation; prompt family C in `REGEN_35_PROMPT_PLAN.md`; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/{regen_07_crystal_castle.png,rejected/regen_07_crystal_castle_clutter_v1.png} — original project-generated 1536x1024 item-07 crystal-castle model-reference iterations made with OpenAI built-in image generation; corrected prompt family D and rejection reason in the concept handoff docs; the rejected draft added loose foundation clutter; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_08_serving_tray.png — original project-generated 1536x1024 item-08 serving-tray model-reference sheet made with OpenAI built-in image generation; prompt family E in `REGEN_35_PROMPT_PLAN.md`; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/{regen_09_10_butterflies.png,rejected/regen_09_10_butterfly_pose_anatomy_v1.png} — original project-generated 1536x1024 items-09–10 butterfly model-reference iterations made with OpenAI built-in image generation; corrected prompt family F and rejection reason in the concept handoff docs; the rejected draft lacked a reliable closed pose and consistent leg anatomy; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_11_pearl_castle_bed.png — original project-generated 1536x1024 item-11 pearl-castle bed model-reference sheet made with OpenAI built-in image generation; prompt family G in `REGEN_35_PROMPT_PLAN.md`; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_20_22_castle_live_modules.png — original project-generated 1536x1024 items-20–22 confirmed-live modular castle model-reference sheet made with OpenAI built-in image generation; prompt family J in `REGEN_35_PROMPT_PLAN.md`; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_23_28_castle_pending_modules.png — original project-generated 1536x1024 items-23–28 concept-only modular castle sheet made with OpenAI built-in image generation; prompt family J in `REGEN_35_PROMPT_PLAN.md`; 3D commission remains held pending the workorder's required callsite verification; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_29_32_park_and_rooted_hedges.png — original project-generated 1536x1024 items-29–32 park and rooted-hedge model-reference sheet made with OpenAI built-in image generation; prompt family K in `REGEN_35_PROMPT_PLAN.md`; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/regen_33_35_pearl_furniture.png — original project-generated 1536x1024 items-33–35 pearl-furniture model-reference sheet made with OpenAI built-in image generation; prompt family L in `REGEN_35_PROMPT_PLAN.md`; no external or protected reference image; generated 2026-07-22.
- assets_src/concepts/cc0_ocean_replacements_2026-07-22/context_{caribbean_reef_density,norway_kelp_coldwater_coral_zones}.png — original project-generated 1536x1024 context-only ecosystem density/placement boards made with OpenAI built-in image generation; ecological fact sources recorded in `ECOLOGY_SOURCES.md`; no reference images or copied source pixels; not Regen roles and not runtime assets; generated 2026-07-22.

## assets_src/concepts/opera_jobs_2p5d_2026-07-24/*.png (24 images) and audit/opera_job_2p5d_contact_sheet_2026-07-24.png
- Source: project-authored concept art generated with OpenAI built-in image
  generation on 2026-07-24; prompts and generation identifiers are recorded
  in `assets_src/concepts/opera_jobs_2p5d_2026-07-24/PROMPTS.md`
- License: project original
- Modifications: accepted scene keys were high-quality resampled from
  1672x941 to 1024x576; accepted environment kits were high-quality resampled
  from 1254x1254 to 1024x1024; the contact sheet is a 1024x1024 composite of
  the accepted images; rejected iterations were not added
- External reference images: none; established project palette and existing
  project-owned Opera job art were used as the style/continuity contract

## assets_src/concepts/opera_jobs_hybrid_finales_2026-07-24/*.png (12 images) and audit/opera_job_hybrid_finale_contact_sheet_2026-07-24.png
- Source: project-authored concept art generated with OpenAI built-in image
  generation on 2026-07-24; prompts and generation identifiers are recorded
  in `assets_src/concepts/opera_jobs_hybrid_finales_2026-07-24/PROMPTS.md`
- License: project original
- Modifications: accepted source images were high-quality resampled from
  1672x941 to 1024x576; the contact sheet is a 1024x1024 composite of the
  twelve accepted images; rejected iterations were not added
- External reference images: none; only established project-owned Mermaid
  Roshan, Opera, outfit, implement, and boss art informed continuity

## assets/art35/opera/*.glb (10 models: arch, curtain, door, medallion, chandelier, bench, railing, lift, maestro, stage_apron)
- Source: project-authored, generated procedurally in Blender by
  tools/build_opera_house_art.py (Codex design pass, 2026-07-21)
- License: project original
- Modifications: n/a (original work); flat toon materials, no textures
- 2026-07-21 addendum: Codex per-act packs added by the same generator
  (dragon, phantom, lantern, crate + lid, silly fish, tiara chest) —
  project original, no textures

## assets/art35/cards/**/*.glb (135 storybook-cutout conversions)
- Source: the project's own flat card art (assets_src/style_review_*,
  assets_src/imagegen chroma pass, assets/props/gen2, assets/mg), converted
  to alpha-clipped extruded cutout GLBs by tools/convert_flat_cards_to_glb.py
  (Blender); NPOT textures resized to POT <=1024 during conversion
- License: project original (derivatives of already-licensed project art)
- Modifications: card mesh + solidify extrusion; texture resize where needed

## Sky Lagoon 2.5D promenade (Codex sprite pass, 2026-07-26)
- `assets/sprites/sky_lagoon/sky_lagoon_plane.png` — project-original
  OpenAI image generation; the project-owned pearl plane in
  `opening_cinematic_test.ogv` was the visual reference; chroma removed and
  resized to 1024px.
- `assets/sprites/sky_lagoon/sky_lagoon_slide.png` — project-original OpenAI
  image generation; corrected playground design with a separate straight
  ladder, horizontal rungs, top platform, and unobstructed aqua chute; chroma
  removed and resized to 1024px.
- `assets/sprites/sky_lagoon/sky_lagoon_swing.png` — project-original OpenAI
  image generation; two-seat shell swing; chroma removed and resized to 1024px.
- `assets/sprites/sky_lagoon/sky_lagoon_seesaw.png` — project-original OpenAI
  image generation; symmetric shell seesaw; chroma removed and resized to
  1024px.
- `assets/sprites/sky_lagoon/sky_lagoon_castle_gate.png` — project-original
  OpenAI image generation; pearl castle and lowered drawbridge; chroma removed
  and resized to 1024px.
- `assets/sprites/sky_lagoon/sky_lagoon_activity_frame_v2.png` —
  project-original OpenAI image generation; lavender shell activity frame;
  chroma removed and resized to 1024px.
- `assets/sprites/sky_lagoon/sky_lagoon_roshan.png` — project-original
  derivative of `assets/characters/roshan_sprite.png`; OpenAI image edit
  changed only the white background to a flat chroma key, followed by local
  alpha extraction and resizing to 1024px; used as the unshaded in-world
  Sprite3D card while the source character art remains unchanged.
- `assets/sprites/sky_lagoon/sky_lagoon_pnw_fir_sway.png` —
  project-original derivative of
  `assets_src/concepts/sky_lagoon_pnw_flat/lagoon_tree_douglas_fir.png`;
  OpenAI image edit replaced only the navy source background with a flat
  chroma key, followed by local alpha extraction and resizing to 1024px.
- `assets/sprites/sky_lagoon/sky_lagoon_pnw_currant_sway.png` —
  project-original derivative of
  `assets_src/concepts/sky_lagoon_pnw_flat/lagoon_shrub_red_flowering_currant_a.png`;
  OpenAI image edit replaced only the navy source background with a flat
  chroma key, followed by local alpha extraction and resizing to 1024px.
- `assets/sprites/sky_lagoon/sky_lagoon_cloud_family_drift.png` —
  project-original OpenAI image generation matching the approved Sky Lagoon
  panorama cloud language; generated on a flat chroma key, locally
  alpha-extracted, and resized to 1024px.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_swing_0.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon swing references; centered two-hand grip pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_swing_1.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon swing references; back-pump seated pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_swing_2_v2.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon swing references; forward-pump seated pose; the 2026-08-09 revision removes only a detached right-edge generation artifact and preserves the complete original figure pixels.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_swing_3_v2.png` — project-original OpenAI built-in image generation derived from the approved clipped swing frame; high-arc two-fist pose regenerated as a complete 2D storybook cutout, chroma-extracted and whole-canvas resized to 512px. Native source, prompt record, and hashes are under `assets_src/imagegen/roshan_playground_cutoff_2026-08-09/`.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_slide_0.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon slide references; compressed ladder-step pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_slide_1.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon slide references; extended ladder-step pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_slide_2_v2.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon slide references; seated-at-lip pose; the 2026-08-09 revision removes only a detached right-edge generation artifact and preserves the complete original figure pixels.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_slide_3_v2.png` — project-original OpenAI built-in image generation derived from the approved clipped slide frame; seated chute-ride pose regenerated as a complete 2D storybook cutout, chroma-extracted and whole-canvas resized to 512px. Native source, prompt record, and hashes are under `assets_src/imagegen/roshan_playground_cutoff_2026-08-09/`.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_0.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon seesaw references; low-seat two-hand pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_1.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon seesaw references; rising two-hand pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_2.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon seesaw references; high-seat two-hand pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_3.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon seesaw references; descending two-hand pose; local chroma extraction and 512px crop.
- `assets_src/imagegen/roshan_playground_cutoff_2026-08-09/roshan_slide_3_native_chroma.png` and `roshan_swing_3_native_chroma.png` — project-original OpenAI built-in image-generation preservation masters for the accepted 2D playground cutoff repairs; excluded from export. Exact prompts, processing, and SHA-256 provenance are in the adjacent `PROMPTS.md`.
- `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_3x1.png` —
  project-original OpenAI image generation; native 2172×724 exact-3:1 master
  flowing from the blocked-water runway shore, through a bounded playground
  meadow, to the coherent pearl castle, Mermaid Roshan stained glass,
  drawbridge, and elevated mountain-pass path. Generated from the prior
  panorama, project pearl-castle facade sheet, historical stained-glass
  visual, and PNW tree/shrub references; preserved without scaling or crop.
- `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_0.png` —
  project-original lossless crop of the native master, rectangle
  `(0, 0, 724, 724)`; no scaling, padding, overlap, or content change.
- `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_1.png` —
  project-original lossless crop of the native master, rectangle
  `(724, 0, 724, 724)`; no scaling, padding, overlap, or content change.
- `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_2.png` —
  project-original lossless crop of the native master, rectangle
  `(1448, 0, 724, 724)`; no scaling, padding, overlap, or content change.
- Style references for every new asset: project-owned
  `sky_lagoon_pnw_tree_prototypes_flat_2026-07-21.png` and
  `sky_lagoon_pnw_shrub_variants_flat_2026-07-21.png`; no external assets.

## Animated dust-bunny enemy (Codex sprite pass, 2026-07-27)

- `assets_src/concepts/dust_bunny_animated_2026-07-27/references/*.png` —
  exact lossless copies of the project-original dust-bunny `curl_ears` and
  `hop` sprites recovered from commit `32eba2ea` on
  `origin/codex/dirty-castle-2d`; no modification.
- `assets_src/concepts/dust_bunny_animated_2026-07-27/chroma/*.png` —
  project-original OpenAI built-in image generations derived only from those
  approved project references and generated dust-bunny atlas continuity;
  six-frame idle, hop, and accepted cleaning-poof atlases normalized to
  768x512; rejected soft-dissolve iteration retained under `rejected/`;
  exact prompts retained beside the sources.
- `assets/sprites/dust_bunnies/*.png` — locally chroma-keyed transparent
  derivatives of those generated atlases; three mobile runtime textures,
  768x512 with six 256x256 frames each.
- `assets/sprites/dust_bunnies/dust_bunny_clean_bubbles.png` — exact lossless
  copy of project-original
  `assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png` recovered from
  commit `32eba2ea` on `origin/codex/dirty-castle-2d`; used as the unshaded
  CLEAN projectile in the live Pearl Castle dungeon encounter; no modification.
- `assets_src/concepts/dust_bunny_animated_2026-07-27/rainbow_dust_bunny_concept.png`
  — project-original OpenAI built-in image generation derived only from the
  approved project curl-ear dust-bunny identity; pastel rainbow color-variant
  concept with prismatic forehead sparkle, locally resized to 1024x1024; exact
  prompt retained beside the source; not used by the runtime.
- `assets_src/concepts/dust_bunny_animated_2026-07-27/dust_bunny_first_boss_concept.png`
  — project-original OpenAI built-in image generation derived only from the
  approved project curl-ear dust-bunny identity; large grey-purple first-boss
  concept with layered storm-cloud curls, oversized spiral ears, and a
  lavender curl-crest sparkle, locally resized to 1024x1024; exact prompt
  retained beside the source; not used by the runtime.
- `assets_src/concepts/dust_bunny_animated_2026-07-27/dust_bunny_first_boss_concept_v2_teeth.png`
  — project-original OpenAI built-in image edit of the grey-purple first-boss
  concept; preserves the complete boss design while adding a compact plum grin
  with exactly two short pointed pearl teeth, locally resized to 1024x1024;
  exact prompt retained beside the source; preferred concept, not used by the
  runtime.
- `assets_src/concepts/dust_bunny_animated_2026-07-27/boss_chroma/*.png`
  - project-original OpenAI built-in image generations derived only from the
  approved grey-purple toothed dust-bunny boss and the same generated animation
  continuity; five four-frame sheets (jump, vulnerable laugh, flinch, angry,
  implosion) normalized to mobile-safe 1024x1024; exact prompts and frame intent
  retained in `BOSS_ANIMATION_DESIGN.md`.
- `assets/sprites/dust_bunnies/boss/*.png` - locally chroma-keyed transparent
  RGBA derivatives of the five boss animation sheets; 1024x1024 with four
  512x512 frames each; used only by the unshaded `DustBunnyBossSprite` 2D card.
- `DustBunnyBossSprite.angry_jump_final` - project-original runtime-only atlas
  sequence assembled without new pixels from approved angry frames 3-4 and
  jump frames 2 and 4. It is the more powerful final-round jump presentation;
  no new generated source, external asset, duplicated texture, or additional
  license applies.
- `tools/process_dust_bunny_boss_animation.py` - project-original deterministic
  source normalization and alpha-validation utility for those sheets; no
  external assets or code.
- License: project original derivative art for this personal game,
  CC0-equivalent.

## Sky Lagoon congruency rebuild (Codex sprite pass, 2026-07-27)
- `assets_src/sky_lagoon/congruency_rebuild_2026-07-27/*.png` — project-original
  OpenAI built-in image-generation sources and rejected audit iterations;
  generation identifiers, reference roles, and rejection reasons are recorded
  in that directory's `README.md`; license: project original; external
  references: none.
- `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v2_3x1.png` —
  project-original 2172×724 exact-3:1 native repaint generated from the prior
  approved project mural; no scaling, crop, padding, extension, letterbox, or
  aspect-ratio change.
- `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v2_tile_{0..3}.png`
  — four project-original lossless non-overlapping crops of the v2 master,
  rectangles `(0,0,543,724)`, `(543,0,543,724)`, `(1086,0,543,724)`, and
  `(1629,0,543,724)`; no scaling or overlap.
- `assets/sprites/sky_lagoon/{sky_lagoon_activity_frame_v3.png,sky_lagoon_castle_gate_v3.png,sky_lagoon_slide_v3.png,sky_lagoon_swing_v3.png,sky_lagoon_plane_v4_audited_360.png,sky_lagoon_seesaw_v4.png,sky_lagoon_cloud_family_v5_audited.png}`
  — project-original OpenAI-generated matte storybook Sprite3D cutouts;
  flat chroma removed locally, transparent bounds padded, authored density
  reduced to the scene-congruency budget, and final luminance/matte grading
  applied where recorded by the audit.
- `assets/sprites/sky_lagoon/{sky_lagoon_pnw_fir_sway_v2.png,sky_lagoon_pnw_currant_sway_audited.png}`
  — project-original derivatives of the existing accepted PNW sprite pack;
  only authored density plus a small cool/matte grade changed; source sprites
  remain unchanged.
- `assets/sprites/sky_lagoon/sky_lagoon_roshan_runtime_audited.png` —
  project-original derivative of the existing protected Mermaid Roshan sprite;
  only downsampling and a non-destructive matte filter reduced oversampling and
  baked highlights; character design and protected source remain unchanged.
- `assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png` —
  project-original 256×128 translucent contact-shadow sprite generated locally
  by `tools/prepare_sky_lagoon_congruency_assets.py`; used only on unshaded
  Sprite3D cards.
- `assets/sprites/sky_lagoon/{sky_lagoon_slide_v3_compact.png,sky_lagoon_swing_v3_compact.png,sky_lagoon_seesaw_v4_compact.png}`
  — project-original, lossless-alpha compact derivatives of the approved
  playground sprites; downsampled once to match their smaller Sprite3D display
  size while preserving the accepted shapes, palette, and transparent bounds.

## Sky Lagoon 6x2 HD panorama and silhouette-fit pass (Codex, 2026-07-28)
- `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v3_hd_3x1.png`
  — project-original 6144×2048 exact-3:1 master assembled from twelve OpenAI
  built-in image-generation detail repaints. Each repaint used one exact
  square crop of the approved v2 master as a strict composition reference;
  a local seam-safe edge blend preserved the approved boundary geometry.
  License: project original; external references: none.
- `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v3_tile_r{0..1}_c{0..5}.png`
  — twelve lossless, non-overlapping 1024×1024 runtime crops of the v3 master;
  no runtime scaling, padding, overlap, or ratio change. Rectangle and hash
  evidence is recorded in `audit/sky_lagoon_hd_grid.json`.
- `assets/sprites/sky_lagoon/{sky_lagoon_plane_v5_hd_grade.png,sky_lagoon_cloud_family_v7_hd_grade.png}`
  — project-original luminance-only derivatives of the approved plane and
  drifting-cloud cards, adjusted to the new HD plate without changing their
  silhouettes, composition, or alpha.
- `assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png` — project-original
  density-matched derivative of the approved seesaw cutout, downsampled once
  for its final non-overlapping Sprite3D display size; design and alpha
  silhouette are unchanged.

## Sky Lagoon tree-card and cloud-clearance correction (Codex, 2026-07-28)
- `assets_src/sky_lagoon/tree_card_rebuild_2026-07-28/*.png` — project-original
  OpenAI built-in image-generation edit sources. Inputs were approved Sky
  Lagoon mural tiles and PNW visual language; no external references. Prompts
  and exact source/output roles are recorded in that directory's README.
- `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v4_hd_3x1.png` —
  project-original 6144x2048 exact-3:1 derivative of the v3 master. Only
  columns 0, 1, and 4 were selectively repainted to remove water-rooted or
  duplicate foreground trees and restore occluded scenery. No crop, padding,
  extension, or ratio change.
- `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v4_tile_r{0..1}_c{0..5}.png`
  — twelve lossless non-overlapping 1024x1024 crops of the v4 master, used as
  unshaded Sprite3D cards. Tile rectangles and hashes are in
  `audit/sky_lagoon_hd_grid.json`.
- `assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_{tall,medium,slender}_v1.png`
  — project-original OpenAI-generated transparent PNW evergreen card family
  derived from approved mural trees. Local checker removal, alpha crop,
  density reduction, and matte/value grading only.
- `assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png` — project-original
  lossless-alpha crop of one cloud from the approved
  `sky_lagoon_cloud_family_v7_hd_grade.png`; no redesign.

## Sky Lagoon reductive 6x2 clean-plate rebuild (Codex, 2026-07-28)
- `assets_src/sky_lagoon/reductive_rebuild_2026-07-28/**` — project-original
  OpenAI built-in image-generation edit sources, overscan references, prompt
  ledger, and deterministic assembly inputs derived from the approved Sky
  Lagoon panorama. `stained_glass_owner_reference.png` is owner-supplied
  project art copied without modification from the file named in the task.
  License: project-owned / owner-supplied; external references: none.
- `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png` —
  project-original 6144x2048 exact-3:1 clean plate assembled from twelve
  native detail edits with 115px generated overscan. The layout, route,
  mountain, off-road cabins, shoreline, and playground clearing derive from
  the approved panorama; only baked-in castle and selected foreground trees
  were removed for separate Sprite3D depth cards.
- `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r{0..1}_c{0..5}.png`
  — twelve lossless, non-overlapping 1024x1024 runtime crops of the v5 master.
  Four cards reconstruct each native 2048x2048 playable screen.
- `assets/sprites/sky_lagoon/sky_lagoon_castle_stained_glass_v1.png` —
  project-original OpenAI built-in extraction of the approved 2D storybook
  castle and drawbridge. The window contents are the exact owner-supplied
  stained-glass reference, deterministically fitted inside the existing gold
  frame with no pixel changes elsewhere on the castle card.
- `assets_src/sky_lagoon/castle_symmetry_2026-07-29/**` — project-original
  OpenAI built-in castle-design studies using only the approved v1 runtime card
  and approved pearl-castle turnaround. The two-tower studies were rejected for
  shrinking the landmark, omitting the intended four-tower hierarchy, and
  weakening the established scene placement; they are retained outside runtime
  loading as design evidence. No external references; generated 2026-07-29.
- `assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v3.png` —
  project-original four-tower completion of the approved Sky Lagoon castle,
  produced with OpenAI built-in image editing from the approved v1 card only.
  The final card has two lower outer towers, two taller inner towers, the exact
  owner-supplied stained-glass source restored inside its frame, and no added
  lighting or post effect. Chroma removal, mobile downscaling, and placement
  fitting are deterministic in `tools/prepare_sky_lagoon_castle_symmetry.py`;
  runtime width, waterline, and bridge landing match the approved fallback.
  No external references; generated and prepared 2026-07-29.
- `assets_src/sky_lagoon/castle_symmetry_2026-07-29/frame_restore_ring_source.png`
  — 249x360 project-original crop from an OpenAI built-in precision-edit
  candidate derived only from the approved v3 and v1 castle cards. The rejected
  full candidate is not shipped; only its bounded clean lavender/gold window
  surround is retained for the deterministic preparation tool.
- `assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png` —
  non-destructive v3 derivative that replaces only the audited stained-glass
  surround with the bounded clean-frame repair. The four-tower silhouette,
  door, bridge, placement contract, and neutral base lighting remain unchanged.
- `assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png` —
  deterministic 199x228 alpha mask cropped from the v4 castle door footprint;
  used only for reversible touch feedback so no full-castle duplicate is drawn.
  No external source or newly painted subject pixels.

## Sky Lagoon playground fit revision (Codex, 2026-07-29)
- `assets_src/sky_lagoon/playground_revision_2026-07-29/**` — project-original
  OpenAI built-in image-generation sources and prompt ledger derived only from
  project-owned Sky Lagoon and Mermaid Roshan references. License:
  project-generated art; external references: none.
- `assets/sprites/sky_lagoon/sky_lagoon_swing_single_mermaid_v1.png` —
  project-original single-seat mermaid swing generated with Codex built-in
  image generation; chroma removed locally and downsampled once from the
  preserved 1338×1176 alpha master to a 655×576 mobile runtime Sprite3D card.
- `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png`
  and `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c{0,1}.png`
  — the approved 6144×2048 panorama and two affected lossless runtime tiles,
  rebuilt with a project-original localized Codex image edit that removes the
  oversized conifer stamp at the screen-one/screen-two bush transition.

## Sky Lagoon living-card fireplace smoke (Codex, 2026-07-29)
- `assets_src/sky_lagoon/living_card_v2_2026-07-29/**` — project-original
  OpenAI built-in image-generation sources, rejected visual trials, accepted
  alpha master, exact prompts, dimensions, hashes, and attempt ledger. No
  external references. License: project original.
- `assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png` — project-original
  46×256 lossless-alpha thin fireplace-smoke wisp, locally chroma-isolated
  and Lanczos-downsampled from the accepted generated source for use as three
  staggered unshaded Sprite3D cards at the mountain cabin chimney.

## Pearl Opera 2D career worlds and rivals (Codex, 2026-07-29)
- `assets_src/concepts/opera_rivals_2026-07-29/authoritative_boxer_imp_reference.png`
  — owner-supplied project character reference, copied byte-for-byte from
  `Generated image 8 (1).png` for local provenance. External source/license:
  owner-supplied project art; no public redistribution claim added.
- `assets_src/concepts/opera_rivals_2026-07-29/opera_rival_boxer_match_master.png`
  — project-authorized OpenAI image edit of that exact owner-supplied
  reference. Modifications: preserved face/horns/body identity; replaced the
  focus mitt with a second glove; removed chest target and pearl belt; plain
  teal waistband; no shell/pearl/ocean motif.
- `assets/opera/rivals/opera_rival_boxer_match.png` and
  `assets/opera/worlds/actors/rival_boxer.png` — non-destructive 1024×1024
  transparent runtime derivatives of the accepted boxer master, prepared by
  `assets_src/concepts/opera_rivals_2026-07-29/prepare_boxer_match_asset.py`
  and `tools/prepare_opera_2d_worlds.py`. Exactly two plain boxing gloves; no
  focus mitt, target, shell, pearl, badge, crest, logo, or marine emblem.
- `assets_src/concepts/opera_rivals_2026-07-29/opera_rival_costume_sheet_master.png`
  — project-original OpenAI image generation based only on the owner-supplied
  imp identity reference. Eleven fixed costume cells: pastry chef, detective,
  ballerina, candy maker, doctor, farmer, magician, painter, astronaut
  engineer, racecar driver, and pop star. Exact constraints and derivation are
  recorded in the adjacent `README.md`; no external assets; all marine
  ornament explicitly excluded.
- `assets/opera/worlds/actors/rival_{chef,detective,ballerina,candymaker,doctor,farmer,magician,painter,astronaut,racer,popstar}.png`
  — deterministic 512×512 transparent slices of the accepted costume sheet.
  Neutral checker presentation removed and cells aspect-fitted by
  `tools/prepare_opera_2d_worlds.py`; no generative reinterpretation.
- The accepted 1024x576 scene keys remain only in `assets_src/concepts/opera_jobs_2p5d_2026-07-24/` as project-owned composition references. They are intentionally not copied or stretched into runtime because they do not meet the 2048px-per-playable-screen background rule.
- `assets/opera/worlds/actors/roshan_{chef,detective,ballerina,candymaker,doctor,farmer,boxer,magician,painter,astronaut,racer,popstar}.png`
  — deterministic 512×512 transparent runtime derivatives of the accepted
  outfit hero cards in
  `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/`. Modifications:
  remove only edge-connected navy presentation field/card border, crop, and
  Lanczos aspect-fit; protected character originals unchanged.
- `assets/opera/rivals/opera_rival_{chef,detective,ballerina,candymaker,doctor,farmer,boxer,magician,painter,astronaut,racer,popstar}.glb`,
  `assets_src/blender/build_opera_rival_imps.py`, and
  `assets_src/blender/qa_opera_rivals/*.png` — preserved project-original
  low-poly fallback/review package derived from
  `assets/dungeon/mischief_imp.glb`. Normal 2D career-door play does not load
  these identity-mismatched QA portraits.
- `assets_src/concepts/opera_rivals_2026-07-29/rejected/*.png` — rejected,
  review-only generated iterations retained for provenance and excluded from
  runtime loading.
- `assets/opera/worlds/props/goal_{chef,detective,ballerina,candymaker,doctor,farmer,boxer,magician,painter,astronaut,racer,popstar}.png`
  — deterministic 512×512 transparent runtime derivatives of one accepted
  gameplay card per career from
  `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/` (the act's goal
  prop, 2026-08-01). Modifications by `tools/prepare_opera_2d_props.py`:
  remove only the edge-connected navy presentation field/card border, crop,
  and Lanczos aspect-fit; source cards unchanged.
- `assets/opera/worlds/actors/imp_{mischief,captain}.png` — project-original
  BASIC placeholder sprites drawn from simple shapes by
  `tools/prepare_opera_2d_props.py` (2026-08-01) for the career-world imp
  scuffle beats; scheduled for replacement by codex mischief-imp sprites per
  OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md. No external sources.
<!-- rows removed 2026-07-28 (asset purge, claude/asset-purge-dead-3d): kits/play (Tiny Treats Fun Playground), assets/sky HDRs (Poly Haven Qwantani day/dusk) - files deleted from repo -->

## Pearl Castle 2.5D room references and derived cards (2026-07-26)

The eight 1024×576 composites below are preserved approved references and the
source of the structurally validated prototype cards. They are not accepted
native-2K masters under the corrected exact-source-ratio gate; no rejected
generator output is present in this directory or connected to runtime art.
- `assets/flats/castle/rooms/room_main_hall.png` — project-authored Pearl Castle presentation render, original project art; resized to 1024×576 for mobile runtime use.
- `assets/flats/castle/rooms/room_opera_hall.png` — original OpenAI ImageGen artwork generated for Mermaid Roshan: Reef of Light from the project-authored opera-gate and Main Hall references; rebuilt as a wide navigable stage and resized to 1024×576.
- `assets/flats/castle/rooms/room_library.png` — original OpenAI ImageGen artwork generated for Mermaid Roshan: Reef of Light from the project-authored library and Main Hall references; rebuilt as a wide navigable stage and resized to 1024×576.
- `assets/flats/castle/rooms/room_playroom.png` — original OpenAI ImageGen artwork generated for Mermaid Roshan: Reef of Light from the project-authored toy-room and Main Hall references; rebuilt as a wide navigable stage and resized to 1024×576.
- `assets/flats/castle/rooms/room_craft_room.png` — original OpenAI ImageGen artwork generated for Mermaid Roshan: Reef of Light from the project-authored craft-room and Main Hall references; rebuilt as a wide navigable stage and resized to 1024×576.
- `assets_src/castle/room_regenerations/room_kitchen_fullframe_v2_1672x941.png` — original complete full-frame OpenAI built-in ImageGen regeneration for Mermaid Roshan: Reef of Light, using the prior Royal Kitchen composite as the composition/style reference; removes the two incompatible ocean-view windows, retains one small opaque shell light inset, and adds the gameplay-critical mint refrigerator; native generation preserved at 1672×941 with SHA-256 `8faa4e15e60503cb0303434b77461fa559a81c3d021eb6c3165e9ed176bfbf3e`; prompt and audit record retained beside it in `room_kitchen_fullframe_v2_provenance.md`; generated 2026-07-29.
- `assets_src/castle/room_regenerations/room_kitchen_kettle_single_spout_chroma.png`, `room_kitchen_kettle_single_spout.png`, and `room_kitchen_fullframe_v3_1672x941.png` — project-original OpenAI built-in ImageGen single-object correction of the v2 stove-kettle defect; the accepted isolated golden kettle has exactly one right-side spout, was hard-key alpha extracted with despill and one-pixel contraction, and was composited only over the restored old-kettle footprint by `tools/repair_kitchen_kettle.py`; native source, exact prompt, hashes, rejected-method note, and production method are recorded in `room_kitchen_fullframe_v3_provenance.md`; generated and integrated 2026-07-29.
- `assets/flats/castle/rooms/room_kitchen.png`, `room_kitchen_background.png`, `room_kitchen_front_left.png`, `room_kitchen_front_right.png`, `room_kitchen_item_sink.png`, `room_kitchen_item_oven.png`, `room_kitchen_item_pan_1.png` through `room_kitchen_item_pan_4.png`, `room_kitchen_item_fridge.png`, `assets_src/castle/room_backgrounds_2k/room_kitchen_background_2k.png`, and `assets/flats/castle/rooms/background_tiles/room_kitchen_background_r*_c*.png` — deterministic derivatives of the preserved Kitchen v3 full-frame source; normalized to the 1024×576 logical stage, separated into outline-refined Sprite3D cards, and whole-canvas Lanczos enlarged to a 4096×2304 background master split into twelve non-overlapping 1024×768 runtime tiles; generated 2026-07-29 by `tools/build_castle_room_layers.py` and `tools/build_castle_room_2k_tiles.py`.
- `assets_src/imagegen/mermaid_pool_room_2026-08-02/room_mermaid_pool_fullframe_v2_native.png`, `room_mermaid_pool_fullframe_v3_native.png`, `room_mermaid_pool_fullframe_v3_prompt.txt`, and adjacent `PROVENANCE.md` — project-original OpenAI built-in ImageGen full-frame Mermaid Pool regenerations; v2 restores the continuously visible rainbow waterfall, removes the dry shell-gate device and ambiguous pipe fixture, and introduces one coherent seahorse fountain; v3 preserves those accepted interaction subjects while enlarging the pool into a broad rounded foreground lagoon. Native sources, exact prompts, references, methods, and SHA-256 values are preserved; generated 2026-08-02.
- `assets/flats/castle/rooms/room_mermaid_pool.png`, `room_mermaid_pool_background.png`, `room_mermaid_pool_{front_left,front_right,mid_pool}.png`, `room_mermaid_pool_item_{waterfall,flower_float,star_float,seahorse_fountain}.png`, `assets_src/castle/room_backgrounds_2k/room_mermaid_pool_background_2k.png`, and `assets/flats/castle/rooms/background_tiles/room_mermaid_pool_background_r*_c*.png` — deterministic normalized, outline-refined, healed-plate, depth-card, 3640x2048 master, and eight non-overlapping 910x1024 runtime-tile derivatives of the accepted 2026-08-02 v3 full-frame source; built by `tools/build_castle_room_layers.py` and `tools/build_castle_room_2k_tiles.py`.
- The superseded original Mermaid Pool composite and its dry v2 generated fixture sheets remain in Git/provenance history for audit only; runtime uses the accepted 2026-08-02 complete room and room-derived interaction atlases.
- `assets/flats/castle/rooms/room_bubble_bath.png` — original OpenAI ImageGen artwork generated for Mermaid Roshan: Reef of Light from the Mermaid Pool, Kitchen, and Main Hall style references; authored as a wide room with separated bathtub, sink, and toilet; resized to 1024×576.
- `assets/flats/castle/rooms/room_*_front_*.png` and `room_*_mid_*.png` — exact-pixel alpha crops derived from the corresponding licensed room backdrops by `tools/build_castle_room_layers.py`; no new source artwork.
- `assets/flats/castle/rooms/room_*_item_*.png` — exact-pixel alpha touch-prop crops derived from the corresponding licensed room backdrops by `tools/build_castle_room_layers.py`; no new source artwork.
- `assets/flats/castle/rooms/room_*_background.png` — clean architecture plates derived deterministically from the corresponding full room composites by `tools/build_castle_room_layers.py`; card-owned pixels are replaced only by interpolated surrounding pixels from the same licensed source image, with no generated or external artwork.
- `assets/flats/castle/rooms/room_actor_shadow.png` — project-authored translucent ellipse generated deterministically by `tools/build_castle_room_layers.py`; original project utility art used as an unshaded Sprite3D contact-shadow card.
- `assets/flats/castle/rooms/room_main_hall_item_fountain_{left,right}_v2.png` — project-original derivatives of the richer shell fountain already painted in `audit/castle_sprite3d/main_hall_screen_b_dressed_preview.png`; tight-alpha extraction and one high-quality downsample to the established 1024-wide runtime scale by `tools/build_castle_item_style_replacements.py`; right instance mirrored; no external or newly generated object design.
- `assets/flats/castle/rooms/room_main_hall_background_v2.png` — deterministic same-source repair of the existing Main Hall clean plate by `tools/build_castle_item_style_replacements.py`; only the padded alpha silhouettes vacated by the two legacy pedestal fountains are refilled from surrounding pixels in the immutable project-owned room composite; original clean plate preserved; no external or generated art.
- `audit/castle_sprite3d/main_hall_2x4_max_native_candidates/*.png` and the associated contact, invariance, and seam proofs — project-authored rejected fidelity candidates generated with OpenAI built-in ImageGen on 2026-07-28 from the project-owned Main Hall cell crops and full-screen context; preserved for audit only, never connected to runtime; exact hashes, dimensions, prompts, and rejection evidence are recorded beside them.
- `audit/castle_sprite3d/main_hall_screen_{a,b}_cleanup_candidate.png` — project-authored OpenAI built-in ImageGen precision edits of the corresponding tightened Main Hall composition proofs; only mixed destination-room furniture and the Screen B fountain obstructing the Stuffie approach were removed, with same-source wall/floor restoration and no replacement prop design; audit-only, below the native-2K runtime gate. `main_hall_screen_{a,b}_clear_preview.png` composites those candidates only inside explicit feathered edit masks, preserving all outside pixels byte-for-byte from the tightened references. `main_hall_2x1_interface_concept_clear.png`, `main_hall_door_clearance_audit.png`, `main_hall_dressing_invariance_audit.png`, the 2×4 preview tiles, and exact reconstructions are deterministic review derivatives made by `tools/audit_castle_hall_dressing.py` and `tools/slice_castle_hall_2x4.py`.
- `audit/castle_sprite3d/main_hall_screen_{a,b}_polish_candidate.png` and `main_hall_screen_a_foreground_cleanup_candidate.png` — project-authored OpenAI built-in ImageGen precision edits made on 2026-07-28 from the approved project-owned Main Hall screens; used only inside documented sign/banner and old-fountain masks, with no generated replacement prop. `main_hall_screen_{a,b}_polished_base.png`, interaction layers, full-resolution play previews, and the audit board are deterministic composites made by `tools/build_castle_hall_polish_interactions.py`; audit-only and below the native-2K runtime gate.
- `audit/castle_sprite3d/main_hall_touch_pearl_shell.png` and `main_hall_touch_wishing_star.png` — project-original derivatives made by `tools/build_castle_hall_polish_interactions.py` from the already licensed Main Hall v2 fountain and `assets/mg/star.png`; respectively an exact crop and one high-quality downsample, with no external source art.

## Pearl Castle room-led two-screen Main Hall (2026-07-28)

- `assets/flats/castle/main_hall_2screen/main_hall_screen_{a,b}_room_led_master.png`
  — project-original 2048x1153 background masters generated with OpenAI
  built-in ImageGen from the project's approved two-screen Main Hall art and
  the existing Kitchen, Library, Opera, Playroom, Craft, Pool, and Bath room
  paintings. No external reference art. The native-detail assembly and repair
  process used only unscaled native generator pixels; dimensions, hashes,
  prompts, rejected passes, crop rectangles, and seam evidence are recorded in
  `audit/castle_sprite3d/room_led_iterations/` and
  `CASTLE_ROOM_LED_CODEX_IMPLEMENTATION_2026-07-28.md`.
- `assets/flats/castle/main_hall_2screen/tiles/main_hall_room_led_*.png`
  — lossless, non-overlapping runtime crops of the documented seam-free
  1672x941 view rectangle inside each accepted 2048x1153 master. No scaling,
  padding, interpolation, or new artwork. Exact source rectangles, hashes, and
  pixel-exact reconstruction proofs are recorded in
  `audit/castle_sprite3d/castle_main_hall_2x4_runtime_manifest.json`.
- `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/{dust_bunny_sleepy,dust_bunny_hop,dust_bunny_shell_hide,dust_bunny_family}.png`
  — reused project-original transparent 512x512 cutouts from commit
  `95132b6b310c34aa1d7fba5330d72f36fed9d4d7`; source was OpenAI built-in
  image generation under project storybook direction, with local alpha cleanup
  documented by the original Dirty Castle manifest. Reused unchanged as
  unshaded Sprite3D interaction cards; license remains project original.
- `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_curl_ears.png`
  — project-original transparent 512x512 RGBA cutout
  (sha256 `d88f667724d2c06fc591b00ea91b018430bad1a359e7527124a6e25b0cc6da0f`),
  the large front-facing spiral-eared pose from the same codex dust-bunny cast
  atlas as the four cards above (prompt and chroma/alpha process recorded in
  `assets_src/concepts/dirty_castle_cleanup_2026-07-22/PROMPTS.md`, "Sprite
  atlas 04 — dust-bunny cast"); source was OpenAI built-in image generation
  under project storybook direction. Brought forward unchanged from
  `codex/dirty-castle-2d` — no scaling, recolour, or repaint — and used as the
  Dust Bunny Boss cutout (`scripts/games/dust_boss.gd`,
  `DUST_BUNNY_BOSS_2026-08-02.md`). License: project original.

## Pearl Castle clean two-screen Main Hall redraw (2026-08-03)

All OpenAI ImageGen files in this section are project-owned original art made
only from already approved Mermaid Roshan project references. There is no
external source or URL. Exact prompts, generator-cache paths, reference hashes,
acceptance decisions, and the owner-authorized production transform are in
`assets_src/imagegen/castle_main_hall_redraw_2026-08-03/PROMPTS.md`.

- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/concept_reference_1774x887.png`
  - project-original OpenAI built-in ImageGen two-screen composition reference;
    review-only because its 2:1 canvas is not the playable two-screen ratio;
    SHA-256 `734a26f8ae41157a0a3f070e6cfdd61ed927462ba21f9071c880d46bab1ac618`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/concept_left_reference_887x887.png`
  - deterministic unscaled left-half crop of the project-owned concept above;
    reference-only; SHA-256
    `73de6e4983d2e0cfc9725190836cc7952d41e8c821faa020f9e908a4edb87716`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/concept_right_reference_887x887.png`
  - deterministic unscaled right-half crop of the project-owned concept above;
    reference-only; SHA-256
    `ea728541fd57934a7b973cdf6bb12e77d676cf244dc613004e3ad33a638c60ad`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/rejected_screen_a_square_1254x1254.png`
  - project-original OpenAI built-in ImageGen candidate; rejected for its 1:1
    playable-screen ratio and retained only for provenance; SHA-256
    `1e2b2d8016ac7f3f811755747aec9ca5c4dd8a03bebcf11c884c66385f47d8e5`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/superseded_decorated_screen_a_native_1672x941.png`
  - project-original OpenAI built-in ImageGen left-screen architectural
    intermediate; composition-approved but superseded because detachable props
    were baked into the plate; SHA-256
    `80a8f6d0a01bda6908c1763462acecf5ca96068bdc0a20a133aa31a711bc6a5a`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/superseded_decorated_screen_b_native_1672x941.png`
  - project-original OpenAI built-in ImageGen right-screen architectural
    intermediate; composition-approved but superseded because detachable props
    were baked into the plate; SHA-256
    `2416cd4475b02c31399ed9c7fa6718e779b33d2bb4c6cb3d5fdac2bd70128381`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_a_native_1672x941.png`
  - accepted project-original OpenAI built-in ImageGen clean left architectural
    plate, with detachable props removed and healed in the same approved castle
    style; native generator file preserved unchanged; SHA-256
    `6e840715f1ff580a21e8df3406b5c23733bf584d5046345f7239d72913c04c5d`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_b_native_1672x941.png`
  - accepted project-original OpenAI built-in ImageGen clean right architectural
    plate, generated against the accepted clean left plate for continuity;
    native generator file preserved unchanged; SHA-256
    `7e77e4c29bbbdcaf2230031a760137a28371532debefda971ab1b251df3ee2ad`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/screen_a_production_master_2048x1152.png`
  - deterministic owner-authorized whole-canvas Pillow Lanczos enlargement of
    `accepted_screen_a_native_1672x941.png`; no crop, padding, local edit, seam
    blend, AI upscale, or new artwork; SHA-256
    `577acdf482afb923e888189351501d3db69fcc9e8ae5d5bd401f64aafd76069a`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/screen_b_production_master_2048x1152.png`
  - deterministic owner-authorized whole-canvas Pillow Lanczos enlargement of
    `accepted_screen_b_native_1672x941.png`; no crop, padding, local edit, seam
    blend, AI upscale, or new artwork; SHA-256
    `8726f60df470dacd34ed3bf8d1ea40dba0d374f1f1b0fb1504a99c134e12e885`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/main_hall_production_master_4096x1152.png`
  - preserved intermediate lossless side-by-side stitch of the two 2048x1152
    production masters above; no overlap, scaling, interpolation, or seam
    repair; SHA-256
  `0bed0ed409c966a2bae7505788f91b86725227b16a46054d85aa672963bfc54c`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/screen_a_production_master_3641x2048.png`
  - superseded whole-canvas Pillow Lanczos Screen A attempt retained for
    provenance; rejected because its cumulative native-ratio rounding error was
    1.151 pixels; SHA-256
    `f8b3af85316f0c3e549227a31fe378b83a3500c3379808657c7eac9662fc2c4d`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/screen_b_production_master_3641x2048.png`
  - matching superseded whole-canvas Screen B attempt, retained only for the
    same rejected transform's provenance; SHA-256
    `89915458278908ef9ed105386ad205227496edad828ce97ffe92e9ab9ed02637`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/main_hall_production_master_7282x2048.png`
  - superseded lossless stitch of the two rejected 3641x2048 attempts; retained
    for provenance and never loaded by Godot; SHA-256
    `e3d91bc5119016c5a1c8bd6fe08a4c1d1964cc16497df3f31515d4bdc1f10d31`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/screen_a_production_master_3640x2048.png`
  - accepted final per-screen whole-canvas Pillow Lanczos enlargement of the
    preserved 2048x1152 Screen A intermediate; all native, intermediate, and
    cumulative aspect-ratio steps remain within one-pixel rounding tolerance;
    no crop, padding, local edit, AI upscale, or new artwork; SHA-256
    `46c0a3443029a5699bf440e9abb8289046bd42d4e62195b2d36ce261883eb948`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/screen_b_production_master_3640x2048.png`
  - accepted final Screen B whole-canvas enlargement under the same method,
    authorization, ratio gates, and restrictions; SHA-256
    `ff8b69b80acda82d156086a33c74ae8f5cc8699ed1cf4d6b69239b7058962f46`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/main_hall_production_master_7280x2048.png`
  - accepted final lossless side-by-side stitch of the two 3640x2048 strict
    per-screen 2K masters; no overlap, scaling, interpolation, or seam repair;
    SHA-256 `297cd6d181288ef6cc364a71a89fdb4da168f688249ca910995e71f6f769a9dd`.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/main_hall_strict_2k_build_manifest.json`
  - project-authored deterministic transform, dimension, aspect-ratio, hash,
    tile-rectangle, and invariance ledger for the native, intermediate, final,
    and runtime files in this section; provenance data, not runtime art.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/PROMPTS.md`
  - project-authored generation and acceptance ledger; records prompts, methods,
    source/cache paths, dimensions, hashes, references, rejection reasons, and
    the production resize authorization; provenance data, not runtime art.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/sign_reuse_manifest.json`
  - project-authored deterministic reuse ledger for every sign card below;
    records output hashes, approved source hashes and crop rectangles, alpha
    treatment, the one whole-card Lanczos resize, and the Family Gallery
    badge's exact collection-palette samples and outline radii; it also keeps
    the eight-sign 4.5/5 compatibility scorecard and acceptance decisions;
    provenance data, not art.
- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/throne_reuse_manifest.json`
  - project-authored deterministic reuse ledger for the retained throne card;
    records its approved source rectangle, hashes, alpha audit, unchanged RGB
    pixels, and no-upscale status; provenance data, not art.

The sixteen runtime background cards below are non-overlapping crops of the
licensed 7280x2048 production master. Every card is 910x1024, so each texture
remains within the
1024-pixel runtime limit. They add no pixels and reconstruct the master exactly.
Source rectangles, hashes, and zero-difference evidence are recorded in the
strict 2K build and audit manifests.

- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r0_c0.png`
  - deterministic 910x1024 crop; SHA-256
    `317cdef9249c73bae64d8b0e7c6590a78b5a4f71d3187a2c32e5fa435150c1cb`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r0_c1.png`
  - deterministic 910x1024 crop; SHA-256
    `2584ed2636652871e5a7eeb3400243a61a2676cf966b9e9f652463f424467e22`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r0_c2.png`
  - deterministic 910x1024 crop; SHA-256
    `ee46dfa20f4de0140c8dbfb56eacba2d59acdb8eff684c0c45422fd34862b892`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r0_c3.png`
  - deterministic 910x1024 crop ending exactly at the Screen A boundary;
    SHA-256 `802731a92762c849f9c0597b2e75a6dbc0336dbf60032ee9290867cd4ce7d1a1`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r0_c4.png`
  - deterministic 910x1024 crop; SHA-256
    `9bfa44736244ae50fda10461c48cc0ee0cf35f195dd6e3b59364c6c9756cfc82`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r0_c5.png`
  - deterministic 910x1024 crop; SHA-256
    `d1e4652e644bd5354c5bd779242f885cc58ad0f2a6adc61dff4105d7417fc0ae`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r0_c6.png`
  - deterministic 910x1024 crop; SHA-256
    `17e74663ad7b95414453e106265258642f51b820001a99e0f1882352a96012da`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r0_c7.png`
  - deterministic 910x1024 crop ending at the panorama edge; SHA-256
    `0fa83e2c10c68d7c86e97b8d6a8ef19eebc7a01fa8f87a05aeb8a312037209b0`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r1_c0.png`
  - deterministic 910x1024 crop; SHA-256
    `d1e3eab5aa9ce34c9b136343c03709b707e775883177c51244fe1b1dc56d74ec`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r1_c1.png`
  - deterministic 910x1024 crop; SHA-256
    `e775495278b8fbcadca429dececa5445fe6dc5d8327f9758966ac4a5ae615129`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r1_c2.png`
  - deterministic 910x1024 crop; SHA-256
    `c2abbd83f3fce093addd9250c1930ee57d86f4c21e170b2d454121d12b723ea5`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r1_c3.png`
  - deterministic 910x1024 crop ending exactly at the Screen A boundary;
    SHA-256 `3b5ba5dd85ba1bf5969be08a191957e2eb476e741b717aa0e7fb843eb0aee40d`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r1_c4.png`
  - deterministic 910x1024 crop; SHA-256
    `9e180247910d843b535998ad1167371b1990834279a26119714743af59a11203`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r1_c5.png`
  - deterministic 910x1024 crop; SHA-256
    `31b6d8a5dfef47c575b63f953c98240c826f5007ef1fa406ef17a853630ff808`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r1_c6.png`
  - deterministic 910x1024 crop; SHA-256
    `0068537a79a205fa50f3747b37735c591f876ceac92d685abaa3d6f57605c92c`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/tiles/main_hall_room_led_r1_c7.png`
  - deterministic 910x1024 crop ending at the panorama edge; SHA-256
    `24a11eb0c82e09c3968f59c8f7418f9628e787ba0c0d1ab53b5ff4a282b98d41`.

The eight 256x256 sign cards below reuse only already licensed, approved
project art. Each source crop, source hash, alpha treatment, and whole-card
Lanczos resize is recorded in `sign_reuse_manifest.json`; the Dream House sign
uses a hand-traced semantic alpha to exclude its portal architecture, plus a
deterministic navy keyline and gold edge sampled from the approved Library
badge. No external or AI-generated RGB artwork was introduced.

- `assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_bubble_bath.png`
  - approved Main Hall Screen B badge reuse; SHA-256
    `3a43e1fc23f95f9f3a2ec256861d418017d783bbf0d30f7b85fee677838aa3c4`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_craft_room.png`
  - approved Main Hall Screen B badge reuse; SHA-256
    `17ccf96d936d557b28a88960d8793f58ceff73fa5328b42c7c41c4f65c138e2e`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_family_gallery.png`
  - approved Family Wing hall crest re-extracted from the full existing source
    so its formerly clipped right edge and adjacent portal scroll are absent;
    semantic alpha, visible-bounds centering, and a deterministic
    collection-sampled keyline only, with no repaint or new RGB artwork;
    SHA-256
    `222d5a5a4c590b6ae951ff5d7f4431bd35ed539e48cf0346a2e31fd83a09a0dd`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_kitchen.png`
  - approved Main Hall Screen A badge reuse; SHA-256
    `7f05f4b227ca10281af798f1ec632c7a662be15797abfc7c5cb15e2682b5d8dd`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_library.png`
  - approved Main Hall Screen A badge reuse; SHA-256
    `7aa633b17cd655f5bf340636555fab1406fc86030e9de38e667f9e701dd764b0`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_mermaid_pool.png`
  - approved Main Hall Screen B badge reuse; SHA-256
    `8ae6239cc8d01eecaa741842b591b2388659ff92929b9dec336e62ffa7ab4033`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_opera_hall.png`
  - approved Main Hall Screen A badge reuse; SHA-256
    `7378b84c037fc6c5fe21880577f6eba2214d3c5e990b726bfaf67d83e8c03fd1`.
- `assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_playroom.png`
  - approved Main Hall Screen B badge reuse, accepted and preserved
    byte-for-byte after review found that removing its minor source-arch cap
    would also cut valid teddy/rim pixels; SHA-256
    `22d9a3df8eda3b95ae93250165a64a947b4157a70b4405f90dc4d600edccd7df`.

The twelve 256x256 elevator crests below are project-authored deterministic
derivatives of the already licensed physical-door art above and the four
approved Dream House portal cards. `tools/build_castle_elevator_picture_icons.py`
alpha-crops the existing crest, applies one aspect-preserving Lanczos fit into
a shared 256x256 transparent canvas with audited optical-size normalization,
and centers it without repainting, stretching, AI generation, or alteration
of any source. Exact source/output
dimensions, crop rectangles, hashes, and transforms are recorded in
`assets/ui/castle_room_buttons_v2/elevator_picture_icon_manifest.json`.

- `assets/ui/castle_room_buttons_v2/room_main_hall.png`
- `assets/ui/castle_room_buttons_v2/room_opera_hall.png`
- `assets/ui/castle_room_buttons_v2/room_kitchen.png`
- `assets/ui/castle_room_buttons_v2/room_library.png`
- `assets/ui/castle_room_buttons_v2/room_playroom.png`
- `assets/ui/castle_room_buttons_v2/room_craft_room.png`
- `assets/ui/castle_room_buttons_v2/room_mermaid_pool.png`
- `assets/ui/castle_room_buttons_v2/room_bubble_bath.png`
- `assets/ui/castle_room_buttons_v2/room_dining_room.png`
- `assets/ui/castle_room_buttons_v2/room_royal_bedroom.png`
- `assets/ui/castle_room_buttons_v2/room_sleepover_bedroom.png`
- `assets/ui/castle_room_buttons_v2/room_movie_lounge.png`

The Royal Hall veil reuses
`assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png` under its existing
project-original license. Five narrow, low-alpha unshaded `Sprite3D` cards use
that exact byte-unchanged texture at separate real depths; this introduces no
new art and does not alter the accepted Main Hall background.

- `assets/flats/castle/main_hall_redraw_2026-08-03/props/main_hall_retained_shell_throne.png`
  - exact RGB crop of the approved Regen-01 pearl-shell throne's orthographic
    front view, with only border-connected studio-matte removal and exclusion
    of its source-sheet floor shadow; no upscale, external source, new RGB
    pixels, or redesign; SHA-256
    `91a8edcb91492d699e228cb4048fa346825f2a9e034ca3c9693f69a98933bcff`.

- `audit/castle_sprite3d/castle_main_hall_redraw_2026-08-04_2k_audit.json`
  and `castle_main_hall_redraw_2026-08-04_2k_{transform_overlay,grid_proof,seam_proof,reconstruction_proof}.png`
  - deterministic project-authored transform-invariance, strict-resolution,
  tile-grid, seam, and exact-reconstruction evidence derived solely from the
  licensed masters and runtime crops above; not additional runtime art. A
  rejected 1025px NPOT bleed experiment and its derivatives are intentionally
  excluded from delivery and do not feed Godot.
- `audit/castle_sprite3d/castle_main_hall_redraw_2026-08-03_node_inventory.json`,
  `castle_main_hall_redraw_2026-08-03_render_audit.json`, and
  `castle_main_hall_redraw_2026-08-03_render_proof.png` - deterministic
  project-authored structural and rendered-scene validation derived only from
  the licensed runtime cards above; these files record Sprite3D node types,
  lighting deltas, and seam measurements and are not runtime art.
- `audit/castle_sprite3d/main_hall.png`, `main_hall_screen_a.png`,
  `main_hall_screen_b.png`, `main_hall_seam_bridge.png`,
  `main_hall_lights_off.png`, and `elevator_menu.png` - project-authored
  Godot 4.7.1 runtime QA captures of the licensed scene, retained as visual
  evidence for door-sign placement, left-end access, two-screen continuity,
  lighting state, and the Storybook travel menu; not runtime art.

## Pearl Castle touch lighting and continuity cards (2026-07-29)

- `assets/flats/castle/main_hall_2screen/castle_shell_sconce_touchable.png`
  — project-original fixture generated with one OpenAI built-in ImageGen call
  using only the project's accepted Main Hall and Opera fixture art as style
  references; generated on a flat chroma background, converted locally to
  alpha with the installed imagegen helper, and downsampled once from
  1254x1254 to the 1024x1024 runtime limit. License: project original. Exact
  prompt, dimensions, hashes, and references are recorded in
  `audit/castle_sprite3d/CASTLE_LIGHTING_CONTINUITY_AUDIT_2026-07-29.md`.
- `assets/flats/castle/main_hall_2screen/castle_shell_sconce_assembly.png`
  — project-original deterministic derivative of the above sconce; a
  matching navy/plum, gold, and pearl architectural mount was added by
  `tools/build_castle_lighting_assets.py` so one identical Sprite3D assembly
  could cover the two baked fixture families without changing either accepted
  background master. Retained as a rejected/audit source after play review
  found that the mount read as a UI button; it is not loaded at runtime.
  License: project original.
- `assets/flats/castle/main_hall_2screen/castle_sconce_glow_reuse.png`
  — deterministic circular crop of the accepted sconce's pearl core by
  `tools/build_castle_lighting_assets.py`. Used as the discreet unshaded
  Sprite3D glint over each existing wall fixture; no new painted pixels,
  external source, or ImageGen call. License remains project original.
- `assets/flats/castle/main_hall_2screen/castle_royal_tapestry_reuse.png`
  — exact-alpha extraction of the already licensed royal shell tapestry from
  the accepted Main Hall 2x4 runtime tiles by
  `tools/build_castle_lighting_assets.py`; no generated pixels or external
  source art. License remains project original.
- `assets/flats/castle/main_hall_2screen/castle_playroom_portal_reuse.png`
  — exact-pixel, alpha-masked extraction of an approved open Main Hall
  corridor from the accepted 2x4 runtime tiles by
  `tools/build_castle_lighting_assets.py`. Reused as a real-depth architectural
  bridge at the Screen A/B material junction and as the missing physical
  Playroom entrance; no scaling of source pixels, new painting, external art,
  or ImageGen call. License remains project original.

## assets/characters/roshan_25d/*.png
- Source: project-authored runtime sprite atlases generated with OpenAI
  built-in image generation on 2026-07-26 from five user-provided Mermaid
  Roshan multi-view reference PNGs; prompt specifications and generation
  identifiers are recorded in `assets/characters/roshan_25d/PROMPTS.md` and
  `assets/characters/roshan_25d/PROMPTS_4X.md`
- License: project original; reference images supplied by the project owner
- URL: none (project-local user references and project generation)
- Modifications: flat green chroma background removed with the Codex
  image-generation helper using soft matte and despill; accepted atlases
  resampled with Lanczos to power-of-two 1024x512 or 1024x1024; the
  256x256 base portrait is a lossless crop of directional frame 0

## assets/props/story/play_swing_{frame,seat}.png
- Source: project-authored runtime sprite layers generated with OpenAI
  built-in image generation on 2026-07-28; the owner-provided Mermaid Roshan
  front-view PNG informed style only. Exact prompts and generation identifiers
  are recorded in `assets/props/story/play_swing_PROMPT.md`
- License: project original; style reference supplied by the project owner
- URL: none (project-local user reference and project generation)
- Modifications: flat magenta chroma background removed with the Codex
  image-generation helper using a soft matte and one-pixel edge contraction;
  cutouts tightly cropped and Lanczos-resampled to 1024x719 (frame) and
  554x1024 (seat/ropes)
## Pearl Castle 2K room cards and final junction derivatives (2026-07-29)

- `assets_src/castle/room_backgrounds_2k/room_*_background_2k.png` —
  six project-original 3640 x 2048 preservation masters plus the Kitchen's
  4096 x 2304 master, derived from the already licensed 1024 x 576 clean room
  plates with whole-canvas Pillow Lanczos under the owner's explicit
  authorization to upscale for this pass. Originals and aspect ratios are
  preserved; no external source or new object design.
- `assets/flats/castle/rooms/background_tiles/room_*_background_r*_c*.png`
  — 48 non-overlapping 910 x 1024 runtime crops of the six native masters plus
  twelve non-overlapping 1024 x 768 Kitchen crops, produced by
  `tools/build_castle_room_2k_tiles.py`. Each tile group reconstructs its
  master pixel-exactly; no scaling occurs during slicing.
- `assets_src/castle/room_backgrounds_2k/castle_live_alpha_baseline_repair.json`
  — project-authored 2026-08-04 provenance and hash ledger for the
  non-destructive seven-room baseline repair. The approved whole-room image is
  restored outside the exact union of active V2/V4 animation-frame alpha and
  static depth-card alpha at the runtime scissor threshold of 128; prior hidden
  fill is retained only beneath that live union. The logical binary union is
  scaled to the native canvas with nearest-neighbor while the approved image
  uses the existing whole-canvas Lanczos transform. All seven repaired masters
  report zero changed native pixels outside the live union; protected originals
  are unchanged; no new art or external source is introduced.
- `assets_src/castle/main_hall_alignment/generated_cleanup_candidate_{a,b}.png`
  — project-original OpenAI built-in ImageGen precision-removal candidates
  made from the two already licensed Main Hall masters. The request removed
  only the three baked fixtures on each screen and restored the same wall;
  no replacement object was generated. Generator paths, final prompts,
  dimensions, hashes, and mask evidence are recorded in
  `audit/castle_sprite3d/castle_hall_alignment_manifest.json`.
- `assets_src/castle/main_hall_alignment/main_hall_screen_{a,b}_fixture_aligned_master.png`
  — deterministic same-size composites made by
  `tools/build_castle_hall_alignment.py`. Candidate pixels are accepted only
  inside six compact fixture masks; pixels outside are exact to the immutable
  licensed masters. Screen B also receives a documented global tone correction
  and a four-pixel exact-edge ramp. License remains project original.
- `assets/flats/castle/main_hall_2screen/castle_shell_sconce_integrated_reuse.png`
  — tight-alpha 96 x 128 extraction of the accepted Screen B shell fixture.
  No generated, external, or newly painted pixels; reused unchanged for all
  six unshaded Sprite3D lights.
- `assets/flats/castle/main_hall_2screen/castle_playroom_portal_cutout_reuse.png`
  — tight-alpha derivative of the already licensed
  `castle_playroom_portal_reuse.png`; the rectangular wall/floor plate is
  removed while the accepted arch, corridor, and badge pixels remain.
- `assets/flats/castle/main_hall_2screen/castle_join_column_cutout_reuse.png`
  — tight-alpha 190 x 941 extraction of an accepted Screen A shell pilaster;
  retained as a provenance derivative but not used by the repaired runtime
  join.
- `assets/flats/castle/main_hall_2screen/castle_join_floor_inlay_reuse.png`
  — 48 x 321 tapered inlay assembled deterministically by rotating and tiling
  the accepted Screen A carpet trim; no new painting or external source. It is
  retained for provenance but retired from runtime because it read as a crack.
- `assets/flats/castle/main_hall_2screen/tiles/main_hall_room_led_*.png`
  — updated lossless runtime crops of the documented derived Main Hall
  masters. Source rectangles and hashes are in
  `audit/castle_sprite3d/castle_main_hall_2x4_runtime_manifest.json`.
- `assets/flats/castle/main_hall_2screen/tiles/runtime_bleed/main_hall_room_led_r{0,1}_c*_bleed.png`
  — deterministic render-only derivatives of all eight accepted source tiles,
  made by `tools/build_castle_hall_runtime_bleed.py`. Each file preserves its
  836 x 470/471 source body pixel-exactly and, where an interior neighbor
  exists, appends that approved neighbor's first column and/or row. Derived
  textures are at most 837 x 471. This creates a one-pixel two-axis
  Mobile-raster safety overlap without scaling, interpolation, content loss,
  generated art, or modification to the accepted source tiles. Exact
  source/derived hashes and edge-equality proofs are recorded in
  `audit/castle_sprite3d/castle_main_hall_runtime_seam_bleed.json`. License
  remains project original.
## Sky Lagoon ambient animals - 2026-07-29

- `assets/sprites/sky_lagoon/animals/*_atlas.png` and
  `assets_src/sky_lagoon/ambient_animals_2026-07-29/**` - five project-original
  ambient-animal sprite families (summer-coat snowshoe hare, Douglas squirrel,
  Pacific Northwest raccoon, North American river otter, and Pacific tree frog),
  generated with OpenAI built-in image generation on 2026-07-29. Source license:
  project original. The generated 2x2 chroma sheets were converted locally to
  alpha and downsampled once, whole-canvas, to 512x512 POT runtime atlases. The
  exact prompts, source/runtime hashes, processing notes, and review contact sheet
  are preserved in the adjacent source ledger. No external or protected project
  art was used as delivery pixels; the ranked black-tailed deer fawn option was
  deliberately excluded from this batch.

## Pearl Castle registered Sprite3D bloom correction (2026-07-29)

- `assets/flats/castle/main_hall_2screen/tiles/main_hall_room_led_r{0,1}_c{2,3}.png`
  and `tiles/runtime_bleed/main_hall_room_led_r{0,1}_c{2,3}_bleed.png` —
  lossless recrops of the already licensed
  `assets_src/castle/main_hall_alignment/main_hall_screen_b_fixture_aligned_master.png`.
  Screen B now uses source rectangle `(376, 147, 1672, 941)` so its fixture
  sockets and walkway align with Screen A at runtime Y=215 and Y=634.
  `tools/build_castle_hall_runtime_registration.py` records dimensions,
  hashes, master rectangles, exact reconstruction, and the one-pixel
  source-exact render bleed. No scaling, interpolation, padding, external art,
  or generated pixels.
- `shaders/castle_fixture_bloom.gdshader` ? project-authored Godot spatial
  shader for the existing licensed 1024 x 1024 shell-sconce cutout. It keeps
  the Sprite3D unshaded, emits HDR light from the pearl/highlights, and derives
  a restrained aura only from the existing alpha margin. No new texture or
  external source. License: project code.
- `shaders/castle_portal_cutout.gdshader` ? project-authored Godot spatial
  shader for the existing licensed Playroom portal card. It discards the
  reused source's rectangular wall/floor area geometrically while retaining
  the same arch and corridor pixels on one unshaded Sprite3D. No new raster,
  external source, model, or generated art. License: project code.
- `assets/flats/castle/main_hall_2screen/castle_shell_sconce_touchable.png` ?
  reused unchanged for all six interactive fixtures in this correction; SHA-256
  remains `dd202d48ca3a9d142fbc7f1f0cc738e6ff7c0610f1018982e5223e7d002b761e`.

<!-- OPERA_REGEN_2026_08_01_START -->
## Opera regeneration — 2026-08-01

- `assets_src/concepts/opera_regeneration_2026-08-01/cards/astronaut_engineer_performance_boss_finale_2026-07-24.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-7ec20da7-2d87-498b-8ff8-1ce09aac83e9.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/boss_midnight_maestro_friendly.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-be832013-604d-4e17-9931-de89bd13a616.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/boss_shadow_phantom_friendly.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-14223439-45d9-4392-a07f-6757b96f2e34.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/boxer_performance_boss_finale_2026-07-24.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-ee9975b1-59e7-4a47-8f29-4f7a8a1d20cb.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/doctor_performance_boss_finale_2026-07-24.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-06322a9d-e58b-4f97-9364-5c56235bf118.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/farmer_gameplay_sheet.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-ba2b918e-93ed-4009-a25f-0ad6f7ccde69.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/farmer_performance_boss_finale_2026-07-24.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-98b68765-4d64-4120-9273-012ff7b01532.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/imp_captain.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-7965759e-156f-4315-bb01-87a9820939b1.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/imp_captain_bopped.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-b8efc220-fe27-450e-b323-b69efa66a4d8.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/imp_captain_bow.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-4cac2c7f-a077-4fc9-859b-91c3c385649e.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/imp_mischief.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-9e92b9fa-b7b5-4a9c-9f2a-e20018bfd8ff.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/imp_mischief_bopped.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-80d9d6fd-c1c6-4340-8578-85784779d49d.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/imp_mischief_bow.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-c06ee44d-9e98-4954-b24b-ae2af4edcf4c.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/magician_performance_boss_finale_2026-07-24.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-d81a17c2-6eed-4acc-9b7f-7786dd135470.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_house_audience_kit.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-f1433e5a-7690-494d-b036-0b3171de0300.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_astronaut_engineer_gameplay_rocket_front.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-7ec64f23-f8db-443f-9825-698cbc2c007e.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_ballerina_gameplay_music_box.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-4236332a-1094-4976-bba1-4a6d554bd166.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_ballerina_outfit_tertiary_tool_or_accessory.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-73ff7986-680c-44ef-b766-e42629c2c2cf.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_boxer_gameplay_championship_belt.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-a984de05-6eec-4cee-b096-5deffa914881.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_boxer_gameplay_imp_bow_group.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-810207d9-2b60-44b3-b2d8-ef52c21ce90f.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_boxer_stage_states_bop_state.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-cffd5543-9456-4160-a8e1-c0cabdc624f7.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_boxer_stage_states_gentle_retry.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-d9a22fa6-1c1e-49c2-b548-d36989317590.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_boxer_stage_states_imp_peek_state.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-f6367beb-4ec3-45df-9511-1604815f64f4.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_candy_maker_gameplay_wrapped_candy_reward.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-3b5632b2-462f-4234-a380-a5f9656848b2.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_candy_maker_stage_states_seven_slot_shelf.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-90f0543a-7011-460d-bef6-646590ded0db.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_candy_maker_stage_states_shelf_complete.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-357d4deb-7e33-414b-a8d8-b8a45fec0700.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_candy_maker_stage_states_timing_pointer.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-f3073d5a-e2d8-4209-9c85-feea39fa9ab0.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_detective_gameplay_magnifier.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-c79a4fbc-83b2-4b03-831f-88a8fb46ba89.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_detective_gameplay_pearl_tiara.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-16885f1a-8e92-49f6-b796-b29ee46925b5.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_detective_stage_states_case_complete_tableau.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-0504f6d2-ad42-4afa-916b-97ff4a110d9b.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_detective_stage_states_chest_pedestal.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-4e244964-dea4-4298-a42e-5c1add1dcdec.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_detective_stage_states_magnifier_pointer.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-f5faed60-669d-406f-b003-f8eabdfe5af7.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_doctor_gameplay_recovered_starfish.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-be9f8a34-354c-41fd-9bc0-4c328e3376ff.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_doctor_outfit_primary_tool_or_accessory.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-6217a596-9d59-44ae-a6f2-d06748b26144.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_doctor_stage_states_four_step_board.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-1ef8b71a-321a-41ff-ace5-861a04032501.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_farmer_gameplay_piggy_fed.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-2518f2b7-e50b-4cc0-b335-b43daea2b38c.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_farmer_stage_states_piggy_finale.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-c4018336-a9dd-406c-b5b1-289671a8d08a.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_magician_gameplay_bunny_fish_peek.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-a053e1f9-2f00-4c44-b237-7b6c40f27a23.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_magician_gameplay_bunny_fish_reveal.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-a03e92fe-c5e6-4414-a6ca-4658311d242a.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_magician_gameplay_bunny_fish_swim.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-d52078dd-65fa-4e9b-b64a-e5f5501a34d0.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_magician_gameplay_pearl_wand.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-ff8c9539-b1b8-48d9-8413-d3586e29eeb5.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_magician_stage_states_bunny_fish_reveal.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-24f3d0a8-7e09-4837-809a-6f8e43de0100.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_magician_stage_states_decoy_state.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-7ef67f19-1835-4a86-98e8-caa106211263.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_magician_stage_states_final_reveal.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-b59b4b99-c335-4bea-a222-c8c1bc8e1f3a.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_magician_stage_states_selector_state.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-2fec0f0e-d44f-46a9-9369-52884aa71c4f.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_magician_stage_states_swap_state.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-18168f63-7820-4d0e-9a92-5083ba382629.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_magician_stage_states_watch_state.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-51224c38-df5a-48dd-a3ee-ab4eb17ef207.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_painter_gameplay_coral_loaded_brush.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-feb2da7c-514b-447b-b7b5-998345a59f45.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_painter_gameplay_cream_loaded_brush.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-9c822771-b48b-41ae-bd46-deef139a1522.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_painter_gameplay_framed_sunrise.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-77a0271f-082d-46a5-a113-d2abaad695bd.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_painter_gameplay_plum_loaded_brush.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-68c1a323-04e6-48b3-a8c3-ff5773b01b18.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pastry_chef_gameplay_finished_cake.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-1a4bec08-a51f-435a-aacb-b84c1d1fa754.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pastry_chef_stage_states_cake_reveal.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-cbd22830-8f7d-4056-8584-d9cd6face619.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pastry_chef_stage_states_oven_alcove.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-fb5f0099-e706-48a9-8f93-78155de39416.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pastry_chef_stage_states_placement_glows.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-2d3dbef1-12ca-4099-aa26-47fa595350a8.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pastry_chef_stage_states_presentation_cart.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-adcc9dcf-7ea7-474a-a663-ea5e1b00bf49.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pastry_chef_stage_states_topping_pedestals.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-9214e5fa-13c7-4c8e-ab6c-f34c2d17ba22.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pop_star_gameplay_microphone_finale.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-38eee3e2-1d54-4301-96bf-3915be39c51d.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pop_star_gameplay_speaker.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-d8b96a02-1d0a-4689-86cb-e26d653dde18.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pop_star_stage_states_arrow_lane.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-38ef1ad2-1d6e-46c0-a854-300e8babf0d2.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pop_star_stage_states_arrows_complete.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-dc442127-5ada-4f5f-b065-c7bd2c26f914.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_pop_star_stage_states_dance_floor.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-e38212da-b14e-451c-a475-d2cebdb8d7f7.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_racecar_driver_gameplay_shell_trophy.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-ce69b6ab-71f9-4954-842d-5cf340c6b39e.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_racecar_driver_gameplay_zoom_strip_active.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-4728d13d-c787-4302-add5-443eac671728.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_job_racecar_driver_outfit_secondary_tool_or_accessory.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-7f5be543-850b-4780-a3dc-5edf0697f063.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_rival_costume_sheet_master.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-7f0a92a5-29f6-41b6-9bfa-8c3069e84dd1.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_upper_access_floor_selector_full.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-bfa93fef-acd4-4a26-bf38-ad973d00c4a1.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_upper_access_floor_selector_ground.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-1375db52-cfcb-4d59-8353-b5a06a33e3ee.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_upper_access_floor_selector_middle.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-b4d908b7-f05d-4ae5-93b0-7f93007838d5.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/painter_performance_boss_finale_2026-07-24.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-15f1f596-8327-4513-8c67-f8c53d9338f3.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/pop_star_performance_boss_finale_2026-07-24.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-42d31345-2667-48bc-9852-601c0b9c7a7b.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/racecar_driver_performance_boss_finale_2026-07-24.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-6b2640d6-be6f-4e3c-a43a-4af8446d71dc.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/roshan_doctor_stethoscope.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-af9814f2-16cc-4e7b-96cc-f3e83bff4d67.png`.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/roshan_racer_steering_wheel.png` — OpenAI-generated project concept art; 2026-08-01; native generated master retained, delivery copies may be whole-canvas normalized, matted, or sliced; project-owned; generation `exec-0ce28eb1-87eb-4090-9533-7016cc47cd16.png`.
<!-- OPERA_REGEN_2026_08_01_END -->

## Pearl Castle semantic interaction atlases and sounds (2026-08-01)

All entries below are project original, have no external URL, and remain under
the project's existing license. Runtime atlases are deterministic derivatives
of already licensed Pearl Castle room art except where the named preservation
master is recorded below. Atlas construction, exact source/runtime hashes,
frame grids, action names, and review state are recorded in
`assets/flats/castle/interactions/castle_interactions.json`.

- `assets/flats/castle/rooms/room_opera_hall_item_footlights.png` - exact-pixel alpha derivative of the licensed Opera Hall room art by `tools/build_castle_room_layers.py`.
- `assets/flats/castle/rooms/room_library_item_book_stack.png` - exact-pixel alpha derivative of the licensed Library room art by `tools/build_castle_room_layers.py`.
- `assets/flats/castle/rooms/room_playroom_item_play_tent.png` - exact-pixel alpha derivative of the licensed Playroom room art by `tools/build_castle_room_layers.py`.
- `assets/flats/castle/rooms/room_craft_room_item_ribbon_rack.png` - exact-pixel alpha derivative of the licensed Craft Room art by `tools/build_castle_room_layers.py`.
- `assets/flats/castle/rooms/room_mermaid_pool_item_star_float.png` - exact-pixel alpha derivative of the licensed Mermaid Pool art by `tools/build_castle_room_layers.py`.
- `assets/flats/castle/rooms/room_bubble_bath_item_rubber_duck.png` - exact-pixel alpha derivative of the licensed Bubble Bath art by `tools/build_castle_room_layers.py`.

- `assets/flats/castle/interactions/main_hall_tapestry_atlas.png` - eight-frame fixed-pivot deterministic atlas derived from the licensed reusable tapestry.
- `assets/flats/castle/interactions/main_hall_sconce_atlas.png` - eight-frame fixed-pivot deterministic atlas derived from the licensed reusable shell sconce.
- `assets/flats/castle/interactions/opera_hall_curtains_atlas.png` - eight-frame fixed-pivot deterministic stage-curtain atlas.
- `assets/flats/castle/interactions/opera_hall_chandelier_atlas.png` - eight-frame fixed-pivot deterministic chandelier light-chase atlas.
- `assets/flats/castle/interactions/opera_hall_footlights_atlas.png` - eight-frame fixed-pivot deterministic footlight-chase atlas.
- `assets/flats/castle/interactions/opera_hall_stage_star_atlas.png` - eight-frame fixed-pivot deterministic marquee-star atlas.
- `assets/flats/castle/interactions/kitchen_sink_atlas.png` - eight-frame fixed-pivot deterministic faucet-and-water atlas.
- `assets/flats/castle/interactions/kitchen_pan_1_atlas.png` - eight-frame fixed-hook deterministic copper-pan atlas.
- `assets/flats/castle/interactions/kitchen_pan_2_atlas.png` - eight-frame fixed-hook deterministic copper-pan atlas.
- `assets/flats/castle/interactions/kitchen_pan_3_atlas.png` - eight-frame fixed-hook deterministic copper-pan atlas.
- `assets/flats/castle/interactions/kitchen_pan_4_atlas.png` - eight-frame fixed-hook deterministic copper-pan atlas.
- `assets/flats/castle/interactions/kitchen_oven_atlas.png` - eight-frame fixed-pivot deterministic oven-door/fire atlas.
- `assets/flats/castle/interactions/kitchen_fridge_atlas.png` - eight-frame fixed-pivot deterministic refrigerator-door/interior atlas.
- `assets/flats/castle/interactions/library_book_stack_atlas.png` - eight-frame fixed-pivot deterministic top-book/page atlas.
- `assets/flats/castle/interactions/library_magic_book_atlas.png` - eight-frame fixed-pivot deterministic book-opening/page atlas.
- `assets/flats/castle/interactions/library_pearl_table_atlas.png` - eight-frame fixed-pivot deterministic reading-pearl atlas.
- `assets/flats/castle/interactions/library_pearl_lamp_atlas.png` - eight-frame fixed-pivot deterministic pearl-lamp atlas.
- `assets/flats/castle/interactions/playroom_play_tent_atlas.png` - eight-frame fixed-pivot deterministic tent-flap atlas.
- `assets/flats/castle/interactions/playroom_stuffie_nook_atlas.png` - eight-frame fixed-pivot deterministic friend-wave atlas.
- `assets/flats/castle/interactions/playroom_stacking_toy_atlas.png` - eight-frame fixed-pivot deterministic ring-restacking atlas.
- `assets/flats/castle/interactions/playroom_blocks_atlas.png` - eight-frame fixed-pivot deterministic block-topple/restack atlas.
- `assets/flats/castle/interactions/craft_room_ribbon_rack_atlas.png` - eight-frame fixed-pivot deterministic ribbon-unroll atlas.
- `assets/flats/castle/interactions/craft_room_idea_board_atlas.png` - eight-frame fixed-pivot deterministic note-flip atlas.
- `assets/flats/castle/interactions/craft_room_paint_table_atlas.png` - eight-frame fixed-pivot deterministic brush-stir atlas.
- `assets/flats/castle/interactions/craft_room_palette_atlas.png` - eight-frame fixed-pivot deterministic paint-mixing atlas.
- `assets/flats/castle/interactions/mermaid_pool_star_float_atlas.png` - eight-frame fixed-pivot deterministic star/ripple atlas.
- `assets/flats/castle/interactions/mermaid_pool_waterfall_atlas.png` - eight-frame fixed-pivot deterministic waterfall-flow atlas.
- `assets/flats/castle/interactions/mermaid_pool_flower_float_atlas.png` - eight-frame fixed-pivot deterministic petal/ripple atlas using the preservation master below.
- `assets/flats/castle/interactions/mermaid_pool_bubble_fountain_atlas.png` - eight-frame fixed-pivot deterministic jet/bubble atlas using the preservation master below.
- `assets/flats/castle/interactions/mermaid_pool_seahorse_fountain_atlas.png` - eight-frame fixed-pivot deterministic water-spray atlas derived from the accepted 2026-08-02 room card; project-original, no external URL.
- `assets/flats/castle/interactions/bubble_bath_rubber_duck_atlas.png` - eight-frame fixed-pivot deterministic squeak/dive atlas color-isolated from the accepted tub preservation master.
- `assets/flats/castle/interactions/bubble_bath_bathtub_atlas.png` - eight-frame fixed-pivot deterministic tap/water/bubble atlas using the preservation master below.
- `assets/flats/castle/interactions/bubble_bath_sink_atlas.png` - eight-frame fixed-pivot deterministic faucet/water atlas using the preservation master below.
- `assets/flats/castle/interactions/bubble_bath_toilet_atlas.png` - eight-frame fixed-pivot deterministic seat/flush atlas using the preservation master below.
- `assets/flats/castle/interactions/castle_interactions.json` - project-authored machine-readable atlas, provenance, semantic-action, audio, frame, hash, and review manifest.

The following native preservation masters were made with OpenAI built-in
ImageGen from only the named approved project-local item crops, on flat chroma,
then keyed with the installed local helper. Exact prompts, helper settings,
hashes, dimensions, rejection notes, and human drift reviews are in
`assets_src/imagegen/castle_interactions_2026-08-01/PROMPTS.md`.

- `assets_src/imagegen/castle_interactions_2026-08-01/bathroom_sink_chroma.png` - native project-original sink extraction generation.
- `assets_src/imagegen/castle_interactions_2026-08-01/bathroom_sink_alpha_hard.png` - accepted hard-alpha sink preservation master.
- `assets_src/imagegen/castle_interactions_2026-08-01/bathroom_sink_alpha.png` - rejected soft-matte sink extraction retained only as audit evidence; never loaded or used to build runtime art.
- `assets_src/imagegen/castle_interactions_2026-08-01/bathtub_chroma.png` - native project-original bathtub extraction generation.
- `assets_src/imagegen/castle_interactions_2026-08-01/bathtub_alpha.png` - accepted hard-alpha bathtub preservation master.
- `assets_src/imagegen/castle_interactions_2026-08-01/toilet_chroma.png` - native project-original toilet extraction generation.
- `assets_src/imagegen/castle_interactions_2026-08-01/toilet_alpha.png` - accepted hard-alpha toilet preservation master.
- `assets_src/imagegen/castle_interactions_2026-08-01/flower_float_chroma.png` - native project-original flower-float extraction generation.
- `assets_src/imagegen/castle_interactions_2026-08-01/flower_float_alpha.png` - accepted hard-alpha flower-float preservation master.
- `assets_src/imagegen/castle_interactions_2026-08-01/bubble_fountain_chroma.png` - native project-original bubble-fountain extraction generation.
- `assets_src/imagegen/castle_interactions_2026-08-01/bubble_fountain_alpha.png` - accepted hard-alpha bubble-fountain preservation master.

All new audio is project-original deterministic offline synthesis by
`tools/build_castle_interaction_audio.py`: fixed-seed NumPy/SciPy PCM, mono
24 kHz, normalized to -3 dBFS, encoded as Ogg Vorbis q4 with the repository's
pinned FFmpeg. No samples, voices, downloaded media, or external sources were
used. Exact PCM/file hashes and cue timing are in the audio manifest.

- `assets/audio/castle/faucet_water.ogg` - synthesized faucet-on/water-flow cue.
- `assets/audio/castle/toilet_flush.ogg` - synthesized seat-tap/flush/water-settle cue.
- `assets/audio/castle/fridge_door.ogg` - synthesized latch/refrigerator-door cue.
- `assets/audio/castle/oven_door.ogg` - synthesized oven-door/warm-fire cue.
- `assets/audio/castle/pan_clang.ogg` - synthesized hanging copper-pan clang cue.
- `assets/audio/castle/curtain_swish.ogg` - synthesized fabric/curtain cue.
- `assets/audio/castle/page_flip.ogg` - synthesized book/page cue.
- `assets/audio/castle/toy_blocks.ogg` - synthesized wooden toy/ring/block cue.
- `assets/audio/castle/craft_brush.ogg` - synthesized brush/paint cue.
- `assets/audio/castle/ribbon_roll.ogg` - synthesized ribbon-spool cue.
- `assets/audio/castle/bubble_water.ogg` - synthesized bubble/pool/water cue.
- `assets/audio/castle/light_switch.ogg` - synthesized switch/pearl-light cue.
- `assets/audio/castle/duck_squeak.ogg` - synthesized rubber-duck squeak cue.
- `assets/audio/castle/castle_interaction_sfx_manifest.json` - deterministic audio provenance, timing, encoding, and hash manifest.
- `audit/castle_interactions/castle_interaction_frames.png` - deterministic all-eight-frame-per-item review contact sheet produced by the atlas builder; project audit evidence, not runtime art.

## Pearl Castle room-selector illustrations (2026-08-01)

- `assets_src/imagegen/castle_room_buttons_2026-08-01/castle_button_*_master.png`
  - project-generated storybook derivatives based on the project's authored
  Pearl Castle rooms and approved replacement Opera House concept. Generated
  with the built-in Codex ImageGen tool; project original, all rights reserved.
  Exact prompts, references, and SHA-256 hashes are recorded in the adjacent
  `PROMPTS.md`.
- `assets_src/imagegen/castle_room_buttons_2026-08-01/references/mermaid_roshan_wisconsonia_cover_reference.jpg`
  - project-owner-supplied authoritative book cover, copied byte-for-byte and
  preserved unchanged (SHA-256
  `3ABEDC5EC0D878CFD7A0E1ABAB18B5C8D61E06275D87ABD29252FEF25CE24CD6`).
  Used only as a visual reference for the simplified Library button; it was not
  destructively edited or recompressed.
- `assets/ui/castle_room_buttons/room_*.png` - project-authored runtime
  derivatives built by `tools/build_castle_room_button_thumbnails.py` as
  400 x 224 center-crop/resamples of the registered masters. No external art
  or additional generated pixels. License remains project original.

## Imp combat animation art (2026-08-02)

One row per accepted runtime file; all native generations, prompt bindings, hashes, rejection notes, per-file acceptance reports, QA renders, and Mobile-renderer captures are retained in the linked source packet.

| Path | Source | License | URL | Modifications |
|---|---|---|---|---|
| assets/opera/worlds/actors/imp_mischief_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_mischief_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_mischief_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_mischief_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_mischief_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_mischief_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_mischief_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_mischief_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_captain_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_captain_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_captain_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_captain_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_captain_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_captain_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_captain_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_captain_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/imp_captain_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_chef_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_detective_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_ballerina_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_candymaker_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_doctor_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_farmer_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_boxer_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_magician_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_painter_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_astronaut_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_racer_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_windup.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_charge.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_slash.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_recover.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_guard.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_stagger.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_flee.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_taunt.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_hop_a.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_hop_b.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_bopped.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/actors/rival_popstar_bow.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/props/fx_telegraph_ring.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x512; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/props/fx_telegraph_bang.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 128x256; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/props/fx_slash_arc.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 512x256; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/props/fx_dust_puff.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 256x256; prompt, hashes and QA in the linked packet |
| assets/opera/worlds/props/fx_stolen_sparkle.png | Non-destructive derivative of approved project art `assets/mg/star.png` | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Uniform whole-star resize and transparent-canvas padding to 128x128; no generated pixels |
| assets/opera/worlds/props/fx_dizzy_stars.png | OpenAI built-in ImageGen using approved project imp/rival or FX style references | **Project-generated © Mermaid Roshan LLC, all rights reserved** | assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md | Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to 256x256; prompt, hashes and QA in the linked packet |
## Pearl Castle dream-house rooms — 2D repair (2026-08-02)

- `assets_src/imagegen/castle_dream_house_2026-08-01/dining_room_reference_1254.png` — OpenAI built-in ImageGen from approved project-local Castle references; project-original composition reference, all rights reserved; below native background requirements and contributes no runtime pixels; prompt in the adjacent `PROMPTS.md`.
- `assets_src/imagegen/castle_dream_house_2d_repair_2026-08-02/door_family_sheet_chroma.png` — OpenAI built-in ImageGen using approved project-local Castle doorway/room references; project-original production sheet, all rights reserved; native accepted chroma master, no post-generation resize.
- `assets_src/imagegen/castle_dream_house_2d_repair_2026-08-02/door_family_sheet_alpha.png` — derivative of the adjacent project-original door chroma master; flat chroma removed with the installed ImageGen helper using border auto-key, soft matte, thresholds 12/220, and despill; no resize or redraw.
- `assets_src/imagegen/castle_dream_house_2d_repair_2026-08-02/furnishing_family_sheet_chroma.png` — OpenAI built-in ImageGen using approved project-local Castle art plus rejected Blender renders only as identity/gameplay-purpose references; project-original production sheet, all rights reserved; native accepted chroma master, no post-generation resize.
- `assets_src/imagegen/castle_dream_house_2d_repair_2026-08-02/furnishing_family_sheet_alpha.png` — derivative of the adjacent project-original furnishing chroma master; flat chroma removed with the installed ImageGen helper using border auto-key, soft matte, thresholds 12/220, and despill; no resize or redraw.
- `assets_src/imagegen/castle_dream_house_2d_repair_2026-08-02/PROMPTS.md` — project provenance ledger containing exact accepted prompts, reference roles, methods, dimensions, and hashes.

The following runtime cards are project-original deterministic crops of the accepted alpha sheets above. Modifications are transparent-bound cropping only (largest connected component for furnishings except the deliberately disconnected place setting); no generated card is enlarged, warped, repainted, or sourced from Blender:

- `assets/flats/castle/dream_house/family_wing_portal.png`
- `assets/flats/castle/dream_house/family_wing_hall_insert.png`
- `assets/flats/castle/dream_house/family_portal_dining.png`
- `assets/flats/castle/dream_house/family_portal_royal_bedroom.png`
- `assets/flats/castle/dream_house/family_portal_sleepover_bedroom.png`
- `assets/flats/castle/dream_house/family_portal_movie_lounge.png`
- `assets/flats/castle/dream_house/dining_table.png`
- `assets/flats/castle/dream_house/dining_seat.png`
- `assets/flats/castle/dream_house/provisions_hutch.png`
- `assets/flats/castle/dream_house/meal_plate.png`
- `assets/flats/castle/dream_house/canopy_bed.png`
- `assets/flats/castle/dream_house/shell_wardrobe.png`
- `assets/flats/castle/dream_house/bedside_table.png`
- `assets/flats/castle/dream_house/story_cushion.png`
- `assets/flats/castle/dream_house/dream_bed_0.png`
- `assets/flats/castle/dream_house/dream_bed_1.png`
- `assets/flats/castle/dream_house/dream_bed_2.png`
- `assets/flats/castle/dream_house/shell_chandelier.png`
- `assets/flats/castle/dream_house/cloud_settee.png`
- `assets/flats/castle/dream_house/cloud_pouf.png`
- `assets/flats/castle/dream_house/movie_screen_frame.png`
- `assets/flats/castle/dream_house/shell_popcorn_bowl.png`

The following retained project-authored background assets are deterministic compositions by `tools/build_castle_dream_house_rooms.py` from already-licensed Castle wall/floor textures. The Movie Lounge master removes its obsolete second screen frame; no protected original is modified:

- `assets_src/castle/dream_house_rooms_2k/room_family_gallery_background_master.png`
- `assets_src/castle/dream_house_rooms_2k/room_dining_room_background_master.png`
- `assets_src/castle/dream_house_rooms_2k/room_royal_bedroom_background_master.png`
- `assets_src/castle/dream_house_rooms_2k/room_sleepover_bedroom_background_master.png`
- `assets_src/castle/dream_house_rooms_2k/room_movie_lounge_background_master.png`
- `assets/flats/castle/rooms/room_{family_gallery,dining_room,royal_bedroom,sleepover_bedroom,movie_lounge}_background.png` — 1024×576 review previews only.
- `assets/flats/castle/rooms/background_tiles/room_{family_gallery,dining_room,royal_bedroom,sleepover_bedroom,movie_lounge}_background_r{0,1}_c{0,1}.png` — exact non-overlapping runtime crops; 1024×576 each.

- `audit/castle_dream_house/dream_house_room_art_manifest.json` — deterministic source, hash, crop, node-type, placement, and tile-reconstruction evidence.
- `audit/castle_dream_house/dream_house_room_shells_contact.png` — five-room native-shell review contact; project audit evidence.
- `audit/castle_dream_house/dream_house_layout_contact.png` — physical four-door gallery and Main Hall entry contact; project audit evidence.
- `audit/castle_dream_house/dream_house_hall_entry_contact.png` — Main Hall integration contact; project audit evidence.
- `audit/castle_dream_house/dream_house_furnished_rooms_contact.png` — four-room furnished placement contact; project audit evidence; protected family movie pixels deliberately omitted.
- `CASTLE_DREAM_HOUSE_2D_REPAIR_AUDIT_2026-08-02.md` — project audit documentation.

`assets/book/hall/p_slide.jpg`, `p_trampoline.jpg`, `p_garden.jpg`, `p_snowman.jpg`, and `p_xmas.jpg` remain protected originals displayed directly and unchanged on the movie Sprite3D card. They are not copied into a derivative runtime or audit image.

## Shared water-FX atlas vocabulary (2026-08-02)

- `assets_src/imagegen/water_fx_2026-08-02/fx_water_splash_small_chroma_native.png` ? Source: OpenAI built-in ImageGen using only approved project-local castle water atlas references; License: project original, all rights reserved; URL: N/A (generated in-project); Modifications: none, preserved native flat-chroma small-splash generation.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_splash_small_alpha_native.png` ? Source: adjacent project-original small-splash chroma master; License: project original, all rights reserved; URL: N/A; Modifications: flat chroma removed with the installed ImageGen helper, soft matte, and despill.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_splash_medium_chroma_native.png` ? Source: OpenAI built-in ImageGen using the accepted project-original small splash as continuity reference; License: project original, all rights reserved; URL: N/A; Modifications: none, preserved native flat-chroma medium-splash generation.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_splash_medium_alpha_native.png` ? Source: adjacent project-original medium-splash chroma master; License: project original, all rights reserved; URL: N/A; Modifications: flat chroma removed with the installed ImageGen helper, soft matte, and despill.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_splash_breach_chroma_native.png` ? Source: OpenAI built-in ImageGen using the accepted project-original small/medium splash family as continuity references; License: project original, all rights reserved; URL: N/A; Modifications: none, preserved native flat-chroma hero-breach generation.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_splash_breach_alpha_native.png` ? Source: adjacent project-original breach chroma master; License: project original, all rights reserved; URL: N/A; Modifications: flat chroma removed with the installed ImageGen helper, soft matte, and despill.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_ripple_ring_chroma_native.png` ? Source: OpenAI built-in ImageGen using the accepted project-original splash family as continuity references; License: project original, all rights reserved; URL: N/A; Modifications: none, preserved native flat-chroma ripple generation.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_ripple_ring_alpha_native.png` ? Source: adjacent project-original ripple chroma master; License: project original, all rights reserved; URL: N/A; Modifications: flat chroma removed with the installed ImageGen helper, soft matte, and despill.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_bubble_burst_chroma_native.png` ? Source: OpenAI built-in ImageGen using approved project-local castle bubbles and the accepted project-original water-FX family as references; License: project original, all rights reserved; URL: N/A; Modifications: none, preserved native flat-chroma bubble-burst generation.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_bubble_burst_alpha_native.png` ? Source: adjacent project-original bubble-burst chroma master; License: project original, all rights reserved; URL: N/A; Modifications: flat chroma removed with the installed ImageGen helper, soft matte, and despill.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_foamline_chroma_native.png` ? Source: OpenAI built-in ImageGen using the accepted project-original water-FX family as reference; License: project original, all rights reserved; URL: N/A; Modifications: none, preserved native flat-chroma foamline generation.
- `assets_src/imagegen/water_fx_2026-08-02/fx_water_foamline_alpha_native.png` ? Source: adjacent project-original foamline chroma master; License: project original, all rights reserved; URL: N/A; Modifications: flat chroma removed with the installed ImageGen helper, soft matte, and despill.
- `assets/sprites/fx_water/fx_water_splash_small_atlas.png` ? Source: accepted project-original small-splash alpha master above; License: project original, all rights reserved; URL: N/A; Modifications: uniform 0.70 saturation grade plus whole-cell normalization to 1024?512, 4?2 packing, and fixed bottom-center alignment by `tools/build_water_fx_atlases.py`.
- `assets/sprites/fx_water/fx_water_splash_medium_atlas.png` ? Source: accepted project-original medium-splash alpha master above; License: project original, all rights reserved; URL: N/A; Modifications: uniform 0.70 saturation grade plus whole-cell normalization to 1024?1024, reviewed eight-cell selection, transparent trailing cell, and fixed bottom-center alignment by `tools/build_water_fx_atlases.py`.
- `assets/sprites/fx_water/fx_water_splash_breach_atlas.png` ? Source: accepted project-original breach alpha master above; License: project original, all rights reserved; URL: N/A; Modifications: uniform 0.70 saturation grade plus whole-cell normalization to 1024?1024, transparent trailing cell, and fixed bottom-center alignment by `tools/build_water_fx_atlases.py`.
- `assets/sprites/fx_water/fx_water_ripple_ring_atlas.png` ? Source: accepted project-original ripple alpha master above; License: project original, all rights reserved; URL: N/A; Modifications: uniform 0.70 saturation grade plus whole-cell normalization to 1024?512, uniform 0.94 cell scale, 4?2 packing, and fixed-center alignment by `tools/build_water_fx_atlases.py`.
- `assets/sprites/fx_water/fx_water_bubble_burst_atlas.png` ? Source: accepted project-original bubble-burst alpha master above; License: project original, all rights reserved; URL: N/A; Modifications: uniform 0.70 saturation grade plus whole-cell normalization to 1024?512 and 4?2 packing by `tools/build_water_fx_atlases.py`, preserving the drawn rise relative to fixed cell center.
- `assets/sprites/fx_water/fx_water_foamline_strip.png` ? Source: accepted project-original foamline alpha master above; License: project original, all rights reserved; URL: N/A; Modifications: uniform 0.70 saturation grade plus whole-canvas normalization to 1024?256 and top-edge waterline alignment by `tools/build_water_fx_atlases.py`; no motion painted or synthesized.
## Pearl Castle authored object interactions v2 (2026-08-01)

All artwork in this v2 interaction pass is project-original OpenAI built-in
ImageGen output made from the approved project-local Pearl Castle cutouts.
No third-party visual source or external URL was used. Raw chroma masters are
preserved under `assets_src/` (excluded from runtime export). Runtime sheets
are non-destructive RGBA derivatives: chroma matte/despill, whole-state
registration to a fixed pivot, interior-alpha recovery, transparent padding,
and at most one uniform whole-sheet downscale. No tweened, composited, or
interpolated pixels were used to author an object state. License: project-owned
original, all rights reserved; source URL: N/A.

Runtime generated full-object state sheets (4 x 2, eight authored states each):

- `assets/flats/castle/interactions_v2/bubble_bath_bathtub_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/bubble_bath_rubber_duck_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/bubble_bath_sink_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/bubble_bath_toilet_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/craft_room_idea_board_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/craft_room_paint_table_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/craft_room_palette_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/craft_room_ribbon_rack_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/kitchen_fridge_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/kitchen_oven_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/kitchen_pan_1_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/kitchen_pan_2_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/kitchen_pan_3_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/kitchen_pan_4_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/kitchen_sink_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/library_book_stack_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/library_magic_book_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/library_pearl_lamp_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/library_pearl_table_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/main_hall_sconce_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/main_hall_tapestry_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/mermaid_pool_bubble_fountain_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/mermaid_pool_flower_float_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/mermaid_pool_star_float_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/mermaid_pool_waterfall_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/opera_hall_chandelier_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/opera_hall_curtains_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/opera_hall_footlights_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/opera_hall_stage_star_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/playroom_blocks_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/playroom_play_tent_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/playroom_stacking_toy_sheet.png` - generated full-object animation states; project-owned original.
- `assets/flats/castle/interactions_v2/playroom_stuffie_nook_sheet.png` - generated full-object animation states; project-owned original.

Preserved generated chroma/source masters:

- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/library_book_stack_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/library_magic_book_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/library_pearl_lamp_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/library_pearl_table_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/main_hall_sconce_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/main_hall_tapestry_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/opera_hall_chandelier_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/opera_hall_curtains_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/opera_hall_footlights_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/opera_hall_stage_star_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/kitchen_fridge_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/kitchen_pans/kitchen_pan_1_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/kitchen_pans/kitchen_pan_2_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/kitchen_pans/kitchen_pan_3_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/kitchen_pans/kitchen_pan_4_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/craft_room_idea_board_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/craft_room_paint_table_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/craft_room_palette_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/craft_room_ribbon_rack_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/mermaid_pool_flower_float_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/mermaid_pool_star_float_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/playroom_blocks_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/playroom_play_tent_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/playroom_stacking_toy_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/playroom_stuffie_nook_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/wet_rooms/bubble_bath_bathtub_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/wet_rooms/bubble_bath_rubber_duck_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/wet_rooms/bubble_bath_sink_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/wet_rooms/bubble_bath_toilet_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/wet_rooms/kitchen_oven_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/wet_rooms/kitchen_sink_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/wet_rooms/mermaid_pool_bubble_fountain_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.
- `assets_src/imagegen/castle_object_animations_v2/wet_rooms/mermaid_pool_waterfall_sheet_chroma.png` - accepted generated chroma master and provenance source; project-owned original.

Runtime fluid, audio, review, and provenance artifacts:

- `assets/shaders/castle_fixture_water.gdshader` - project-authored masked fixture-water shader; reuses already licensed in-repo ripple/caustic textures; no external source.
- `assets/audio/castle/fridge_open.ogg` - project-original deterministic latch/open/interior-chime synthesis; no samples or external source.
- `assets/audio/castle/fridge_close.ogg` - project-original deterministic door-close/latch synthesis; no samples or external source.
- `assets/flats/castle/interactions_v2/castle_interactions_v2.json` - project-authored runtime state, placement, water, physics, hash, and review manifest.
- `assets/flats/castle/interactions_v2/castle_interactions_v2_normalization.json` - project-authored fixed-pivot and alpha-normalization evidence ledger.
- `audit/castle_interactions_v2/castle_interaction_frames_v2.png` - project-authored all-state visual review contact sheet; development evidence, not runtime art.
- `assets_src/imagegen/castle_object_animations_v2/provenance.json` - exact refrigerator prompt, hashes, generation method, alpha QA, and Codex visual-review evidence (not owner/human approval).
- `assets_src/imagegen/castle_object_animations_v2/dry_rooms/provenance.json` - exact Main Hall, Opera Hall, and Library prompt/hash/review evidence.
- `assets_src/imagegen/castle_object_animations_v2/wet_rooms/provenance.json` - exact kitchen/bath/pool prompt/hash/review evidence.
- `assets_src/imagegen/castle_object_animations_v2/play_craft_pool/provenance.json` - exact playroom/craft/pool prompt/hash/review evidence.
- `assets_src/imagegen/castle_object_animations_v2/kitchen_pans/provenance.json` - exact four-pan prompt/hash/rejection/review evidence.

## Pearl Castle native-object interactions V4 (2026-08-04)

This corrective pass isolates and animates only objects already present in the
approved Pearl Castle rooms. All files in this section are project-owned
originals or non-destructive derivatives of already licensed project art; no
third-party visual source or external URL was used. Approved parent room images
remain unchanged. Exact source, native-generation, derivative, delivery, and
rejection hashes are recorded in the V4 runtime and ImageGen provenance
manifests. Rejected and superseded generations are non-runtime evidence only.

Runtime healed background tiles:

- `assets/flats/castle/interactions_v4/background_tiles/room_bubble_bath_background_r0_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_bubble_bath_background_r0_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_bubble_bath_background_r0_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_bubble_bath_background_r0_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_bubble_bath_background_r1_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_bubble_bath_background_r1_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_bubble_bath_background_r1_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_bubble_bath_background_r1_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_craft_room_background_r0_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_craft_room_background_r0_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_craft_room_background_r0_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_craft_room_background_r0_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_craft_room_background_r1_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_craft_room_background_r1_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_craft_room_background_r1_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_craft_room_background_r1_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r0_c0.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r0_c1.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r0_c2.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r0_c3.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r1_c0.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r1_c1.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r1_c2.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r1_c3.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r2_c0.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r2_c1.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r2_c2.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r2_c3.png` - project-authored non-destructive runtime tile of the V4 healed Kitchen plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_library_background_r0_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_library_background_r0_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_library_background_r0_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_library_background_r0_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_library_background_r1_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_library_background_r1_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_library_background_r1_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_library_background_r1_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_mermaid_pool_background_r0_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_mermaid_pool_background_r0_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_mermaid_pool_background_r0_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_mermaid_pool_background_r0_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_mermaid_pool_background_r1_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_mermaid_pool_background_r1_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_mermaid_pool_background_r1_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_mermaid_pool_background_r1_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_opera_hall_background_r0_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_opera_hall_background_r0_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_opera_hall_background_r0_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_opera_hall_background_r0_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_opera_hall_background_r1_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_opera_hall_background_r1_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_opera_hall_background_r1_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_opera_hall_background_r1_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_playroom_background_r0_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_playroom_background_r0_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_playroom_background_r0_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_playroom_background_r0_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_playroom_background_r1_c0.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_playroom_background_r1_c1.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_playroom_background_r1_c2.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.
- `assets/flats/castle/interactions_v4/background_tiles/room_playroom_background_r1_c3.png` - project-authored non-destructive runtime tile of the V4 healed room plate; project-owned derivative; no external source.

Full healed room plates:

- `assets/flats/castle/interactions_v4/backgrounds/room_bubble_bath_background.png` - project-authored non-destructive healed derivative of the approved room art; protected parent unchanged; no external source.
- `assets/flats/castle/interactions_v4/backgrounds/room_craft_room_background.png` - project-authored non-destructive healed derivative of the approved room art; protected parent unchanged; no external source.
- `assets/flats/castle/interactions_v4/backgrounds/room_kitchen_background.png` - project-authored non-destructive healed derivative of the approved Kitchen art, limited to the cleaned refrigerator's source-owned/live-frame union; protected parent unchanged; no external source.
- `assets/flats/castle/interactions_v4/backgrounds/room_library_background.png` - project-authored non-destructive healed derivative of the approved room art; protected parent unchanged; no external source.
- `assets/flats/castle/interactions_v4/backgrounds/room_mermaid_pool_background.png` - project-authored non-destructive healed derivative of the approved room art; protected parent unchanged; no external source.
- `assets/flats/castle/interactions_v4/backgrounds/room_opera_hall_background.png` - project-authored non-destructive healed derivative of the approved room art; protected parent unchanged; no external source.
- `assets/flats/castle/interactions_v4/backgrounds/room_playroom_background.png` - project-authored non-destructive healed derivative of the approved room art; protected parent unchanged; no external source.

Exact source-owned resting cards:

- `assets/flats/castle/interactions_v4/rest_cards/bubble_bath_vanity_mirror_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/craft_room_supply_cupboard_left_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/kitchen_fridge_rest.png` - exact-RGB derivative of the approved pre-existing teal Kitchen refrigerator card with contaminated purple-wall, neighboring-cabinet, sub-16-alpha, and sub-eight-pixel alpha components removed; no RGB repaint; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/library_ceiling_chandelier_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/library_pearl_lamp_right_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_flower_float_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_seahorse_fountain_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_star_float_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_waterfall_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/opera_hall_pearl_sconce_left_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/opera_hall_pearl_sconce_right_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/playroom_shelf_sailboat_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.
- `assets/flats/castle/interactions_v4/rest_cards/playroom_tent_flaps_right_rest.png` - exact-pixel, alpha-isolated derivative of the approved pre-existing room object; project-owned; no external source.

Eight-state runtime atlases:

- `assets/flats/castle/interactions_v4/sheets/bubble_bath_vanity_mirror_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/craft_room_supply_cupboard_left_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/kitchen_fridge_sheet.png` - project-authored RGBA 3-by-3 runtime derivative containing eight fixed-base refrigerator states and one unused cell; exact cleaned source-owned rest state replaces frame 0; generated-state segmentation, edge cleanup, method, and hash are recorded in the V4 runtime and ImageGen provenance manifests.
- `assets/flats/castle/interactions_v4/sheets/library_ceiling_chandelier_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/library_pearl_lamp_right_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/mermaid_pool_flower_float_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/mermaid_pool_seahorse_fountain_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/mermaid_pool_star_float_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/mermaid_pool_waterfall_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/opera_hall_pearl_sconce_left_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/opera_hall_pearl_sconce_right_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/playroom_shelf_sailboat_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.
- `assets/flats/castle/interactions_v4/sheets/playroom_tent_flaps_right_sheet.png` - project-authored RGBA 4-by-2 runtime derivative with exact rest state and fixed pivot; project-owned; exact source/method/hash in the V4 runtime manifest.

Ownership masks:

- `assets_src/castle/interactions_v4/masks/bubble_bath_vanity_mirror_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/craft_room_supply_cupboard_left_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/kitchen_fridge_existing_mask.png` - project-authored alpha ownership mask for the cleaned pre-existing Kitchen refrigerator; purple wall and neighboring cabinet are excluded; no external source.
- `assets_src/castle/interactions_v4/masks/library_ceiling_chandelier_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/library_pearl_lamp_right_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/mermaid_pool_flower_float_existing_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/mermaid_pool_seahorse_fountain_existing_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/mermaid_pool_star_float_existing_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/mermaid_pool_waterfall_existing_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/opera_hall_pearl_sconce_left_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/opera_hall_pearl_sconce_right_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/playroom_shelf_sailboat_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.
- `assets_src/castle/interactions_v4/masks/playroom_tent_flaps_right_mask.png` - project-authored ownership mask for a pre-existing approved room object; no external source.

Accepted built-in ImageGen sources and alpha derivatives used by runtime:

- `assets_src/imagegen/castle_object_animations_v4/craft_room/craft_room_supply_cupboard_left_sheet_alpha.png` - project-authored alpha derivative of an accepted project-owned OpenAI built-in ImageGen source; no external source.
- `assets_src/imagegen/castle_object_animations_v4/craft_room/craft_room_supply_cupboard_left_sheet_chroma.png` - hash-verified repository copy of accepted project-owned OpenAI built-in ImageGen output; no external source.
- `assets_src/imagegen/castle_object_animations_v4/kitchen/kitchen_fridge_sheet_checkerboard.png` - hash-verified byte-identical repository copy of the accepted 1536x1024 RGB OpenAI built-in ImageGen refrigerator source; its baked pale checker field is not true alpha/chroma and is removed only by the fully recorded deterministic segmentation in `PROVENANCE.json`; no external source.
- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/mermaid_pool_flower_float_sheet_alpha.png` - project-authored alpha derivative of an accepted project-owned OpenAI built-in ImageGen source; no external source.
- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/mermaid_pool_flower_float_sheet_chroma.png` - hash-verified repository copy of accepted project-owned OpenAI built-in ImageGen output; no external source.
- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/mermaid_pool_star_float_sheet_alpha.png` - project-authored alpha derivative of an accepted project-owned OpenAI built-in ImageGen source; no external source.
- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/mermaid_pool_star_float_sheet_chroma.png` - hash-verified repository copy of accepted project-owned OpenAI built-in ImageGen output; no external source.
- `assets_src/imagegen/castle_object_animations_v4/playroom/playroom_shelf_sailboat_sheet_alpha.png` - project-authored alpha derivative of an accepted project-owned OpenAI built-in ImageGen source; no external source.
- `assets_src/imagegen/castle_object_animations_v4/playroom/playroom_shelf_sailboat_sheet_chroma.png` - hash-verified repository copy of accepted project-owned OpenAI built-in ImageGen output; no external source.

Source-review pass superseded by the final ownership gate:

- `assets_src/imagegen/castle_object_animations_v4/playroom/playroom_tent_flaps_right_sheet_alpha.png` - project-authored alpha derivative that passed source review but is non-runtime because the tent outer canopy/knob is not source-owned.
- `assets_src/imagegen/castle_object_animations_v4/playroom/playroom_tent_flaps_right_sheet_chroma.png` - hash-verified project-owned OpenAI built-in ImageGen output that passed source review but is non-runtime because the tent outer canopy/knob is not source-owned.

Rejected built-in ImageGen evidence and alpha derivatives:

- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/mermaid_pool_seahorse_fountain_sheet_alpha.png` - rejected project-authored alpha derivative of project-owned ImageGen output; retained only as non-runtime provenance evidence after the final room review found body-color and silhouette drift.
- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/mermaid_pool_seahorse_fountain_sheet_chroma.png` - rejected hash-verified project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence after the final room review found body-color and silhouette drift.
- `assets_src/imagegen/castle_object_animations_v4/bubble_bath/rejected/rejected_source_ownership_bubble_bath_toilet_roll_sheet_alpha.png` - rejected project-authored alpha derivative of project-owned ImageGen output; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/bubble_bath/rejected/rejected_source_ownership_bubble_bath_toilet_roll_sheet_chroma.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/bubble_bath/rejected/toilet_roll_attempt1_includes_baked_holder.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/craft_room/rejected/craft_room_ribbon_rack_right_sheet_alpha.png` - rejected project-authored alpha derivative of project-owned ImageGen output; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/craft_room/rejected/craft_room_ribbon_rack_right_sheet_chroma.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/craft_room/rejected/supply_cupboard_attempt1_merged_layout.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/kitchen/rejected/attempt2_kitchen_tea_service_sheet_alpha.png` - rejected project-authored alpha derivative of project-owned ImageGen output; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/kitchen/rejected/attempt2_kitchen_tea_service_sheet_chroma.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/kitchen/rejected/rejected_source_ownership_kitchen_stove_pot_lid_sheet_alpha.png` - rejected project-authored alpha derivative of project-owned ImageGen output; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/kitchen/rejected/rejected_source_ownership_kitchen_stove_pot_lid_sheet_chroma.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/kitchen/rejected/rejected_source_ownership_kitchen_stove_pot_sheet_alpha.png` - rejected project-authored alpha derivative of project-owned ImageGen output; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/kitchen/rejected/rejected_source_ownership_kitchen_stove_pot_sheet_chroma.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/kitchen/rejected/tea_service_attempt1_spout_away_from_cup.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/kitchen/rejected/tea_service_attempt2_duplicate_baked_cup.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/kitchen/rejected/teapot_attempt3_clean_but_source_extraction_failed.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/rejected/attempt1_magenta_sheet_alpha_failed.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/rejected/attempt1_magenta_sheet_chroma.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/rejected/bubble_fountain_attempt1_design_drift.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/rejected/rejected_design_drift_mermaid_pool_waterfall_sheet_alpha.png` - rejected project-authored alpha derivative of project-owned ImageGen output; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/mermaid_pool/rejected/rejected_design_drift_mermaid_pool_waterfall_sheet_chroma.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/playroom/rejected/full_arch_playroom_play_tent_right_sheet_alpha.png` - rejected project-authored alpha derivative of project-owned ImageGen output; retained only as non-runtime provenance evidence.
- `assets_src/imagegen/castle_object_animations_v4/playroom/rejected/full_arch_playroom_play_tent_right_sheet_chroma.png` - rejected project-owned OpenAI built-in ImageGen output/repository copy; retained only as non-runtime provenance evidence.

Runtime and provenance records:

- `assets/flats/castle/interactions_v4/castle_interactions_v4.json` - project-authored runtime delivery, frame, placement, ownership, water, physics, and hash manifest.
- `assets_src/castle/interactions_v4/castle_interaction_frame_approval_ledger.json` - project-authored exact-hash Codex visual-review ledger for all 104 authored runtime states and every measured static-card occlusion relation; no external source.
- `assets_src/imagegen/castle_object_animations_v4/PROVENANCE.json` - project-authored built-in generation attempt, native-path/ID, source, derivative, status, reason, and hash ledger.
- `CASTLE_NATIVE_INTERACTIONS_V4_AUDIT_2026-08-04.md` - project-authored comprehensive placement, blending, child-interest, animation-semantics, rejection, and duplication audit.

## Pearl Castle static depth-card alpha repair (2026-08-04)

The existing room foreground cards retain their approved source RGB wherever
visible. This pass only tightens alpha to reviewed physical subjects, clears RGB
beneath fully transparent pixels, and retires the Pool's full-water-oval mid card
from runtime; no object or background art was generated or repainted.

- `assets_src/castle/depth_cards/source_alpha/room_bubble_bath_front_left_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Bubble Bath foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_bubble_bath_front_right_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Bubble Bath foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_craft_room_front_left_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Craft Room foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_craft_room_front_right_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Craft Room foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_kitchen_front_left_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Kitchen foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_kitchen_front_right_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Kitchen foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_library_front_left_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Library foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_library_front_right_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Library foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_main_hall_front_left_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Main Hall foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_main_hall_front_right_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Main Hall foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_mermaid_pool_front_left_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Mermaid Pool foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_mermaid_pool_front_right_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Mermaid Pool foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_opera_hall_front_left_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Opera Hall foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_opera_hall_front_right_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Opera Hall foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_playroom_front_left_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Playroom foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/source_alpha/room_playroom_front_right_alpha.png` - lossless pre-repair alpha channel preserved from the project-owned Playroom foreground card; audit/rebuild source only.
- `assets_src/castle/depth_cards/static_depth_card_refinement.json` - project-authored exact source/output hash, reviewed keep-shape, alpha/RGB metric, placement, retirement, and contact-sheet provenance ledger; no external source.
- `audit/castle_static_depth_cards/static_depth_card_refinement_contact.png` - deterministic project-authored before/after checkerboard review sheet for all sixteen retained static depth cards; generated only from the licensed card/source pixels and alpha evidence above; no external source.

## Opera Codex art regeneration - 2026-08-02

OpenAI built-in ImageGen natives and project-authored non-destructive derivatives/composites. Copyright Mermaid Roshan LLC; no external asset license. Approved in-repo Opera cards used by Path-A widget compositions retain their existing provenance and licenses.

- `assets/opera/worlds/backdrops/stage_astronaut_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_astronaut_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_astronaut_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_astronaut_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_ballerina_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_ballerina_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_ballerina_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_ballerina_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_boxer_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_boxer_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_boxer_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_boxer_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_candymaker_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_candymaker_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_candymaker_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_candymaker_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_chef_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_chef_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_chef_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_chef_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_detective_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_detective_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_detective_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_detective_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_doctor_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_doctor_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_doctor_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_doctor_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_farmer_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_farmer_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_farmer_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_farmer_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_magician_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_magician_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_magician_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_magician_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_nursery_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_nursery_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_nursery_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_nursery_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_painter_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_painter_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_painter_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_painter_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_popstar_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_popstar_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_popstar_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_popstar_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_racer_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_racer_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_racer_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/stage_racer_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_astronaut_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_astronaut_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_astronaut_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_astronaut_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_ballerina_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_ballerina_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_ballerina_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_ballerina_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_boxer_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_boxer_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_boxer_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_boxer_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_candymaker_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_candymaker_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_candymaker_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_candymaker_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_chef_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_chef_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_chef_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_chef_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_detective_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_detective_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_detective_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_detective_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_doctor_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_doctor_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_doctor_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_doctor_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_farmer_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_farmer_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_farmer_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_farmer_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_magician_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_magician_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_magician_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_magician_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_nursery_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_nursery_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_nursery_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_nursery_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_painter_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_painter_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_painter_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_painter_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_popstar_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_popstar_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_popstar_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_popstar_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_racer_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_racer_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_racer_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/backdrops/world_racer_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/props/goal_nursery.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/stage/finale_stage_c0r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/stage/finale_stage_c0r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/stage/finale_stage_c1r0.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/stage/finale_stage_c1r1.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/ui/magnifier.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/ui/station_marker.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/ui/task_card_frame.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_basin_doctor.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_basin_doctor_bubbles.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_basin_nursery.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_basin_nursery_bubbles.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_basin_shared_shine.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_catch_nursery.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_catch_nursery_cradle.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_catch_nursery_pillows.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_astronaut.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_astronaut_full.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_astronaut_glow.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_ballerina.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_ballerina_full.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_ballerina_glow.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_farmer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_farmer_full.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_farmer_glow.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_magician.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_magician_full.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_magician_glow.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_popstar.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_popstar_full.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_charge_popstar_glow.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_astronaut.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_astronaut_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_astronaut_progress.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_ballerina.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_ballerina_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_ballerina_progress.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_candymaker.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_candymaker_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_candymaker_progress.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_chef.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_chef_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_chef_progress.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_doctor.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_doctor_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_doctor_progress.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_magician.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_magician_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_magician_progress.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_painter.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_painter_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_painter_progress.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_popstar.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_popstar_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_popstar_progress.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_racer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_racer_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_crank_racer_progress.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_gauge_astronaut.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_gauge_astronaut_success.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_gauge_chef.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_gauge_chef_success.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_gauge_racer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_gauge_racer_success.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_gauge_shared_needle.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_astronaut.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_astronaut_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_ballerina.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_ballerina_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_boxer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_boxer_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_candymaker.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_candymaker_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_detective.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_detective_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_doctor.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_doctor_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_farmer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_farmer_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_magician.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_magician_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_painter.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_painter_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_popstar.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_popstar_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_lanes_shared_pick.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_candymaker.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_candymaker_fill.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_candymaker_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_chef.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_chef_fill.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_chef_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_nursery.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_nursery_fill.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_nursery_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_painter.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_painter_fill.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_pour_painter_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_push_boxer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_push_boxer_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_push_farmer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_push_farmer_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_push_nursery.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_push_nursery_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_push_racer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_push_racer_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_push_shared_arrow_down.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_push_shared_arrow_lr.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_astronaut.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_astronaut_mark.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_astronaut_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_boxer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_boxer_mark.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_boxer_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_boxer_success.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_candymaker.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_candymaker_mark.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_candymaker_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_chef.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_chef_mark.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_chef_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_doctor.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_doctor_mark.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_doctor_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_farmer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_farmer_mark.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_farmer_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_painter.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_painter_mark.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_painter_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_racer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_racer_mark.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_target_racer_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_ballerina.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_ballerina_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_chef.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_chef_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_detective.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_detective_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_doctor.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_doctor_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_magician.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_magician_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_painter.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_trace_painter_lit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_ballerina.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_ballerina_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_boxer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_boxer_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_candymaker.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_candymaker_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_detective.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_detective_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_farmer.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_farmer_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_magician.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_magician_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_nursery.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_nursery_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_popstar.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_popstar_mover.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets/opera/worlds/widgets/widget_track_shared_hit.png` - project-authored runtime derivative/composite from project-owned Opera art; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_finale_master_2048.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_astronaut.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_ballerina.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_boxer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_candymaker.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_chef.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_detective.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_doctor.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_farmer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_magician.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_nursery.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_painter.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_popstar.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_racer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_astronaut.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_ballerina.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_boxer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_candymaker.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_chef.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_detective.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_doctor.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_farmer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_magician.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_nursery.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_painter.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_popstar.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_racer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_basin_doctor.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_basin_nursery.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_catch_nursery.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_charge_astronaut.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_charge_ballerina.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_charge_farmer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_charge_magician.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_charge_popstar.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_crank_astronaut.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_crank_ballerina.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_crank_candymaker.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_crank_chef.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_crank_doctor.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_crank_magician.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_crank_painter.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_crank_popstar.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_crank_racer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_gauge_astronaut.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_gauge_chef.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_gauge_racer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_lanes_astronaut.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_lanes_ballerina.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_lanes_boxer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_lanes_candymaker.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_lanes_detective.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_lanes_doctor.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_lanes_farmer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_lanes_magician.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_lanes_painter.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_lanes_popstar.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_pour_candymaker.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_pour_chef.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_pour_nursery.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_pour_painter.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_push_boxer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_push_farmer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_push_nursery.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_push_racer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_target_astronaut.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_target_boxer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_target_candymaker.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_target_chef.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_target_doctor.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_target_farmer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_target_painter.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_target_racer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_trace_ballerina.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_trace_chef.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_trace_detective.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_trace_doctor.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_trace_magician.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_trace_painter.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_track_ballerina.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_track_boxer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_track_candymaker.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_track_detective.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_track_farmer.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_track_magician.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_track_nursery.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/cards/widget_track_popstar.png` - project-authored staging master or Path-A composition derived from project-owned Opera art; non-destructive; no external source.
- `assets_src/concepts/opera_regeneration_2026-08-01/contact_sheets/opera_p7_gameplay_scale_1280x720.png` - project-authored visual QA evidence derived from the licensed Opera delivery; not runtime art.
- `assets_src/concepts/opera_regeneration_2026-08-01/contact_sheets/opera_widgets_contact_01.png` - project-authored visual QA evidence derived from the licensed Opera delivery; not runtime art.
- `assets_src/concepts/opera_regeneration_2026-08-01/contact_sheets/opera_widgets_contact_02.png` - project-authored visual QA evidence derived from the licensed Opera delivery; not runtime art.
- `assets_src/concepts/opera_regeneration_2026-08-01/contact_sheets/opera_widgets_contact_03.png` - project-authored visual QA evidence derived from the licensed Opera delivery; not runtime art.
- `assets_src/concepts/opera_regeneration_2026-08-01/contact_sheets/opera_widgets_contact_04.png` - project-authored visual QA evidence derived from the licensed Opera delivery; not runtime art.
- `assets_src/concepts/opera_regeneration_2026-08-01/contact_sheets/opera_widgets_contact_05.png` - project-authored visual QA evidence derived from the licensed Opera delivery; not runtime art.
- `assets_src/concepts/opera_regeneration_2026-08-01/contact_sheets/opera_widgets_contact_06.png` - project-authored visual QA evidence derived from the licensed Opera delivery; not runtime art.
- `assets_src/concepts/opera_regeneration_2026-08-01/contact_sheets/opera_widgets_contact_07.png` - project-authored visual QA evidence derived from the licensed Opera delivery; not runtime art.
- `assets_src/imagegen/opera_codex_2026-08-02/native/candymaker_chutes_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/doctor_xray_viewer_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/goal_nursery_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/magician_rope_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/magnifier_alpha_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/magnifier_chroma_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/opera_stage_finale_master_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_astronaut_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_ballerina_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_boxer_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_candymaker_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_chef_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_detective_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_doctor_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_farmer_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_magician_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_nursery_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_painter_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_popstar_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/stage_racer_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/station_marker_alpha_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/station_marker_chroma_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/task_card_frame_alpha_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/task_card_frame_chroma_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_astronaut_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_ballerina_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_boxer_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_candymaker_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_chef_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_detective_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_doctor_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_farmer_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_magician_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_nursery_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_painter_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_popstar_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.
- `assets_src/imagegen/opera_codex_2026-08-02/native/world_racer_native.png` - accepted OpenAI ImageGen native or transparent derived native; project-owned original; source/prompt/hash in OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json.

## Fable Opera animation review kit (2026-08-04)

- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/review_masters/opera_imp_family_master_contact.png` - project-authored Godot 4.7.1 Mobile-render visual QA evidence copied byte-for-byte from the ignored Opera capture tree; not runtime art; source and SHA-256 in the adjacent manifest.
- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/review_masters/opera_60_widget_master_contact.png` - project-authored Godot 4.7.1 Mobile-render visual QA evidence copied byte-for-byte from the ignored Opera capture tree; not runtime art; source and SHA-256 in the adjacent manifest.
- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/review_masters/opera_12_rival_master_contact.png` - project-authored Godot 4.7.1 Mobile-render visual QA evidence copied byte-for-byte from the ignored Opera capture tree; not runtime art; source and SHA-256 in the adjacent manifest.
- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/review_masters/opera_selected_scuffles_master_contact.png` - project-authored Godot 4.7.1 Mobile-render visual QA evidence copied byte-for-byte from the ignored Opera capture tree; not runtime art; source and SHA-256 in the adjacent manifest.
- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/review_masters/opera_stress_master_contact.png` - project-authored Godot 4.7.1 Mobile-render visual QA evidence copied byte-for-byte from the ignored Opera capture tree; not runtime art; source and SHA-256 in the adjacent manifest.
- `assets/audio/sfx/combat_*.wav` (combat_pop, combat_bonk, combat_poof,
  combat_freeze, combat_charge_ring, combat_fizzle) — synthesized entirely
  by `tools/gen_combat_sfx.py` in this repository (deterministic
  pure-stdlib waveforms, seeded noise, no external sources, no recordings).
  The combat feel-stack reaction voices: hit pop, harm bonk, death poof,
  freeze tinkle, charge-ring shimmer, kind-miss fizzle. Owner-recorded
  replacements can drop in at the same paths (all callers check
  ResourceLoader.exists). License: project code.

## Combat tutorial training art (2026-08-01)

- `assets/castle/training/training_grotto_backdrop.png`,
  `ghost_hand.png`, `verb_chip_tap.png`, `verb_chip_hold.png`, and their
  preservation masters under
  `assets_src/imagegen/combat_tutorial_2026-08-01/` are project-original art
  generated with OpenAI built-in image generation on 2026-08-01. License:
  project original. URL: none (project-local generation). The backdrop was
  whole-canvas resized to 2048x1024. The three simple opaque subjects were
  generated on flat green, converted to alpha with the installed Codex chroma
  helper using soft matte and despill, then whole-canvas resized to 512x512 or
  256x256. Exact prompts, generation identifiers, dimensions, hashes, reuse
  audit, and processing notes are recorded in the adjacent `PROMPTS.md`.

## Seek animated Evie and Lamb-a' actors (2026-08-09)

- `assets_src/imagegen/seek_animated_2026-08-09/evie_atlas_chroma.png` -
  project-original eight-frame Evie animation source generated with OpenAI
  built-in image generation on 2026-08-09. License: project original. URL:
  none (project-local generation). The protected
  `assets/characters/friends/pearl_friend.png` was used read-only as an
  identity reference and was not modified or copied into the delivery.
  Source SHA-256:
  `2b1cd2703388f14525603146545d7b9299e53d68e0d0ead449b3a5d85fe40597`.
- `assets_src/imagegen/seek_animated_2026-08-09/lamma_atlas_chroma.png` -
  project-original eight-frame Lamb-a' animation source generated with OpenAI
  built-in image generation on 2026-08-09. License: project original. URL:
  none (project-local generation). Existing Lamb-a' art was used read-only as
  identity reference; no protected original was modified. Source SHA-256:
  `7f38bb41209073f38aaec2cd4a99ed609154da71b02a383e89bfa58548a051fa`.
- `assets/minigames/seek/evie_animation.png`,
  `assets/minigames/seek/lamma_animation.png`, and
  `assets/minigames/seek/evie_portrait.png` - project-authored deterministic
  transparent derivatives of the two project-original sources above. The
  repository builder removes border-connected chroma, removes bounded
  cross-cell fragments, normalizes complete drawings into a 4x2 grid of
  256x256 cells, and decontaminates residual chroma only in a narrow
  transparent-edge shell; it does not alter the protected reference art.
  Runtime SHA-256 values are recorded in the adjacent build manifest.
- `assets_src/imagegen/seek_animated_2026-08-09/PROMPTS.md` and
  `build_manifest.json` - project-authored provenance records containing the
  exact prompts, declared references, source/output hashes, frame semantics,
  and deterministic processing evidence. `tools/build_seek_animation_assets.py`
  is the binding reproducible builder and `--check` validator.

## Opera Roshan career animation atlases (2026-08-09)

All accepted-generation, identity, costume, topology, row-contract, native-hash,
and runtime-hash review evidence is recorded in
`assets_src/imagegen/opera_roshan_animation_2026-08-09/OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
Each adjacent per-career `*_pack_report.json` records the exact alpha input,
4x4 component assignment, shared scale, 256px-cell packing, output path, and
input/output hashes.

- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_astronaut_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_astronaut_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_ballerina_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_ballerina_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_boxer_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_boxer_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_candymaker_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_candymaker_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_chef_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_chef_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_detective_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_detective_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_doctor_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_doctor_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_farmer_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_farmer_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_magician_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_magician_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_nursery_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_nursery_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_painter_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_painter_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_popstar_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_popstar_sheet_a_pack_report.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_racer_sheet_a_native.png` - project-owned original generated with built-in OpenAI ImageGen; URL none; acceptance and hash recorded in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json` and `roshan_racer_sheet_a_pack_report.json`.

- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_astronaut_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_astronaut_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_astronaut_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_ballerina_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_ballerina_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_ballerina_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_boxer_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_boxer_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_boxer_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_candymaker_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_candymaker_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_candymaker_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_chef_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_chef_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_chef_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_detective_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_detective_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_detective_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_doctor_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_doctor_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_doctor_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_farmer_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_farmer_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_farmer_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_magician_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_magician_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_magician_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_nursery_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_nursery_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_nursery_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_painter_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_painter_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_painter_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_popstar_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_popstar_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_popstar_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets_src/imagegen/opera_roshan_animation_2026-08-09/roshan_racer_sheet_a_alpha_native.png` - non-destructive transparency derivative of `roshan_racer_sheet_a_native.png` made with the installed `remove_chroma_key.py`; original preserved; alpha-input hash recorded in `roshan_racer_sheet_a_pack_report.json` and review chain in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.

- `assets/opera/worlds/actors/animation/roshan_astronaut_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_astronaut_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_astronaut_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_ballerina_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_ballerina_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_ballerina_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_boxer_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_boxer_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_boxer_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_candymaker_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_candymaker_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_candymaker_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_chef_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_chef_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_chef_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_detective_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_detective_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_detective_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_doctor_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_doctor_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_doctor_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_farmer_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_farmer_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_farmer_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_magician_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_magician_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_magician_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_nursery_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_nursery_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_nursery_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_painter_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_painter_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_painter_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_popstar_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_popstar_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_popstar_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.
- `assets/opera/worlds/actors/animation/roshan_racer_sheet_a.png` - non-destructive 4x4 runtime atlas packed from `roshan_racer_sheet_a_alpha_native.png` by `tools/prepare_opera_roshan_animation.py`; exact cell transforms and hashes in `roshan_racer_sheet_a_pack_report.json` and acceptance in `OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.

## Opera lobby crest runtime derivatives (2026-08-09)

Each file below is a non-destructive whole-image 256x256 derivative of the
named approved project source, made without repainting by
`ffmpeg -i SOURCE -vf scale=256:256:flags=lanczos -frames:v 1 OUTPUT`; the
approved source remains preserved and its existing project license carries
through to the runtime derivative. For the sixteen `opera_crest_*` files, the
connected navy square outside the oval was then converted to transparency with
the installed `remove_chroma_key.py --auto-key border --soft-matte
--transparent-threshold 18 --opaque-threshold 72 --edge-feather 0.7 --despill`
helper; this changes alpha only and preserves the approved RGB crest artwork.
`goal_nursery.png` already had authored alpha and received only the resize.

- `assets/opera/worlds/ui/crests/goal_nursery.png` - 256x256 Lanczos derivative of approved source `assets/opera/worlds/props/goal_nursery.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_ballerina.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_ballerina.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_boxer.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_boxer.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_candy.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_candy.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_chef.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_chef.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_detective.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_detective.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_doctor.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_doctor.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_dragon.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_dragon.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_engineer.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_engineer.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_farmer.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_farmer.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_house.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_house.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_maestro.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_maestro.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_magician.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_magician.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_painter.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_painter.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_phantom.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_phantom.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_racer.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_racer.png`; no external source or new RGB artwork.
- `assets/opera/worlds/ui/crests/opera_crest_singer.png` - 256x256 Lanczos derivative of approved source `assets_src/concepts/opera_house_flat/cards/opera_crest_singer.png`; no external source or new RGB artwork.

## Opera minigame quality art (2026-08-09 through 2026-08-10)

All files in this section are project-original art or non-destructive derivatives
of approved project-original Opera art; license: project original; URL: none.
`assets_src/imagegen/opera_minigame_quality_2026-08-09/PROVENANCE.json`
records every exact source path and SHA-256, runtime SHA-256, crop/composite/matte/
resize operation, generated-source prompt and result identifier, and artifact QA
result. Derivatives were built deterministically by
`tools/prepare_opera_minigame_art.py`; all approved source masters are preserved.

- `assets_src/imagegen/opera_minigame_quality_2026-08-09/opera_minigame_prop_sheet_native.png` - project-owned OpenAI built-in ImageGen source board generated 2026-08-09; exact prompt, result ID, original result path, and SHA-256 are in `PROVENANCE.json`.
- `assets_src/imagegen/opera_minigame_quality_2026-08-09/opera_minigame_prop_sheet_alpha_native.png` - non-destructive alpha derivative of the preserved native board made with installed `remove_chroma_key.py`; exact command, matte report, and hashes are in `PROVENANCE.json`.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/GENERATION.json` - project-authored generation/provenance manifest for the scoped Candy Maker SYRUP replacement; records every exact prompt, result ID, project-local reference, accepted role, and local alpha/mask operation; no external source or URL.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_empty_draft_native.png` - project-owned OpenAI built-in ImageGen full-frame composition source; preserved as the input to the accepted project-style transfer; no external source or URL.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_empty_native.png` - accepted project-owned OpenAI built-in ImageGen full-bleed empty-mold backdrop, restyled using only the shipped project-owned Candy Maker world as visual reference; no external source or URL.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_full_native.png` - project-owned OpenAI built-in ImageGen full-syrup visual reference; preserved for provenance but not used as registered runtime geometry because the edit changed the shell outline slightly; no external source or URL.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_fill_chroma_native.png` - project-owned OpenAI built-in ImageGen cavity-only amber/marbled syrup source on flat chroma, generated from the accepted empty mold reference; no external source or URL.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_fill_alpha_native.png` - non-destructive alpha derivative of the preserved cavity-only syrup source made with the installed `remove_chroma_key.py`; exact command is in `GENERATION.json`.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_ladle_style_reference.png` - immutable project-owned copy of the pre-replacement Candy Maker syrup jug supplied to ImageGen only as a style/detail reference; preserved from repository commit `39746756`; no external source or URL.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_ladle_chroma_native.png` - project-owned OpenAI built-in ImageGen right-facing copper candy-syrup ladle source on flat chroma, styled only from approved project-owned Opera art; no external source or URL.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_ladle_alpha_native.png` - non-destructive alpha derivative of the preserved copper-ladle source made with the installed `remove_chroma_key.py`; exact command is in `GENERATION.json`.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_ladle_empty_chroma_native.png` - project-owned OpenAI built-in ImageGen edit of the accepted right-facing ladle on flat chroma; changes only the bowl from syrup-bearing to visibly dry; no external source or URL.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_ladle_empty_alpha_native.png` - non-destructive alpha derivative of the preserved empty-ladle source made with the installed `remove_chroma_key.py`; exact prompt, result ID, command, and project-local reference are in `GENERATION.json`.
- `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/candymaker_syrup_cavity_mask.png` - reviewed non-runtime registration mask derived from the accepted empty backdrop; used byte-for-byte to keep syrup inside the authored shell hollow; derivation parameters are in `GENERATION.json`.
- `assets/opera/worlds/widgets/widget_pour_chef_mover.png` - 256x256 alpha batter-pitcher cell derived from the reviewed generated board.
- `assets/opera/worlds/widgets/widget_pour_candymaker.png` - 1024x576 opaque full-bleed Candy Maker workspace derived by whole-canvas Lanczos resize from the accepted empty-mold native; replaces the card, finished candy, cropped plates, tab, and pill.
- `assets/opera/worlds/widgets/widget_pour_candymaker_fill.png` - 1024x576 transparent cavity-only molten-syrup derivative; accepted alpha source is fitted to and intersected with the reviewed empty-mold mask, with no pixels outside the receiver.
- `assets/opera/worlds/widgets/widget_pour_candymaker_mover.png` - 512x256 transparent right-facing copper-ladle derivative, aspect-fitted from the accepted alpha native with safe padding and no chroma spill.
- `assets/opera/worlds/widgets/widget_pour_candymaker_mover_empty.png` - 512x256 transparent matching dry-ladle derivative shown as the syrup reserve empties and throughout accepted completion.
- `assets/opera/worlds/widgets/widget_pour_nursery_mover.png` - 256x256 alpha feeding-bottle cell derived from the reviewed generated board.
- `assets/opera/worlds/widgets/widget_crank_racer_mover.png` - 256x256 alpha mechanic-wrench cell derived from the reviewed generated board.
- `assets/opera/worlds/widgets/widget_clue_board_empty.png` - full 1024x608 Detective case-board state derived from the approved empty case-board source.
- `assets/opera/worlds/widgets/widget_clue_board_complete.png` - full 1024x608 Detective case-board state derived from the approved complete case-board source.
- `assets/opera/worlds/widgets/widget_clue_board_tokens.png` - 3x256 paw/feather/ribbon strip derived from the three approved Detective clue sources.
- `assets/opera/worlds/widgets/widget_crown_chest_closed.png` - 512x512 alpha object derived from the approved closed clue-chest source.
- `assets/opera/worlds/widgets/widget_crown_chest_open.png` - 512x512 alpha object derived from the approved open clue-chest/tiara source.
- `assets/opera/worlds/widgets/widget_magic_cabinet_closed.png` - 512x512 alpha cabinet derived from the approved closed trick-cabinet source.
- `assets/opera/worlds/widgets/widget_magic_cabinet_reveal.png` - 512x512 open-door reveal composite derived from the approved cabinet shell and approved Lamba reveal, with the reveal clipped inside the transparent cabinet opening.
- `assets/opera/worlds/widgets/widget_magic_vanish_hat.png` - 512x512 alpha prop derived from the approved open magic-hat source.
- `assets/opera/worlds/widgets/widget_magic_vanish_wand.png` - 512x512 alpha prop derived from the approved pearl-wand source.
- `assets/opera/worlds/widgets/widget_magic_vanish_reveal.png` - 512x512 coherent Lamba-over-hat reveal derived from approved Lamba and open-hat sources.
- `assets/opera/worlds/widgets/widget_portal_magician_mover.png` - 256x256 portal-only alpha mover derived from the approved Opera upper-access open-portal source.
- `assets/opera/worlds/widgets/widget_crank_racer.png` - 1024x608 pit-tune card derived from the established Racer widget frame and approved side-kart/toolkit sources.
- `assets/opera/worlds/widgets/widget_crank_racer_wheel.png` - 256x256 installable wheel derived from the approved side-kart source.
- `assets/opera/worlds/widgets/widget_crank_popstar_mover.png` - 256x256 finale mover derived from the approved active microphone/sound-wave source.
- `assets/opera/worlds/widgets/widget_gauge_chef_success.png` - 1024x608 achieved overlay derived from the approved finished-cake source.
- `assets/opera/worlds/widgets/widget_target_chef_mark.png` - 128x128 thematic target mark derived from the approved Chef badge source.
- `assets/opera/worlds/widgets/widget_target_chef_piece_0.png` - 256x256 isolated cherry topping derived from the approved Chef placement-glows source; serving display and shadow excluded by connected colour matte.
- `assets/opera/worlds/widgets/widget_target_chef_piece_1.png` - 256x256 isolated cream topping derived from the approved Chef placement-glows source; serving display and shadow excluded by connected colour matte.
- `assets/opera/worlds/widgets/widget_target_chef_piece_2.png` - 256x256 isolated chocolate topping derived from the approved Chef placement-glows source; serving display and shadow excluded by connected colour matte.
- `assets/opera/worlds/widgets/widget_target_candymaker_mark.png` - 128x128 thematic target mark derived from the approved Candy Maker badge source.
- `assets/opera/worlds/widgets/widget_target_candymaker_piece_0.png` - 256x256 candy token derived from the approved coral-flower artwork stored in the audited `teal_spiral_candy` source export.
- `assets/opera/worlds/widgets/widget_target_candymaker_piece_1.png` - 256x256 candy token derived from the approved teal-shell artwork stored in the audited `plum_wrapped_candy` source export.
- `assets/opera/worlds/widgets/widget_target_candymaker_piece_2.png` - 256x256 candy token derived from the approved plum-wrapped artwork stored in the audited `cream_heart_candy` source export.
- `assets/opera/worlds/widgets/widget_target_farmer_mark.png` - 128x128 thematic target mark derived from the approved Farmer badge source.
- `assets/opera/worlds/widgets/widget_target_farmer_piece_0.png` - 256x256 carrot token derived from the approved carrot artwork stored in the audited Farmer `hay_bale` source export.
- `assets/opera/worlds/widgets/widget_target_farmer_piece_1.png` - 256x256 corn token derived from the approved corn artwork stored in the audited Farmer `piggy_fed` source export.
- `assets/opera/worlds/widgets/widget_target_farmer_piece_2.png` - 256x256 pumpkin token derived from the approved pumpkin artwork stored in the audited Farmer `piggy_munch` source export.
- `assets/opera/worlds/widgets/widget_target_astronaut_mark.png` - 128x128 project-original code-drawn thematic target mark using the established Opera palette and approved Astronaut widget source reference.
- `assets/opera/worlds/widgets/widget_target_astronaut_piece_0.png` - 256x256 project-original code-drawn shell patch using the established Opera palette and approved Astronaut widget source reference.
- `assets/opera/worlds/widgets/widget_target_astronaut_piece_1.png` - 256x256 project-original code-drawn rivet patch using the established Opera palette and approved Astronaut widget source reference.
- `assets/opera/worlds/widgets/widget_target_astronaut_piece_2.png` - 256x256 project-original code-drawn repair patch using the established Opera palette and approved Astronaut widget source reference.
- `assets/opera/worlds/widgets/widget_target_painter_mark.png` - 128x128 literal paint-splat mark cropped from the approved Painter splat-state source.
- `assets_src/imagegen/opera_minigame_quality_2026-08-09/OPERA_MINIGAME_ART_CONTACT_SHEET_2026-08-09.png` - deterministic project-authored visual-QA contact sheet of every runtime derivative above; not runtime art.

## Opera diegetic hotspot gap art (2026-08-09)

Project-original OpenAI built-in ImageGen art; license: project original; URL:
none. Generation was limited to the single verified gap: an isolated Magician
`ROPE` object. `assets_src/imagegen/opera_diegetic_hotspots_2026-08-09/`
records the exact reference, two attempts (including the rejected artifact
attempt), prompts, result IDs, hashes, alpha command, deterministic runtime
normalization, and Codex artifact review. Owner/human review remains pending.

- `assets_src/imagegen/opera_diegetic_hotspots_2026-08-09/native/magician_rope_native.png` - preserved 1254×1254 chroma native generated from the approved Magician trace-card reference; no external source.
- `assets_src/imagegen/opera_diegetic_hotspots_2026-08-09/magician_rope_alpha_native.png` - 1254×1254 non-destructive alpha derivative made with the installed `remove_chroma_key.py`; source native preserved.
- `assets/opera/worlds/hotspots/magician_rope.png` - 512×128 POT Lanczos runtime derivative of the accepted alpha native; whole rope retained with 16/22/16/22-pixel alpha margins.

## Opera borderless pit-stop kart (2026-08-10)

- `assets_src/imagegen/opera_borderless_pitstop_2026-08-10/native/racer_pitstop_kart_chroma_native.png` - project-owned OpenAI built-in ImageGen source, generated from the approved Opera Racer card as a design/style reference; exact prompt, result path, review state, and SHA-256 are in the adjacent `PROMPT.md`, `REVIEW.md`, and `PROVENANCE.json`.
- `assets_src/imagegen/opera_borderless_pitstop_2026-08-10/racer_pitstop_kart_alpha_native.png` - non-destructive alpha derivative made with the installed `remove_chroma_key.py` helper; source native preserved; exact matte command and metrics are in `PROVENANCE.json`.
- `assets/opera/worlds/widgets/widget_crank_racer_kart.png` - 512×512 RGBA/POT whole-canvas Lanczos runtime derivative; one connected borderless side-view kart with its approved front wheel and intentional empty rear wheel arch; project-owned, no external source.

## Opera borderless Doctor patient (2026-08-10)

- `assets_src/imagegen/opera_borderless_doctor_2026-08-10/native/doctor_starfish_patient_chroma_native.png` - project-owned OpenAI built-in ImageGen source, generated from the approved Opera Doctor card as a character/style reference; exact prompt, result path, review state, and SHA-256 are in the adjacent `PROMPT.md`, `REVIEW.md`, and `PROVENANCE.json`.
- `assets_src/imagegen/opera_borderless_doctor_2026-08-10/doctor_starfish_patient_alpha_native.png` - non-destructive alpha derivative made with the installed `remove_chroma_key.py` helper; source native preserved; exact matte command and metrics are in `PROVENANCE.json`.
- `assets/opera/worlds/widgets/widget_crank_doctor_patient.png` - 512×512 RGBA/POT whole-canvas Lanczos runtime derivative; one connected five-armed starfish plush with no pre-painted bandage, allowing the minigame to animate the wrap causally; project-owned, no external source.

## Personalized pearl-castle banner art (2026-08-10)

All files in this section are project-original OpenAI built-in ImageGen art or
non-destructive derivatives of it; license: project original; URL: none. The
exact prompts, reference paths, generation-result identifiers, SHA-256 hashes,
chroma-matte commands, and derivation method are recorded in
`assets_src/castle/logo_studio_v2/PROVENANCE.md`. Runtime derivatives were built
deterministically by `tools/build_castle_banner_art.py`; both native keyed
generations and transparent source masters remain preserved.

- `assets_src/castle/logo_studio_v2/castle_personal_banner_keyed.png` - native project-owned ImageGen banner generation on a magenta key field.
- `assets_src/castle/logo_studio_v2/castle_personal_banner_master.png` - transparent source master derived from the preserved keyed banner with the installed chroma-key helper.
- `assets_src/castle/logo_studio_v2/castle_banner_motifs_keyed.png` - native project-owned ImageGen eight-motif generation on a magenta key field.
- `assets_src/castle/logo_studio_v2/castle_banner_motifs_master.png` - transparent source master derived from the preserved keyed motif sheet with the installed chroma-key helper.
- `assets/flats/castle/logo_studio_v2/castle_banner_pink.png` - 256x512 high-key pink cloth derivative of the transparent banner master.
- `assets/flats/castle/logo_studio_v2/castle_banner_gold.png` - 256x512 high-key gold cloth derivative of the transparent banner master.
- `assets/flats/castle/logo_studio_v2/castle_banner_mint.png` - 256x512 high-key mint cloth derivative of the transparent banner master.
- `assets/flats/castle/logo_studio_v2/castle_banner_ocean.png` - 256x512 high-key ocean-blue cloth derivative of the transparent banner master.
- `assets/flats/castle/logo_studio_v2/castle_banner_purple.png` - 256x512 high-key purple cloth derivative of the transparent banner master.
- `assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png` - 256x512 muted-rainbow cloth derivative of the transparent banner master.
- `assets/flats/castle/logo_studio_v2/castle_banner_motif_rainbow.png` - 256x256 transparent rainbow emblem cell from the authored motif master.
- `assets/flats/castle/logo_studio_v2/castle_banner_motif_shell.png` - 256x256 transparent fan-shell emblem cell from the authored motif master.
- `assets/flats/castle/logo_studio_v2/castle_banner_motif_kitty.png` - 256x256 transparent plush-kitty emblem cell from the authored motif master.
- `assets/flats/castle/logo_studio_v2/castle_banner_motif_dog.png` - 256x256 transparent plush-puppy emblem cell from the authored motif master.
- `assets/flats/castle/logo_studio_v2/castle_banner_motif_star.png` - 256x256 transparent star emblem cell from the authored motif master.
- `assets/flats/castle/logo_studio_v2/castle_banner_motif_heart.png` - 256x256 transparent heart emblem cell from the authored motif master.
- `assets/flats/castle/logo_studio_v2/castle_banner_motif_crown.png` - 256x256 transparent pearl-crown emblem cell from the authored motif master.
- `assets/flats/castle/logo_studio_v2/castle_banner_motif_butterfly.png` - 256x256 transparent complete-butterfly emblem cell from the authored motif master.
