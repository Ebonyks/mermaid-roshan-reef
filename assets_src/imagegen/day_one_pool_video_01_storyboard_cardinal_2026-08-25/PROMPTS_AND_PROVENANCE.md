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

## Luna close-up extension — dirty waterfall

The first waterfall frame is retained as rejected continuity evidence only:
v01 lacked a Roshan context anchor, read as a product/detail plate, repeated
leaves, and did not make the canonical pink wrapper or timeline neighbors
clear. The replacement is a fresh complete whole-canvas generation.

| File | Built-in result ID | Subject | Dimensions | SHA-256 | Prompt SHA-256 | Status |
|---|---|---|---:|---|---|---|
| `closeups_rejected/dirty_waterfall_closeup_v01_rejected.png` | `exec-66ce478d-6755-4e05-8bf1-7083118bd2d4` | rejected dirty waterfall close-up | `1672×941` | `2DE869C67548F6A4DE2E31EFBC8145C3B288B8D683C01CB2E7125976D61C916D` | see v01 prompt file | `REJECT_KNOCKOUT` |
| `closeups_accepted/dirty_waterfall_closeup_v02b.png` | `exec-88aae78e-21ad-4636-a9fe-365d117e39b3` | dirty waterfall close-up with Roshan edge anchor | `1672×941` | `9B98443D48373158F1D7CA0F9DE5071B17A5F83BDAC6760BA238463BDFFEFC96` | `5A17152CAFFDFC6F6C52A239C6F9F515F62532BC3C5AA60F85ACC2D0265AEE10` | `AUDIT_PASS_OWNER_PENDING` |

Exact v02b prompt: `prompts/dirty_waterfall_closeup_v02b.txt`. Full audit:
`closeups_accepted/DIRTY_WATERFALL_CLOSEUP_V02_AUDIT.md`. Intended timeline is
`CU-WF 2.00–3.00`; previous neighbor is S01 native hash
`777F44C65B2C76B3DC4595ADD5C6ED6CC44F297E7BF81A48D116FC3027D65223`; intended
next neighbor is the accepted dirty seahorse close-up hash
`C8F6D98C82EC5CAACA1D423168F647460C3D6F1068E2E2184AC337110545630C`.
The v02b candidate is not a runtime asset or final-film frame until owner,
M11, and Grok temporal review pass.

## Luna close-up extension — dirty seahorse

The selected seahorse frame is attempt `3/20`. The original attempt lacked a
Roshan context anchor and wrapped the fixture in excessive vines. A second
fresh attempt added Roshan but retained the long body/tail vine. Both remain
under `closeups_rejected/`; neither is Grok authority.

| File | Built-in result ID | Subject | Dimensions | SHA-256 | Prompt SHA-256 | Status |
|---|---|---|---:|---|---|---|
| `closeups_accepted/dirty_seahorse_closeup_v02.png` | `exec-aa806da1-9c70-4f74-8338-5668cf05a3bc` | sick seahorse with pink wrapper and modest olive weed rooted behind the nozzle lip | `1672×941` | `C8F6D98C82EC5CAACA1D423168F647460C3D6F1068E2E2184AC337110545630C` | `40D8391D0BF2AA45298C5EFA7AB36A2C0429E1DBAFBCE7F630A27E7998D2D616` | `AUDIT_PASS_OWNER_PENDING` |

Exact prompt, reference hashes, rejected-attempt hashes, normalized Roshan/
fixture/mouth geometry, and generation declaration are recorded in
`closeups_accepted/V02_PROMPT_AND_PROVENANCE.md`. Independent review is in
`design/review/day_one_pool_video_01_cardinal_2026-08-25/LUNA_CLOSEUP_CONTINUITY_AUDIT_2026-08-25.md`.

## Close-up delivery normalization and integrated index

The two native frames were each normalized by one whole-canvas Lanczos resize.
No subject-local crop, mask, translation, warp, or relighting was applied.

| Delivery file | Dimensions | SHA-256 |
|---|---:|---|
| `closeups_delivery_1280x720/CU_WF_dirty_waterfall.png` | `1280×720` | `EDD3C80BA353F01BFCD49D69D7D08A4DA0BC9AA6390B70B9D095F0A07DA5448A` |
| `closeups_delivery_1280x720/CU_SH_dirty_seahorse.png` | `1280×720` | `0A58B7D1F66D9DBE7A11F058B6B9638A37E306AB46B6081ED87A9A13ECC68A34` |

`STORYBOARD_CARDINAL_PLUS_CLOSEUPS_CONTACT_SHEET.png` is a deterministic
`1920×540` review-only 4×2 index in locked order S01, CU-WF, CU-SH, S02, S03,
S04, S05, S06. SHA-256:
`615A8AB609F8DCB00346DE07392153499F0C8A6794711CCF947404255C936B16`.
It is never a generation plate or Grok upload reference.
