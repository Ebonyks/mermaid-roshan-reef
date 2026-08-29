# Owner-run Grok handoff — Day One Main Hall entry animation

## Use and authority

This is a copy/pasteable **visual-only** handoff for the first Day One Main
Hall entry animation. The owner alone performs every Grok upload, submission,
and download. Grok is a visual generation worker only. It may report a narrow
feasibility limitation, but it may not remove, reorder, simplify, or approve
any required beat. Luna authors the generation/review instructions and reviews
returned outputs, but never submits to Grok or operates the Grok interface. Sol
audits the handoff and every candidate against the direction and quality gates;
owner review is final.

This handoff explicitly inherits the organization of
`design/HANDOFF_GROK_DAY_ONE_POOL_NEXT_ANIMATION_2026-08-23.md`: use and
authority, numbered appearance-bearing references, non-negotiable continuity,
required visual beats, paste-ready generation directions, and delivery/review
contract. It changes the subject from pool restoration to the Main Hall entry,
adds a seven-perspective entry shot plan, and makes the hall's existing dirt
landmarks and three bunny identities binding. It does not supersede the
cinematic direction protocol, temporal quality gate, protected-asset rules, or
owner acceptance.

Do not ask Grok for music, ambience, foley, voices, dialogue, subtitles, or a
final mix. Any returned audio is disposable and must be muted/discarded. Audio
and any recorded family voice work are separate owner-authorized production
tasks. Never upload, imitate, or repurpose protected family voice files.

Do not make one long clip covering all seven perspectives. Generate each
perspective as its own short candidate clip and/or complete full-frame study,
with at least three candidates per perspective. Preserve every native
candidate before editorial selection, trimming, normalization, or encoding.

### Study versus final delivery

Every Grok video or short clip requested below is a **STUDY-ONLY direction and
motion study**. Its pixels, frames, interpolated frames, retimed sections,
trimmed subclips, or exports may not enter the final cinematic. A study may
inform framing, screen direction, timing, gaze order, acting, and camera
blocking only. For final delivery, the owner must submit a Luna-authored
FINAL-DELIVERY-FRAME request to Grok for every changed timeline frame, and each
returned frame must be individually authored as a complete flattened image in
the approved 2D storybook style. Only a declared intentional hold may repeat
an accepted frame, and its narrative purpose must be recorded in the manifest.
This rule applies even when a study clip appears visually successful.

### Paste-ready FINAL-DELIVERY-FRAME generation template

The following is the only permitted generation instruction for a final changed
timeline frame. Submit **one request per changed frame**; never submit a clip,
contact sheet, montage, or batch and then treat its frames as final. Replace the
bracketed metadata before the owner submits it to Grok. The owner alone submits;
Luna may author this filled-in prompt and review the returned frame but never
operates Grok.

```text
FINAL-DELIVERY-FRAME. Generate exactly one new complete flattened 2D storybook
image for scene DAY_ONE_MAIN_HALL_ENTRY, shot [SHOT_ID], timeline_index
[TIMELINE_INDEX]. This is final-delivery frame attempt [ATTEMPT] and is not a
study frame, video frame, interpolation, inbetween, composite, cutout, layer
render, or image edit. Return exactly one newly generated whole-canvas image at
[NATIVE_WIDTH]x[NATIVE_HEIGHT], preserving the approved 16:9 composition.

Exact temporal boundary references: the immediately prior accepted complete
frame is [BEFORE_PATH], SHA-256 [BEFORE_SHA256]. The immediately following
accepted complete frame is [AFTER_PATH], SHA-256 [AFTER_SHA256]. Preserve their
camera, background landmarks, screen direction, perspective, character
identity, and object ownership except for the declared action below. Do not
blend their pixels or copy any pixels from either boundary.

Exact declared state: [ACTION_OR_HOLD_STATE]. Motion/hold purpose:
[DECLARED_MOTION_OR_INTENT]. Timeline action window: [WINDOW_START]–[WINDOW_END].
This frame's subject geometry is [SUBJECT_GEOMETRY: character IDs, normalized
bounding boxes, eye lines, hands, tails, bunny ID/contact, and active prop].
Camera/crop locks are [CAMERA_CROP_LOCKS: framing, crop, horizon, fixed
landmarks, screen direction, and permitted camera motion]. Identity/style locks
are [IDENTITY_STYLE_LOCKS: Roshan/Daddy passport versions, face, hair, crown,
glasses, costume, one tail each, Main Hall palette, contours, shading, and
dirty-landmark IDs].

OWNER UPLOAD ORDER FOR THIS FINAL FRAME: upload the fixed shot-matrix
appearance/composition references first, in their prescribed order; then upload
[BEFORE_PATH] as the complete temporal_before image; then upload [AFTER_PATH]
as the complete temporal_after image; then, only if needed, upload
[POSITION_GUIDE_PATH] as the neutral position_only guide. Record every uploaded
item, exact role, path, and SHA-256 in ordered_uploaded_references. If a
neighbor is absent at a scene/shot boundary, do not upload a substitute: record
its path and SHA-256 as null and the boundary reason as [BOUNDARY_REASON].

Use only the approved appearance and composition references listed for this
shot. A position guide, if supplied, is POSITION_GUIDE_ONLY and controls only
normalized position/bounds; its pixels, silhouette, color, lighting, texture,
or design must not appear in this image. Keep every inactive landmark and
character still. No text, UI, pointer, watermark, audio, generic castle,
extra bunny, extra character, legs, feet, shoes, tail split/fusion, face drift,
style clash, sticker dirt, global tint, camera drift, pan, zoom, translated
layer, composited cutout, sprite/rig motion, tween, morph, optical flow,
cross-dissolve, procedural warp, duplicated motion frame, or copied boundary
pixels. Return one complete newly generated flattened image only.
```

