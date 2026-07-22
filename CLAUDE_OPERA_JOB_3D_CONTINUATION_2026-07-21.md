# Claude handoff — Opera House job levels, assets, and outfits

## Source of truth

Use `assets_src/concepts/opera_jobs_flat_2026-07-21/` as the visual source of
truth for the twelve non-boss jobs. Each job has three accepted sheets:

- `<job>_outfit_sheet_2026-07-21.png`
- `<job>_gameplay_sheet_2026-07-21.png`
- `<job>_stage_states_sheet_2026-07-21.png`

Use `audit/opera_job_flat_prototype_ledger_2026-07-21.csv` for the exact 576
card paths. Use `OPERA_JOB_FLAT_ART_AUDIT_2026-07-21.md` for scores and binding
continuity rules. The full set already passed a 4.5/5 gate.

Every individual card in `cards/` is 1024 x 1024. Treat those files as the
primary close-up modeling references. The 36 whole sheets are composition and
family-consistency references. Do not downsample the individual cards in the
source library, and do not regenerate a card merely to make it look more
realistic. The owner accepted the flat designs as shown.

Do not use earlier realistic or mesh-first experiments as style targets. Do
not modify protected book art, family voices, or friend cutouts. Do not create
Curtain Dragon, Shadow Phantom, or Midnight Maestro assets in this phase.

## Owner intent and definition of done

Build the complete non-boss Opera experience as a coherent 3D toy-theatre
system, not twelve unrelated prop drops. The lobby remains the primary stage
and navigation space. Four career doors belong to each of three floors. A
career door opens a focused show set assembled from the corresponding cards.
Upper floors remain visibly desirable but physically inaccessible until the
existing progression unlocks them. Boss encounters are not part of this work.

A job is not complete when its hero object exists. Each job needs:

1. a reversible Roshan outfit kit or a clearly staged outfit stand while the
   current cutout fallback is in use;
2. the complete set of mechanic-critical implements and their readable state
   changes;
3. a small theatrical environment that frames the mechanic without hiding it;
4. nonverbal guidance, gentle retry, progress, completion, and curtain-call
   presentations;
5. integration at the live node hooks without changing the subgame rules; and
6. Mobile-render evidence at the actual gameplay camera.

Do not model every decorative card at maximum detail before the mechanic reads.
Finish one vertical slice per job in this order: outfit silhouette, primary
touch target, required state swaps, guidance, completion, then scenic dressing.

## How to use the delivered art

Each job has three sheets, and each sheet has sixteen individual 1024 cards.
Use them differently:

- **Outfit cards** define Roshan's career silhouette and the wearable-kit
  breakdown. `hero_front_three_quarter`, the two turnaround cards, and
  `signature_action_pose` control proportions. The accessory cards control
  removable pieces. The silhouettes are a phone-readability test, not separate
  costumes. `wardrobe_display` is the lobby display treatment.
- **Gameplay cards** are the mechanical source of truth. If several cards show
  one object in different conditions, build one scene with named state nodes or
  material states; do not ship disconnected substitutes with drifting scale.
- **Stage/state cards** define composition, guidance, retry, reveal, and
  curtain-call beats. Scenic cards may become low-detail modules or camera-facing
  flats. State cards are timing/layout references and should not become dense
  permanent geometry.

Recommended per-card workflow:

1. Find the asset in the CSV ledger and record its job, sheet family, accepted
   score, source sheet, and exact card path.
2. Open the individual 1024 card together with its full sheet. The card supplies
   shape detail; the sheet prevents palette or scale drift.
3. Mark the object as `mechanic`, `state`, `guidance`, `reward`, `scenic`, or
   `outfit`. This determines collision, animation, and triangle budget.
4. Block the object with two to six rounded primitives. Match silhouette and
   major color areas before adding trim.
5. Set its pivot and state architecture using the conventions below.
6. Render 0, 45, and 135 degree review views against a neutral navy card plus
   one actual gameplay-camera view.
7. Compare against the accepted card at thumbnail size. Reject clipped,
   realistic, over-detailed, off-palette, or ambiguous versions.

