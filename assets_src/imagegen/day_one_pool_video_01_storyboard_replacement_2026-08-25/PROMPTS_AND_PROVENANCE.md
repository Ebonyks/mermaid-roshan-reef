# Day One Mermaid Pool Video 01 replacement storyboard — prompts and provenance

Generated 2026-08-25 with the built-in OpenAI image-generation tool after the
owner rejected the first storyboard's theater-flat camera grammar and style
drift. Every attempt was one independent, new, complete flattened full-frame
generation. No delivery candidate was composited, cropped from a scene plate,
translated, mirrored, tweened, morphed, interpolated, cross-dissolved, rigged,
warped, or assembled from cutouts. No position guide was used.

The six files under `accepted/` are independently accepted storyboard keys,
not final
cinematic delivery frames. Their native `1672x941` raster ratio is
`1672 / 941 = 1.7768331562`, a near-16:9 ImageGen output. Native bytes are
preserved. Exact 1280x720 whole-canvas normalization was made only after the
independent visual gate passed.

## Generation method

- Tool: built-in OpenAI `image_gen`, one call per attempt.
- Method: `fresh_full_frame_generation`.
- Result type: complete flattened PNG.
- Position guide: none.
- Protected originals: reference-only, never modified or overwritten.
- Appearance edits after generation: none.
- Declared action: all six are observation/inspection keys; no cleanup action,
  magic, Rumi reveal, basket, or tool.

## Approved source authority

| Role | Path | SHA-256 |
|---|---|---|
| Canonical room | `assets/flats/castle/rooms/room_mermaid_pool.png` | `1a9a2005d4d27bd57848130c5d7b402b71d8004d4eb803fa16e1493f6a6a222d` |
| Exact sick V4 seahorse | `assets/castle/day_one_pool/activities/seahorse_sick_clear_mouth.png` | `88aa2ce07e79144b13d8e699341404e7b15e79baed861169c9c17e196ddba941` |
| Exact mouth plug | `assets/castle/day_one_pool/activities/seahorse_mouth_trash.png` | `9c48ac1ca7be923fcb14902b3e2b62263f34d53e031f11002776bfc4322652f9` |
| Exact clogged waterfall | `assets/castle/day_one_pool/activities/waterfall_clogged_original_match.png` | `d4da588daece3fa12b5f094b50f5c8b33eeae31fd0761f1eeedce882cf1b7507` |
| Six debris identities | `assets/castle/day_one_pool/activities/floating_trash_atlas.png` | `e554c4f253bcaa9e5893d9e4fffe03feef96528211f2458dc5d8fc81299f56df` |
| Roshan identity | `assets/characters/roshan_25d/roshan_base.png` | `69827625a8a795f1303c90a465454dd8529f10d5401c78911d00b90be8d1e1ab` |

Protected book art was used only by the Luna authority analysis for identity,
line, and palette rules. No protected book pixel was uploaded into these six
final ImageGen calls or copied into their output.

## Accepted candidate ledger

Prompt hashes are SHA-256 of the verbatim UTF-8 prompt transcript files with
LF line endings. The adjacent rejected full frame supplied to a correction
call was continuity/layout evidence only; it contributed no delivery pixels.

