# Roshan rig pilot: animation job card V1

Reference-only study, owner commissioned 2026-10-07. Template:
[Animation job card V1](../../../design/templates/ANIMATION_JOB_CARD_V1.md). Baseline
`6238934447cf28834874396dfbaff65effafda46` (dev). No runtime, delivery or owner acceptance.

## Brief and limits

| Field | Value |
|---|---|
| Identity | `claude-rig-pilot-20261007`, revision 3 (run 1 closed after owner rejection; run 2 takes on the PC runner; outfits on clips), Claude, 2026-10-07; Mermaid Roshan, [movement language v1](../../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md) |
| Output lane | Reference-only study: run 1 runtime-rig test (rules off, rejected), run 2 rig-guided LTX takes, game outfits baked onto whole-frame clips |
| Intention | Roshan gives the same gentle one-hand wave as the Union study, at one constant size |
| Required action | Rest 0 to 3, rise, above head about 17, lower past face and chest, settle 36 to 40; one arm, left of image |
| Fixed elements | Camera, neutral background, approved 2D identity; 256 px cell (run 1) and 640x896 canvas with waist at (216.5, 485) (run 2); outfits keep K0's bodice box size on every frame |
| Entry / exit | Frames 0 and 40 are the approved K0 cell pose; no prop or contact |
| Reuse / gap | Approved `roshan_gesture_a.png` K0 and K2 hands; motion from existing Union take 1. Gap: no approved front-facing closed eyes, so the pilot blink is painted on K0's eyes (pending Codex/owner review) |
| Method | LTX motion tracked and solved onto a fixed-length rig. Run 1: Godot 4.7.2 Skeleton2D with skinned Polygon2D and hand sprites (owner-permitted rules-off exception); revision 2 adds authored acting and idle on the LTX timing, a hair chain, a free-arm chain and a painted blink. Run 2: Union guide port with the rig arm at the W3 lengths and one master phase |
| Runtime size | Run 1: 256 px cell art, rendered at 512 px (2x), 41 frames at 24 fps. Run 2: guides at 640x896, 320x448 and 160x224 |
| Motion tolerances | W2 figure ≤ 1.0% and head ≤ 2.0% peak-to-peak; W3 arm segments ±5% of 25.5, 24.5 and 20.5 cell px; frames 0 and 40 identical |
| Limits | Run 2: at most 8 local RTX 3060 Ti takes counting failures (`ODR-RIG-PILOT-TRIALS-20261007`, bounded exception to the default two under `DL-MOT-16`), enforced by the PC runner, diagnosed between batches; 20-minute default and 40-minute hard job cap; 0 ImageGen, API or paid calls |
| Stop / fallback | Stop at the take cap, a STOP file or the owner closing the runner. If a take still changes size or smears the hand, diagnose before the next batch; no per-frame still campaign, no part repair |

## Bound inputs and provenance

| Input | SHA-256 / revision | Role |
|---|---|---|
| `assets/characters/roshan_25d/roshan_gesture_a.png` | `e70139b23c9f84c0e8f0c1063145ca4e9e67ee32c57aa544bc08193326af9b9d` | Rig parts (K0 body, arm, rest hand, sleeve; K2 open hand) and silhouettes |
| `assets_src/cinematics/ltx25_union_trial_20261004/take_1/refined_frames/0000-0040.png` | per-file hashes in [manifest](manifest.json) | Motion source (numbers only) |
| `assets_src/cinematics/ltx25_union_trial_20261004/scripts/guide.lua` | per-file hash in [manifest](manifest.json) | Contours and pose keys ported to `render_guides.py` |
| `docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/tools/measure_wave.py` | per-file hash in [manifest](manifest.json) | W2/W3 measurement |
| Godot `Godot_v4.7.2-stable_linux.x86_64.zip` | SHA-512 `9aa00f7a...c54c65`, matches `tools/godot_baseline.json` | Run 1 build and render (not redistributed) |

Run 2 guides are position-only controls, excluded from runtime, `used_as_delivery_pixels: false`.

## Reviews

| Lane | Result |
|---|---|
| Human identity / style | Owner 2026-10-07 on revision 1: rough take, frozen body, frame artifacts (`ODR-RIG-PILOT-REV2-20261007`); revision 2 rejected: overdraw, figure not moving as a whole, rough crops (`ODR-RIG-PILOT-REV2-REJECTED-20261007`); run-2 takes and the outfit clips pending |
| Human motion / seam | Agent notes only, in README run 1 shortfalls; owner review pending |
| Source / export machine | Run 1 revision 1: rest composite equals K0 (0 px), `measure_wave.py` PASS. Revision 2: rest composite differs from K0 in 40 contour/hem px, Godot keys exact, `measure_wave.py` PASS (figure 0.3%, head 0.67%), arm acceleration cut from 76 to 13 °/frame². Run 2: W3 0.0% on all guide frames; takes pending. Outfits on Union take 1 frames: 41/41 frames dressed for all four outfits, clothing area spread ≤ 2.3%, drift on the bodice ≤ 0.35 px; builder default outputs byte-identical (56 files) |
| Gameplay machine | Not applicable: no runtime file changed. `tools/build_fashion_outfits.gd` gained an opt-in `--fit/--out` mode; its default game outputs are byte-identical |
| Device | Not run: Mobile renderer and target device untested |
| Child / owner | Pending |
