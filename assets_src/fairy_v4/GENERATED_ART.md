# Fairy Pond V4 readability cues

Generated 2026-07-27 with the built-in OpenAI image-generation tool. These
two flat 2D cues deliberately use opposite shape and color languages so a
non-reader can distinguish guidance from danger without relying on text.

## Helpful flower gate

- Built-in generation id: `call_lXFZPITIxCYEgcTaG5t6xZt5`
- Source: `concepts/helpful_flower_gate_chroma.png`
- Transparent master: `runtime_textures/helpful_flower_gate.png`
- Prompt: a single top-down, thick circular wreath of six broad rounded lotus
  petals with a large empty center; mint, pale aqua, cream, and warm gold with
  a navy storybook outline; flat 2D watercolor/cel sprite; uniform `#ff00ff`
  chroma background including the center; no purple, coral, points, 3D, text,
  shadow, glow, clutter, watermark, or protected reference art.

## Danger thorn halo

- Built-in generation id: `call_PUx6MU6sMXZT5dfmdQ8ADlBZ`
- Source: `concepts/danger_thorn_halo_chroma.png`
- Transparent master: `runtime_textures/danger_thorn_halo.png`
- Prompt: a single top-down, jagged thorn-ring with a large empty center;
  alternating blunt coral thorns and dark plum points with a navy outline;
  flat 2D watercolor/cel sprite; uniform `#00ff00` chroma background including
  the center; no mint, aqua, gold, rounded petals, 3D, text, shadow, glow,
  clutter, watermark, or protected reference art.

## Processing

The installed image-generation chroma helper sampled the flat border, applied
a soft matte and despill, and produced the transparent masters. Run
`python tools/process_fairy_readability_art.py` to crop and normalize the
runtime cards to 1024×1024 RGBA without changing the illustrated subjects.