The cards contain dark presentation backgrounds and cell framing. Those are
not textures to project onto the 3D object. Extract only the depicted design.

## Level architecture

### Lobby as primary stage

Preserve the live three-floor plan in `scripts/opera_house.gd`: four career
doors per floor, visible vertical circulation, and one centre medallion per
floor. The lobby should feel like an early twentieth-century live-performance
theatre interpreted as a pastel underwater playset, with the warmth and legible
showmanship of the Peach Showtime lobby influence but no copied symbols,
characters, or architecture.

The lobby needs five visual layers:

- **Navigation layer:** broad carpet paths, door arches, lift/bubble route,
  guarded upper-floor landings, and the central medallion. These must read first.
- **Career layer:** twelve distinct wardrobe displays and marquee doors. Use
  each outfit's crest and wardrobe-display cards; avoid text-only signs.
- **Theatre layer:** box-office forms, balcony fronts, curtain swags, pearl
  sconces, brass rails, poster frames, velvet ropes, benches, and shell trim.
- **Progress layer:** door illumination, earned-show marks, floor unlock glow,
  and the centre-stage medallion. Use material changes or visibility states,
  never extra OmniLights.
- **Atmosphere layer:** sparse bubbles, broad caustic cards, restrained sparkle,
  and distant audience silhouettes. This layer must cull on Speedy.

Upper-floor lock design must be clear without reading. Before unlock, stop the
route with a closed shell gate or crossed velvet ropes, dim the next-floor door
crests, and show one large pictorial progress medallion beside the route. Do not
use an invisible wall by itself. On unlock, animate the barrier open, send a
single golden path toward the route, and play the existing voice guidance.
Never show a punitive red lock or failure message.

### Career show modules

Build one shared show-room shell with replaceable stage packages. The shell
should provide a shallow proscenium, wing masking, a broad interaction deck,
rear scenic slot, two prop rails, an optional low catwalk, and fixed camera and
player anchors. Each job package supplies its backdrop, hero implements,
guidance/effects, and reward tableau. This keeps camera, collision, lighting,
and performance predictable while allowing strong job identity.

Keep the mechanical plane open. At gameplay camera, reserve approximately the
middle 70 percent of the screen width and lower 65 percent of the frame for
touch targets, Roshan, and feedback. Scenic dressing belongs behind, above, or
outside that region. The principal target should occupy roughly 10–18 percent
of screen height; secondary targets should not fall below roughly 7 percent.

### Scale calibration

Use the live Roshan avatar as the only absolute scale reference. In the current
act, the sprite is normalized to about 6.2 Godot units high. Import a nonshipping
6.2-unit proxy into every Blender job scene and validate these bands:

- hand tools: 0.7–1.4 units long, deliberately chunky;
- tabletop targets and clues: 1.2–2.6 units across;
- pedestals and boxes: 2.5–4.0 units across;
- hero machines, canvas, chest, or exam table: 5–8 units across;
- playable decks: preserve the live builder footprints rather than rescaling
  the gameplay around the mesh;
- scenic arches and proscenia: large enough to frame the mechanic without
  intersecting the fixed gameplay camera.

These are starting bands. Existing touch distances and positions in
`scripts/opera_act.gd` win over aesthetic rescaling.

## Asset construction conventions

### Pivots, axes, and transforms

- Author in meters with +Y up and -Z facing the audience/gameplay camera.
- Apply scale and rotation before export; scene roots remain at 1,1,1.
- Place touch-target pivots at the object's visual centre near its interaction
  plane, not at an arbitrary imported origin.
- Place doors, lids, press arms, curtain panels, hats, valves, and wheels at
  their real hinge/rotation axes.
- Place floor-standing scenic modules at floor-centre. Provide a separate
  `Anchor_Player`, `Anchor_Camera`, and `Anchor_Reward` only in stage modules,
  never inside reusable props.
- Keep all state variants spatially registered. Switching `closed` to `open`
  must not change the parent transform or scale.

