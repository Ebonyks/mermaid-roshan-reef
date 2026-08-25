# Prompts and provenance — Day One Pool Video 01 cardinal room tour

## Generation method and source roles

All accepted PNGs are project-original complete flattened images generated
with OpenAI built-in ImageGen on 2026-08-25. No CLI/API fallback, crop, mirror,
translated plate, compositing, sprite, rig, tween, optical flow, morph,
cross-dissolve, or procedural warp supplied delivery pixels.

Reference roles:

- `assets/flats/castle/rooms/room_mermaid_pool.png` — canonical north-wall
  materials, fixture order, palette, and storybook style; never a crop plate;
- `assets/castle/day_one_pool/waterfall_clogged_turgid.png` — exact dirty
  waterfall state;
- `assets/castle/day_one_pool/seahorse_sick.png` and
  `activities/seahorse_mouth_trash.png` — exact sick fixture and obstruction;
- `activities/floating_trash_atlas.png` — six debris identities;
- `assets/characters/roshan_25d/roshan_base.png` — approved Roshan identity;
- the accepted four-direction turnaround master — newly authored wall compass,
  spatial/style reference only; no master pixels were copied into shot keys.

## Accepted native manifest

| File | Built-in result ID | Bearing | Dimensions | SHA-256 |
|---|---|---:|---:|---|
| `accepted/C00_room_cardinal_turnaround_master.png` | `exec-005148e4-2c99-49ea-9341-4beef7d4762a` | compass | `1774×887` | `c43e4492b9c64ce6ed7ba5fd60703383e0cea77ef80dd90581bd615c15c694cd` |
| `accepted/S01_N_cardinal_return.png` | `exec-5bf80ac9-36a7-4b44-b771-d74074da9b6a` | `000°` | `1672×941` | `777f44c65b2c76b3dc4595add5c6ed6cc44f297e7bf81a48d116fc3027d65223` |
| `accepted/S02_E_cardinal.png` | `exec-92f3aa3c-9462-410e-8abf-37f3e4a43e22` | `090°` | `1672×941` | `3adfe2a3f34f05ddc4fb170f73d0e93fba40e243b81593ff0ce52a0b6d94e5ea` |
| `accepted/S03_SE_connector.png` | `exec-5b359cf2-fc42-438c-86d8-13565924aae4` | `135°` | `1672×941` | `649c7ef61241268cded70d025b527ac5289df503c4d483c6beb280543e090fbe` |
| `accepted/S04_S_cardinal.png` | `exec-776a4b48-5213-4005-bd18-58f5adff520f` | `180°` | `1672×941` | `ae5c18f2df8d039d40d0eb510b8fb105919f53a55c5b2f7640d2b064a73804a5` |
| `accepted/S05_SW_connector.png` | `exec-bee096a4-61ee-49e1-b3b9-1a667ccdbf61` | `225°` | `1672×941` | `1379c180ecec86fddfa3232ae32eb0af43a95c5e7e7d7062143717268845b756` |
| `accepted/S06_W_cardinal.png` | `exec-c9aa8e6b-18b2-4dde-a839-12faf13088bb` | `270°` | `1672×941` | `06b5578d23441c434446ab26bcd2e24a2e5707b3ff4f1d29d1365ddd419a6804` |

## Delivery hashes

| File | SHA-256 |
|---|---|
| `delivery_1280x720/S01_N_cardinal_return.png` | `b701facb7747f1897f992b9b4e967f47186445261ebadb852cd7a2d317545f62` |
| `delivery_1280x720/S02_E_cardinal.png` | `0a06d5f94e33dd54f3f5d21b6ff7caa65fff2ee44f3ef7a45682165020802e3f` |
| `delivery_1280x720/S03_SE_connector.png` | `309c66106288da794876a8f647b07e9525b76229549d1239ce01d4115a138d66` |
| `delivery_1280x720/S04_S_cardinal.png` | `0b9cf7b392ab8189d51e0faf5743cd260abb0f1de236b79aa03c9369946e8ccb` |
| `delivery_1280x720/S05_SW_connector.png` | `bc8be477c44657c094270b6da4cde46dc56fa247a5710fe920c2db6ac7ba1d69` |
| `delivery_1280x720/S06_W_cardinal.png` | `1e539467299f63eb9daf6e5f33611c67d9d3c09eed70206a3031bb58a5df6405` |
| `STORYBOARD_CARDINAL_CONTACT_SHEET.png` | `7a14af755633e26db83f8b2673188347547c360dcfdd38830505d5275b8ac27d` |

Delivery copies use one whole-canvas `1672×941 → 1280×720` Lanczos resize.
The same transform applies to every pixel; no subject-specific normalization.

## Prompt authority

Every prompt named one physical bearing and required a fresh complete frame.
Shared constraints were:

```text
One complete Mermaid Pool chamber; one oval pool; exact polished flattened
hand-painted 2D children's storybook style. North is the canonical fixture
wall. East is the shell towel/storage wall. South is the deep shell entrance,
curtains, changing niches and promenade. West is the shell step/service wall.
Show coping overlap, wall returns, columns, floor convergence, waterline and
near/far scale. Dirty olive pool only. No crop, pan, mirror, translated plate,
composite, 3D/PBR, theater staging, cleanup, tool, UI, Rumi, reward or text.
```

Per-shot additions locked `000°`, `090°`, `135°`, `180°`, `225°`, and `270°`
headings and the exact wall/connector content recorded in the handoff. Final
repair prompts changed only the failed issue while requiring a fresh complete
painting: remove duplicate orange leaf in East; correct six unique debris and
increase Roshan 12% in South; remove the forbidden handheld object and keep
Roshan's hands empty in Southeast.

## Attempt/rejection register

Eleven shot candidates were generated. Five were rejected:

- `exec-2a46b8ca-78b0-48f9-8221-64aea72be0c8` — East duplicate orange leaf;
- `exec-7e42ddcd-8630-438e-b8df-d74f1b5f8eda` — South duplicate orange leaf
  and marginal Roshan phone size;
- `exec-9c22b82b-f99b-4aa2-9ea4-af38823d3842` — Southeast Roshan too small
  and can/lid overscale;
- `exec-fbce3528-baad-423e-9cf7-3290f3535f2b` — forbidden handheld object;
- `exec-ce9a0d18-d5bb-4b16-9ea1-059c4f6dcb13` — useful lateral architecture
  study but not selected for the locked six-shot clockwise tour.

Discarded variants remain outside the project package, as permitted for
non-delivery ImageGen attempts. No rejected image is Grok authority.

## Human/Luna review

Three independent Luna reviews inspected the actual local PNGs with the
project master/style audits. Final scores are recorded in
`design/review/day_one_pool_video_01_cardinal_2026-08-25/CARDINAL_STORYBOARD_AUDIT.md`.
All six pass `>=4.5/5` with no knockout. M11, child, owner, final-film temporal,
and audio review remain open.
