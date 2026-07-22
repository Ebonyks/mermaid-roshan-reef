# Ocean Kingdoms 2D-to-3D Handoff

Status: **reference-only**. These four high-resolution sheets are inputs for
Claude's 3D reconstruction lane. They are not runtime textures, are not evidence
of an accepted 3D asset, and must not be copied into `assets/` unchanged.

| Sheet | Resolution | Intended 3D families |
|---|---:|---|
| `caribbean_environment_kit_reference.png` | 1536x1024 | shell/sun gate, Caribbean coral, sponge, seagrass, limestone, wayfinder |
| `norwegian_environment_kit_reference.png` | 1536x1024 | whale/current gate, kelp, basalt, ice/current fins, cold benthos, wayfinder |
| `caribbean_fauna_reference.png` | 1536x1024 | blue tang, sergeant major, royal gramma, parrotfish, angelfish, nurse shark |
| `norwegian_fauna_reference.png` | 1536x1024 | cod, herring, mackerel, salmon, harbor seal, orca |

`rejected/caribbean_fauna_reference_v1.png` is retained for honest provenance
only. It depicted the blue tang with an Indo-Pacific regal-tang pattern and is
not approved for modeling or runtime use. The accepted Caribbean sheet replaces
that row with an adult Atlantic blue tang.

## Claude reconstruction contract

- Build one modular family at a time. Do not auto-convert the full sheet into a
  single mesh.
- Treat every view as design guidance, not exact engineering projection. Resolve
  small view-to-view inconsistencies conservatively and preserve the strongest
  child-readable silhouette.
- Use original low-poly geometry and hand-painted Mobile-safe materials. Do not
  embed these reference sheets as model textures.
- Give every prop a grounded support surface and every creature a complete
  silhouette from gameplay camera distance.
- Keep fins, kelp blades, coral fingers, and ice edges thick enough for the
  Speedy-tier device. Avoid alpha cards and transparent overdraw.
- Do not add OmniLights, copyrighted symbols, generic tropical scatter to the
  Norwegian kit, or penguins to the Norwegian ecosystem.
- Export each candidate as an isolated GLB with an editable source, license row,
  runtime destination, triangle/material measurements, and a render from at
  least front, side, back, and representative gameplay distance.
- Quarantine candidates until exported-GLB inspection and the project's known-bad
  negative control prove the QA path is working. No sheet or isolated render can
  establish a 4/5 score.

The exact built-in image-generation prompts are retained in `PROMPTS.md`.
