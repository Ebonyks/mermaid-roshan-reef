# Racer rebuild: "Reef Grand Prix"

- **Status:** `PROPOSED / CANDIDATE` design for Codex. Written by Claude; no
  game file, image or audio is changed by this document.
- **Owner direction:** the Racer must be completely rebuilt (2026-10-17). The
  owner chose this side-scrolling race on 2026-10-18
  (`ODR-RACER-VIEW-20261018`). It supersedes TUNE, TO THE LINE and the
  circle/steering-bar grammar in `DL-INT-10` once Codex lands it. The parts of
  `DL-INT-10` that forbid an external kart scene or a probe-only bypass stay.
  The imp's win rule is `DL-INT-14`.
- **Shared systems:** [SHARED_SYSTEMS.md](SHARED_SYSTEMS.md). **Evidence:**
  [REFERENCES.md](REFERENCES.md).

## 1. The idea

A side-scrolling kart race through the reef, in painted 2D layers that slide
past at different speeds. Roshan's kart drives itself forward while the child
plays; she chooses one of three lanes by tapping it, and the kart swerves
there. Lanes hold rainbow boost rings, little ramps and gentle bumps. The
imp's kart races beside her in the same lanes. First across the finish ribbon
wins; if he wins, the race restarts at once and, after two losses, he slows
right down. Before the race she picks her kart's colour and helps fit its
wheels.

## 2. Why this shape

| Pattern | From | How it is used here |
|---|---|---|
| Assists that keep a young driver on the road and moving | Mario Kart 8 Deluxe Smart Steering and Auto-Accelerate (Nintendo recommends both to beginners); Mario Kart Tour's one-finger steering with automatic acceleration; Kirby Air Ride's auto-forward craft | The kart drives and stays on the track by itself; the child only chooses where |
| No holding for the whole race | Blaze and the Monster Machines: Axle City Racers moved acceleration off the held trigger because long holds suit 3–4-year-olds poorly | Driving continues for 3 s after any touch; holding is never required and is the slowest way to race |
| Speed comes from aimed taps on visible targets, never from mashing | Cars: Fast as Lightning (cars steer themselves; tap boost zones at the right moment); Excitebike (a held turbo overheats). Counter-examples: Go Go Thomas ("tap as fast as you can") and Pokémon Dash (rub faster to run faster) | Boosts come only from choosing the lane with the ring or ramp |
| Steer by pointing, into big lanes | Toca Cars (steer toward where you touch); Subway Surfers (three lanes); Excitebike (four lanes) | Three lanes; tap a lane and the kart glides there. Research: 4–5-year-olds track and steer continuously poorly (Flatters et al. 2014) |
| One big obvious control | Nielsen Norman Group: one large button to drive a car worked for young children | The whole lane band is the button |
| Ramps, tricks and boosts as the fun of speed | Mario Kart jump and trick boosts, Excitebike ramps, Team Sonic Racing speed panels, Blaze landing boosts | Ramps launch automatically; a tap in the air does a trick and a landing boost |
| Keep it close, fairly and invisibly | Mario Kart's position-weighted items and adaptive CPUs; mild rubber-banding in Nickelodeon Kart Racers 3; the pack kept bunched in Blaze; players exploit adaptation they notice (dynamic difficulty literature) | The imp paces off her, gently and unannounced; his scripted spin-out; half speed after two losses |
| Slipstream | Every Mario Kart since Mario Kart 64 except two | Driving in the imp's sparkly wake for 1 s charges a bubble boost, so catching up is deliberate |
| Bumps, not crashes | Out Run's designer wanted players to enjoy driving rather than explode; contrast Hill Climb Racing and Hot Wheels: Race Off, whose crashes end runs | Obstacles slow the kart for a moment and never stop it |
| See it coming, with the camera looking ahead | Defender (camera about 25% ahead), Donkey Kong Country (camera aims where the player is about to be); research advice of at least 2 s warning and no quick reactions under 5 | The kart sits at the left third of the screen; objects are visible for at least 2 s |
| Speed from painted layers | Parallax at several speeds (Moon Patrol), speed lines (early race posters, manga) | Four parallax layers and painted speed streaks during boosts |

The verified details and links for each reference are in REFERENCES.md.

