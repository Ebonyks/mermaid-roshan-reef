# Pearl Castle interaction extraction provenance — 2026-08-01

These are preservation-focused source masters for the few props whose painted
room cutouts could not pass the Roshan-overlap audit. The approved room item
crop was the sole identity authority in every call. Runtime files are smaller,
fixed-pivot derivatives built by `tools/build_castle_interaction_atlases.py`;
these native outputs are never loaded directly by Godot.

Tool: OpenAI built-in ImageGen, followed locally by
`C:/Users/Peter/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py`.
No external art or downloaded reference was used.

## Bathroom sink

Reference: `assets/flats/castle/rooms/room_bubble_bath_item_sink.png`.

Prompt:

> Use case: background-extraction. Asset type: Pearl Castle Godot Sprite3D
> prop rest frame. Image 1 is the edit target and authoritative approved
> design. Isolate only the complete pearl-shell bathroom sink/vanity and gold
> faucet; remove every wall, window, coral, floor, and room shadow. Preserve
> the same viewpoint, shell silhouette, peach pearl basin, teal cabinet, gold
> trim, proportions, painted linework, and colors; do not redesign. Place one
> complete closed/rest fixture, centered and padded, on a perfectly flat solid
> #ff00ff chroma background with no gradient, shadow, glow, scenery, text, or
> watermark. Do not use #ff00ff inside the subject.

- Native chroma: `bathroom_sink_chroma.png`, 1394×1128,
  SHA-256 `e34827adfb6b917e636fb88d73129c5a50dde39549a9a8ac461707da6bf59258`.
- Accepted hard-alpha master: `bathroom_sink_alpha_hard.png`, 1394×1128,
  SHA-256 `8c2378cb073a680afb0d4b4e78f0b8928dcbd56f48e2bf221986a29c639e6eaa`.
- Key command: `--auto-key border --tolerance 32 --edge-contract 1 --force`.
- Rejected matte: `bathroom_sink_alpha.png`; the broad soft matte introduced
  gray despill artifacts in legitimate peach/pink fixture pixels. It is kept
  only as rejection evidence and is never referenced by the runtime builder.
- Review: background and shadow are fully removed. The complete vanity,
  faucet, knobs, shell basin, and cabinet are present. The reconstruction is
  slightly more front-facing and fills previously occluded cabinet detail;
  no topology important to the faucet interaction changed.

## Bathtub

Reference: `assets/flats/castle/rooms/room_bubble_bath_item_bathtub.png`.

Prompt:

> Use case: background-extraction. Asset type: preservation-focused 2D game
> interaction cutout. Image 1 is the edit target and sole identity/style
> reference. Isolate only the complete approved peach-pink scalloped shell
> bathtub, oval basin, gold faucet and controls, turquoise water and bubbles,
> yellow duck, aqua lower band, pearls, and front shell ornament. Remove every
> room, wall, floor, and external shadow pixel. Preserve the same viewpoint,
> proportions, palette, outlines, and storybook rendering. Show the complete
> fixture, centered and uncropped, on a perfectly flat solid #ff00ff field;
> no gradient, texture, scenery, reflection, contact shadow, extra object,
> text, or watermark.

- Native chroma: `bathtub_chroma.png`, 1604×980,
  SHA-256 `120d4bd19e237063b9d010e9759bed7152a64cd359d418206c1e8560cd2d8b62`.
- Accepted hard-alpha master: `bathtub_alpha.png`, 1604×980,
  SHA-256 `4e5752d4bdb7fec8fbd8d0d9100eafb3567f885090d05ed7735f28b76203c3d6`.
- Key command: `--auto-key border --tolerance 75 --edge-contract 1 --force`.
- Review: complete, one fixture, transparent border, no room/floor/shadow.
  Fine faucet, bubbles, pearl trim, and ornament spacing were regularized and
  the proportions became slightly broader. The runtime builder heals the duck
  out of the bathtub source and color-isolates that same duck as its own card,
  preventing a duplicated painted duck.

## Toilet

Reference: `assets/flats/castle/rooms/room_bubble_bath_item_toilet.png`.

