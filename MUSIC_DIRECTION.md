# MUSIC_DIRECTION.md — Reef of Light soundtrack direction

**OWNER DECISION 2026-08-16: Condard's beats are the primary musical
inspiration for this game.** Beats only — the rap layer is explicitly out of
scope (owner). This document is the binding music direction; it supersedes the
ad-hoc "whatever CC0 track fits" approach that produced the current set.

Status: direction only. **No audio files change in this commit.** The existing
17 tracks keep playing exactly as they do today until they are replaced
track-by-track under the migration plan at the end of this doc.

---

## 1. The reference

**Condard** — Albuquerque, NM. Chiptune hip-hop. Album *Harder not Smarter*
(2026-05-17): New Saga / Ode to Gunpei / Caught in 4k / Harder not Smarter /
Violence is the Question / Dogs Down. Bandcamp tags: electronic, hip hop,
chiptune, gameboy. The defining production constraint, stated by the artist:

> All instrumentation has been made with a single Game Boy running
> Little Sound DJ.

That constraint — not the artist's catalogue — is what we inherit.

### What we take
- **The instrument.** One Game Boy's worth of voices, and no more.
- **The groove.** Hip-hop pulse: a real backbeat, swung sixteenths, head-nod
  tempos, a bassline that walks instead of pads.
- **The ethic.** *"There is no secret formula to replace love and labor."*
  Every track in this game is hand-built from primitives, deterministically,
  by a script or a tracker we control. This is also the practical rule — see
  §5.

### What we do NOT take
- **No rap, no vocals, no lyrics** (owner). Instrumental beds only. The only
  voices in this game are the recorded family voices, which are sacred and
  which the music must always duck under.
- **No lyrical or thematic content.** The source album's subject matter is
  adult and political. It has no bearing on a 4-year-old's reef.
- **No sampling, no stems, no specific-track reproduction.** We do not lift or
  reprocess Condard audio, and we do not set out to recreate a particular
  Condard track closely enough that it stands in for that track. The genre,
  the groove and the hardware constraint are the reference — not any one
  recording.
- **No aggression.** Distorted noise slams, harsh transients, sub-bass drops
  and anything that reads as threat are out. See §4.

### On AI generation — OWNER NOTE 2026-08-16

AI is a permitted authoring channel here, and its use is deliberate rather
than incidental. In the owner's framing: the source album takes a broad-handed
oppositional stance toward AI, and making this soundtrack *with* AI, in that
style, is the artistic statement — a contrasting vision from a future that
understands the place and time of the tool rather than refusing it outright.
Working in an established style has never been plagiarism, and nothing here
passes itself off as Condard's work or competes with it: this is the score to
a private game made for one child.

The line that does hold is §1's — no sampling, no stems, no standing in for a
specific track. Beyond that, use whichever channel in §3 produces the best
result in her hands.

---

## 2. Why this fits the game

This is not a style graft — the constraint happens to solve four real problems
this project already has:

1. **Phone speaker.** The target device is a 3–4-year-old Android phone. It
   reproduces almost nothing below ~400 Hz. Orchestral and piano beds lose
   their bottom half and turn to mush; pulse waves in the 500–2000 Hz band
   survive a tiny speaker intact. Chiptune is the format that *already sounds
   like itself* on the hardware we ship to.
2. **Size.** Game Boy-palette tracks synthesize to short, seamless, low-bitrate
   OGG loops. The APK stays small.
3. **Toy playset art direction.** The world is oversized, rounded, pastel,
   graphic — a plastic toy. Four-channel chiptune is the toy-sounding music.
   Orchestral JRPG scoring is aiming at a different game than the one we built.
4. **Short sessions.** A 4-bar chiptune loop is legible in three seconds. A
   90-second orchestral arrangement with a slow intro is not, when the session
   is four minutes long.

Also, unavoidably: *Ode to Gunpei* is a nod to Gunpei Yokoi, who made the Game
Boy. That is the register this soundtrack lives in — affectionate, handmade,
built out of deliberately tiny parts.

---

## 3. The palette (hard constraint)

Every new music track is written for **four voices and no more**, matching the
Game Boy APU that LSDJ drives:

| Voice | What it is | Use it for |
|---|---|---|
| **PU1** | Pulse, duty 12.5 / 25 / 50 / 75%, with pitch sweep | Lead melody, the hook |
| **PU2** | Pulse, same duties, no sweep | Counter-melody, arpeggio chords, stabs |
| **WAV** | 4-bit programmable wavetable | Bass — the walking line; occasionally soft pad |
| **NOI** | LFSR noise | The kit: kick body, snare, hats |

