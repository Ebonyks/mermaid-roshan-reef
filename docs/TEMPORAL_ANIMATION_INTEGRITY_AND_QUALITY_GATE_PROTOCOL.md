# Temporal Animation Integrity and Quality Gate Protocol

## Purpose

This document defines the production gate for every animated cinematic, scene,
and repair. Its purpose is to ensure that the finished work reads as deliberate
animation rather than a sequence of independently attractive images.

It is the companion to `CINEMATIC_DIRECTION_AND_INTENT_PROTOCOL.md`.

- The **Cinematic Direction and Intent Protocol** decides what a scene should
  mean, feel like, show, and hold.
- This **Temporal Animation Integrity and Quality Gate Protocol** proves that
  the rendered scene honors that approved intention over time.

No OGV, review master, or in-game cinematic is release-ready solely because it
has a valid codec, resolution, duration, or an attractive still frame.

## Non-negotiable quality principle

Animation quality is temporal. A frame can be beautiful and still fail when:

- a face, hand, prop, or costume subtly changes identity;
- camera, body, hair, background, and effects move without a hierarchy;
- contact slides, floats, penetrates, or vanishes;
- an action lacks anticipation, reaction, or settling;
- background layout or perspective changes during a supposedly continuous
  scene; or
- cuts interrupt rather than complete an emotional beat.

The quality gate therefore evaluates frames, action windows, scenes, characters,
edits, and the whole cinematic. It combines automated measurements with human
review; automation identifies evidence and regressions, while people retain
authority over performance, emotion, beauty, and intent.

## Scope and terminology

| Term | Meaning |
|---|---|
| **Frame** | One displayed image at the delivery frame rate. |
| **Action window** | A coherent movement, usually five to nine frames, with a stable purpose and boundary frames. |
| **Scene** | A continuous background/layout context. A hard cut, major location shift, or layout reset starts a new scene. |
| **Shot** | A camera-continuous section within a scene. |
| **Character passport** | The canonical reference package that defines character identity across the whole production. |
| **Rhythm contract** | The approved timing, holds, motion hierarchy, and cut conditions from the direction brief. |
| **Hard failure** | A defect that blocks release regardless of the numerical average. |
| **Repair window** | The smallest temporally coherent span regenerated or corrected after a failure. |

## Quality hierarchy and release floors

Scores use a five-point scale. Averages never excuse critical failure.

```text
Frame integrity                         >= 4.80 / 5.00
Scene congruency                        >= 4.85 / 5.00
Scene rhythm and emotional readability  >= 4.85 / 5.00
Production-wide character identity      >= 4.90 / 5.00
Final cinematic / editorial acceptance  >= 4.90 / 5.00
```

Every required criterion at a level must meet that level's floor. A hard failure
blocks the candidate even when all numerical scores are otherwise high.

## Gate 0 — Inputs and traceability

Every candidate must have versioned inputs before review begins:

- approved Scene Direction Brief and rhythm contract;
- source frame sequence or source-video manifest;
- scene, shot, background, camera, character, and prop identifiers;
- character passport versions used by the scene;
- delivery settings, including source and delivery frame rates;
- generator, renderer, repair, compositing, and export provenance;
- reviewer decisions, defects, repairs, and waiver records.

Never allow an untraceable render to enter the game or replace an accepted
candidate.

## Gate 1 — Frame integrity

### Goal

Catch defects that are visible in a single frame or obvious pairwise comparison.

### Required review categories

- construction: anatomy, perspective, silhouette, scale, and composition;
- identity: face, hair, costume, accessories, props, and palette;
- geometry: stable background layouts, object form, and depth order;
- style: line hierarchy, cel shading, detail density, lighting, and color;
- contact: hands, feet, tails, carried objects, and collision/occlusion;
- frame readability: the intended subject and emotion remain clear at delivery
  size.

### Hard failures

- missing, duplicated, or impossible fingers, limbs, eyes, or accessories;
- unapproved face/body/costume/prop replacement;
- impossible occlusion or perspective break;
- contact penetration, floating, or an object changing ownership;
- unapproved style or palette discontinuity; and
- a frame that fails the approved intent or accessibility/readability rule.

## Gate 2 — Temporal triplet and action-window integrity

### Principle

The prior frame is essential but not enough. Evaluate:

```text
approved frame t-1  -> candidate frame t -> approved/key frame t+1
```

For a repair, use the approved frames before and after the repair window as
locked boundary conditions. For an intended key-pose transition, use approved
key poses rather than treating a purposeful pose change as a defect.

### Audit requirements

- Camera-compensated landmark tracks for all continuity-critical objects.
- Stable object identifiers, masks, depth order, and ownership.
- Motion vectors compared with planned motion arcs.
- Pair, triplet, and full-action-window comparison.
- No unplanned teleport, reversal, flicker, strobing, or one-frame detour.
- Contacts have declared start, hold, release, and tolerance.
- Motion follows anticipation, action, reaction, and settle when the direction
  brief calls for it.

### Minimum tracked landmarks

The exact list is scene-specific, but close character scenes normally track:

- head center and silhouette;
- eyes, mouth center, and face construction lines;
- shoulders, elbows, wrists, and hands;
- distinctive costume features and accessories;
- tail root, center, and tip when visible;
- contact surfaces and carried objects; and
- fixed background anchors such as chair edges, windows, railings, lamps,
  horizon, or doorframes.

## Gate 3 — Scene congruency

### Goal

Evaluate the completed scene as a living whole. A sequence of acceptable frames
does not automatically make an acceptable scene.

### Required dimensions

| Dimension | Review question |
|---|---|
| Character model | Do proportions, face, costume, silhouette, and accessories remain coherent? |
| Spatial layout | Does the same room/world retain its perspective, scale, geometry, and depth? |
| Motion | Are arcs, speed, easing, overlap, contacts, and settle intentional? |
| Camera | Are framing, lens feel, screen direction, and parallax controlled? |
| Performance | Are gaze, pose, and reaction legible and emotionally coherent? |
| Style | Do line, shading, palette, detail density, and lighting stay unified? |
| Rhythm | Does the scene provide orientation, observation, action, consequence, and rest as intended? |

### Acceptance rule

The scene score and every required dimension must be at least **4.85 / 5.00**.
There is no compensating average. One identity, contact, perspective, or rhythm
hard failure rejects the scene.

### Required playback modes

Review every completed scene:

1. at normal speed, with sound;
2. at normal speed, without sound;
3. at half speed; and
4. by frame step / onion-skin / adjacent-frame comparison.

Silent normal-speed review is mandatory because music, dialogue, and sound
effects can mask rushed staging or unstable motion.

## Gate 4 — Character passport and anti-morph review

### Goal

Ensure a character has not gradually changed during production. Scene-level
review misses small changes that only become obvious when early and late scenes
are placed together.

### Character passport contents

Every recurring character requires:

- approved turnarounds and silhouette guide;
- face construction, eye line, mouth placement, and landmark ratios;
- body-proportion envelope;
- hair, costume, accessory, and material inventory;
- palette and line/shading rules;
- approved expression set;
- approved pose/deformation envelope; and
- reference images for front, profile, three-quarter, and key emotional states.

### Global review method

Create contact sheets grouped by character, not by scene. Compare matching
angles, poses, lighting situations, and expressions where possible. Include the
first, middle, and final appearance, difficult poses, close-ups, and repairs.

Audit for:

- body/face proportion drift;
- face, eye, mouth, hairline, and silhouette drift;
- missing, duplicated, relocated, or redesigned accessories;
- palette/material/costume drift;
- unapproved age, body-type, or emotional-read shift; and
- cumulative changes too small to notice one scene at a time.

The global identity score and every identity criterion must be at least
**4.90 / 5.00**. Any unapproved morph is a hard failure.

## Gate 5 — Interaction, contact, and world-state integrity

Every declared interaction has a beginning, a contact/ownership state, and an
end. The audit must prove that the world agrees with itself.

Track:

- hand-to-hand, hand-to-prop, foot-to-ground, and tail-to-surface contacts;
- chair, stair, rail, door, vehicle, and furniture relationship;
- prop ownership and handoff;
- depth/occlusion order;
- entrances, exits, carried objects, and costume state; and
- environmental cause/effect where required by the scene brief.

Reject contact that slides, floats, penetrates, snaps, or changes state without
an authored action.

## Gate 6 — Camera and editorial continuity