The returned image is a candidate until Luna and Sol review it. For an
intentional hold, record the hold span and narrative purpose; a hold may not
replace a required gaze, departure, contact, bunny hop, reaction, or settle.

#### FINAL-DELIVERY-FRAME upload order exception

The fixed shot-matrix upload list remains the appearance/composition authority
for every study and every final frame. A FINAL-DELIVERY-FRAME request has one
additional, explicit upload order so temporal continuity can be checked without
changing those authorities. The owner must upload:

1. the fixed shot-matrix references for that shot, in the matrix order;
2. the complete approved neighbor-before frame, if one exists;
3. the complete approved neighbor-after frame, if one exists; and
4. optionally, one neutral `POSITION_GUIDE_ONLY` guide.

Neighbor-before and neighbor-after uploads are temporal context only. They do
not replace, override, or become substitutes for any appearance or composition
reference in the fixed shot matrix. Every uploaded item must be recorded in
`ordered_uploaded_references` with its exact upload order, path, SHA-256, and
role: `appearance`, `composition`, `temporal_before`, `temporal_after`, or
`position_only` as applicable. The same item may have only the role it actually
serves in that request; do not silently treat a runtime capture or temporal
neighbor as an identity authority.

If an approved temporal neighbor does not exist at a scene or shot boundary,
the owner must not invent, duplicate, synthesize, or substitute a frame. Record
the corresponding neighbor path and SHA-256 as `null` and record a boundary
reason such as `scene_start_no_prior_frame` or `shot_end_no_next_frame` in the
delivery manifest and the filled-in FINAL-DELIVERY-FRAME prompt. The owner
still uploads the available fixed shot-matrix references in their prescribed
order, followed by any available temporal neighbor, then the optional neutral
position guide.

## References for the owner to upload

Upload only the references listed for the selected shot, in the order stated
below. Appearance-bearing references control identity and design. Runtime
captures control composition and the visible dirt arrangement only; they are
not delivery pixels and do not authorize copying UI, pointers, debug marks, or
screen overlays.

### Ordered reference deck

1. `assets/characters/roshan_25d/roshan_base.png`
   Roshan's canonical front identity: face, brown hair with rainbow streak,
   pink top, rainbow tail, palette, proportions, and child-readable silhouette.
2. `assets/characters/roshan_25d/roshan_directional.png`
   Roshan's approved directional silhouettes and screen-direction authority.
3. `assets/characters/roshan_25d/roshan_gesture_a.png`
   Roshan's approved wave/cheer/clap/twirl gesture vocabulary; use only the
   relevant standing/look gesture as a pose reference.
4. `assets/characters/roshan_25d/roshan_gesture_b.png`
   Roshan's approved look, giggle, sleep, and point/reach vocabulary; use it to
   guide the discovery glance and pointing response without redesigning her.
5. `assets/characters/roshan_25d/roshan_gesture_c.png`
   Roshan's approved small reaction/boing/collect vocabulary; use only for a
   restrained surprised-but-safe reaction.
6. `assets/characters/roshan_25d/roshan_gesture_d.png`
   Roshan's approved remaining gesture vocabulary and silhouette consistency.
7. `assets/characters/friends/daddy.webp`
   Daddy Mermaid's in-project character identity reference: face, long brown
   hair, pointed ears, glasses, ornate crown, dark navy/blue clothing, teal
   cape, and rainbow mermaid tail.
8. `assets_src/daddy_master.png`
   Daddy Mermaid's higher-resolution appearance authority. There is no approved
   Daddy walk atlas. Do not invent one, and do not use a rig, model, legs, feet,
   or shoes to solve movement.
9. `tmp/grok_v03_refs/G03_REF2_ROSHAN_DADDY_FULLBODY_F0000.png`
   Prior full-body Roshan/Daddy relationship, height, costume, tail, and
   two-character proportion reference only.
10. `tmp/grok_v03_refs/G02_IDENTITY_CABIN_V02_F0048.png`
    Prior face, hair, crown, glasses, and color identity reference only.
11. `tmp/grok_v03_refs/G02_IDENTITY_HANDHOLD_V02_F0108.png`
    Prior safe handhold/relationship reference only; it does not authorize a
    new pose, background, or camera design.
12. `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_a_native_1672x941.png`
    Clean left architectural screen A; exact 0–1672 composition and art style.
13. `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_b_native_1672x941.png`
    Clean right architectural screen B; exact 1672–3344 composition and art
    style.
14. `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/main_hall_production_master_7280x2048.png`
    Continuous clean two-screen hall geography and seam/landmark authority.
15. `tmp/day_one_capture_latest/dirty_left.png`
    Dirty left runtime composition and child-readable dirt placement only.
16. `tmp/day_one_capture_latest/dirty_shock_left.png`
    Roshan's dirty-hall arrival/reaction composition only; do not copy capture
    UI, pointers, debug text, or delivery pixels.
17. `tmp/day_one_capture_latest/dirty_right.png`
    Dirty right runtime composition and back-room-side landmark placement only.
18. `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_sleepy.png`
    Sleeping bunny identity and child-readable scale reference.
19. `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_shell_hide.png`
    Shell-hide bunny identity and hiding behavior reference.
20. `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_hop.png`
    Hopping/runner bunny identity, hop silhouette, and motion reference.

For any selected shot, references 1–11 establish character identity and
relationship; references 12–17 establish the hall and composition; references
18–20 establish the existing three bunny designs. Use the following upload
matrix so the owner does not over-upload unrelated references:

| Shot | Upload, in this order | Omit |
|---|---|---|
| 01 Threshold | 1, 2, 7, 8, 9, 13, 17, 20 | 3–6, 10–12, 14–16, 18–19 |
| 02 Right discovery | 1, 2, 4, 7, 8, 13, 17, 20 | 3, 5–6, 9–12, 14–16, 18–19 |
| 03 Daddy departure | 1, 2, 7, 8, 9, 13, 17, 20 | 3–6, 10–12, 14–16, 18–19 |
| 04 Roshan exploration | 1, 2, 4, 13, 17, 20 | 3, 5–12, 14–16, 18–19 |
| 05 Bunny low angle | 1, 13, 17, 20 | 2–12, 14–16, 18–19; upload only the selected runner bunny if fixed |
| 06 Left discovery | 1, 2, 4, 12, 15, 18 | 3, 5–11, 13–14, 16–17, 19–20 |
| 07 Cleanup-ready | 1, 2, 4, 12, 16, 19 | 3, 5–11, 13–15, 17–18, 20 |

The matrix is deliberately one bunny reference per shot. If a shot is locked to
a different one of the three bunnies, replace its single bunny reference with
that bunny's one assigned file; never upload all three. Right-screen Shots
01–04 use clean screen B (13) and dirty-right composition (17). They may add
the continuous master (14) only when a specific continuity landmark cannot be
read from screen B. Left-screen Shots 06–07 use clean screen A (12), with
Shot 06 using dirty-left (15) and Shot 07 using the dirty shock composition
(16). References 12–14 are clean architecture authorities; 15–17 are dirty
composition authorities and contain no delivery pixels.
Shot 06 uploads only the sleepy bunny (18), never both sleepy (18) and
shell-hide (19); Shot 07 uploads only shell-hide (19). Roshan gesture B (4) is
reserved for the look/point/reach discovery beats in Shots 02, 04, 06, and 07;
gesture A is not a substitute for those looks.
Do not upload rejected art, alternate castle rooms, a generic castle, a prior
clean-room capture, or any reference not assigned to the shot.

## Scene Direction Brief

```text
scene_id: DAY_ONE_MAIN_HALL_ENTRY
version: direction-v1-2026-08-28
working_title: The Castle Is Dusty
scene role: Day One entrance into the already-dirty castle Main Hall
point_of_view: Roshan after the shared arrival, with Daddy as the caring guide
scene purpose: establish that the whole castle is visibly messy, split Daddy's
back-room cleanup task from Roshan's Main Hall discovery, and hand the child a
clear, wordless cleanup-ready room
required audience takeaway: Daddy and Roshan entered together, they saw the
same big mess, Daddy went to clean the back room, and Roshan stayed to notice
the bunnies and the things she can clean
start state: Daddy and Roshan approach/enter the dusty Main Hall together;
the hall is visibly dirty before either character acts
end state: Daddy has gone toward the curtained Royal Hall/back-room arch;
Roshan remains in the foreground walk lane, looking at a bunny and the visible
mess, ready for touch-based cleanup
emotional arc: welcome -> shared discovery -> Roshan's safe surprise ->
curiosity and agency
location: the continuous two-screen Main Hall, 0–3344 art-space pixels
time: Day One, immediately after arriving at the castle
environment role: the dirty hall is an active story participant; it shows dull
cobwebbed lamps, wall grime, chunky footprints, floor mud/dust/ribbon mess,
and three friendly hopping/hiding bunnies without obscuring the play lane
```

### Beats

```text
orientation: threshold wide establishes both mermaids, one complete right-screen
hall slice, and multiple unmistakable dirt landmarks before movement
observation: Roshan's eyes and head follow the nearest bunny and then the wall
or floor mess; Daddy notices the same state and looks toward the back room
action: Daddy gestures that he will go through the back-room arch while Roshan
takes a few gentle tail-glides into the hall
reaction: Roshan pauses, eyes widen, and she gives a small safe gasp/surprised
look as a bunny hops or peeks from the dirty runner
consequence: the bunny settles near a cleanable landmark; the lamps, handprint
or splash, footprints, and floor pile remain visibly dirty around it
exit: Daddy is absent through the curtained back-room arch; Roshan is settled
in a clear foreground position facing the bunny and messes, with no overlay
instruction required to understand the next playable action
```

## Rhythm contract

- Delivery baseline: 24 fps when target-device playback permits; each short
  candidate is a self-contained shot with its own native frame sequence.
- Orientation holds: at least 0.8 seconds in the arrival wide and at least
  0.5 seconds in every closer perspective before the dominant action.
- Motion hierarchy: one character action or one bunny action is dominant at a
  time. Background architecture and all non-active dirt landmarks hold still.
- Required gaze order: Roshan's eyes find the bunny or dirt first, her head
  follows, then her torso/tail chooses a direction. Daddy looks toward Roshan
  before indicating the back room.
- Required Daddy departure shape: glance -> small open-hand gesture -> wait for
  Roshan's acknowledgment -> one gentle tail-glide toward the arch -> settle
  at/through the curtained doorway. No pulling, rushing, or disappearance cut
  before the destination reads.
- Required Roshan discovery shape: orientation -> look -> small safe surprise
  -> one step/tail-glide -> stop -> look back down at the bunny/mess -> settle.
- Required bunny shape: crouch/peek or anticipation -> one readable hop ->
  landing/contact -> small settle. Never use a swarm, clone, or continuous
  bobbing field.
- Camera: lock during gaze, surprise, hand gesture, bunny contact, and final
  settle. A restrained camera move is permitted only in the threshold arrival
  wide to reveal the hall and must stop before Roshan's discovery.
- Cut condition: every perspective ends after its intended look, gesture, hop,
  or departure has settled. Do not cut on the first literal movement.