| Shot | Attempt | Built-in result | Native candidate / SHA-256 | Prompt / SHA-256 | Exact uploaded references |
|---|---:|---|---|---|---|
| S01 | 4 | `exec-756efd4d-4fb6-4470-85fe-0f96db770ad1.png` | `accepted/S01_south_entry_attempt04.png` / `2af2dea67bc605f1fb186c5cb1e5740c1a5568128ea4ca43e8bb573bc00dc416` | `prompts/S01_attempt04.txt` / `777b2b24c611d91af6663303416aa547f5e2a06251ea0c9c81bd87e2af13b36e` | rejected S01 a03 + sick seahorse + mouth plug + clogged waterfall + Roshan |
| S02 | 3 | `exec-05f57b0b-1ebf-45ee-a31a-8a20ab259323.png` | `accepted/S02_west_stair_attempt03.png` / `6f49208c17b4e725d519176451932708013eeeaf2c4b424e39ad03c7c23871bc` | `prompts/S02_attempt03.txt` / `b3d23738f0057ccafc3561df45c3e87ae4d03f4b17f596939afea7e301ee04c7` | rejected S02 a02 + canonical room + clogged waterfall + trash atlas + Roshan |
| S03 | 3 | `exec-d66cd1c7-68da-4b9a-ab0c-e854c6af7484.png` | `accepted/S03_northwest_high_attempt03.png` / `073afb4773922bc8a273447a723cf65579106c63cc4bcfff450eb8bebbafeda7` | `prompts/S03_attempt03.txt` / `ef10394afb6ef2bf7eb74be4cdbfc061d57be4661bfb539172eff5231b11c669` | rejected S03 a02 + canonical room + clogged waterfall + trash atlas + Roshan |
| S04 | 6 | `exec-92b72ea2-7765-4a4a-93c9-7ba5ca8969ea.png` | `accepted/S04_east_reverse_attempt06.png` / `4f0a20ec7a0cfd6e938247f60f229c6bffaf08cefbc88a6aac303b73097afe3c` | `prompts/S04_attempt06.txt` / `f6b59107273769de27a0cd8f860232d7c3632ca5fbb81528b061b6ba317d220b` | rejected S04 a05 + canonical room + trash atlas + clogged waterfall + Roshan |
| S05 | 4 | `exec-d2d94d95-4127-440a-a4a6-d46df0f75552.png` | `accepted/S05_waterline_attempt04.png` / `ef22b36625677b22a6a01c9379d2b0873ede2286068dccf738f7e7e58c620132` | `prompts/S05_attempt04.txt` / `fe1abbda1c4b4cea25d959c2d1c8df54802c83d0dcfc359e78fa9919c9109c24` | rejected S05 a03 + sick seahorse + mouth plug + Roshan + canonical room |
| S06 | 4 | `exec-7339cd23-71e6-40dc-9862-640dc9314215.png` | `accepted/S06_southeast_return_attempt04.png` / `46b4045369a6218764e053c00d4d793c06d4853245e54d913fb8843389162cf1` | `prompts/S06_attempt04.txt` / `0a0744a0c17c9ef2e35f68881e5c5707d9da61f34a8564b13ba6794853df967b` | rejected S06 a03 + canonical room + sick seahorse + mouth plug + clogged waterfall |

## Neighbor continuity and declared holds

| Shot | Time | Camera / declared state | Previous candidate | Next candidate |
|---|---:|---|---|---|
| S01 | `0.00-2.20` | South threshold, north-facing wide; arrival/notice settle | none | S02 / `6f49208c...71bc` |
| S02 | `2.20-4.35` | Low west stair, east-southeast; T1/T2 inspection | S01 / `2af2dea6...c416` | S03 / `073afb47...eda7` |
| S03 | `4.35-6.45` | High northwest ledge, southeast; trash-depth explanation | S02 / `6f49208c...71bc` | S04 / `4f0a20ec...fe3c` |
| S04 | `6.45-8.55` | East-side reverse; T4/T5/T6 inspection | S03 / `073afb47...eda7` | S05 / `ef22b366...0132` |
| S05 | `8.55-11.20` | Waterline northwest; mouth-obstruction recognition | S04 / `4f0a20ec...fe3c` | S06 / `46b40453...62cf1` |
| S06 | `11.20-13.40` | Elevated southeast return; problem-map settle | S05 / `ef22b366...0132` | none |

These are storyboard holds only. They do not authorize duplicating a frame to
hide motion in Grok's eventual film. Every changed delivery frame remains
subject to the full-frame cinematic rule.

## Human geometry / identity / topology pre-review

Normalized boxes are visual estimates, not masks or generation guides.

| Shot | Roshan bbox `(x,y,w,h)` | Active subject / fixture notes | Sol pre-review |
|---|---|---|---|
| S01 | `(0.04,0.46,0.22,0.47)` | full debris field; waterfall ~`(0.37,0.26)`; seahorse ~`(0.72,0.31)` | Exact blue-purple fixture family, six trash IDs, opaque Roshan, dirty pool; mouth plug visible; no flow. |
| S02 | `(0.02,0.22,0.35,0.43)` | T1/T2/T3 ~`(0.38,0.67,0.52,0.14)`; seahorse intentionally offscreen | Face and hand readable; low stair/water contact; no invented doorway. |
| S03 | `(0.02,0.39,0.31,0.54)` | T1/T2/T3 diagonal ~`(0.44,0.57,0.34,0.20)`; seahorse intentionally offscreen | Genuine high oblique; face/pointing hand readable; opaque one-tail topology. |
| S04 | `(0.05,0.21,0.28,0.40)` | T4/T5/T6 ~`(0.21,0.59,0.43,0.19)`; seahorse intentionally offscreen behind east camera | Trash hierarchy leads; true east-side crop; face/pointing hand readable; no duplicate fixture. |
| S05 | `(0.22,0.20,0.25,0.63)` | seahorse/nozzle ~`(0.67,0.22,0.16,0.30)`; plug ~`(0.71,0.29,0.05,0.07)` | Roshan opaque; complete fixture receded to room scale; high-contrast plug remains visible; no contact/rescue. |
| S06 | `(0.72,0.44,0.19,0.49)` | full debris field; seahorse ~`(0.60,0.11,0.13,0.32)` | Central window restored; six trash IDs once; southeast column/coping establish moved camera. |

