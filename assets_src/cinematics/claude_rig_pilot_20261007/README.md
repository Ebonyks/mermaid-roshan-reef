# Roshan deterministic-rig pilot: LTX motion onto a fixed rig, two runs (2026-10-07)

**Run 1 `EXECUTION_PASS / RULES_OFF_TEST_ONLY`. Run 2 `GUIDES_READY / TAKE_NOT_RUN`.**
Both runs take their motion from LTX-2.5 Union take 1 and put it on one deterministic rig
whose bone lengths never change. Run 1 ignores the owner rules for testing, as the owner asked.
Its analysis found shortfalls, so run 2 brings the rules back. Nothing here is runtime,
delivery, device, child or owner acceptance. No finding lifecycle changes.

## Owner answers

| Date | Owner's words / choice | Register |
|---|---|---|
| 2026-10-07 | Chose "Rig drives the guides": solve the LTX take onto a fixed-length rig and use its poses as the guides for the next whole-frame LTX take. | `ODR-RIG-PILOT-GUIDES-20261007` |
| 2026-10-07 | "Yes, render them": Claude may render this pilot's guide images and preview (one-time exception to the 2026-09-30 written-handoff rule). | `ODR-RIG-PILOT-IMAGE-EXCEPTION-20261007` |
| 2026-10-07 | "Trial two test runs, one that completely ignores these rules for purposes of testing, and then if there are problems or shortfalls with the drafts that are analyzed, introduce these rules back again. The game was previously incapable of animating in this way, I suspect that it may be, but permit claude to trial using a different approach." | `ODR-RIG-PILOT-RULES-OFF-TEST-20261007` |

The rules set aside for run 1 only: `ODR-ROSHAN-WHOLE-FRAME-20261005`, `ODR-SPRITE-WHOLE-UNIT-20261007`,
the CLAUDE.md rule that Roshan has no rig or skeleton, and the written-handoff rule. They stay
binding for production and for run 2.

## Watch

| Run | Review video | Authoritative frames |
|---|---|---|
| 1, rules off | [LTX take 1 / Godot rig, same scale](run1/review.mp4) | [run1/frames](run1/frames) (512 px = 2 x cell) |
| 2, rules back | [Union guide / rig guide / LTX take 1](run2/review.mp4) | [run2/guide_full](run2/guide_full), [half](run2/guide_half), [quarter](run2/guide_quarter) |

Both videos are 41 frames at 24 fps (1708 ms). H.264 copies are lossy; PNGs are authoritative.

## Shared motion pipeline (numbers only)

1. [`track_ltx.py`](scripts/track_ltx.py) reads the 41 native take-1 frames. Body landmarks use
   `measure_wave.py`'s tracker plus a hair and a fin point. The waving arm is solved by
   analysis-by-synthesis: the rig arm (capsules plus the approved K0 rest hand or K2 open hand)
   is fitted to the take's arm skin mask. Free values: three angles, a small shoulder offset and
   the two segment lengths as scales of the W3 contract. Median IoU 0.67, minimum 0.45.
2. [`solve.py`](scripts/solve.py) re-poses the fixed-length rig onto those joints with two-bone IK.
   The wrist goes to the take's wrist, clamped to the arm's reach. The elbow bends to the take's
   side, and the hand keeps the take's direction. Automatic cleanup, all recorded in
   [`rig_pose.json`](data/rig_pose.json):
   - one rest, open, rest hand schedule (open hand frames 7 to 32)
   - a wrist limit of ±75°
   - IoU-weighted smoothing (sigma 1 frame)
   - exact K0 rest at frames 0 and 40

   No hand polish was applied.

What the fit measured in the LTX take itself ([run2_measure.json](data/run2_measure.json)):
- **Upper arm, raised (frame 17):** 33.7% longer than the contract.
- **Upper arm, rising (frame 5):** 50.5% shorter.
- **Forearm, lowering (frame 27):** 54.7% shorter.
- **The cause is in the guide.** The Union guide asked for these changes. Its interpolated joints
  run the upper arm from −43.6% to +17.3% and the forearm from −62.0% to +40.7%, and its hand
  outline is 19.3% under contract.

Frames 4 to 5 and 25 to 31 are low confidence (IoU under 0.6), because the take's hand there is smeared and
missing from the skin mask. On straight-arm frames the split between upper arm and forearm is
ambiguous; only their sum is measured.

## Run 1: rules off, runtime rig in Godot 4.7.2

[`build_parts.py`](scripts/build_parts.py) cuts the approved atlas
(`roshan_gesture_a.png`, SHA-256 `e70139b2...`) into five 256 px parts:

| Part | Source | Godot node |
|---|---|---|
| Body | K0 without the waving arm and sleeve | Polygon2D, 1,509 vertices, skinned to torso, head, hair, tail1, tail2, fin |
| Arm | K0 upper arm and forearm, plus a 38 px skin cap hidden under the sleeve | Polygon2D, skinned to upper arm and forearm |
| Rest hand | K0 relaxed hand | Sprite2D on the hand bone |
| Open hand | K2 open hand, scaled to the W3 hand length | Sprite2D on the hand bone |
| Sleeve | K0 left sleeve ruffle | Sprite2D on the torso, drawn over the shoulder joint |

At rest the parts recombine to K0 exactly: 0 premultiplied pixels differ.
[`build_rig.gd`](run1_godot/tools/build_rig.gd) builds [`rig_wave.tscn`](run1_godot/rig_wave.tscn)
from those parts. The scene has a Skeleton2D with 10 Bone2D, the two skinned Polygon2D, the
sprites, and an AnimationPlayer `wave` with one key per frame (looping for preview).

