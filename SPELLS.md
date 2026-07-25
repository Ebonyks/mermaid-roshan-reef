# MAGIC WORDS — spoken spells

Roshan casts a spell when the child **shouts the word into the phone's
microphone**. The first (and so far only) spell is **FREEZE**: a short frost
cone puffs out in front of her and every enemy standing in it freezes solid.

Owner-facing summary: it is **off by default**, it lives behind a pause-menu
toggle, nothing is recorded or sent anywhere, and the game is 100% completable
without ever switching it on.

| | |
|---|---|
| Engine | `scripts/voice_spells.gd` (`VoiceSpells`, Phase 7 satellite) |
| State | on `main` — `spells_pref`, `spells_on`, `spells_forgiving`, `spell_*` |
| Arena hook | `CombatArena.cast_freeze()` in `scripts/combat_arena.gd` |
| Toggle | pause menu → **Magic Words: On / Off** |
| Saved as | `reef_save.json` key `spells` (bool, defaults `false`) |
| Probe | `scripts/probe_spells.gd` (in `ci.sh` and the probes workflow) |

## What the matcher really is — read this before tuning it

Godot ships no speech recogniser, and the game has to work offline on a
three-year-old Android phone. So this is **not speech-to-text**. It is a shout
detector plus a coarse word-*shape* check, in three stages:

1. **Loudness gate.** The utterance must sit `TRIGGER_MARGIN_DB` (14 dB) above
   the room's tracked noise floor *and* above an absolute `SHOUT_MIN_DB`
   (−30 dB). The floor follows the room fast downward and slowly upward, so a
   noisy playroom raises the bar rather than casting spells by itself.
2. **Duration gate.** `MIN_WORD_SEC` 0.20 s to `MAX_WORD_SEC` 2.0 s. A clap is
   too short; a sung verse is too long. A held "FREEEEEZE" closes at the cap
   and still counts.
3. **Shape score.** "Freeze" is /f r/ → /iː/ → /z/: **hiss at both ends with a
   voiced vowel in the middle**. Three one-pole filters split each 20 ms frame
   into low (<400 Hz) / mid / high (>1800 Hz) energy, the utterance is cut into
   three equal slices, and the slices are matched against the profile in
   `SPELLS`. The decisive term is `min(first.high, last.high) − middle.high`.

Two mistakes are already baked into the tests because both actually happened:

* the release-hold frames at the end of an utterance are **silence**, and room
  tone is broadband — leaving them in the feature list made every vowel look
  like it ended on a /z/, and "aaaah" scored as high as "freeze";
* averaging the two edges instead of taking the **weaker** one let "GO!"
  through on the strength of its plosive onset alone.

### Forgiving mode (`m.spells_forgiving`, default **on**)

Hard rule: no fail states. In forgiving mode a loud, word-length shout casts
the one spell she knows **even when the shape score misses** — a 4yo's
"FEEEZ!" has to work. The shape score's real job is deciding *which* spell once
there is more than one. Turning forgiveness off (as the probe does) isolates
the matcher: then only a genuinely freeze-shaped utterance casts.

Nothing in the game is ever gated behind being heard. The ICE button does the
same job, always.

## Feel

* **Cone:** 15 m long, 34° half-angle, plus a 2.5 m point-blank bubble so an
  imp right on top of her always counts. The dragon-turtle is a bigger target
  and counts from 19 m / 6 m.
* **Recharge:** 6 s (`SPELL_COOL`). The spell is a special move *beside* the
  ICE button, never a replacement for it — and a shout while it recharges gets
  an answer out loud, never silence.
* **Frozen** enemies enter exactly the same state the ICE berry produces, so
  the popcorn finish and the win check are unchanged.
* **Missing costs nothing** but the recharge, and she gets a "turn toward the
  golden arrow" hint instead of a telling-off.
* **Retrigger lockout:** 0.75 s, *and* the signal must actually fall quiet
  again before a new utterance can start — otherwise one long scream (or a
  vacuum cleaner) machine-guns the spell.

## Non-reader affordances

* A pulsing **🗣 ❄** bubble at the top of the screen whenever the mic is
  listening, with a live loudness worm underneath: she can *see* the phone
  hearing her before any word lands.
* The same icon pair appears in the combat objective banner, hollowed to
  `🗣 ❄(…)` while the spell recharges.
* Every cast fires a voice line through `_say`/`show_msg`. Drop a real family
  recording at `assets/audio/voices/roshan_freeze.ogg` and it plays
  automatically — no code change (see `AudioDirector._say`).

## Privacy and permissions

* `audio/driver/enable_input=true` in `project.godot` only *allows* an input
  device to be opened. The microphone stream is `play()`ed solely inside
  `VoiceSpells._open_mic()`, which runs only after the pause-menu toggle. A
  family that never switches Magic Words on never sees a permission dialog or
  a mic indicator.
* Android: `permissions/record_audio=true` in `export_presets.cfg`; the runtime
  grant is requested on first enable via `OS.request_permission`.
* The `Mic` bus is created **muted** at −80 dB — the effect still sees the
  signal, but the phone never plays the child's own voice back at her.
* Samples are read into a loudness/band envelope and dropped. Nothing is
  buffered to disk, nothing leaves the device, and no audio is stored in the
  save file. The only persisted value is the on/off preference.
* If the mic cannot be opened this session, the saved *preference* is kept
  (`spells_pref`), so a temporary denial never quietly erases the family's
  answer.

## Adding the second spell

1. Add an entry to `SPELLS` in `scripts/voice_spells.gd`: an `icon`, a
   three-slice `profile` of (low, mid, high) energy fractions, and `edge_hiss`.
2. Handle the new word in `VoiceSpells._route_cast` (or set
   `cast_handler` from whichever scene owns it).
3. Add probe cases: the new word casts, and it is **not** confused with
   "freeze" with `spells_forgiving = false`.
4. Note that with two or more spells the forgiving fallback stops firing — it
   only applies while exactly one spell exists, because there is no longer an
   unambiguous "the word she meant".

## Tuning on the real phone

`SHOUT_MIN_DB` is the knob. Phone mic gain varies a lot; if she has to scream
to be heard, **lower** it toward −36; if the game casts while she is just
chatting, **raise** it toward −24.
`m.spell_last_score` and `m.spell_last_matched` record how the last shout
scored, for exactly this.
