# Audio and Sound-Design Audit — 2026-08-23

## Status and scope

**Result: `GAPS_CONFIRMED`; discovery only.** The game has a sound architecture and a large music/voice inventory, but it does not yet provide consistent action-specific audio feedback or exact non-reader speech for every important objective. The external intro video has technically valid audio but it is effectively silent for most of its 42-second timeline.

This audit is bound to repository commit `89b004ac91c959a0dc990e5e525e16136c9c3a97` on `codex/audio-soundscape-audit` and to the read-only source video below. No runtime audio, protected voice, source video, art, scene, or gameplay file was changed during discovery.

- Source video: `C:\Users\Peter\Intro for mermaid roshan.mp4`
- Source SHA-256: `8506F97A7CD2E3B8697FF6B09399A44D9ABB74B508F30115A8E189BE900E644E`
- Source size: 15,370,770 bytes
- Protected paths remain untouched: `assets/book/`, `assets/audio/voices/`, and `assets/characters/friends/`

The review used static inspection of scripts, scenes, audio inventories/manifests, design/audit authority, and read-only `ffprobe`/`ffmpeg` measurements of the source MP4. Timeline sound suggestions are editorial recommendations, not claims that the existing sparse audio is semantically wrong; final choices require owner listening and picture review.

## Executive priorities

1. **P1 — exact non-reader objective speech:** Seek, Dolls, and Lamba are already authoritative open accessibility findings. Harper's fish objective, Dust Boss instructions, and several first-action prompts also fall back to generic speech rather than saying what to do.
2. **P1 — intro video coverage:** audio is silent from 0–17.00 seconds and again after roughly 23.00 seconds. The important cabin conversation at 23.04–28.00 seconds is completely silent.
3. **P1 — semantic feedback consistency:** gameplay has strong generic taps/chimes and a combat pack, but many actions depend on one generic sound or visuals alone. A small, reusable semantic SFX vocabulary should distinguish select/confirm, progress, success, blocked/retry, pickup/drop, movement/contact, and transitions.
4. **P2 — mix and transitions:** music changes are hard stream swaps with fixed starting gain; five buses exist but have no limiter, compressor, or side-chain effect. Existing script ducking is helpful but human voice-mix, mono, two-wrap, transition, and Lenovo Tab M11 acceptance remain open under `MA-AUDIO-001`.

There is no evidence of a broad need to regenerate the 42 deterministic area cues or the existing Castle prop pack. Reuse and bounded additions are the correct path.

## Current foundation and verified strengths

| Area | Exact evidence | Assessment |
|---|---|---|
| Named buses | `default_bus_layout.tres` defines `Music`, `Voice`, `SFX`, `Ambience`, and `UI`; `scripts/probe_audio.gd:25-38` checks existence and routing. | Good routing foundation. There are no bus effects or a master safety limiter. |
| Voice resolution | `scripts/audio_director.gd:13-47` tries `<speaker>_<event>.ogg`, then `<speaker>.ogg`, then pitched `assets/audio/voice_yay.mp3`; duplicate recordings are suppressed across the voice pool. | Graceful technical fallback, but a generic acknowledgement is not an exact non-reader instruction. |
| Dialogue/captions | `scripts/audio_director.gd:52-177` queues dialogue, allows touch-to-advance, and restores a caption in Opera when an exact clip is missing. | Strong non-blocking flow and adult reading aid. Captions cannot close a four-year-old non-reader speech gap. |
| Music | `assets/audio/music/area_music_manifest.json` owns 42 deterministic area cues; `scripts/probe_audio.gd:14-73` checks cue existence, looping, unique Opera cues, and Castle mappings. | Mechanically mature. Human style, fatigue, mono, voice masking, loop-wrap, and M11 review remain open. |
| Ambience | `scripts/audio_director.gd:203-257` maps tracks to `ambience_reef.ogg`, `ambience_lagoon.ogg`, or `ambience_hall.ogg` and ducks music/ambience by 6 dB while pooled voices play. | Continuous basic beds exist, but only three broad environments are represented. |
| UI and gameplay SFX | `scripts/audio_director.gd:261-323` supplies global button taps, a combat pop pitch ladder, and a four-player WAV SFX pool. `scripts/arena/castle_rooms_25d.gd:3314-3324` routes Castle prop sounds. | Good primitives; semantic coverage is uneven outside combat and Castle props. |
| Existing audit authority | `audit/findings/ACTIVE_FINDINGS_2026-08-13.md`, `MA-ACCESS-001..003` and `MA-AUDIO-001`. | Existing blockers remain authoritative and are not superseded by this report. |

## Game-wide gaps