- Sound-off readability: the dirt, bunny, Daddy departure, and Roshan's
  readiness must all read without audio or text.

## Master continuity and negative locks

### Hall geography and dirt

- Preserve the continuous hall as one space: screen A occupies art-space
  x=0–1672 and screen B occupies x=1672–3344. Each 1280x720 shot shows one
  motivated screen slice at a time; do not pretend one frame can show both
  screens or the full 3344px hall. Do not mirror, compress, stretch, recompose,
  or invent a third screen.
- Preserve the established lavender shell-stone architecture, cream-gold trim,
  aqua/lavender shadows, red runner, floor horizon, doorway positions, and
  corridor depth. The clean hall references are architecture/style authorities;
  the dirty captures are composition/dirt authorities.
- The far-right curtained Royal Hall/back-room arch at approximately x=2870 is
  Daddy's story-only destination in this scene. It is not a new room, portal,
  or interactive object, and it must not be replaced by a generic door.
- Keep the main walk lane broad and visible. Characters may pass in front of
  architecture, but dirt must not cover Roshan's face, tail, path, or the
  child-readable interaction targets.
- Preserve the existing dirt vocabulary: dull/cobwebbed shell lamps; a large
  handprint or wall splash; chunky runner footprints; the brown mud/dust/ribbon
  floor pile; and the three established bunnies. Dirt must be local, physical,
  varied, and visibly contrast with the cleaned architecture. A whole-frame
  dimmer is not a substitute for dirt.
- Keep exactly three bunny identities in the hall: sleepy, shell-hide, and
  runner/hop. One may be partly hidden, but do not duplicate, merge, recolor,
  or redesign them. Each bunny has a clear ground/contact relationship.

### Character and action

- Roshan remains the approved child mermaid: brown hair with rainbow streak,
  pink top, rainbow tail, approved face, hands, and proportions.
- Daddy Mermaid remains the approved adult: long brown hair, pointed ears,
  glasses, ornate gold crown, dark navy/blue outfit, teal cape, and one rainbow
  mermaid tail. There is no approved Daddy walk atlas. Use brief, broad,
  controlled tail-glide poses based on the supplied identity/full-body
  references; do not invent human locomotion.
- Neither mermaid has legs, feet, or shoes. Do not split or fuse tails. No
  duplicated arms, fingers, crowns, glasses, faces, or character clones.
- Daddy and Roshan enter together and share the discovery. Daddy goes to the
  back room; Roshan remains in the Main Hall. Daddy does not clean the visible
  Main Hall in this entry animation, and Roshan does not enter the back room.
- Preserve screen direction across the seven perspectives unless a cut is
  explicitly motivated by the shot plan. Do not reverse the hall's spatial
  landmarks or swap Daddy/Roshan ownership of the action.

### Production and style

- Final visual medium is polished flattened 2D storybook art: rounded forms,
  navy/plum contours, broad painted value bands, restrained highlights, and
  aqua/lavender shadows. Match the established Main Hall; do not create a
  photoreal, 3D, anime, glossy, horror, or dark-fantasy castle.
- No text, captions, subtitles, labels, UI, touch pointers, debug marks,
  watermarks, logos, interface rings, full-screen tint panels, sticker outlines,
  or opaque overlays.
- Do not cover a clean background with unrelated dirty stickers. Dirt must be
  integrated into the floor, wall, runner, lamp, or bunny contact area with
  local shadows and matching light.
- Each generated delivery frame must be a newly authored complete flattened
  frame. Never supply missing action with tweening, morphing, optical flow,
  cross-dissolve, duplicated frames, translated camera/background layers,
  sprite/cutout motion, rigging, procedural warp, or composited characters.

## Seven-perspective shot plan

| Shot | Duration | Perspective and purpose | Dominant action | Required settle/cut |
|---|---:|---|---|---|
| 01 — Threshold arrival wide | 4 s | Right-screen threshold wide, both mermaids and the dirty right hall slice readable | Daddy and Roshan enter together from screen-right and stop; runner bunny may peek | Hold on shared realization of the dirty hall |
| 02 — Right discovery two-shot | 3 s | Right-screen medium two-shot favoring Roshan and the right lamp/wall/floor mess | Roshan notices the runner bunny, then the nearest dirty landmark; Daddy follows her gaze | Hold her safe surprised look before the cut |
| 03 — Right-side Daddy departure | 4 s | Right-side three-quarter view including the back-room curtained arch | Daddy indicates and tail-glides toward the back room; Roshan acknowledges and stays | Hold with Daddy framed at the arch and Roshan still in the hall |
| 04 — Roshan over-shoulder exploration | 4 s | Over Roshan's shoulder toward the central/right floor and wall mess | Roshan advances one short glide and looks between bunny, footprints, and floor pile | Hold on her settled, curious posture |
| 05 — Bunny low angle | 2–3 s | Low runner-level view, bunny foreground with Roshan readable behind | One established bunny performs one hop/peek and lands | Hold on contact and a tiny settle; no swarm |
| 06 — Left mess discovery | 4 s | Motivated cut to the left screen; Roshan medium/close near sleepy and shell-hide bunnies, left lamp/wall/runner mess | Roshan looks from bunny to a specific cleanable mess and points/raises a hand | Hold the clear “I see the mess” reaction |
| 07 — Final cleanup-ready wide | 3 s | Stable left-screen wide with Roshan, visible dirt field, and playable hall lane | Daddy is gone; Roshan turns toward the nearest bunny/mess and settles | End on the playable hall, no text or pointer needed |

All seven perspectives are required in the final sequence. The owner selects
exactly one accepted candidate for each perspective, only after Luna and Sol
verify boundaries, identity, dirt continuity, and camera geography. These are
separate candidates, never one long clip. If a shot requires a new angle,
regenerate that complete shot; do not pan or translate a still to simulate it.

