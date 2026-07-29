# Opening cinematic full-frame regeneration process audit

Date: 2026-07-29

## Owner rule and scope

The production target remains the current polished 2D storybook
image-generation style. This trial did not use sprites, tweening, optical flow,
morphing, cross-dissolves, frame duplication, rig animation, subject
translation, or chroma compositing in delivered pixels.

The only non-production visual aid was `POSITION_GUIDE_ONLY`: a flat chroma
footprint or coordinate mark on a neutral field. It supplied position evidence
to the generator and was never inserted into an accepted frame.

This is a process proof for the opening airplane flight, not a finished
five-second master.

## Result

Four consecutive, unique full-frame generations (timeline frames 0–3) are the
last fully accepted sequence:

| Frame | Measured nose edge at native width 1672 | Step |
|---:|---:|---:|
| 0 | 684 | — |
| 1 | 698 | +14 |
| 2 | 715 | +17 |
| 3 | 727 | +12 |

The plane remains on-model, continues screen-right without reversal, and has
negligible cross-axis drift. The strict frame-regeneration report passes with
zero errors. The 24 fps four-frame OGV proof has:

- median adjacent-frame delta: 3.1334 at 320×180;
- mean pixels changing by more than eight luminance levels: 4.54%;
- near-hold ratio: 0%;
- candidate cuts: 0; and
- no duplicated delivery frame.

The 8% anti-boil target passes in this short window, but four frames are too few
to approve the complete action.

Frame 4 is not accepted. Forty-seven retained frame-4 candidates demonstrated
stationary, reversal, overshoot, and scale-growth modes. The initial
correction-guide result reduced an x=758 overshoot to x=749, then bracketed the
x=741 target at x=733 and x=783. A later no-guide batch collapsed to x=726 or
jumped to x=751–753. A new neutral-field bounding-box guide produced a first
x=755 result, then grew and overshot the plane as far as x=801. Its calibrated
correction batch returned x=712/726 reversals and stalls or x=756/762
overshoots. None landed inside the full motion, altitude, and scale tolerance.
The audit prevented those visually plausible images from silently entering the
sequence.

Across the complete working pool, 104 candidate images are retained under the
ignored build tree. This remains below the owner-authorized ceiling of 200
attempts. Continuing blind sampling after the repeated frame-4 modes would not
be evidence-led.

## Review artifacts

- `build/cartoons/opening_first5_fullframe_v4/accepted/`
- `build/cartoons/opening_first5_fullframe_v4/accepted_sequence_manifest_strict.json`
- `build/cartoons/opening_first5_fullframe_v4/accepted_sequence_audit_report_strict.json`
- `build/cartoons/opening_first5_fullframe_v4/opening_first5_strict_partial_4f_24fps.ogv`
- `build/cartoons/opening_first5_fullframe_v4/opening_first5_strict_partial_4f_24fps.mp4`
- `build/cartoons/opening_first5_fullframe_v4/opening_first5_strict_partial_4f_24fps_analysis.json`
- `build/cartoons/opening_first5_fullframe_v4/strict_partial_contact_sheet.png`

These remain review artifacts under `build/`; none is approved for runtime
`assets/`.

## Audit-tool successes

1. **Method enforcement worked.** The manifest accepts only
   `full_frame_image_generation`, rejects forbidden temporal techniques, and
   requires `temporal_derivation: none`.
2. **Evidence is hash-bound.** Candidate, prompt, accepted neighbor, generation
   reference, guide, and mask hashes are verified before artistic metrics are
   considered.
3. **Guide authority is explicit.** Generation references carry roles and
   `used_as_delivery_pixels: false`. Candidate-to-guide mean delta and exact
   pixel reuse checks make accidental guide delivery visible.
4. **Plane tracking is materially better.** Purple-outline segmentation avoids
   the earlier cloud-merging failure, and a nose-region leading-edge anchor is
   more stable than full visible-bounds center tracking while the plane enters
   from offscreen.
5. **Motion is signed and sequential.** The tool now measures direction, actual
   step versus guide step, and cross-axis displacement. It rejects reversal,
   stalls, overshoot, and vertical jitter instead of reporting only unsigned
   distance.
6. **Scale drift is no longer invisible.** Consecutive candidate-mask bounding
   height is recorded and gated, catching gradual zoom or shape growth that a
   nose coordinate alone would miss.
