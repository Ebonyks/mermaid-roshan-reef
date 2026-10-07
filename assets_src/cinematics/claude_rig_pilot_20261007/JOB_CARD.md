# Roshan rig pilot: animation job card V1

Reference-only study, owner commissioned 2026-10-07. Template:
[Animation job card V1](../../../design/templates/ANIMATION_JOB_CARD_V1.md). Baseline
`6238934447cf28834874396dfbaff65effafda46` (dev). No runtime, delivery or owner acceptance.

## Brief and limits

| Field | Value |
|---|---|
| Identity | `claude-rig-pilot-20261007`, revision 1, Claude, 2026-10-07; Mermaid Roshan, [movement language v1](../../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md) |
| Output lane | Reference-only study: run 1 runtime-rig test (rules off), run 2 structural guides for the next LTX take |
| Intention | Roshan gives the same gentle one-hand wave as the Union study, at one constant size |
| Required action | Rest 0 to 3, rise, above head about 17, lower past face and chest, settle 36 to 40; one arm, left of image |
| Fixed elements | Camera, neutral background, approved 2D identity; 256 px cell (run 1) and 640x896 canvas with waist at (216.5, 485) (run 2) |
| Entry / exit | Frames 0 and 40 are the approved K0 cell pose; no prop or contact |
| Reuse / gap | Approved `roshan_gesture_a.png` K0 and K2 hands; motion from existing Union take 1; no new art generated |
| Method | LTX motion tracked and solved onto a fixed-length rig. Run 1: Godot 4.7.2 Skeleton2D with skinned Polygon2D and hand sprites (owner-permitted rules-off exception). Run 2: Union guide port with the rig arm at the W3 lengths and one master phase |
| Runtime size | Run 1: 256 px cell art, rendered at 512 px (2x), 41 frames at 24 fps. Run 2: guides at 640x896, 320x448 and 160x224 |
| Motion tolerances | W2 figure ≤ 1.0% and head ≤ 2.0% peak-to-peak; W3 arm segments ±5% of 25.5, 24.5 and 20.5 cell px; frames 0 and 40 identical |
| Limits | 0 generated takes in this session; run 2 allows at most two takes, counting failures, within the 2026-10-07 wave handoff's brief; 0 ImageGen or paid calls |
| Stop / fallback | If the run-2 take still changes size or smears the hand, diagnose the guide/control family before another take; no per-frame still campaign |

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
| Human identity / style | Pending owner review of `run1/review.mp4` and `run2/review.mp4` |
| Human motion / seam | Agent notes only, in README run 1 shortfalls; owner review pending |
| Source / export machine | Run 1: rest composite equals K0 (0 px), frames 0 and 40 identical, Godot keys reproduced to 1e-6 rad, `measure_wave.py` PASS. Run 2: W3 0.0% on all frames |
| Gameplay machine | Not applicable: no game file changed |
| Device | Not run: Mobile renderer and target device untested |
| Child / owner | Pending |
