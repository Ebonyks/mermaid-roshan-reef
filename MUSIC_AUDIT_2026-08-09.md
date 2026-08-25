# Mermaid Roshan: Reef of Light — Music Audit and Composition Bible

- **Audit date:** 2026-08-09
- **Status:** Implemented; automated composition, render, loop, and routing validation complete; human listening and Lenovo Tab M11 mix review remain
- **Scope:** 15 legacy files already in `assets/audio/music/`, 42 new area cues, their transition ownership, and the musical language that joins them

## 1. Purpose and audience

This is the human-readable source of truth for how music should work in *Mermaid Roshan: Reef of Light*. It is for the owner, composers, audio implementers, reviewers, and future maintainers who need to understand both the feeling of the score and the reasons behind the file-and-code decisions.

The central design decision is that every meaningful place or self-contained activity should sound like itself. In this audit, **quiet** means either literal silence or an area that only inherits an unrelated parent cue. A room can therefore be technically audible and still be musically unauthored.

The result is not 42 unrelated genre exercises. It is one child-friendly storybook score in which each room changes the pace, meter, articulation, and a few featured colors. The Royal Kitchen may waltz, the Detective may tiptoe, and the Farmer may play a porch reel, but they remain members of the same Mermaid Roshan musical family.

This document does not replace the legal ledger or machine-readable score:

- `ASSET_LICENSES.md` remains authoritative for licensing and attribution.
- `assets_src/audio/music/area_music_scores.json` is authoritative for the 42 new declarative compositions.
- `assets/audio/music/area_music_manifest.json` (schema `reef.area-music-manifest.v1`) is authoritative for rendered hashes, durations, codecs, loudness, peaks, and loop measurements; all 42 cue records are complete and validated.

## 2. Status vocabulary and scope decision

| Status | Meaning |
|---|---|
| **RETAINED** | An existing file remains the intended cue for its current role. It is not a placeholder targeted by this pass. |
| **NEW — RENDERED** | The cue has a unique score, production OGG, loop import, routing owner, and hash-backed measurement record. |
| **INTENTIONAL REUSE** | An existing minigame cue is deliberately reused because the interaction is the same musical activity, not because an area was forgotten. |
| **SFX, not score** | The file lives in the legacy music directory but is routed and designed as a sound effect. |

The new-cue count is exactly **42**:

- 12 Castle side-room cues. The Main Hall keeps the existing `hall` cue.
- 1 Opera lobby cue, 13 career cues, and 3 friendly boss cues.
- 9 world, dungeon, combat, tutorial, and Stuffie cues.
- 4 picture-game cues.

For coverage, an **area** is a soundtrack scene, not every camera cell or prop. A discrete illustrated Castle room, Opera act, full-screen picture game, world, dungeon, or combat state owns a cue. A continuous ten-room dungeon keeps one developing suite across its chambers so exploration is coherent and the loop is not restarted at every doorway. Likewise, contiguous subregions inside one world keep that world’s cue unless gameplay enters a separately owned state.

## 3. Audit findings and decisions

### 3.1 The legacy folder contains 15 OGG files, but only 14 are score

`assets/audio/music/banjo.ogg` is the looping magic-beans toot. It is routed through the SFX bus and must not be counted as background music merely because of its path. The other 14 files are score loops or one-shot score stingers.

Five retained location cues are CC0 works by Juhani Junkala. Their exact mapping was established when they entered the project in commit `fe44318b`:

- `world` — *Tropical Island*
- `world_night` — *Prairie Nights*
- `level2` — *Sunshine Coast*
- `hall` — *Sand Castles*
- `home` — *A Place I Call Home*

The remaining legacy cues are project-original synthesis. Their finished binaries and license classification exist, but no reconstructable score/render source was found during this audit. They are retained as legacy masters; future provenance must not pretend they can be deterministically regenerated.

### 3.2 `ASSET_AUDIT.md` is stale for music

Its row describing “11 loops” as wholly project-synthesized predates the five Juhani replacements and the current 15-file directory. It is historical context, not current source truth. `ASSET_LICENSES.md`, the actual files, commit `fe44318b`, and this audit supersede that row for music inventory.

### 3.3 “Inherited-stale” music hid missing area authorship

Before this pass, many transitions requested no valid local cue. The previously audible stream continued, so the game rarely went completely silent, but a Castle room, Opera act, or remote world could sound like whichever area happened to run before it.

There was also a state bug: a missing cue request could update `cur_track` before the file-existence check. The old stream remained audible while the state claimed the missing slug was active. A later nested activity then tried to restore that nonexistent slug. The current decision is:

- Verify the OGG exists before changing `cur_track`.
- If it is missing, leave both the audible stream and the restorable state untouched.
- Once an accepted unique cue exists, transition owners explicitly save and restore it.

This graceful fallback protects play during development, but a missing file is still a release failure for any of the 42 required slugs.

### 3.4 Unique area music and deliberate minigame reuse are different things

Room and world identity now receives a unique cue. A few short activities continue to reuse established music because the cue already describes the activity and because the activity owns a clean return path.

| Existing cue | Intentional reuse |
|---|---|
| `fetch` | The snowy 3D slide race. Its bouncing run is musically the same quick chase gesture. |
| `melody` | Fairy play and Dance Engine’s “Rainbow Stage.” Both are explicitly note-and-sparkle music activities. |
| `race` | Kart races, legacy brawl and Dust Boss action, the Opera in-act kart segment, and Dance Engine’s “Rainbow Race.” |
| `finale` | Dance Engine’s “Castle Celebration,” in addition to the retained story-finale stinger. |

