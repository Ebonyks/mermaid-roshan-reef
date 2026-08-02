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
| assets/characters/roshan.glb, huluu.glb, lamb.glb | plushie meshes generated from the book art (tools/build_plushie.py) | derivative of © book art — all rights reserved | — | silhouette-extruded, rigged |
| assets/characters/roshan_sprite.png, roshan_tex_2k.webp, lamb_0.png, skins/* | book-art derivatives | © Mermaid Roshan LLC, all rights reserved | — | palette/skin variants |
| assets/audio/voices/daddy1-3.ogg, chuck*.ogg | family recordings (+ Pixabay dog bark, see below) | **© family / Pixabay Content License** | pixabay.com | trim + loudnorm — SACRED |
| assets/audio/voices/voice_yay.mp3 | floraphonic via Pixabay | Pixabay Content License | pixabay.com | none — SACRED |
| assets/audio/voices/* (all other lines) | Kokoro-82M neural TTS (Apache-2.0 model), lines written for this project | synthesized output, owned by project | huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX | pitch/tempo/loudnorm per VOICE_MANIFEST.md |
| assets/audio/voices/chuck_whimper.ogg | original numpy synthesis | project original | — | -16 LUFS |
| assets/audio/music/world, world_night, level2, hall, home (.ogg) | Juhani Junkala JRPG Packs 1/2/4 | **CC0** | opengameart.org/content/jrpg-pack-1-exploration (+pack-2-towns, +pack-4-calm) | -18 LUFS loudnorm |
| assets/audio/music/* (finale + minigame stingers) | synthesized for this project | project original | — | — |
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
| assets/props/gen2/craft_kitty_mask.png, craft_birdie_mask.png | paint-zone masks baked from the rigged meshes (tools/bake_zone_mask.py) | project-owned | — | R/G/B = body/accent/third paint zones matching the book-art coloration; black = fixed features (horn, feet, beak) |
| assets/audio/penguin_giggle.ogg | synthesized squeak giggle (numpy, tools history 2026-07-12) | project-owned | — | baby penguin voice: escape burst, catch, portal greet |
| assets/terrain/up_cliffwall_col.jpg | nano-banana generation (gemini-3-pro-image, 2026-07-13, bare-stone regen same day) | project-owned | — | painted cliff-wall tile: terrain steep-slope blend; BARE stone by rule - 3D coral props decorate surfaces |
| assets/terrain/backdrop_seamounts.jpg | nano-banana generation (gemini-3-pro-image, 2026-07-13) | project-owned | — | seamount silhouette panorama: world-edge backdrop ring |
| assets/audio/purr.wav | synthesized cat purr (numpy: 55/110/165 Hz body, 25 Hz AM pulse, seamless 2s loop) | project-owned | — | craft kitty nuzzle loop; WAV not OGG (no vorbis encoder available in build env); loop set in code |
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
- `assets/sprites/sky_lagoon/roshan_playground/roshan_swing_2.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon swing references; forward-pump seated pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_swing_3.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon swing references; high-arc seated pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_slide_0.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon slide references; compressed ladder-step pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_slide_1.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon slide references; extended ladder-step pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_slide_2.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon slide references; seated-at-lip pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_slide_3.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon slide references; seated chute-ride pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_0.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon seesaw references; low-seat two-hand pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_1.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon seesaw references; rising two-hand pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_2.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon seesaw references; high-seat two-hand pose; local chroma extraction and 512px crop.
- `assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_3.png` — project-original OpenAI image generation derived from the project Mermaid Roshan and Sky Lagoon seesaw references; descending two-hand pose; local chroma extraction and 512px crop.
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
- `assets/flats/castle/rooms/room_mermaid_pool.png` — original OpenAI ImageGen artwork generated for Mermaid Roshan: Reef of Light; prompt-authored Pearl Castle mermaid pool; resized to 1024×576 for mobile runtime use.
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
  seven project-original 2048 x 1152 preservation masters derived from the
  already licensed 1024 x 576 clean room plates with Pillow Lanczos under the
  owner's explicit authorization to upscale for this pass. Originals and
  aspect ratios are preserved; no external source or new object design.
- `assets/flats/castle/rooms/background_tiles/room_*_background_r*_c*.png`
  — 28 non-overlapping 1024 x 576 runtime crops of the seven masters above,
  produced by `tools/build_castle_room_2k_tiles.py`. Every four-card group
  reconstructs its master pixel-exactly; no scaling occurs during slicing.
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
  used as the real-depth A/B architectural divider.
- `assets/flats/castle/main_hall_2screen/castle_join_floor_inlay_reuse.png`
  — 48 x 321 tapered inlay assembled deterministically by rotating and tiling
  the accepted Screen A carpet trim; no new painting or external source.
- `assets/flats/castle/main_hall_2screen/tiles/main_hall_room_led_*.png`
  — updated lossless runtime crops of the documented derived Main Hall
  masters. Source rectangles and hashes are in
  `audit/castle_sprite3d/castle_main_hall_2x4_runtime_manifest.json`.
- `assets/flats/castle/main_hall_2screen/tiles/runtime_bleed/main_hall_room_led_r0_c*_bleed.png`
  — deterministic render-only derivatives of the four accepted top-row
  tiles, made by `tools/build_castle_hall_runtime_bleed.py`. Each 836 x 471
  file preserves its 836 x 470 source body pixel-exactly and appends the first
  approved pixel row of the corresponding lower tile. This creates a
  one-pixel Mobile-raster safety overlap without scaling, interpolation,
  content loss, generated art, or any modification to the accepted source
  tiles. Exact source/derived hashes and row-equality proofs are recorded in
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
  and `tiles/runtime_bleed/main_hall_room_led_r0_c{2,3}_bleed.png` ?
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
<<<<<<< HEAD
- `assets/audio/sfx/combat_*.wav` (combat_pop, combat_bonk, combat_poof,
  combat_freeze, combat_charge_ring, combat_fizzle) — synthesized entirely
  by `tools/gen_combat_sfx.py` in this repository (deterministic
  pure-stdlib waveforms, seeded noise, no external sources, no recordings).
  The combat feel-stack reaction voices: hit pop, harm bonk, death poof,
  freeze tinkle, charge-ring shimmer, kind-miss fizzle. Owner-recorded
  replacements can drop in at the same paths (all callers check
  ResourceLoader.exists). License: project code.
=======

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
