# Codex art work order — opera acts, mechanic-driven

**This supersedes the prop lists in `OPERA_ASSET_REQUESTS_2026-07-19.md` for
the twelve career acts.** Those lists described the acts as they were: taps on
static props. Every act has since been rebuilt around its own input gesture
(see `OPERA_JOB_GIMMICKS_2026-07-25.md`), and the art the gestures need is
different from the art the taps needed.

The rule that generates this whole document: **if the child's finger changes
what a thing looks like, that thing needs states, not a single pose.**

## House rules (unchanged, binding)

- CC0 sources or original, restyled through the `_toonify` pastel pipeline.
- ≤1024px longest side **or** power-of-two. VRAM compress only if POT.
- One `ASSET_LICENSES.md` line per asset, in the commit that adds it.
- Never modify book art, family voices, or friend cutouts.
- Emissive only — no new OmniLights. Decorative tiers must cull on Speedy.
- Non-reader: every state reads as a **picture**, never a word.
- Naming: `assets/opera/jobs/<job>/opera_<job>_<thing>.glb`, states as child
  nodes named `State<Name>` toggled by `_job_state()`.

## What is already built and must not be re-specified

Twelve dressed stages exist in `OperaAct.STAGE_SETS` as toon primitives:
Pastry Kitchen, Prop Library, Recital Hall, Candy Workshop, Plushy Clinic,
Meadow Flat, Toy Ring, Conjuring Parlour, Sunrise Gallery, Launch Pad, Grand
Prix Circuit, Starlight Concert. **Replace these in place** — same positions,
same colour roles (`deck` / `pillar` / `beam` / `backdrop` / `wing` / `crest` /
`pool`) — do not re-place them.

Scenery envelope: `|x| >= 19` or `z <= -15.5` or `z >= 17`. Anything inside
that box collides with gameplay props.

---

# Per-act art, driven by the mechanic

## 1. Pastry Chef — circular drag to stir

The finger traces circles round the bowl. The bowl is the only thing the child
looks at for ~40 seconds, so it carries the act.

**Priority items**
- `opera_chef_bowl.glb` — **needs 4 batter states**, not one: `StateEmpty`,
  `StateLoose` (thin, streaky), `StateThick` (ribboning), `StateComplete`
  (peaked, glossy). The stir meter reads 0→100% three times; the batter must
  visibly change or the gesture feels inert.
- **Stir swirl decal** — a spiral that rides the batter surface and rotates
  with the drag. This is the single most important asset in the act: it is the
  only feedback that the *circle* (not the tap) is what worked.
- Whisk with a motion-blur ghost pose.
- `opera_chef_oven.glb` — `StateClosed` / `StateGlow` / `StateOpen` with a
  risen cake inside.

**Background** — Pastry Kitchen: painted reef-seascape flat (the concept card's
teal/coral seascape), oven alcove with a warm interior glow, an ingredient
shelf of flour sacks, bowls and a rolling pin, gold apron footlights.

## 2. Detective — drag a magnifier, hold to open

Clues are **invisible outside the lens**. The lens is the act.

**Priority items**
- `opera_detective_lens.glb` — gold rim, translucent pane, angled handle. Must
  read at a glance while sitting *over* other objects.
- **Clue glint sprite** — the thing that appears only inside the lens. Needs to
  be legible against the dark indigo deck: warm, high-contrast, animated.
- **Dwell ring** — a 0.7s radial fill drawn round the box the lens is holding
  over. Without it the hold is invisible and feels broken.
- Six box silhouettes, each **distinct in outline** (`StateClosed` /
  `StateOpen` / `StateFish` for the decoy giggle).

**Background** — Prop Library: archive shelving stacked with wrapped props, a
leaning ladder, warm pillar lanterns, a crescent-moon window, and the scalloped
searchlight pool on the floor. Keep it **dark** — the lens only reads as a
light source if the room is dim.

## 3. Ballerina — hold the pose

A step needs 1.1 seconds of stillness. The child must *see* the hold filling.

