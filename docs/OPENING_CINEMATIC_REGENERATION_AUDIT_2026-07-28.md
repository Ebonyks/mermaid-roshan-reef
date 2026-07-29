# Opening Cinematic V2 — Regeneration Result and Audit-Tool Review

Date: 2026-07-28

> **Historical animatic only.** Owner decision 2026-07-29 supersedes the
> pose-reuse, held-frame, layer, inpaint, and compositing production methods
> described below. The required product remains the current polished
> full-frame image-generation style. Defective action frames must now be
> regenerated and accepted individually; the only guide exception is a
> disposable neutral-field chroma position reference that contributes no
> delivery pixels or appearance.

Source OGV SHA-256:
`D01B7B4AB2C24E2AD6626F03007F60C1255ECF507A99BB2D6EF8A4B2CAE8EACE`

Final OGV SHA-256:
`E2A5A2976FB86E147A372F3A1D43D8E2F237EBCD29AB553202CEC66E1AF58345`

Final MP4 SHA-256:
`B2949CCEA0B78819CDC57DEA205C578C9823B5561919CDB08592042F86AF9E64`

## Executive result

The 15-second test was rebuilt as a 42.5-second, 24 fps, 1020-displayed-frame
limited-animation cut. It reuses the existing approved 2D illustrations and
does not call an image generator, create 3D content, alter protected source art,
or synthesize family voices.

The final review artifacts are:

- `build/cartoons/opening_cinematic_v2_final.ogv` — 1280×720 Theora, silent,
  5,953,341 bytes;
- `build/cartoons/opening_cinematic_v2_final.mp4` — 1280×720 H.264, silent,
  11,874,435 bytes;
- `build/cartoons/opening_cinematic_v2_final_frames/provenance.json` — source
  frame, shot, exclusion, and repair provenance; and
- `build/cartoons/opening_cinematic_v2_final_automatic_analysis.json` —
  decoded-delivery automatic evidence.

This is a materially improved review master and a stable V2 animatic. It is not
yet a production-approved in-game cinematic because the human character
passport, contact, scene-performance, and target-device gates remain open.

## Input-audit mismatch

The supplied defect handoff describes an underwater swim/glow film. The actual
movie at the supplied path is the pearl-airplane arrival sequence with Roshan
and Daddy. Its semantic shot descriptions, character callouts, and repair
instructions therefore cannot be applied literally.

Some of the handoff's numeric transition observations align with the source
movie's nine-frame generation lattice, but that agreement is not evidence that
its semantic review is correct. The actual movie was re-inspected and the
repository's V2 direction brief was used as the story and timing authority.

This mismatch is the most important audit-tool lesson: pixel statistics can
look internally consistent while the written interpretation describes the
wrong content.

## What changed in the film

- Expanded the 30 half-second storyboard groups into the approved 18-shot,
  42.5-second rhythm contract.
- Used deliberate held poses with longer anticipation and settle drawings
  instead of replaying every independently redrawn frame.
- Removed source frames 90–98, the prohibited landing-wheel/runway insert.
- Removed source frames 261–269, where the final handhold breaks and Daddy
  waves.
- Locked source frame 260 for the final reveal and hold, preserving Roshan and
  Daddy's joined hands.
- Removed the premature island/castle silhouette from the opening sky.
- Removed production frame-number labels from reused later poses with a soft,
  non-text corner repair.
- Authored the reveal as one deterministic 1.2-second ease-out followed by a
  locked hold.
- Kept the film silent because no new approved family recordings were supplied;
  no protected voice file was cut, stretched, cloned, or repurposed.

## Regeneration attempts

Seven bounded attempts were sufficient; continuing toward the allowed maximum
of 200 would have spent time on the same source-art ceiling rather than improving
the result.

1. Dense pose reuse: acting coverage was highest, but automatic changed-pixel
   coverage remained 10.16%, above the 8% anti-boil target.
2. Sparse pose reuse: changed-pixel coverage fell to 4.60%, but too much acting
   information was lost.
3. Adaptive pose reuse: retained critical hand/rise/stair/reaction poses at
   6.41%.
4. Adaptive plus direction repairs: removed the premature destination and
   production labels.
5. Label inpaint trial: removed text but created an objectionable hard corner
   patch.
6. Quiet–motion–quiet timing: doubled the relative duration of anticipation
   and settle drawings.
7. Final label-feather/master pass: removed text without a rectangular patch
   and produced the delivered OGV/MP4.

## Automatic before/after evidence

Measurements are decoded at 320×180 grayscale. `changed > 8` is the fraction of
pixels whose adjacent-frame luminance difference exceeds eight levels.

| Metric | Source test | Final OGV | Result |
|---|---:|---:|---|
| Displayed frames | 270 | 1020 | approved V2 count |
| Frame rate | 18 fps | 24 fps | approved V2 cadence |
| Duration | 15.0 s | 42.5 s | approved V2 duration |
| Median transition delta | 15.9233 | 0.0009 | substantially calmer |
| Mean `changed > 8` | 41.22% | 6.15% | passes the 8% aggregate anti-boil target |
| Near-hold transition ratio | 0.00% | 84.59% | deliberate limited-animation cadence |
| 9-frame boundary/non-boundary ratio | 2.4700 | 1.3805 | below the 1.5× seam target |

The final numbers do not prove anatomy, identity, emotion, or contact. They show
that the source's pervasive full-frame redraw and nine-frame seam signature
were removed from the displayed timeline.

## Current audit tool — what worked

