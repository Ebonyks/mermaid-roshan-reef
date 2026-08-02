# Fairy Pond V5 single-canvas panorama

Generated 2026-07-27 with the built-in OpenAI image-generation tool. No
protected book art, family voice, or friend asset was used or modified.

## Continuous 4:1 pond

- Built-in generation id: `call_UkfgoypocUXQcQ00A0aueiPM`
- Raw source: `concepts/fairy_pond_panorama_raw.png`
- Runtime texture: `../../assets/fairy/pond_panorama.png`
- References: the three historical V2 pond concepts, used only to preserve the
  established top-down watercolor language.
- Final prompt: one continuous, extremely wide 4:1 orthographic fairy pond;
  pale-aqua dawn at left flows through saturated turquoise/cobalt twilight to
  a deep-indigo and royal-purple moonlit flower clearing at right. Broad
  S-shaped aqua/blue/lavender/violet water bands, curved ripple arcs,
  star-like pollen trails, lily pads, lavender reeds, mint foliage, and smooth
  stones create a dramatic gradient while leaving a calm central flight lane.
  One image and one location only; no seams, borders, panels, tiles, repeated
  landmarks, montage, characters, bugs, gates, UI, text, boss flower, 3D
  rendering, or watermark.

`tools/process_fairy_panorama.py` performs one deterministic resample of this
single generated canvas to the 4096x1024 power-of-two runtime texture. It does
not tile, join, mirror, bridge, crossfade, or synthesize transition strips.

## Independent bank ornaments

- Built-in generation id: `call_oC8Crmf3pCZBweMc2pLEiBVu`
- Chroma source: `concepts/pond_ornaments_chroma.png`
- Transparent masters:
  `runtime_textures/ornament_lily_cluster.png` and
  `runtime_textures/ornament_lavender_reeds.png`
- Runtime Sprite3D cards:
  `../../assets/fairy/sprites/ornament_lily_cluster.png` and
  `../../assets/fairy/sprites/ornament_lavender_reeds.png`
- Reference: the accepted V5 panorama.
- Final prompt: exactly two isolated, straight-down ornaments on one uniform
  `#ff0000` key—left, three rounded mint lily pads with two cream blossoms and
  aqua ripples; right, curved lavender reeds, purple flowers, mint leaves, and
  one smooth blue stone. Matching watercolor texture, navy/lavender outline,
  generous separation, no shadows, labels, characters, hazards, extra
  clusters, perspective, 3D rendering, or watermark.

The red key is absent from the subjects. The processor splits the two halves,
removes only connected red-dominant key colors, and centers each result on a
1024x1024 transparent card.