### Scene and node pattern

Use this pattern for mechanic-critical props:

```text
Job_ObjectName
  Visual
    State_Idle
    State_Active
    State_Complete
  TouchTarget
  CollisionStatic          # only if physically required
  FXAnchor
  PointerAnchor
  AudioAnchor
```

Only one visual state is visible unless the reference explicitly layers them.
Use AnimationPlayer for hinge motion, squash, recoil, valve rotation, ribbon
reveal, and simple pose swaps. Keep gameplay truth in the existing script;
animations report completion but do not decide whether the child succeeded.

### Materials

Create a small shared material library: deep navy outline/underside, warm
coral, clear teal, cream, plum, pearl, brushed toy brass, pale aqua shadow,
lavender shadow, soft wood, and three or four job accents. Use flat or gently
ramped shading with high roughness. Favor painted color blocks over photo
texture. Put thin decorative lines into a shared trim atlas rather than geometry.

Pearl and brass need restrained highlights. They must not become realistic
metal/glass. Emission is for active arrows, pointers, progress lamps, fitted
pipe confirmation, boost strips, and final reveals. Emission should replace
additional lights, remain broad, and never blow out the base color.

### Touch and collision

Touch geometry must be simpler and slightly larger than the visible mesh.
Children should be able to touch the apparent object edge and still select it.
Keep separate selection areas for adjacent pads. Only use physical collision
for floors, ring edges, major machinery, track barriers, and surfaces that
actually stop Roshan. Scenic flats, curtains, shelves, particles, clues in
flight, and crowd dressing should not become physics bodies.

### Effects

Pointers, toss arcs, swap trails, rhythm ribbons, paint swipes, bubble exhaust,
confetti, and sparkle bursts should use unshaded cards, short ribbon meshes, or
small capped particle systems. Author a Speedy version with fewer particles and
no more than two transparent layers at the same screen location. Effects must
not obscure the target they explain.

## Modeling boundary

The flat sheets are design/model references, not runtime sprite atlases. Build
original, efficient 3D interpretations with the accepted silhouette, palette,
and state logic. Do not trace every illustrated highlight into geometry.

Roshan's current act avatar is still a `Sprite3D` using
`assets/characters/roshan_sprite.png`. Until an approved outfit-aware 3D
character pipeline exists, build each outfit as a separate, reversible kit:

- headwear or hair-adjacent accessory;
- chest/shoulder garment shell;
- high tail sash/apron/belt attachment;
- primary hand prop;
- optional secondary prop;
- crest and wardrobe display.

Never replace Roshan's mermaid tail with legs. Outfit geometry must not clip
the tail silhouette or cover the face. Keep the cutout fallback unchanged.

## Live job map

`scripts/opera_house.gd` is the roster source of truth. The older asset request
that mentioned Opera Star was stale; the live Floor 2 slot is Boxer.

| Job | Runtime kind / builder | Critical live nodes or hook |
| --- | --- | --- |
| Pastry Chef | `order` / `_build_order()` | `OperaPad0..2`, `OperaGoal`, cake order, stir, toppings |
| Detective | `sleuth` / `_build_sleuth()` | `SearchProp0..5`, `TiaraChest`, three clue states |
| Ballerina | `echo` / `_build_echo()` | `OperaPad0..3`, demo/repeat tile glow |
| Candy Maker | `press` / `_build_press()` | `CandyPress`, gauge/slider, seven candies |
| Doctor | `doctor` / `_build_doctor()` | `PlushPatient`, `Stethoscope`, `Thermometer`, `BandageRoll` |
| Farmer | `scroll` / `_build_farm()` | CanvasLayer piggies, food target, toss feedback |
| Boxer | `box` / `_build_box()` | Ring, round waves, friendly imps, championship belt |
| Magician | `shuffle` / `_build_shuffle()` | `OperaHat*`, bunny-fish, shuffle/select/reveal |
| Painter | `order` / `_build_order()` | `OperaPad0..2`, `OperaGoal`, `PaintBrush`, canvas stripes |
| Astronaut Engineer | `fix` / `_build_fix()` | `PipePiece0..2`, ghost slots, valve, rocket launch |
| Racecar Driver | `race` / `_build_race()` | `RaceFlag`; existing KartGame is complete |
| Pop Star | `dance` / `_build_dance()` | `StarMicrophone`; existing DanceEngine is complete |