These reuses must never become a blanket fallback for a new room or career. In particular, `opera_racer` is the Opera act’s identity; the existing `race` cue is only the nested kart engine’s temporary activity cue and returns to `opera_racer` afterward.

### 3.5 Hard cuts are the current transition language

The runtime has one Music player and no crossfade system. A direct cue change is useful feedback for a four-year-old: the new musical identity arrives with the new screen. This pass keeps that simple ownership model. Crossfades, stems, and parallel music players are not added without a separate device-performance and state-restoration design.

## 4. Legacy inventory and measured baseline

All 15 files are Ogg Vorbis. Duration, stream metadata, integrated loudness, and true peak were measured on 2026-08-09 with `ffprobe` and FFmpeg `ebur128=peak=true`. “kbps” below is the nominal stream metadata value, not a file-size-derived average. Every legacy `.ogg.import` currently says `loop=false`, `loop_offset=0`, `bpm=0`, and `beat_count=0`; continuous legacy tracks are looped in runtime code. This is grandfathered behavior, not the standard for new assets.

| File | Current role and source | Duration | Hz / channels / nominal kbps | LUFS-I / dBTP | Loop contract | Decision |
|---|---|---:|---|---|---|---|
| `banjo.ogg` | Magic-beans toot; project synthesis | 15.000 s | 44,100 / mono / 96 | -17.9 / -5.7 | Runtime loop on SFX bus | **SFX, not score** |
| `castle_open.ogg` | Castle-door reveal; project synthesis | 6.200 s | 44,100 / mono / 96 | -18.1 / -4.6 | One-shot; caller restores prior cue | **RETAINED** |
| `dolls.ogg` | Dolls minigame; project synthesis | 12.857 s | 22,050 / mono / 50 | -18.0 / -7.8 | Runtime loop | **RETAINED** |
| `fetch.ogg` | Fetch and slide activity; project synthesis | 8.889 s | 22,050 / mono / 50 | -17.8 / -9.1 | Runtime loop | **RETAINED / INTENTIONAL REUSE** |
| `finale.ogg` | Story celebration and Dance Engine selection; project synthesis | 42.000 s | 44,100 / mono / 96 | -17.9 / -3.1 | One-shot in story; looped by Dance Engine | **RETAINED / INTENTIONAL REUSE** |
| `hall.ogg` | Pearl Castle Main Hall; Juhani Junkala, *Sand Castles*, CC0 | 71.111 s | 44,100 / stereo / 160 | -18.1 / -1.6 | Runtime loop | **RETAINED** |
| `home.ogg` | Castle sleep/tuck-in; Juhani Junkala, *A Place I Call Home*, CC0 | 46.452 s | 44,100 / stereo / 160 | -17.8 / -4.0 | Runtime loop for sleep span | **RETAINED** |
| `level2.ogg` | Sky Lagoon; Juhani Junkala, *Sunshine Coast*, CC0 | 112.340 s | 44,100 / stereo / 160 | -17.9 / -6.3 | Runtime loop | **RETAINED** |
| `melody.ogg` | Melody, Fairy, and Dance Engine; project synthesis | 8.571 s | 22,050 / mono / 50 | -17.9 / -8.8 | Runtime loop | **RETAINED / INTENTIONAL REUSE** |
| `race.ogg` | Kart/action activity and Dance Engine; project synthesis | 10.000 s | 22,050 / mono / 50 | -17.8 / -7.8 | Runtime loop | **RETAINED / INTENTIONAL REUSE** |
| `seek.ogg` | Seek minigame; project synthesis | 7.869 s | 22,050 / mono / 50 | -17.9 / -8.2 | Runtime loop | **RETAINED** |
| `shop.ogg` | Pearl Shop; project synthesis | 18.143 s | 44,100 / mono / 96 | -17.9 / -1.4 | Runtime loop | **RETAINED** |
| `treasure.ogg` | Treasure minigame; project synthesis | 32.000 s | 44,100 / mono / 96 | -17.8 / -2.9 | Runtime loop | **RETAINED** |
| `world.ogg` | Day reef; Juhani Junkala, *Tropical Island*, CC0 | 53.333 s | 44,100 / stereo / 160 | -18.0 / -3.8 | Runtime loop | **RETAINED** |
| `world_night.ogg` | Night reef; Juhani Junkala, *Prairie Nights*, CC0 | 92.903 s | 44,100 / stereo / 160 | -18.0 / -5.2 | Runtime loop selected by `world` at night | **RETAINED** |

The five 22.05 kHz / nominal 50 kbps minigame files — `dolls.ogg`,
`fetch.ogg`, `melody.ogg`, `race.ogg`, and `seek.ogg` — are a legacy
exception. They should not be destructively recompressed merely to change a
metadata number, but no new cue may use that exception. Each remains a
listening-led replacement candidate in the all-audio ledger. New area music
uses the stricter 48 kHz stereo / managed 96 kbps delivery profile in Section
6, which also clears the project-wide minimum of 64 kbps.

## 5. Shared musical language

### 5.1 Storybook acoustic chamber-pop

The score’s common language is **storybook acoustic chamber-pop**: a small, warm ensemble playing clear tunes and gentle repeated patterns, with occasional toy-like or soft electronic color. It should feel handmade and singable, not like a large cinematic library, a genre parody, or a wall of synthetic sound.

