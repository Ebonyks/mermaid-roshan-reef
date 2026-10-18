# Pop Star rebuild: "Roshan's Rainbow Band"

- **Status:** `PROPOSED / CANDIDATE` design for Codex. Written by Claude; no
  game file, image or audio is changed by this document.
- **Owner direction:** the Pop Star must be completely rebuilt; the note-memory
  echo is a usable mechanic inside a poor shell (2026-10-17, to Claude). Earlier
  the same day, to Codex: "This is supposed to be a rhythm game, not just a
  repeating game." Retained earlier owner choices: drums, falling ribbons that
  reach the actual drum, one-bar practice, a visible seat with the tail behind
  the kit, and genuine contact with each of three instruments for the birthday
  contribution (recorded in Codex's `popstar-rhythm-20261017` work, not yet
  published).
- **Shared systems:** the music clock, cue judge, scaffold and section
  controller are specified once in [SHARED_SYSTEMS.md](SHARED_SYSTEMS.md) and
  used here.
- **Evidence for the choices:** [REFERENCES.md](REFERENCES.md).

## 1. The idea

Roshan is the drummer and star of the family band on the Opera Hall stage.
Daddy plays ukulele and Baby Eagle plays bass. The song is the backbone: it
never stops for a mistake, and every part of it asks for one kind of play.

- In the **echo verses** the band plays a one-bar phrase and Roshan answers it
  on her drums in the very next bar. This is the existing note-memory echo,
  now in time with the music: which drum **and** when.
- In the **choruses** ribbons fall onto the drums and the child plays along.
- In the **crowd break** the child leads: she taps the microphone and the
  crowd sings "Hey!" back.
- The **big finish** waits for her last cymbal crash.
- Then the costumed imp drummer arrives for a **drum-off** (`DL-INT-14`).

The child supplies timing and choice of drum; the game makes every hit sound
like part of the song.

**Rhythm is the reward, not the gate.** About a third of 3–4-year-olds could
not lock their drumming to a beat even with a live adult partner (Woodruff
Carr et al. 2014; see REFERENCES). Good timing therefore keeps the band in the
groove, lights the stage and earns the medal, while a child who cannot yet keep
time still finishes by hitting the right drums: after repeated help the band
waits for each hit (section 5). Zero input and random tapping never finish.

## 2. Why this shape

