# Ballerina rebuild: "Lamma's Music-Box Ballet"

- **Status:** `PROPOSED / CANDIDATE` design for Codex. Written by Claude; no
  game file, image or audio is changed by this document.
- **Owner direction:** the Ballerina must be completely rebuilt (2026-10-17).
  The owner chose this music-box ballet on 2026-10-18
  (`ODR-BALLET-CONCEPT-20261018`). It supersedes the three-act recital
  contract in `DL-INT-08` once Codex lands it; until then `DL-INT-08` still
  describes the shipping game.
- **Canon used:** the candidate Day Two draft makes the ballet a little stage
  show whose star is Lamma, with Kitty and Bunny; the music box; Roshan
  teaching "Point! Twirl! Bow!" (`design/day_two_story_v2/` on
  `origin/ccr-ba906acd-1aepcb`). The imp's twirl-off is a target rule
  (`DL-INT-14`).
- **Shared systems:** [SHARED_SYSTEMS.md](SHARED_SYSTEMS.md). **Evidence:**
  [REFERENCES.md](REFERENCES.md).

## 1. The idea

Every touch makes Roshan dance. The child is not answering a quiz or tracing
a worksheet: she is the dancer's choreographer and partner. The music box
plays the waltz, Lamma shows the next step, and the child performs it with one
of five one-finger moves on Roshan herself. Roshan starts moving the instant
the finger lands and finishes the step on the music's next beat, so the dance
always looks in time even though the child is never judged against the beat.
A free ribbon dance in the middle and a twirl-off against the imp at the end
complete the show.

## 2. Why this shape

| Pattern | From | How it is used here |
|---|---|---|
| Don't dress a quiz or a tracing exercise up as ballet | Ballerina Toddler Fun Game (a quiz in a tutu), Diva Girls: Diva Ballerina (tracing as the only mechanic, reviewed "Poor"), My Ballet Studio (input that doesn't match the dancer) | No matching portraits, no fixed curve to trace; every input is a dance move Roshan performs |
| Show, then copy | Space Channel 5, Pokémon Diamond/Pearl contest dance round (copy the leader's 3 steps), Just Dance Kids (the leader's hand glows) | Lamma demonstrates each step; the cue sits on the dancer, not on a card strip |
| Move timing judged loosely or not at all for young children | Phillips-Silver et al. 2024 and Eerola et al. 2006 (under-5s rarely lock whole-body movement to the beat); Dance Dance Revolution's Beginner mode lets songs play to the end | The dancer's animation, not the child, lands on the beat |
| One celebrated held pose | Just Dance Gold Moves, Just Dance Kids Freeze bonus, Dance Central 3 Strike A Pose | The "statue" balance: hold until the music box chimes |
| A spin is a circle, capped | Elite Beat Agents spinners (without their uncapped bonus) | The pirouette: one deliberate circle around Roshan, never a scribble race |
| Mistakes change the mood, never end the show; slow rehearsal after trouble | Dance Central (lights dim, Break It Down slows and counts aloud), Space Channel 5 Part 2 (the dance falters) | Lights soften and Lamma shows the step again, slower, with a spoken count |
| Freestyle that is celebrated | Dance Central freestyle, Fantasia: Music Evolved (gestures change the music) | The ribbon dance interlude |
| Kids-mode posture | Just Dance 2018 Kids Mode (positive feedback only, no text, short songs) | No scores, no text, a short waltz |
| Build a routine, then perform it | Toca Dance (pose slots, then a stage show) | A later free-play encore (section 9) |

Avoided: health or rating meters, game over, multi-finger puppeteering, a
strip of small move cards to read, jeering audiences, paid content and
passing with no input.

## 3. Options considered