Across the six accepted storyboard keys: Roshan has one head, two arms when both
are visible, and one continuous mermaid tail; the sick seahorse remains the
blue/turquoise, lavender-faced V4 family; the waterfall and seahorse emit no
water; the separate bright-pink wrapper plus olive seaweed is present whenever
the nozzle is in frame. Rumi, basket, skimmer, UI, text, and cleanup reward are
absent. Independent Luna scores are S01 `4.69`, S02 `4.69`, S03 `4.56`,
S04 `4.60`, S05 `4.56`, and S06 `4.52`; every key clears the `4.5` floor
without a knockout. Owner/device acceptance remains pending, and no agent has
assigned a 5/5.

## Whole-canvas 1280x720 normalization

After the six native keys passed the independent gate, FFmpeg 8.1.2 applied
one complete-canvas Lanczos scale to each file:

```text
ffmpeg -i <accepted-native> -vf scale=1280:720:flags=lanczos -frames:v 1 <delivery-copy>
```

No crop, mask, alpha repair, subject isolation, translation, compositing, or
appearance edit occurred.

| Delivery copy | SHA-256 |
|---|---|
| `delivery_1280x720/S01_south_entry_attempt04.png` | `a3ae76def8ea601a7e484a1aa1b634a02fb742a792fe330c15f305cd667d9104` |
| `delivery_1280x720/S02_west_stair_attempt03.png` | `5f2b7fca6753f9168ec95d53c17bdc127d9c1a464809c15e4f088f6fd4f3046a` |
| `delivery_1280x720/S03_northwest_high_attempt03.png` | `a8f4f7c48bef7c8d269621cc0b2404e498df9acc4e780ce5d47d6d4a582f77d1` |
| `delivery_1280x720/S04_east_reverse_attempt06.png` | `f7090219c0a7a5355d81af39f7b9d78405fc41392639e199fd14989f4da5619c` |
| `delivery_1280x720/S05_waterline_attempt04.png` | `e5346eeadd479b095955dd8072962147d8d281b74bf5aaf403dfa981b75cf8f7` |
| `delivery_1280x720/S06_southeast_return_attempt04.png` | `0e514bbe7d6ee8edeffffb9e4c5d124e4f86c67cae798b1cc46019ad5380a317` |

`STORYBOARD_CONTACT_SHEET.png` is a deterministic review-only 3x2 arrangement
of those exact six 1280x720 copies, with whole-frame downscaling to 640x360
and `xstack` placement only. SHA-256:
`148a14048973e91df37f9a5c7ca5d9536a763bf2fd9ba53f108838428b597430`.

The repository lighting-image diagnostic scanned all six accepted natives:
0 unreadable, 0% crushed, 0% blown. Its report is
`design/review/day_one_pool_video_01_2026-08-25/REPLACEMENT_LIGHTING_AUDIT.md`.
`tools/audit_cinematic.py` requires a rendered video plus per-frame tracks and
therefore remains a downstream Grok-delivery gate; a storyboard contact sheet
cannot truthfully satisfy it.

## Rejected attempt ledger

All rejected natives are preserved under `rejected/`. Their exact full prompt
text is not reconstructed here; those candidates remain ineligible and are
never continuity references except where the later accepted prompt explicitly
declares one as layout-only. This omission cannot elevate a reject's status.

