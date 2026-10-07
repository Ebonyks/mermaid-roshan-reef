# Roshan wave: whole-frame drawings (revision 2)

> **OWNER_REJECTED 2026-10-07.** The owner's verdicts: "This is worse than the previous results,
> roshan mutates in size still" and "There are also significant overdraw issues, sprites need to
> be drawn whole, as a single unit, in this game." Measured afterwards: the head is 2.0–2.9%
> smaller from frame 6 to 31, the upper arm runs from 40% short to 36% stretched, and every frame
> is built from separately warped pieces of one drawing. Kept as evidence only. See the
> [Codex handoff](../../../docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/README.md).

Status: `REFERENCE_ONLY` / `OWNER_REJECTED`, owner-commissioned 2026-10-05. Baseline `e174a52dafb83e13df249ba040339554ca364ecf`.
This packet makes no runtime change, accepts no production asset, and closes no finding.

![Roshan waving: 41 frames at 24 fps](review/wave.gif)

## Owner correction 2026-10-05

The owner rejected [revision 1](../claude_2d_deform_wave_20261005/README.md):

> No arm moves as a single figure, the whole body moves at once, drawn as a whole frame

Revision 1 moved a cut-out arm over a body taken from a different drawing, and gave hair,
tail and fin their own delays. This revision changes three things:

- **One drawing per frame.** Every frame is exactly one complete approved drawing of
  Roshan (K0–K3, row 0 of `assets/characters/roshan_25d/roshan_gesture_a.png`). No frame
  combines pixels from two drawings, and nothing is filled from another drawing.
- **The whole body moves at once.** Arm, shoulders, head, hair, ponytail, torso, tail and
  fin all follow the same timing curve. Nothing lags behind, and nothing is added that the
  four drawings do not already show.
- **Whole frames in the master.** [`wave_master.aseprite`](wave_master.aseprite) has one
  layer, with one complete cel per frame.

## Review footage

- [Review movie, 768×768, 24 fps](review/wave_review.mp4) and the GIF above.
- [Native 256 px frames at 3× nearest-neighbour](review/wave_native256_x3_nearest.mp4).
- The authoritative pixels are the [41 native frames](frames/native/) (256×256 RGBA, the
  runtime cell size) and the master. The videos are H.264 viewing copies.

## Timeline

Codex's wave timeline is unchanged: 41 frames at 24 fps (1708 ms).

| Frames | Beat | Drawing used |
|---|---|---|
| 0–3 | Rest | K0, unchanged |
| 4–5 | Arm starts to rise | K0 bent toward K1 |
| 6–12 | Rise to the shoulder, then upward | K1, bent before and after its own pose (frame 7) |
| 13–21 | Overhead wave | K2, bent before and after its own pose (frame 17) |
| 22–31 | Lowering past the head, then out and down | K3, bent before and after its own pose (frame 27) |
| 32–35 | Lower to rest | K0 bent toward rest |
| 36–40 | Rest | K0, unchanged |

The drawing changes once per beat, at frames 6, 13, 22 and 32. At each change, the
outgoing and incoming drawings are bent to the same pose, so only drawing detail changes,
for example the closed smile of K0 versus the open smile of K1–K3. The script picks
the change frame by minimising bend plus gap
([`data/schedule.json`](data/schedule.json)); the source of every frame is listed in
[`data/frame_sources.json`](data/frame_sources.json).

## Method

1. **Correspondences.** 167 points on the whole figure (face, crown, neck, waist,
   hair, ponytail, other arm, tail, fin, silhouette) are matched across all four drawings
   ([data](data/correspondences.json)). The waving arm is described by its shoulder, elbow,
   wrist and fingertip in each drawing. The waist root is fixed.
2. **One pose curve.** The figure's pose at each frame is interpolated from the four
   drawings' poses with one non-uniform Catmull-Rom curve, easing in from and out to rest.
3. **One drawing, bent as a whole.** The frame's drawing is bent into that pose. The body
   follows a moving-least-squares rigid deformation, and the arm bends at the shoulder,
   elbow and wrist. Both deformations act on the same drawing. The drawing's own sleeve
   stays over the arm root, and the arm's own skin closes the armpit when it rotates.
4. **Gaps.** Where the drawing's own arm hid a few body pixels that become visible, the
   gap is closed from the surrounding pixels of the same frame. This affects at most
   21 px at 256 px, in frame 13, and is recorded per frame.
5. **No blending.** Each output pixel is one spatial resample of the frame's one drawing.
   There is no cross-dissolve, no temporal interpolation and no generated pixels.

## Machine verification

[`verification.json`](verification.json) records 20 checks, all PASS:

- The approved atlas hash is unchanged.
- There are 41 frames of 256×256 RGBA, and nothing touches the cell border.
- Rest frames 0–3 and 36–40 are byte-identical to the approved K0 cell, so the clip
  leaves and returns to idle cleanly.
- Every frame names exactly one source drawing, and there are exactly four drawing
  changes.
- At most 21 gap pixels are filled per frame, all from the same frame.
- Six frames re-render pixel-identically.
- The waist root target stays within 0.607 px.
- The eye spacing, crown–waist, neck–waist and crown–neck target distances stay inside
  the four drawings' own range.
- The master has one layer whose 41 cels equal the exported PNGs, totalling 1708 ms.

Rebuild everything with [`scripts/run_all.sh`](scripts/run_all.sh). It needs Python with
numpy, scipy, opencv-python-headless and pillow, plus ffmpeg, and takes about 6 minutes
on four CPU cores. [`manifest.json`](manifest.json) lists every file's SHA-256. These
checks are machine checks only.

## Known limits (agent review, not owner review)

- **Only four drawings exist.** Every in-between is one of them bent, not a new drawing.
  The furthest bends are where the arm swings out to the side: frames 4–6 and 29–33,
  up to 147° from the drawing's own arm pose. In these frames the rest drawing's relaxed
  hand, or K3's raised hand, is carried sideways. A drawn whole-figure key with the
  arm out to the side and the hand open would replace the largest bends. Under `DL-ASSET-02`
  that is the named gap; it would be one new whole drawing, not a per-frame campaign.
- **Elbow.** The elbow kinks slightly where K1's bent arm is straightened toward
  overhead. This is most visible at frame 12.
- **Hair near the raised arm.** The hair beside the raised arm is slightly ragged at
  frame 13, where the gap fill is largest.
- **Specks.** A few one-pixel matte specks sit near the hand in frame 31 and beside the
  bodice tip in frame 32.
- **Drawing changes.** The changes at 6, 13, 22 and 32 swap the face expression, the tail
  sparkles and the ponytail detail at once, as a whole-frame redraw would. They may read
  as a small jump when stepping frame by frame.
- **Resolution.** The review movie is a 3× render of 256 px art. Detail is capped by the
  approved atlas.
- **Aseprite.** The master was written to the published Aseprite file format by
  `scripts/aseprite_io.py` and has **not yet been opened in Aseprite**.

Human identity, motion and seam review, runtime atlas packing (`MA-ROSHAN-003`), device
playback, child review and owner acceptance are all outstanding.

## Cost

No ImageGen, video-model, paid-API or model-download calls were made. A full CPU rebuild
takes about 6 minutes. Annotation and iteration time was not metered.