The default ensemble is one readable lead, one harmony or ostinato voice, one rounded bass, one sparse accent color, and only as much percussion as the action needs. Flute, clarinet, piano, harp, pizzicato strings, warm strings, marimba, toy piano, music box, bell, ukulele, banjo-like plucks, fiddle-like lines, warm toy brass, and soft synth are members of the same palette. The instrument names in the declarative score describe musical roles and synthesized timbre families; they do not authorize downloaded samples or soundfonts.

Genre color is seasoning:

- Major is the default home language.
- Lydian supplies weightless wonder without abandoning tonality.
- Mixolydian supplies playful folk motion and confident action.
- Dorian supplies mystery, ice, and tiptoe curiosity without fear.
- Minor is reserved for warm stakes and friendly bosses, with consonant turns, major inflections, and reassuring resolutions.
- Waltz and 6/8 rock gently; 4/4 clarifies touch timing; 2/4 gives Craft Room a compact handwork pulse.

The family singer-songwriter/ukulele direction recorded in `gen2/GEN2_REBUILD_WORKORDER.md` remains part of the project’s heritage. It appears literally where natural, such as the Garden, and more broadly through human-sized phrases, open voicings, and a sense that the tune could be hummed at home.

### 5.2 The Roshan motif

Every new cue shares the six-note Roshan contour declared in `area_music_scores.json`:

`scale degrees [0, 2, 4, 5, 4, 2]` with rhythm units `[1, 1, 2, 1, 1, 2]`.

It is a rise, a brave crest, and a gentle return. Each cue states it once and restates it through the room’s own physical verb: a curtain call, page turn, paint dab, bubble bounce, porch reel, countdown, rocking cradle, snow echo, or another named treatment. It may change key, mode, octave, articulation, instrumentation, and rhythmic scale. It must remain recognizable as a contour without sounding pasted into every loop at the same pitch. The second half of a loop reharmonizes or develops the idea; it does not merely duplicate the opening phrase.

### 5.3 The sparkle cadence

The shared six-note Roshan contour is also the score’s binding **sparkle-return cadence**: rise, brave crest, gentle return. A bell, chime, celesta, music box, or bright pluck may color its arrival where the room calls for a visible glint, but the timbre is optional and the contour is the identity. Bells and chimes are punctuation, not continuous glitter noise.

This is deliberately separate from the runtime reward fanfare, which is already a three-attack rising `chime.ogg` gesture at pitch scales `0.90`, `1.12`, and `1.35` and approximately `0`, `160`, and `340` milliseconds. Do not paste that UI event into every music loop. A sparse score glint may prepare or answer a safe reveal, but a real reward fanfare must still read as a distinct event.

### 5.4 Preschool pacing and emotional safety

- Put the area’s identity in the first two bars. There is no long ambient fade-in before the child hears where she is.
- Keep phrases predictable enough to support one-finger timing and repetition, while leaving small rests for touch sounds, laughter, and voice instructions.
- Action means buoyancy, a clearer pulse, and brighter articulation—not menace, alarms, sirens, harsh cymbals, distorted impacts, or a fail timer.
- Mystery means curiosity and looking around, never dread.
- Boss music describes a large friendly stage event. Every shadow, stomp, or minor turn resolves toward play and belonging.
- There are no lyrics or vocal-like foreground parts. Family voices are irreplaceable and always win the midrange.

## 6. Mix, voice, loop, and mobile rules

### Voice and bus hierarchy

- Music plays on the Music bus at a runtime base of `-8 dB`.
- While any family voice in the voice pool is speaking, music ducks another `-6 dB` toward `-14 dB`.
- Shared ambience sits at `-10 dB` and ducks to `-16 dB` under voices.
- Compositions must still leave spectral and rhythmic room for speech before ducking. Avoid constant lead activity in the speech band, especially in instruction-heavy Opera acts.
- Pop Star must use actual call-and-answer holes. Its backing should not fight the direction chimes or spoken prompts during the child’s answer window.

### Loudness and dynamics

- New output target: `-18.0 LUFS-I`, with an acceptance window of `-18.5` to `-17.5 LUFS-I`.
- True peak for every new render: at or below `-3.0 dBTP`.
- Preserve small-scale musical dynamics. Do not flatten the cues into constant loudness or let ducking pump audibly.
- Compare every new cue against `hall`, `world`, `level2`, and at least one retained minigame cue at the in-game `-8 dB` setting, not at arbitrary desktop playback gain.

### Codec and loop delivery

- Production format is Ogg Vorbis, 48,000 Hz stereo, using managed 96 kbps as the target with 80 kbps minimum and 128 kbps maximum. This remains above the repository’s binding 64 kbps floor.
- Each production loop is 24–40 seconds and an exact integer number of bars. The score catalog enforces that range before rendering.
- The catalog’s `bpm_unit` is `notated_denominator`: BPM counts quarter-note pulses in 2/4, 3/4, and 4/4, and eighth-note pulses in 6/8. `beat_count` and `bar_beats` use that same pulse, so duration and Godot’s musical loop boundary agree exactly.
- Every one of the 42 new area cues is a seamless musical loop. Vorbis comments must include `LOOPSTART=0`, `LOOPEND` and `LOOPLENGTH` equal to the exact sample count, plus `BPM`, `METER`, and `CUE_ID`.
- Godot `.ogg.import` metadata must set `loop=true` and record the cue’s BPM and beat count. Runtime loop assignment remains a defensive fallback, not the only loop declaration.
- Start and end on whole-bar musical boundaries. Reverb and delay must wrap or resolve without a click, level step, doubled transient, or conspicuous empty gap.
- Do not hide a bad seam under a long tail or silence. Validate at least two consecutive wraps by measurement and by listening.
- `castle_open` and `finale` remain explicit legacy one-shots; they are not models for new area-loop metadata.

