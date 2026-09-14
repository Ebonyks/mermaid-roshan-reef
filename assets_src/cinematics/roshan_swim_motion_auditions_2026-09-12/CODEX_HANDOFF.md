# Codex handoff — reserved swim, combined clips

From Reef Imagine Bridge, 2026-09-14. For Codex on `Ebonyks/mermaid-roshan-reef`.
Do not commit this as delivery. `DELIVERY_ACCEPTED` stays false.

## Job

Reconstruct selected reserved swim motion in Aseprite from the take-03 references.
Imagine made the videos. Codex reconstructs movement. Video remains reference until
an explicit later production decision.

## Combined clips (playable in the Imagine Bridge)

| File | SHA-256 | Duration | What it is |
| --- | --- | --- | --- |
| `RESERVED_REEL.mp4` | `7360743e173cc4d83869d66d037abf82cd1312091079738fa35e635db7cc000b` | 91.60s | All eight take-03 clips, 1.25s slates, straight cuts. Review order, not one performance. |
| `ASSEMBLY-01.mp4` | `29c0977cac9d5641d86f2af9bdf200f453892a6155f0cab7cc85cad4ef51884c` | 22.31s | Fragment assembly: idle → glide → glance → bank → arrival. New reference candidate. |

GitHub cannot store the MP4s through the text file API. Hashes above are the
authority. Originals live in the Bridge under `auditions/` and `auditions/combined/`.

## Source takes (reserved pass)

All take-03. Tool: `imagine_image_to_video` on locked painted 8-view openings.
Native 10.04s / 1280×720 / 24 fps / AAC.

| ID | SHA-256 | Disposition |
| --- | --- | --- |
| RSW-01 | `027ff011…ca8c673d` | comparison_candidate |
| RSW-02 | `7095f4de…7e1a48b4` | comparison_candidate |
| RSW-03 | `a24e44bf…32692715` | comparison_candidate · shortlist |
| RSW-04 | `07274109…f6f27a42` | comparison_candidate · shortlist |
| RSW-05 | `f0327efa…708d51ea` | comparison_candidate · shortlist |
| RSW-06 | `9478b60c…c11a70e7` | comparison_candidate |
| RSW-07 | `678edf78…d3400483` | inspiration_only · bracelet mutation |
| RSW-08 | `092e8b46…c51ba831` | inspiration_only · bracelet mutation |

Full hashes and reviews: `RETURN_MANIFEST.take-03.json` on PR #9.

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
- Locked openings (cutouts on navy): `6b091896…` / `042c2e05…`

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
- This combined handoff: `codex/roshan-swim-combined-handoff-20260914` off `dev`, never master
