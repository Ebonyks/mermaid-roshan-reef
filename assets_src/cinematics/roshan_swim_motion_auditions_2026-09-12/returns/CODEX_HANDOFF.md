# Codex handoff — reserved swim, combined clips

From Reef Imagine Bridge, 2026-09-14. For Codex on `Ebonyks/mermaid-roshan-reef`.
Do not commit this as delivery. `DELIVERY_ACCEPTED` stays false.

## Job

Reconstruct selected reserved swim motion in Aseprite from the take-03 references.
Imagine made the videos. Codex reconstructs movement. Video remains reference until
an explicit later production decision.

## MP4s are on this branch

All original H.264 files live here (19 files, ~89 MB):

https://github.com/Ebonyks/mermaid-roshan-reef/tree/codex/roshan-swim-combined-handoff-20260914/assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/returns/videos

Inventory with hashes: [returns/videos/README.md](returns/videos/README.md)

| Path on this branch | SHA-256 | Duration | What |
| --- | --- | --- | --- |
| `returns/videos/combined/RESERVED_REEL.mp4` | `7360743e173cc4d83869d66d037abf82cd1312091079738fa35e635db7cc000b` | 91.60s | All eight take-03 clips, slated. Review order, not one performance. |
| `returns/videos/combined/ASSEMBLY-01.mp4` | `29c0977cac9d5641d86f2af9bdf200f453892a6155f0cab7cc85cad4ef51884c` | 22.31s | Fragment assembly. New reference candidate. |
| `returns/videos/take-03/RSW-0N_take-03.mp4` | see README | 10.04s each | Reserved sources. Use these. |
| `returns/videos/take-01/` | see README | 10.04s each | Style rewrite. Do not adapt. |
| `returns/videos/take-02/RSW-01_take-02.mp4` | `fabb219b99df6ecfd0fd6f3b8578ecb204ce019541e3e0088b74d787529ecbf5` | 10.04s | Painted identity, camera-greeting. Do not adapt. |

Raw combined reel:

https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/codex/roshan-swim-combined-handoff-20260914/assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/returns/videos/combined/RESERVED_REEL.mp4

Raw assembly:

https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/codex/roshan-swim-combined-handoff-20260914/assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/returns/videos/combined/ASSEMBLY-01.mp4

## Source takes (reserved pass)

All take-03. Tool: `imagine_image_to_video` on locked painted 8-view openings.
Native 10.04s / 1280×720 / 24 fps / AAC.

| ID | GitHub path | SHA-256 | Disposition |
| --- | --- | --- | --- |
| RSW-01 | `returns/videos/take-03/RSW-01_take-03.mp4` | `027ff0112eab282e990fa15a4ea8ec1fa5ad101f189e350fb7d6935cca8c673d` | comparison_candidate |
| RSW-02 | `returns/videos/take-03/RSW-02_take-03.mp4` | `7095f4de8cb39f3ed30ccf0952af287e040d73422adc685aa67c07ff7e1a48b4` | comparison_candidate |
| RSW-03 | `returns/videos/take-03/RSW-03_take-03.mp4` | `a24e44bf84bc7aa3f8679fddf482058442ee49f3009c22521a5cfca032692715` | comparison_candidate · shortlist |
| RSW-04 | `returns/videos/take-03/RSW-04_take-03.mp4` | `072741097f2b43af119a9b65fbb23d4904adfd109fe4a3c19c4ea2a3f6f27a42` | comparison_candidate · shortlist |
| RSW-05 | `returns/videos/take-03/RSW-05_take-03.mp4` | `f0327efa16a8821f8d77b17198a761de9b5001e8fe0a3138512b9616708d51ea` | comparison_candidate · shortlist |
| RSW-06 | `returns/videos/take-03/RSW-06_take-03.mp4` | `9478b60c3f182c3b491fc3af854f7f6d85cc08346150ed1d1fdaf996c11a70e7` | comparison_candidate |
| RSW-07 | `returns/videos/take-03/RSW-07_take-03.mp4` | `678edf78e584624202cdc9bf5f301512095e0c68f612f7313befcd65d3400483` | inspiration_only · bracelet mutation |
| RSW-08 | `returns/videos/take-03/RSW-08_take-03.mp4` | `092e8b4659a7156d0dd7e5f1157e7f80216500e66f628f0fa20c05c51ba83128` | inspiration_only · bracelet mutation |

## ASSEMBLY-01 edit list (straight cuts)

1. RSW-05 0.00–3.00 idle wait — `f0327efa…`
2. RSW-01 1.00–5.50 ribbon glide — `027ff011…`
3. RSW-03 2.50–6.00 soft glance — `a24e44bf…`
4. RSW-04 2.00–7.00 shallow bank — `07274109…`
5. RSW-06 5.00–10.04 arrival hover — `9478b60c…`

No crossfade, morph, optical flow, reverse, or duplicated frames.
Joins are not matched on pelvis/phase. Inspect before adapting.

## Appearance lock

- Identity: `references/approved-front.png` `db2d2c13c2ccf9f0727934434adccdbf9d1d127943f743f436a48fff7c62ba3c`
- 8-view front-right: `b818e9d8852dcde1043662f290cf3f19e8c7e1bd8be55395548e5f54ee875ad6`
- 8-view right: `5f2eec477d00de4625c3dc501de71739fcb2e27ce3c76de6aac9dc464dcf5825`
- Locked openings (cutouts on navy, on this branch): `openings/locked-front-right.png` `6b091896…` / `openings/locked-right.png` `042c2e05…`
- Do not bind `openings/front-right.png` / `right.png` — CGI redraw used for take-01.

Painted storybook. Gold crown, one teal gem. Rainbow streak on anatomical left.
Pink bodice, lilac frills, pearlescent tail. Not Disney/Pixar 3D.

## Do not

- Adapt take-01. Style rewrite (bun, silver crown, extra fauna).
- Promote 07/08 gold bracelets as design.
- Treat the reel as a single generated performance.
- Switch to 3D, invent a new mermaid, or change Godot runtime / cinematics.
- Set `DELIVERY_ACCEPTED`.

## Related

- Packet: `codex/roshan-grok-motion-auditions-20260912` / live `dev` `f98ef836`
- Take-01 receipts: PR #8
- Reserved-pass receipts: PR #9
- This combined handoff + MP4s: [PR #10](https://github.com/Ebonyks/mermaid-roshan-reef/pull/10) off `dev`, never master