## Separate copy/paste Grok prompts

### Shot 01 — Threshold arrival wide

```text
STUDY-ONLY: Create one new short 16:9 direction/motion-study video candidate,
1280x720, 24 fps, as a complete polished flattened 2D storybook animation of
the Mermaid Roshan Day One Main Hall entry. This study's pixels and frames may
not be used as final delivery; use it only to learn framing, direction, timing,
and acting. Use the supplied Roshan, Daddy, clean Main Hall, dirty runtime
capture, and bunny references only for their assigned authorities. This is one
4-second threshold-arrival wide shot, not a montage and not part of one long
clip.

Start just inside the Main Hall entrance with a right-screen threshold wide
view of both mermaids and the established shell architecture. The hall is
visibly dirty before they move: dull cobwebbed shell lamps, wall grime or
splash, chunky footprints on the red runner, a brown mud/dust/ribbon floor
pile, and the established runner bunny are readable in this screen slice.
Preserve the continuous hall's exact perspective and keep the far-right
curtained Royal Hall/back-room arch readable as Daddy's destination; do not
attempt to show both 1672px screens in this 1280px frame.

For the first 0.8 seconds, hold the threshold orientation. Then Daddy Mermaid
and Roshan enter together with one gentle mermaid-tail glide and stop. Daddy is
the taller adult with long brown hair, pointed ears, glasses, ornate crown,
navy outfit, teal cape, and one rainbow tail. Roshan is the smaller child with
brown hair and rainbow streak, pink top, and rainbow tail. Their faces,
costumes, hands, tails, and proportions stay constant. They look at the room
and share one readable safe surprise; one bunny may peek once and settle.

Use one restrained camera ease only while revealing the hall, then lock before
the shared look. Give the completed arrival at least 0.7 seconds of stillness.
Keep architecture and all inactive dirt landmarks still. No dirt overlay, whole
frame darkening, extra bunny, extra character, generic castle, legs, feet,
shoes, fused tails, face drift, camera cut, camera pan, camera zoom, UI, text,
pointer, watermark, dialogue, music, or generated audio. Return a complete
newly authored flattened shot with no composited cutouts, sprite motion,
interpolation, morphing, optical flow, cross-dissolve, or duplicated motion
frames.
```

### Shot 02 — Right discovery two-shot

```text
STUDY-ONLY: Create one new 3-second, 1280x720, 24 fps, 16:9 polished flattened
2D storybook direction/motion-study video candidate. Its pixels and frames may
not be used as final delivery; use it only to learn framing, direction, timing,
and acting. This is a separate locked right-screen medium two-shot inside the
exact dirty Mermaid Roshan Main Hall. Preserve the supplied hall architecture
and composition. Use the dirty capture for dirt placement only, never its UI,
pointer, debug marks, or delivery pixels.

Roshan stands foreground/left with Daddy beside or slightly behind her on the
right screen. Roshan first holds still for 0.6 seconds, her eyes find the
established runner dust bunny, and her head follows. She then notices the nearby
dull cobwebbed lamp, wall splash, tipped bucket, or chunky floor footprints. Her
expression is a small safe surprise that becomes curiosity. Daddy only follows
her gaze and softens his expression. Roshan may make one small hand/upper-body
discovery gesture; she does not clean anything yet.

The dirt must read as physical, child-readable mess integrated into the local
wall, lamp, runner, or floor. The bunny has one clear contact shadow and does
one peek or tiny hop, then settles. Keep all other objects still. Match the
approved identities exactly: Roshan has brown hair with rainbow streak, pink
top, rainbow tail; Daddy has long brown hair, pointed ears, glasses, crown,
navy outfit, teal cape, and one rainbow tail. No legs, feet, shoes, tail split,
face drift, new characters, bunny clones, generic castle, whole-frame dimming,
stickers, overlays, UI, text, audio, camera move, cut, tween, morph, optical
flow, composited cutout, or duplicate motion frame. Hold her completed look for
the final 0.6 seconds and return a complete newly authored flattened shot.
```

### Shot 03 — Right-side Daddy departure

```text
STUDY-ONLY: Create one new 4-second, 1280x720, 24 fps, 16:9 polished flattened
2D storybook direction/motion-study video candidate. Its pixels and frames may
not be used as final delivery; use it only to learn framing, direction, timing,
and acting. This is a separate right-screen three-quarter shot of the exact
dirty Main Hall. Include the established far-right curtained Royal Hall/back-
room arch as Daddy's destination within this screen slice; do not attempt to
show the entire A/B hall in one frame. Do not invent a new room or portal. The
supplied dirty right capture controls visible dirt arrangement only; do not copy
UI, pointers, debug marks, or pixels.

For the first 0.7 seconds, Daddy and Roshan hold in the dirty right-screen hall
while the curtained arch and several messes read: a dull cobwebbed lamp, wall
splash/grime, floor footprints, a brown mud/dust/ribbon pile, and the
established runner bunny. Daddy looks to Roshan, then toward the curtained arch,
then gives one small open-hand gesture meaning he will handle that back room.
He waits for Roshan's acknowledgment. Daddy then makes one gentle controlled
mermaid-tail glide toward the arch and settles at/through its curtain. Roshan
remains in the Main Hall, visibly watching him go; she does not follow.

Daddy is the approved adult with long brown hair, pointed ears, glasses, ornate
crown, navy outfit, teal cape, and one rainbow mermaid tail. No approved Daddy
walk atlas exists: use only broad storybook tail-glide poses based on the
supplied identity references. Roshan remains the approved child with brown hair
and rainbow streak, pink top, and rainbow tail. No legs, feet, shoes, fused or
split tails, face/costume drift, extra character, bunny clone, camera pan/zoom,
hall mirroring, cut during the gesture, full-screen dimmer, dirt stickers, UI,
text, audio, interpolation, morphing, optical flow, composited cutouts,
translated layers, or duplicate motion frames. Keep the hall landmarks fixed;
hold Daddy's departure and Roshan's remaining position for the final 0.7
seconds. Return one complete newly authored flattened shot.
```

