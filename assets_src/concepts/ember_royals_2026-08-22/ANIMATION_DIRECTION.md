# Ember Royals animation direction

Status: motion-development canon for `ember_king_motion_concept_v1.png` and
`ember_prince_motion_concept_v2.png`, based on `ember_king_concept_v6.png` and
`ember_prince_concept_v4.png`. These are review/source concepts, not accepted
runtime atlases or gameplay specifications.

## Shared rules

- Animate as true 2D with stable pivots and opaque, phone-readable silhouettes.
- Every action follows anticipation, readable action, contact/payoff, and
  settle. Speed comes from spacing and timing, never hidden poses or blur.
- Author for a 30 fps game. Core loops can use six to eight unique drawings
  with held frames; important acting poses should survive at least two frames.
- Secondary motion clarifies mass, then rests. Avoid constant hair, cloth,
  shell, flame, particle, or tail noise in idle loops.
- Keep faces, hands, feet, shell edges, and garment silhouettes readable. Fire
  and ice effects stay away from the face and torso whenever possible.
- No predatory charge, shell spin, violent impact, injury, punitive knockback,
  or fail-state acting.

## Ember King: blundering weight

His foot reaches the pose first; hips and torso compress next; shell,
shoulders, hair, and huge cape arrive late. His body keeps exposing the eager,
awkward feelings that his practiced bored expression tries to hide.

### Heavy walk

- Target loop: about 0.9 seconds, eight drawings, asymmetrical four-beat rhythm.
- Pose order: raised-foot anticipation; broad foot contact; deep compression;
  passing body; shell catch-up; awkward overstep; cape drag; annoyed upright
  recovery into the opposite step.
- Keep his feet close to the floor. One small rounded ember puff may mark a hard
  contact, but the step communicates weight rather than damage.
- The head tries to stay aloof and level while the torso bobs beneath it. One
  eye may widen during the overstep before returning to a half-lidded stare.
- The two cape panels lag the torso by one or two frames, remain tailored around
  the shell, overshoot, and then come fully to rest.

### Idle and turn

- Idle is a sparse two-to-three-second phrase: slouch, breath, slow blink or eye
  roll, small shoulder correction, then stillness. A hand can gather the cape
  edge like an oversized favorite hoodie.
- An interesting object triggers a two-pose eye/head snap before he deliberately
  resumes the slouch. The candle is scene-specific story business and does not
  belong in the reusable idle art.
- Turn target: 0.5 to 0.7 seconds over five poses. Eyes turn first, then head,
  shoulders/torso, hips/feet, and finally shell/cape with a broad soft settle.

### Blunder, eager burst, cape fan, and brace

- Blunder target: about 0.8 seconds. One foot advances too far, torso continues,
  arms and cape counterbalance, and a second heavy plant catches him. Hold the
  embarrassed realization briefly, then reset the cape into bored dignity.
- Eager burst target: about 0.5 seconds. Lean, two or three unexpectedly quick
  heavy steps, abrupt stop, shell/cape catch-up, pretend-calm settle.
- Cape fan target: about 0.8 seconds. Gather and lean back; lift the broad edge;
  sweep one clean arc; show a rounded warm gust; overshoot and settle.
- Shell brace is a planted half-turn toward a harmless incoming object. Never
  curl him into the shell or spin him.

## Ember Prince: sleek evasion

His motion is narrow, diagonal, and economical. Eyes choose the path before the
body commits. His anatomical shell stays close and controlled while hair, coat
tails, and tail draw restrained follow-through arcs.

### Non-negotiable shell construction

- The shell grows from the Prince's exposed coral-red scaled back. It never
  behaves as a backpack, armor plate, or object laid over the coat.
- A continuous red skin halo remains visible around the complete shell in every
  side, rear, turn, crouch, guard, and transition drawing.
- The jacket's center-back panel is absent. No fabric may appear beneath,
  behind, across, or over the shell, even for a single in-between frame.
- Jacket edges terminate outside the skin halo. The two coat tails begin below
  the opening and split around a visible red-skinned tail root.
- Use `ember_prince_concept_v4.png` and the rear poses in
  `ember_prince_motion_concept_v2.png` as construction authority. Motion V1 and
  character V3 retain the earlier layering error and are superseded evidence.

### Sleek walk and Cinderstep

- Walk target: about 0.65 seconds, eight drawings. Use soft toe-led or
  heel-to-toe contacts, long passing poses, level shoulders, little vertical
  bounce, and a narrow silhouette.
- The tail counterbalances without whipping. Hair and coat tails lag the hips
  by one frame, then align before the next contact; the shell stays stable.
- Cinderstep target: 0.4 to 0.5 seconds over five poses: low diagonal crouch,
  compressed launch, extended passing pose, soft landing, upright settle.
- Wider launch-to-passing spacing creates speed. A short ember footprint may
  remain after he leaves; no teleport flash, smoke cloud, or full-body streak.

### Evasion, shell guard, and decision

- Evasive sidestep target: about 0.5 seconds. Eyes locate the incoming object;
  one foot slips sideways; torso turns; tail reaches opposite; trailing foot
  closes. Hair and coat tails settle one beat later.
- Shell guard target: about 0.6 seconds. Plant, pivot, present the natural shell
  at a protective angle, hold safe contact for two frames, and unwind. Preserve
  the red skin halo and empty jacket opening throughout.
- Idle is a sparse breath, glance toward the King, fingers at the ember-heart
  clasp, then stillness. His decision phrase is hesitation, backward glance,
  hand near clasp, weight shift, and one clean confident step.

## Fire and ice motion language

- Warm actions use short coral/orange arcs, rounded ember puffs, expansion, and
  broad outward timing. Cool actions use aqua/lavender crescents, small crystal
  paths, gentle holds, and cleaner pauses.
- Fire is not villain animation and ice is not hero animation. Either can help,
  obstruct, reveal, slow, warm, cool, or make a safe route.
- Combined actions resolve with high-key steam, rainbow mist, or cooled
  obsidian. Effects follow the readable action and never hide the silhouette.

## Paired family timing

Use `ember_royals_family_journey_concept_v1.png` as the acting reference for
their shared travel rhythm. The unseen candle motivates the King alone.

- Normal travel uses a repeating offset: the King plants heavily on the beat;
  the Prince crosses the same space about a quarter-beat later with one sleek
  step. Their feet should rarely contact together.
- When the King notices the candle, his eyes and head snap toward it and his
  whole body follows. The Prince's eyes snap toward the King instead. Never give
  them matching fascinated expressions or a shared reach.
- In the cape-save beat, the King accelerates, fabric lags, and the Prince uses
  one economical hand motion to lift or clear the trailing edge. The Prince
  does not yank the King backward or stop the journey; he prevents the trip and
  immediately releases the cape.
- Recovery is staggered: the King resets his slouch first; the cape settles;
  the Prince eye-rolls only after the King can no longer see it, then smoothly
  returns to his one-step-behind position.
- At arrival, the King occupies the broad foreground gesture while the Prince
  stands half a step behind and watches the people reacting. This frames the
  Prince as family, not as a second claimant to the candle.

## Runtime handoff gate

After owner acceptance, derive separate 2D atlases for locomotion, idle/acting,
and ability poses. Test silhouettes at target phone size and on the 30 fps
Speedy tier before adding polish frames. Preserve these concepts and generate
runtime derivatives at new paths.
