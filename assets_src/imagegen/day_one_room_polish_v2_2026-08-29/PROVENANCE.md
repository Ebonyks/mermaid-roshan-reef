# Day One room-polish target provenance

Date: 2026-08-29
Generator: OpenAI Codex built-in ImageGen (`image_gen` tool)
License: project-generated, © Mermaid Roshan LLC, all rights reserved
External source URL: none
Delivery role: transparent room-specific pre-clean targets; no generated image
replaces an approved room plate, character, protected book asset, or voice.

## Reference authority

The local exact-Godot-4.7.2 Mobile screenshots below were supplied only as
storybook palette, outline, value-band, and phone-scale context. They are not
delivery pixels and were not modified.

| Room | Reference | SHA-256 | Role |
|---|---|---|---|
| Bathroom | `audit/day_one_gameplay_2026-08-29/visuals/current_4_7_2/bathroom/00_dirty_basket_prompt.png` | `c79f2a63d8895ce786ad796eefe757ec48c77490730b7459916554c11265680d` | bathroom palette, linework, and scale |
| Pool | `audit/day_one_gameplay_2026-08-29/visuals/current_4_7_2/pool/00_dirty_arrival.png` | `abe2c118bef5ada9341e7274875bae842f0e8b8176a0daa8b9f0e37af2384921` | pool palette, linework, and scale |
| Stuffie | `audit/day_one_gameplay_2026-08-29/visuals/current_4_7_2/stuffie/00_blocked_dirty_playroom.png` | `9b440af7e4dd0f99ab6db3a61394860185c02389888787538c7cdbac087cffa3` | playroom textile palette and scale |
| Art | `audit/day_one_gameplay_2026-08-29/visuals/current_4_7_2/art/00_loose_supplies.png` | `6832af65c90d40f7b2469a49d56145ea3233ea36c81acedaff8e68ca4ac735a4` | studio paint palette, linework, and scale |

## Accepted generation prompts and results

### Bathroom soap splatter

Accepted alpha-correction result:
`exec-46dcfb5e-b349-4033-b0f8-1418c7bddf6f.png`.

> Create one isolated, child-friendly bathroom cleaning target: a silly soap
> and toothpaste splatter made from mint-blue curls, lavender foam bubbles,
> and one soft peach smear. Match the supplied room's polished pastel 2D
> storybook art, broad painted value bands, navy-purple contour, and oversized
> phone-readable shape. No character, face, toilet humor, tool, hand, arrow,
> text, UI, floor, room, border, watermark, or shadow. Return a complete cutout
> on genuine transparency.

### Pool algae tangle

Accepted first result:
`exec-4a5a6a0b-f263-4a8f-b76e-319a235f9b38.png`.

> Create one isolated pool-cleaning target: a chunky algae ribbon tangle with
> two brown leaves, a few teal bubbles, and one small pink shell. Match the
> supplied room's polished pastel 2D storybook art, broad painted value bands,
> navy-purple contour, and oversized phone-readable silhouette. No character,
> seahorse, dust bunny, tool, hand, arrow, text, UI, floor, room, border,
> watermark, or shadow. Return a complete cutout on genuine transparency.

### Stuffie loose stuffing

Accepted alpha-correction result:
`exec-d6f88fab-9c07-480e-bb40-c363b668cd16.png`.

> Create one isolated Stuffie Playroom cleaning target: a soft pile of loose
> cream plush stuffing and lint with lavender dust curls and a few aqua thread
> loops. Match the supplied room's polished pastel 2D storybook art, textile
> softness, broad value bands, navy-purple contour, and oversized phone-readable
> shape. No character, face, animal, dust bunny, toy, tool, hand, arrow, text,
> UI, floor, room, border, watermark, or shadow. Return a complete cutout on
> genuine transparency.

### Art Studio rainbow spill

Accepted alpha-correction result:
`exec-445163f7-a6b9-44f9-b54a-afd7465dadf6f.png`.

> Create one isolated Art Studio cleaning target: a playful rainbow paint
> puddle using coral pink, aqua, lavender, and warm yellow with a few rounded
> droplets. Match the supplied room's polished pastel 2D storybook art, broad
> painted value bands, navy-purple contour, and oversized phone-readable shape.
> No character, face, brush, cleaning tool, hand, arrow, text, UI, floor, room,
> border, watermark, or shadow. Return a complete cutout on genuine transparency.

The initial Bathroom, Stuffie, and Art results painted checkerboard backdrops
and were rejected as delivery art. Their accepted correction used this edit
instruction with the respective rejected result as the sole subject input:

> Isolate the exact subject and remove only the checkerboard/background. Preserve
> the design, colors, contour, scale, placement, and complete silhouette. Return
> real antialiased alpha with no backdrop, glow, halo, shadow, text, or added
> object. Do not redraw or redesign the subject.

## Accepted files and normalization

| Native master | Geometry | Native SHA-256 | Runtime derivative | Geometry | Runtime SHA-256 |
|---|---:|---|---|---:|---|
| `art_rainbow_spill_native.png` | 1536×1024 RGBA | `60194d8a51bb1bd33af82fa3d819e1357de8eee7a7536e8996e8bca2544ac81a` | `assets/castle/day_one_polish_v2/art_rainbow_spill.png` | 1024×614 RGBA | `02bbd05f423f15d7388eb1c2b7de5636de5552c8b7b445bd18943190b9290af3` |
| `bathroom_soap_splatter_native.png` | 1536×1024 RGBA | `b8bdc25164b56b87668627343a1361bf47b29dcf2a9330becde2fd0340f5ad53` | `assets/castle/day_one_polish_v2/bathroom_soap_splatter.png` | 1024×592 RGBA | `9677438df2e809e95ad308dd35c28a4f0687493898493ab9bfa3b93795b3b126` |
| `pool_algae_tangle_native.png` | 1448×1086 RGBA | `c229e0792187c7180c40211bd07de76dc42864b6ac1725654fa69f6a0b9c5a83` | `assets/castle/day_one_polish_v2/pool_algae_tangle.png` | 1024×758 RGBA | `adddd75115d290d99bf7252e789bb6437128f8d2fbdc3b437d5c598fe8f4c37e` |
| `stuffie_loose_stuffing_native.png` | 1536×1024 RGBA | `52f785b3cde51f19ea3a2dc4b40af3d03dba7fd107b852591c07cfc173619972` | `assets/castle/day_one_polish_v2/stuffie_loose_stuffing.png` | 1024×614 RGBA | `2f7c55ac2b660dddea62fc1634312fe6fb7e63bc30fad0b939009688438c9908` |

Runtime normalization used an alpha-threshold crop (alpha below 8 cleared),
then a proportional whole-image Lanczos downscale to a longest edge of 1024.
No subject-local repaint, warp, relight, compositing, or protected-source edit
was performed. The accepted native masters remain unchanged beside this file.

## Review status

- Genuine RGBA transparency: pass by pixel/alpha audit.
- Runtime longest edge at or below 1024: pass.
- True 2D Sprite2D use: pass in exact-engine probes.
- Protected originals changed: none.
- Owner/human art review: pending.
- Lenovo Tab M11 performance acceptance: pending external device test.
