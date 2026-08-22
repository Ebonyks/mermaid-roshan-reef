# Cinematic Direction and Intent Protocol

## Purpose

This document defines the conscious pre-generation process for every cinematic
scene. It exists to prevent vague prompts, technically competent images without
meaning, rushed montage pacing, and post-production attempts to invent artistic
intent after the work has been generated.

It is the companion to `TEMPORAL_ANIMATION_INTEGRITY_AND_QUALITY_GATE_PROTOCOL.md`.

- This protocol answers: **What should the audience feel, notice, understand,
  and remember?**
- The Temporal Animation Integrity and Quality Gate answers: **Did the finished
  work faithfully realize that approved intent?**

No generation instruction may be issued until this protocol produces an
approved Scene Direction Brief.

## Foundational principle

The project values patient attention over empty slowness and meaningful motion
over continuous activity. A scene has time to breathe when the audience is able
to inhabit a character's experience of place, thought, feeling, and change.

```text
Character intention
        ↓
Action or discovery
        ↓
Time to observe and feel it
        ↓
Visible consequence
        ↓
Next intention
```

This is the **action–observation–consequence** model. It is a production rule,
not a suggestion.

## Directional influences and boundaries

Use admired films as study references for craft: pacing, observant staging,
environmental life, emotional cause and effect, clear silhouettes, and the
balance of activity and quiet.

Do not copy a specific studio's characters, artwork, shot designs, or signature
visual formula. The project must retain its own original world, character
designs, visual language, and story.

The desired original production language is:

- character-centered and emotionally legible;
- patient but never inert;
- clear in silhouette, staging, and spatial logic;
- early-1990s-cartoon-informed in repeatable construction, controlled contour,
  restrained shading, and purposeful timing;
- delivered at 24 fps when target-device playback permits it;
- selective in animation density: intentional held/on-twos moments for calm,
  unique 24 fps motion for camera moves, turns, contacts, close acting, and
  fast gestures; and
- resistant to contemporary high-detail rendering that makes temporal drift more
  visible.

## The Cinematic Intent Companion

The companion is a structured conversation, not a prompt generator. It must
challenge unclear choices before it writes scene instructions. It is used by the
director or scene owner before any AI, animation, or compositing work begins.

It must never respond to a request such as “make this cinematic” by immediately
generating a visual instruction. It first obtains the choices below.

### Required conversation

Ask, record, and resolve:

1. **Point of view** — Whose experience is the audience following, and what can
   that character perceive now?
2. **Scene purpose** — Why does this scene exist? What would be lost if it were
   removed?
3. **Emotional change** — What does the character feel at the start, and what is
   different at the end?
4. **Concrete event** — What happens in the world?
5. **Observation** — What does the character notice, listen to, consider, or
   choose before acting?
6. **Dominant motion** — What is the one most important movement? What must stay
   still so it reads?
7. **Place** — What does the environment contribute emotionally and physically?
8. **Performance** — What do gaze, pose, hands, timing, and settle communicate?
9. **Rhythm** — Where must the audience orient, breathe, react, and rest?
10. **Camera** — What should framing reveal, protect, wait for, or withhold?
11. **Continuity** — Which character, prop, costume, background, and world-state
    facts cannot change?
12. **Exit** — What completed beat earns the cut to the next scene?

If an answer is “because it looks good,” refine it until it describes audience
experience, character intent, or story consequence.

## Artistic principles

### 1. Stillness is active

Stillness must contain a readable action: looking, listening, choosing, working,
recovering, resting, noticing, or changing. A static image with no subject of
attention is not breathing room; it is dead time.

### 2. One dominant change at a time

Normally, a shot should make one change primary. If the face, body, camera, hair,
background, effects, and props all move with equal force, the audience cannot
tell what matters.

### 3. Motion communicates thought

Movement requires a reason: want, discovery, effort, surprise, care, fear,
relief, play, or decision. Decorative motion is excluded unless it supports the
world's atmosphere without competing with the character.

### 4. Every meaningful action has a shape

Use anticipation, action, reaction, and settle. Hand contact, a turn, a look,
standing, a reveal, or a departure is not complete when the body reaches a new
position; it is complete when the audience has read the consequence.

### 5. The world participates

Backgrounds are not blank waiting rooms. A cabin, stairway, sky, room, weather,
or distant landmark should provide place, scale, atmosphere, and a source of
attention. It must remain spatially stable unless a deliberate change occurs.

### 6. Camera movement earns its place

