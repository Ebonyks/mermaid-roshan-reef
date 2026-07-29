# Opening Cinematic — Art Direction, Cinematography, and Script Brief V2

Date: 2026-07-26

Status: production-direction proposal for human approval before regeneration

Source under review:
`build/cartoons/opening_cinematic_test.mp4`

Deliverable boundary: this file is a written cinematography, staging, rhythm,
performance, and script handoff for a separate production AI. It does not
authorize this reviewing agent to generate, edit, encode, or integrate video.

## Executive direction

The current 15-second test is an effective event-list animatic and an attractive
collection of individual illustrations. It is not yet a directed scene.

The clearest story already inside it is:

> Roshan feels a small uncertainty, chooses Daddy's hand, experiences safety,
> crosses a threshold with him, and discovers a world that now feels possible.

The next version must protect that sentence. The airplane, buckle, door, stair,
and kingdom are not five equal attractions. They are physical stages in
Roshan's emotional movement from uncertainty to trust to agency to wonder.

The principal cinematography change is therefore not "more camera." It is more
point of view, more completed actions, fewer simultaneous changes, and enough
quiet after each meaningful contact for a four-year-old to read it.

Recommended duration: **42.5 seconds**.

Recommended production master: **24 fps, 1020 frames**, using held or on-twos
animation for calm observation and unique 24 fps drawings only where they
matter: camera moves, gaze changes, hand contacts, the cabin settle, the
threshold crossing, and Roshan's close reaction. An 18 fps delivery version may
be tested later on the Lenovo Tab M11; it must not determine the direction
before the performance works.

All production art remains original Mermaid Roshan 2D artwork. This handoff is
limited to cinematic composition, performance, rhythm, visual continuity, and
editorial intent. Do not imitate another film's protected artwork or shot
design.

## The guide being applied

This brief applies the repository's
`docs/CINEMATIC_DIRECTION_AND_INTENT_PROTOCOL.md` first and
`docs/TEMPORAL_ANIMATION_INTEGRITY_AND_QUALITY_GATE_PROTOCOL.md` second.
They are deliberately different documents.

The direction protocol determines:

- whose experience the audience follows;
- why the scene exists;
- the emotional change;
- what Roshan notices before she acts;
- the dominant movement and what must remain still;
- how the location participates;
- what gaze, hands, posture, and settling communicate;
- where the audience orients, breathes, reacts, and rests;
- what the camera reveals, protects, waits for, or withholds; and
- what completed beat earns every cut.

Its governing structure is:

```text
character intention
    -> action or discovery
    -> time to observe and feel it
    -> visible consequence
    -> next intention
```

That action–observation–consequence chain is currently compressed into an
action–cut–action chain.

The protocol's seven artistic rules are directly relevant:

1. Stillness is active. A held Roshan is looking, listening, deciding, or
   recovering; she is not frozen.
2. One dominant change at a time. During the hand reach, the camera, cabin,
   hair, cape, and background do not all compete with the hand.
3. Motion communicates thought. Eyes move before head, and head before body.
4. Meaningful actions have anticipation, action, reaction, and settle.
5. The world participates. The pendant, cloud light, shell lamp, doorway wind,
   and stair chime support Roshan's experience.
6. Camera movement earns its place. Intimate contact and facial reaction are
   locked; the reveal receives the one expressive camera move.
7. Cuts follow completion. Contact, landing, threshold, and discovery are held
   after the literal event has happened.

The temporal quality gate then proves whether the render faithfully realizes
those choices. It checks frame construction, global identity, stable layouts,
contacts, motion arcs, camera continuity, rhythm, style, encode, and target
playback. A valid 1280×720 H.264 file can pass its technical encode check and
still fail direction completely.

That distinction matches the existing opening-cinematic audit. The prior review
master had correct frame count, rate, duration, codec, and pixel format, but the
production profile still reported 56 non-compensating quality-floor failures.
The audit identifies the reaction close-up as the strongest performance span
and the cabin-release/door and stair/platform spans as the weakest construction,
motion, and contact spans. This brief keeps the close reaction, rebuilds the
threshold logistics, and treats technical validation as evidence after
direction rather than as a substitute for it.

The binding `OPENING_CINEMATIC_270_FRAME_GUIDE.md` and
`guide_parts/continuity_and_qc.md` remain authoritative for character identity,
the two-seat cabin, airplane topology, hand ownership, screen direction, six
steps, two rails, the accepted Sky Lagoon geography, the delayed reveal, and
the UI-free final pose. This brief revises shot duration and cinematographic
emphasis, not those locks.