| Pattern | From | How it is used here |
|---|---|---|
| Call bar, then answer bar, at one tempo; a beat pulse that never stops | Patapon (drums beats 1–4, the army sings back on 5–8), PaRappa the Rapper (teacher line, then player line), Space Channel 5 (opponent dances, player copies) | Echo verses: Daddy's band plays the call, Roshan answers in the next bar |
| One drum = one colour = one sound, tuned so any order sounds good | Simon (tones form a major triad), Donkey Konga (a colour per drum), Patapon (named drums) | Three drums, three colours, three pitches from the song's own chord |
| The cue travels to the real target | Taiko no Tatsujin, Donkey Konga, Project DIVA, Cytus | Ribbons land on the actual drum heads (owner's falling-ribbon choice) |
| Watch, practise, then play | Rhythm Heaven DS practice rounds, Rock Band 2 Drum Trainer, Taiko's Auto mode | Rehearsal with Daddy before the song; ghost ribbons demonstrate each call |
| Never react to one miss; offer a way forward after repeated trouble | PaRappa (two bad lines in a row before the rank drops), Rhythm Heaven (skip after three tries), Sayonara Wild Hearts (skip after several failures), Rock Band 2 No Fail | The band repeats a section with more help instead of failing; zero input still never advances |
| The child supplies timing; the game supplies the notes | Wii Music, Incredibox, Toca Band | Every tap sounds in key; credit depends on timing and the right drum |
| A free solo inside a structured song; a finale that needs one last on-beat hit | Rock Band drum fills and Big Rock Ending; Toca Band's star spot | Crowd break and big finish |
| Social partner | Kirschner and Tomasello (2009): young children drum more accurately with a live partner than with a drum machine (see REFERENCES) | Daddy plays the call and nods the beat |

What it deliberately avoids from those games: health or rating meters that can
run out, game-over screens, misleading visuals, "both drums at once" notes,
paid or text-prompted continues, and muting the child's instrument.

## 3. Options considered

| Option | What the child does | For | Against | Verdict |
|---|---|---|---|---|
| **A. Rainbow Band (recommended)** | Echo verses in time, play-along choruses, crowd break, big finish, drum-off | Keeps the owner's usable echo and makes it a rhythm game; uses the owner's drums and ribbons; varied but one skill | Needs a new song arrangement and a drummer animation set | Build |
| B. Falling-ribbon play-along only (Codex's 2026-10-17 draft direction) | Tap each ribbon as it lands, through the whole song | Simplest rhythm game; Codex has started a timing helper for it | Drops the memory echo the owner just called usable; sight-reading only for 60–90 s | Fold in as the chorus sections of A |
| C. Band sandbox (Toca Band, Incredibox style) | Choose band members and parts, then play freely | Creative, no failure | Not a rhythm game, which the owner asked for | Later free-play extra at most |

## 4. The show, beat by beat

Timings assume the concert arrangement keeps the existing cue's 118 BPM in 4/4
(one beat ≈ 0.51 s, one bar ≈ 2.0 s). That is deliberate: 3–5-year-olds tap
at their own tempo of roughly 300–500 ms and rarely follow a slower one
(McAuley et al. 2006; Bobin-Bègue et al. 2014), so the beat should sit in the
400–600 ms band and child cues should never ask for a steady slower pulse.
All values are starting points for device and child tuning (section 11).

| # | Part | Bars | What happens | What the child does | Done when |
|---|---|---|---|---|---|
| 0 | Walk on | – | The Opera Hall stage; Roshan swims to her seat behind the kit; the tail ends behind it | Nothing required | Roshan seated (travel owned by navigation, `DL-INT-02`) |
| 1 | Rehearsal | 3–6 | Daddy says hello with his ukulele. Each drum glows in turn with its sound ("boom", "tap", "ting"); then one 2-note call and answer | Tap each glowing drum once; answer one phrase | Each of the three drums struck once by a genuine contact, and one answer credited |
| 2 | Count-in | 1 | Sticks click four times | Listen | Automatic |
| 3 | Echo verse 1 | 4 (2 calls, 2 answers) | Ghost ribbons play Daddy's call onto the drums; solid ribbons return for her answer | Answer two 2-note phrases | Section target met (SHARED_SYSTEMS §3) |
| 4 | Chorus 1 | 4 | Ribbons fall on beats 1 and 3: big drum, then tom or cymbal | Play along | Section target met |
| 5 | Echo verse 2 | 4 | Three-note calls, using the existing verses `[0,1,2]` and `[2,1,0]` | Answer two 3-note phrases | Section target met |
| 6 | Crowd break | 2 | Roshan lifts the microphone; the crowd waits | Tap the microphone on beats 1 and 3; the crowd sings "Hey!" on 2 and 4 | Two on-beat leads |
| 7 | Chorus 2 | 4 | As chorus 1, the cymbal now on beat 4 | Play along | Section target met |
| 8 | Big finish | 2 | A one-bar drum roll, then the band holds its last chord until she crashes the cymbal | Roll freely; then one cymbal hit | Cymbal hit after the roll; the band waits while she is idle |
| 9 | Drum-off | rounds | The imp drummer enters with his own small kit (section 6) | Answer his phrases | She reaches 3 points first, or he wins and only the contest restarts |
| 10 | Encore and bow | 2 | Confetti, the crowd's light-sticks, the family bows; the imp's defeat line | Tap the star cymbal once for the final crash | Curtain call |

About 45 s of song, 15 s of walk-on and rehearsal and 30 s of drum-off: about
90 s in all when nothing repeats, against 79–127 s of scripted chores today
(DIAGNOSIS §2). A child who repeats sections takes longer, but every repeat is
music, not waiting.

## 5. Rules of play

**Targets.** Three drums are the only targets in the song: a teal tom (left,
"tap"), the big lavender shell bass drum (centre, "boom") and a gold star
cymbal (right, "ting"). Each hit region covers its whole painted drum plus a
margin and is at least 200×200 base pixels (`DL-UI-03`). Positions never
change. The microphone becomes a fourth target only in the crowd break.

**Cues.** Ribbons fall onto the drum they belong to. A ghost ribbon
(translucent, outlined, with a soft ukulele note) belongs to the band's call
and plays its drum by itself. A solid ribbon in the drum's colour is hers. A
cue's arrival at the drum's rim ring is the beat. No cue path may cross
Roshan's face: lanes are laid out so that streamers drop onto each drum from
just above it, and the centre drum's streamer arcs in beside her rather than
through her (`DL-READ-05`; checked geometrically, section 11).

**Scaffold.** Echo answers have three help levels, raised and lowered per
child by the shared scaffold controller:

| Level | During her answer bar |
|---|---|
| 1 Ribbons | Solid ribbons replay the call exactly, so she can play along |
| 2 Glow | No falling ribbons; the right drum glows as each beat of the phrase arrives |
| 3 Memory | Only the steady beat pulse; she plays the phrase from memory |

She starts at level 1, moves up after two clean answers and down after one
missed answer. Choruses always show ribbons. Phrases start at two notes and
never exceed three: at age 4 a sequence of two locations is recalled reliably
and three about half the time (Gathercole et al. 2004). Level 3 is offered only
for two-note phrases.

Falling ribbons matter for a second reason: they turn "keep the beat", which
many 4-year-olds cannot yet do, into "hit the drum when the ribbon touches it",
a visible arrival she can anticipate.

**Judging** (shared cue judge, SHARED_SYSTEMS §2): the first tap inside a cue's
window owns that cue, so sweeping all three drums cannot shop for a hit. A
credited tap needs the right drum, the window, and a calm hand (the anti-mash
damper). Windows lean late because young children rarely tap ahead of the beat
(Bobin-Bègue et al. 2014): credit from 0.20 s before to 0.32 s after the beat;
the brighter "well-timed" star from 0.12 s before to 0.18 s after. Taps are
timed at touch-down. A second trigger on the same drum within 0.12 s is a
finger bounce and is ignored; a long press counts as one tap; a palm or
several fingers count as one touch (Vatavu et al. 2015). Off-beat and
wrong-drum taps still sound like the drum, because a drum should always make a
sound, but they credit nothing and pay no crumbs.

**Feedback within two frames** (`DL-AGE-07`): every tap moves the drum head,
plays its pitched hit and starts Roshan's matching strike. A credited hit adds
a sparkle burst on the drum and a light-stick wave in the crowd; a
well-timed hit adds a brighter star. A wrong drum gets a soft "dum" and the
right drum glows once. Daddy smiles and nods on the beat throughout.

**When a section is not met** the band vamps (repeats the same bars) with one
help level more, as a real band would. Mercy then escalates without ever
playing for her:

| Step | When | What changes |
|---|---|---|
| Help | First vamp | One scaffold level easier; Roshan's voice repeats the instruction |
| Mercy 1 | After two vamps in which she was clearly playing: at least two taps on a cue's own drum, in time or not, that the anti-mash damper allowed | Half the cues; windows widen to 0.30 s early and 0.45 s late |
| Mercy 2, "the band waits" | After two more vamps of the same kind | Timing is no longer judged: each cue waits on its drum, glowing, while the band holds the groove, until she hits that drum. The order still matters. A wrong drum credits nothing and makes the waiting cue rest for one beat before it can be hit (Patapon asks for one clean beat after a slip), and the anti-mash damper still applies, so sweeping the drums stays slower than one deliberate tap |

Mercy 2 is the research-backed floor for a child who cannot yet lock to a beat:
she still finishes by playing the right drums in the right order, and a medal
records that the band had to wait. Zero input keeps the band vamping and never
advances (`DL-AGE-04`); after about 7 s without a touch Roshan re-invites her
with the instruction and a ghost hand on the next drum (Sesame Workshop
2012). Random tapping can reach the mercy steps but advances far more slowly
than intentional play (`DL-AGE-05`).

**Crowd break.** A tap on the microphone within the window on beat 1 or 3
makes the crowd answer "Hey!" on the next beat. Two such leads complete it.
Off-beat taps make Roshan sing a little "la" with no crowd answer.

## 6. Drum-off: the imp contest

This replaces the SING-OFF in
[the imp contest specification §6.12](../codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md#612-pop-star--sing-off-points-inserted-before-encore-stage-only)
while keeping its contract (C1–C16) and owner decisions OD-A to OD-E.

- **Entrance:** the costumed imp (`rival_popstar` family) is not seen before
  the drum-off. He bounces in with a small purple kit at stage right
  (contest §4.1).
- **Skill:** listening and answering, the echo skill.
- **Rounds:** he plays a phrase on his kit (purple ghost ribbons on his
  drums); she answers on hers with the current scaffold level. A credited
  answer (every note credited, or all but one note in a 3-note phrase) is her
  point; a missed answer is his point. First to three wins. Ties go to her.
- **Flub:** when he leads or the score is level at two, his next phrase falls
  apart off the beat; he wobbles (`stagger`, `recover`). Line: "Was that the
  beat? It felt like a beat."
- **His win:** a beat of at most 2 s, then only the drum-off restarts (C7).
  After two failures his phrases slow to half-time (notes every second beat)
  and his target rises by three (C9).
- **Idle:** he does not play while she is idle (C8).
- **Lines** (new, exact): his challenge "Drum-off! Play my beat back to me!";
  her instruction "Listen to the imp, then play it back!"; his defeat line
  "My ears! Okay, okay, you're the drummer."

## 7. The stage, in words

The proscenium of the existing Pop Star stage painting
(`assets/opera/worlds/backdrops/stage_popstar_c*r*.png`) frames the band:
curtains at both sides, the underwater scene and its musical rainbow ribbon
behind. Roshan, in her Pop Star outfit, sits behind her shell drum kit in the
centre of the lower half of the screen, facing the audience; her face, arms
and sticks are above the kit and her rainbow tail curls out behind it to the
right. The kit is three separately owned cards (tom, bass drum, cymbal) so
each can move and light alone; the existing prototype painting
`assets/prototypes/bands/roshan_drums.png` (on `origin/codex/battle-of-bands-20260920`)
is the identity and design reference for the kit and her pose. Daddy, with
his ukulele, stands to her left a step back, and Baby Eagle with his bass to
her right, both smaller than Roshan. A low row of audience silhouettes with
light-sticks runs along the bottom edge, never above the drums
(`DL-LAY-08`). Three soft spotlights fall on the band. The imp's purple kit
appears at stage right only for the drum-off.

## 8. Art, animation and sound to produce

Codex builds every image from these descriptions (CLAUDE.md written-handoff
rule) under the art-quality policy and the animation protocol
(`DL-MOT-12`, `DL-MOT-14` to `DL-MOT-16`).

| Item | Description | Notes |
|---|---|---|
| Roshan drummer set | Whole-frame sprites in the Pop Star outfit, seated at the kit: groove idle (bobbing on the beat), tom strike, bass strike, cymbal strike, listening (hand to ear, smiling), drum roll, big-finish arms up with sticks, microphone lift, bow, wave | Pilot the bass strike first (`DL-MOT-16`). One whole drawing per frame, constant size (owner decisions 2026-10-05 and 2026-10-07) |
| Kit cards | Tom, bass drum and cymbal as separate cards with rest, struck and glowing states; each head visibly dips when struck | From the prototype kit design |
| Daddy and Baby Eagle | Strum and bass-bob loops, a nod, a cheer, a bow | Prototype stills on the bands branch are the references |
| Imp drummer | The `rival_popstar` imp at a small purple kit: strike, taunt, flub wobble, defeated slump, bow | Reuse his existing 13 poses where they fit |
| Ribbons | Three solid ribbon streamers in the drum colours and one ghost style; rim "now" rings; hit sparkle | Painted, not code-drawn shapes (`MA-VIS-008`) |
| Crowd | Silhouette row with light-stick wave states | Sparse foreground |
| Music | A new concert arrangement of "Starlight Singalong" (`opera_popstar`) in the score catalogue: sections intro, verse, chorus, verse, crowd break, chorus, finale, each a whole number of bars and loopable for vamps | Rendered by `tools/build_area_music.py`; backing without the child's drum part |
| Hits and calls | One-shot drum hits for the three drums, a roll, ghost ukulele call notes, crowd "Hey!", stick clicks | Pitched to the arrangement's chords so any order sounds right |
| Voice | Exact new Roshan cues: "Tap each drum when it glows!", "Listen to the band, then play it back!", "Play along with the ribbons!", "Now you lead! Tap the microphone!", "Big finish! Crash the star cymbal!" | Existing synthetic Roshan workflow; protected family recordings untouched (`DL-SND-05`) |

## 9. Routes, saves and the story

- **Free play:** the Opera Hall's Pop Star door (`DL-INT-12`). Return to the
  Opera Hall as today.
- **Saves:** keep the existing career star bit and medal keys. Add, with
  defaults, a section checkpoint (last completed section index) and the
  child's scaffold levels (`DL-SAVE-01`). Re-entry resumes at the start of the
  last unfinished section with a fresh count-in.
- **Chapter 2 / Day Two:** the same engine plays the story's drum part. The
  candidate Day Two draft (on `origin/ccr-ba906acd-1aepcb`) asks for "six
  forgiving taps on the glowing drum" over the Iko Iko opening and twelve
  across the battle of the bands. With this engine those become a chart on
  the Iko Iko recording, kept unedited and untimed (`DL-CIN-16` does not
  apply; the song's own rules do), if and when the owner clears its game-use
  rights (Day Two decision 15). Story runs keep no imp (contest C13).

## 10. What retires

SOUND CHECK (hold), DANCE (choice), RHYTHM (untimed echo) and ENCORE (circle)
as Pop Star activities; the practice-then-stage duplication for Pop Star in
`OperaPerformancePlan`; the stage-long rival race and his mirrored widget for
Pop Star; the 500×376 action panel; code-drawn echo stars and the medal
overlay digits. The echo's verse content (`[0,2]`, `[0,1,2]`, `[2,1,0]`),
harmless replay and checkpoint ideas carry forward.

## 11. Acceptance tests

Machine (a new trusted probe, plus updates to `probe_opera_2d` and
`probe_voice`):

1. Zero input for 120 s from the first section: no section completes, no
   star, the band keeps vamping, a re-invitation plays.
2. Intentional play by a scripted child (each cue hit within ±0.15 s on the
   right drum) completes every section without a vamp.
3. A 5 Hz masher on all three drums, and a 5 Hz masher on any single drum,
   earn at most 10% of cues and complete no section in 120 s before mercy;
   forced into Mercy 2, the masher still completes a section more slowly than
   a scripted child who taps the glowing drum once per cue.
3a. A scripted child who always hits the right drum 0.6 s late (never inside
   a window) reaches Mercy 2 after four vamps and then completes every section:
   timing never blocks an engaged child.
4. Wrong drum inside the window consumes the cue without credit; the
   correct drum glows.
5. Holding one finger down produces exactly one hit; a second finger cannot
   strike while the first owns its route (`DL-UI-04`).
6. Pause, focus loss, Back and close cancel held input, stop the music and
   leave no stale credit; resume restarts the section with a count-in
   (`DL-UI-05`, `DL-SAVE-03`).
7. Chart validation: every cue on the beat grid of its section; spacing at
   least twice the window; no cue in the first two beats after a count-in;
   ribbon paths never intersect Roshan's face rectangle.
8. Clock: the judged time never decreases within an epoch; a new epoch
   after resume.
9. Drum-off: his win after a scripted loss restarts only the drum-off within
   2 s; after two losses his phrases are half-time and his target is three
   higher; zero input decides nothing.
10. Save and re-entry at each section boundary; earned star and medal kept;
    no duplicate award.
11. Overdraw: `tools/measure_overdraw.py` states for rehearsal, chorus,
    crowd break and drum-off pass OD1–OD6 (gold-star C7).

Human: target-phone latency and touch (does the beat feel right?), an
observed child session (does she understand listen-then-play, and does she
want to play again?), and the owner's verdict. Machine success grants none of
these.

## 12. The owner's choices (2026-10-18)

The owner chose the recommended option for each question (README §6):

1. **Rhythmic echo plus play-along**, not play-along only
   (`ODR-POPSTAR-CORE-20261018`).
2. **A new concert arrangement of the existing song first**, with Iko Iko for
   the Day Two story once its rights are confirmed
   (`ODR-POPSTAR-SONG-20261018`).
3. **Daddy and Baby Eagle** as the free-play band
   (`ODR-POPSTAR-BAND-20261018`).