The camera can orient, reveal, accompany, isolate, or change emphasis. It cannot
merely add activity. During an intimate gaze, touch, or emotional settle, camera
motion is normally locked unless the Scene Direction Brief explicitly calls for
it.

### 7. Cuts follow completion

Cut after the intended feeling/action becomes readable, not at the first frame
where the literal action has occurred. A scene may end on a held connection,
look, or decision.

## Scene Direction Brief

Every scene must result in a versioned brief using this schema.

```text
scene_id and version
scene role in the wider sequence
point_of_view character
scene purpose and required audience takeaway
start state / end state
emotional arc
location, time, and environment role
characters, character-passport versions, props, and continuity locks

beats:
  orientation
  observation
  action
  reaction
  consequence
  exit

rhythm contract:
  delivery frame rate
  orientation hold
  required gaze / discovery / contact / reveal / settle holds
  dominant, secondary, and forbidden simultaneous motion
  camera path and camera-lock intervals
  cut condition

shot plan:
  framing, screen direction, lens/scale intent, depth, transition logic

performance plan:
  gaze, pose, hand/contact, expression, and silhouette requirements

art direction:
  palette, line/shading constraints, detail hierarchy, world-style constraints

generation constraints:
  approved references, layers allowed to vary, layers that must remain locked

acceptance questions and known risks
```

The brief becomes the human-readable source of truth and the machine-readable
input to the animation quality gate.

## Rhythm contract requirements

The rhythm contract makes patient pacing auditable without reducing art to a
timer. It records:

- why the scene needs an orientation period;
- when the audience must understand a character's thought or discovery;
- which hold makes an action emotionally legible;
- which element is allowed to move first and which must remain quiet;
- when the camera may move or must remain locked;
- what visual event justifies the cut; and
- the intended alternation of quiet, motion, and quiet.

Example: a cabin scene involving a child and adult

```text
Audience takeaway: The child feels safe enough to choose the next adventure.
Orientation: Establish the cabin and the pair before anyone stands.
Dominant motion: Child's gaze and head turn toward the destination.
Secondary motion: Adult notices, then shifts gaze; no camera move.
Connection beat: Adult offers hand; child chooses contact.
Required settle: Hold the completed hand contact before movement resumes.
Cut condition: The shared decision to leave is readable.
Forbidden: simultaneous reframing, face/body/hair drift, or unrelated effects
during contact.
```

## Generation instructions

The Companion translates only approved direction into generation instructions.
Those instructions must include:

- scene purpose, point of view, and emotional beat;
- camera/layout and persistent-background requirements;
- approved character reference and exact continuity locks;
- key poses, contact points, and boundary frames;
- temporal context: previous accepted frame, next key/boundary frame, object
  masks, depth order, and landmark tracks;
- motion hierarchy and cadence;
- permitted variation and prohibited changes; and
- the requirement that every repair preserve the Direction Brief.

Never ask an AI to “make it more cinematic” without these constraints. That
invites novelty, camera churn, and identity drift instead of direction.

## Review and revision loop

1. The scene owner completes the Companion conversation.
2. A human approves the Scene Direction Brief before generation.
3. Generation/animation proceeds under that brief.
4. The Temporal Animation Integrity and Quality Gate evaluates the result.
5. Mechanical defects return to animation repair with the brief held fixed.
6. If the scene fails on emotion, rhythm, point of view, or purpose, return to
   this protocol. Do not try to solve an intent failure with random regeneration.
7. A revised brief receives a new version and the scene is re-reviewed.

## Direction acceptance questions

Before approving a scene for production, answer yes to all of these:

- Can someone state whose experience the scene follows?
- Is the emotional change clear and observable?
- Does the setting contribute to the moment?
- Is there a reason for every movement and camera change?
- Is there enough time for the key discovery, feeling, contact, or decision to
  land?
- Would removing a hold lose meaning rather than merely shorten runtime?
- Does the cut arrive after a completed beat?
- Can the scene be described without relying on “more detail,” “more movement,”
  or “more cinematic” as its only rationale?
- Can the quality gate test the declared rhythm, continuity, and performance
  requirements?

If any answer is no, the scene is not ready for generation.

## Relationship to the quality gate

The direction protocol gives the quality gate a standard to enforce. The quality
gate must not invent the intended emotion or pacing after the scene is made.

```text
Cinematic Intent Companion
        ↓
Approved Scene Direction Brief + rhythm contract
        ↓
Generation / animation / compositing
        ↓
Temporal Animation Integrity and Quality Gate
        ↓
Pass, targeted repair, or return to direction
```

This separation preserves artistic authorship. Direction determines the desired
experience; technical and human review ensure the audience receives it.
