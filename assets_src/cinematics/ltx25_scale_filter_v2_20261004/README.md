# Roshan scale filter correction, v2

Status: `REJECTED_REFERENCE_ONLY`. This is a deterministic correction of the
existing fifth LTX-2.5 take, with **zero additional model takes or ImageGen calls**.
The preceding five-take/one-key generation caps remain exhausted.

## Owner correction

Owner, 2026-10-04: “Problem is still present, if improved. We were able to fix this
same issue in the previous grok handoffs, and i'm unsure why we're struggling here.”
The prior direction requires static world size and Aseprite continuity filtering
at multiple corresponding figure anchors. This packet records the correction;
it does not establish owner acceptance of the animation.

## What went wrong

The v1 filter skipped correction whenever an anatomy fit failed. Failed spans
therefore returned to native size/position in the same review clip. Its scale was
also rounded to multiples of 1/64, creating 1.5625% size steps (about12px over a
750px figure). Equal canvas dimensions and Aseprite anchor metadata do not impose
a constraint on an LTX sampler receiving PNG guides.

Both filter errors are repaired here. Every one of41 frames uses its own single
continuous uniform scale and translation, sampled once from its preserved native
frame inside Aseprite. Anatomy status never bypasses that transform. No body-part
warp, copied neighbor pixels, repeated action frame, temporal interpolation or
additional generation is used. Failed anatomy stays visible and marked.

## What the earlier Grok work contributes

- The [master formula](../../../design/GROK_MASTER_HANDOFF_FORMULA_2026-08-30.md)
  establishes canonical identities, relative scale and an approved complete
  first-frame layout before a bounded motion job.
- The [continuity protocol](../../../design/GROK_HANDOFF_2_CONTINUITY_PROTOCOL_2026-09-09.md)
  checks fixed scene landmarks, subject bounds and camera/scale drift in normalized
  coordinates. A prompt alone is insufficient.
- The [Chapter2 scale contract](../chapter2_lawn_scale_v2_2026-09-06/SCALE_CONTRACT.json)
  fixes shared-plane display heights and prop ratios while retaining art proportions.
  That packet is planning evidence, not proof of a delivered accepted clip.
- [Roshan's Grok opening builder](../../../tools/aseprite/roshan_grok_openings.lua)
  performs one common uniform source scale and placement before motion.
- The [DayOne return audit](../../../tools/build_day_one_grok_regeneration_handoffs.py)
  records `D1-C01-S03` as `ACCEPT_MOTION_REFERENCE`, specifically including stable
  scale. Its acceptance is scoped to motion reference, not a final cinematic audit.

The transferable method is common staging followed by verification of the actual
result. LTX timed guides are soft conditioning; they do not guarantee exact pose,
size or anatomy at the requested frame. This study had also independently redrawn
a missing key, adding an identity/proportion risk that global registration cannot
remove. The v2 filter fixes its implementation bugs without claiming model errors
have disappeared.

## Measured result

| Check | Raw fifth take | Faulty v1 | Continuous v2 |
|---|---:|---:|---:|
| Maximum waist/root error |9.29px|8.28px|0.80px|
| Maximum residual global scale correction |2.40%|1.53%|0.28%|

All41 v2 exports meet the declared **1px root /0.3% global residual** limits.
Internal geometry still fails on **12–15 and22–24**. The five landmarks (crown gem,
both eyes, neck base and waist) diagnose head/torso registration; they do not prove
full tail anatomy. The remaining head/torso proportions, tail deformation, fingers,
motion blur, source clipping and loop seam require coherent figure review/repair.
The loop is not accepted for runtime use.

Frame29's dark eyelash touches hair, defeating the broad component detector.
Native inspection established a specific corresponding eye ROI; its coordinates,
threshold and source hash are in [the plan](registration_plan.json). Frame29's hand
was already cut off at the original canvas edge. A constant **24px rightward layout
offset across the whole clip** prevents further clipping; it cannot restore that
missing hand. Every transform preserves the complete native figure proportions.

Actual exported landmarks required one bounded feedback update for10,31,32.
Those three were resampled afresh from their original native frame; the earlier
resample was never used as a rendering source. [Initial evidence](initial_verification.json),
[final checks](verification.json), [comparison metrics](comparison_metrics.json)
and every float transform remain inspectable.

## Watch and inspect

[Corrected global registration review](registered_review.mp4)

[Same-frame comparison](raw_v1_v2_comparison.mp4): **left = raw fifth take,
middle = faulty v1, right = continuous v2**. All three retain indices0–40 at24fps.
The v2 column includes the declared constant stage offset; no column is temporally
substituted. Encoded previews are lossy H.264; PNGs and the master preserve QA pixels.

[Editable41-frame Aseprite master](registered_review.aseprite) contains205 target
anchor slices and41 review tags. All41 reopened exports are pixel-exact. Registration
is applied even to the seven anatomy failures. The PNGs under `frames/` retain native
576×832 output size. The Aseprite millisecond timeline totals1708ms; video clock is
the original41/24 seconds.

## Reproduce and limits

Run `scripts/run.py` with the existing embedded Python environment. It calls Aseprite
for pixel work and FFmpeg for declared encoding only. `scripts/verify.py` reads
images without editing them, checks256 independent affine pixel samples per frame,
native geometry and Aseprite roundtrip. No model server or network generation is
used. Reproduction requires the preceding source packet's hash-bound native frames.

The [manifest](manifest.json) records payload/source hashes and declared transforms.
Anonymous immutable GitHub verification is written separately after publication.
`ARCHIVE_COMPLETE` does not grant `DELIVERY_ACCEPTED`, identity/motion, device or
child acceptance. Runtime and protected originals are unchanged.

For future production, reuse one approved opening and shared scale contract,
register every complete-figure pose before submission, consume actual exported
guides, then separate global registration from anatomy review after decode. Add
pose-aware shoulder, pelvis/tail-junction and lower-body checks rather than claiming
these upper-body anchors lock the full figure. When native internal shape fails,
queue coherent whole-figure redraw/retake spans under a newly commissioned budget;
global scaling is not a substitute for that repair.
