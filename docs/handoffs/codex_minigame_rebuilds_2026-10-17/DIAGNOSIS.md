# Why Pop Star, Ballerina and Racer are weak: current-state diagnosis

- **Status:** `SUPPORTING_CURRENT` analysis for the rebuild handoff. It grants no
  acceptance and changes no game file.
- **Baseline:** `dev` at `7a65b9f0abacddeee70230f220955f4d18d551b5`
  (2026-10-17). Every `file:line` anchor below refers to that commit.
- **Method:** source reading of the three careers and their shared host, the
  gold-star scorecard (`design/reference/games.json`, assessed at `87f99268`),
  the 2026-10-12 Luna study's scripted timing and code reviews, and direct
  inspection of the existing art files. No game capture was made, per the
  CLAUDE.md written-handoff rule.
- **Owner verdict (2026-10-17):** "The weakest of the minigames so far are the
  pop star, the ballerina, and the racer ... These need to be completely
  rebuilt, current version are very weak. One minigame, the note memory one, in
  the pop star, is a usable mechanic, even if the shell is poor."

## 1. What the child actually does today

| Game | Activities a child plays | What the finger does | What Roshan does | Real decision or skill | Music or speed |
|---|---|---|---|---|---|
| Pop Star | 7 in the Opera Hall: SOUND CHECK, DANCE, RHYTHM as practice, then all four again on stage with ENCORE | Hold to fill; tap the glowing lane; tap three stars back in order; draw a circle | Stands beside a 500×376 activity panel | Order of 2–3 stars, at any tempo | None tied to play |
| Ballerina | 6: PEARL MIRROR, RIBBON TRAIL, GRAND TWIRL, twice | Tap the portrait the ghost finger just tapped; trace one fixed wave; drag once around a ring | Holds one static pose key at a time | None left after the demonstration | None tied to play |
| Racer | 3: TUNE, TO THE LINE, RACE | Draw circles; swipe; hold a slider bar for about 48 seconds | A cropped bust inside a 150 px kart on a fixed painting | Steering moves the kart at most about 19 px | No camera, no speed sensation |

Gold-star scores at the last assessment: Pop Star 13/24, Ballerina 14/24,
Racer 15/24 (`python -B tools/gold_star.py --rank`). All three are rated 1/5
because no child can yet reach them from a fresh save (`MA-PLAY-005`), but
their core-loop criteria are also below the gold star: C5 (kind no-fail and
real agency) and C6 (truthful action) are each at most 1/2 in at least two of
the three.

## 2. Pop Star today

**Structure.** The shipping table is SOUND CHECK (`hold`, goal 3.8), DANCE
(`choice`, goal 6), RHYTHM (`echo`, goal 3) and ENCORE (`circle`, goal 1.8)
(`scripts/opera_career_world_2d.gd:343-348`). Because Pop Star is one of the
three Opera Hall careers, `OperaPerformancePlan` copies the first three
activities into a practice part and then plays all four again on stage
(`scripts/opera_performance_plan.gd:8-34`). The child therefore plays seven
activities, three of them twice. The Luna study's scripted personas needed
78.6, 96.1 and 127.0 seconds of game clock for this
(`audit/cycles/luna-playtest-20261012/TIMING_SUMMARY.md`).

**SOUND CHECK** is a hold-to-fill gauge. The microphone pulses and code-drawn
sound arcs and note dots grow with the fill
(`scripts/opera_gesture_surface.gd:2644-2690`). Holding still is the whole
skill.

**DANCE** is the generic `choice` mode: the screen is split into lanes and the
lane under the finger is compared with the glowing target lane
(`scripts/opera_gesture_surface.gd:965-970`). The voice says "Tap the glowing
dance arrow!" The answer is shown, so there is nothing to decide and nothing
is danced. A wrong lane pays a progress crumb (`_miss_pay`, `:399-404`).

