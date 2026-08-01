# Pearl Castle room-button image-generation record

Generated with the built-in Codex ImageGen tool on 2026-08-01. The selected
full-resolution masters are preserved in this directory; runtime thumbnails are
non-destructive center-crop/resample derivatives built by
`tools/build_castle_room_button_thumbnails.py`.

The Library reference is the user-supplied, project-owned cover copied unchanged
to `references/mermaid_roshan_wisconsonia_cover_reference.jpg` (SHA-256
`3ABEDC5EC0D878CFD7A0E1ABAB18B5C8D61E06275D87ABD29252FEF25CE24CD6`).
The protected cover itself was not edited or recompressed.

## Selected master hashes

| Room | Master | SHA-256 |
|---|---|---|
| Main Hall | `castle_button_main_hall_master.png` | `C6A175FBC340F08F054D300E4611C569642012810B32DBDF8D9629A2390961FB` |
| Opera Hall | `castle_button_opera_house_master.png` | `E2ED9D39093559F527E26D576D2C42DF4E6DCCCA35B4EC3825ECB8141E9FD90A` |
| Royal Kitchen | `castle_button_kitchen_master.png` | `CDB85AAC8742261EB19DB87C7E841C47558CA01FF66632929FEF0051948F2CE6` |
| Royal Library | `castle_button_library_master.png` | `CD12676514C9CF51D4317DE4E7A7040F85EA8B40801BF97061CEEA62DDA8A674` |
| Stuffie Playroom | `castle_button_playroom_master.png` | `819652ABCE28DBF45E493F034EE7058BA5BDF799A0B666ADC5399E76BBC6E41A` |
| Craft Room | `castle_button_craft_room_master.png` | `48B4657F37BFA0C9458ED3804040A5B786C93EE68D6F0E02DBF9651845D1A2FD` |
| Mermaid Pool | `castle_button_mermaid_pool_master.png` | `0E90D41D68FE208D47567DFA6511AFD417B2B803AEF09A880C3255A2323FD25F` |
| Bubble Bath | `castle_button_bubble_bath_master.png` | `3827EFC32B7AF36AEFD27255A3CF94449E500F49FAAE90837714D38383541FBC` |

## Shared room prompt

Mode: `stylized-concept`.

> Create full-bleed, picture-first room-selection art for a non-reading
> four-year-old. Faithfully preserve the room's authored architecture and
> palette, simplify secondary detail, and enlarge one authentic hero prop so
> the purpose reads immediately. Polished 2D storybook illustration, landscape
> 5:3, hero occupies about 45 percent of the composition. No characters, text,
> labels, UI chrome, white margins, or invented furniture.

Room-specific hero focus:

- Main Hall: the existing rainbow-shell throne and recognizable portal doors,
  with lavender columns and red carpet.
- Royal Kitchen: the cream shell oven/fire, gold kettle and pot, teal cabinetry,
  refrigerator, and purple arches.
- Stuffie Playroom: the shell stuffie nook and pastel plush friends, retaining
  the authored hall and toy context. This does not rebuild the Stuffie anchor.
- Craft Room: the low paint table with paper, brushes and jars, ribbon wall, and
  idea board.
- Mermaid Pool: the rainbow shell waterfall, pool, ocean window, steps, floats,
  and fountains.
- Bubble Bath: the pearl tub with aqua bubbles and yellow duck, plus the authored
  sink, mirror, toilet, windows, and towels.

## Replacement Opera Hall prompt

Mode: `precise-object-edit`.

> Preserve the approved replacement Opera House composition, architecture,
> salmon/burgundy/teal/gold palette, three lobby floors, twin staircases,
> colored act doors, shell chandeliers, and dominant closed burgundy-curtain
> stage. Remove the baked navy/gold rounded border and all white exterior
> margin. Extend the same Opera House room artwork naturally to every canvas
> edge as a full-bleed landscape illustration. Landscape 5:3, safe for a slight
> 25:14 mobile crop. No elements from the removed purple auditorium, ocean
> scenic backdrop, text, label, UI chrome, watermark, or characters.

References: the approved replacement Opera concept and
`assets_src/concepts/opera_house_flat/opera_house_master_scene_key_2026-07-21.png`
plus `opera_house_stage_scene_key_2026-07-21.png`.

## Final Library icon prompt

Mode: `precise-object-edit`.

> Simplify only the printed artwork on the large upright magical book so it
> reads instantly as a small picture icon. Keep the approved shell-library
> room, book shape, pearl pedestal, framing, palette, and lighting unchanged.
> Remove all title and author lettering from this tiny thumbnail version.
> Enlarge Roshan to occupy nearly the entire front cover, including the former
> title area. Her smiling face, small crown, brown hair with one broad rainbow
> sweep, purple top, and large iridescent rainbow mermaid tail form one bold
> central silhouette. Place her head high on the cover and sweep her tail
> diagonally through the lower half. Keep a simple snowy blue-white Wisconsin
> lake-and-rock background. Retain only large supporting cues: the black dog,
> colorful bird, and pink flower friend. Omit the cake, watering can, backpack,
> loose gems, small snowflakes, and every other tiny detail. Use broad clean
> shapes, strong navy outlines, high contrast, and minimal internal detail.
> The book remains nearly front-facing and fills the central pearl pedestal;
> Roshan must remain unmistakable when the full room is reduced to 200 by 112
> pixels. No text anywhere, no character standing in the room, and no UI frame,
> border, white margin, label, watermark, or invented furniture.

References: the prior approved Library composition and the unchanged
authoritative `mermaid_roshan_wisconsonia_cover_reference.jpg`.
