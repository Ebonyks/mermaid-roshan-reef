# Boxer engine roadmap (2026-11-01)

Status: `PROPOSED / CANDIDATE` design reference for the Boxer's return visits.
Editions 1 and 2 are commissioned in the [work order](README.md); Editions 3–5
and the boss toolkit are planned here and need their own handoffs. The owner
accepted the edition order and these defaults on 2026-11-01
(`ODR-BOXER-EDITION-ORDER-20261101`, `ODR-BOXER-FAMILY-SPARRING-20261101`,
`ODR-BOXER-NO-DODGE-20261101`, `ODR-BOXER-FLOATING-GLOVES-20261101`). Story
placement is out of scope by owner direction (`ODR-BOXER-EDITIONS-20261101`).

## 1. Core idea

Keep the opponent's threat in its floating gloves, and describe every attack
as data: a path, a timing on the beat, and a warning. The current Title Imp is
already two floating gloves. A new attack is then data plus a pose or two of
glove art, not a new body animation. Roshan's side stays the same two gloves
under her finger, so each edition adds a situation, not a control.

Punch-Out!! on the Wii followed this pattern in its Title Defense mode:
beaten opponents return faster, with new moves and new ways to protect their
weak spots ([Wikipedia](https://en.wikipedia.org/wiki/Punch-Out!!_(2009_video_game));
[Nintendo World Report](https://nintendoworldreport.com/review/18483/punch-out-wii)).

## 2. Rules every edition keeps

1. **The warning never lies.** The swoosh shows exactly the path and timing
   the blocking check uses. There are no fake-outs; a delayed punch shows its
   extra beat honestly.
2. **One new idea per edition**, with everything earlier returning, remixed.
3. **One finger finishes everything** (`DL-AGE-02`, `DL-INT-09`). Two
   fingers are a bonus, never a requirement.
4. **Defense matters, nothing is lost** (`DL-AGE-03`). Unblocked punches stay
   harmless and progress never goes backward. A first-to-N bout (`DL-INT-14`)
   restarts and never erases anything.
5. **Intent beats noise** (`DL-AGE-04`, `DL-AGE-05`). Every scoring action
   needs a readable intent, and random scribbling stays measurably slower
   than purposeful play.
6. **Fair timing for small hands.** At least 2.0 s from warning to contact at
   entry level, a counter window of at least 2.4 s, fixed windup lengths and
   a steady beat.
7. **Flash-safe by construction.** At most 3 flashes in any second, at least
   334 ms between flash starts, at most 2.5 s of flashing per warning, and one
   small flashing area at a time.
8. **Skill adds celebration and never takes progress away.** The positive
   tiers Pop, Sparkle and Pearl come from the unmerged Boxer V2 design
   (`ed4851a0`).

## 3. Opponent move set

| Move | What it adds to play | Engine need | Edition |
|---|---|---|---|
| Jab | Straight to the chest emblem or a side pad | Exists; lanes must be spread | 1 |
| Hook | Guard at the side; counter the open side | Curved paths; counter target per side | 2 |
| Combo | Two or three punches on the beat (jab-jab, jab-hook, hook-hook alternating) | Several attacks at once; beat clock | 3 |
| Delayed punch | An honest extra beat shown in the count-in; teaches waiting for "go" | Per-attack beat timing | 3 |
| Body shot | A low path; guarding gains an up-and-down dimension | Low targets; vertical lanes | 4 |
| Guard stance | The opponent covers one side or high/low; punch the open spot | Opponent defense zones | 4 |
| Sway | The opponent's target drifts left and right | Moving counter targets | 4 |
| Big swing | Slow, wide and long-warned; a good block makes the opponent dizzy | Large fist; long warning; dizzy state | 5 |
| Thrown ball | Soft balls from the corners; block or bat back for a bonus | Projectiles in the same contact system | 5 |
| Two opponents | Attackers on the left and right taking turns | Several attackers; one flashing area at a time | 5 |

## 4. Roshan's moves

| Move | Gesture | Why it is fun | Edition |
|---|---|---|---|
| Guard | Put a glove in the path | Stopping a punch feels strong | 1 |
| Counter | Push a glove forward into the open target | Her turn to bop | 1 |
| Aimed counter | Punch the side that opened | Her first real decision | 2 |
| Early catch | Block near the start of the punch's path | Brighter Sparkle, faster power meter; never required | 3 |
| One-two | Two counters with alternating gloves in one opening | A rainbow link (from V2) | 3 |
| Pearl Power | No button: a meter fills from blocks and counters, and the next counter becomes a super punch | Earned spectacle; the meter never drains (from V2) | 3 |
| Uppercut | A quick upward flick from low while the opponent is dizzy | A finisher with a big payoff | 4 |
| Two-glove guard | Place one glove, then the other; "sticky" gloves stay put | Building a wall with one finger | 5 |

Ducking and dodging stay out (`ODR-BOXER-NO-DODGE-20261101`). They would need
a new Roshan body pose under the identity rules, and a gesture that competes
with glove dragging.

## 5. Edition ladder

Each return keeps today's shape: guide, drills that teach the new idea, bout,
belt.

| Edition | Headline | Supporting | New drill | Returns remixed |
|---|---|---|---|---|
| 1 Jab and Guard | Today's game with the review fixes, spread lanes and the new warning | Launch and "now" sounds | Current drills, retimed | None yet |
| 2 Hooks | Hooks from both sides | Aimed counters on the open side | Hook Pad | Jabs |
| 3 Rhythm | Combos on the beat | Early catch, one-two, Pearl Power | Beat Pads | Jabs, hooks, aimed counters |
| 4 Read the Guard | Opponent stances | Body shots, sway, uppercut finisher | Open-Spot Mitts | Combos, Pearl Power |
| 5 Two at Once | Two attackers or thrown balls | Big swings, two-glove guard | Wall Builder | Everything earlier |
| Boss-ready | Phases that switch move sets, super attacks with long warnings, a finisher sequence | A hosting interface for another scene | Optional practice of any phase | All moves |

Difficulty may start each edition from Roshan's measured skill in the previous
one, never below the safe timing floors.

## 6. Engine features beyond Editions 1–2

| Feature | What it does | Edition |
|---|---|---|
| Scoring and mercy, full | First-to-N with restart, the power meter, and per-phase scoring rules | 3 |
| Local skill telemetry | Reaction times, blocks by move and side, counter speed, kept on the device and shown in the DEV playtest menu. An optional saved skill profile (new save keys with defaults) can set the next edition's starting level. | 3 |
| Attack source switch | Punches come from the opponent brain or from a person | 3 |
| Family Sparring | A parent taps punch buttons on their side of the tablet while Roshan defends and counters, under the same warning and safety limits. Parent-started and outside the required path (`ODR-BOXER-FAMILY-SPARRING-20261101`). | 3 |
| Free Sparring Ring | Replay any opponent she has met, at her current level | 3 |
| Guard zones and moving targets | Opponent stances, sway and low targets | 4 |
| Upward-flick recognizer | Uppercut finisher with an intent check | 4 |
| Several attackers and projectiles | Two opponents, thrown balls, one clear first contact per object | 5 |
| Sticky gloves | Placed gloves stay put for building a two-glove guard | 5 |
| Boss toolkit | Phases with their own move sets and visuals, super attacks with long warnings, a finisher sequence, events plus pause and resume so another scene can host a bout | Boss |

The boxing warning is new for boxing and borrows nothing from Grand Puff's
(`ODR-BOXER-WARNING-20261101`). If the engine later hosts a boss, its
relationship to the boss-warning trope in
[`BOSS_SPLASH_DESIGN_LANGUAGE.md`](../../../design/BOSS_SPLASH_DESIGN_LANGUAGE.md)
needs an explicit owner decision at that time.

## 7. Gates every edition must pass

| Gate | Threshold |
|---|---|
| Counter chances | The typical player takes at least 80%, the slow player at least 60% |
| New move | The typical player blocks the edition's new move at least 70% of the time after its drill |
| Random play | Random scribbling at least 1.5 times slower than the typical player in every phase |
| Parking | No single parked glove (or two-glove wall, before Edition 5) blocks more than half of a mixed bout |
| Warning honesty | The swoosh matches the collision path within 1 px, and every flash schedule passes the safety limits |
| Contact | No wrong call more than 1 px from the contact edge at a steady 30 and 60 fps |
| Length | A typical full visit under 5 minutes, with no gap between points over 15 s at the 90th percentile |
| Passive | No input earns nothing, on phone and tablet |

## 8. What makes it fun beyond the rules

- **Personality through the gloves.** Each opponent gets a signature move
  with a funny, readable tell: a wiggle before its hook, a little dance after
  a miss.
- **Earned spectacle.** Pearl Power, a dizzy spin, and the opponent's bow.
  Basic play always earns the finale; skill earns it sooner.
- **Feel.** A brief freeze on impact (a few dozen milliseconds) helps a hit
  register. It belongs to a stack with squash, a small shake, particles and
  layered sound
  ([Sakurai on hitstop](https://sourcegaming.info/2015/11/11/thoughts-on-hitstop-sakurais-famitsu-column-vol-490-1/);
  [Critical Points](https://critpoints.net/2017/05/17/hitstophitfreezehitlaghitpausehitshit/)).
- **Short rounds with a breath between them**, matching the chapter guide's
  call for natural stopping points.