### P1 — exact speech and non-reader comprehension

| Activity / objective | Current evidence | Child-facing gap | Required disposition |
|---|---|---|---|
| Seek | `scripts/games/seek.gd:232-233,602-603` records `objective_recording_gap = "evie_tap_wiggly_bush"`. The message says “Tap the wiggly tree”; visual wiggle/U-cue/peek/pointer exist. `MA-ACCESS-003` is `BLOCKED_EXTERNAL`. | Generic Evie speech does not name the exact tap action. | Owner-authorized exact Evie line; preserve all existing recordings and pair it with the existing pointer. |
| Dolls | `scripts/games/dolls.gd:248-258` records `objective_recording_gap = "faron_catch_three"`; current goal is three while the available protected catch line says five. A pointer exists. | Spoken count conflicts with current objective. | Owner-authorized “catch three” recording at a new path/key; old protected file remains intact. |
| Lamba | `MA-ACCESS-002` confirms the current semantic role can still play protected legacy “bunny-fish” speech. | Voice and visible identity disagree. | Owner-authorized corrected recording and exact routing; add a negative test that the legacy mismatch is unreachable. |
| Harper fish objective | `scripts/games/slide_race.gd:334,481` requests `harper_hint`; no `harper_hint.ogg` exists, so `harper.ogg` is used. Persistent side arrows provide the visual cue. | The visual destination is strong, but the speech does not state the fish action. | Add an owner-authorized exact clip or approve an independently sufficient existing cue after child/device review. |
| Dust Boss | `scripts/games/dust_boss.gd:136,222,307,322,391,398,401,467,747-761` uses `dustboss_show/tell/closer/dizzy/hit/win`; matching recordings are absent. Captions and finger/open-state pointers exist. | Bespoke action events collapse to generic Roshan/environment fallback. | Choose an intentional speaker, then authorize exact clips for indispensable instructions. Do not synthesize or overwrite protected voices. |
| Shop | `scripts/games/shop.gd:237` gives a generic “tap to buy” prompt; no dedicated picture-first objective card or explicit pointer was evident. | Weakest discoverability case: proximity, readable text, and a generic voice are insufficient evidence for a non-reader. | First add/reuse a visible item pointer/card; then obtain exact speech only if the visual+diegetic buy cue is not independently sufficient. |

### P1/P2 — generic first-action prompts

The following prompts use default `"talk"` or family fallback while visuals do much of the teaching. Each needs a short objective-contract review: one exact spoken action plus a synchronized visual pointer, or a proven independently sufficient diegetic alternative.

- Treasure: `scripts/games/treasure.gd:113` (“follow the sparkles”); sparkles/checkpoints exist.
- Fetch: `scripts/games/fetch.gd:199`; the green-arrow throw cue is visually strong.
- Fairy: `scripts/games/fairy.gd:334`; flower/shadow/shield visuals exist but the instruction is multi-part.
- Music room: `scripts/main.gd:7244,7252`; bell highlights/chimes teach “ring/copy the bells,” while speech is generic.
- Dungeon puzzle: `scripts/dungeon_puzzle_room.gd:61,474,485,489,492`; golden arrows/picture matching exist, while speech is generic.
- Free-roam onboarding: `scripts/main.gd:8047-8055` speaks movement/action/light-pillar text, but the function itself does not couple each line to a dedicated pointer. Verify whether the visible stick/action UI is sufficient on phone.

### P2 — speaker identity and fallback semantics

`scripts/audio_director.gd:107-135` maps unrecognized speaker labels to Roshan. Environment labels such as `Ember King`, `Dusty Attic`, `Toy Castle`, `Fairy Pond`, `Secret Cave`, `Penguin Slide`, `Music Room`, and `Rainbow Road` can therefore speak with a generic Roshan fallback. This is technically safe but semantically ambiguous. Activities should pass an explicit speaker identity, or the resolver should define intentional non-character handling. Never make an environment label masquerade as a new family voice.

### P2 — sound vocabulary, mix, and transitions

- `_play_music()` in `scripts/audio_director.gd:326-351` swaps streams and starts at `-8 dB`; there is no crossfade or bounded fade-to-ambience transition. Audit transitions before adding fades because one-shot cues such as `castle_open` and `finale` must retain authored timing.
- `_tick_ambience_duck()` uses player-state polling and fixed targets (`Music -14 dB`, `Ambience -16 dB` while talking). It does not show true-peak or dialogue-priority protection at the bus level.
- `default_bus_layout.tres` has no limiter/compressor. A child-safe master limiter is a candidate only after measured listening proves it necessary; do not use it to mask bad gain staging.
- `assets/audio/buzz.ogg`, `assets/audio/fart.ogg`, and `assets/audio/purr.wav` appear unreferenced in runtime searches. Preserve them; do not delete or repurpose without owner review.
- Music-off behavior only drives the `Music` player to `-60 dB`; SFX, UI, ambience, and Voice remain available. That is desirable for non-reader feedback, but needs device verification.

