# Codex handoff: Roshan wave as whole sprites at one size

Status: `PROPOSED / CANDIDATE`, written by Claude for Codex on 2026-10-07. Baseline
`27fa7d075fccac79b36accb71f8a5d17dca52d68` (dev). This is a written specification: Claude
recommends and Codex builds. It grants no asset, runtime or owner acceptance.

## Owner corrections

| Date | Owner's words | Register |
|---|---|---|
| 2026-10-05 | "No arm moves as a single figure, the whole body moves at once, drawn as a whole frame" | `ODR-ROSHAN-WHOLE-FRAME-20261005` |
| 2026-10-07 | "This is worse than the previous results, roshan mutates in size still" | `ODR-ROSHAN-CONSTANT-SIZE-20261007` |
| 2026-10-07 | "There are also significant overdraw issues, sprites need to be drawn whole, as a single unit, in this game" | `ODR-SPRITE-WHOLE-UNIT-20261007` |

The first two corrections reject Claude's
[cut-out wave](../../../assets_src/cinematics/claude_2d_deform_wave_20261005/README.md) and
[whole-frame bending wave](../../../assets_src/cinematics/claude_whole_frame_wave_20261005/README.md).
The third applies to every sprite in the game, not only the wave.

## What the numbers show

[`tools/measure_wave.py`](tools/measure_wave.py) reads exported frames and writes numbers only.
It measures figure scale (one similarity fit to the crown gem, eyes, mouth, neckline, waist and
tail), head scale (whole-patch alignment of the face), the waving arm's segment lengths
against the contract below, and the master's layer count. All three wave candidates,
measured against each clip's own frame 0:

| Clip | Figure scale peak-to-peak | Head scale peak-to-peak | Arm vs contract (worst) | Master layers | Result |
|---|---|---|---|---|---|
| Claude revision 1, cut-out arm ([data](data/claude_rev1_cutout.json)) | 0.80% | 2.61% | upper arm −40.1% (frame 7), hand −13.0% (frame 32) | 5 | FAIL |
| Claude revision 2, bent whole drawings ([data](data/claude_rev2_whole_frame.json)) | 0.78% | 2.71% | upper arm −40.1% (frame 7), hand −15.0% (frame 31) | 1 | FAIL |
| Codex LTX-2.5 Union take 1 ([data](data/codex_ltx25_union_take1.json)) | 0.11% | 0.34% | not measured (no joint annotation) | not checked | size PASS |

Roshan's overall size held in all three. What changed size was her head and her arm.

- **Head.** In revision 2 the head is 2.0–2.9% smaller from frame 6 to 31 and snaps back
  at frame 32. The approved keys K1, K2 and K3 (`roshan_gesture_a.png` row 0, columns 1–3)
  draw her head about 2.5% smaller than K0.
- **Arm.** The keys draw the upper arm at 24.5, 15.3, 26.7 and 22.0 px (K0–K3, 256 px cell).
  The hand is 16.2 px in K0 (relaxed, by design) and 18.9–21.0 px open. K1's elbow points
  toward the viewer, so its upper arm is foreshortened to 15.3 px. Anything that moves
  between these drawings makes the arm grow and shrink. That includes bending them, which
  Claude did, and generating in-betweens guided by them.
- **Overdraw.** Revision 1 stacked arm, body, sleeve and shoulder pieces over each other.
  Revision 2 kept one layer but still built every frame from separately warped pieces.
  Both are what the owner called overdraw.

Claude's conclusion is that deformation cannot meet these rules. It cannot move a whole
single-unit sprite's arm between these four drawings without cutting the sprite into
pieces or stretching the skin between arm and body, and it inherits the keys' size
differences. Claude does not propose another bending attempt. Codex's whole-frame Union
take is the only candidate that holds size, and it generates each frame whole. Its open defect is the smeared
fingers recorded in its own packet.

## Requirements for the next wave