**Priority items**
- **Pose ribbon** — six beads winding up around Roshan as the hold fills. It
  currently uses primitive spheres; it wants an authored ribbon that spirals.
  This is the act's entire feedback channel.
- Four dance tiles, distinguished by **colour AND icon** (not colour alone),
  with `StateIdle` / `StateDemo` / `StatePressed` as emissive swaps.
- Mirror-ball rig with a slow rotating highlight.
- Curtain-call bouquet.

**Background** — Recital Hall: big blush scallop fan upstage, practice barres
along both wings, tall mirror panels behind them.

## 4. Candy Maker — drag candies into colour chutes

**Priority items**
- **Seven candy bodies with distinct silhouettes** — the shape is how a
  non-reader tells them apart while they slide past. Each wears a **collar
  ring in its chute colour**; the collar is the match cue and must be readable
  from above at speed.
- **Three chutes** — pink / blue / gold, each with a mouth that reacts:
  `StateIdle`, `StateHover` (a candy is over it), `StateAccept`, `StateReject`.
- **Conveyor belt** with a scrolling tread texture. The belt visibly speeds up
  as the batch grows; the tread must sell that acceleration.

**Background** — Candy Workshop: upstage jar wall, mixing counters in both
wings, hanging swirl lollipops.

## 5. Doctor — read the pictogram, pick the tool

**Priority items**
- **Four symptom pictograms** — 💗 heartbeat, 🌡 temperature, 🩹 ouchie,
  🎀 bandage. Currently `Label3D` emoji. These want authored icons on a card
  that floats over the plush. **Highest-value single asset in the act** — the
  whole mechanic is reading them.
- `opera_doctor_patient.glb` — the coral five-armed starfish plush, **never**
  another species. States: `StateWorried`, `StateListening`, `StateWarm`,
  `StateKissed`, `StateBandaged`, `StateComplete` (happy + blush).
- Four tools, each silhouetted to match its pictogram so the pairing is
  visual: stethoscope, thermometer, heart-puff, bandage roll.

**Background** — Plushy Clinic: quilted teal wall with a gold scallop
medallion, tool trolley, handwashing basin, waiting bench with more plushes.

## 6. Farmer — drag back and lob

**Priority items**
- **Aim-dot arc** — seven dots showing where the veggie will land. This is the
  charge feedback; without it the pull is guesswork.
- **Veggie set** (carrot, apple, corn, berry, pumpkin) with a **spinning
  in-flight pose**.
- Piggy sprite with `trot` / `hop` / `munch` / `fed` frames and a want-bubble.
- Landing puff for a lob that hits the grass.

**Background (2D parallax)** — Meadow Flat: distant hills, orchard mid-layer,
fence-and-flower foreground, red barn for the finale, sunset curtain-call sky.

## 7. Boxer — punch on the beat

**Priority items**
- **The beat pulse** — imps duck and rise on a 1.6s bar. They need a
  `StateDown` (squashed, 0.72 scale) and `StateUp` (full, braced) that read
  instantly, plus a **ring-side beat lamp** that pulses on the bar so the
  rhythm is visible and not only audible.
- Training bag on its strap, with a swing-arc smear pose.
- Championship belt + victory podium, `StateDim` / `StateGold`.
- Corner stools (one coral, one teal), pennant bunting.

**Background** — Toy Ring: dark hall strung with swagged warm bulbs. Keep it
dark so the beat lamp carries.

## 8. Magician — hide the fish, then track it

**Priority items**
- **Three hats**, coral / teal / cream bands, with `StateIdle`, `StateLifted`
  (carried by the finger), `StateSettled`.
- `opera_magician_bunnyfish.glb` — a pink **fish** with fins, tail and long
  rabbit ears. Never rabbit legs. Needs `StateVisible` / `StateHidden` and a
  reveal pop.
- **Swap trail** — a star-swirl ribbon between two hats during a shuffle, so
  the dance is followable.

**Background** — Conjuring Parlour: plum velvet valance, coral and teal fronds
in the wings, star-studded trick cabinet, gold-framed rolling mirror.

