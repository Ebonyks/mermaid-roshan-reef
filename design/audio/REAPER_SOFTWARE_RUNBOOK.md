# REAPER software and production runbook

Status: `SUPPORTING_CURRENT`, operational companion to the
[authoring workflow](REAPER_MUSIC_PRODUCTION_WORKFLOW.md).
Observed software baseline: 2026-09-20. Versions below record the tested machine;
they are not permanent minimum versions or instructions to update a working rig.
New plugins join through the onboarding procedure below. Game delivery authority
remains with the music bible and design language, not this runbook.

## 1. Software responsibilities and known baseline

| Software | Observed version / role | Operational boundary |
|---|---|---|
| REAPER x64 | 7.80; recording, arrangement, MIDI, automation, FX, rendering | Authoritative musical timeline is the selected RPP, not an analysis file. |
| Embedded Lua / ReaScript | Supplied by REAPER | Preferred project editing interface; external Python does not need REAPER's Python integration enabled. |
| Python audio environment | 3.13.14; NumPy 2.5.3, SciPy 1.18.1, SoundFile 0.14.0, librosa 1.0.0 | Inspect renders, extract review clips, measure and maintain manifests. Detection is evidence, not automatic musical correction. |
| Kontakt 8 VST3 | 8.13.1; Player-compatible Shreddage libraries | Host, library activation, loaded patch and output routing are four separate checks. |
| Melodyne 5 VST3 | 5.3.1.18; vocal pitch/phrase inspection and selective correction | ARA integration is available; unrestricted scripted note editing is not verified. |
| sforzando VST3 | 2.1.2.3; SFZ instruments | Working alternative for compatible sample instruments, not an arbitrary Kontakt-file loader. |
| MT-PowerDrumKit | Version must be recorded on next onboarding check | v89 uses an audible safety print; a plugin entry alone does not prove a successful render. |
| REAPER stock FX | ReaEQ, ReaComp, ReaVerbate, ReaSamplOmatic5000 and JSFX | Record actual enabled chain, parameters and envelopes; plugin presence does not imply use. |
| FFmpeg / ffprobe | 8.1.2 | Encoding, loudness/true-peak inspection and metadata; preserve the approved lossless source. |
| music-perception-mcp + local adapter | Upstream commit `b7e8cc2d2011269972e2ca6f311fd7f3da9289f3` | Measurements and bounded Google listening reviews, never sole acceptance authority. |

Keep a per-host environment lock and a per-cue plugin inventory. The existing
Python lock is `requirements-local.lock.txt` in the local MCP installation.
Do not upgrade the DAW, Kontakt, libraries and analysis stack together while
trying to diagnose a musical regression.

### Current Windows locations (machine-specific evidence)

- REAPER: `C:\Program Files\REAPER (x64)\reaper.exe`.
- Kontakt: `C:\Program Files\Common Files\VST3\Native Instruments\Kontakt 8.vst3`.
- Melodyne: `C:\Program Files\Common Files\VST3\Celemony\Melodyne\Melodyne.vst3`.
- sforzando: `C:\Program Files\Common Files\VST3\sforzando.vst3\Contents\x86_64-win\sforzando.vst3`.
- Audio tools: `C:\Users\Peter\Documents\REAPER Media\tools\music-perception-mcp`;
  Python is its `.venv\Scripts\python.exe`.
- FFmpeg directory: `C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin`.
- The tested render resource configuration is
  `C:\Users\Peter\Documents\REAPER Media\free-instrument-trial\host\reaper.ini`.

On another machine resolve these afresh. Keep sample libraries in their own
content directory with all required resources together. They do not belong in
the VST3 binary directory. Register/locate supported Kontakt libraries through
Native Access; copying a `.nicnt` file is not activation. For SFZ, preserve the
relative paths between the `.sfz` definition and its sample files.

## 2. Begin a session without losing the selected version

1. Complete the [cue worksheet](../templates/MUSIC_CUE_WORKSHEET.md). Record the
   selected RPP hash, source media, tempo map, phrase anchors and owner direction.
2. Identify the live REAPER instance, resource directory, open project path/GUID
   and dirty state. Preserve unsaved work separately. Do not overwrite an older
   live tab with a saved candidate silently.
3. Create a candidate RPP with a new revision and render directory. Protect source
   recordings; edit item/take settings, MIDI and automation non-destructively.
4. Read enabled FX, instruments, sends, mute/solo states, master FX and render
   bounds. Decide which tracks use live instruments and which use safety prints.
5. Produce an unchanged baseline render before modifying the candidate. Match it
   against the selected master; investigate missing audio or changed tone first.

