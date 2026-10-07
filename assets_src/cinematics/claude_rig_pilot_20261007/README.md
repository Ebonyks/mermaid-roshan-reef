# Roshan deterministic-rig pilot: LTX motion onto a fixed rig, two runs (2026-10-07)

**Run 1 revision 2 `EXECUTION_PASS / OWNER_REJECTED`. Run 2 `GUIDES_READY / TAKES_QUEUED_ON_PC`.
Cosmetics on clips `PIPELINE_PASS / OWNER_REVIEW_PENDING`.**
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
| 2026-10-07 | On run 1: "This is acceptable as a rough take, but mermaid roshan is frozen otherwise. Give her a full body natural movement that accompanies the hand raise, have her blink, make her hair flow slightly in the water. It's progress" and "There are also a lot of frame-by-frame artifacts present currently". | `ODR-RIG-PILOT-REV2-20261007` |
| 2026-10-07 | On revision 2: "No, these are failures. there are overdraw errors, the figure doesn't move as a whole, there are some rough crop issues as well. analyze potential solutions, including the old protocols" | `ODR-RIG-PILOT-REV2-REJECTED-20261007` |
| 2026-10-07 | "Continue, trial methods until satisfied" | `ODR-RIG-PILOT-TRIALS-20261007` |
| 2026-10-07 | "Also, in this process, Insure that cosmetics, like new clothes, will still work with the animation process, this is critical" | `ODR-RIG-PILOT-COSMETICS-20261007` |

The rules set aside for run 1 only: `ODR-ROSHAN-WHOLE-FRAME-20261005`, `ODR-SPRITE-WHOLE-UNIT-20261007`,
the CLAUDE.md rule that Roshan has no rig or skeleton, and the written-handoff rule. They stay
binding for production and for run 2.

## Watch

| Run | Review video | Authoritative frames |
|---|---|---|
| 1, rules off, revision 2 | [LTX take 1 / revision 1 / revision 2, same scale](run1_rev2/review.mp4) | [run1_rev2/frames](run1_rev2/frames) (512 px = 2 x cell) |
| 1, rules off, revision 1 | [LTX take 1 / Godot rig, same scale](run1/review.mp4) | [run1/frames](run1/frames) |
| 2, rules back | [Union guide / rig guide / LTX take 1](run2/review.mp4) | [run2/guide_full](run2/guide_full), [half](run2/guide_half), [quarter](run2/guide_quarter) |
| Cosmetics on a clip (Union take 1) | [base / ribbon / party / garden / disguise](cosmetics/union_take1/cosmetics_review.mp4) | [outfit atlases](cosmetics/union_take1/outfits), [base atlas](cosmetics/union_take1/atlas.png) |

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

## Run 1 revision 2: whole body, blink, hair (owner review 2026-10-07)

The owner called revision 1 "acceptable as a rough take" but frozen, with frame-by-frame artifacts.
The measurements agreed:
- **Frozen body.** The body copied LTX's own body motion, which is noise-level.
- **Jitter.** The arm kept the smeared LTX frames' jumps: up to 76°/frame² of acceleration and nine
  direction reversals.
- **Edge artifacts.** The sleeve overlay carried hair pixels, which cut the hair at the shoulder
  once the head moved. The arm's removal left the bodice without a contour, and stray specks rode
  along with the arm.