### Mobile constraints

- Use one rendered music stream at a time. Do not add runtime stems, sample players, convolution, or live synthesis to achieve the arrangement.
- Keep the required stereo render legible on a small mono phone speaker: rounded bass without sub-only information, centered melody, restrained high bells, and no essential identity encoded only in stereo width.
- A cue must start without a perceptible transition stall on the target Android device and loop for several minutes without under-run or memory growth.
- Music-off remains absolute. Ducking or a later transition must never pull muted music back above `-60 dB`.

## 7. New composition briefs

All 42 rows below are **NEW — RENDERED**. Tempo, meter, bars, mode, instrumentation, and narrative intent come from `assets_src/audio/music/area_music_scores.json`; measured delivery evidence comes from `assets/audio/music/area_music_manifest.json` and is summarized in Section 9.3.

### 7.1 Pearl Castle side rooms — 12 cues

The Main Hall is deliberately absent from this table because it retains `hall.ogg` (*Sand Castles*). Moving through `show_room()` changes the authoritative room state; the Level 2 soundtrack owner observes the live Castle stage and selects the destination cue, including returning to `hall` for `main_hall`.

| Slug and title | Authored form | Palette | Individual composition brief |
|---|---|---|---|
| `castle_opera_hall` — *Pearl Curtain Promenade* | 8 bars · 92 BPM · 6/8 · D Lydian | Clarinet, harp, warm bass, bell; brushes | A poised theatre promenade. Harp footsteps and clarinet curtain calls create anticipation without rushing the child toward a door. |
| `castle_kitchen` — *Copper Kettle Waltz* | 12 bars · 90 BPM · 3/4 · C major | Clarinet, toy piano, warm bass, pizzicato; brushes | A homey little classical waltz. Toy-piano flourishes and pizzicato stirring motions leave generous room for cooking voices. |
| `castle_library` — *Lanterns Between Pages* | 8 bars · 76 BPM · 4/4 · F major | Flute, harp, warm bass, music box; no percussion | Flute phrases open like picture-book pages over soft harp arpeggios. Long rests and sustained warmth keep it curious rather than sleepy. |
| `castle_playroom` — *Stuffie Parade* | 12 bars · 108 BPM · 4/4 · B-flat major | Marimba, warm brass, warm bass, toy piano; soft march | A soft toy march with marimba feet and rounded brass answers. It invites make-believe marching but never sounds military. |
| `castle_craft_room` — *Paintbox Polka* | 24 bars · 112 BPM · 2/4 · G Mixolydian | Pizzicato, accordion-like harmony, warm bass, bell; shaker | A compact handwork polka in which bright chord squeezes and plucked dots trade colors. Bell accents land like occasional stickers, not constant sparkle noise. |
| `castle_mermaid_pool` — *Moonpool Ripples* | 8 bars · 82 BPM · 6/8 · A Lydian | Flute, harp, warm pad, chime; no percussion | A slow aquatic 6/8 of flute bubbles, harp ripples, and glassy support. Phrases rise to the surface and settle before repeating. |
| `castle_bubble_bath` — *Bubble Duck Bounce* | 12 bars · 104 BPM · 4/4 · C major | Marimba, pizzicato, warm bass, bell; bubble percussion | Rounded marimba bubbles pop over buoyant plucks and a tiny bath-toy bass line. Syncopation suggests splashing without becoming busy. |
| `castle_dining_room` — *Supper Table Grace* | 12 bars · 84 BPM · 3/4 · F major | Clarinet, piano, warm bass, warm strings; no percussion | A warm chamber waltz passes one polite melody around the table. Stable cadences make every arrival feel like coming home. |
| `castle_royal_bedroom` — *Crown of Dreams* | 6 bars · 68 BPM · 6/8 · D major | Music box, harp, warm pad, flute; no percussion | A spacious lullaby whose high notes have time to fade. The Roshan motif becomes a reassuring good-night phrase. |
| `castle_sleepover_bedroom` — *Whispered Pillow Fort* | 8 bars · 74 BPM · 6/8 · B-flat major | Music box, pizzicato, warm pad, bell; tiptoe pulse | Hushed but mischievous: music-box whispers and pizzicato steps suggest friends trying not to giggle after bedtime. |
| `castle_movie_lounge` — *Cloud-Reel Matinee* | 12 bars · 96 BPM · 4/4 · E-flat major | Clarinet, piano, warm strings, bell; brushes | A miniature storybook film score. Clarinet introduces the scene, piano turns the reel, and strings briefly widen before returning to couch-sized comfort. |
| `castle_family_gallery` — *Portraits Come Home* | 12 bars · 80 BPM · 3/4 · G major | Piano, warm strings, warm bass, bell; no percussion | A gentle family-album waltz. Bell highlights mark remembered adventures while every phrase resolves safely home. |

### 7.2 Pearl Opera House — lobby, 13 careers, and 3 bosses

The Opera is a theatre family inside the broader score. The lobby’s harp ostinato and warm curtain-call colors act as the foyer; each act changes costume while retaining the motif, rounded orchestration, and child-safe cadence.