The frames were rendered by the official Godot 4.7.2 Linux build. Its SHA-512 matches
`tools/godot_baseline.json`. Rendering used `gl_compatibility` under Xvfb, since this session has
no Vulkan, so the Mobile renderer is untested. Manual-mode seeking reproduces every key to
1e-6 rad. Open [`run1_godot/project.godot`](run1_godot/project.godot) in Godot 4.7.2 and press
F5 to watch it.

**Answer: yes, the game engine can animate this way.** Skeleton2D skinning, bone keys and the
hand swap all run in 4.7.2 with ordinary 2D nodes.

| Check (`measure_wave.py`, [run1_measure.json](data/run1_measure.json)) | Result |
|---|---|
| Figure scale peak-to-peak (≤ 1.0%) | **0.05% PASS** |
| Head scale peak-to-peak (≤ 2.0%) | **0.16% PASS** |
| Arm vs W3 (±5%) | **PASS**: upper −3.9%, forearm +4.1% (K0's own drawing), hand 0.0% |
| Frames 0 and 40 | identical; frame 0 vs K0 at 2x, mean absolute difference 0.31/255 |

**Shortfalls found in analysis (why run 2 exists):**
1. **Overdraw, rejected 2026-10-07.** Each frame stacks four draws: body, arm, hand and sleeve.
   This is the part-layer construction `ODR-SPRITE-WHOLE-UNIT-20261007` rejects.
2. **The arm moves alone, rejected 2026-10-05.** The body follows LTX's own body motion, which is
   almost nothing: torso ≤ 0.49°, tail ≤ 0.70°, hair ≤ 0.49°, head ≤ 0.17°, root ≤ 0.05 px. The
   result reads as a still figure with a moving arm. A bigger authored body response would be a
   per-part addition rather than a redrawn figure.
3. **No redraw.** K0's hanging arm is rotated, so its painted shading and outline rotate with it.
   There is no foreshortening. Resampling 256 px art softens the arm and hand.
4. **Hand pop.** The relaxed and open hands are different drawings. They switch at frames 7
   and 33.
5. **The rig cannot follow length changes.** Where LTX lengthens the arm (frames 14 to 20), the
   rig hand falls up to 13.9 cell px below the take's hand. Smeared take frames give
   low-confidence poses that would need hand polish in the AnimationPlayer.

What run 1 does well: size is constant by construction, rest frames are exact, the motion is
deterministic and editable, and all of it costs four small textures and two meshes. For props,
items and non-Roshan characters with no whole-sprite rule, this is a usable route today.

## Run 2: rules back, rig drives the guides

[`render_guides.py`](scripts/render_guides.py) ports the Union `guide.lua`: the same contours,
Catmull-Rom spans, 1 px lines and full, half and quarter grids. Two things change:
- **The waving arm is the rig arm** at the W3 lengths, posed by the same LTX solve. The upper arm
  is 81.7 px, the forearm 78.5 px and the open hand 65.7 px on the 640×896 canvas. It is always
  in-plane, with a rounded elbow.
- **One timing for the whole body.** Lean, shoulder lift, hair and tail all follow one master
  phase: the solved arm's own elevation. This replaces the Union guide's separate
  `sin(i*pi/20)` hair and tail sway (W4).

| W3 on the guide joints ([run2_measure.json](data/run2_measure.json)) | Upper arm | Forearm | Hand |
|---|---|---|---|
| Union take-1 guides | −43.6% to +17.3% | −62.0% to +40.7% | −19.3% |
| Rig guides (run 2) | **0.0%** | **0.0%** | **0.0%** |

The guides are structural controls only (`used_as_delivery_pixels: false`, see
[guide_plan.json](run2/guide_plan.json)).

**Next step, not run here.** The cloud session has no GPU, so the take still has to run on the
RTX 3060 Ti. [`run_take.py`](scripts/run_take.py) is the Union `render.py` recipe with the same
seed (20261004), adapter, identity opening and two stages. Only two things change: the guides,
and one prompt sentence on constant arm length ([prompt](run2/prompt.txt)). Its result is
therefore a controlled comparison with Union take 1. To run it:
1. Copy [`comfy_rig_pilot_nodes.py`](scripts/comfy_rig_pilot_nodes.py) into `ComfyUI/custom_nodes`
   and restart the server.
2. Run `python run_take.py take_1`.

The script is untested. Its cap is two takes, counting failures (`DL-MOT-16`). The takes count
against the 2026-10-07 wave handoff's brief, not a new budget. Measure the result with
`measure_wave.py` (W2, plus W3 on annotated joints) before owner review.

## Reproduce

```text
python -I scripts/track_ltx.py      # take-1 numbers -> data/take1_tracks.json
python -I scripts/solve.py          # rig pose -> data/rig_pose.json
python -I scripts/build_parts.py    # run 1 parts, meshes, weights -> run1_godot/
godot --headless --import --path run1_godot
godot --headless --path run1_godot -s res://tools/build_rig.gd
xvfb-run godot --path run1_godot --rendering-method gl_compatibility -s res://tools/render_frames.gd -- <abs>/run1/frames
python -I scripts/render_guides.py  # run 2 guides
python -I scripts/review.py         # measurements and review videos
```

The [manifest](manifest.json) lists every packet file with its SHA-256. The
[job card](JOB_CARD.md) records the brief, limits and review lanes, and the
[impact record](../../../design/audit_impacts/claude-rig-pilot-20261007.json) records the rules
and gates. `ARCHIVE_COMPLETE`, `GENERATION_READY` and `DELIVERY_ACCEPTED` stay separate; none is
claimed for a delivered wave.
