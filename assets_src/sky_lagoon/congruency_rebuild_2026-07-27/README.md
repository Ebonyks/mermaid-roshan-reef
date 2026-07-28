# Sky Lagoon congruency rebuild — 2026-07-27

Project-original raster sources generated with the built-in OpenAI image tool.
The approved 3:1 mural, the prior project-owned sprite for each subject, and
the accepted PNW fir were the only visual references. No external art, 3D
model, GLB, procedural mesh, or Blender content was used.

The Claude artifact's seven-criterion contract is implemented by
`tools/audit_scene_congruency.py`; the machine-readable result is
`audit/congruency_sky_lagoon.json`.

## Accepted generation sources

- `../masters/sky_lagoon_panorama_master_v2_3x1.png` —
  `call_SUu0RijBYBIIdI2moduiE050`; native 2172×724 exact-3:1 repaint,
  preserving the water dock, central lawn, PNW planting, castle, Mermaid
  Roshan stained glass, drawbridge, and upper mountain path.
- `sky_lagoon_activity_frame_v3_chroma.png` —
  `call_eByaWahnrDrJXEzAPmfJuGTx`; simplified green/lavender wooden easel.
- `sky_lagoon_castle_gate_v3_chroma.png` —
  `call_DU7p6xC1xEBHJ2bLLHW7fp7H`; straight-on castle-door focus layer.
- `sky_lagoon_slide_v3_chroma.png` —
  `call_GlYXXqbQ7fC1fSxImAACZBLU`; matte slide with a real rung ladder,
  never staircase geometry.
- `sky_lagoon_swing_v3_chroma.png` —
  `call_0Re9V5TWVaQqcfCVCDMldzAt`; two large usable seats and clear ropes.
- `sky_lagoon_plane_v4_chroma.png` —
  `call_NfGSbWT6ZD6N8bVptMQJYdZL`; approved pearl-plane design repainted in
  the plate's cool sage/aqua values.
- `sky_lagoon_seesaw_v4_chroma.png` —
  `call_Cwfh5A5yP2SAyah3lpKhXdDd`; symmetric, mechanically legible,
  green/teal seesaw.
- `sky_lagoon_cloud_family_v5_chroma.png` —
  `call_79f6ey3cV0cdxzRWtkWw2T90`; cool cyan cloud family with a broad
  lavender-blue underside.

## Rejected audit iterations retained as evidence

- `sky_lagoon_plane_v3_chroma.png`: failed C1/C2.
- `sky_lagoon_seesaw_v3_chroma.png`: failed C1/C4.
- `sky_lagoon_cloud_family_v3_chroma.png`: failed C1/C2/C4.
- `sky_lagoon_cloud_family_v4_chroma.png`: failed C1/C2/C4.

All accepted chroma sources were alpha-extracted, trimmed, and downsampled
once with `tools/prepare_sky_lagoon_congruency_assets.py`. The PNW fir and
currant and Mermaid Roshan were derived from their existing project-owned
sprites; only authored density and a non-destructive matte/color grade changed.
Their protected source artwork remains untouched.