| Slug and title | Authored form | Palette | Individual composition brief |
|---|---|---|---|
| `opera_lobby` — *Marquee of Many Dreams* | 8 bars · 96 BPM · 6/8 · E-flat Lydian | Clarinet, harp, warm brass, bell; brushes | A welcoming theatrical promenade whose harp ostinato links all three floors. It previews many careers without favoring one door. |
| `opera_chef` — *Flour-Dusted Overture* | 16 bars · 92 BPM · 3/4 · C major | Clarinet, piano, warm bass, pizzicato; brushes | A classical baker’s waltz: piano measures, pizzicato stirs, and clarinet presents a proud cake melody with space for instructions. |
| `opera_detective` — *The Tiptoe Clue* | 12 bars · 88 BPM · 4/4 · D Dorian | Clarinet, pizzicato, warm bass, marimba; tiptoe pulse | Sneaky clarinet questions and muted plucked answers pause to search corners. The mystery is observant and playful, never frightening. |
| `opera_ballerina` — *Ribbon Arabesque* | 12 bars · 84 BPM · 3/4 · D major | Flute, warm strings, warm bass, music box; no percussion | A graceful three-step waltz with legato lines and clear landing points that support watching and repeating dance patterns. |
| `opera_candymaker` — *Sugar-Spun Clockwork* | 12 bars · 116 BPM · 4/4 · F Lydian | Toy piano, marimba, warm bass, bell; shaker | Toy piano and marimba interlock like a friendly candy machine. It is quick and precise but never frantic. |
| `opera_doctor` — *Gentle Hands Relay* | 12 bars · 86 BPM · 4/4 · C major | Clarinet, piano, warm bass, bell; brushes | A calm practice pulse with tiny bell checkmarks. Even phrases and soft cadences communicate care, order, and reassurance. |
| `opera_farmer` — *Piggy Picnic Reel* | 12 bars · 112 BPM · 4/4 · G Mixolydian | Banjo-like plucks, fiddle-like replies, warm bass, pizzicato; bluegrass pulse | Child-friendly bluegrass with a happy root-fifth trot and voice-sized gaps. It suggests a porch reel, not a hard-driving breakdown. |
| `opera_boxer` — *Pillow-Glove Shuffle* | 12 bars · 120 BPM · 4/4 · E-flat Mixolydian | Warm toy brass, marimba, warm bass, bell; soft march/swing | Brass calls and marimba mitt replies ride an unmistakable practice beat. It is sporty, bouncy, and soft-edged. |
| `opera_magician` — *Silk Hat Starlight* | 8 bars · 92 BPM · 6/8 · A Dorian | Clarinet, harp, warm bass, chime; tiptoe pulse | Harp misdirection and low clarinet questions lead to chime reveals. Each magical suspense turn resolves with a smile. |
| `opera_painter` — *Sunrise in Seven Colors* | 12 bars · 88 BPM · 4/4 · D Lydian | Flute, piano, warm bass, bell; brushes | A flowing melody adds color one note at a time over piano brushstrokes, blooming only at the gallery reveal. |
| `opera_astronaut` — *Bubble-Rocket Workshop* | 12 bars · 110 BPM · 4/4 · E Lydian | Soft synth, marimba, synth bass, bell; clean pulse | Rounded electronic motion and marimba tools orbit a warm center. Upward sequences imply launch while staying playful and grounded. |
| `opera_racer` — *Pearl Grand Prix* | 16 bars · 128 BPM · 4/4 · G Mixolydian | Soft synth, pizzicato, synth bass, bell; drive pulse | A bright four-on-the-floor drive with plucked engine rhythm and short fanfares. Forward motion is clear without sirens or aggressive timbres. |
| `opera_popstar` — *Starlight Singalong* | 12 bars · 118 BPM · 4/4 · A major | Soft synth, toy piano, synth bass, bell; pop pulse | A simple child-pop groove built from genuine call-and-answer shapes. The arrangement must leave open answer windows for direction chimes, touch timing, and spoken prompts. |
| `opera_nursery` — *Moonbeam Tuck-In* | 7 bars · 70 BPM · 6/8 · F major | Music box, flute, warm pad, harp; no percussion | A rocking lullaby quiet enough for bedtime voices, with a pulse clear enough to support gentle care actions. |
| `opera_boss_dragon` — *Curtain Dragon's Stomp* | 12 bars · 112 BPM · 4/4 · D minor | Warm brass, warm strings, warm bass, bell; soft combat | A large but friendly stage-puppet stomp. Bell openings mark safe peek moments and every dark chord turns bright. |
| `opera_boss_phantom` — *Lanterns in the Wings* | 8 bars · 96 BPM · 6/8 · E Dorian | Clarinet, harp, warm bass, chime; tiptoe pulse | A shy shadow dance in which chimes appear like lanterns, turning uncertainty into gentle hide-and-seek. |
| `opera_boss_maestro` — *The Kind Midnight Baton* | 16 bars · 124 BPM · 4/4 · C minor | Warm brass, warm strings, synth bass, bell; soft combat | The largest Opera cue uses grand gestures and baton taps, but remains consonant and ends in a welcoming ensemble cadence. |

### 7.3 Worlds, dungeons, combat, tutorial, and Stuffie play — 9 cues