## Intro video audit

### Technical measurements

| Property | Measured value |
|---|---|
| Container / encoder | MP4 / DaVinci Resolve |
| Video | H.264 Main, 1280×720, 16:9, BT.709 progressive, 24 fps, 42.125 s, about 2.659 Mbps |
| Audio | AAC-LC stereo, 48 kHz, 256 kbps, 42.133 s |
| A/V duration difference | About 8 ms |
| Integrated loudness | **-37.1 LUFS** |
| Loudness range | **20.4 LU** |
| True peak | **-20.4 dBFS** |
| `volumedetect` | Mean **-50.4 dB**, max **-20.5 dB** |
| Stereo relationship | Correlation **0.9967**; effectively dual-mono |
| Silence at -40 dB | **0.000–17.000646 s** |
| Clearly active audio | About **17.0006–21.2288 s** |
| Low-level tail at -50 dB | Detectable to about **22.99 s**; silent thereafter to 42.1333 s |

The very low integrated loudness is primarily a consequence of missing coverage, not evidence that the entire file should simply receive a large gain boost. Normalizing the existing sparse stem alone would leave the story silent and could make the short active passage disproportionately loud.

The active span is low-mid-heavy at 17–18 seconds (roughly -38 to -37 dBFS RMS, 75–83% of energy below 300 Hz), contains a very quiet transient/whoosh around 18.75–19.25, reaches its strongest activity around 19.75–20.00 seconds (about -33.95 dBFS RMS), and decays with a higher-frequency tail through about 22.99 seconds. Audio-only measurement cannot prove whether this is engine, creature, movement, or another intended effect; retain it as a reference and evaluate it against picture before reuse.

### Timeline sound map

| Time | Picture/action observation | Current audio | Sound-design need |
|---|---|---|---|
| 00:00–00:02 | Airplane cruising | Silent | Gentle plane/air bed and a soft opening musical identity; no harsh engine start. |
| 00:02–00:04.5 | Roshan and child inside plane | Silent | Quiet cabin room tone; optional short authorized family exchange if the story needs an instruction. |
| 00:04.5–00:07.5 | Island/castle aerial reveal and approach | Silent | Small magical reveal and restrained transition lift. Reuse chime language only if it does not imply gameplay success. |
| 00:07.5–00:12.5 | Castle, forest path, lakeside | Silent | Layered but sparse birds/forest/water ambience with gentle, non-startling perspective changes. |
| 00:12.5–00:14 | Playground airplane before otter arrival | Silent | Carry the ambience; add a soft anticipatory cue only if picture timing supports it. |
| 00:14–00:17 | Otter arrival begins | Silent | Child-readable arrival/movement cue; preserve headroom for the existing 17-second onset. |
| 00:17–00:23 | Otter climbs/plays around plane | Existing low-level active span | Identify the existing sound by listening, then supplement only missing arrival, climb, contact, movement, and reaction beats. Avoid wall-to-wall cartoon noise. |
| 00:23.04–00:28 | Cabin conversation / wide shot | Completely silent | **P1:** authorized dialogue or a clear nonverbal conversational/story cue. A visible conversation without speech is the largest accessibility discontinuity. |
| 00:28.04–00:36.08 | Family and otter outside plane | Silent | Gentle footsteps/body movement and one or two interaction acknowledgements; keep voices dominant. |
| 00:36.08–00:42.125 | Family approaches castle bridge | Silent | Water/bridge ambience and a warm arrival cadence that resolves without sounding like a fail/win gate unless the story declares one. |

## Reuse-first palette

Use the smallest number of recognizable, soft sounds. Candidate sources already in the repository:

- UI/feedback: `assets/audio/ui_tap.ogg`, `assets/audio/chime.ogg`, `assets/audio/buy.ogg`, `assets/audio/hop_boing.ogg`, `assets/audio/penguin_giggle.ogg`.
- Gameplay reactions: `assets/audio/sfx/combat_pop.wav`, `combat_bonk.wav`, `combat_poof.wav`, `combat_freeze.wav`, `combat_fizzle.wav`, and `combat_charge_ring.wav`. These may be reused only when their semantics match; do not make every action sound like combat.
- Castle props: the bounded set in `assets/audio/castle/castle_interaction_sfx_manifest.json` (`curtain_swish`, water, door, page, brush, blocks, switch, and related cues).
- Beds: `assets/audio/ambience_reef.ogg`, `ambience_lagoon.ogg`, and `ambience_hall.ogg`. Derive or layer new beds only when these materially fail the scene, at new paths with provenance.
- Existing music: the deterministic area catalog in `assets/audio/music/area_music_manifest.json`; do not broadly regenerate it.
- Existing voice fallbacks are useful for greetings/reactions, not as substitutes for exact instructions. Everything under `assets/audio/voices/` is protected for this task.

