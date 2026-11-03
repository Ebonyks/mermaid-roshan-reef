# Expanded palette and three private soundtrack tests

Status: `PRIVATE_REVIEW_TESTS_AUTHORIZED`; final artistic, game-mix, device and child acceptance remain pending. The [owner commission](expanded_palette_test_tracks_owner_direction_20261101.json) requests arrangements followed by test tracks. This scoped permission permits the tests while the final-review boundary in `DL-SND-18` remains intact.

The [ten-bank inventory](INSTALLED_PALETTE_2026-11-01.json), [native auditions](INSTRUMENT_AUDITIONS_2026-11-01.json), [performer profiles](performers/README.md) and [section call sheets](CUE_PLANS_2026-11-01.json) are the working sources. Bonobo remains the producer's single primary identity. References guide technique, form and ensemble judgement; their melodies and recordings are not construction material.

## Confirmed expansion

Falcon inside REAPER displays Atmospherics, Beatbox Anthology 2, Ether Fields, Jazzistic, Key Suite Acoustic, Key Suite Electric, LoFi Dreams, Percussion Factory, Sunbird and World Suite 3. Sunbird is the explicitly requested Acousticsamples library powered by UVI. Soul Bass and Soul Drums files were also discovered, but their native mounting is unverified and they are not selected for these tests.

The private host previously scanned a parent soundbank folder non-recursively. File links expose the same original bank files at that scanned level. Originals remain intact; no activation files or licensing settings were edited. Both Falcon interfaces display `v26.0.3 x64`; the executables' file-version metadata reports `26.0.1`. This was a search-location problem rather than evidence that Percussion Factory was absent.

Five exact native programs were captured, recalled in REAPER, rendered, checked for finite/unclipped stereo output and level-matched: Percussion Factory **Mambo Night 100BPM**, Key Suite Acoustic **TDR Mellow Dark**, Key Suite Electric **W 200 Basic Dry**, Atmospherics **Warmth**, and Ether Fields **FM Harp**. A sixth diagnostic separately tests Mambo Night's factory sequence and host tempo. All six have silent prerolls and passed native/measurement checks; together with the earlier 28 comparisons there are 34 tests.

The Mambo kit's direct white-key mapping is MIDI 24/26/28/29/31/33/35/36. MIDI 72 triggers its factory sequence. The songs use authored direct claves/shekere notes, not that factory sequence. These are legacy Percussion Factory observations; no newer edition's features are assumed. See the [official legacy manual](https://uvi.s3.amazonaws.com/Manuals/percussion_factory_manual.pdf).

Five 15.3-second new auditions were assessed through the owner-approved listening service. Its warmth/brightness opinions are advisory. In particular, its suggested percussion click at 0.8 seconds falls inside measured digital silence; that timestamp is not accepted as a defect. Native source identity, codec, loudness, peaks and mono measurements are separate evidence from listening acceptance.

## Written arrangements

| Cue | Form and length | Lead and section identity | New colours |
|---|---|---|---|
| Opera House — The Curtain Opens | 112 BPM, D major, 4/4; 96 bars, about 3:32 | Four-bar curtain hook; two 16-bar verses, four-bar keyboard preparations, eight-bar refrains, eight-bar keys bridge, eight-bar guitar dialogue, 16-bar final refrain and four-bar close. One pan owns the melody; guitar and keys take foreground during its rests. | Dry W200 reed piano; hand-written Percussion Factory claves/shekere; soft Ace T1 pulse under congas. |
| Sky Lagoon — Cloudwater Crossing | 100 BPM, G major, 4/4; 88 bars, about 3:40 | Plucked opening; recurring eight-bar flute refrains; contrasting verses and keyboard preparations; plucked dialogue; Udu bridge; 16-bar final return and landing. Tabla and Udu alternate. | Atmospherics Warmth enters selected later refrains, leaving the opening exposed. Valiha is the actual D1 selection inside the legacy program named Kora 1. |
| Castle — Welcome Home | 84 BPM, Bb major, 3/4; 96 bars, about 3:32 | Guitar threshold and home refrain; 16-bar verses; piano bridge; nylon-guitar dialogue; final homecoming and eight-bar coda. Bodhran belongs to the verses, soft lo-fi drums to refrains. | Tender upright's TDR Mellow Dark; sparse FM Harp replies in selected developed sections. |

The original owner-approved A/B melody files are checked against their approval receipt by **file SHA-256**. Opera's A–B–D recognition and complete answer return in its refrains, with one bounded alternating-strike cadence roll per selected statement. Sky's G–D–E theme expands its original quarter-note phrasing into 4/4; plucked statements move down an octave. Castle returns to the original approved 3/4 theme's D–C–Bb descent and answer, rather than retaining the later 4/4 study's rhythm. Reference recordings are not transcribed.

Each selected player has a profile revision/hash, source program/articulation, section role, foreground/groove responsibility, handoff and physical limitation in the call sheet. Comping and foreground lines from one keyboard/guitar are printed on separate editable tracks with mutually exclusive roles. They do not imply two simultaneous physical performances. Bass anchors phrases; chorus lifts add density; bridges and codas remove it. Bounded timing/velocity differences support the shared pocket rather than randomized pitch or constant fills.

## Native construction and mix

A private REAPER profile uses Dummy Audio and no user project. After the one-time native preset captures, the Lua worker performs MIDI construction, instrument recall, ReaEQ, section-volume envelopes, five group prints, routing, shared room, mix printing and mastering. It accepts only named stages. Files stay in ignored build locations and the owner's private REAPER review folder. Vendor banks and captured preset states are not published.

Guitar touch/register and small staggered voicings precede EQ. Native guitar EQ removes sub-bass, softens the upper mids and rolls the top gently. Pan has its source maximizer bypassed and dedicated headroom. Keys and pads leave room for bass and melody; the atmosphere is high-passed and intentionally quiet. Group levels are measured before mastering. Native glue uses a gentle 1.35:1 ratio, 25 ms attack and 150 ms release; album gain targets approximately -20 LUFS with a -2 dB native peak guard. Final decoded WAV/OGG checks verify actual loudness, true peak, finite samples, DC and mono behaviour. A short fade affects only the declared post-performance tail.

The editable native composition and printed review audio are distinct artifacts. These tests are full songs, with developed returns and endings, rather than production loop exports. Runtime loop seams, family-voice integration, M11 playback, child listening and owner acceptance remain later evidence lanes. `MA-AUDIO-001` retains its existing state.

The implementation uses the documented [REAPER ReaScript API](https://www.reaper.fm/sdk/reascript/reascripthelp.html), including native project snapshots, track/FX/MIDI control and rendering. The guarded authoring stages and measurement receipts are reproducible through the project's test workflow; default full-arrangement construction remains blocked until its review condition is met.


## Original-draft mix review — 2026-11-02

The owner requested comparison with the original drafts to preserve melody/background hierarchy. Three level-matched 20-second comparisons contain ten seconds of the original theme draft followed by ten seconds of the new refrain. Source scores identify Opera pan, Sky flute and Castle Sunbird as the principal themes; the call sheets identify the written foreground handoffs. Model listening supported melodic audibility but is bounded and advisory: its Sky instrument list incorrectly mentioned pan, which is absent from the new score. Castle receives +1.2 dB foreground, -1.5 dB chord backing and -0.5 dB bass relative to its first test balance, with loudness and peaks rechecked after native re-render. The reproducible cue-plan adjustment preserves the source MIDI and instrument EQ.
