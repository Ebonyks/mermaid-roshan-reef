# Rebuilding Pop Star, Ballerina and Racer: Codex handoff

- **Status:** `PROPOSED / CANDIDATE`. Owner-requested analysis and redesign;
  the designs await the owner's answers to section 6 (defaults apply until
  then). Publication grants no visual, device, child or owner acceptance.
- **Prepared by:** Claude, as written analysis and specification only: no
  game change, no image (CLAUDE.md "Claude writes, Codex builds images").
  Codex implements.
- **Recipient:** Codex.
- **Evidence baseline:** `dev` at `7a65b9f0abacddeee70230f220955f4d18d551b5`.
- **Delivery:** this folder on the project's GitHub repository, with a
  SHA-256 manifest ([MANIFEST.json](MANIFEST.json)).
- **Records:**
  - finding [`MA-OPERA-014`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-014);
  - owner decision `ODR-MINIGAME-REBUILD-20261017` in
    [the decision register](../../../design/reference/OWNER_DECISIONS.md);
  - [impact record](../../../design/audit_impacts/minigame-rebuild-handoff-20261017.json).

## 1. The request

The owner, 2026-10-17: "The weakest of the minigames so far are the pop star,
the ballerina, and the racer (there are several games build in this minigame
that are superior) analyze potential improvements and redesigns from the
ground up, citing game designs used in other similar games for consoles, pc
or android. These need to be completely rebuilt, current version are very
weak. One minigame, the note memory one, in the pop star, is a usable
mechanic, even if the shell is poor."

## 2. The verdict in one table

| Game | Why it is weak today ([DIAGNOSIS.md](DIAGNOSIS.md)) | The rebuild | Spec |
|---|---|---|---|
| **Pop Star** | Seven chores with no beat: hold a microphone, tap the lit lane, repeat three stars at any tempo, draw a circle, half of them twice, in a panel beside a static Roshan | **Roshan's Rainbow Band.** The family band plays a song; Daddy's band calls a phrase and Roshan answers it on her drums in the next bar. This is the owner's note-memory echo, now in time. Ribbons fall onto the real drums for play-along choruses; the crowd sings back when she leads; a big finish; a drum-off against the imp | [POP_STAR.md](POP_STAR.md) |
| **Ballerina** | A demonstration taps the right portrait before she can; a fixed wave to trace; one circle; Roshan can only hold still poses | **Lamma's Music-Box Ballet.** Lamma shows a step and the child dances it on Roshan with one of five one-finger moves (point, twirl, glide, balance, bow). Roshan lands every step on the waltz's beat, so the dance always looks in time. A free ribbon dance, then a twirl-off against the imp | [BALLERINA.md](BALLERINA.md) |
| **Racer** | Hold a slider bar for about 48 s while a 150 px kart circles a still painting; steering moves it at most about 19 px; she always wins | **Reef Grand Prix.** A side-scrolling three-lane race through painted parallax reef layers. Tap a lane to swerve into rings and ramps and past gentle bumps. The imp's kart really races her and can win, which restarts the race; he slows after two losses. First she picks her kart's colour and fits its wheels | [RACER.md](RACER.md) |

All three share one music clock, cue judge, mercy rules, contest hookup and
probe plan ([SHARED_SYSTEMS.md](SHARED_SYSTEMS.md)). The designs cite
published games and child-development research
([REFERENCES.md](REFERENCES.md)). Two research findings shaped them most:
- a third of 3–4-year-olds could not lock to a beat even with a live adult
  partner, so rhythm must reward rather than gate;
- 4–5-year-olds steer and track poorly, so the race uses lanes, not steering.

## 3. What the stronger careers teach

From the scorecard and code (DIAGNOSIS §6): Boxer, Magician, Nursery,
Geologist, Teacher and the Mermaid Pool each give the child one real skill
that belongs to the job, a world object that visibly changes, Roshan acting at
the place, and mercy that widens or slows rather than playing for her. The
three rebuilds follow that pattern.

## 4. Files

| File | Role |
|---|---|
| `README.md` | Entry point, work order, owner questions |
| `DIAGNOSIS.md` | Current-state analysis with code anchors at the baseline |
| `POP_STAR.md` | Pop Star rebuild specification |
| `BALLERINA.md` | Ballerina rebuild specification |
| `RACER.md` | Racer rebuild specification |
| `SHARED_SYSTEMS.md` | Clock, judge, mercy, move reader, contests, staging, saves, probes, art order |
| `REFERENCES.md` | Game and research references with links |
| `MANIFEST.json` | Byte sizes and SHA-256 of every file |
| `.gdignore` | Keeps Godot from importing this folder |

## 5. Work order for Codex