| Option | What the child does | For | Against | Verdict |
|---|---|---|---|---|
| **A. Music-box ballet (recommended)** | Five one-finger moves performed on Roshan as Lamma shows each step; a ribbon dance; a twirl-off | Every input is dance; research-backed timing; uses Lamma canon | Needs a real ballet animation set | Build |
| B. Rhythm-judged ballet (closing rings on each beat) | Tap, hold or circle when a ring closes on the beat | Strong rhythm-game feel | Asks under-5s to time whole moves to music, which the evidence says they rarely can; overlaps Pop Star's skill | Use only as the optional "well-timed" sparkle |
| C. Choreograph then perform (Toca Dance) | Choose three step cards, then watch and join the show | Creative ownership, replay | Less play on the first visit; a choice step before any dancing | Free-play encore after the first show |

## 4. The five moves

All moves are made on or around Roshan, whose hit region is her whole figure
plus a margin (at least 260×300 base pixels). Each cue is a large pictured
step bubble above Lamma (one at a time, never a strip) plus Lamma performing
it.

| Move | Gesture | What Roshan does | Accepted when | Fallback after two tries |
|---|---|---|---|---|
| Point | Tap Roshan | Rises into the crown pose with arms in fifth, then settles | Any single tap on her | – |
| Twirl | Draw a circle around Roshan, starting on or near her | A full pirouette, tail swirling | At least 270° swept around her centre, either direction, within 2 s | A tap on the glowing twirl ring at her feet |
| Glide | Drag Roshan to the glowing flower spot, or tap the spot | Glides across the stage to it, ribbon trailing | Finger released within the spot's generous area, or a tap on the spot | – (tap is always allowed, per Nielsen Norman Group advice) |
| Balance | Press and keep a finger on Roshan while the music box chimes three times (about 1.5 s) | Arabesque, held, sparkles growing with each chime | 1.5 s of contact, allowing one lift shorter than 0.25 s | 0.6 s of contact |
| Bow | Swipe down on Roshan, or tap the bow bubble | Curtsies (existing curtain-call frames) | A downward drag of 60 px or more, or the tap | – |

A different gesture from the one cued earns no progress: Roshan glances at the
bubble and Lamma shows the step again; nothing is lost. "Two tries" means two
genuine attempts at that gesture (a drag that starts on or near Roshan, or a
press), so plain tapping never unlocks a fallback. Taps arriving while a move
is still being danced are ignored, so a step cannot be skipped by mashing.

Every touch gets a visible response within two frames (`DL-AGE-07`): Roshan's
anticipation frames start at once, and the move's main action lands on the
waltz's next beat (at most 0.71 s later at 84 BPM). The research reason is in
section 2; the motion reason is `DL-MOT-03` (anticipation, action, payoff,
settle). A step done near the "1" of the bar gets a brighter sparkle; nothing
else depends on timing.

## 5. The show, beat by beat

The music is the existing "Ribbon Arabesque" (`opera_ballerina`, 84 BPM, 3/4),
re-arranged into sections in the score catalogue so the waltz can loop a
section while she works (SHARED_SYSTEMS §3). It never stops for a mistake.

| # | Part | What happens | What the child does | Done when |
|---|---|---|---|---|
| 0 | Curtain up | The music box opens and starts the waltz; Roshan glides to the centre of the stage; Lamma waits on her little star pedestal, Kitty and Bunny behind | Nothing required | Roshan in place |
| 1 | Warm-up with Lamma | Lamma shows Point, then Twirl, then Balance, one at a time, each with a bleat and a ghost hand on Roshan | Copy each step | Each of the three moves performed once |
| 2 | Recital, phrase 1 | Lamma and the stuffies show a two-step phrase (Point, Twirl); then the bubbles return one at a time for Roshan | Dance the two steps | Both steps danced |
| 3 | Recital, phrase 2 | Glide to the flower spot, then Balance | Dance them | Both danced |
| 4 | Ribbon dance | A ribbon appears in Roshan's hand; the music swells for eight bars | Drag Roshan anywhere; her rainbow ribbon follows the finger and the stuffies sway | Eight bars pass with her moving; zero input pauses it and Roshan invites her |
| 5 | Recital, phrase 3 | Twirl, Glide, Point (three steps, the longest phrase) | Dance them | All three danced |
| 6 | Twirl-off | The ballerina imp pirouettes in (section 6) | Three twirls | She finishes her three first, or the contest restarts |
| 7 | Bow | Flowers land on the stage; the stuffies bow with her | Bow | Curtain call |