## Per-job 3D level and implement guide

### 1. Pastry Chef — The Great Cake Show

- **Set:** use the pastry proscenium, counter, ingredient shelf, topping
  pedestals, oven alcove, and reveal table as a shallow coral-and-cream kitchen
  theatre. Put the three ingredient pads across the front play line and the
  bowl/cake goal at centre-back. The oven and shelf are scenic until their
  corresponding state is active; do not let them compete with the pads.
- **Implements:** the vanilla, coral, and plum layers are three distinct chunky
  cylinders on matching pedestals. The recipe board shows shape/color tokens in
  the live sequence; it is a pictorial state display, not text. Keep bowl-empty,
  calm, and stirring visuals in one registered bowl scene. Keep oven closed/open
  on a real hinge. Make the whisk and piping ribbon broad enough to read from
  the gameplay camera.
- **Sequence:** support five layer deliveries using the live order, then three
  visible stir beats, then three topping targets. A selected layer moves to the
  goal without changing its size. A wrong layer wobbles and returns. Topping
  targets glow one at a time and turn into permanent toppings when touched.
- **Completion:** transition the working bowl/cake into the finished cake on the
  reveal table; open the oven or curtain only as supporting motion. Use one
  frosting ribbon, pearl bloom, and curtain-call bow. Avoid dense food particles.

### 2. Detective — The Missing Tiara

- **Set:** build a moonlit prop-library stage with six search objects placed in
  an alternating shallow zigzag, leaving a clear sight line to the tiara chest
  at centre-back. Archive shelves and the case board are rear flats. Use one
  searchlight pool at a time rather than six permanent glows.
- **Implements:** all six boxes must differ in silhouette: mystery boxes,
  hatbox, trunk, round ribbon box, and tall crate. Give every lid a correct
  hinge. Paw, feather, and ribbon are the only clues; fish and sock are friendly
  decoys. The magnifier is a pointer motif, not a second interaction mode.
- **Sequence:** opening a box is permanent for the round. A clue rises and flies
  to one of three case-board/chest sockets. A decoy pops up, bows or wiggles,
  then clears without marking failure. After three clues, change the chest from
  locked/dim to ready/glowing and route the pointer to `TiaraChest`.
- **Completion:** the chest opens, the pearl tiara rises above its pedestal, and
  the case board changes from empty to complete. Keep the reveal centred and
  unobstructed by shelf dressing.

### 3. Ballerina — The Dance Recital

- **Set:** use the recital proscenium, four-tile dance floor, low practice barre,
  mirror-panel flats, and one mirror-ball silhouette. The floor is the mechanic;
  curtains and barre sit outside its touch footprint.
- **Implements:** tile identity must pair color and icon: coral shell, teal wave,
  plum ribbon, cream pearl. Build idle, demonstration glow, pressed ripple, and
  completion bloom as material/visibility states on the same four tiles.
- **Sequence:** the live rounds demonstrate 3, then 4, then 5 steps. During
  `watch`, block touch and pulse one tile at a time. During `repeat`, leave all
  four readable and show a broad press ripple. A wrong press gently resets the
  current sequence; it never paints a red mark or knocks Roshan down.
- **Completion:** use the twirl ribbon and recital reveal behind Roshan, then
  place the bouquet/curtain-call marker at the edge of the floor so it does not
  cover the last tile.

### 4. Candy Maker — The Candy Parade

- **Set:** centre the press machine and timing gauge on a toy workshop platform.
  Put the hopper and conveyor behind it, the seven-slot shelf to one side, and
  the wrapping station/parade cart on the other. The gauge and moving marker
  must be visible above Roshan and the machine.