Avoided: free steering that can leave the track, tilt or two-thumb controls,
item attacks, laps that need a map, timers, losing collected pearls, and a
race that holding a finger down can win (today's flaw).

## 3. Options considered

| Option | For | Against | Verdict |
|---|---|---|---|
| **A. Side-scrolling three-lane race (recommended)** | Fits the painted side-view kart art; discrete lanes suit age 4; parallax gives real speed in true 2D | Needs new painted course layers and a side-view driver set | Build |
| B. Keep the painted top-down circuit with a following camera and finger steering | Reuses the circuit painting | Continuous steering relative to the kart's heading is hard at 4; the painting is too small to zoom (DIAGNOSIS §4) | Reject |
| C. Behind-the-kart pseudo-perspective road (Out Run, Super Mario Kart Mode 7) | Strong speed feel | Striped-road drawing replaces painted art with code stripes and Mode 7 warps one painted plane; heavy overdraw; least like the storybook medium | Reject (painted props that scale up as they approach may still be used as accents) |

## 4. The race, beat by beat

| # | Part | What happens | What the child does | Done when |
|---|---|---|---|---|
| 0 | Paddock | Roshan swims into the pit garage of the existing Racer world painting; her kart waits | Nothing required | Roshan at the kart (travel, `DL-INT-02`) |
| 1 | Pick a colour | Three big painted kart colours on the garage wall | Tap one; the kart repaints | One chosen (remembered for next time; a later visit offers "keep" or "change") |
| 2 | Wheels on | Roshan holds her wrench (existing atlas pose); the two visible wheel spots glow | Tap each wheel spot; Roshan fits the wheel with a clunk and a spin | Both wheels on, each after Roshan's contact |
| 3 | Starting line | The imp's kart rolls up beside her, and he calls the challenge (he is hidden until here, contest C1–C2). Three pearl lights count down | Listen | "Go!" |
| 4 | The race | About 45 s through three scenes: reef start, kelp forest, castle bridge. Lanes carry boost rings, ramps, pearls and gentle bumps | Tap lanes; tap in the air for a trick | Either kart crosses the finish ribbon |
| 5 | Finish | Photo-flash if it is close; confetti; the podium with the existing trophy | Tap the trophy to lift it | Curtain call, or the instant rematch if he won |

## 5. Rules of play

**Lanes.** Three horizontal lane bands on the track: far (upper), middle and
near (lower). Each band, across the full screen width, is the touch target
for its lane (at least 150 base pixels tall). A tap anywhere in a band steers
the kart there; the kart swerves in about 0.4 s with a lean. Dragging the
kart up or down also works. Tapping the kart's own lane does nothing except a
little hop.

**Driving.** While she is playing, the kart drives forward by itself and the
camera follows it, with the kart held at the left third of the screen. "Playing"
means a touch within the last 3 s. After 3 s without a touch both karts glide
to a stop together, Roshan says "Tap a lane to drive!", and nothing is won or
lost (`DL-AGE-04`, contest C8). Holding a finger down keeps the kart driving
but cannot steer, so it hits bumps and misses rings: the slowest way to race.

**On the track.** Every object is visible at least 2 s before the kart reaches
it.

| Object | Effect |
|---|---|
| Rainbow boost ring | 1.5 s burst of speed with streaming bubbles |
| Ramp | Launches the kart automatically; a tap while airborne does a spin trick and gives a short landing boost |
| Gentle bump (sleepy turtle, kelp tuft, sand mound) | The kart hops and slows for about 0.8 s; it never stops and nothing is lost |
| Pearl | Collected into the pearl count for the medal; never lost |
| The imp's wake | Driving in his sparkly trail for 1 s charges a bubble boost (slipstream) |

Placement guarantees that each stretch has a better lane than the one she is
in, so lane choices matter, and that a ring or ramp is never placed directly
behind a bump in the same lane, so there is never a trap.

**Pace.** Base scroll speed is about 300 base pixels per second, about 450
during a boost, which still shows objects about 2 s ahead. The course is
about 45 s long at base speed. These are starting values for device tuning.

**The imp.** His kart drives the same lanes, changes lane with a
telegraphing wiggle, and paces relative to Roshan (the contest's
`base_seconds` rule: an engaged child should win the first attempt about
three times in four). At the first bend of the kelp forest he spins out for
1.5 s (his flub). He moves only while she is playing. If he finishes first
there is a beat of at most 2 s (he waves from the podium), then the race
restarts at the starting line with nothing she earned lost; after two of his
wins he drives at half speed for the rest of the visit (contest C7, C9). Ties
go to her.

**Feedback.** Every lane tap moves the kart at once (`DL-AGE-07`). Rings ring,
ramps whoosh, bumps boing, pearls chime; the music gains a layer while she
boosts. The camera stays level apart from a small, gentle settle on landing
(`DL-MOT-06`).

## 6. The course, in words

The finish stadium is the existing Racer world painting
(`assets/opera/worlds/backdrops/world_racer.png`): pit garages at the left,
the pearl tube arch, the grandstand and the shell trophy dais. The race runs
left to right through three painted scenes, each built from four parallax
layers:
- far: castle towers and sea light, moving slowest;
- middle: coral and kelp;
- the track: three lanes in the painted road surface;
- foreground: a sparse coral and bubble edge along the very bottom, moving
  fastest.

Roshan's kart, in side view and in the colour she chose, sits on the track at
the left third of the screen, with Roshan visible from the waist up at the
wheel and her rainbow tail fin on the kart's tail. The imp's purple kart is
beside her or a little ahead or behind. The finish ribbon
(`assets/kart/finish_banner.png`) spans the track at the stadium.

## 7. Art, animation and sound to produce

| Item | Description | Notes |
|---|---|---|
| Kart | The existing side-view kart (`widget_crank_racer_kart.png`, front facing left) mirrored to face right, in three colour variants, plus wheel-off and wheel-on states for the pit stop | Owned cards; the wheel art (`widget_crank_racer_wheel.png`) spins |
| Roshan driver set | Whole-frame side-view sprites at the wheel: driving idle with flowing hair, lean up, lean down, boost delight, bump giggle, airborne trick, cheering, waving | The racer atlas is the identity and costume reference; it has front-facing poses only. Pilot the lean first |
| Imp kart and driver | A purple kart with the `rival_racer` imp at the wheel in side view: driving, wiggle, spin-out, podium wave, defeated slump | His existing 13 poses are references |
| Course | Three scenes (reef, kelp forest, castle bridge), each in four parallax layers, the track with three readable lane bands, and the finish stadium from the world painting | Native coverage per screen follows `DL-LAY-07`; repeating segments are allowed for the middle and far layers |
| Track objects | Boost ring, ramp, sleepy turtle, kelp tuft, sand mound, pearl, the colour swatches and glowing wheel spots | Painted, cartoony, never scary (`DL-AGE-08`) |
| Music | "Pearl Grand Prix" (`opera_racer`, 128 BPM) arranged with a boost layer, a countdown sting and a finish fanfare | `tools/build_area_music.py`; `AudioStreamSynchronized` for the boost layer |
| Voice | Exact new Roshan cues: "Pick a colour for our kart!", "Tap each wheel to put it on!", "Tap a lane to drive!", "Ramp! Tap for a trick!", "We won the Grand Prix!" plus the contest lines for the imp | Existing synthetic Roshan workflow; imp lines as in the contest specification |

## 8. Routes and saves

- **Free play:** the Movie Lounge's Racer route (`DL-INT-12`).
- **Saves:**
  - keep the career star bit and medal keys;
  - add, with defaults, the chosen kart colour and the race checkpoint (pit
    stop done or not), per `DL-SAVE-01`;
  - re-entry after the pit stop starts at the starting line.
- **Medals, wordless:**
  - bronze for finishing first;
  - silver for winning without the half-speed mercy;
  - gold for winning on the first attempt with at least half the pearls.
- **Chapter 2:** the adapter's `chapter2_grand_prix` set is empty today; this
  race can serve it later without the imp (contest C13).

## 9. What retires

The following go:
- TUNE (circle);
- TO THE LINE (swipe);
- the painted-circuit race with its 770×126 steering bar, turbo button and
  code-drawn lap dials;
- "hold anywhere to drive".

`scripts/kart_driving.gd` stays for the dormant kart game. The new race needs
only lane, boost and bump logic, which a small `RacerLanes` model can own.
Reuse `KartDriving`'s boost timing only if it fits.

## 10. Acceptance tests

Machine (a new trusted probe plus updates to `probe_opera_2d` and
`probe_voice`):

1. **Zero input.** For 60 s after "Go!" neither kart moves, there is no
   result, and the invitation plays.
2. **Lane steering.** A lane tap changes lane within 0.5 s. A tap in the
   current lane, or a second finger, changes nothing (`DL-UI-04`).
3. **Hold only.** Holding only, with no lane change:
   - the race is slower than the scripted lane-changing child;
   - the imp wins attempt 1;
   - after two losses, at half speed, a scripted engaged child always wins.
4. **Bumps.** They never drop speed to zero; pearls are never removed.
5. **Visibility.** Every object is first visible at least 2 s before contact
   at base and boost speeds.
6. **Imp win.** Restart within 2 s at the starting line; colour, wheels,
   medals and the star are kept.
7. **Ties** go to Roshan.
8. **Interruptions.** Pause, focus loss, Back and close stop both karts and
   cancel touches; resume starts a countdown (`DL-UI-05`).
9. **Pit stop.** Each wheel counts only after Roshan's contact animation, not
   on the tap alone (`MA-PLAY-004`).
10. **Overdraw.** States for paddock, race (all three scenes) and finish pass
    OD1–OD6. Note that parallax layers are the main overdraw risk.

Human checks:
- Target-phone frame pacing with scrolling layers.
- Does she understand "tap a lane"?
- Does she want to race again?
- The owner's look at the course art.

Machine success grants none of these.
