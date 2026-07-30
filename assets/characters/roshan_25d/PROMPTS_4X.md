# Mermaid Roshan 4x animation expansion provenance

- Date: 2026-07-26
- Tool path: OpenAI built-in image generation (`image_gen`)
- Use case: `stylized-concept`
- Identity references: `roshan_directional.png`, `roshan_gestures.png`,
  `roshan_play.png`, and `roshan_swim.png`
- Background removal: `remove_chroma_key.py`, border auto-sampling, soft
  matte, thresholds 12/220, and despill
- Runtime normalization: Lanczos resampling to 1024x1024, except the 4x2
  `gesture_d` atlas at 1024x512

Every accepted prompt required the exact same young Mermaid Roshan in every
cell: child face and age, gold aqua-gem tiara, brown wavy hair with rainbow
ponytail, pink ruffled top, pearlescent lavender/aqua scaled tail, rainbow
fins, clean dark-plum outlines, and soft cel shading. All prompts required a
perfectly flat solid `#00ff00` background, crisp opaque silhouettes, complete
limbs and fins, equal cells, consistent scale and padding, no shadows,
gradients, texture, checkerboard, floor, reflections, grid lines, labels,
text, icons, sparkles, watermarks, bubbles, props, or extra objects. They
explicitly prohibited repeated frames, abrupt jumps, pose-order errors,
extra/missing/fused limbs, cropping, identity/costume drift, camera jumps,
and motion blur.

## `roshan_gesture_a.png`

Generation: `exec-25046551-76d2-48a3-8882-e8e66a5af506.png`

```text
Create one exact 4-column by 4-row sprite atlas for four smooth Mermaid
Roshan animations. Each row is one animation and its four columns are four
chronological keyframes: anticipation, transition, peak action, and
settle/return.

Row 1 WAVE: neutral hover with waving hand beginning to lift; hand halfway
up; hand overhead waving at peak; hand lowering while smiling.
Row 2 CHEER: hands near chest; both arms halfway raised; both arms fully
overhead in joyful cheer; arms easing downward.
Row 3 CLAP: hands apart near chest; hands moving inward; palms touching at
clap peak; hands separating.
Row 4 TWIRL: upright wind-up; quarter-turn flowing pose; broad graceful spin
peak with tail and rainbow hair following; settling toward upright.
```

## `roshan_gesture_b.png`

Generation: `exec-c6954d7a-d89b-49bf-8ac3-d213af5966bc.png`

```text
Create one exact 4-column by 4-row sprite atlas for four smooth Mermaid
Roshan animations. Each row is one animation and its four columns are four
chronological keyframes: anticipation, transition, peak action, and
settle/return.

Row 1 LOOK: relaxed forward gaze; eyes and head beginning to turn; curious
full side-look with one hand near chin; gaze easing forward.
Row 2 GIGGLE: warm smile with hands low; hands rising toward mouth; eyes
joyfully closed with both hands at mouth; hands lowering while still smiling.
Row 3 SLEEP: drowsy upright hover; eyes closing and body beginning to curl;
peaceful fully curled sleeping pose with hands tucked; gentle partial uncurl
as if stirring.
Row 4 POINT/REACH: arm low; one arm extending halfway forward; one arm fully
extended in a clear child-readable point/reach; arm retracting halfway.
```

## `roshan_gesture_c.png`

Generation: `exec-a140d9da-f5a0-4c91-9b1b-da28d02d0666.png`

```text
Create one exact 4-column by 4-row sprite atlas for four smooth Mermaid
Roshan animations. Each row is one animation and its four columns are four
chronological keyframes: anticipation, transition, peak action, and
settle/return.

Row 1 COLLECT/SCOOP: open hands low; both hands reaching forward; hands
scooping inward at peak; hands drawing back toward chest.
Row 2 BOING: relaxed hover; tail and body softly squashing/coiling; delighted
upward stretch peak with hands lifted; gentle landing/settle.
Row 3 HAIR-TWIRL: hand low; hand reaching toward the rainbow ponytail;
fingers playfully twirling a rainbow lock at peak; hand releasing and
lowering.
Row 4 HUM: hands moving together; hands clasped with eyes beginning to close;
happy humming sway to one side with eyes closed; small sway to the other side
while settling.
```

## `roshan_gesture_d.png`

Generation: `exec-8e22a7cd-6e6f-46f6-80ae-28a927e1e6f2.png`