**RHYTHM (the note-memory echo)** is the one mechanic the owner keeps. Three
stars sit at fixed points across the panel (`:5903-5905`). The stars sing a
verse one note at a time, 0.55 s apart (`:5907-5930`); verses are
`[0, 2]`, `[0, 1, 2]` and `[2, 1, 0]` (`:114`). The child then taps them back.
The source comment states the design: the child taps them back "in ANY tempo",
order matters and speed never does (`:111-113`). A tap selects the nearest
star within 92 px (`:5937-5944`). A wrong star replays the verse and pays a
0.05 crumb once per cooldown (`:5962-5968`, `:399-404`). Taps during the
demonstration only twinkle (`:5945-5949`).

What works: clear turn-taking (listen, then answer), pitched notes per star,
a harmless replay, and fine-grained checkpoints (gold-star C9 2/2). What is
missing: a beat. Nothing the child does is timed against music, so it is a
memory toy rather than a rhythm game, which the owner also told Codex earlier
today ("This is supposed to be a rhythm game, not just a repeating game").

**ENCORE** is the shared `circle` crank (`_draw_popstar_crank`,
`:2484-2512`): draw a circle and the microphone leans.

**Staging.** On stage, every Pop Star activity runs inside a 500×376 action
panel in the middle of the screen; Roshan is a 300 px actor at the left and
the rival a 220 px actor at the right (`scripts/opera_career_world_2d.gd:5120-5146`).
The rival "races" through his own input-transparent copy of the same widget
(`:5201-5226`). The pop star never sings, plays, dances or faces a crowd; the
show is a card on a stage.

**Scorecard notes** (games.json): the echo stars are code-drawn when their
art is missing and the medal overlay is code-drawn with number labels (C7);
other actions are silent and the win is a generic cheer (C8); the activity
uses the generic gesture surface without per-finger ownership (C4).

## 3. Ballerina today

**Structure.** PEARL MIRROR (`ballet_pose`, goal 3), RIBBON TRAIL
(`ballet_ribbon`) and GRAND TWIRL (`ballet_twirl`)
(`scripts/opera_career_world_2d.gd:282-286`), played once as practice and once
on stage, so six activities.

**PEARL MIRROR.** Three rounds. Roshan holds the target pose and the child
taps the matching portrait among two or three
(`scripts/opera_ballet_surface.gd:19-26`). Every round starts with a 2.15 s
demonstration during which input is blocked (`:28`, `:214-219`, `:314-316`),
and the ghost finger travels from the target portrait to the correct answer
(`:734-747`). The child then taps where the ghost tapped. The intended
"watch and match" decision is made for her before she can act.

**RIBBON TRAIL.** One fixed sine curve from the left edge to the right
(`:155-162`), painted as stacked code-drawn lines over a dark corridor
(`:639-681`). Forward tracing banks progress; lifting and resuming is safe
(`:433-468`). It is a tracing worksheet: the curve does not move, does not
follow the waltz, and Roshan does not travel along it.

**GRAND TWIRL.** One full turn of a handle around a code-drawn ring around the
music-box art, either direction (`:494-548`). Pose cues change in thirds of
the turn.

**Roshan.** Her ballerina atlas cells are pose keys, not in-betweens;
neighbouring cells jump 41.6–47.3% in silhouette, so the runtime may only hold
a pose (`DL-MOT-09`). She therefore cannot dance in the current game: each
"move" is a cut to a still.

**Music.** The career cue "Ribbon Arabesque" is an 84 BPM 3/4 waltz
(`assets_src/audio/music/area_music_scores.json`, id `opera_ballerina`), but
no action is tied to its beat.

**Story run.** The Chapter 2 phase set asks for goals of 6 and 2 that the
surface can only pay 1 against, a dead end recorded on the scorecard (C5).

What works and should survive the rebuild: one geometry for paint,
demonstration and hit testing; monotonic banked progress; assistance clocks
that exclude demonstration time and never pay progress (`:258-274`); and a
twirl that accepts either direction.

