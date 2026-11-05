# RetroPlug / LSDJ Game Boy writing desk

Status: **Installed; native REAPER hosting and saved-project recall verified.** Ember King chiptune is owner-directed. A finished melody, arrangement and final tone are still to be designed and heard.

## Owner direction and scope

On 2026-11-01 the owner requested RetroPlug installation for the newly downloaded LSDJ, assigned chiptune as the Ember King theme, and explicitly called this an exception to the UVI-only rule. The [source capture](retroplug_owner_direction_20261101.json) records both messages. The general UVI/Sunbird instrument family continues for the other band roles.

This is the Game Boy/chiptune lane of the [producer reference matrix](ENSEMBLE_DESIGN_GUIDE_2026-11-01.md). Condard is the practical reference, particularly **boombox.sav** and **new_saga.sav**. [Artist recordings and production notes](https://condard.bandcamp.com/album/goes-hard-vol-4-harder-not-smarter-instrumentals)

The genre assignment belongs to the **Ember King character theme**. It does not automatically replace the current Ember approach/dungeon cues or change gameplay. Hook, form, tempo, section roles and instrument settings still get a proposed cue plan before construction. The demo freeze remains in force.

## Installed tools and integrity

- **RetroPlug 0.7.4, Windows x86-64 VST3**, from the [official release](https://github.com/tommitytom/RetroPlug/releases/tag/v0.7.4).
- **retroplug-cli 0.7.4**, from the same release, for background ROM checks and future printing.
- **LSDJ 9.4.2 stable**, from the owner's existing `lsdj9_4_2-stable.zip`; no replacement download or ROM modification.

Both RetroPlug archives matched the SHA-256 digests in GitHub's official release metadata before extraction. The installed module and original/extracted LSDJ hashes are recorded in the [installation evidence](retroplug_installation_20261101.json). Software, ROM, licence files, native snapshots and SRAM remain in the private local tool/project folders. The downloaded LSDJ licence states personal/educational use and prohibits software redistribution.

The VST3 bundle is at `%LOCALAPPDATA%/Programs/Common/VST3/RetroPlug.vst3`, a folder already included in the user's REAPER scan paths. The CLI and licences are under `%LOCALAPPDATA%/Programs/RetroPlug/v0.7.4/`. User audio settings were preserved.

## Editable starter session

Private owner folder:

`Documents/REAPER Media/Mermaid Roshan Soundtrack 20261031/Game Boy Tools 20261101/`

Open **Ember King - LSDJ.RPP**. It contains one live RetroPlug source and four stereo returns:

| Return | Proposed musical job |
|---|---|
| Pulse 1 | Clear principal hook with shaped envelopes and selected ornaments. |
| Pulse 2 | Answer, counterline or compact arpeggiated harmony; full rests when useful. |
| Wave | Identifiable low figure and body; audition waveform/touch before selecting a bass. |
| Noise | Rhythmic punctuation and section accents, with deliberate density changes. |

These jobs are proposed arranging choices. The song itself is blank. The four returns allow separate EQ, level and effects choices once actual performances exist. Source main-send is disabled to avoid a duplicated mix; the four returns begin at conservative gain. No EQ/mastering quality is claimed for an empty writing desk.

The folder also holds **Ember King - LSDJ.rplg.zip**, which references the private ROM, and the preserved LSDJ licence/ROM. Open the source track's RetroPlug FX to edit the tracker. Keep editable LSDJ song/save exports and versioned REAPER projects alongside future printed stems.

The writing desk is 48 kHz with a **104 BPM placeholder**, inherited from the existing Ember-area cue. It is not an accepted tempo for the new character theme. Native state currently uses **CGB-C / accurate high-pass**. Hardware-model tone comparisons belong to the focused audition. RetroPlug reports MIDI-sync mode with auto-start off; set and verify the LSDJ song's clock mode/arming before synchronized song renders.

## Verified readiness and remaining work

An isolated REAPER **7.80/x64** profile using Dummy Audio discovered and instantiated `VST3i: RetroPlug (tommitytom) (8 out)`. Native save contained the correct LSDJ ROM reference, Game Boy savestate and SRAM. A separate REAPER process, launched **without** the setup autoload variable, reopened the saved project and restored its ROM/native state, channel-split setting and all four correct source-channel pairs.

The background CLI identified `LSDJ-V9.4.2` and completed a two-second blank-ROM boot render. This checks loading; it is not an authored song, articulation audition or transport-sync test. The [reusable Lua setup helper](https://github.com/Ebonyks/mermaid-roshan-reef/blob/codex/music-full-arrangements-20261101/tools/reaper/setup_retroplug.lua) guards its isolated profile, protects nonempty projects and saves a native writing desk. All software/ROM paths are supplied through an ignored local request file.

Next musical work is a focused pulse/wave/noise and model audition, then the Ember King hook and section plan for review. After notes exist, verify clock start/stop, timing, four-stem rendering, EQ/balance/master headroom, saved-song recall and the normal human/voice/mono/phone/child gates. Installation and genre authorization do not accept music or a runtime replacement.
