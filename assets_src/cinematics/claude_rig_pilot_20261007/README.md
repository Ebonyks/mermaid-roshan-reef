# Roshan deterministic-rig pilot: LTX motion onto a fixed rig, two runs (2026-10-07)

**Run 1 revision 2 `EXECUTION_PASS / OWNER_REJECTED`. Run 2 `EXECUTION_PASS (8 of 8 takes) / OWNER_REVIEW_PENDING`;
best candidate `g1_slowwave`. Cosmetics on clips `PIPELINE_PASS (all 8 takes) / OWNER_REVIEW_PENDING`.**
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
| **2, takes: start here** | [a2 / e1 / f1 / g1 / g1 in the party dress, game cells at 2x](run2/comparison.mp4) | each take's `clip/cells` and `clip/atlas.png` |
| 2, best candidate g1 | [guide / take / Union take 1](run2/g1_slowwave/review.mp4); [outfits](run2/g1_slowwave/clip/cosmetics_review.mp4) | [native frames](run2/g1_slowwave/refined_frames), [game cells](run2/g1_slowwave/clip/cells), [outfit atlases](run2/g1_slowwave/clip/outfits) |
| 2, other takes | `run2/<take>/review.mp4` and `run2/<take>/clip/cosmetics_review.mp4` for a1, a2, c1, d1, d2, e1, f1 | `run2/<take>/refined_frames`, `run2/<take>/clip` |

All videos are 41 frames at 24 fps (1708 ms). H.264 copies are lossy; PNGs are authoritative.

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
`DL-MOT-16`). It unloads the models after 30 idle minutes. It runs ComfyUI graphs only. All 8 takes
are now spent. The first submission of a1 and a2 was refused before any GPU work: the connected-folder
copy adds a C2PA content-credentials chunk to PNGs, so the bytes on the PC differ while the pixels match.
Those refusals are not takes. Jobs now carry the hash of the copy actually on the PC, after a pixel check
against the source (`make_jobs.py --device-copies`).

[`make_jobs.py`](scripts/make_jobs.py) writes the [jobs](jobs). Each keeps the Union take-1 recipe:
seed 20261004, adapter, identity opening, both stages.

| Job | Change from Union take 1 | Purpose |
|---|---|---|
| `a1_rigguides` | Rig guides, plus one arm-length sentence ([prompt](run2/prompt.txt)) | Controlled test: do proportion-locked guides stop the size and arm changes? |
| `a2_endlock` | a1, plus the opening image locked again at frame 40, plus a finger-separation sentence in place of "Clean connected fingers" | Loop closure (W5) and hand smear |
| `c1_acting` | a2 on run-3 guides: whole-body acting on the wave's timing (lift, lean, head tilt, counter-swings, hair wave, bob), smoothed arm, blink; an acting sentence | Owner: the figure must move as a whole, blink, hair flow |
| `d2_occlude` | a2 on run-4s guides: the waving arm drawn in front (hair, face and body lines under it removed), body still | Does occlusion stop the hand smear? |
| `d1_act_occl` | c1 on run-4 guides: acting plus occlusion, one closed-eye frame | c1's long blink |
| `e1_outward` | Run-5 guides on an opening image moved 40 px right: the hand goes out and up at her side, waves twice at the top, returns the same way | Keep the fast hand off the face |
| `f1_sidewave` | Run-6 guides: a side wave whose hand never crosses her hair, face or body; eyes open, no blink request | e1 still crossed the hair; blink requests shut the eyes |
| `g1_slowwave` | f1 on run-7 guides: same path, a third less peak hand speed, one wave at the top | f1's fastest frames still smeared |

[`process_take.py`](scripts/process_take.py) brings a finished take home and takes these steps:
- It checks the receipt hashes.
- It tracks the arm, seeded from the rig guide, and runs `measure_wave.py` for W2 and W3.
- It compares the end frames with K0.
- It runs the cosmetics pipeline below and writes `run2/<job>/review.mp4`.
- It counts the frames where the lids cover most of the iris ([`eye_openness.py`](scripts/eye_openness.py)).
- With `--grade` it matches the clip's colour to K0 once for the whole clip (below).

