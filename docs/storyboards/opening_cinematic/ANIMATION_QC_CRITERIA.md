# Opening Cinematic Animation QC Criteria

These gates apply to storyboard animatics and to later production animation.
Passing the image-generation prompt is not a quality decision; every shot must
survive the automated pass, full-resolution visual review, and encoded-playback
review.

This document's numerical camera/stutter checks are a **diagnostic animatic
preflight**, not the final release authority. Production acceptance additionally
requires the Codex Temporal Animation Integrity protocol and
`tools/audit_cinematic.py` from the `codex-local-cartoon-video` worktree.

## 1. Shot declaration

Before generating frames, declare:

- camera mode: locked, pan, track, crane, or motivated cut;
- static landmarks used to measure camera motion;
- moving subjects and their intended screen path;
- the beginning, apex, and settled pose;
- continuity constraints inherited from the previous and following shots.

A camera move that is not declared is a defect.

## 2. Hard rejection conditions

Reject and rebuild a frame or shot when any of these appears:

- an unmotivated angle, lens, horizon, crop, or viewpoint change;
- a background landmark moving more than 1% of frame width in a locked shot;
- duplicated faces, limbs, crowns, labels, borders, or transparent ghost poses;
- a hold followed by an unexplained large pose or camera pop;
- a body-scale change greater than 2% for an anchored character;
- a non-monotonic action path, backward step, or extra direction reversal;
- a change to the airplane's seat count, door side, or stair construction;
- a stair that does not open outward from the aircraft and downward;
- a Sky Lagoon landmark changing location, count, or silhouette;
- a frame label, stabilization edge, or interpolation artifact entering picture;
- a duration, frame-count, frame-rate, codec, or pixel-format mismatch.

## 3. Camera stability measurement

For each locked shot, define a static-background region that excludes moving
characters as much as possible. Downsample it to 96x54 and search translations
within +/-3 pixels for each adjacent pair.

Acceptance targets:

- aligned grayscale difference: target <=10, hard ceiling 16;
- camera acceleration RMS: target <=1.5 low-resolution pixels;
- direction reversals: zero when the estimated motion vector is non-zero;
- horizon displacement: <=3 full-resolution pixels;
- no search result repeatedly saturating the +/-3-pixel search boundary.

When character occlusion contaminates the vector estimate, the shot may pass
only if the aligned-difference ceiling passes and a full-resolution landmark
review confirms that the camera itself is stationary. That exception must be
recorded in the audit.

## 4. Motion and stutter measurement

An automatic hold-then-pop flag is raised inside a shot when:

- the preceding aligned difference is <6 and the next is >16; or
- the next difference is >12 and more than 3x the preceding difference.

Every flag requires visual review. It may be classified as an intentional
action accent only when all three are true:

1. the static-background region remains below its discontinuity ceiling;
2. the action advances monotonically along the declared path;
3. there is no camera, scale, anatomy, or silhouette discontinuity.

Otherwise, regenerate an in-between or retime the pose sequence. Do not use a
transparent crossfade to hide a failed pose; double contours are a hard reject.

## 5. Reflexive improvement loop

1. Generate or edit the smallest defective shot group.
2. Extract individual frames mechanically.
3. Run camera, discontinuity, and stutter scans.
4. Review the sheets at full resolution.
5. Encode a review master and inspect difficult transitions in motion.
6. Reject any output that improves a metric but creates a visible artifact.
7. Repeat until the shot passes or record it as a conditional animatic-only
   exception.

Original frames remain available until the replacement passes. Rejected review
encodes are not shipped beside the approved master.

## 6. Delivery gate

The approved storyboard animatic must be:

- exactly 270 frames;
- exactly 12 fps and 22.500 seconds;
- 1280x720 H.264 with YUV420p pixel format;
- silent;
- free of missing, duplicated, or out-of-order source frames.

Motion-interpolated versions are optional review artifacts. They may not replace
the authored 12 fps master unless intermediate-frame inspection shows crisp
single contours at character, stair, and landmark edges.

## 7. External production-quality gate

After the diagnostic preflight, bootstrap and complete the external cinematic
manifest. It requires:

- contiguous declared scenes and shot-aware reviewer overrides;
- a versioned background/layout identifier for every scene;
- a character passport with canonical references and landmarks;
- a sample on every frame for every declared track;
- declared contacts and ownership spans;
- scene scores in construction, identity, motion, contact, style, and
  performance;
- production-wide character identity review; and
- traceable generator, renderer, repair, compositing, and encode provenance.

Non-compensating floors:

- scene criteria: 4.85/5.00 each;
- global character-passport criteria: 4.90/5.00 each.

The Python tool validates the manifest and score floors; it does not replace
human visual authority. A production pass also requires normal-speed,
silent-normal-speed, half-speed, frame-step, onion-skin, contact, and
cross-scene character-passport review.

An MP4 that passes frame count, duration, codec, and the local jitter screen can
still fail production for anatomy, identity drift, unstable contact,
performance, rhythm, scene congruency, or missing human review.

## 8. Named audit profiles

The external tool has two explicit score-floor profiles:

| Profile | Scene criteria | Global character-passport criteria | Meaning |
|---|---:|---:|---|
| `production` | 4.85/5.00 each | 4.90/5.00 each | Blocking release-quality target; default |
| `animatic` | 4.25/5.00 each | 4.50/5.00 each | Story, timing, and editorial review only |

Use the lower profile only when the artifact is labelled as an animatic and
both profile results are retained. A lower-profile pass must never overwrite,
hide, or be described as a production pass.

Example:

```powershell
python tools/audit_cinematic.py opening.mp4 `
  --manifest review_manifest.json `
  --profile animatic `
  --report cinematic_quality_report_animatic.json
```

The strict default remains:

```powershell
python tools/audit_cinematic.py opening.mp4 `
  --manifest review_manifest.json `
  --profile production `
  --report cinematic_quality_report_production.json
```