### Shot 04 — Roshan over-shoulder exploration

```text
STUDY-ONLY: Create one new 4-second, 1280x720, 24 fps, 16:9 polished flattened
2D storybook direction/motion-study video candidate. Its pixels and frames may
not be used as final delivery; use it only to learn framing, direction, timing,
and acting. This is a locked over-Roshan-shoulder exploration shot in the exact
dirty Main Hall. Roshan is the point-of-view character. Daddy is not the focal
subject and is either absent through the back-room curtain or quiet at its edge;
do not bring him back into the hall action.

Begin with a 0.6-second hold behind Roshan so the viewer can orient to the
runner, wall, and floor. Roshan's eyes first find the single supplied runner
bunny, then her head and torso follow. She makes exactly one short
mermaid-tail glide into the open walk lane and stops. Her attention moves from
the bunny to the chunky runner footprints and the brown mud/dust/ribbon pile,
ending in a calm curious posture that says she has found things to clean.

Preserve the exact clean-hall architecture and the dirty capture's local
landmarks: dull cobwebbed lights, wall handprint/splash, footprints, floor
mess, and one of the three existing bunny designs. Dirt must touch or belong to
the floor/wall/runner and retain local shadows; never use a general dark tint or
floating sticker. Roshan's approved face, brown rainbow-streaked hair, pink top,
rainbow tail, hands, and proportions cannot change. She has no legs, feet, or
shoes. No extra characters, bunny clones, camera translation, orbit, zoom, pan,
cut, UI, text, audio, overlay, interpolation, morph, optical flow, composited
cutout, sprite motion, or duplicate motion frames. Lock the camera during her
gaze and final settle. Return a complete newly authored flattened shot.
```

### Shot 05 — Bunny low angle

```text
STUDY-ONLY: Create one new 2.5-second, 1280x720, 24 fps, 16:9 polished
flattened 2D storybook direction/motion-study video candidate. Its pixels and
frames may not be used as final delivery; use it only to learn framing,
direction, timing, and acting. This is a separate bunny discovery shot, not a
swarm montage. Use the single selected approved dust-bunny file for bunny
identity and the dirty runtime capture for composition/dirt placement, never
for UI or delivery pixels.

Place exactly one selected established bunny (prefer the runner for the right
screen continuity) in the foreground with a clear contact shadow on the red
runner or lavender floor.
Roshan remains readable in the middle background as the child observer. Hold
the bunny in a crouch/peek for 0.5 seconds, then show one unmistakable hop or
peek movement, ground contact, and a tiny settle. Roshan's eyes follow it with
one small safe delighted-surprised reaction; she does not chase it. Keep the
dull lamp, wall grime/handprint, footprints, and floor pile visible behind the
action as quiet environmental context. Do not add any other bunny identity.

The bunny must remain the supplied child-friendly shape and color, with no
duplicate ears, eyes, limbs, bunny copies, swarm, smoke, sparkle cloud, or
continuous bobbing. Roshan keeps brown hair with rainbow streak, pink top,
rainbow tail, and approved face/proportions; no legs, feet, shoes, or tail
fusion. Preserve the hall perspective and lighting. No camera move, zoom, pan,
cut, overlay, sticker dirt, whole-frame darkening, UI, text, audio, generated
voice, interpolation, morphing, optical flow, composited cutout, or duplicate
motion frames. Hold the bunny's landed contact for the final 0.5 seconds and
return one complete newly authored flattened shot.
```

### Shot 06 — Left mess discovery

```text
STUDY-ONLY: Create one new 4-second, 1280x720, 24 fps, 16:9 polished flattened
2D storybook direction/motion-study video candidate. Its pixels and frames may
not be used as final delivery; use it only to learn framing, direction, timing,
and acting. This is a stable Roshan medium/close shot on the left screen of the
exact dirty Main Hall, following a motivated cut as she continues screen-left.
Use the left dirty capture only as a composition and dirt-landmark reference.
Preserve the wall, runner, lamps, and floor perspective; do not copy capture
UI, pointers, debug marks, or pixels.

Roshan begins still for 0.7 seconds after entering from screen-right. Her eyes
find the single supplied sleepy bunny, then move to a nearby
specific cleanable mess: the dull cobwebbed lamp, the wall handprint/splash,
the chunky runner footprints, or the brown mud/dust/ribbon pile.
Her head follows, she makes one small point/reach or open-hand discovery
gesture, and she settles with a clear safe “I see that” expression. She does
not clean the landmark yet. The selected mess remains visibly dirty and
physically integrated while other dirt landmarks remain quiet. The bunny does
one small hop or holds a peek, then settles.

Roshan is the approved child mermaid with brown rainbow-streaked hair, pink top,
rainbow tail, approved face, hands, and proportions. No legs, feet, shoes,
fused/split tail, face drift, extra character, or bunny clone. Keep the
storybook palette and local contact shadows. No global darkening, generic
castle, dirt sticker, opaque overlay, camera move, pan, zoom, cut, UI, text,
audio, interpolation, morph, optical flow, composited cutout, translated layer,
or duplicate motion frame. Lock the camera during gaze, gesture, and settle.
Hold the completed discovery for the final 0.7 seconds and return a complete
newly authored flattened shot.
```

### Shot 07 — Final cleanup-ready wide