### Guides for runs 3 to 7

[`render_guides_acting.py`](scripts/render_guides_acting.py) keeps run 2's contours and the rig arm at
the W3 lengths. It moves the whole outline by rigid region turns: lift, lean about the waist, head tilt,
shoulder lift, free-arm and tail counter-swings, a wave through the hair, a buoyant bob. Frames 0 and
40 stay exactly the K0 guide. `--occlude` removes every line inside the waving arm's outline, so the
arm reads as in front. The arm paths:

| Guides | Arm path | Script |
|---|---|---|
| run3, run4, run4s | The revision-2 path: the hand passes in front of the hair and face on the way down | `render_guides_acting.py` (run4s: `--still`) |
| run5 | The revision-2 rise played forward and back, two waves at the top; figure 40 px right | [`animate_run5.py`](scripts/animate_run5.py) |
| run6 | A side wave: rise in front-left with the elbow out to a top pose beside the head, two waves, back the same way. The forearm and hand stay at least 5 cell px outside the K0 head, hair and body in every frame (6.6 px measured), fingertip at canvas x ≥ 45 | [`animate_run6.py`](scripts/animate_run6.py) |
| run7 | run6's path, rise 3 to 15 and lowering 23 to 35 at constant speed with 3-frame ramps; peak fingertip speed 15.1 instead of 20.1 cell px per frame; one wave | `animate_run6.py --run7` |

Runs 5 to 7 shift the opening image and guides 40 canvas px right
([`run5/identity_shift40.png`](run5/identity_shift40.png)); scripts that read those takes run with
`PILOT_CANVAS_SHIFT_X=40`, so the cells map back to the same 256 px cell.
Re-rendering all six guide sets with the commands under Reproduce gives byte-identical files (738 of 738).

### Run 2 results

Eight takes, 6 to 19 minutes each, peak 7,808 MiB sampled on the 8 GB card. Game cells and measurements per take are
in `run2/<take>/summary.json`. "Arm" is upper arm plus forearm from the silhouette fit against the
contract's 50 cell px; the fit is loose on blurred frames, so read it as a range, not a per-frame
measurement. "Eyes" lists the frames where the lids cover most of the iris.

