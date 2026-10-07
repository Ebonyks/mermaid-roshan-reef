# Roshan whole-frame wave — animation job card V1

Template: [Animation job card V1](../../../design/templates/ANIMATION_JOB_CARD_V1.md).
This is a reference-only study with no runtime, production, device, child or owner acceptance.
**OWNER_REJECTED 2026-10-07:** "roshan mutates in size still"; "sprites need to be drawn whole, as a
single unit". See the [Codex handoff](../../../docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/README.md).

## Brief and limits

| Field | Value |
|---|---|
| Identity | `claude-whole-frame-wave-20261005`, revision 2 (supersedes the owner-rejected [revision 1](../claude_2d_deform_wave_20261005/JOB_CARD.md)), Claude, 2026-10-05. Source commit `e174a52dafb83e13df249ba040339554ca364ecf`. Movement direction: [Roshan movement language](../../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md). |
| Output lane | Reference-only study for a gameplay sprite (256 px cell). Not integrated. |
| Intention | Roshan greets: she lifts her hand above her head, waves it down past her head, and settles back to her friendly rest pose. |
| Required action | The whole figure moves at once. Arm, shoulders, head, hair, ponytail, torso, tail and fin follow one timing curve. There is no contact and no prop. |
| Owner direction | 2026-10-05: "No arm moves as a single figure, the whole body moves at once, drawn as a whole frame". |
| Fixed elements | The waist root is fixed at (135.5, 143) in the cell. World scale is constant, the background neutral, and the approved 2D identity unchanged. |
| Entry / exit | Starts and ends on the K0 cell verbatim (frames 0–3 and 36–40). Front view. Mirroring for left/right is a later runtime choice. |
| Reuse / gap | Uses only `roshan_gesture_a.png` row 0, columns 0–3, and one whole drawing per frame. Named gap: a whole-figure drawing with the arm out to the side and the hand open, which would cover frames 4–6 and 29–33. |
| Method | Local, CPU-only. Each frame bends one complete approved drawing as one figure, using moving-least-squares body deformation and shoulder/elbow/wrist bends on that same drawing. The drawing changes once per beat, with no blends. The output goes to a one-layer Aseprite master. This departs from the LTX default because Codex's bounded LTX trials stayed nonviable on hand sharpness and the owner allowed other methods. |
| Runtime size | 256×256 RGBA, 41 frames at 24 fps (1708 ms). Review copy 768×768. |
| Motion tolerances | Root target within 1 px of rest (measured 0.607 px). Inter-anchor distances stay inside the four drawings' own range ±0.3 px. Rest frames equal K0 exactly. Gap fill is at most 25 px per native frame. |
| Limits | No generated takes, ImageGen or paid calls. The CPU rebuild must finish in under 10 minutes. Annotation and iteration time was not metered. |
| Stop / fallback | If whole-frame bending still reads as mechanical, commission the named arm-out drawing (one whole key). Alternatively, use this sequence as a whole-figure motion control for a V2V or IC-LoRA pass, with hand-smear review. No per-frame ImageGen campaign. |

## Bound inputs and provenance

- `assets/characters/roshan_25d/roshan_gesture_a.png`: 1024×1024 RGBA, SHA-256
  `e70139b23c9f84c0e8f0c1063145ca4e9e67ee32c57aa544bc08193326af9b9d`. It is approved
  project art and is unchanged.
- Derivations: [`data/`](data/) (roots, anchors, correspondences, schedule with every
  candidate's bend and gap, per-frame source) and [`frames/native/`](frames/native/).
  The master is [`wave_master.aseprite`](wave_master.aseprite): one layer, 41 whole cels.
  The full code is in [`scripts/`](scripts/), and every file's hash is in
  [`manifest.json`](manifest.json).
- Spatial resampling: each output pixel samples the frame's one drawing once. Native
  frames use bilinear sampling; review frames use bicubic at 3×. On the 3× canvas, the body
  deformation is solved on a 3 px grid and only the coordinates are upsampled.
- Gap fill: at most 21 px per native frame, taken from the same frame (OpenCV Telea
  inpainting, radius 3). The per-frame counts are in `data/frame_sources.json`.
- Not used: temporal interpolation, cross-dissolve, generated pixels, pixels from a
  second drawing, and position guides.
- Holds: frames 0–3 and 36–40 are the K0 rest drawing that frames the gesture.

## Reviews and integration

| Evidence lane | Result |
|---|---|
| Human identity / topology / style | PENDING. The agent's notes are under known limits in the README. |
| Human motion / contact / seam | PENDING. Agent notes: largest bends at frames 4–6 and 29–33, an elbow kink at frame 12, and drawing changes at 6, 13, 22 and 32. |
| Source / export machine | PASS: 20 checks in [`verification.json`](verification.json). |
| Cinematic machine | NOT_APPLICABLE. This is a gameplay-sprite study. |
| Gameplay machine | NOT_APPLICABLE until runtime integration (atlas packing, `MA-ROSHAN-003`). |
| Device | PENDING. |
| Child / owner | PENDING. |

| Status | State |
|---|---|
| `ARCHIVE_COMPLETE` | Pending GitHub publication. |
| `GENERATION_READY` | Not applicable. |
| `DELIVERY_ACCEPTED` | No. |
