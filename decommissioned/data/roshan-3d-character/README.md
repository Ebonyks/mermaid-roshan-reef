# Retired 3D Mermaid Roshan package

Archived 2026-08-09 by direct owner instruction. Mermaid Roshan is a 2D
character and the game must not expose, import, instantiate, or ship a 3D
Roshan model.

This directory preserves the two formerly runtime-eligible GLB revisions,
their authored base-colour textures, the importer-extracted texture files that
were present in the working project, and both ignored Meshy source bundles.
The active game uses the approved `assets/characters/roshan_25d/` sprite
atlases instead.

Source paths before retirement:

- `assets/characters/roshan_v3.glb`
- `assets/characters/roshan_v3_Baked_BaseColor.jpg`
- `assets/characters/roshan_v4.glb`
- `assets/characters/roshan_v4_Baked_BaseColor.jpg`
- importer-extracted `roshan_v4_Image_0.jpg` and `roshan_v4_Image_1.jpg`
- `gen2/meshy/roshan_playable/` (raw rejected model bundle)
- `gen2/meshy/roshan_v2/` (raw superseded model bundle)
- `retired-pipeline/` (orphan runtime, broken rig probes, 3D-only build/audit
  tools, and the generated pose-stress review renders)

The `.import` files are evidence only. The parent `decommissioned/.gdignore`
keeps every file here outside Godot's resource index and all APK exports.

Do not restore these files to `assets/`, add a Roshan GLB load path, or revive
the skeleton/rig probes. A future reversal requires a new explicit owner
decision and a new art/playability audit.
