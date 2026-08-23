# Reference upload matrix

## Stable character authorities in this Project

- `ROSHAN_IDENTITY` → `../../characters/roshan/ROSHAN_FRONT_IDENTITY.png`
- `ROSHAN_REAR` → `../../characters/roshan/ROSHAN_REAR_POSE_SHEET.png`
- `RUMI_IDENTITY` → `../../characters/rumi/RUMI_FULL_BODY_IDENTITY.png`
- `RUMI_POSES` → `../../characters/rumi/RUMI_EIGHT_POSE_ATLAS.png`
- `RUMI_RELATIONSHIP` →
  `../../characters/rumi/RUMI_AND_ROSHAN_RELATIONSHIP_SAMPLE.png`

Use `RUMI_RELATIONSHIP` only for relative scale, affection and trust. It does
not override either character's own face, costume or anatomy authority.

## Immutable game-source references

Download these exact files from green commit `71198979`. Preserve filenames and
hashes when adding them to the Grok Project asset library.

| Alias | Authority domain | Immutable URL |
|---|---|---|
| `POOL_CLEAN_FULL` | Sole whole-room geography, recurring architecture, clean palette and fixture placement | [room_mermaid_pool.png](https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/7119897920e14724baaedd9c9dc254a95421027d/assets/flats/castle/rooms/room_mermaid_pool.png) |
| `SEAHORSE_CLEAN` | Seahorse identity, silhouette, pedestal, palette and clean nozzle stream | [mermaid_pool_seahorse_fountain_rest.png](https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/7119897920e14724baaedd9c9dc254a95421027d/assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_seahorse_fountain_rest.png) |
| `WATERFALL_CLEAN` | Rainbow shell-waterfall design and clean flow | [mermaid_pool_waterfall_rest.png](https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/7119897920e14724baaedd9c9dc254a95421027d/assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_waterfall_rest.png) |
| `DIRTY_POOL_CONTENT` | Content-only: surface algae, seaweed, wrapper, cup, leaves and murky bubbles | [pool_algae_trash.png](https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/7119897920e14724baaedd9c9dc254a95421027d/assets/castle/day_one_pool/pool_algae_trash.png) |
| `DIRTY_WATERFALL_CONTENT` | Content-only: hanging growth, leaves and mineral grime | [waterfall_growth.png](https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/7119897920e14724baaedd9c9dc254a95421027d/assets/castle/day_one_pool/waterfall_growth.png) |
| `DIRTY_RIM_CONTENT` | Content-only: slime, scraps, cap, ribbon, sponge and dead seaweed | [pool_rim_grime.png](https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/7119897920e14724baaedd9c9dc254a95421027d/assets/castle/day_one_pool/pool_rim_grime.png) |
| `SEAHORSE_SICK_CONTENT` | Dirty-state content and mouth blockage only; clean reference still controls identity | [seahorse_sick.png](https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/7119897920e14724baaedd9c9dc254a95421027d/assets/castle/day_one_pool/seahorse_sick.png) |

## Authority warnings

- `POOL_CLEAN_FULL` is the first image for every new room composition.
- `SEAHORSE_CLEAN` must precede `SEAHORSE_SICK_CONTENT` whenever the dirty or
  rescued seahorse is generated.
- The four dirty-state images never control gloss, linework, value density,
  lighting or background finish. Restyle their story content into the approved
  matte painted-cel language.
- Do not upload any file from a `rejected/` directory.
- Attach one or two owner-approved base-video style stills to every production
  still/video after those stills exist. They control finish and cadence only.

## Shot reference order

| Shot/anchor | Attach in this order | Purpose |
|---|---|---|
| `A01_DIRTY_ROOM` | `POOL_CLEAN_FULL`, `DIRTY_POOL_CONTENT`, `DIRTY_WATERFALL_CONTENT`, `DIRTY_RIM_CONTENT`, `SEAHORSE_CLEAN`, `SEAHORSE_SICK_CONTENT` | Lock dirty room geography before characters. Six references are justified because each has a distinct domain. |
| `A02_SEAHORSE_RESCUE` | accepted `A01_DIRTY_ROOM`, `SEAHORSE_CLEAN`, `SEAHORSE_SICK_CONTENT`, `ROSHAN_IDENTITY` | Lock the final rescue contact and mouth debris. |
| `A03_CLEAN_REVEAL` | `POOL_CLEAN_FULL`, `SEAHORSE_CLEAN`, `WATERFALL_CLEAN`, `RUMI_IDENTITY`, `ROSHAN_IDENTITY` | Lock final lighting, clean fixtures and character scale. |
| `SH010` | accepted `A01_DIRTY_ROOM`, `ROSHAN_IDENTITY` | Roshan enters and discovers the room. |
| `SH020` | accepted `SH010` ending frame, `ROSHAN_IDENTITY`, `SEAHORSE_CLEAN`, `SEAHORSE_SICK_CONTENT` | Concerned discovery of the clogged seahorse. |
| `SH030` | accepted `SH020` ending frame, `ROSHAN_IDENTITY`, `DIRTY_POOL_CONTENT` | Remove pool-surface pollution. |
| `SH040` | accepted `SH030` ending frame, `ROSHAN_IDENTITY`, `WATERFALL_CLEAN`, `DIRTY_WATERFALL_CONTENT` | Clear waterfall growth. |
| `SH050` | accepted `SH040` ending frame, `ROSHAN_IDENTITY`, `DIRTY_RIM_CONTENT` | Clear pool-rim trash. |
| `SH060` | approved `A02_SEAHORSE_RESCUE` | Extract wrapper and free the seahorse. |
| `SH070` | accepted `SH060` ending frame, `POOL_CLEAN_FULL`, `SEAHORSE_CLEAN`, `WATERFALL_CLEAN` | Light, water and fixture restoration. |
| `SH080` | approved `A03_CLEAN_REVEAL`, `RUMI_IDENTITY`, `RUMI_POSES` | Rumi rises, settles upright and waves. |
| `SH090` | accepted `SH080` ending frame, `RUMI_IDENTITY`, `ROSHAN_IDENTITY`, optional `RUMI_RELATIONSHIP` | Silent dialogue-friendly introduction and Roshan's warm response. |

Keep the normal reference pack to three to five images. `A01_DIRTY_ROOM` is the
only deliberate six-image exception; production shots inherit its accepted
full-frame result rather than reattaching all dirty cutouts.