7. **Canvas normalization is honest.** Native generated frames and hashes are
   preserved while whole-canvas delivery normalization is declared separately.
   Subject-specific resizing or repair is still forbidden.
8. **Pre-generation provenance is available.**
   `tools/create_cinematic_regeneration_job.py` writes and hashes the prompt and
   both references before a call, preventing retrospective prompt invention.
9. **The tool failed safely.** Frame 4 did not pass merely because individual
   candidates looked attractive. This is the most important success of the
   redesign.

## Audit-tool failures and blind spots

1. **The mask extractor is shot-specific.** Purple-outline segmentation works
   for this plane but is not a general subject tracker. A subject without the
   lavender contour needs a different evidence path.
2. **Identity and topology remain human-scored.** The tool verifies that scores
   exist and meet the floor but cannot independently prove window count, shell
   design, cockpit topology, perspective, or painterly identity.
3. **Position-guide non-reuse is only a pixel test.** Low exact-pixel reuse does
   not prove that a generator ignored guide styling semantically. Neutral-field
   guides reduce this risk but do not eliminate it.
4. **Pre-generation jobs are not yet mandatory in schema V1.** Early accepted
   frames have prompt artifacts, but frame 0 predates the job writer and lacks
   complete prompt provenance. A retrospective job would be misleading and was
   not fabricated.
5. **The report can be bound to the wrong timing authority.** The strict
   manifest was validated against the 18 fps source OGV for frame-index bounds,
   while the partial proof is 24 fps. The tool reports this correctly but does
   not yet require one exact target-sequence identity and cadence.
6. **No candidate-pool optimizer exists.** Sequence-level path selection was
   manual. A locally closest frame can make the next state impossible, as the
   competing frame-3 branches demonstrated.
7. **No automatic guide calibration exists.** A footprint guide produced
   stationary and overshoot modes; a marker-only guide overshot even more.
   Red/green correction guides improved one branch but did not converge
   reliably. A bounding-box-only guide briefly narrowed the error, then caused
   scale growth, larger overshoots, reversals, and stalls.
8. **Full-frame boil remains coarse.** Whole-frame change includes intended
   plane motion and painterly background redraw. Static-region masks are still
   needed to isolate background instability.
9. **Four frames cannot prove 24 fps playback quality.** Normal-speed review,
   half-speed review, Godot playback, and Lenovo Tab M11 evidence remain open.

## Recommendations

### Before further generation

1. Introduce `cinematic-frame-regeneration-v2` and require a pre-generation job
   for every candidate: exact target timeline, target fps, prompt hash, accepted
   adjacent frame hashes, guide hash, model/run ID, and attempt ID.
2. Bind the audit to the exact target frame sequence or review master rather
   than using a different source video only for frame-count bounds.
3. Add a candidate-pool solver that minimizes, over a whole window:
   signed step error, step acceleration, cross-axis motion, bounding-height
   drift, identity review penalty, and absolute guide error. Do not greedily
   accept the closest current frame.
4. Enforce a bounded branch policy: sample a small pool, retain distinct valid
   states, and expand the strongest sequence paths. After two batches repeat the
   same position modes, branch from a different accepted state instead of
   spending dozens of identical retries.

### Improve controllability without changing the final medium

5. Prefer an image-generation interface that accepts an explicit layout box or
   spatial-control channel while still returning a new complete flattened
   frame. The control input may guide position; it must never become delivered
   pixels.
6. Keep the accepted prior full frame as the sole appearance authority. Use
   neutral-field position guides only, and record marker-only or correction
   variants as experiments until measured candidate pools prove they help.
7. Add automatic rejection for window-count changes, cockpit/shell landmark
   drift, and plane-height changes before human review.

### Expand the audit

8. Add per-shot static-region masks and camera compensation for background
   boil.
9. Produce first/middle/final identity contact sheets and overlay nose,
   cockpit, emblem, and wing landmarks automatically.
10. Require normal-speed, half-speed, frame-step, Godot, and target-device
    review before a five-second window can be called satisfactory.

The production phase remains unchanged: accepted delivery frames are complete
image-generation outputs in the current style. The work that needs further
redesign is spatial control, candidate-path selection, and audit coverage.