| Slug and title | Authored form | Palette | Individual composition brief |
|---|---|---|---|
| `northern` — *Snowcap Lantern Trail* | 8 bars · 84 BPM · 6/8 · D major | Flute, harp, warm bass, bell; shaker | Open flute calls cross a broad snowy landscape. Bell points act as trail lanterns and rests preserve the kingdom’s quiet scale. |
| `galaxy` — *Pocket Constellation Waltz* | 16 bars · 96 BPM · 3/4 · A Lydian | Celesta, soft synth, warm pad, bell; pulse | Celesta stars orbit in a slow three-count while a grounded bass keeps space cozy. The motif hops between constellations. |
| `ember` — *Warm-Coal Courage* | 12 bars · 104 BPM · 4/4 · E minor | Marimba, warm strings, warm bass, bell; soft march | Low marimba and strings step steadily through glowing terrain. Rising bell answers frame embers as warmth and courage rather than danger. |
| `dungeon_ice` — *Crystal Footsteps* | 12 bars · 90 BPM · 4/4 · D Dorian | Music box, pizzicato, warm bass, chime; tiptoe pulse | Music-box crystals answer muted footsteps. A patient bass supports exploration without implying a fail timer. |
| `dungeon_ember` — *Lanterns Under the Mountain* | 12 bars · 100 BPM · 4/4 · E minor | Pizzicato, warm strings, warm bass, bell; soft march | Plucked lantern notes travel in a measured march. Minor depth is repeatedly warmed by reassuring major inflections. |
| `combat_ice` — *Snowball Sparkle Scramble* | 16 bars · 124 BPM · 4/4 · D Dorian | Marimba, warm strings, synth bass, chime; soft combat | Fast marimba snowballs and chime hit markers create readable action without harsh cymbals, alarms, or menace. |
| `combat_fire` — *Pepper-Pop Parade* | 16 bars · 128 BPM · 4/4 · E Mixolydian | Warm brass, pizzicato, synth bass, bell; soft combat | Warm brass pops and bright plucks sound cheeky and brave, never hot, threatening, or punishing. |
| `combat_tutorial` — *Royal Hall Practice Pals* | 12 bars · 104 BPM · 4/4 · C major | Marimba, warm brass, warm bass, toy piano; tutorial brushes | A clear practice pulse whose accents teach timing while the harmony says “play,” not danger. |
| `stuffie_battle` — *Hug-It-Out Hoedown* | 12 bars · 116 BPM · 4/4 · G major | Banjo-like lead, fiddle-like replies, warm bass, marimba; bluegrass pulse | A friendly hoedown about befriending a Stuffie, never defeating one. Its portable arrangement works over reef, lagoon, or Castle ambience. |

### 7.4 Picture games — 4 cues

Picture games are full-screen overlays. Each saves the parent cue, plays its own track, and restores only if it still owns the close operation; a delayed win callback must not overwrite music chosen by a newer screen.

| Slug and title | Authored form | Palette | Individual composition brief |
|---|---|---|---|
| `picture_snowman` — *Roll a Round Snow Friend* | 8 bars · 104 BPM · 6/8 · D major | Clarinet, pizzicato, warm bass, bell; sleigh pulse | Cheery rolling phrases grow from small to large like the three safe snowballs. Bell snowflakes mark progress without crowding touch sounds. |
| `picture_garden` — *Little Garden, Big Sun* | 12 bars · 92 BPM · 4/4 · F major | Flute, ukulele, warm bass, pizzicato; shaker | Sunny ukulele planting strokes and flute sprouts rise at an easy walking pace, then settle in warm soil. |
| `picture_trampoline` — *Up, Up, Soft Landing* | 12 bars · 116 BPM · 4/4 · C major | Marimba, pizzicato, warm bass, bell; bubble pulse | Predictable marimba jumps and pizzicato landings trace an up-down arc with enough space for touch timing and giggles. |
| `picture_xmas` — *Cozy Winter Decorating* | 8 bars · 84 BPM · 6/8 · G major | Celesta, warm strings, warm bass, bell; sleigh pulse | A non-religious cozy-winter cue about decorating, snowlight, and family togetherness. Sleigh color is gentle, not constant. |

## 8. Transition and ambience ownership

The owner of a temporary musical state must capture the cue before changing it and restore that exact cue on every normal, cancel, back, pause-leave, and delayed-callback exit.