1. **Strict production manifest.** The tool refuses a production pass when
   human scores, character passports, or per-frame tracks are absent. That
   prevented automatic smoothness metrics from being misrepresented as artistic
   approval.
2. **Reproducible evidence.** It emits deterministic JSON, explicit floors, and
   machine-readable failures.
3. **Useful bootstrap skeleton.** On the MP4 it produced a contiguous candidate
   scene manifest that is a workable review starting point.
4. **Regression coverage.** Unit tests protect strict production floors,
   animatic overrides, missing tracks, duplicate samples, zero-index manifests,
   and rate parsing.
5. **Automatic transition metrics.** The added `--analyze` path now reports
   delta distribution, changed-pixel coverage, holds, lattice concentration,
   and candidate transitions without claiming creative authority.
6. **Displayed-timeline normalization.** The corrected tool handles Theora held
   drawings where decoded-frame reporting can be shorter than the logical
   constant-rate timeline.

## Current audit tool — failures and blind spots

1. **The primary OGV originally crashed.** `avg_frame_rate=0/0` caused a
   division-by-zero exception, even though OGV is the project's game master.
   The tool now falls back to `r_frame_rate`.
2. **Decoded-frame count was mistaken for displayed-frame count.** FFprobe
   reports 576 decoded frames for the final Theora master even though its
   declared 24 fps, 42.5-second display timeline contains 1020 frames. The
   initial fix still undercounted the final hold; the analyzer now materializes
   the declared CFR timeline and pads the tail before frame-indexed measurement.
3. **The original bootstrap was one-indexed.** That contradicted the supplied
   zero-index extraction contract. Schema V2 now records
   `frame_index_origin: 0`, while the validator remains backward-compatible
   with V1 manifests.
4. **Cut detection has no semantic authority.** It found only four source cuts
   under its conservative threshold, while the actual V2 story has 18 directed
   shots. On the final limited-animation cut it reports 49 candidate cuts
   because decisive pose changes resemble edits numerically.
5. **The tool could not detect the wrong-film handoff.** No content hash,
   representative-frame evidence, or semantic confirmation tied the written
   audit to the supplied media.
6. **No automatic identity or anatomy evidence exists.** Passport references
   and scores are required but the tool does not generate face/hand overlays,
   landmark variance, finger-count evidence, or cross-scene identity sheets.
7. **Tracks are supplied, not discovered.** `max_step` checks a provided track,
   but the bootstrap does not establish units, normalization, confidence, or a
   tracker that can create the samples.
8. **Contacts were previously inert.** The manifest carried a `contacts` list
   but did not validate its spans. Basic bounds validation is now present, but
   no ownership/contact state machine is measured against pixels.
9. **Global boil conflates intent and defects.** Without camera compensation,
   object masks, and rhythm annotations, intentional camera moves and decisive
   pose changes inflate the same metric used for unwanted redraw noise.
10. **No playback or device evidence is captured.** Normal-speed, silent,
    half-speed, frame-step, Godot, and Lenovo Tab M11 review remain outside the
    tool.

## Recommendations

### Highest priority

1. Bind every audit to SHA-256, duration, frame rate, and a generated
   first/middle/final contact sheet. Require a reviewer to confirm that the
   semantic brief describes those images before accepting prose findings.
2. Make the approved shot/rhythm contract authoritative. Automatic cut
   detection should propose evidence only; reviewers must classify each
   transition as cut, pose change, camera move, or defect.
3. Normalize every input to a displayed-frame timeline before any frame-indexed
   test. Keep coded-packet count as separate codec evidence.
4. Add per-shot static-region masks and camera transforms. Report background
   boil only after camera compensation and report moving subjects separately.

### Next

5. Generate reviewer-editable landmark tracks with normalized coordinates,
   confidence, and explicit units. Track face construction, both hands, tail
   root/tip, buckles, joined hands, stairs, rails, and platform contacts.
6. Add interaction state machines: anticipated, approaching, contact, held,
   released. Reject ownership swaps, sliding contact, missing settle, and
   undeclared release.
7. Produce character-passport contact sheets automatically across first,
   middle, final, close, difficult-pose, and repaired appearances. Keep human
   scoring authoritative.
8. Add hard-fail codes and repair-window suggestions to reports so a failure is
   actionable without reading free-form logs.

### Release workflow

9. Separate gates into technical, animatic, and production tiers. Automatic
   stability can pass an animatic; production still requires human direction,
   identity/contact review, Godot playback, and target-device evidence.
10. Store the report, provenance, contact sheet, and hashes beside every review
    master. Reject untraceable replacements.
11. Update encoder validation to report both coded packets and logical displayed
    frames, and verify the requested frame rate rather than only printing it.
12. Follow the repair protocol's escalation rule: after two failed repairs of
    the same coherent window, fix the plate/layer/model-sheet architecture
    instead of spending dozens of generator retries.

## Remaining release blockers

- The result still reuses independently drawn storyboard poses. The lower
  temporal frequency makes identity drift less disruptive but does not prove the
  ±2% close-face landmark target or constant hand construction.
- The production-label cleanup is intentionally soft and visible as a small
  defocused top-left region in later shots. A true clean source plate would be
  preferable for a shipping master.
- No approved dialogue, ambience, music, or newly recorded family voice is
  included.
- The human production manifest, character passports, contact review, Godot
  playback, and Lenovo Tab M11 performance test have not been completed.

Do not move this review master into `assets/` until those blockers are resolved.