| Take | Guides | W2 figure / head (limit 1.0% / 2.0%) | Arm | Eyes | Hand (Claude's frame review) | Body |
|---|---|---|---|---|---|---|
| a1 | run2 | 0.13% / 0.31% | −31.9% to +10.8% | open | Smudged where it crosses the hair and face, about 8 to 10 and 24 to 29 | Nearly still |
| a2 | run2 + end lock | 0.05% / 0.26% | −9.5% to +13.7% | open | The same crossings, 24 to 27 the worst; least texture boil | Nearly still |
| c1 | run3 | 0.97% / 0.88% | −8.8% to +20.6% | **closed 25 to 36** | Smudged 24 to 30 | Moves as a whole; bodice turns 1.75° |
| d2 | run4s | 0.00% / 0.12% | −31.3% to +11.7% | open | Occlusion alone did not stop the smudge | Still (by design) |
| d1 | run4 | **1.03%** / 0.82% | −12.4% to +15.5% | **closed 25 to 35** | Smudged 26 to 30 | Moves as a whole |
| e1 | run5 | 0.52% / 0.46% | −9.6% to +22.7% | **closed 12 to 37** | Crisp at the top; smudged where it passes the hair, about 8 to 11 and 27 to 31 | Moves as a whole |
| f1 | run6 | 0.65% / 0.69% | −26.1% to +18.9% | open | Crisp through both waves (13 to 25); soft in the fastest frames, about 9 to 11 and 28 to 30 | Moves as a whole |
| **g1** | run7 | 0.63% / 0.74% | −1.9% to +22.0% | open | Crisp through the wave (12 to 24); still a soft grey blob in about 8 to 11 and 25 to 31 | Moves as a whole; bodice turns 1.76° |

What the takes show:
- **Size holds.** Every take keeps W2 except d1, which misses the figure limit by 0.03%. The rig guides
  hold the arm far better than Union take 1's guides (−52% to +27%), but no take proves W3 per segment.
- **Hands smear when they move fast over detail.** LTX-2.5 packs 8 frames into each latent frame, and
  at 320x448 the hand is about one latent token. A hand moving across the hair or face inside one
  group comes out as a smudge (a1 to e1). Keeping the hand outside the hair and face (f1, g1) makes the
  wave itself crisp. The remaining soft frames are the fastest rise and lowering frames, and cutting
  the peak speed by a quarter (g1) did not remove them.
- **Blink requests close the eyes for too long.** Every take that asked for a blink (c1, d1, e1) shut
  her eyes for 11 to 26 frames, even with a one-frame request. The takes that did not ask kept them
  open. There is still no approved front-facing closed-eye drawing to lock as a keyframe.
- **The whole body moves together** once the guides move it (c1 onward): lean, head tilt, hair and
  tail on one timing, with no part layers.
- **Colour.** LTX renders the figure about 6 levels darker than K0. `--grade` fits one per-channel
  gain and offset to the opaque interior of frames 0 and 40 and applies it to every cell, so the clip
  does not pop when the game swaps the still sprite for it. g1's cells are graded: frame-0 colour
  error 16.2 to 15.0 levels (the round trip of K0 alone through the opening image is 9.6).

**g1 is the best candidate** (game cells at [run2/g1_slowwave/clip](run2/g1_slowwave/clip)): constant
size, the whole body moving, eyes open, a crisp wave, frames 0 and 40 back at K0's silhouette
(IoU 0.97). It is not deliverable as it stands, for two reasons:
- **Hand.** About 11 frames show a soft grey hand on the way up and down.
- **Blink.** The owner asked for a blink, and g1 has none.

The 8-take budget is spent; further takes need the owner. Candidate next methods, untested:
- A plain mitten outline for the moving hand in the guides.
- A longer clip (more frames for the rise).
- An owner-approved closed-eye K0 drawing from Codex, used as a keyframe at the blink.
- The gated Refine Details IC-LoRA, which needs the owner's HuggingFace access.

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

The same pipeline ran on all eight run-2 takes, including the five whose whole body leans and bobs
([summaries](run2), `cosmetics` and `bodice_*` keys):

| Takes | Frames dressed (each outfit) | Clothing area spread | Drift on the bodice | Bodice travel / turn | Slip |
|---|---|---|---|---|---|
| a1, a2, d2 (body nearly still) | 41/41 | ≤ 2.6% | ≤ 0.44 px | ≤ 0.3 px / ≤ 0.46° | ≤ 0.3 px |
| c1, d1, e1, f1, g1 (whole body moves) | 41/41 | ≤ 3.5% | ≤ 0.88 px | ≤ 3.2 px / ≤ 1.85° | ≤ 0.66 px |

In g1's party-dress atlas the dress stays on the bodice through the lean and bob, and the waving arm
stays in front of it.

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
python -I scripts/render_guides_acting.py --out run3   # run4: --occlude --blink quick; run4s: --occlude --still
PILOT_CANVAS_SHIFT_X=40 python -I scripts/animate_run5.py          # run-5 pose
PILOT_CANVAS_SHIFT_X=40 python -I scripts/animate_run6.py [--run7] # run-6 / run-7 pose
PILOT_CANVAS_SHIFT_X=40 python -I scripts/render_guides_acting.py --occlude --pose data/rig_pose_run7.json --out run7  # same for run5, run6
python -I scripts/make_jobs.py <job> --device-copies <ltx25/input staged back from the PC>
[PILOT_CANVAS_SHIFT_X=40] python -I scripts/process_take.py <job> <staged results/rig_pilot/<job>> --guide-set <runN> [--grade] --godot <4.7.2>
python -I scripts/compare_takes.py  # run2/comparison.mp4
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