| ID | Work | Depends on | Done when |
|---|---|---|---|
| MR0 | Read the owner's answers; update the imp contest specification §6.3, §6.11 and §6.12 to match | Section 6 | Specification and register agree |
| MR1 | BeatKit (SHARED_SYSTEMS §2), folding in Codex's uncommitted `popstar_rhythm_phrase.gd`, plus `probe_beatkit.gd` | – | Probe green on exact Godot 4.7.2; clock proved on the target phone |
| MR2 | Pop Star: concert arrangement and chart from the score; band staging; echo, chorus, crowd break, finish; drum-off; `probe_popstar_band.gd` | MR1, MR5 pilot | POP_STAR §11 machine legs green |
| MR3 | Ballerina: move reader; recital sections; ribbon dance; twirl-off; `probe_ballet_show.gd` | MR1 clock, MR5 pilot | BALLERINA §11 machine legs green |
| MR4 | Racer: lane model; paddock; course; imp race; `probe_racer_lanes.gd` | MR5 course art | RACER §11 machine legs green |
| MR5 | Art and animation: pilot one action per game (bass-drum strike, pirouette, lane-change lean); owner look; then the full sets and course layers | Owner's look at each pilot | Assets with provenance, licences and hashes; whole-frame sprites |
| MR6 | Voice: the exact new Roshan cues and imp lines with the existing synthetic workflow | – | Every objective has its exact cue (`DL-SND-01`) |
| MR7 | Integration: remove Pop Star and Ballerina from `OperaPerformancePlan.ENABLED`; retire the stage-long rival race for them; additive saves; routes; Chapter 2 adapter; update `DL-INT-07`, `DL-INT-08`, `DL-INT-10`, `DL-INT-14`, `DL-QA-12`; gold-star re-assessment and `--rebind`; overdraw measurement | MR2–MR6 | Full trusted suite green; OD1–OD6 measured; records updated |
| MR8 | Acceptance: phone latency and frame pacing; one observed child session per game; the owner's verdict | MR7 | Recorded separately; machine success grants none of these |

Suggested order: MR1 first; the Pop Star next, because Codex's rhythm work on
it is already in progress; then the Ballerina and the Racer. Art pilots can
start at once.

## 6. Questions for the owner

Codex proceeds on the default unless the owner chooses otherwise.

| # | Question | Default |
|---|---|---|
| Q1 | Pop Star core: the timed echo plus play-along choruses, or ribbon play-along only (the direction Codex drafted on 2026-10-17)? | Timed echo plus play-along: it keeps the note-memory mechanic you called usable and makes it a rhythm game |
| Q2 | Pop Star song: a new concert arrangement of the existing "Starlight Singalong", or Iko Iko? | The original song first (clean rights, exact chart from its score). Iko Iko for the Day Two story once its game-use rights are confirmed |
| Q3 | Pop Star band: Daddy and Baby Eagle, or an Opera house band so the family band stays special to the birthday story? | Daddy and Baby Eagle |
| Q4 | Ballerina: the music-box ballet (dance at her own pace; Roshan lands on the beat), a rhythm-judged ballet, or "make your own dance" first? | Music-box ballet; "make your own dance" as a later encore |
| Q5 | Racer: the side-scrolling three-lane race with a colour and wheels pit stop, or a following camera over the existing painted circuit? | The side-scrolling race |

Not asked because they are already decided or are defaults:
- **Retire the practice duplication and the stage-long rival race.** These go
  for the two Hall careers: the imp contest packet already recommends
  retiring the stage-long race.
- **One imp contest at the end.** `DL-INT-14` already requires it.
- **A rich, whole-frame animation set.** The owner decided this on
  2026-10-04 and 2026-10-07.

## 7. Relationship to other work

- **Codex, Pop Star rhythm (2026-10-17, uncommitted).** Codex recorded the
  owner's instruction "This is supposed to be a rhythm game, not just a
  repeating game" and drafted a timing helper and a falling-ribbon
  direction. That work lives in the `popstar-rhythm-20261017` worktree and is
  not yet on GitHub. POP_STAR.md extends it rather than replacing it: the
  helper's judging becomes BeatKit's core, and the play-along becomes the
  choruses.
- **Imp contests (`DL-INT-14`).** The target rule stays; this packet
  re-specifies three of its contests for the rebuilt skills.
- **Day Two draft and Battle of the Bands (unmerged).** The candidate Day Two
  draft and the battle-of-bands prototype are the canon sources for the
  family band, Iko Iko and Lamma. Both remain candidates on their branches.
- **Job platform.** If its content layer lands first, express these careers
  in it.

## 8. Three separate claims

- **Implemented:** nothing in the game. This packet is design and analysis.
- **Machine-verified:** the document and coverage gates for this change
  (impact record).
- **Outstanding:** every runtime, art, voice, device, child and owner gate for
  the rebuilt games, and the owner's answers in section 6.