Rules:
- **Four channels, monophonic each.** Chords are arpeggios, not stacks. If a
  part needs a fifth voice, cut a part.
- **No sampled instruments** in music. No orchestral hits, no piano, no real
  drums, no guitar.
- **Bass lives on WAV**, and its fundamental sits **at or above ~120 Hz** so
  the phone speaker reproduces something rather than flapping.
- **The hook sits 500–2000 Hz** on PU1. That band is what a child actually
  hears through a phone held at arm's length.
- Volume envelopes and vibrato are the expression tools. No filters, no
  reverb tails baked into the music bed — the room tone is the ambience layer's
  job (`assets/audio/ambience_*.ogg`).

**Three authoring channels**, all legitimate. Pick by what gets the best track,
not by principle:

1. **A real LSDJ (or equivalent tracker) session**, recorded and rendered by
   the owner. Gives the genuine article by definition.
2. **Deterministic project synthesis**, following `tools/gen_combat_sfx.py`
   conventions: pure-stdlib, seeded RNG, 44.1 kHz mono, explicit fades, one
   script that regenerates the exact same bytes.
3. **AI generation** (see the owner note in §1). Two sub-routes, and the second
   is usually the better one:
   - *Direct audio generation.* Fastest, but be aware that most music models
     produce "chiptune-flavoured" synth — chip timbres over a modern
     multi-track arrangement — rather than something a Game Boy could actually
     play. Audition against §3's four-voice rule; if you can hear five things
     at once or a bass note under 120 Hz, it missed the constraint that makes
     this style sound like itself.
   - *AI-composed, chip-rendered.* Have the model write the note data —
     pattern, groove, swing, bassline, hook — and render it through a true
     four-channel Game Boy synth (route 2's script, extended into
     `tools/gen_music.py`). This keeps the hardware constraint exact while the
     composition comes from the model, and it is reproducible from source: the
     repo holds the pattern data and the renderer, not just an opaque WAV.
     It is also the most literal form of the owner's statement — AI writing
     inside the same four-channel box the reference venerates.

---

## 4. The child rules — these outrank the genre

Where the genre and the 4-year-old disagree, the 4-year-old wins.

- **No fail-signalling music, ever.** There are no fail states in this game and
  the score must never invent one. No minor-key "you lost" sting, no descending
  sad trombone, no music that stops dead on a miss. A miss gets the same warm
  loop it had a second earlier.
- **No startle.** Nothing enters at full volume. Every loop point is seamless
  and every new track fades in at the engine's `-8 dB` base. Transient peaks
  stay soft — the combat SFX pack's `peak=0.28` ceiling is the reference for
  how hard anything is allowed to hit.
- **No noise-channel abuse.** The NOI kit is brushes and taps: short, filtered,
  quiet. A trap-style rattling hi-hat roll or a distorted 808 is a startle
  device on a phone speaker held near a small face. Out.
- **Tempo ceiling 112 BPM.** Above that the music starts pushing, and this game
  never pushes her.
- **Music is always the floor, never the event.** It sits under the family
  voices (`-6 dB` duck, already implemented) and under every objective cue. If
  a track ever competes with a spoken line for attention, the track is wrong.
- **Loop, don't arrange.** 4 or 8 bars, seamless, no long intro, no build, no
  drop. She may hear the reef loop for twenty minutes; it has to stay pleasant
  at minute twenty, which means gentle variation, not a structure with a
  destination.

---

## 5. Per-zone specification

Tempos are the target for **new** tracks. All are ≤112 BPM per §4, and all use
a swung sixteenth feel (roughly 56–60% swing) unless noted — that swing is the
single most Condard-ish thing in the whole spec, and it is what separates this
from generic chiptune.