- **Implements:** one press scene needs open, descending, squish, and returned
  poses. The timing gauge requires a generous teal success zone and a high-
  contrast moving marker. The seven candies need different outer silhouettes,
  not seven face decals on one shape. Mold plates, scoop, and tongs are dressing
  unless later wiring explicitly uses them.
- **Sequence:** each press creates one candy, gives a soft squash, wraps it, and
  moves it into the next shelf slot. A mistimed press creates the same safe candy
  with a funny wobble and resets the marker. Keep all seven shelf occupants
  instanced and use visibility/state changes for empty versus full slots.
- **Completion:** light the complete shelf, roll the parade cart under the arch,
  and present the wrapped-candy reward. Do not flood the screen with individual
  candy particles.

### 5. Doctor — The Plushy Checkup

- **Set:** stage a cosy cream/aqua clinic around a low exam platform. Put the
  stethoscope pedestal front-left, thermometer front-right, bandage front-centre,
  and the same patient at centre-back. The trolley, basin, cabinet, curtain, and
  bench frame the scene but remain outside the swim/touch path.
- **Implements:** the patient is always one five-armed coral starfish plush.
  Build worried, calm, happy, and recovered expressions as face/pose states on
  one rig or registered meshes. The stethoscope needs a broad chest contact pad.
  The thermometer needs cool/warm states. Provide five registered boo-boo/heart
  sockets and one bandage-wrap state.
- **Sequence:** match the live eight beats: stethoscope, thermometer, five
  individually tended boo-boos, then bandage. Only the current implement or
  socket glows. Early touches wobble and re-point. Do not substitute the four-
  pictogram summary board for the actual five heart sockets.
- **Completion:** all hearts remain visible, the bandage appears cleanly around
  the plush, and the same starfish hops into its recovered pose. No medical
  realism, needles, distress, injury, or species substitutions.

### 6. Farmer — The Piggy Picnic

- **Set:** retain the existing side-scrolling CanvasLayer mechanic. The 3D show
  room supplies the meadow proscenium, barn-wing silhouette, hay/fence edge
  dressing, and final picnic reveal; it must not replace the tested 2D timing
  layer. The three meadow/orchard/flower layers remain flat parallax art.
- **Implements:** provide piggy trot A/B, hop, munch, and fed poses with identical
  body scale. Nine live piggies may instance these poses. Cycle the five food
  pictograms—carrot, apple, corn, berries, pumpkin—in desire bubbles. Basket,
  toss arc, mud puff, and hay are supporting cards.
- **Sequence:** a piggy travels toward the toss zone, the one-finger TOSS sends
  the pictured food along the broad arc, and the piggy swaps to munch/fed/hop.
  A toss with no nearby piggy simply bounces and returns. Avoid physics food and
  physics foliage; this remains deterministic screen-space timing.
- **Completion:** park the nine fed piggies in a readable picnic group, reveal
  the blanket and produce basket, warm the backdrop toward sunset, and keep
  individual animals large enough to distinguish.

### 7. Boxer — The Championship Bout

- **Set:** preserve the live ring footprint, posts, and two rope heights. Use a
  padded cream deck, coral/teal corners, shell bell, three progress lamps,
  pennant crowd flats, and a belt pedestal outside the fight path.
- **Implements:** Roshan's gloves, focus mitt, bell, training bag, and belt use
  oversized toy forms. Imps are friendly moving targets with peek, bopped, bow,
  and captain-return states. Bubble puffs and recoil arcs replace hit sparks.
- **Sequence:** live rounds contain 3, 4, then 5 imps. Roshan PUNCHes the nearest
  target within the existing range. Ordinary imps bow/clear after one bop; the
  last-round captain may bounce away and return once. Ring lamps show round
  progress. A close imp bounces against the bubble shield; there is no damage.
- **Completion:** ring the bell, light all three progress lamps, raise the padded
  championship belt, and pose the imp group bowing around the victory podium.
  Never depict injury, anger, teeth, bruises, or realistic combat equipment.

### 8. Magician — The Magic Hat Trick