```text
STUDY-ONLY: Create one new 3-second, 1280x720, 24 fps, 16:9 polished flattened
2D storybook direction/motion-study video candidate. Its pixels and frames may
not be used as final delivery; use it only to learn framing, direction, timing,
and acting. This is the final stable cleanup-ready wide of the exact dirty
Mermaid Roshan Main Hall on screen A after a motivated cut. Preserve the clean
architecture and left dirty capture composition; do not attempt to show the
continuous A/B hall, and do not copy UI, pointers, debug marks, or delivery
pixels.

Daddy has already gone through the curtained back-room arch and is not visible
in this shot. Roshan remains in the broad foreground walk lane. Start with a
0.6-second orientation hold showing several unmistakable cleanable things at
once in this left-screen slice: dull cobwebbed lamps, wall handprint/splash,
chunky runner footprints, brown mud/dust/ribbon floor pile, and the single
supplied shell-hide bunny. Roshan turns her eyes
and head toward the nearest bunny/mess, makes one tiny ready-to-help gesture,
then settles facing the play space. The room remains dirty; nothing is cleaned
and no instructional pointer is needed.

Keep Roshan's approved child identity, brown rainbow-streaked hair, pink top,
rainbow tail, hands, face, and proportions. No legs, feet, shoes, fused/split
tail, extra characters, bunny clones, generic castle, mirrored screen,
full-screen dimmer, stickers, opaque overlay, UI, text, voice, music, or
generated audio. Keep all architecture and inactive dirt still. Lock the camera
after orientation; hold the final ready posture for at least 0.7 seconds. No
tweening, morphing, optical flow, cross-dissolve, composited cutout, translated
camera/background layer, sprite/rig motion, or duplicated frame may supply
action. Return one complete newly authored flattened shot.
```

## Delivery and review contract

For each of the seven required perspectives (all seven must appear in the
final sequence, with exactly one accepted candidate selected for each):

1. The owner generates at least three independent native study candidates,
   recording the perspective ID, attempt number, model/settings, exact ordered
   uploads, and generation timestamp. Luna authors the prompt and reviews the
   returned candidates; Luna never uploads, submits, or operates Grok.
2. Preserve native study clips and any individually generated complete
   full-frame candidates before trimming, normalization, encoding, or editorial
   assembly. Study clips are evidence only and are never a generation source or
   delivery asset. Do not submit a montage as the generation source.
3. Final cinematic delivery consists only of individually generated, accepted
   complete flattened frames. Every changed delivery frame must be authored and
   reviewed as its own frame; no study-clip frame, interpolation, retime,
   optical flow, morph, cross-dissolve, translated layer, sprite/cutout motion,
   rig, procedural warp, or duplicated motion frame may supply it. Holds are
   allowed only where the rhythm contract declares stillness, and their
   narrative purpose must be recorded.
4. Record the previous and next accepted boundary frames, character passport
   versions, hall/background landmark IDs, bunny IDs, camera crop/scale,
   screen direction, character bounding boxes, eye lines, tail contacts, and
   Daddy's back-room entry/exit state.
5. Luna performs the first visual/technical review at normal speed, silent
   normal speed, half speed, and frame step. Luna must reject identity drift,
   dirt disappearance, bunny duplication, camera churn, contact errors, and
   invented overlays.
6. Sol audits the handoff and candidate evidence against the Scene Direction
   Brief, rhythm contract, character continuity, dirt readability, geography,
   and all hard negative locks. Sol must issue an explicit `ACCEPT` or
   `REJECT`, with shot IDs and repair windows for every rejection.
7. The owner makes the final acceptance decision. No candidate enters runtime
   solely because Grok or an automated metric reports success.

### Split study and delivery manifests

Use separate machine-readable manifests adjacent to the handoff export. A
study manifest may describe a Grok motion study, but a study-derived frame may
never appear in the delivery manifest or delivery directory.

#### `study_manifest.json`

Record one entry per study attempt:

```text
schema_version
scene_id / scene_version
shot_id / perspective_name / study_attempt
generator / model / generation_mode / native_settings
ordered_uploaded_references: file, source_repo_path, role, sha256
study_native_clip_path / study_native_clip_sha256
study_native_dimensions / source_fps / duration / frame_count
study_prompt_path / study_prompt_text / study_prompt_sha256
study_purpose: framing, screen direction, timing, gaze, acting, or blocking
study_derived_frame_prohibited: true
luna_study_review: decision, notes, reviewer, date
sol_study_audit: decision, notes, reviewer, date
```

#### `delivery_manifest.json`

Record one entry for **every individually submitted changed timeline frame and
every attempt**. No clip frame, study frame, interpolated frame, retimed frame,
or derived export qualifies as a delivery entry.

```text
schema_version
scene_id / scene_version
shot_id / perspective_name / timeline_index / attempt
generator / model / generation_mode / native_settings
ordered_uploaded_references: file, source_repo_path, role, sha256
exact_prompt_path / exact_prompt_text / exact_prompt_sha256
generation_method: complete_newly_generated_flattened_frame
full_frame_candidate_path / full_frame_candidate_sha256
native_unnormalized_frame_path / native_unnormalized_frame_sha256
native_dimensions / delivery_dimensions / source_fps / delivery_fps
approved_neighbor_before_path / approved_neighbor_before_sha256
approved_neighbor_after_path / approved_neighbor_after_sha256
approved_neighbor_before_boundary_reason: nullable; required when the
  corresponding before path and SHA-256 are null
approved_neighbor_after_boundary_reason: nullable; required when the
  corresponding after path and SHA-256 are null
action_or_hold_state / declared_motion / hold_purpose / cut_condition
subject_geometry: character IDs, normalized bounding boxes, eye lines, hands,
  tails, active prop, bunny ID, bunny bounding box, and contact state
camera_crop_locks: framing, crop, horizon, fixed landmarks, screen direction,
  camera-lock interval, and permitted camera path
identity_style_locks: passport versions, face, hair, crown, glasses, costume,
  one-tail topology, palette, contours, shading, and dirty-landmark IDs
position_guide_path / position_guide_sha256 / position_guide_role
position_guide_used_as_delivery_pixels: false
forbidden_method_scan
human_identity_review: reviewer, date, decision, notes
human_topology_review: reviewer, date, decision, notes
human_style_review: reviewer, date, decision, notes
luna_review: decision, scores, defects, repair_window, reviewer, date
sol_audit: decision, scores, hard_fail_codes, notes, reviewer, date
owner_acceptance: decision, date
```