## What the current 15-second test communicates

Technical facts observed from the supplied MP4:

- 1280×720 H.264;
- exactly 270 frames at 18 fps;
- exactly 15.000 seconds;
- no audio stream;
- SHA-256
  `0CA0E4DD3BDFAFB9F1B4F663B7BFAB3995EFA17C208443F8F1F8FE71926DDEA4`.

At 18 fps, each nine-frame storyboard group receives only 0.5 seconds. The test
therefore asks the audience to process all of the following in fifteen seconds:
flight, cabin orientation, jolt, fear, Daddy noticing, reaching, embracing,
swaying, landing, safe-light recognition, two buckle releases, two rises, aisle
travel, pad activation, door opening, stair deployment, two threshold
transfers, six-step descent, platform balance, invitation, facial recognition,
kingdom reveal, and final handoff composition.

The story remains understandable because the poses are broad and attractive,
but the emotional cause and effect does not have enough screen time to become
felt experience.

### What should be retained

- The pearl plane crossing a bright cloud sea is a clean, immediate tone.
- The two-seat cabin has a readable Roshan-left/Daddy-right relationship.
- Roshan's hand moving toward Daddy is the correct emotional axis.
- The side hug is gentle, belted, and child-safe.
- The shell light changing to aqua is an excellent nonverbal safety cue.
- Daddy demonstrates the buckle before Roshan copies him.
- Daddy leads every threshold action and keeps Roshan connected.
- The open door letting sunlight and wind touch hair and cape makes the world
  participate.
- The exterior stair deployment clearly explains the route.
- F244–F252 contains the sequence's best acting idea: Roshan sees, breathes,
  smiles, and then shares the feeling with Daddy.
- The final rear view points directly toward the destination.

### Directional defects to correct

1. **The opening spoils the discovery.** The island and castle silhouette are
   visible beneath the aircraft in the first second. The binding guide withholds
   readable geography until the final reveal. Replace the island with open cloud
   sea and an ambiguous turquoise glint.
2. **The scene has no settled point of view.** It begins objectively, observes
   the cabin objectively, explains hardware objectively, and shows the map
   objectively. After the exterior orientation, the audience must inhabit
   Roshan's experience. Daddy is sometimes the subject of a shot, but Roshan
   remains the point-of-view character.
3. **The cabin does not orient before the jolt.** The audience sees the two
   characters and the jolt nearly together. Hold the intact cabin, belts,
   porthole light, and pendant before anything changes.
4. **Fear advances too quickly.** Roshan tightens, looks, reaches, and receives
   reassurance in roughly two seconds. Let her notice the pendant and cloud
   movement, then let her eyes find Daddy, then let her choose contact.
5. **The hug arrives but does not land.** The hug, sway, eye close, smile, and
   release are all present, but each receives only fractions of a second. Hold
   completed contact. The audience should feel her breathing slow.
6. **The landing insert contradicts the guide.** F091–F099 invents visible
   landing gear and a tiled runway/platform, despite the binding instruction to
   keep landing gear outside the composition and not invent a runway. Remove the
   entire exterior wheel shot. Experience touchdown from inside the hug.
7. **The safe cue is not given its own observation.** Let the pendant settle
   first; let the aqua shell light glow second; let Roshan notice it third.
8. **Standing is physically and emotionally rushed.** Daddy moves from seated
   to upright in only a few displayed frames, and Roshan accepts his hand and
   rises immediately. Daddy must plant his tail, rise, settle, offer, and wait.
   Roshan must look at the hand, look at him, decide, make contact, then rise.
9. **The doorway breeze is good but abbreviated.** This is the first sensory
   touch from the new world. Hold it. Roshan's hair streak lifts first, her eyes
   brighten second, and Daddy waits.
10. **Stair deployment reads as a hardware montage.** Give it a single locked
    wide, a visible destination platform from the first frame, four clear
    mechanical stages, and a completion hold. The stair must visibly meet the
    platform before either character moves.
11. **The threshold sequence explains every pose but not the feeling of
    crossing.** Use fewer camera setups, preserve the upper-left to lower-right
    diagonal, and make Daddy's look back the controlling beat.
12. **The platform arrival skips Roshan's final transfer.** In the current
    sequence she is on the stair in one image and effectively settled on the
    platform in the next. Show tail-to-platform contact, Daddy's counterbalance,
    Roshan checking the contact, and both bodies settling.
