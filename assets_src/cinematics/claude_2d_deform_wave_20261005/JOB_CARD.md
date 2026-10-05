# Roshan 2D-deformation wave — animation job card V1

Template: [Animation job card V1](../../../design/templates/ANIMATION_JOB_CARD_V1.md).
Reference-only study; no runtime, production, device, child or owner acceptance.
**OWNER_REJECTED 2026-10-05:** "No arm moves as a single figure, the whole body moves at once,
drawn as a whole frame." Superseded by [revision 2](../claude_whole_frame_wave_20261005/JOB_CARD.md).

## Brief and limits

| Field | Value |
|---|---|
| Identity | `claude-2d-deform-wave-20261005`, revision 1, Claude, 2026-10-05; source commit `f73236759755fd220cc495cc48f9e822a3d65ced`; [Roshan movement language](../../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md) |
| Output lane | Reference-only study for a gameplay sprite (256 px cell). Not integrated. |
| Intention | Roshan greets: she lifts her hand above her head, waves it down past her head, and settles back to her friendly rest pose. |
| Required action | The waving arm (her right, image-left) rises from rest, goes overhead and lowers. The shoulder, torso lean, head, hair, other arm, tail and fin respond. No contact or prop. |
| Fixed elements | Waist root (135.5, 143) in the cell, constant world scale, neutral background, approved 2D identity. |
| Entry / exit | Both enter and exit on the K0 cell verbatim (frames 0 and 40), so the clip can leave and return to idle. Front view; left/right mirroring is a later runtime choice. |
| Reuse / gap | Uses only `roshan_gesture_a.png` row 0, columns 0–3. No new key was drawn. Codex's ImageGen key 22 is not used. Gap: four keys leave the straight-out arm and elbow-fold in-betweens soft; a named new key would need `DL-ASSET-02`. |
| Method | Local, CPU-only authored 2D: per-key arm/body layer split, MLS rigid body deformation, per-segment rigid arm warp, drawing switches with no blends, and an Aseprite master. Routing exception from the LTX default: Codex's bounded LTX trials remain nonviable for hand sharpness, and the owner allowed other methods. |
| Runtime size | 256×256 RGBA, 41 frames at 24 fps (1708 ms). Review copies at 640×896. |
| Motion tolerances | Root target ≤ 1 px from rest (measured 0.607 px). Inter-anchor distances must stay inside the approved keys' range ±0.3 px. Endpoints must equal K0 exactly. |
| Limits | Zero generated takes, zero ImageGen, zero paid calls. CPU rebuild under 10 minutes. Cleanup and annotation time was not metered. |
| Stop / fallback | If the owner rejects the arm layer as limb animation, use this sequence only as a whole-figure control for a V2V or IC-LoRA pass, or commission named in-between keys. Never start a per-frame ImageGen campaign. |

## Bound inputs and provenance

- `assets/characters/roshan_25d/roshan_gesture_a.png`: 1024×1024 RGBA, SHA-256
  `e70139b23c9f84c0e8f0c1063145ca4e9e67ee32c57aa544bc08193326af9b9d`, last changed in
  `d652d5a78477825b49416778957dc2698d269439`. It is approved project art and is unchanged.
  Cells (0, 0)–(3, 0) supply all pixels.
- Comparison input only: the Codex LTX-2.5 Union take 1 native frames and the K0 guide at
  commit `405cb1c6d4869c15edd032494c83f383d6e3e398`. Hashes are in
  [`comparison/codex_source.json`](comparison/codex_source.json). These frames are never a
  source of delivery pixels.
- Derivations: [`data/`](data/) (roots, anchors, correspondences, canvas fit, per-frame
  sources), [`layers/`](layers/) (arm cut-outs and donor-filled arm-free bodies),
  [`frames/native/`](frames/native/), and [`wave_master.aseprite`](wave_master.aseprite).
  The complete code is in [`scripts/`](scripts/). Every file's hash is in
  [`manifest.json`](manifest.json).
- Spatial resampling: each output pixel samples one source layer once. Native frames use
  bilinear sampling; review frames use bicubic. Large canvases solve the body MLS field on
  a 3 px grid and upsample the coordinates only, with a mean deviation of 0.0005 from the
  exact solve.
- No temporal interpolation, cross-dissolve, generated pixel or position guide is used.
- Holds: frames 0 and 40 are the K0 rest drawing, framing the gesture. Frames 1–3 and
  37–39 carry anticipation and settle motion.

## Reviews and integration

| Evidence lane | Result |
|---|---|
| Human identity / topology / style | PENDING. Agent notes are in the README's known defects. |
| Human motion / contact / seam | PENDING. Agent notes: shoulder seam, elbow fold, drawing changes at frames 5, 7, 12, 23, 32 and 33. |
| Source / export machine | PASS: 21 checks in [`verification.json`](verification.json). |
| Cinematic machine | NOT_APPLICABLE. This is a gameplay-sprite study, not cinematic footage. |
| Gameplay machine | NOT_APPLICABLE until runtime integration (atlas packing, `MA-ROSHAN-003`). |
| Device | PENDING. |
| Child / owner | PENDING. |

`ARCHIVE_COMPLETE`: pending GitHub publication of this packet. `GENERATION_READY`: not
applicable, since no generator job is involved. `DELIVERY_ACCEPTED`: no.