When no position guide is used, record null values and
`position_guide_used_as_delivery_pixels: false`. When one is used, it must be
a neutral-field `POSITION_GUIDE_ONLY` guide with the path, SHA-256, and role
`position_only` recorded exactly. The guide may communicate position, bounds,
scale, and orientation only; it may not contribute appearance or pixels.

Recommended manual export layout, following the prior Grok package convention
while separating studies from final-frame candidates:

```text
tmp/grok_day_one_main_hall_entry_20260828/
  README_FIRST.md
  REFERENCE_DECK.md
  study_manifest.json
  delivery_manifest.json
  trial_log.md
  studies/
    SH01_threshold_arrival/attempt_01_native.*
    SH02_right_discovery/attempt_01_native.*
    SH03_daddy_departure/attempt_01_native.*
    SH04_roshan_exploration/attempt_01_native.*
    SH05_bunny_low/attempt_01_native.*
    SH06_left_mess/attempt_01_native.*
    SH07_cleanup_ready/attempt_01_native.*
  delivery_frame_candidates/
    SH01_threshold_arrival/000000/attempt_01_native.png
    SH02_right_discovery/000000/attempt_01_native.png
    SH03_daddy_departure/000000/attempt_01_native.png
    SH04_roshan_exploration/000000/attempt_01_native.png
    SH05_bunny_low/000000/attempt_01_native.png
    SH06_left_mess/000000/attempt_01_native.png
    SH07_cleanup_ready/000000/attempt_01_native.png
  audit/<shot_id>_luna_review.json
  audit/<shot_id>_sol_review.json
  provenance.json
```

The `delivery_frame_candidates/<shot>/<timeline_index>/` directories contain
only complete, individually generated frame attempts. A study-derived frame,
study clip frame, interpolation, retime, normalized replacement, or editorial
export is expressly prohibited there. The `studies/` directory is evidence and
must never be read as a delivery source.

The seven shots must be edited together only after each shot independently
passes review, and the owner must select exactly one accepted candidate for
each perspective. Any final frame sequence must be auditable by
`tools/audit_cinematic.py` and must preserve native candidate files and hashes.
No position guide may contribute delivery pixels; if one is used, it must be a
neutral-field `POSITION_GUIDE_ONLY` guide with `used_as_delivery_pixels: false`
recorded in provenance.

## Luna-generation and Sol-audit checklist

### Luna instruction/review (owner operates Grok)

- [ ] Inventory and preserve the exact ordered references before each shot.
- [ ] Author the prompts and have the owner generate at least three independent
      study candidates for each of the seven required perspectives; Luna never
      uploads or submits to Grok.
- [ ] For every changed final timeline frame, author a separate
      FINAL-DELIVERY-FRAME prompt and have the owner submit one frame request per
      timeline index and per attempt.
- [ ] Confirm Main Hall A/B continuity, fixed doorway landmarks, broad walk
      lane, and the x~2870 curtained back-room arch.
- [ ] Confirm dirt is visible as local physical mess, not as a dimming filter or
      overlay: lamps, wall mark, footprints, floor pile, and three bunnies.
- [ ] Confirm Daddy and Roshan identity, one tail each, no legs/feet/shoes, and
      no Daddy walk-atlas invention.
- [ ] Confirm Daddy departs to the back room while Roshan remains in the hall.
- [ ] Confirm every bunny action has one hop/peek, ground contact, and settle.
- [ ] Review normal speed, silent normal speed, half speed, and frame step.
- [ ] Preserve study candidates separately from individually generated delivery
      frame candidates; record all hashes, boundaries, mandatory frame fields,
      human identity/topology/style reviews, and repair logs.

### Sol audit

- [ ] Handoff structure and reference roles inherit the prior pool handoff
      without granting Grok audio/editorial/approval authority.
- [ ] Scene Direction Brief answers point of view, purpose, emotional change,
      observation, dominant motion, place, performance, rhythm, camera,
      continuity, and exit.
- [ ] Each perspective has one dominant readable action and a meaningful hold.
- [ ] Dirty landmarks remain in correct locations and read at phone size.
- [ ] The three bunny identities remain distinct, child-safe, and non-duplicated.
- [ ] Daddy's back-room destination, Roshan's remaining location, and screen
      direction are unambiguous.
- [ ] No style clash, background repaint, sticker/overlay dirt, camera churn,
      impossible occlusion, contact failure, or character morph is present.
- [ ] Every changed frame is a complete generated frame; forbidden temporal
      shortcuts are absent from provenance and delivery.
- [ ] Delivery contains one accepted candidate for every changed timeline index,
      never a study-derived frame, clip frame, interpolation, or retime.
- [ ] All machine-readable provenance fields, reviewer decisions, repair
      windows, and owner-acceptance fields are complete.
- [ ] Issue explicit `ACCEPT` only when all required shot-level and scene-level
      gates pass; otherwise issue `REJECT` with precise repair instructions.