| State or transition | Music owner and contract | Ambience contract |
|---|---|---|
| Reef day/night | `AudioDirector` resolves logical `world` to `world_night` at night while keeping `cur_track == "world"` restorable | Reef bed for `world`; reef bed for `finale` |
| Sky Lagoon | Main selects `level2` on entry | Lagoon bed |
| Castle door reveal | Main saves `prev_track`, plays `castle_open` once, and restores only while that stinger still owns the player | Lagoon bed |
| Castle rooms | The Level 2 owner observes `castle_room_id` while the Castle stage is visible, mapping `main_hall` to retained `hall` and each side-room ID to its matching `castle_*` cue | Hall room tone for `hall`, `home`, and every `castle_*` cue |
| Castle sleep | Legacy full sleep selects `home` and currently returns to `hall`; any future sleep entry from a side-room context must capture and restore its caller rather than assume Main Hall | Hall room tone |
| Opera House | `OperaHouse.start()` captures the incoming Castle cue, owns `opera_lobby`, returns to it after each act, then restores the captured cue on exit | Hall room tone for `opera_lobby` and all `opera_*` cues |
| Opera act | `OperaAct` captures lobby music, owns the act cue, and restores its captured cue on completion or cancellation | Hall room tone |
| Opera nested race | The kart segment temporarily owns retained `race`, then returns to `opera_racer` | Existing legacy minigame behavior during the nested segment |
| Northern Kingdom | Main owns `northern` from cave entry until return to `level2` | Lagoon bed |
| Galaxy | Main owns `galaxy`; nested combat or Fairy play must return to it before the world exits | Lagoon bed |
| Ember approach | Main owns `ember`; the dungeon captures and restores it | Lagoon bed |
| Ice/Ember dungeons | Main captures `dungeon_prev_track`, plays `dungeon_ice` or `dungeon_ember`, and restores the exact parent cue on exit | Lagoon bed |
| Ice/Fire combat | Main captures `combat_prev_track`, plays `combat_ice` or `combat_fire`, and restores the exact parent cue | Lagoon bed for Ice; Hall bed for Fire because the pepper encounter belongs to the Pearl Castle route |
| Combat tutorial | `CombatTutorial` captures its caller, owns `combat_tutorial`, and restores only if it successfully acquired ownership | Hall room tone |
| Stuffie battle | Main captures `stuffie_prev_track`, owns `stuffie_battle`, then restores it | Preserve the source area’s current ambience instead of replacing it |
| Picture overlay | `PictureGames` stores `music_return`, plays `picture_<kind>`, and lets only the first close restore it | Lagoon bed for all four picture cues |
| Dance Engine | Saves the exact prior stream, playback position, and playing state; uses its own music player for `melody`, `race`, or `finale`; restores the exact stream position | Does not redefine the area ambience |
| Legacy minigames | The minigame/main owner captures `return_track` and restores it at the activity boundary | Existing behavior retained; legacy cues not listed in the area ambience map may stop the shared bed |
| Missing file | `AudioDirector` returns before changing `cur_track`, stream, or ambience | Existing music and ambience remain coherent |

The current ambience families are therefore intentional rather than inferred from filename alone:

- **Reef bed:** `world`, `finale`.
- **Lagoon bed:** `level2`, `castle_open`, `northern`, `galaxy`, `ember`, `dungeon_ice`, `dungeon_ember`, `combat_ice`, and every `picture_*` cue.
- **Hall bed:** `hall`, `home`, `combat_tutorial`, `combat_fire`, every `castle_*` cue, and every `opera_*` cue.
- **Preserve caller’s bed:** `stuffie_battle`.

## 9. Render evidence and provenance

### 9.1 New-score provenance

The declarative score identifies itself as schema `reef.area-music-scores.v1` and declares: “Project-owned original composition and deterministic synthesis; no samples, soundfonts, downloaded audio, or protected recordings.” `tools/build_area_music.py` rendered all 42 cues and produced `assets/audio/music/area_music_manifest.json`, schema `reef.area-music-manifest.v1`. The renderer, outputs, hashes, import metadata, and explicit `ASSET_LICENSES.md` entry passed automated and independent source review; subjective listening remains separate.

No book art, family voice, or friend recording may be changed, sampled, recompressed, or embedded to make these tracks. Synthesized labels such as banjo, fiddle, accordion, brass, celesta, and ukulele describe original procedural timbres, not third-party recordings.

### 9.2 Required manifest evidence

The deterministic rendered-audio manifest contains shared build provenance plus one output record for every new slug. Together, its top-level and per-output fields record:

- cue slug, title, score-schema version, and source score hash;
- renderer path/version and renderer hash;
- deterministic seed namespace and derivation rule for every seeded-noise event;
- PCM/render hash, production OGG path and SHA-256, and license class;
- duration, sample rate, channels, codec, nominal bitrate, and file-size-derived average bitrate;
- integrated LUFS, loudness range if reported, and true peak;
- loop start/end or whole-file loop declaration, import-loop state, and seam test result;
- the exact recorded Python, NumPy, SciPy, and FFmpeg toolchain.

Wall-clock timestamps are intentionally omitted from the manifest so a byte-identical rebuild can produce byte-identical evidence. The version-control commit supplies historical time. Human two-wrap listening, voice-over intelligibility, mono fold-down, and target-device review remain review records in this document rather than invented machine fields.

### 9.3 Measurement status for the 42 new cues

| Evidence field | Status as of this implemented audit |
|---|---|
| PCM hash, production OGG path, and OGG SHA-256 | **COMPLETE** — 42 unique PCM hashes and 42 unique OGG hashes |
| Measured duration | **COMPLETE** — 24.000–38.918917 seconds; every cue is an integer-bar loop |
| Measured channels and sample rate | **COMPLETE** — all Ogg Vorbis, 48,000 Hz, stereo |
| Measured bitrate | **COMPLETE** — 89,766–98,551 bps; all clear the 64 kbps floor |
| LUFS-I / true peak / LRA | **COMPLETE** — −18.05 to −17.97 LUFS; −8.76 to −4.10 dBTP; 1.1–6.1 LU LRA |
| Loop tags/import flags/seam metric | **COMPLETE (automated)** — exact-sample tags, `loop=true`, BPM/meter/beat metadata, decoded seam jump ratio 0.00054–0.19840 |
| Reproducible source evidence | **COMPLETE** — generator `49578229…8509d`; score catalog `a85bb860…c575a`; 42-record complete manifest; 14.249 MiB total |
| Human style, voice, and two-wrap listen | **PENDING** |
| Lenovo Tab M11 start/loop/performance listen | **PENDING** |

The exact unabridged measurements and full hashes live in `area_music_manifest.json`; shortened hashes above are for human scanning only.