| Shot/attempt | Built-in result | Rejected native / SHA-256 | Reason |
|---|---|---|---|
| S01 a01 | `exec-8b5f5984-a27b-4f4b-99fe-0ea5210cf306.png` | `S01_attempt01_illegal_stream.png` / `2d5010c78acd3d1c3db3c0bb3752da25f18ce1898a5c184dceab43c57f3db39c` | Wrong cream/horned fixture and illegal clear seahorse stream. |
| S01 a02 | `exec-6fefc4b7-dd8f-4871-aae7-9c82655b1a16.png` | `S01_attempt02_wrong_fixture.png` / `372a2fe5884b32ae919ad75078011ea2b60ed1db8c89c58018248476f7a1fe15` | Wrong cream/horned fixture. |
| S01 a03 | `exec-de567b69-3c37-470c-ad27-05dced13b67f.png` | `S01_attempt03_bright_water.png` / `4fac330497a3a7d2b66301119ef71574552c2874631291ea69ec3fe5e7e32a7e` | Exact fixture restored, but pool remained too clean/turquoise. |
| S02 a01 | `exec-89661419-93d3-4633-99bb-d8b7e27cd0d4.png` | `S02_attempt01_wrong_fixture_arch.png` / `d2a3bc5217d1f07418327510e631d1c0fa18ee9d1d54c132597e025b5acdf51f` | Wrong fixture plus invented doorway. |
| S02 a02 | `exec-001e324c-c710-4b58-bd8a-5674e0fdd7af.png` | `S02_attempt02_clean_water.png` / `d50bd44d4c635cec47bf32438d10cb118690ea13249faa8a28a2469527de9d13` | Pristine cyan pool violated dirty opening. |
| S03 a01 | `exec-96bfdfed-0d56-4031-af9a-a445463f6762.png` | `S03_attempt01_wrong_fixture_arch.png` / `85fd984311e341a72b4c8e28545aa47c62f42d702f89b64fad66edfd13c5d55e` | Wrong fixture and invented right doorway. |
| S03 a02 | `exec-012192ae-265b-4668-b90c-b95c3b29a1b6.png` | `S03_attempt02_unreadable_face.png` / `d4b3439c485aee0183bd1111186e99f0789780555c0b55d07fbb22043d550a3d` | Back-facing Roshan failed phone acting/readability. |
| S04 a01 | `exec-55d2cf60-2989-4441-bf1d-805d9df25479.png` | `S04_attempt01_giant_wrong_fixture.png` / `4466ab5882b7e73cd4abb541fd43aef4e0a2f6eabab406e5aad91927dfce80e6` | Giant cream/horned theater-statue fixture. |
| S04 a02 | `exec-bcd3c3ae-4f49-4270-bc83-9a3eb93334ff.png` | `S04_attempt02_clean_water.png` / `f08b5d0b2f02f5e12c2769c233ff784b400c6038948e61fa0787d575885e5eb7` | Clean cyan pool and weak mouth seaweed. |
| S04 a03 | `exec-41a9e2ec-47c4-42d5-ae19-78491510e9e2.png` | `S04_attempt03_frontal_repeat.png` / `db7c08bcc2ecb7db3b40c4d69cf563287f20e940e62dba5c0a01e930e8b38c7d` | Camera collapsed into S01-like frontal repeat. |
| S04 a04 | `exec-769fd07c-9243-4897-a9db-de9eff6039d7.png` | `S04_attempt04_theater_hierarchy.png` / `22dd4d8618e1bfc51e0b4c611a58731e9b096488fb6c10b38e1092879a77b041` | Oversized seahorse/tiny Roshan destroyed trash hierarchy. |
| S04 a05 | `exec-b6d34220-a127-4de8-bf0e-9d088d590e9e.png` | `S04_attempt05_still_overscale.png` / `5edf14db08858aac4bb91f23f8f57fab2f73c36c51055afb8c7daa64f5c028d5` | Exact fixture restored but still exceeded the shot's rear-right scale limit. |
| S05 a01 | `exec-8271c470-f3d2-45ea-a0d0-6b805e3a6ca8.png` | `S05_attempt01_wrong_fixture.png` / `34520fe96e5ed133985d77798fec49b4ee2fde7ed73a0a4fb6915a85cddf0d49` | Wrong cream fixture/Roshan identity drift. |
| S05 a02 | `exec-40b26a14-de8c-43aa-9c4b-d182ef6ea698.png` | `S05_attempt02_ghost_roshan.png` / `e4564e6bd7c274c046af9bcbfbe1ace633cb7e94d4f8307e899f8f03bead0979` | Roshan body/tail became translucent. |
| S05 a03 | `exec-bffab348-bdad-4d9e-9d89-fe40391da7c7.png` | `S05_attempt03_giant_fixture.png` / `1ffe29488803eaefd8f3732c1e1295f055b8b136743914a213a9f07505e3e195` | Roshan opacity fixed, but seahorse remained a giant foreground portrait. |
| S06 a01 | `exec-b50dd841-b80d-420a-96ec-c3cd997853df.png` | `S06_attempt01_wrong_fixture.png` / `3ebeaba812e05d95aa664549c052e62b994e05934594498fb1373cf37486715b` | Wrong cream/horned fixture. |
| S06 a02 | `exec-481f5b79-6931-4bb6-9ca0-633cf923839f.png` | `S06_attempt02_missing_plug_duplicate_trash.png` / `ffce02eb7338703eeb0325aacc9f2d7afdd1e000347482af75f81b734f1fa5e4` | Mouth plug absent; duplicate leaf/incoherent trash. |
| S06 a03 | `exec-ede239a1-c131-413a-9c3c-50bad9dd07dc.png` | `S06_attempt03_missing_window.png` / `7cc719f6074b4fcfd22028bba6f34dfc8e9d47ee0e3d4f4f15c66324b4960313` | Canonical central underwater window missing. |

Rejected files are review evidence only. They must never be supplied to Grok
as approved continuity/style frames.