```text
Create one exact 4-column by 2-row sprite atlas for two smooth Mermaid Roshan
animations. Each row is one animation and its four columns are four
chronological keyframes.

Row 1 PLAYFUL FLOP: upright wind-up; body tipping sideways with arms lifting;
joyful fully sideways floating flop at peak; recovering halfway toward
upright.
Row 2 CARRY: hands low and open; both hands lifting and cupping forward/up;
stable peak carry pose with both hands distinctly cupped under an imaginary
toy; same carry stance with a gentle body/tail bob for a seamless hold loop.
No toy or object is drawn.
```

## `roshan_play_a.png`

Generation: `exec-2098dbdc-1d84-4731-bf07-7bb92b3cd870.png`

```text
Create one exact 4-column by 4-row sprite atlas for four smooth Mermaid
Roshan playground animations. Each row is one animation and its four columns
are four chronological keyframes.

Row 1 SWING: seated hover with tail curled and both hands gripping two
imaginary ropes at back arc; passing through bottom; forward arc with
body/tail pumping; passing bottom while returning.
Row 2 CLIMB: crouched/coiled reach; pushing upward with hands higher;
airborne full upward reach; catching/settling at the next step.
Row 3 RIDE: ducked start with both hands forward gripping imaginary rails;
beginning the drop; arms lifting in delight; peak wheee pose with both arms
overhead and tail streaming.
Row 4 LAND: descending with arms still high; arms spreading for balance;
soft landing squash with tail coiled; upright settled recovery.

No ropes, rails, slide, seat, playground equipment, or props are drawn.
```

## `roshan_play_b.png`

Generation: `exec-a6d9ee8f-7ced-4db8-937c-907e60324ecb.png`

```text
Create one exact 4-column by 4-row atlas. Each row is one animation with four
chronological keyframes.

Row 1 DIG LEFT: ready; left hand reaching down; left hand at lowest scoop;
left hand drawing back.
Row 2 DIG RIGHT: mirrored ready; right hand reaching down; right hand at
lowest scoop; right hand drawing back.
Row 3 SEATED HOVER: tail curled beneath; both empty hands held forward at
chest height with gently closed fists; gentle upward bob; gentle downward
bob; return to center. Her hands never touch anything.
Row 4 DRY-LAND HOP: tail tightly coiled; launching; airborne apex with arms
lifted; soft landing.

ABSOLUTE OBJECT-FREE RULE: draw only Roshan. Do not draw a bar, rope, handle,
rail, seat, toy, sand, playground equipment, line, stick, or any object in
any cell, including between or beneath her hands.
```

## `roshan_swim_front.png`

Generation: `exec-99a3025f-de32-4cf7-a6d9-4f4e678fc935.png`

```text
Create one exact 4-column by 4-row atlas containing sixteen consecutive
chronological keyframes of one seamless Mermaid Roshan swim cycle, all from
the same FRONT THREE-QUARTER camera view. Reading order is left-to-right,
top-to-bottom.

Frames 1-4: relaxed glide, arms begin reaching forward, arms halfway forward,
arms almost fully forward while tail sweeps from left toward right.
Frames 5-8: full forward/up reach, hands begin sweeping outward, arms halfway
outward, arms fully spread at shoulder height while tail passes center.
Frames 9-12: arms begin sweeping down/back, arms halfway down, arms trailing
gently behind, relaxed powered glide while tail sweeps to the left.
Frames 13-16: arms return low, begin the next reach, halfway toward the
initial pose, final loop-closure pose nearly matching frame 1.

Hair and fins lag the motion naturally. Make every frame distinct but close
enough to its neighbors for smooth playback.
```

## `roshan_swim_back.png`

Generation: `exec-f07bd58e-0288-49c0-83c6-94f008fe0eda.png`

```text
Create one exact 4-column by 4-row atlas containing sixteen consecutive
chronological keyframes of one seamless Mermaid Roshan swim cycle, all from
the same BACK THREE-QUARTER camera view. Her face is not visible; preserve
the brown hair mass, rainbow ponytail, back of tiara, and pink top
consistently. Reading order is left-to-right, top-to-bottom.

Frames 1-4: relaxed glide, arms begin reaching forward, arms halfway forward,
arms almost fully forward while tail sweeps from left toward right.
Frames 5-8: full forward/up reach, hands begin sweeping outward, arms halfway
outward, arms fully spread at shoulder height while tail passes center.
Frames 9-12: arms begin sweeping down/back, arms halfway down, arms trailing
gently behind, relaxed powered glide while tail sweeps left.
Frames 13-16: arms return low, begin the next reach, halfway toward initial
pose, final loop-closure pose nearly matching frame 1.

Hair and fins lag naturally. Make every frame distinct but close enough to
neighbors for smooth playback.
```