13. **The invitation changes viewpoint inside a supposed locked shot.**
    F235–F243 moves from front/side to rear without a clean, continuous,
    motivated camera path. Use a locked side two-shot. Save the camera move for
    the wide reveal.
14. **The reveal is a checklist rather than a hierarchy.** Castle, path,
    playground, river, mountains, and props are presented with similar weight,
    like a theme-park map. The castle and path are the first read. Playground
    color is second. Water and mountains are atmospheric third reads.
15. **The final action contradicts the handhold lock.** In F265–F270 Roshan
    releases Daddy and starts forward while he waves. The guide requires them
    to hold hands through F270. Player input may motivate a later release; the
    cinematic may not.
16. **Production labels enter the picture.** Frame labels are visible from F136
    onward. They are review metadata and must never appear in the clean master.
17. **The rendering is too independently redrawn.** Fine costume filigree,
    crowns, hair, hands, tails, stairs, and background geometry change subtly
    between panels. Use canonical locked 2D character and set layers and
    regenerate only the smallest moving part or coherent repair window.

## Ghibli-derived cinematography principles

These are craft influences, not a request to imitate Studio Ghibli artwork,
characters, compositions, or a proprietary visual formula. Mermaid Roshan keeps
its own protected character art, early-1990s-cartoon-informed construction, and
storybook world.

### My Neighbour Totoro — child pace and environmental attention

The useful influence is the willingness to tell a child-scale event at the
child's pace. BFI describes the film as a less-is-more story built from
carefully constructed sequences and wide-eyed attention to nature, connection,
and change. Apply that idea to Roshan noticing the pendant, the porthole light,
the entering wind, and Daddy's waiting hand. A cloud or breeze is not filler;
it is something she experiences.

Production translation:

- place the cabin camera near Roshan's seated eye height;
- let her eyes discover before the edit explains;
- keep the room still enough that one small movement reads;
- use the world as a companion to emotion, never as decorative noise.

Reference:
https://www.bfi.org.uk/film/659f87a6-000d-59a5-b3ab-536f10de2c39/my-neighbour-totoro

### Miyazaki's “ma” — space that makes action meaningful

In his Roger Ebert interview, Miyazaki explained the value of the interval
between actions and warned that nonstop activity becomes busyness. The
repository direction protocol makes the same distinction as “patient attention
over empty slowness.”

Production translation:

- after the hand closes, hold the contact;
- after the hug settles, let Roshan exhale;
- after the shell light turns aqua, let her see it;
- after the stair meets the platform, hold the safe route;
- after the kingdom appears, stop moving the camera.

Reference:
https://www.rogerebert.com/interviews/hayao-miyazaki-interview

### Kiki's Delivery Service and Porco Rosso — flight with weight and air

The useful influence is not an airplane design. It is spatial confidence in
flight: a stable horizon, layered cloud parallax, a vehicle that holds its mass,
and wind that has visible consequences. The current shot-to-shot scale pumping
should become one calm crossing of a stable sky.

Production translation:

- keep the camera nearly locked while the plane crosses left-to-right;
- use restrained near, middle, and far cloud parallax;
- allow only one small wing flex and one highlight travel;
- match the exterior porthole position to the cabin porthole cut;
- do not use a chase-camera swoop, barrel roll, push-in, or island flyover.

References:
https://www.bfi.org.uk/lists/5-things-watch-weekend-20-22-december
and https://www.ghibli.jp/works/

### Spirited Away — thresholds and reaction before spectacle

The useful influence is the seriousness given to crossing into a new world.
The audience understands a threshold because the character pauses, observes,
then crosses. BFI also highlights the film's quiet train passage as a period in
which the audience can process prior events.

Production translation:

- the door opening is not the same beat as leaving;
- wind reaches Roshan before she crosses;
- Daddy tests the stair before asking her to follow;
- the close reaction comes before the map-like wide;
- the final wide is held long enough to let the world become a place.

References:
https://www.bfi.org.uk/film/f25b5afd-4b55-598b-8bed-f284de120f94/spirited-away
and
https://www.bfi.org.uk/lists/10-great-animated-coming-age-films

### Isao Takahata / Only Yesterday — small performance, not face replacement

The useful influence is restrained facial acting: tiny eye, cheek, mouth, and
posture changes that remain within one stable character construction. The BFI
notes the quiet naturalist attention to small muscle movement in *Only
Yesterday*.

Production translation:

- do not swap expressions by regenerating a new face;
- maintain one locked face base and animate eyes, brows, lids, mouth, and cheek
  tint as separate controlled layers;
- let Daddy's eyes move before his head;
- let Roshan's mouth part before her smile;
- let Daddy watch Roshan's response before he looks at the kingdom.

Reference:
https://www.bfi.org.uk/lists/great-japanese-film-every-year-from-1925-now

## Approved Scene Direction Brief, proposed V2

### Scene identity

```text
scene_id: OPENING_ARRIVAL
version: direction-v2-proposed
working title: The Reef Is Waiting
duration: 42.5 seconds
master cadence: 24 fps, 1020 displayed frames
point of view: Roshan after the opening exterior orientation
```

### Scene role

Introduce Roshan and Daddy's relationship, prove that the journey is safe, let
Roshan choose the transition into the world, reveal Sky Lagoon as an invitation,
and hand off to play without an emotional or camera discontinuity.

### Required audience takeaway

“Roshan was a little unsure, Daddy stayed with her, she chose to go forward, and
the beautiful reef is ready for her.”

### Start and end state

- Start: Roshan is physically safe but internally uncertain; the destination is
  unknown.
- End: Roshan is calm, connected, facing a clear destination, and ready to act.
  Daddy has not pulled her forward; she has chosen readiness.

### Emotional arc

```text
small sensory uncertainty
    -> seeks Daddy
    -> contact and regulated calm
    -> sees objective safety cues
    -> copies a manageable action
    -> accepts a hand and crosses
    -> wonder
    -> readiness
```

### Location and environment role

- The sky establishes gentleness, scale, and possibility.
- The cabin provides a small, stable, protective room.
- The pendant makes the jolt and settle legible.
- The aqua shell light makes safety legible without reading.
- Doorway wind makes the new world touch Roshan before she enters it.
- The stair turns open sky into a visible, finite, supported route.
- Sky Lagoon resolves from color and light into navigable geography.

### Continuity locks

All locks in the 270-frame guide remain binding, especially:

- exactly two passenger seats;
- Roshan screen-left and Daddy screen-right until the approved rear reveal;
- Roshan's left hand and Daddy's right hand are the continuing inner pair;
- belts remain closed until their demonstrated release and then rest beside
  their own cushions;
- no legs, feet, shoes, fused tails, owner-swapped flukes, or changed costumes;
- aircraft nose/door remain screen-right;
- the door opens forward/outward;
- exactly six pearl steps, exactly two lavender rails, and a separate platform;
- Daddy leads and Roshan is never alone outside;
- the kingdom is not readable before the final reveal;
- accepted castle/path/playground/water/mountain geography;
- no HUD through the final cinematic frame;
- hand contact remains through the final frame.

### Beat plan

```text
orientation: gentle flight, then intact two-seat cabin
observation: Roshan notices the jolt and Daddy notices Roshan
action: Roshan chooses his hand and they hug
reaction: her breathing and expression settle
consequence: landing and aqua light prove safety
next action: she copies the buckle, accepts his hand, and crosses
discovery: wind, platform, and Daddy's invitation lead her gaze
reaction: wonder becomes a smile shared with Daddy
consequence: the kingdom becomes navigable, not merely spectacular
exit: stable handhold and final rear composition
```

### Rhythm contract

- Every shot begins with enough spatial information to identify subject and
  state before the primary movement.
- Hand reach order: eyes to hand, eyes to Daddy, fingers open, arm moves,
  contact closes, contact holds.
- Hug order: invitation, lean, torso contact, arm closure, shared sway, exhale,
  settle.
- Landing order: whole cabin dips, bodies and cushions respond, pendant follows,
  system rebounds, pendant settles, light changes, Roshan observes.
- Rise order: Daddy tail plant, push, vertical motion, cape follow-through,
  settle, hand offer, wait; Roshan look, decide, contact, rise, settle.
- Door order: pad contact, seam light, door motion, wind entry, Roshan reaction,
  hold.
- Stair order: mechanism deploys completely and safely before locomotion begins.
- Reveal order: Daddy invites, Roshan looks, close reaction completes, then
  camera reveals.
- Camera locks during hand contact, hug, buckle, close reaction, and final hold.
- The only expressive camera move is the kingdom reveal.
- Quiet–motion–quiet alternation is mandatory in every action shot.

### Performance plan

Roshan:

- uncertainty is small: fingers tighten, shoulders rise slightly, breath catches;
- she never cries, recoils, or appears endangered;
- gaze motivates every body action;
- reaching and crossing are voluntary choices;
- wonder begins as stillness and widened attention, not an immediate oversized
  grin;
- final expression is confident delight.

Daddy:

- notices with eyes before head;
- never grabs, pulls, rushes, or blocks Roshan's face;
- offers an open hand and waits;
- checks every contact and the stair before moving;
- watches Roshan's reaction more than the spectacle;
- pride is warm and quiet, not presentational showmanship.

## Revised cinematography and production-AI shot plan

Lens numbers below describe perspective intent rather than a required technical
camera implementation. Reproduce the framing, scale relationships, depth,
parallax, and screen direction faithfully in the production medium.

| Shot | Seconds | Frames at 24 fps | Framing and camera | Dominant action | Required stillness and cut condition |
|---|---:|---:|---|---|---|
| 01 — Open sky | 0.00–2.00 | F001–F048 | 55 mm-feel extreme wide; horizon upper-middle; locked camera; plane enters left and travels right through layered clouds. No island. | Plane crosses about one third of frame; one restrained wing flex. | Horizon and plane topology locked. Cut when a porthole catches one small glint and forward motion is established. |
| 02 — Safe room | 2.00–4.00 | F049–F096 | Match porthole glint to 35 mm-feel, Roshan-eye-height cabin wide. Exactly two seats. | After 0.7 s orientation, one mild 1.5° jolt moves cabin and occupants as one system. | No face acting before the jolt. Hold the rebound long enough to see both belts remain closed. |
| 03 — Roshan notices | 4.00–6.00 | F097–F144 | Locked 60 mm medium on Roshan with Daddy present but secondary at frame-right. Pendant and porthole remain visible. | Pendant completes a small arc; Roshan's fingers tighten, then eyes move toward Daddy. | Daddy body, camera, background, and shell light stay quiet. Cut after Roshan has chosen where to look. |
| 04 — Daddy notices | 6.00–7.50 | F145–F180 | Locked 55 mm two-shot favoring Daddy's face and Roshan's hand. | Daddy's eyes move to her hand, then his head turns; his right palm opens. | Roshan holds her look. No camera push. Cut only after the open palm is readable. |
| 05 — The choice | 7.50–9.50 | F181–F228 | 65 mm medium-close including both faces and the full hand path. | Roshan looks palm→Daddy→palm, opens her left fingers, reaches, and closes contact with his right hand. | Pendant nearly still; Daddy's arm waits. Hold completed contact at least 12 displayed frames. |
| 06 — Reassurance | 9.50–12.00 | F229–F288 | Locked 48 mm medium two-shot; preserve both faces, belts, and separate tails. | Daddy opens his right arm; Roshan leans; arm closes; one slow supported sway. | No camera movement or unrelated sparkle. Cut after Roshan exhales and her shoulders lower. |
| 07 — Arrival felt inside | 12.00–14.25 | F289–F342 | Continue the same axis, widen only 5% to include pendant and aqua wall shell. No exterior wheel insert. | Whole cabin compresses about 2% on touchdown, rebounds, and settles; aqua shell light turns on after the pendant nears vertical. | Hug remains secure through impact. Hold on Roshan seeing the light and forming a small smile. |
| 08 — Daddy demonstrates | 14.25–16.75 | F343–F402 | Locked 45 mm medium-wide showing both lap buckles and both faces. | Daddy releases hug, nods, presses and opens only his buckle, then lays both halves beside his cushion. | Roshan watches; her belt remains closed. Cut when Daddy's hands leave the open belt and look returns to Roshan. |
| 09 — Roshan copies | 16.75–18.50 | F403–F444 | Same camera and scale; do not cut closer. | Roshan checks Daddy's open belt, presses her shell buckle, opens it, and places halves beside her cushion. | Daddy waits without moving her hands. Cut on her proud look up, not on the buckle's first opening frame. |
| 10 — The offered hand | 18.50–21.50 | F445–F516 | 40 mm full two-shot showing seats, tail support, belt halves, and floor. | Daddy plants tail, rises, settles, offers right hand; Roshan observes, accepts with left, rises, and settles. | One person moves at a time. The hand offer must visibly wait. Cut only when both are balanced and connected. |
| 11 — Together to the door | 21.50–23.50 | F517–F564 | 40 mm side/rear three-quarter track; camera translates right at the same average speed as the pair. | Two gentle tail-glide pulses; Daddy leads. | Exactly two seats recede without changing. No zoom. End with both stopped before the closed door. |
| 12 — New air | 23.50–26.00 | F565–F624 | Locked 50 mm door-side medium. Door remains screen-right. | Daddy's left hand presses pad; aqua seam traces; door opens outward; sunlight and wind enter; Roshan's hair streak lifts and she inhales. | Their joined hands and bodies remain stable. Hold 0.6 s after the breeze touches Roshan. |
| 13 — A complete safe route | 26.00–28.50 | F625–F684 | Cut outside to locked 32 mm wide. Plane upper-left, separate landing platform lower-right and visible from frame one. | Cassette slides outward, pivots down, six steps unfold, two rails extend, stair meets platform, completion light travels once. | Roshan and Daddy remain framed in doorway. No person moves until a 0.7 s completion hold proves the bridge. |
| 14 — Crossing | 28.50–32.50 | F685–F780 | 42 mm low side profile; stable upper-left to lower-right diagonal; a restrained parallel track may follow downward without changing lens. | Daddy tests first tread and looks back; Roshan crosses; they descend with Daddy one tread ahead; Daddy reaches platform and steadies her final transfer. | Show actual tail-to-tread and tail-to-platform contacts. No pose teleport. End only after both tails and torsos settle on the platform. |
| 15 — Invitation | 32.50–34.75 | F781–F834 | Locked 55 mm side two-shot at Roshan eye height. Kingdom remains offscreen; at most one finial and warm color reflection. | Daddy looks toward unseen kingdom, then looks to Roshan and gently inclines his head. Roshan follows his gaze. | No camera orbit. Hair and cape answer one breeze and settle. Cut after Roshan's eyes land offscreen. |
| 16 — Wonder arrives | 34.75–37.50 | F835–F900 | Locked 75 mm front close two-shot from kingdom side. Keep joined hands or Daddy's reassuring shoulder contact in lower frame. | Roshan's pupils rise, mouth parts, breath pauses, then a smile forms; Daddy watches her first, then shares her gaze. | Face construction cannot change. Hold the shared glance. Cut when Roshan turns her attention back toward the kingdom. |
| 17 — The reef is waiting | 37.50–41.00 | F901–F984 | 28 mm-feel rear hero wide. Begin close behind their shoulders, crane up and ease back for 1.2 s, then lock for 2.3 s. Castle/path first read, playground second, water/mountains third. | Roshan's free right hand lifts slightly toward the path. Two butterflies and one distant train puff may move; nothing else competes. | Camera stops completely before the final second. Do not pan across attractions. Hold until the path and castle read as the playable destination. |
| 18 — Final handoff | 41.00–42.50 | F985–F1020 | Cut or ease to the approved 38°-FOV rear composition, UI-free. | Roshan lowers her free hand. Daddy and Roshan keep inner hands joined; both settle. One warm wayfinding sparkle appears left of path. | No waving, walking, hand release, camera drift, or HUD. End only after the composition and both characters have fully settled. |