- **Set:** centre three hat pedestals on a rail with the trick table behind and
  the cabinet/mirror in the rear wings. Keep identical spacing and camera scale
  for every shuffle so tracking is fair.
- **Implements:** hats differ only by clear band colors—coral, teal, cream—while
  sharing one silhouette and scale. The bunny-fish is always a pink finned fish
  with a tail and long rabbit ears, never a rabbit body. Build swim, peek, and
  reveal states. Swap trails, crossed trails, feint, selector glow, and decoy
  bubble puff are temporary effects.
- **Sequence:** show the bunny-fish entering one hat, perform the live four
  shuffle rounds, then enable selection. Hat roots move; do not teleport or
  swap colors under the child. A wrong choice produces a friendly decoy puff
  and resets the same round without a penalty.
- **Completion:** open the chosen hat, lift the bunny-fish into its reveal pose,
  add one pearl-wand flourish, and hold the final lineup long enough to read.

### 9. Painter — Paint the Sunrise

- **Set:** put the large canvas at centre-back, three ordered paint pedestals
  across the front, and rinse/paint carts outside the carry path. Use a drop
  cloth and blank gallery frames as quiet dressing. Keep the ordered color board
  immediately above or beside the canvas.
- **Implements:** lock every cue to plum, coral, cream. One brush scene needs
  unloaded and three loaded-tip material states. One canvas needs blank, plum,
  plum-plus-coral, and finished states registered to the same frame. Swipes and
  splats are broad temporary ribbons/stamps.
- **Sequence:** the live sequence is plum, coral, cream, then plum again. Touch
  the correct pot, carry the loaded brush, swipe the canvas, and reveal the next
  registered stripe. After the four swipes, expose three splat targets. A wrong
  pot wobbles and the golden pointer returns to the correct pot.
- **Completion:** replace the working state with the framed sunrise on the
  gallery reveal wall, then use the before/after tableau and curtain call. No
  alternate color ordering is permitted in props, signage, or effects.

### 10. Astronaut Engineer — The Bubble Rocket

- **Set:** place the rocket and mobile gantry at centre-back, three pipe sockets
  in a readable work wall, loose pieces across the front, bubble tank to one
  side, and valve pedestal to the other. Keep the rocket exhaust area visibly
  clear for the finale.
- **Implements:** straight, elbow, and ring pipes each require loose, ghost-slot,
  wrong-hover, and fitted states with matching silhouette. Use one pipe scene
  per shape and keep fitted endpoints registered. The bubble tank, pressure
  lamps, valve wheel, wrench/tool belt, rocket window, and bubble stream share
  the rounded retro-future language.
- **Sequence:** the child carries each loose piece to the socket with the same
  picture. Wrong shapes gently return; correct shapes snap in and change their
  socket from ghost to fitted. After all three are fitted, route the pointer to
  the valve and rotate it through a clear full turn.
- **Completion:** fill pressure lamps, send bubbles through the fitted route,
  glow the prelaunch outline, and launch with bubbles only. No flame, smoke,
  realistic aerospace labeling, or unreadable pipe clutter.

### 11. Racecar Driver — The Opera Grand Prix

- **Set:** keep the existing `KartGame` course and controls. Add the Opera skin:
  starting arch, banked-curve dressing, padded barriers, pit cart, grandstand
  flats, progress lamps, finish ribbon, and trophy podium. Do not rebuild the
  driving engine inside `OperaAct`.
- **Implements:** the kart needs front/side/rear consistency, a tail-safe seat
  channel, steering wheel, turbo control, and clear driver silhouette. Boost
  strips need idle/active material states. Flags, pit tools, shell trophy, and
  bubble turbo trail are supporting assets.
- **Sequence:** `RaceFlag` launches one special lap. Steering remains one-finger,
  zoom strips activate the authored ribbon, and TURBO adds a short bubble trail.
  Finishing in any place completes the act. Closing early returns safely to the
  flag and preserves the chance to restart.
- **Completion:** break the finish ribbon, wave broad flags in the rear layer,
  and move the same kart to the victory pedestal with the shell trophy. Keep
  confetti sparse enough that the kart silhouette remains visible.