For new non-voice runtime SFX, bounded procedural synthesis is acceptable when reuse is semantically wrong. New audio must be OGG, music at least 64 kbps and loop-tagged, and must receive an `ASSET_LICENSES.md` entry in the same implementation commit.

## Concrete remediation backlog

### Track A — safely implementable without new owner recordings

1. **A1 / P1: objective-contract inventory and probe.** Create a data-backed test that enumerates first-action objectives and asserts a visual pointer plus either an exact authorized clip or a declared diegetic alternative. Seed it with Seek, Dolls, Lamba, Harper fish, Dust Boss, Shop, Treasure, Fetch, Fairy, Music Room, Dungeon, and free-roam onboarding. This must not pretend generic `talk` proves exact coverage.
2. **A2 / P1: Shop visual discoverability.** Reuse existing item art/objective-card/pointer components to add an unmistakable picture-first buy target before commissioning voice.
3. **A3 / P1: semantic SFX matrix.** Inventory gameplay actions against seven gentle families: focus/select, confirm, progress, success, blocked/retry, pickup/drop/contact, and world transition. Reuse current assets where meaning fits; create only missing non-voice cues procedurally at new paths.
4. **A4 / P2: explicit speaker routing.** Stop using environment labels as implicit speaker identities. Pass a known speaker for each message or define a deliberate silent/non-character route; preserve current captions and fallback behavior until focused probes are green.
5. **A5 / P2: bounded music-transition prototype.** Add a two-player or tweened gain handoff only for audited area-to-area changes, with cancellation/teardown, pause, music-off, re-entry, and one-shot tests. Do not crossfade authored stingers indiscriminately.
6. **A6 / P2: extend audio probes.** Verify SFX/UI/Voice/ambience behavior with music off, no duplicate generic voice overlap, transition restoration, and missing-cue negatives. Keep human listening as a separate gate.
7. **A7 / P1 intro design:** build a cue sheet and reuse audition for the timeline above. Preserve the original MP4 and its current audio as immutable reference; create all mixes/renders at new paths.

### Track B — explicitly owner-authorized recording work

1. **B1:** Evie exact “tap the wiggly tree” line.
2. **B2:** Faron exact “catch three” line.
3. **B3:** corrected Lamba identity/objective line.
4. **B4:** Harper exact fish-objective line if the existing pointer does not pass child comprehension alone.
5. **B5:** intentional Dust Boss speaker and the minimum indispensable `dustboss_*` instructions.
6. **B6:** intro cabin conversation and any family lines required to explain the 23.04–28.00-second beat.

These are blocked until the owner supplies or explicitly authorizes new recordings. Add new files and provenance; never edit, recompress, overwrite, or substitute existing protected originals.

### Track C — listening and acceptance

1. Listen to two complete wraps of all 42 deterministic area cues, including hard transitions and return paths.
2. Test exact voices over music/ambience, music-off/on restoration, and mono fold-down on headphones, a small mono speaker, the 3–4-year-old Android phone, and Lenovo Tab M11.
3. For the intro, review picture with the existing stem, then the proposed cue sheet, then a complete mix. Measure final integrated loudness/true peak only after coverage is authored.
4. Observe the child completing each P1 objective without reading or adult instruction. Machine routing and captions are supporting evidence, not substitutes.

## Acceptance gates for implementation

- No protected original or source MP4 changes; hashes are preserved.
- Every new objective has synchronized exact speech and a visual pointer, or an owner-approved independently sufficient diegetic alternative.
- Wrong actions never produce a success cue; passive input never advances progress.
- Music-off leaves Voice/UI/SFX accessibility feedback audible and does not resurrect muted music during ducking or transitions.
- No harsh startle peaks, alarm-like failure language, or punitive sounds; feedback remains calm, brief, and distinct on the target devices.
- New assets meet codec/bitrate/loop rules and receive same-commit license/provenance entries.
- Parser/lint, focused audio/voice/passive/activity probes, full Godot 4.7.1 CI, mono/headphone/device listening, and child comprehension all pass before closure.