## 9. Painter — drag to paint

The canvas is a **live 96×96 image the child paints into**. This changes what
art is needed more than any other act.

**Priority items**
- **Brush stamp texture** — a soft round alpha stamp, 32px, used as the brush
  head. Currently a hard circle. This is what every stroke looks like; it is
  the highest-value asset in the act.
- **Primed canvas texture** — the cream base the paint goes onto, with a faint
  tooth so bare canvas reads as canvas.
- **Three paint pots + three loaded brushes** (plum, coral, cream), where the
  loaded brush's tip is unmistakably the colour it will lay down.
- **Finished-sunrise reference card** on the easel — what she is painting
  toward, small, beside the canvas.
- Splat stamp set for the finale; rinse cup.

**Background** — Sunrise Gallery: the sunrise being painted, rising sun and
rays, banded water, paint cart, rinse station, spattered drop cloth.

## 10. Astronaut Engineer — hold the countdown

**Priority items**
- **Thrust bar** — a vertical gauge climbing the gantry as the hold builds,
  and **sagging** when the finger lifts. The sag must be visible; it is the
  only thing telling her to hold on.
- **Bubble column** under the rocket, growing with the fill.
- `opera_astronaut_rocket.glb` — `StateIdle`, `StateStrain` (shuddering on the
  pad), `StateLaunch`. Exhaust is **bubbles, never flame**.
- Pipe pieces (straight / elbow / ring) + ghost slots that only accept their
  own shape; valve wheel.

**Background** — Launch Pad: starfield with a ringed planet and a moon, teal
deco skyline, circular launch platform with a gold ring, mobile gantry.

## 11. Racecar Driver — steering, two laps

Kart engine content is complete. Needed: opera-liveried kart skin, **lap
counter reading 1/2 and 2/2 as pips, not digits**, zoom-strip road decal with
idle/active states, checkered flag, grandstand banner, trophy podium.

**Background** — Grand Prix Circuit: swirl night sky, striped coral/teal/
lavender track, starting arch, grandstand flats, padded barriers.

## 12. Pop Star — arrow rhythm

Dance engine content is complete. Needed: pearl microphone on its pedestal,
**four arrow glyphs paired to coral/teal/plum/cream**, a hold-note tail sprite
for sustained arrows, glow-stick rail, encore reveal banner.

**Background** — Starlight Concert: rainbow arc wall, speaker stacks, catwalk
running into the house, pearl light frame.

---

# Cross-cutting asks

These are worth more than any single prop because they appear in every act.

1. **Gesture affordance icons** — a small pictogram shown once when a beat
   starts, teaching the gesture without words: a circling finger, a dragging
   finger, a pressed-and-held finger, a pull-back-and-release. Six acts now
   open by teaching a gesture and all six currently do it with a voice line
   alone.
2. **Progress rings** — one shared radial-fill asset, used by the stir meter,
   the lens dwell, the pose ribbon and the thrust bar. Consistency here teaches
   "filling = keep going" once instead of four times.
3. **Gentle-miss puff** — one shared "that didn't work, no harm done" burst.
   Every act has a miss; they should all look like the same friendly nothing.
4. **The four pacing archetypes** want distinguishable lighting moods:
   metronomic (pulsing), escalating (brightening), calm exploration (dim, warm
   pools), build-and-payoff (dark → blaze at the end).

# Priority order

If capacity is limited, this is the order that buys the most:

1. Painter brush stamp + primed canvas *(the act is unreadable without them)*
2. Doctor symptom pictograms *(the mechanic is literally reading them)*
3. Chef bowl batter states + stir swirl *(40s of staring at one object)*
4. Detective clue glint + dwell ring *(the hold is currently invisible)*
5. Candy collars + chute states *(the match cue at speed)*
6. Boxer beat lamp + imp up/down states *(the pulse must be visible)*
7. Farmer aim-dot arc *(the charge is currently guesswork)*
8. Astronaut thrust bar + bubble column
9. Shared progress ring + gentle-miss puff
10. Everything else