### 12. Pop Star — The Starlight Concert

- **Set:** use the concert proscenium, pearl light frame, speaker stacks,
  catwalk, rainbow backdrop, dance floor, microphone pedestal, and audience
  glow rail. The arrow lane and performer area must stay free of speaker or
  catwalk occlusion.
- **Implements:** `StarMicrophone` becomes the pearl microphone with idle and
  active states. Pair left/right/up/down with coral/teal/plum/cream and preserve
  both arrow shape and color. Speakers, monitor, tambourine, beat pulse, pressed
  arrow, rhythm ribbon, and microphone finale share the same rounded finish.
- **Sequence:** touching the microphone opens the existing `DanceEngine` in
  guest mode. Do not replace its timing or input. Active arrows pulse in the
  fixed lane; correct taps create broad rhythm ripples and grow the rainbow
  ribbon. Closing before a happy hit returns safely to the microphone.
- **Completion:** after the first successful guest round, bring the microphone
  to its finale state, complete the rainbow backdrop, brighten the pearl frame,
  and hold an uncluttered encore pose.

## Required continuity by job

- Chef: preserve the live layer order; bowl, stir, oven, topping targets, and
  final cake must be separate states.
- Detective: six boxes need different silhouettes. Only paw, feather, and
  ribbon are clues; fish/sock are friendly decoys; three clues open the tiara
  chest.
- Ballerina: four tiles differ by color and icon. Demonstration and pressed
  states must remain readable with emissive material swaps, not added lights.
- Candy Maker: the gauge has a broad green-teal center. Seven candies differ by
  body silhouette, not only by face decal.
- Doctor: every patient is the same coral five-armed starfish plush. Never swap
  to a bear, rabbit, axolotl, or ordinary fish.
- Farmer: keep three flat parallax layers and pose-swapped pig sprites/meshes.
  Do not turn the meadow into physics foliage.
- Boxer: all equipment is padded and toy-like. Imps are friendly targets;
  impact is a bubble puff, never injury.
- Magician: the bunny-fish is a pink fish with fins and tail plus long rabbit
  ears; it never gains rabbit legs.
- Painter: the order is plum, coral, cream wherever shown. Keep blank, first,
  second, and finished canvas states consistent.
- Astronaut Engineer: straight, elbow, and ring pipe pieces must only fit their
  matching sockets. Launch exhaust is bubbles, not flame.
- Racecar Driver: retain the existing kart engine. Add an Opera skin, tail-safe
  seat/channel, boost strip, flags, and reward props only.
- Pop Star: retain the existing dance engine. Use left/right/up/down arrows
  paired with coral/teal/plum/cream, a pearl microphone, and broad rhythm
  effects.

## Recommended asset architecture

Create one shared Opera job library plus small per-job scenes:

```text
assets/opera/jobs/shared/
assets/opera/jobs/pastry_chef/
assets/opera/jobs/detective/
...
assets/opera/jobs/pop_star/
assets_src/blender/opera_jobs_2026-07-21.blend
assets_src/blender/qa_opera_jobs_2026-07-21/
```

Shared pieces should include shell/pearl trim, low pedestals, curtain flats,
rounded brass frames, pointer glow, bubble puff, confetti, and bow marker. Job
folders should contain only distinct hero props and state variants.

Use one mesh with material/visibility states where practical:

- open/closed oven, chest, hat, press, and curtain;
- idle/active tile, gauge, boost strip, and progress lamps;
- blank/progressive/finished canvas;
- empty/filled shelves and boards;
- pipe loose/ghost/fitted states;
- before/after patient and reward tableaux.

Do not model the contact-sheet background or cell dividers.

## Modeling order

1. Shared palette/material library, trim, pedestals, pointers, and effects.
2. Floor 1 gameplay hero props and state swaps.
3. Floor 2 gameplay hero props, with Doctor species lock reviewed first.
4. Floor 3 gameplay hero props, with Painter order and pipe matching reviewed
   before integration.