| Track | Where it plays | BPM | Feel |
|---|---|---|---|
| `world` | Reef promenade (the main world; 6 call sites) | 84 | Half-time boom-bap. Walking WAV bass, brushed noise kit, lazy PU1 hook. The signature track — everything else is heard relative to this. |
| `world_night` | Reef at night (auto-swap in `_play_music`) | 72 | Same bassline, halved kit, PU1 replaced by long soft WAV tones. Lullaby version of the day theme, deliberately recognisable as the same tune. |
| `level2` | Sky Lagoon; also the opera-race restore track | 90 | Lighter, airier. Duty-12.5% PU1 sparkle, kit up an octave, more space. |
| `hall` | Castle hall | 78 | Slow, plush, indoor. WAV bass and PU2 arpeggios carry it; kit reduced to soft taps. |
| `home` | Home / castle interior | 76 | The quietest bed in the game. Nearly beatless — arpeggio and bass only. |
| `race` | Kart / slide race (4 call sites) | 108 | The fastest thing we ship, and still under the ceiling. Driving WAV bass, straighter (less swung) kit, PU1+PU2 trading the hook. |
| `fetch`, `dolls`, `seek`, `melody`, `shop`, `treasure` | Minigame arenas via `_play_music(kind)` | 92 | One shared groove skeleton, one distinct PU1 hook each, so the minigames sound like siblings. Shortest loops in the game (4 bars). |
| `castle_open` | One-shot stinger (`loop=false`) | — | ≤4 bars, rising, resolves into `hall`. |
| `finale` | One-shot celebration (`loop=false`) | — | ≤8 bars. The one place all four channels go full and bright at once. Still no startle transient. |

Two notes on the existing files:
- `banjo.ogg` lives in `assets/audio/music/` but is **not music** — it is the
  beans banjo SFX, played through the dedicated `beans_sfx` player so it works
  with music turned off (`main.gd:633`). This direction does not apply to it.
- `melody`'s in-game chime ladder (`m.chime.pitch_scale = 0.9 + caught * 0.07`,
  `games/melody.gd:540`) is a gameplay cue, not a music voice, and is out of
  scope here.

---

## 6. Mix and engine contract

These are already implemented in `scripts/audio_director.gd` — new tracks must
be authored to sit correctly inside them, not to require changes to them:

- Bus **`Music`** (`default_bus_layout.tres`). Base level **`-8 dB`**, muted at
  `-60 dB` when `music_on` is false.
- **Voice duck:** music lerps to **`-14 dB`** whenever any voice-pool player is
  active (`_tick_ambience_duck`). Master a track so it is still legible ducked —
  if the hook disappears at -14 dB it was mixed too quiet relative to its kit.
- **Ambience bed** runs underneath at `-10 dB` (`-16 dB` ducked) and is a
  separate layer; do not bake room tone or water noise into a music track.
- **Format** (CLAUDE.md hard rule): OGG, **≥64 kbps**, **loop-tagged**. Looping
  tracks are loaded with `loop = true`; the two stingers pass `loop=false`.
  Target **-18 LUFS** to match the existing bed.
- Mono is acceptable and preferred — the target device is a single small
  speaker, and mono halves the file.

## 7. Licensing

Every new track gets its line in `ASSET_LICENSES.md` **in the same commit that
adds it** (CLAUDE.md hard rule). State the channel honestly, because the
provenance differs by route:

- **Tracker session** — "project original", name the session/instrument.
- **Deterministic synthesis** — "project original", name the generating script.
  Reproducible from source.
- **AI generation** — name the model/service and the generation ID, the same
  way the Codex and OpenAI concept-art entries already do further down that
  file. For the AI-composed/chip-rendered route, also name the renderer script
  and commit the pattern data, so the track rebuilds from the repo.

No Condard recording, stem, or sample ever enters this repository.

---

## 8. Migration plan (nothing changes until each step is taken deliberately)

The current set is a mix of Juhani Junkala's CC0 JRPG packs
(`world`, `world_night`, `level2`, `hall`, `home`) and project-synthesized
stingers (everything else). The Junkala tracks are the direct conflict with
this direction: they are orchestral/JRPG-scored, arranged rather than looped,
and bottom-heavy for a phone speaker. They are also perfectly good music that
currently ships and works, so:

1. **`world` first.** It is the track she hears most and the one that defines
   the rest. Build it, A/B it on the actual phone, and only then continue.
2. `world_night` next, derived from `world` so the pair matches.
3. The minigame set (`fetch`/`dolls`/`seek`/`melody`/`shop`/`treasure`) as one
   batch — they share a skeleton.
4. `race`, then `level2`, then `hall`/`home`.
5. Stingers (`castle_open`, `finale`) last.

Each step is one commit, replacing one track (or one batch), with the probe
suite green and the ASSET_LICENSES.md line included. A replaced track keeps its
exact filename, so no code changes and no save-compatibility risk. Keep the old
file in `attic/` until the new one has been play-tested on the phone — if a
track is worse in the child's hands, revert it; the direction serves her, not
the other way round.