For v89, the selected source is `Iko iko - production v89 soundstage.rpp`.
The rejected v90 is not the next starting point. A project visibly open in REAPER
may still be a different revision; filename alone is insufficient evidence.

## 3. Add any new VST or library through the same acceptance procedure

Copy [VST_INSTRUMENT_PROFILE.json](../templates/VST_INSTRUMENT_PROFILE.json)
for each instrument/effect role. Keep one profile per distinct library/patch
and signal chain even when several roles share Kontakt. Nulls mean unverified.

1. Record vendor, official source, license/activation requirements, download and
   installed size, host compatibility, binary format and exact version. Record
   library version separately. Never include serials, credentials or installers
   in a public project package. Do not redistribute sample libraries.
2. Install to a canonical x64 plugin location; register the content directory
   through the vendor's supported mechanism. Verify the standalone and REAPER
   instances refer to the intended version. Re-scan only when necessary; save
   first and avoid deleting working duplicates until their use is understood.
3. Add the instrument on a temporary REAPER track. Check its actual FX identity,
   patch title, activation state, sample availability, MIDI channel and audio
   outputs. A Native Access “Installed” badge is not an audible playback test.
4. Create a short MIDI test covering sustained notes, short notes, two velocities,
   repeated notes, a simple chord where appropriate, release tails, and required
   articulations. Stay inside the documented playable range. Keep keyswitches
   separate from playable notes and verify MIDI note numbers, not octave labels.
5. Render the test dry, then through the proposed effects. Listen in solo and in
   the cue. Check silence, stuck notes, missing samples, attack, release, stereo
   routing and unwanted automatic strumming/arpeggiation. Repeat after save/reopen.
6. Test a short background render using the production resource profile. If it
   fails while interactive playback succeeds, keep the previous working source
   or an approved print; investigate the difference before replacement.
7. Save the verified profile, test MIDI/audio hashes and reusable track template.
   Record exposed automation parameter identifiers and units/ranges; parameter
   indexes can change after an update. Keep a print and original MIDI for recall.
8. Relevel in context. Compare at similar perceived loudness; a louder plugin is
   not automatically better. Check CPU/RAM and available sample-disk space.

State progression: `unverified` → `loaded` → `audible_test_passed` →
`reopen_render_passed` → `accepted_in_cue`. A failure returns the role to its last
verified source. New instruments expand the palette; they do not automatically
replace accepted parts in every song.

### Existing Iko iko roles and limitations

| Role | Source and processing to preserve/inspect | Known limitation |
|---|---|---|
| Guitar | Shreddage 3 Stratus FREE in Kontakt; ReaEQ, JS gain, amp model and `guitar_space_v83.jsfx` | Obsolete Hydra is not the intended source. Confirm active patch and section automation. |
| Bass | Shreddage 3 Precision FREE in Kontakt; `precision_definition_v83.jsfx`, gain and amp model | Sampled bass and metal amp tone are separate; confirm playable range and note lengths before adding distortion. |
| Banjolele | sforzando/SFZ path, ReaEQ and `banjolele_blast_tone.jsfx` | Older RS5K fallbacks remain in the project; inspect bypass/mute rather than enabling all sources. |
| Jug / washboard | ReaSamplOmatic5000 sample instruments | Record mapping, source rights, pitch and envelopes. |
| Drums | Audible MT-Power safety print | Original MIDI/plugin track is muted. Repair and verify its render before changing drum MIDI or replacing the print. Never double both sources accidentally. |
| Room / vocal warmth | Stock effects and cue-specific JSFX | Preserve JSFX source/hash; these are custom assets, not universally installed stock presets. |

Existing custom JSFX names include `banjolele_blast_tone`, `guitar_space_v83`,
`polish_shelf`, `precision_definition_v83`, `short_stage_v89` and
`verse_vocal_warmth`, under `Effects/IkoIko/`. Check the resource directory used
by the rendering instance as well as the interactive instance.

## 4. Record, align and edit performances

Record voice and acoustic instruments as separate preserved sources where
possible. Establish input gain without unwanted recording overload, a short
room-tone sample, count-in/reference and phrase markers. Note microphone,
distance and room changes. Irregular noise, plosives and reverberant masking can
require another take; EQ cannot reconstruct missing performance information.

Use the accompaniment and repeated lyric phrases as timing references. Annotate
actual syllable onsets and strum transients on the rendered timeline. Compare
corresponding phrases before editing; allow pickups, offbeats, swing and breath.
Do not infer a global one-beat shift from a single onset detector. Repair only
clear outliers with a bounded item shift or selective stretch marker. A rejected
stretch must be removed, not compensated by more stretching. Re-audition with
both neighboring phrases and their transitions.