5. Job stage modules and scenic flats.
6. Reversible Roshan outfit kits and wardrobe displays.
7. Optional secondary dressing only after all mechanic-critical props pass.

Review every family in fixed 0°, 45°, and 135° isolated renders plus at least
one Mobile-render gameplay camera. Reject any interpretation below 4.5/5 or
any version that loses the flat prototype's silhouette/state logic.

## Mobile constraints

- Godot Mobile renderer on every platform; Speedy is the default.
- No new OmniLights. Use existing scene lighting, matte materials, selective
  emission, and cheap unshaded effect cards.
- Shared palette materials; no unique 1024 texture per small prop.
- Keep primary props approximately 500–4,000 triangles, major stage modules
  under 10,000, and tiny dressing under 1,000 unless a measured exception is
  justified.
- Use simple static collision only on floors, large machines, ring edges,
  track barriers, and direct interaction surfaces.
- Farmer scenery and most scenic flats must never become physics bodies.
- Limit glass to the Engineer helmet, bubble tank, and one rocket window layer.
- Cap bubble/confetti/ribbon particles aggressively and provide a Speedy cull
  path.
- New textures remain at or below 1024 px; POT only if VRAM compressed.

## Integration discipline

- Preserve state on `ReefMain`; follow the existing extracted
  `scripts/opera_act.gd` architecture.
- Replace primitive builders mechanically, one job family per commit. Do not
  redesign gameplay and modeling in the same commit.
- Keep current node names or add an explicit adapter so probes and interaction
  logic remain stable.
- Outfit integration must retain the current cutout fallback and must not
  destructively edit `roshan_sprite.png`.
- Every new GLB, texture, and Blender source needs an `ASSET_LICENSES.md` line.

## Claude delivery checklist

Deliver in reviewable job-sized batches. For each job, provide:

- one Blender collection for the outfit kit, one for mechanic-critical props,
  one for stage modules, and one for temporary effects/reference planes;
- linked shared Opera materials and shared trim/effect collections rather than
  local duplicates;
- named idle, active, retry, progress, and complete states matching the ledger
  terminology where those states exist;
- a Godot scene or explicit assembly manifest showing which GLB/node replaces
  each live primitive node;
- outfit/front, implement 0/45/135, stage-wide, active-state, retry-state, and
  completion renders;
- a Mobile-render screenshot at the real act camera with touch targets and
  Roshan visible;
- triangle counts, texture dimensions, material count, transparency count,
  collision type, and Speedy cull behavior in the batch note;
- new source, GLB, and texture registrations in `ASSET_LICENSES.md`; and
- a green exact-commit probe run before the job batch is considered complete.

Use a predictable naming family:

```text
opera_<job>_<object>.blend collection or source object
opera_<job>_<object>.glb
Opera<Job><Object>                 # Godot scene root
StateIdle / StateActive / StateComplete
TouchTarget / PointerAnchor / FXAnchor
```

Keep `assets_src` references at their delivered 1024 resolution. Runtime
optimization may bake or atlas textures at an appropriate measured size, but
must create new runtime derivatives; never overwrite or reduce the source
cards. Shared flat-color materials often eliminate the need for a unique prop
texture entirely.

Recommended review batches are Floor 1, Floor 2, and Floor 3, but do not submit
an entire floor without intermediate isolated renders. Doctor must receive a
species-continuity review before Floor 2 integration. Painter and Engineer must
receive order/socket reviews before Floor 3 integration. Race and Pop Star must
demonstrate reuse of their existing engines rather than duplicated mechanics.

## Validation

For each job family:

1. Run the GDScript parser and inference lint on changed scripts.
2. Import under Godot 4.4 Mobile rendering.
3. Capture outfit/front, hero-prop, stage-wide, active-state, and completion
   views at the actual gameplay camera.
4. Verify the pointer, voice line, retry loop, and completion remain usable by
   a non-reader with one finger.
5. Run `scripts/ci.sh` and require every trusted probe to pass.

Do not begin boss work until the owner explicitly starts the boss phase.