## 4. Racer today

**Structure.** TUNE (`circle`, goal 1.8), TO THE LINE (`swipe`, goal 5) and
RACE (`kart_race`, two laps) (`scripts/opera_career_world_2d.gd:331-335`).
TUNE and TO THE LINE are generic crank and push chores.

**The race.** A small kart follows a closed `Curve2D` traced over the static
painted `world_racer` circuit (`scripts/opera_racer_surface.gd:19-26`,
`:100-111`). Two laps of 24 s each (`:11`, `scripts/kart_driving.gd:6`) take
about 49.8 s of holding in the centre-hold diagnostic
(`design/OPERA_RACER_ENGINE_INTEGRATION_2026-09-05.md`).

**Steering barely shows.** The control is a 770×126 bar at the bottom of the
screen (`:14`). Its x position sets the steering value (`:195`), which moves
the kart's lateral offset up to the wall value 8 (`:12`,
`scripts/kart_driving.gd:131-141`), drawn at 2.4 px per unit (`:119`): at most
about 19 px either side of the centre line on a 1280 px canvas. Pearls sit at
offset 3, about 7 px off centre (`:31-35`). At phone size the child cannot see
steering do anything.

**Holding is enough.** The kart drives whenever a finger is down, and for 2 s
after it lifts (`:13`, `:244-251`). Holding any point of the bar completes both
laps (scorecard C5). Turbo is a separate 120 px button at the bottom right
(`:15-16`) that also auto-fires when its meter is full.

**The result is fixed.** The rival runs at 0.94 of nominal pace with a
catch-up clamp (`:298-305`), and only Roshan's finish ends the race
(`:311-314`), so she always wins and the rival never matters. The owner's
`DL-INT-14` rule (the imp's kart finishing first is his win and restarts the
race) is not implemented.

**Presentation.** The kart is 150 px at most, scaled 0.65–1.0 by depth, with
Roshan drawn as a cropped bust (`:373-417`). There is no camera, parallax,
speed line or sense of distance; the painting never moves. The steering bar,
lap dials, turbo and countdown lights are code-drawn (`:419-469`).

What works and should survive: the shared `KartDriving` kernel (charge, turbo,
drift, wall assist), per-touch ownership with pause and focus-loss
cancellation (`:129-169`, `:219-233`), no movement without input, and the
existing painted kart, wheel, driver and rival art.

## 5. Causes the three share

1. **A shared motor primitive stands in for the job.** Hold, choice, circle,
   swipe and trace are reused motor verbs. `DL-INT-07` allows shared
   primitives but requires each career's signature engine to express its job;
   here the primitives are the whole game.
2. **Time does not matter.** Two performance careers have no beat and a race
   has no speed. The defining pleasure of each fantasy is missing.
3. **The performer is a sticker.** Roshan does not drum, sing, dance or
   visibly drive. That breaks the spirit of `MA-PLAY-004` and `DL-INT-02`
   (Roshan does the job, at the place, with visible contact) and
   `DL-MOT-07` (an animated character must advance authored frames).
4. **Controls are interface, not world.** A slider bar, a ring, a lane strip,
   stars on a panel. `DL-INT-01` is met technically, because the hit regions
   match what is drawn, but what is drawn is a widget rather than a drum, a
   dance or a road.
5. **The demonstration decides.** The ballet ghost finger shows each answer;
   DANCE lights the answer lane.
6. **Repetition without growth.** The Hall performance plan replays each
   chore, so a child does the same hold, choice and echo twice in a row.
7. **Generic payoff.** A cheer, a code-drawn medal overlay with digits, no
   finale song, no podium or photo finish.

## 6. What the stronger careers do differently

The scorecard and code show a common pattern in the careers that hold up
better:

| Career | The one real skill | Why it works |
|---|---|---|
| Boxer | Punch when the target opens | Timing skill; one punch per press; contact puff at the impact point; per-finger ownership (scorecard C4, C5 2/2) |
| Magician | Follow the hat through the shuffle | Attention skill; the hat really travels over Lamb-a'; the cabinet opens only with a downward pull (C6 2/2) |
| Nursery | Slide the cradle under falling babies | Continuous steering from a touch anywhere, with mercy after two misses (C5 2/2) |
| Geologist | Dig, brush, wash, crack | The material really changes under the finger (`design/GEOLOGIST_REBUILD_2026-09-05.md`) |
| Teacher | Count, match, complete the pattern | A real question; every pearl is spoken (C3, C8) |
| Mermaid Pool (gold-star reference) | Travel, contact, then credit | Roshan goes to the place and the tool does the work there (GS-01, GS-02) |

The rebuilds should keep that pattern: one real skill that belongs to the job,
a world object that visibly changes, Roshan acting at the place, and mercy
that widens a window or slows a cue rather than completing the work.

## 7. What can be reused

| Kind | Asset or system | Note |
|---|---|---|
| Backdrops | `assets/opera/worlds/backdrops/world_{popstar,ballerina,racer}.png` (1024×576 keys) and their 2×2 world and stage tiles | The Pop Star stage tiles already paint a proscenium with curtains and a musical rainbow ribbon |
| Roshan | `assets/opera/worlds/actors/animation/roshan_{popstar,ballerina,racer}_sheet_a.png` (4×4, 256 px cells) | Pose keys only (`DL-MOT-08`, `DL-MOT-09`); identity and costume references for new animation |
| Rivals | `assets/opera/worlds/actors/rival_{popstar,ballerina,racer}*.png`, 13 poses each | Already used by the imp-contest specification |
| Props | `goal_popstar.png` (microphone), `goal_ballerina.png` (music box), `goal_racer.png` (trophy); `widget_crank_racer_kart.png` (side-view kart, front facing left), `widget_crank_racer_wheel.png`, `assets/kart/boost_ribbon.png`, `assets/kart/finish_banner.png` | The kart is drawn in side view, which suits a side-scrolling race |
| Friends | `assets/minigames/seek/lamma_animation.png` (Lamma, 8 frames), `assets/sprites/stuffie_studio/lamma.png` | Lamma is the star of the Day Two ballet draft |
| Band (unmerged) | `assets/prototypes/bands/roshan_drums.png`, `daddy_ukulele.png`, `eagle_bass.png` on `origin/codex/battle-of-bands-20260920` | `CANDIDATE` prototype art; Roshan at a shell kit with two toms, a bass drum and a cymbal |
| Music | `opera_popstar` "Starlight Singalong" 118 BPM 4/4 with a call-and-answer motif; `opera_ballerina` 84 BPM 3/4 waltz; `opera_racer` 128 BPM drive | Rendered by `tools/build_area_music.py` from declarative scores, so exact beat maps and separate parts can be derived |
| Music (unmerged) | Iko Iko v89 derivative `assets/prototypes/bands/iko_iko_v89.ogg` on the bands branch | Game-use rights are an open owner decision (Day Two decision 15) |
| Code | `scripts/kart_driving.gd`; `scripts/games/dance_engine.gd` (audio-clock judging, 0.46 s window, 2.55 s travel; scorecard: mashing all lanes hits everything); `scripts/games/melody.gd` (press-ownership guards) | Reuse the clock and ownership patterns, not the flat presentation |
| Code (uncommitted) | `scripts/popstar_rhythm_phrase.gd` in Codex's `popstar-rhythm-20261017` worktree | Clock-based judging, 2.4 s preview, ±0.30 s window, first-in-window ownership, generation counters; not yet published |
| Rules | `DL-INT-14` imp contests (target) and `docs/handoffs/codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md` | Twirl-off, Grand Prix and Sing-off are specified there for today's mechanics |