Phrases stay at two or three steps, matching what a 4-year-old can hold in
mind (REFERENCES). No timing window applies to recital steps; the next bubble
appears after the current step is danced. When she has not touched for about
7 s, Lamma repeats the step and the ghost hand shows it (Sesame Workshop
2012). After two genuine but unsuccessful attempts at a step, Lamma shows it
again slowly while Roshan's voice counts "one, two, three"; the waltz softens
until the step is done (Dance Central's Break It Down).

Without repeats the show takes about 75–90 s.

## 6. Twirl-off: the imp contest

This keeps
[the imp contest specification §6.3](../codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md#63-ballerina--twirl-off-race-replaces-the-stage-copy-of-grand-twirl)
(a race, three turns, flub after his second turn, contract C1–C16) but moves
the skill onto Roshan: each of her turns is the Twirl move above, a deliberate
circle around her that she visibly pirouettes. The imp (`rival_ballerina`
family) spins at his mark beside a small music box, alternating `charge` and
`slash`; his purple arc grows turn by turn; he flops dizzily after his second
turn (`bopped` with `fx_dizzy_stars.png`). His pace stays the specification's
provisional 10.5 s for three turns and drops to 0.4 after two failures. He
spins only while she is playing. A scribbled circle counts as one turn at
most per 2 s, so speed cannot beat care. The fallback tap is not available in
the contest (C11 requires the activity's own verb); the radical slowdown is
the mercy there.

## 7. The stage, in words

The existing Ballerina stage painting
(`assets/opera/worlds/backdrops/stage_ballerina_c*r*.png`) frames the show,
with its world painting (`world_ballerina.png`) as the reference for the
music-box gazebo, mirrors and flower tuffets. The open music box
(`assets/opera/worlds/props/goal_ballerina.png`) stands at the front left as
the source of the music. Roshan, in her ballerina costume, dances in the
centre of the stage at full size, always visible (`DL-READ-05`). Lamma stands
on a small star pedestal to her right, a little behind, with Kitty and Bunny
behind Lamma. The step bubble floats above Lamma. Two or three flower spots
for glides are painted cards on the stage floor, left and right of centre.
No dark corridor, ring or code-drawn ribbon appears; the twirl ring at her
feet is painted art and shows only as a fallback.

## 8. Art, animation and sound to produce

| Item | Description | Notes |
|---|---|---|
| Roshan ballet set | Whole-frame sprites in the ballerina costume: waltz idle sway, Point (rise to crown pose), Twirl (a full pirouette cycle), Glide left and right, Balance (arabesque with a gentle held sway), wobble (a happy recovery when a balance ends early), Bow | The current atlas cells are pose keys that cannot be looped (`DL-MOT-09`); this is new animation under `DL-MOT-12` and `DL-MOT-14` to `DL-MOT-16`. Pilot the Twirl first. One whole drawing per frame, constant size, left and right only for travel (owner decisions 2026-10-04 to 2026-10-07) |
| Lamma | Demonstration poses for each step (point, twirl, balance, glide, bow), a happy bounce, a bleat-shaped idle | `assets/minigames/seek/lamma_animation.png` (8 frames) is the identity reference |
| Kitty and Bunny | Sway, copy-step and bow poses | Use approved stuffie art if it exists; otherwise new art in the same painted style |
| Step bubbles | One painted bubble per move, showing Roshan's silhouette doing it | Wordless |
| Stage cards | Flower glide spots; the twirl ring for the fallback; footlights that brighten after each phrase; flowers for the bow | Painted cards, not code shapes (`MA-VIS-008`) |
| Ribbon | A painted rainbow ribbon strip that trails Roshan's hand in the ribbon dance | One owned card stretched along recent finger samples; check overdraw |
| Imp | Existing `rival_ballerina` poses plus a small music box | Contest §4.16 art-reuse rules |
| Music | "Ribbon Arabesque" arranged in loopable sections: curtain, warm-up, three recital phrases, ribbon swell, twirl-off, bow | `tools/build_area_music.py`; the music box chime as a separate one-shot for the Balance count |
| Voice | Exact new Roshan cues: "Let's dance with Lamma!", "Tap me to point!", "Draw a circle around me to twirl!", "Slide me to the flower!", "Hold me still while the music box sings!", "Swipe down to bow!", "Dance with your ribbon!" | Lamma has bleats only; existing synthetic Roshan workflow |

## 9. Routes, saves, story and later play

- **Free play:** the Opera Hall's Ballerina door (`DL-INT-12`).
- **Saves:** keep the existing career star bit and medal keys; add, with
  defaults, the last completed part index (`DL-SAVE-01`). Re-entry resumes at
  the start of the last unfinished part.
- **Medals, wordless:** bronze for the finished show; silver when no step
  needed its fallback or slow rehearsal; gold when, in addition, the twirl-off
  was won on the first attempt.
- **Day Two story:** the same engine with Lamma on the star pedestal and the
  draft's lines ("Point!", "Twirl!", "Bow! Our show is ready!"); no imp
  (contest C13). The draft's dead-end story goals (DIAGNOSIS §3) disappear
  because each step is a single completion.
- **Encore (later, optional):** after the first finished show, a "make your
  own dance" card lets her pick three steps from two or three big step cards
  each, then perform her dance with Lamma (Toca Dance pattern). Not part of
  the first build.

## 10. What retires

PEARL MIRROR (portrait matching with an answer-revealing demonstration),
RIBBON TRAIL (fixed sine tracing over a dark corridor) and GRAND TWIRL as
built today; the practice-then-stage duplication for Ballerina in
`OperaPerformancePlan`; the stage-long rival race; code-drawn shells, ribbon
and ring. The current surface's good habits carry forward: one geometry for
paint, demonstration and hit testing; monotonic progress; assistance clocks
that exclude demonstration time and never pay.

## 11. Acceptance tests

Machine (a new trusted probe plus `probe_opera_2d` and
`probe_opera_gesture_quality` updates):

1. Zero input for 120 s: no step completes; Lamma re-invites; nothing is
   awarded.
2. A scripted child performing each cued gesture completes the show; Roshan's
   action frame for each step lands on a beat boundary (within one frame).
3. Taps alone cannot complete a Twirl, Glide-by-drag, Balance or Bow, and do
   not unlock fallbacks; a 5 Hz tapper completes only Point steps, no faster
   than the scripted child.
4. A circle that sweeps less than 270°, or is drawn far from Roshan, does not
   count; a circle in either direction does.
5. Balance: 1.5 s holds count; one lift under 0.25 s is forgiven; after two
   short attempts, 0.6 s counts.
6. One finger owns its gesture until release; a second finger cannot start
   another (`DL-UI-04`); pause, focus loss, Back and close cancel a held
   Balance without credit (`DL-UI-05`).
7. Twirl-off follows contest C1–C16, including restart within 2 s, the 0.4
   pace after two failures, and one turn at most per 2 s.
8. Save and re-entry at each part; no duplicate star or medal.
9. Overdraw states for warm-up, ribbon dance and twirl-off pass OD1–OD6.

Human: does the child understand "Lamma shows, I dance"? Can she make the
circle and the hold on the phone? Does she want to dance again? Owner
identity and style review of the new animation. Machine success grants none
of these.
