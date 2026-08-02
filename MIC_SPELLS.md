# Spoken spells — microphone input for FREEZE and FIREBALL

**Status: PROTOTYPE, landed 2026-08-02. Toggle defaults ON.**
Owner sign-off is still outstanding on two things: the default, and whether
`RECORD_AUDIO` belongs on a four-year-old's phone at all
(`OPERA_JOB_GIMMICKS_2026-07-25.md` flagged that as the owner's call, not the
agent's). Nothing here is hard to reverse — see **Turning it off** below.

## What it is

Say **"freeze"** or **"fireball"** during a combat arena and the spell casts,
exactly as if the ICE or FIRE button had been tapped. That is all it does. It
adds no objective, no failure, and no requirement: the buttons remain the
primary control and work identically whether the microphone is on, off, denied
or broken.

## What it is not

It is not speech recognition. There is no ASR engine, no model file, no native
binary, no network call, and no audio ever leaves the device or is written to
disk. The full landscape was surveyed before choosing (sherpa-onnx KWS at
~5 MB, Vosk at 40 MB, whisper.cpp tiny at ~31 MB, microWakeWord, Porcupine);
this route was chosen because it adds **zero bytes of dependency** and because
speaker dependence — normally a liability — is an advantage when there is
exactly one player.

## How it works

1. **Front end (free).** A muted `Mic` bus carries an `AudioStreamMicrophone`
   through an `AudioEffectSpectrumAnalyzer`. Godot already runs that FFT in
   C++; `mic_input.gd` only reads 20 mel-spaced magnitudes per frame, logs
   them, and subtracts the per-frame mean (which discards loudness and the
   fixed colouration of this phone and this room).
2. **Endpointing.** A rolling noise floor — up fast, down slow, so it can
   absorb music starting but cannot chase a word — opens a capture when the
   frame is 12 dB above it and closes it after 250 ms below +6 dB. Four frames
   of pre-roll are kept so an /f/ onset is not clipped.
3. **Normalisation.** The utterance is resampled to a fixed 32 frames. This is
   what makes recognition frame-rate independent: the same word captured at
   30 fps on the phone and 60 fps on the desktop produces the same matrix.
   Duration is kept separately as a weak extra cue, so a three-syllable word
   cannot masquerade as a one-syllable one.
4. **Matching.** Banded DTW (Sakoe-Chiba radius 8) against five recorded
   templates per word. About 11k operations per template, ~110k per spoken
   word, and **exactly zero between words**. The cost matrix is allocated once.

Because the template is a time × frequency shape rather than a band-energy
test, it carries syllable count and formant movement — which is why "freeze"
(one syllable) and "fireball" (three) separate despite both opening on /f/.

## The decision rule

Accept only if `best < ACCEPT_DIST` **and** `best < ACCEPT_RATIO × runner_up`.

The ratio does the real work; the distance is a sanity ceiling. That split is
measured, not guessed — `tools/dtw_calib.py` reports:

| sound | distance | ratio |
|---|---|---|
| same word, clean | 0.06 | 0.16–0.18 |
| same word, sloppy delivery | 0.09–0.14 | 0.23–0.50 |
| same word, very noisy | 0.21–0.26 | 0.47–0.55 |
| ambiguous half-word | 0.28–0.30 | 0.65–0.67 |
| room noise | 0.34–0.46 | 0.69–0.90 |

Absolute distance does **not** separate those classes: room noise reaches down
to 0.34 while a genuine noisy word reaches up to 0.26. The ratio does, and it
is scale-invariant, so it survives a different room. Anything that fails either
gate casts nothing at all — silence is always the safe answer, because the
buttons are right there.

## Teaching the spells

The toggle lives in the pause menu (`🎤 SAY SPELLS`). Switching it on with no
spells taught opens a teach overlay: a giant glyph, a spoken prompt, and five
pips that fill in as she says the word. `✔ ALL DONE` is always available and
always safe — a word with two or more templates still works.

Templates live in `user://mic_spells.json`, **never** in `reef_save.json`, so
the save file's compatibility contract is untouched. A corrupt or missing
template file degrades to "no spells taught", never to a crash. Only the `mic`
boolean is added to the save, with a default matching `ReefMain.MIC_DEFAULT_ON`.

Re-teach after a growth spurt, a cold, or a new room: switch the toggle off and
on again.

## Privacy and permission

- The microphone device is opened **on entering a battle** and closed on
  leaving it. Never at boot, never in the reef, never while paused.
- `RECORD_AUDIO` is requested lazily at that same moment, at most twice ever.
  A denied permission sets `mic_permission_denied`, disables the feature
  permanently and silently, and the battle proceeds on buttons.
- Nothing is recorded to disk. The stored templates are 32×20 log-magnitude
  matrices — no audio, and not reconstructible into any.
- `project.godot` sets `audio/driver/enable_input=true`. That only *permits*
  capture; Godot opens the device when an `AudioStreamMicrophone` actually
  plays.

## Turning it off

`ReefMain.MIC_DEFAULT_ON` in `scripts/main.gd` is the single flip point — set
it to `false` and the toggle, the save default and every fresh install ship the
feature dark. To remove the permission from the APK as well, drop
`permissions/record_audio=true` from `export_presets.cfg`.

## Known risks, unverified on device

Nothing below can be settled in CI; all of it needs the phone.

1. **Android audio routing.** On some OEM builds, opening a capture stream
   flips the device into communication routing: output ducks, loses the
   low-latency path, or moves to the earpiece. This is the single biggest risk
   and it would degrade audio game-wide, not just in combat. **Test music and
   voice lines during a battle before promoting to master.**
2. **Speaker feedback.** Game audio re-enters the microphone. Voice lines and
   chimes gate detection off (plus a 250 ms tail), and the noise floor absorbs
   steady music, but a loud SFX during a word may still spoil it.
3. **Threshold realism.** `ACCEPT_DIST`/`ACCEPT_RATIO` are calibrated against
   synthetic words. Real speech is messier. If she is not being heard, watch
   `mic_last_dist` and raise `ACCEPT_RATIO` toward 0.70; if the dishwasher
   casts fireballs, lower it toward 0.50.
4. **Battery.** An open capture stream keeps the audio HAL awake — roughly
   1–3%/hour, but only for the duration of a battle.
5. **Other speakers.** Templates are hers. Anyone else playing needs their own
   enrollment (toggle off, toggle on).

## Testing

    python3 tools/dtw_calib.py          # thresholds still have head-room
    $GODOT --headless -s scripts/probe_mic.gd

`probe_mic.gd` drives the real endpoint-to-verdict path with synthetic
utterances — there is no microphone in CI, but the recogniser itself is under
test, not a stub. Both are wired into `scripts/ci.sh`. The negative half
matters as much as the positive: silence, a too-short blip, room noise, an
ambiguous near-miss and a switched-off toggle must all resolve to no spell.

## Files

| file | role |
|---|---|
| `scripts/mic_input.gd` | the whole engine: capture, endpointing, DTW, enrollment, teach overlay |
| `scripts/combat_arena.gd` | arms/disarms per battle; a spoken word chooses the power |
| `scripts/pause_menu.gd` | the `🎤 SAY SPELLS` tile |
| `scripts/save_state.gd` | the `mic` boolean |
| `scripts/probe_mic.gd` | headless probe |
| `tools/dtw_calib.py` | threshold calibration, also a CI gate |