For MIDI, program playable register, voicing, note lengths, velocities and
articulations before tone processing. A sample library cannot make an impossible
voicing or perpetual short high notes sound like natural rhythm guitar. Preserve
source MIDI and compare chordal, rhythmic and melodic options in the full mix.

## 5. Melodyne and recorded-track processing

Use Melodyne **VST3 with ARA as the first track insert**, before EQ/compression.
REAPER saves ARA state with the project; verify the actual instance has analyzed
the intended item and that saving/reopening preserves the edit. See
[Celemony's REAPER setup](https://helpcenter.celemony.com/M5/doc/melodyneEssential5/en/M5tour_ReaperARA_InsertVorbereitungen?env=reaper).

Listen dry first. In Melodyne verify detected notes and choose the appropriate
algorithm, then correct clearly unintended pitch centers or isolated timing
errors. Preserve slides, consonants and expressive drift. Do not force growls
onto pitched notes or globally quantize a performance as a cleanup shortcut.
Print a candidate and compare against bypassed audio at matched loudness.

ReaScript can manage FX hosting, exposed parameters, items and rendering. This
workflow has **no verified public Melodyne note-edit scripting interface**.
Do not report “Melodyne corrected” merely because an instance was inserted.
When note editing requires its UI and the owner requests scripts only, document
that pending operation and continue other independent work. Never substitute an
unannounced pitch algorithm and label it Melodyne. Avoid importing Melodyne's
tempo into the project during diagnosis: it can change the timeline being tested.

A starting recorded-vocal chain after correction is corrective ReaEQ → gentle
ReaComp → selective de-essing if needed → subtle warmth → level automation →
room send. Set it from the recording, not a fixed template: remove rumble without
thinning fundamentals, reduce harsh bands only where heard, use compression to
control peaks while preserving consonants, and avoid a gate that eats syllables.
For uke/banjolele masking, compare their verse parts together and make small
complementary EQ/arrangement changes; a chorus fix does not repair verse overlap.

## 6. Section-specific amps, pedals and soundstage

Keep an instrument's MIDI/source separate from its amp/cabinet/effects choices.
For folk sections use a clean or lightly colored path, suitable chord voicing,
controlled pick attack and a short shared room. For heavy sections compare a
high-gain amp **with cabinet filtering** at matched loudness; distortion without
appropriate filtering can exaggerate synthetic fizz. On bass preserve a defined
low foundation and audition a parallel driven midrange path where useful.
Check latency/phase when combining parallel paths and avoid doubling the clean
signal through two unintended routes.

Use verified wet/bypass or routing envelopes for section changes. Label the
transition anchors; avoid clicks, abrupt level leaps and leftover reverb tails
masking a return. Print tests across each boundary, not just inside the section.
Do not hard-code Iko's distortion timing into the reusable template.

Assign center anchors and deliberate pan/depth positions. Use short shared room
sends rather than a long independent reverb on every track. Check mono, headphones
and a small speaker. Keep drums transient and audible under distorted layers;
turning up every instrument defeats this. Let different instruments briefly
carry focus through automation. The final mix is approved in context, not by
isolated preset demonstrations.

## 7. Scripted changes and background rendering

Use Lua for project-aware edits. Relevant APIs include `EnumProjects`,
`IsProjectDirty`, `GetResourcePath`, `GetTrackGUID`, `TrackFX_GetFXName`,
`TrackFX_GetEnabled`, `TrackFX_GetParamFromIdent`, `GetFXEnvelope`,
`InsertEnvelopePoint`, `Envelope_SortPoints`, and the MIDI item APIs.
Use undo blocks for edits and save an explicit candidate. Validate signatures
against the installed version's [official ReaScript API](https://www.reaper.fm/sdk/reascript/reascripthelp.html).

The old local `worker-resume.lua` shared `task.lua` polling queue is **not a safe
reusable runner**: multiple instances can consume it and modal dialogs can block
it. A future runner must bind project path/GUID, instance/resource profile,
request ID and expected source hash, reject stale requests, and return a matching
result ID. It is planned tooling, not implemented by this documentation.

Prefer ReaScript over raw RPP rewriting. Offline edits, if necessary, operate on
saved copies and preserve opaque VST/ARA chunks, take offsets/loops, MIDI event
deltas, tempo, markers and envelopes. Never treat an RPP as arbitrary flat text.

The following launch pattern has been used successfully on this machine. Supply
validated absolute paths for `$resourceConfig` and `$candidateProject` first:

```powershell
$renderProcess = Start-Process `
  -FilePath 'C:\Program Files\REAPER (x64)\reaper.exe' `
  -ArgumentList @(
    '-newinst', '-noactivate', '-nosplash', '-ignoreerrors',
    '-cfgfile', ('"' + $resourceConfig + '"'),
    '-renderproject', ('"' + $candidateProject + '"')
  ) -WindowStyle Hidden -PassThru
$renderProcess.Id
```

Before launching, the candidate must contain a unique, nonexistent output path,
explicit bounds/format and the intended master chain. Prevent overwrite dialogs.
`-ignoreerrors` is not evidence of a successful render. Monitor only the process
you launched, check completion/file finalization, then decode the result and
verify sample rate, channel count, duration, finite samples, peaks and non-silent
expected sections. Do not kill the owner's REAPER process. Keep waits bounded
and report a stuck job instead of launching overlapping retries.

## 8. Measurement and Google listening loop

Use SoundFile/NumPy for decoded sample checks, SciPy for spectral comparisons,
librosa for candidate onsets/pitch and FFmpeg `ebur128=peak=true` for loudness.
Measure the actual output, not just project settings. A whole-song BPM/key
estimate is not authority over a tempo map or unpitched vocals.

The local MCP integration has an upstream server plus a modified
`cloud_enabled.py` adapter. Preserve the upstream commit, adapter hash and local
package lock independently. Upstream installation alone does not guarantee the
same bounded behavior. Current adapter configuration uses `gemini-3.6-flash`
with google-genai 2.24.0; verify model availability before a future session.
ROSVOT is disabled; monophonic transcription uses the available local fallback.

Available calls in the current integration:

```text
perception_info({})
analyze_audio({path: absolute_clip_path})
measure_loudness({path: absolute_clip_path})
transcribe_melody({path: absolute_clip_path, bpm: known_bpm,
                  start_seconds: 0, max_seconds: clip_length,
                  min_note_ms: chosen_minimum, quantize_beats: 0})
listen_subjective({path: absolute_clip_path, question: focused_question})
```

`transcribe_melody` is a monophonic diagnostic, not reliable full-mix notation.
Check returned tool schemas before invoking them after an upgrade.

1. Verify the service with `perception_info`; test local analysis on a known clip.
   Keep Google credentials in the approved local secret mechanism, never in RPPs,
   commands, prompts, logs, manifests or Git. Do not copy credential files.
2. Obtain project-specific cloud authorization. Iko's allowance does not authorize
   uploading other family recordings. Record actual call counts and scope.
3. Export a focused clip with useful context, normally at most 20 seconds. Record
   source render hash, exact start/duration, clip hash and revision. The present
   adapter sends only the **first 20 seconds** as inline PCM16 WAV with a 60-second
   request timeout; a whole-song path will not yield a whole-song review.
4. Ask one answerable question: identify lyric/pulse mismatch, instrument masking,
   harsh syllables, bass attack, or transition continuity. Ask for clip-relative
   timestamps, uncertainty and concrete observations. Do not request a generic
   release score and treat it as a measurement.
5. Convert returned timestamps to song time using the logged offset. Verify each
   finding against audio/measurements and owner-approved musical intent. Reject
   hallucinated instruments, timestamps outside the clip and generic advice.
6. Change one bounded hypothesis, render again with identical bounds and compare
   at matched loudness. Alternate comparison order where possible. Log accepted,
   rejected or inconclusive results and retain rollback artifacts.
7. Stop a line of edits when it regresses, repeats unsupported claims, or needs a
   new recording/plugin/owner judgment. More calls do not establish correctness.
   Final human selection remains separate from model recommendations.

For a new installation pin upstream, restore a tested local dependency lock,
verify the adapter's actual clip/time limits and error redaction, run offline
checks, then one authorized cloud test before a batch. Never assume those limits
from the upstream repository name alone.

## 9. Render, archive and game handoff

Keep selected RPP, original MIDI, authorized source media, plugin profiles,
custom JSFX, tempo/markers, stems, lossless master, review results and a hash
manifest. Print indispensable proprietary instruments for future recall while
retaining editable MIDI and library requirements. A collected RPP without the
required libraries is not a fully reproducible software environment.

Separate private source archives from approved public masters. Exclude credentials,
serials, commercial sample content and unapproved original recordings. v89's
public release contains finished masters; publication of its collected original
recordings remains a separate decision.

For game delivery derive 48 kHz stereo Ogg Vorbis from the accepted lossless
master, at least 64 kbps, with explicit loop metadata, integer-bar duration and
exact loop boundaries. Test seams
across repeated wraps, dialogue ducking, mono, sound-off/return behavior and the
target device. Update provenance, the all-audio ledger and audit evidence.
The existing synthesis-based rebuild checker still needs an implemented external
DAW ingestion lane; this runbook does not claim that integration already exists.
Report source-production completion, machine checks and outstanding listening/
child/device acceptance separately. Do not use a model's numerical rating as a
release gate.