Revision 2 ([`animate_rev2.py`](scripts/animate_rev2.py), [rig_pose_rev2.json](data/rig_pose_rev2.json))
keeps LTX for what it measured well (the arm's path and timing) and authors the rest on that
timing:

| Layer | What it does | Range |
|---|---|---|
| Arm | Revision-1 IK angles through an IoU⁴-weighted smoothing spline, ends eased to K0 | max acceleration 6.9 / 13.0 / 8.9 °/frame² (was 31 / 76 / 39) |
| Acting on one master phase (arm elevation), 1 to 5 frame overlapping-action lags | Anticipation dip, body lift, lean away from the raised arm, head tilt toward the hand, shoulder lift, free-arm counter-swing, tail counter-swing and fin follow-through | torso −0.2° to 2.2°, head −5.1° to 1.4°, free arm −3.8°, root ±0.4 / −1.7 to 1.1 cell px |
| Underwater idle, one 40-frame cycle | Buoyant bob, tail undulation, a travelling wave through a new three-bone rainbow-hair chain and the left strands | hair tip −4.0° to 6.5°, fin −4.5° to 2.0° |
| Blink | Half lid frame 33, closed 34 and 35, half lid 36 | painted overlays (below) |

Rig fixes in [`build_parts.py`](scripts/build_parts.py):
- **Hair and sleeve.** Hair-coloured pixels stay in the skinned body instead of the sleeve
  overlay, and the rainbow hair is weighted by its own region, so it hangs free over the
  shoulder.
- **Shoulder.** The pivot moved 3.5 px up, inside the sleeve, so the arm's top never swings out
  from under it.
- **Contours.** The bodice contour and sleeve hem are closed in K0's outline colour where the arm
  used to cover them. Stray specks are gone.
- **Mesh.** The body mesh is denser: 2,215 vertices with a 3 px grid.

The rest composite now differs from K0 in 40 pixels, all closed contour and hem pixels.

**Blink art.** No approved front-facing closed-eye drawing exists; all six closed-eye cells in the
atlases are tilted or turned heads. The half-lid and closed overlays are painted on K0's own eyes
for this pilot only:
- the covered eye is refilled with K0's own skin colour, row by row;
- each lid is a single lash line in K0's lash colour, with a flick at the outer corner.

The blink is pending Codex and owner review as production art.

| Check | Result |
|---|---|
| `measure_wave.py` on the Godot render, joints read from Godot's own bone transforms ([run1_rev2_measure.json](data/run1_rev2_measure.json)) | **PASS**: figure 0.3%, head 0.67% peak-to-peak (rotation and blink, no scale anywhere in the rig); arm −3.9% / +4.1% / 0.0% |
| Godot keys reproduced | max error 0.000000 rad over 41 frames |

The run-1 shortfalls about rule conflicts still stand: part layers and a hand swap. Revision 1
frames remain as evidence; reproduce them from commit `e9eb0e87`.

**Owner review: rejected** (`ODR-RIG-PILOT-REV2-REJECTED-20261007`): overdraw errors, the figure
does not move as a whole, and rough crops. These are structural to a cut-out rig: parts overlap
where they meet, each part turns about its own pivot, and moving the arm uncovers body pixels the
drawing never had. Run 1 is closed as evidence; the rig now only authors guides (run 2).

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

### Running the takes on the RTX 3060 Ti

The cloud session has no GPU and cannot type into terminals on the PC. Instead, the owner starts
[`start_rig_pilot_runner.bat`](pc_runner/start_rig_pilot_runner.bat) once, and Claude passes job
files through the connected `ltx25` folder. [`rig_pilot_runner.py`](pc_runner/rig_pilot_runner.py)
works as follows:
- It starts the isolated ComfyUI core (port 8194, the Union trial's arguments plus the
  [`mermaid_rig_pilot`](pc_runner/mermaid_rig_pilot/__init__.py) guide loader).
- It checks the SHA-256 of every input.
- It accepts only allow-listed node classes and save paths.
- It copies frames and latents back with a receipt.

The runner stops at 8 takes, counting failures (`ODR-RIG-PILOT-TRIALS-20261007`, bounded under
`DL-MOT-16`). It unloads the models after 30 idle minutes. It runs ComfyUI graphs only.

[`make_jobs.py`](scripts/make_jobs.py) writes the [jobs](jobs). Each keeps the Union take-1 recipe:
seed 20261004, adapter, identity opening, both stages.

| Job | Change from Union take 1 | Purpose |
|---|---|---|
| `a1_rigguides` | Rig guides, plus one arm-length sentence ([prompt](run2/prompt.txt)) | Controlled test: do proportion-locked guides stop the size and arm changes? |
| `a2_endlock` | a1, plus the opening image locked again at frame 40, plus a finger-separation sentence in place of "Clean connected fingers" | Loop closure (W5) and hand smear |

[`process_take.py`](scripts/process_take.py) brings a finished take home and takes these steps:
- It checks the receipt hashes.
- It tracks the arm, seeded from the rig guide, and runs `measure_wave.py` for W2 and W3.
- It compares the end frames with K0.
- It runs the cosmetics pipeline below and writes `run2/<job>/review.mp4`.

## Cosmetics: the game outfits on an animation clip

The owner made this critical (`ODR-RIG-PILOT-COSMETICS-20261007`). The game dresses Roshan by
baking each outfit (ribbon, party, garden, disguise) into a copy of every atlas. The builder is
[`tools/build_fashion_outfits.gd`](../../../tools/build_fashion_outfits.gd), and it reads one
bodice box per 256 px cell from
[`pose_fit.json`](../../fashion_designer/party_garment_v1/pose_fit.json). The swim cycles already
work this way. A whole-frame animation clip is one more atlas, so outfits reach every animation
frame through three steps:
1. **Game cells.** [`clip_cells.py`](scripts/clip_cells.py) mattes each whole take frame and maps
   it back to the approved 256 px cell. One uniform 2.5 px edge erosion removes the opening
   image's upscale spread. Frame 0 matches K0's silhouette at IoU 0.975, up from 0.935.
2. **Clothing fit per frame.** [`clip_pose_fit.py`](scripts/clip_pose_fit.py) keeps K0's bodice box
   size on every frame and moves the box with the tracked neck and waist. This way the dress
   never changes size. Per-cell measured boxes, as the static atlases use, would make it breathe.
3. **The production builder.** It has one new option, `-- --fit=<json> --out=<dir>`. With that
   option it bakes the same outfits onto any clip atlas and leaves the game outputs untouched.
   [`bake_clip_outfits.sh`](scripts/bake_clip_outfits.sh) runs it in a throwaway project.
   Without the option, the builder's 56 game outputs are byte-identical to the unmodified builder
   (Godot 4.7.2, same machine).

Test on real generated frames, Union take 1
([review](cosmetics/union_take1/cosmetics_review.mp4): base | ribbon | party | garden | disguise;
[report](cosmetics/union_take1/cosmetics_report.json)):

| Outfit | Frames dressed | Clothing area spread | Drift on the bodice |
|---|---|---|---|
| Ribbon | 41/41 | 0.0% | 0.00 px |
| Party dress | 41/41 | 0.3% | 0.05 px |
| Garden | 41/41 | 2.3% | 0.35 px |
| Disguise | 41/41 | 0.8% | 0.18 px |

The wave's arm and hands stay in front of the dress, because the builder restores skin over the
garment. Take 1's body barely moves: the bodice travels 0.28 px and turns 0.5°. The rig-guided
takes lean and bob, so they test the fit harder.

Two limits remain. The garment snaps to whole pixels, so up to 0.5 px of slip is reported per
frame. The garment also does not turn with the torso. If a take leans more than about 2°, the
next step is an optional angle in the fit, still in the same builder.

None of these outfit clips are runtime assets.

## Reproduce

```text
python -I scripts/track_ltx.py      # take-1 numbers -> data/take1_tracks.json
python -I scripts/solve.py          # rig pose -> data/rig_pose.json
python -I scripts/animate_rev2.py   # run 1 revision 2 pose -> data/rig_pose_rev2.json
python -I scripts/build_parts.py    # run 1 parts, meshes, weights, blink overlays -> run1_godot/
godot --headless --import --path run1_godot
godot --headless --path run1_godot -s res://tools/build_rig.gd
xvfb-run godot --path run1_godot --rendering-method gl_compatibility -s res://tools/render_frames.gd -- <abs>/run1_rev2/frames
python -I scripts/render_guides.py  # run 2 guides
python -I scripts/review.py         # measurements and review videos
python -I scripts/make_jobs.py      # run 2 job files -> jobs/ (copied to the PC runner's queue)
python -I scripts/process_take.py <job> <staged results/rig_pilot/<job>> --godot <4.7.2>
python -I scripts/clip_cells.py ../ltx25_union_trial_20261004/take_1/refined_frames/%04d.png cosmetics/union_take1
python -I scripts/clip_pose_fit.py cosmetics/union_take1 roshan_wave_union_take1
GODOT=<4.7.2> scripts/bake_clip_outfits.sh assets_src/cinematics/claude_rig_pilot_20261007/cosmetics/union_take1
python -I scripts/cosmetics_review.py cosmetics/union_take1 roshan_wave_union_take1
```

The [manifest](manifest.json) lists every packet file with its SHA-256. The
[job card](JOB_CARD.md) records the brief, limits and review lanes, and the
[impact record](../../../design/audit_impacts/claude-rig-pilot-20261007.json) records the rules
and gates. `ARCHIVE_COMPLETE`, `GENERATION_READY` and `DELIVERY_ACCEPTED` stay separate; none is
claimed for a delivered wave.