## Production-AI staging constraints

### Persistent layers

Create and version these once:

- cabin background plate with exactly two seats;
- Roshan canonical 2D body, face base, hair, rainbow streak, hands, tail, fluke,
  belt, and buckle layers;
- Daddy canonical 2D body, face base, glasses, crown, coat, filigree, cape,
  hands, tail, fluke, belt, and buckle layers;
- plane exterior plate;
- door, pad, seam light, stair cassette, six tread layers, two rail layers,
  platform, and completion light;
- Sky Lagoon hero plate with locked landmark IDs and depth-separated foreground,
  midground, and background;
- cloud parallax bands, doorway breeze displacement, pendant, shell lights,
  restrained butterflies, train puff, and wayfinding sparkle.

Do not redraw an entire character because eyes, fingers, or cloth need to move.
Repair the smallest coherent layer window while preserving accepted boundaries.

### Motion density

- Calm holds: base art on twos, with only gaze/blink/breath layers changing.
- Camera translation, hand approach, contact closure, doorway opening, stair
  deployment, final tail contact, and facial close acting: unique 24 fps motion
  where needed.
- Hair and cape follow primary motion by 2–4 frames and settle once.
- No perpetual bobbing, sparkle storms, independent cloth flutter, or uniform
  movement on every layer.

### Camera and layout locks

For every shot, record:

- shot ID and version;
- background plate and visible layer IDs;
- camera framing, crop, scale, lens/FOV intent, and permitted path;
- horizon and two static landmark coordinates;
- character bounding boxes and eye lines;
- hand, belt, stair, rail, tail, and platform contact states;
- intended front-to-back order, masks, and foreground framing;
- first/last approved boundary frames.

Any undeclared camera, crop, scale, horizon, axis, character proportion,
landmark, contact, or foreground-framing change is a defect, even if the
individual frame is pretty.

### Absolute negative constraints

- no Studio Ghibli characters, designs, painted backgrounds, copied shots, or
  style imitation;
- no runway, landing wheel, airport, pilot, cockpit, controls, crew, luggage,
  extra seat, or extra passenger;
- no readable kingdom before Shot 17;
- no camera movement during the hand reach, hug, buckles, or reaction close-up;
- no label, caption, watermark, dialogue text, or UI;
- no hand-owner swap, merged fingers, contact slide, fused tails, legs, feet, or
  shoes;
- no extra or missing stair, rail, platform, porthole, door, emblem, crown,
  glasses, or hair streak;
- no open castle door, relocated playground, tropical palm, fog, extra sun, or
  generic theme-park castle;
- no final hand release or walking before the cut.

## Timed screenplay and audio script

This script must remain visually understandable with audio muted. Dialogue is
brief support, never exposition.

Any new Daddy dialogue requires a **new separately recorded family clip**.
Never cut, pitch, time-stretch, clone, overwrite, or repurpose sacred
`daddy1.ogg`, `daddy2.ogg`, or `daddy3.ogg`.

### OPENING — “THE REEF IS WAITING”

**0.00–2.00 s — EXT. CLOUD SEA — DAY**

A small pearl-and-lavender passenger jet glides left-to-right through a deep,
quiet sky. Near clouds pass slowly. Far clouds barely move. The destination is
not visible.

SOUND: Soft air. A distant, warm engine hum. Three sparse music notes with room
between them.

**2.00–4.00 s — INT. TWO-SEAT CABIN — CONTINUOUS**

Roshan sits window-side. Daddy sits beside her. Both belts are closed. The shell
pendant hangs nearly still.

The cabin gives one small, harmless roll. Seats, bodies, tails, pendant, window
light, and cape move together. Everything returns.

SOUND: Gentle cabin hum; one soft pearl chime from the pendant; no alarm.

**4.00–6.00 s — ROSHAN**

The pendant completes its arc. Roshan's left fingers press into the armrest.
Her eyes follow the pendant, then find Daddy.

She does not panic. She considers.

SOUND: Roshan's small inhale. Music leaves space.

**6.00–7.50 s — DADDY**

Daddy notices her hand first. His eyes soften. He turns his head and opens his
right palm between them.

He does not reach across the space. He waits.

**7.50–9.50 s — THEIR HANDS AND FACES**

Roshan looks at the open palm, up to Daddy, and back to the palm. Her left hand
leaves the armrest. Their fingers close gently.

DADDY, quiet:
“I'm right here, Roshan.”

They hold contact.

**9.50–12.00 s — THE HUG**

Daddy opens his right arm. Roshan leans in by choice. He wraps her securely
without hiding her face. They make one slow, supported sway.

Roshan exhales. Her shoulders lower. Her eyes close for one comfortable beat
and reopen.

SOUND: Cloth and scales shift softly. Music resolves the opening phrase.

**12.00–14.25 s — ARRIVAL**

Still together, they feel one feather-soft downward compression and rebound.
The pendant lags, swings, and returns toward vertical.

Only then, the wall shell changes from warm amber to calm aqua.

Roshan sees it. A small smile begins.

DADDY, almost a whisper:
“We're here.”

SOUND: Soft landing “whump,” followed by a clear two-note aqua chime.

**14.25–16.75 s — DADDY'S BUCKLE**

Daddy releases the hug but keeps his body turned toward Roshan. He nods toward
the aqua shell, then down to his lap. He presses his shell buckle, separates
the halves, and places them neatly beside his cushion.

Roshan watches every step.

**16.75–18.50 s — ROSHAN'S BUCKLE**

Roshan checks Daddy's open belt, then presses her own shell buckle. It opens.
She places both halves beside her cushion exactly as he did.

She looks up, proud.

DADDY:
“Ready?”

Roshan gives one clear nod.

ROSHAN, bright but small:
“Ready.”

**18.50–21.50 s — RISING**

Daddy plants the lower curve of his tail, presses on the armrest, rises, and
settles in the aisle. His cape follows and becomes still.

He offers his right hand.