Hard cuts are not jitter. Detect scene and shot boundaries before evaluating
temporal continuity.

At every transition, review:

- scene purpose and point of view;
- screen direction and camera axis;
- character/prop location, scale, direction, and state;
- headroom, eyeline, and composition;
- matching action when relevant;
- continuity of time, place, costume, lighting, and prop ownership;
- whether the cut follows the scene's declared emotional completion; and
- whether a longer hold, not another cut, is the correct solution.

## Gate 7 — Rhythm and emotional readability

This gate protects the project from technically stable but emotionally rushed
animation.

Use the approved rhythm contract to review:

- orientation before action;
- a dominant motion and a hierarchy of secondary/still elements;
- anticipation, action, reaction, and settle;
- required gaze, contact, discovery, and reveal holds;
- adequate visual rest;
- meaningful stillness: looking, listening, choosing, working, resting, or
  changing; and
- cuts that occur after, not before, the intended beat lands.

The objective is patient attention, not empty duration. A long shot with no
readable thought or action is slow plotting, not breathing room.

## Gate 8 — Whole-cinematic style and world coherence

Review the entire work as one production:

- original early-1990s-cartoon-informed line, color, shading, and shape language;
- restrained, repeatable rendering rather than unstable high-detail illustration;
- consistent world scale, perspective, lighting, and camera grammar;
- controlled motion density and cadence;
- coherent emotional progression; and
- no scene that is visually polished yet belongs to a different production.

Use historic animation as a study reference for pacing and craft, not as a
template to imitate or reproduce.

## Gate 9 — Technical encode, playback, and release validation

The OGV pipeline remains responsible for:

- frame count, order, duration, dimensions, pixel format, codecs, and audio;
- source-to-output decode comparison;
- OGV and in-engine playback at the target frame rate;
- target-device CPU, memory, frame pacing, loading, and scene-entry behavior;
- audio synchronization, dialogue intelligibility, and loudness; and
- source integrity and provenance.

Use **24 fps delivery** as the artistic baseline once target-device tests prove
it is viable. This does not require uniform motion every displayed frame:

- use held or on-twos animation for intentional calm and simple acting;
- use unique 24 fps motion for camera movement, turns, contacts, close acting,
  and fast gestures; and
- never use a lower cadence to conceal temporal instability.

## Repair protocol

1. Classify the defect: intent, identity, construction, layout, motion, contact,
   camera, rhythm, style, edit, or technical playback.
2. If the problem is artistic intent, return to the Cinematic Direction and
   Intent Protocol before attempting visual repair.
3. Otherwise, identify the smallest coherent repair window.
4. Lock approved boundary frames, camera, background, object IDs, masks, depth
   ordering, and valid character landmarks.
5. Repair only the affected layers/objects whenever possible; never regenerate
   the whole scene merely because one hand, face, or accessory failed.
6. Re-run frame, triplet, action-window, scene, character-passport, and
   neighboring-transition gates affected by the repair.
7. Escalate after two failed automated repair attempts. Repeated failure usually
   means the key pose, layout, model sheet, or direction is wrong.

No repair may silently alter already accepted neighboring frames.

## Tool requirements

The implementation must support:

- OGV/frame-sequence decoding and deterministic frame numbering;
- scene/shot boundary detection and reviewer overrides;
- versioned Scene Direction Brief and rhythm-contract input;
- per-frame landmark, mask, object-ID, camera, and contact annotations;
- pair/triplet/action-window temporal comparisons;
- character-passport contact sheets across all production appearances;
- defect taxonomy, scores, hard-fail codes, repair windows, and reviewer notes;
- machine-readable reports for CI/release gating; and
- human review interfaces for normal-speed, silent, half-speed, frame-step,
  onion-skin, and side-by-side passport comparison.

The initial implementation is `tools/audit_cinematic.py`. It is deliberately
strict: a scene cannot pass without human scores, a character passport, and a
per-frame track for every declared character. Expand it incrementally, without
allowing automation to replace artistic review.

## Release decision

A cinematic may enter the game only when all required gates are green, all
critical reviewer notes are resolved, no waiver is expired, and the current
version has traceable inputs and target-device playback evidence.

The final question is simple: does the audience see intentional character,
place, feeling, and motion—or merely a succession of images? Only the former is
acceptable.