### 9.4 Audit provenance

This document was prepared on branch `codex/unique-area-music-20260809`, based on commit `ecad384e99c3f956e7559f9801c37f4a4a1a2111`, and then reconciled against the completed score, renderer, production manifest, and music-routing diff. Evidence inspected includes:

- `assets/audio/music/*.ogg` and every paired `.ogg.import`;
- `ASSET_LICENSES.md`, `ASSET_AUDIT.md`, commit `fe44318b`, `CC0_REPLACEMENT_WORKORDER_2026-07-22.md`, and `gen2/GEN2_REBUILD_WORKORDER.md`;
- `assets_src/audio/music/area_music_scores.json`, `tools/build_area_music.py`, and the complete 42-record `assets/audio/music/area_music_manifest.json`;
- `scripts/audio_director.gd`, `scripts/main.gd`, `scripts/arena/castle_rooms_25d.gd`, `scripts/opera_house.gd`, `scripts/opera_act.gd`, `scripts/combat_tutorial.gd`, `scripts/games/picture_games.gd`, and `scripts/games/dance_engine.gd`;
- the owner’s 2026-08-09 request and Craft Room reference, especially the request for sneaky Detective music, classical/homey Baker music, and bluegrass Farmer music within one child-friendly family;
- `ffprobe` stream inspection and FFmpeg EBU R128/true-peak analysis for the 15 legacy files;
- the renderer’s complete build and `--check` run with pinned FFmpeg 8.1.2, plus independent catalog, hash, codec, bitrate, loudness, decode, seam, and import-metadata review.
- exact Godot 4.7.1 branch CI at commit `27c2c95d`, including static gates, import, the real script analyzer, every trusted probe, boot gate, balance checks, and visual captures: [run 31354631664](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/31354631664).

## 10. Acceptance criteria

The music pass is complete only when all of the following are true.

### Coverage and ownership

1. Exactly all 42 required new slugs have production OGGs at `assets/audio/music/<slug>.ogg`.
2. The 12 Castle side rooms have unique cues and `main_hall` still uses retained `hall`.
3. Opera lobby plus all 16 acts have unique cues; no two Opera acts share a slug.
4. Northern, Galaxy, Ember, both dungeons, both combats, Stuffie battle, combat tutorial, and all four picture games enter with the expected cue.
5. Every temporary activity restores the exact caller cue on success, cancel, Back, pause-leave, and delayed close. A stale callback cannot overwrite a newer area cue.
6. Requesting a nonexistent cue changes neither the audible stream nor `cur_track`.
7. Requesting the already-active cue does not restart it; it may repair ambience without resetting musical position.

### Composition and child experience

8. Each cue communicates its area within the first two bars and is recognizably distinct from adjacent areas after two loops.
9. Each cue states and transforms the Roshan motif; the result sounds composed for the room, not mechanically pasted in.
10. The sparkle-return cadence remains recognizable while bright accent timbres stay sparse and do not mask real reward fanfares, dialogue, or touch feedback.
11. Detective is sneaky but safe; Chef/Baker is classical and homey; Farmer is bluegrass but gentle; all other briefs meet the pacing and emotional intent in Section 7.
12. No cue contains lyrics, sirens, alarm-like pulses, harsh cymbal crashes, aggressive distortion, fail-state tension, or frightening unresolved endings.
13. Family voice instructions remain intelligible at default volume on phone speaker. Pop Star and other rhythm-heavy cues leave real answer space.

### Audio and loop quality

14. Every new file is Ogg Vorbis, 48 kHz stereo, 24–40 seconds, an exact integer number of bars, and encoded at managed 96 kbps within the allowed 80–128 kbps range.
15. Every new OGG carries exact-sample `LOOPSTART`, `LOOPEND`, and `LOOPLENGTH` tags plus `BPM`, `METER`, and `CUE_ID`; its Godot import has loop, BPM, and beat count enabled.
16. Each new cue measures from -18.5 to -17.5 LUFS-I and no higher than -3.0 dBTP.
17. Two consecutive loop wraps have no click, doubled attack, level jump, codec flutter, conspicuous silence, or harmony/reverb discontinuity by automated check and human listening.
18. Mono fold-down preserves melody, bass, pulse, and room identity without cancellation or an abrasive high-frequency balance.
19. Music ducking reaches the intended voice-safe level without pumping, and music-off remains silent through transitions and ducking.

### Runtime, device, and provenance

20. The audio probe confirms every required file exists, imports looped, routes through Music, retains the correct ambience family, and satisfies unique Castle/Opera coverage.
21. Full trusted probes pass under exactly Godot 4.7.1-stable.
22. On Lenovo Tab M11, every new cue starts without a noticeable stall and loops for several minutes without under-run, runaway memory, or overlapping music players.
23. `area_music_manifest.json` contains all fields in Section 9.2, including score, generator, PCM, and OGG hashes, and its measured values are represented here without invention.
24. `ASSET_LICENSES.md` records the score source, renderer, outputs, project-owned license, and the fact that no samples, soundfonts, downloaded audio, or protected recordings were used.
25. Source score, renderer, native render if distinct, production OGG, import metadata, and hashes are preserved together so the 42 cues are reproducible and reviewable.

Criteria 1–7, 14–16, 20, 21, and 23–25 now have automated evidence. Criteria 8–13, 17–19, and 22 include human listening, in-game mix, or target-device judgment and remain open until those reviews are recorded; no automated measurement is presented as a substitute for a child-facing listen.