Roshan looks at the hand, looks at him, and accepts with her left. She plants
her tail, rises, and settles beside him.

Their joined hands remain between them.

**21.50–23.50 s — THE AISLE**

Daddy leads with two gentle tail-glides. Roshan follows, still connected. The
two empty seats recede behind them.

They stop together at the closed forward door.

SOUND: Two soft scale-and-carpet swishes.

**23.50–26.00 s — THE DOOR**

Daddy touches the aqua shell pad with his free left hand. Light traces the door
seam. The door opens forward and outward.

Warm daylight enters. A clean breeze lifts Roshan's rainbow streak, then
Daddy's cape. Roshan inhales the new air and looks beyond the sill.

No kingdom is visible yet—only sky.

SOUND: Shell-pad tone; soft door mechanism; wind grows present.

**26.00–28.50 s — THE STAIR**

From outside, the landing platform is already visible below and to the right.
The stair cassette slides out beneath the sill, pivots down, unfolds exactly
six pearl treads, and raises exactly two lavender rails. It settles onto the
platform with no gap.

A small aqua-gold light travels down the completed route once.

Daddy and Roshan wait in the doorway until the light reaches the platform.

SOUND: Four rounded pearl clacks, then one reassuring completion chime.

**28.50–32.50 s — THE CROSSING**

Daddy keeps Roshan's hand, takes the nearer rail with his left, and tests the
top tread. He looks back to her.

Roshan chooses forward. Her tail meets the first tread. Daddy stays one tread
ahead, never pulling.

They descend together. Daddy reaches the platform, turns, and gives Roshan room.
Her tail touches the platform. She checks the contact. He counterbalances her
hand until both are steady.

SOUND: Soft tread notes descending in pitch; wind; no danger cue.

**32.50–34.75 s — THE INVITATION**

On the platform, Daddy looks toward something beyond frame. Before presenting
it, he looks back at Roshan.

He gives one small, encouraging incline of his head.

DADDY:
“Look, Roshan.”

Roshan follows his gaze. The breeze settles.

**34.75–37.50 s — ROSHAN SEES**

In close view, warm lavender, gold, aqua, and green reflect in Roshan's eyes.
Her pupils rise. Her lips part in a quiet breath. Wonder becomes a smile.

Daddy watches her—not the view.

Roshan looks up to Daddy. He answers with the smallest nod. She looks back.

ROSHAN, softly:
“Wow.”

**37.50–41.00 s — THE REEF**

The camera eases behind them and rises just enough to reveal Sky Lagoon.

The pearl-lavender castle and straight path read first. The playground's
rainbow shapes read second. Water, mountains, village, trees, and distant
activity give the world depth without demanding attention.

Roshan lifts her free right hand toward the path. Two butterflies cross a patch
of sunlight. A distant train gives one small puff.

The camera stops. The world breathes.

DADDY, warm:
“Your reef is waiting.”

SOUND: Main theme opens into its fullest statement, still gentle. Water, wind,
one distant bird, no crowd roar.

**41.00–42.50 s — FINAL HOLD**

The frame settles into the approved rear composition. Roshan lowers her free
hand. She and Daddy remain hand-in-hand, facing the castle.

One warm sparkle appears beside the left edge of the path.

Music lands on a held, welcoming chord.

No one walks. No one waves. No hand releases. No interface appears.

End on the held composition after the music and ambient sound have settled.

## Acceptance questions

Human direction approval requires “yes” to all:

- Is the scene unmistakably Roshan's experience after the opening exterior?
- Does she move from small uncertainty to calm, then choose the next action?
- Is Daddy's care shown through waiting, gaze, and support rather than pulling?
- Does every camera move orient, reveal, accompany, or change emphasis?
- Does the camera stay locked during intimate contact and facial settling?
- Does every meaningful action include anticipation, action, reaction, and
  settle?
- Does the world participate through pendant, light, wind, stair, and landscape?
- Is the kingdom withheld until Roshan has earned and emotionally registered it?
- Can a non-reader understand safety, sequence, and destination with sound off?
- Would removing each specified hold remove meaning, not merely shorten the
  sequence?
- Does each cut occur after the completed beat is readable?
- Does the final frame preserve hand contact, geography, and the approved
  UI-free handoff composition?

Production acceptance additionally requires every temporal quality gate:
frame integrity, action windows, scene congruency, character passport,
interaction/contact, camera/editorial continuity, rhythm, whole-cinematic
coherence, encode, and target-device playback.