Prompt:

> Use case: background-extraction. Asset type: preservation-focused 2D game
> interaction cutout source. Image 1 is the edit target and sole authority for
> identity, design, colors, proportions, ornaments, and viewpoint. Isolate the
> complete whimsical pink pearl/shell toilet on a perfectly flat solid
> #ff00ff field. Preserve the front-left three-quarter view, raised scalloped
> rear lid, pearl-and-gold crown, oval bowl and rim, scalloped gold-trimmed
> front, pearl-cluster base, right plumbing, pastel palette, and storybook
> linework. Remove only wall, window, coral, floor, room context, and external
> shadow. Do not redesign, rotate, mirror, crop, simplify, add scenery, text,
> or watermark.

- Native chroma: `toilet_chroma.png`, 1174×1340,
  SHA-256 `6ef4d4da0797947556363d685bfd8410c2756e9684892e730b72d6ddfd87ed24`.
- Accepted hard-alpha master: `toilet_alpha.png`, 1174×1340,
  SHA-256 `fcdc43d489b0c1c5a81cc02a64cf3150220d70f329fd3d82b75c6fdfa639a64e`.
- Key command: `--auto-key border --tolerance 32 --edge-contract 1 --force`.
- Review: one connected complete fixture, fully transparent border, no room
  pixels. The crown jewel is a little more faceted and hinge/pipe ornament is
  slightly elaborated; viewpoint and interaction topology are preserved.

## Mermaid Pool flower float

References: the approved item crop plus its approved full-room composition.

Prompt:

> Use case: background-extraction. Image 1 is the edit target containing the
> exact approved pink flower float and unwanted cyan pool water; Image 2 is
> context only. Replace only every surrounding water/background pixel with a
> perfectly flat solid #ff00ff field. Preserve the same five rounded petals,
> pearl-yellow center, proportions, orientation, palette, contours, highlights,
> and storybook brushwork. One complete centered float with even padding; no
> water, ripple, reflection, shadow, star, other prop, scenery, text, or
> watermark. Do not redraw, symmetrize, beautify, or add detail.

- Native chroma: `flower_float_chroma.png`, 1202×1309,
  SHA-256 `40137db47f2c4edd7b28b62bae45cc3244be76a71e52a08ef951cd73ebb3f3a2`.
- Accepted hard-alpha master: `flower_float_alpha.png`, 1202×1309,
  SHA-256 `ae0a274a486c2efa5324b895b99e7fe94a762effc8f6ed049eb2532ce7bd06b5`.
- Key command: `--auto-key border --tolerance 64 --edge-contract 2`.
- Review: one connected subject with no water/background. Low drift is limited
  to highlight brushwork and small petal-lobe proportion differences.

## Mermaid Pool bubble fountain

References: the approved item crop plus its approved full-room composition.

Prompt:

> Use case: background-extraction. Image 1 is the edit target containing the
> exact approved tiny bubble fountain and unwanted cyan pool water; Image 2 is
> context only. Replace only the surrounding water/background with a perfectly
> flat solid #ff00ff field. Preserve the small pink/lavender pearl-shell saucer,
> clear aqua center jet, compact four-bubble group, proportions, viewpoint,
> palette, contours, highlights, and storybook brushwork. Keep it compact and
> centered. No surrounding water, waves, reflection, shadow, flower, star,
> pedestal, extra ornament, extra bubbles, scenery, text, or watermark.

- Native chroma: `bubble_fountain_chroma.png`, 1346×1168,
  SHA-256 `8c4e5a3d9dfbd66396a1044f0f97f1168497774e9053e96c5616f6d16cbfe230`.
- Accepted hard-alpha master: `bubble_fountain_alpha.png`, 1346×1168,
  SHA-256 `37020656d12b87c0fac563296b62f905e6a4c2b2debdb5dffb19c477e51eddf9`.
- Key command: `--auto-key border --tolerance 64 --edge-contract 2`.
- Review: one connected subject with no water/background. Exact bubble offsets
  and scallop details required moderate extrapolation from the tiny source;
  rejected ornate variants were not retained.