| ID | Requirement | Check |
|---|---|---|
| W1 | **Whole sprite.** Every delivered frame is one complete drawing of Roshan in one layer. No part layers, pasted hands or arms, cross-fades or stacked copies, at export or at runtime. Any repair is painted into that one frame and reviewed as the whole frame. | `measure_wave.py --master` reports 1 layer; frame review. |
| W2 | **One size.** Figure scale peak-to-peak ≤ 1.0% and head scale peak-to-peak ≤ 2.0% against frame 0. | `measure_wave.py`. |
| W3 | **Fixed arm proportions.** In the 256 px cell, the upper arm is 25.5 px, the forearm 24.5 px and the open hand 20.5 px (wrist to longest fingertip), each ±5%. The waving arm stays in the picture plane, with no elbow-toward-viewer pose like K1's. Frames showing K0's relaxed rest hand set `hand_open: false`. | `measure_wave.py --joints`, with shoulder, elbow, wrist and fingertip annotated per frame in Aseprite. |
| W4 | **Whole body at once.** Arm, shoulders, head, hair, torso and tail move together on one timing, with no per-part delays. Hands and fingers stay crisp and painted. | Normal-speed and frame-step review. |
| W5 | **Same clip contract.** 41 frames at 24 fps (1708 ms). Frames 0 and 40 are the approved K0 cell, so the wave leaves and returns to idle cleanly. | Byte comparison with K0. |
| W6 | **Numbers before review.** Run the tool on the native frames and publish its report with the frames, a one-layer master and the rejected takes. | Report in the packet. |

The W3 lengths come from the full-length approved drawings, K0 and K2. W3 is Claude's
reading of "mutates in size" for the arm. If the owner prefers to keep a foreshortened
pose, change the contract in the tool and record it.

## Recommended route

1. **Keep the whole-frame route.** Use the Union structural-control recipe from
   [`ltx25_union_trial_20261004`](https://github.com/Ebonyks/mermaid-roshan-reef/tree/405cb1c6d4869c15edd032494c83f383d6e3e398/assets_src/cinematics/ltx25_union_trial_20261004)
   (branch `codex/ltx25-8gb-wave-20261004`). It generates one whole frame at a time and
   held size to 0.11% and 0.34%.
2. **Correct the guide family before the next take.**
   - Annotate the arm joints in every structural outline and run W3 on them.
   - Redraw the outlines derived from K1 and K3 so the arm keeps the contract lengths in
     the picture plane.
   - Scale any guide built from K1–K3 so its head matches K0's. Use one uniform scale per
     guide, in Aseprite.
   - Without these fixes, the next take is asked to change her size.
3. **Treat the fingers as the one open defect.** Try Codex's planned temporal-detail stage
   first. If a repair is still needed, paint it into the flattened frame (W1), not as a
   pasted hand layer.
4. **Budget.** `DL-MOT-16` applies: two takes per brief, with every take and its cost
   recorded. This is not a per-frame ImageGen campaign.

## Files

| Path | Role |
|---|---|
| [`tools/measure_wave.py`](tools/measure_wave.py) | Numbers-only check (W1–W3). Run it with `python -I`. |
| [`data/`](data/) | Reports for the three candidates, plus the joints Claude's revisions drew. |
| `assets/characters/roshan_25d/roshan_gesture_a.png` | Approved keys, row 0. SHA-256 `e70139b23c9f84c0e8f0c1063145ca4e9e67ee32c57aa544bc08193326af9b9d`. |

Codex's take 1 was measured on its native frames at commit `405cb1c6`, scaled from the
256 px cell by 3.2025, offset (−216.95, 33.85):

```text
python -I tools/measure_wave.py --frames 'take_1/refined_frames/%04d.png' --count 41 \
    --cell-scale 3.2025 --offset -216.95 33.85
```

`ARCHIVE_COMPLETE`, `GENERATION_READY` and `DELIVERY_ACCEPTED` stay separate. Owner review
at normal speed on the tablet remains the acceptance gate.
