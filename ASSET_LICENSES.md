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
| assets/book/** (incl. hall/) | Mermaid Roshan storybook scans | **Original work © Mermaid Roshan LLC, all rights reserved** | — | cropped/resized for in-game frames |
| assets/characters/friends/* | book character art (family) | **© Mermaid Roshan LLC, all rights reserved** | — | background removal only — SACRED, never restyle |
| assets/characters/roshan.glb, huluu.glb, fairy.glb, lamb.glb | plushie meshes generated from the book art (tools/build_plushie.py) | derivative of © book art — all rights reserved | — | silhouette-extruded, rigged |
| assets/characters/roshan_sprite.png, roshan_tex_2k.webp, lamb_0.png, skins/* | book-art derivatives | © Mermaid Roshan LLC, all rights reserved | — | palette/skin variants |
| assets/audio/voices/daddy1-3.ogg, chuck*.ogg | family recordings (+ Pixabay dog bark, see below) | **© family / Pixabay Content License** | pixabay.com | trim + loudnorm — SACRED |
| assets/audio/voices/voice_yay.mp3 | floraphonic via Pixabay | Pixabay Content License | pixabay.com | none — SACRED |
| assets/audio/voices/* (all other lines) | Kokoro-82M neural TTS (Apache-2.0 model), lines written for this project | synthesized output, owned by project | huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX | pitch/tempo/loudnorm per VOICE_MANIFEST.md |
| assets/audio/voices/chuck_whimper.ogg | original numpy synthesis | project original | — | -16 LUFS |
| assets/audio/music/world, world_night, level2, hall, home (.ogg) | Juhani Junkala JRPG Packs 1/2/4 | **CC0** | opengameart.org/content/jrpg-pack-1-exploration (+pack-2-towns, +pack-4-calm) | -18 LUFS loudnorm |
| assets/audio/music/* (finale + minigame stingers) | synthesized for this project | project original | — | — |
| assets/audio/ambience_*.ogg, ui_tap.ogg | original numpy synthesis | project original (CC0-equivalent) | — | seamless loops |
| assets/audio/buy, buzz, chime, fart (.ogg) | synthesized for this project | project original | — | — |
| assets/aquatic/*.glb | Riley *Aquatic Animal Models* (itch.io) | **"free use, no redistribution"** — see OPEN QUESTION below | itch.io | integrated as-is; Rock2 re-textured with project nano-banana sheets (tools/bake_nano_wrap.py, 2026-07-12) |
| assets/terrain/up_*_rgh.jpg (roughness maps only) | ambientCG | **CC0** | ambientcg.com | resized ≤1K |
| assets/terrain/up_*_col.jpg (all 13 roles) | GEN2 pipeline: family-style painted tiles (Gemini; audit picks; castle re-generated r3 as a proper wall) | © Mermaid Roshan LLC — generated for this project | gen2/generated/terrain_up_*/ | 2048→1024 POT, JPEG q88; matching _nrm.jpg flattened to neutral 64px |
| assets/terrain/caustics.png, scales*, polyp*, flower*, leaf, beachball, star_detail (.png) | painted/generated for this project | project original | — | — |
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
| assets/mg/*.png | drawn/generated for this project (PIL) from book-art motifs | © Mermaid Roshan LLC derivatives / project original | — | craft zone masks, minigame art |
| assets/props/gen2/*.glb | GEN2 pipeline: family-style art (Gemini, audited) → 3D (Meshy image-to-3D) | © Mermaid Roshan LLC — generated for this project | gen2/ (workorder, audit) | tools/shrink_glb.py: textures ≤1024, speculars stripped, shadow lift, albedo posterized to 8 flat PNG fills (WW look) |
| assets/props/gen2/*.png | GEN2 pipeline sprites (Gemini, audited), alpha-cut via tools/polish_sprite.py | © Mermaid Roshan LLC — generated for this project | gen2/ | white bg → alpha, tight crop |
| assets/props/gen2/seagrass.png | GEN2 pipeline: family-style sea grass sprite (Gemini, aquatic_seaweed2 v1, audit 9/10 clean) | © Mermaid Roshan LLC — generated for this project | gen2/generated/aquatic_seaweed2/ | polish_sprite.py alpha cutout, 892×735 |
| assets/props/gen2/starfish_decal.png | derived: top render of assets/props/gen2/starfish.glb (project Gemini+Meshy art) | project-owned | — | flat decal for the seabed scatter field |
| assets/props/gen2/clownfish_side.png | derived: side render of assets/props/gen2/clownfish.glb (project Gemini+Meshy art) | project-owned | — | sprite for the ambient school quads |
| assets/props/gen2/craft_kitty.glb | craft-studio kitty: HER book art (Gemini, doll_cat) → luma-neutralized source → Meshy image-to-3D + texture | © Mermaid Roshan LLC — generated for this project | Downloads/Meshy_AI_Whiskercorn_* | tools/import_craft_creature.py: decimate 309k→9k, textures ≤1024, normal/MR stripped; recolored in-game by the craft sway shader |
| assets/props/gen2/craft_birdie.glb | craft-studio birdie: HER book art (Gemini, baby_eagle) → luma-neutralized source → Meshy image-to-3D + texture | © Mermaid Roshan LLC — generated for this project | Downloads/Meshy_AI_Pufflet_* | tools/import_craft_creature.py: decimate 541k→9k, textures ≤1024, normal/MR stripped; recolored in-game by the craft sway shader |
| assets/props/gen2/craft_kitty_rigged.glb | craft kitty rigged: the kitty mesh on Chuck's 20-bone quadruped rig with idle/walk/run/happy clips | © Mermaid Roshan LLC — generated for this project | Downloads/Meshy_AI_Whiskercorn_* | tools/build_chuck_rig.py (rig) + tools/animate_kitty.py (clips), texture ≤1024, maps stripped; recolored in-game by the sway shader (sway_amount 0) |
| assets/props/gen2/craft_birdie_rigged.glb | craft birdie rigged: its own 12-bone standing-bird skeleton (two-bone legs + wing chains) with idle/walk/run/happy clips | © Mermaid Roshan LLC — generated for this project | Downloads/Meshy_AI_Pufflet_* | tools/rig_birdie.py (rig+clips, penguin-pipeline weights), texture ≤1024, maps stripped; recolored in-game by the sway shader (sway_amount 0) |
| assets/audio/penguin_giggle.ogg | synthesized squeak giggle (numpy, tools history 2026-07-12) | project-owned | — | baby penguin voice: escape burst, catch, portal greet |
| assets/terrain/up_cliffwall_col.jpg | nano-banana generation (gemini-3-pro-image, 2026-07-13, bare-stone regen same day) | project-owned | — | painted cliff-wall tile: terrain steep-slope blend; BARE stone by rule - 3D coral props decorate surfaces |
| assets/terrain/backdrop_seamounts.jpg | nano-banana generation (gemini-3-pro-image, 2026-07-13) | project-owned | — | seamount silhouette panorama: world-edge backdrop ring |
| assets/audio/purr.wav | synthesized cat purr (numpy: 55/110/165 Hz body, 25 Hz AM pulse, seamless 2s loop) | project-owned | — | craft kitty nuzzle loop; WAV not OGG (no vorbis encoder available in build env); loop set in code |
| assets/characters/roshan_v2.glb | ROSHAN V2: owner-spec turnarounds (Gemini) → Meshy multi-image i23d → weight transfer onto her original 26-bone rig | © Mermaid Roshan LLC — generated for this project | gen2/turnarounds/roshan_v2/, gen2/ROSHAN_V2_WORKORDER.md | shrink pass ≤1024, tools/roshan_v2_retarget.py |
| assets/characters/fairy_v2.glb | FAIRY V2: turnarounds (Gemini) → Meshy multi-image i23d → weight transfer onto the 26-bone rig + auto-detected wingL/wingR flap bones | © Mermaid Roshan LLC — generated for this project | gen2/turnarounds/fairy_v2/ | shrink pass ≤1024, tools/roshan_v2_retarget.py (wings mode) |
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
