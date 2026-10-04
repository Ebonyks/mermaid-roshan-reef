# Imagine bridge return — 2026-09-13

Topic branch: `grok/imagine-bridge-return-20260913` off `origin/dev`
(`f98ef836`). Return PR: https://github.com/Ebonyks/mermaid-roshan-reef/pull/8
Do not treat `ca4dd196` as current status.

Filled Codex intake files live next to the packet templates:

- `CAPABILITY_CHECK.json`
- `RETURN_MANIFEST.json`
- this receipt
- `STYLE_DIAGNOSIS.md` (session 2)

## Session 4 — binaries and locked openings on GitHub

Owner asked to continue, complete, and upload onto git — not merge to master/dev,
not treat as delivery.

Complete packet now lives on `codex/roshan-swim-combined-handoff-20260914`
([PR #10](https://github.com/Ebonyks/mermaid-roshan-reef/pull/10)):

- 19 original H.264 MP4s under `returns/videos/` (~89 MB)
- Locked openings `openings/locked-front-right.png` / `locked-right.png`
- Full take-03 RETURN_MANIFEST, CORE_ART_AUDIT, reserved prompts

`BINARIES_ON_GITHUB` is true. `DELIVERY_ACCEPTED` stays false. Never master.

## Session 2 — style lock

Take-01 did not take the Grok handoffs. It emulated a new 3D mermaid instead of
the painted storybook character. See `STYLE_DIAGNOSIS.md`.

Repair executed here:

- Bound the unused 8-view painted cutouts (alpha already present).
- Composited them onto navy 1280×720. No character redraw.
- Animated RSW-01 take-02 with `imagine_image_to_video` from that still.
- Marked the eight take-01 clips rejected for STYLE_REWRITE.
- Quota 9 / 10. Locked-opening layout approval still pending.

Take-02 SHA-256 `fabb219b99df6ecfd0fd6f3b8578ecb204ce019541e3e0088b74d787529ecbf5`.
Identity holds. Delivery remains false.

## What was broken (session 1)

1. The packet the owner linked was a historical snapshot. Live publication is
   on `dev` with `ARCHIVE_COMPLETE: true` and `GENERATION_READY: false`.
2. Grok chats without video tools substituted still boards. START_HERE now
   forbids that.
3. Imagine cannot be driven from a GitHub tree URL. Images must be hashed,
   downloaded, and attached as IMAGE_1 + IMAGE_2.
4. Native video length is 6 / 10 / 15 seconds, not 8. This return uses 10s
   and labels it honestly.
5. GitHub's text file API cannot store the original MP4s. Hashes below are
   the authority. Playable files live in Reef Imagine Bridge.
6. **Style (session 2):** IMAGE_1 GitHub openings were a 3D redraw. The tool
   used (`reference_to_video`) invents a new scene. The 8-view cutouts were
   never bound.

## Bound inputs

| Role | File | SHA-256 |
|---|---|---|
| IMAGE_1 take-01 (do not reuse) | openings/front-right.png | `cb4f0ccccf31937aabeecc4cba0232d2e50ab37fe0dc97c9b9ac2ef986959bf0` |
| IMAGE_1 take-02 / take-03 | openings/locked-front-right.png | `6b0918967e5b1703e4b04a67b27798b7a733a6ab79c44314ebcf6f12bf1be685` |
| 8-view cutout | references/front-right.png | `b818e9d8852dcde1043662f290cf3f19e8c7e1bd8be55395548e5f54ee875ad6` |
| IMAGE_2 (all) | references/approved-front.png | `db2d2c13c2ccf9f0727934434adccdbf9d1d127943f743f436a48fff7c62ba3c` |

## Take hashes

Binaries are on PR #10. Hashes remain the authority.

| Sample | Disposition | SHA-256 |
|---|---|---|
| RSW-01 take-01 | rejected (style rewrite) | `a8de1b06b47860894b9d834b897358dfdbadce1a4508a49f95ad927803fe6366` |
| RSW-01 take-02 | comparison_candidate | `fabb219b99df6ecfd0fd6f3b8578ecb204ce019541e3e0088b74d787529ecbf5` |
| RSW-02 take-01 | rejected (style rewrite) | `78c91b17af0a20126ed7c456b8a08970b8b7fde272a1464742a2c2427490cb0a` |
| RSW-03 take-01 | rejected (style rewrite) | `96048e0ec855de8d1016c99732afe07f6e026cef1905074441df71d57d0e09cb` |
| RSW-04 take-01 | rejected (style rewrite) | `e7faf6a569c4c28d8538d67eef6138b35a35ea2995b8e823acfb1496d4fd98eb` |
| RSW-05 take-01 | rejected (style rewrite) | `735491d3c33d0261790abf3e73c41e31bc4298a0e2bccb6afe9b36dc87ab909f` |
| RSW-06 take-01 | rejected (style rewrite) | `f6110264954b243193b4d70ffc046adcb419bfbc801d2f246b5f4be91272b7fa` |
| RSW-07 take-01 | rejected (style rewrite) | `9df10f68a5e4db29478c4a5c3e3c367cb606579fe573b4fe96ce48247830a39e` |
| RSW-08 take-01 | rejected (style rewrite) | `51efe2fb3c1d48e7bb4131ef151a63779e9034d700cad0697735c3802efb5c9d` |

Native files: 10.04s, 1280×720, 24 fps, H.264 + unwanted AAC. Requested 8s silent.

Owner selection and `DELIVERY_ACCEPTED` stay false. No Aseprite conversion,
no runtime integration, no cinematic acceptance.
