# REAPER music production workflow

Status: `BINDING_DOMAIN` for the owner's 2026-09-20 authoring direction: use
REAPER, suitable VST instruments/effects, and recorded performances for future
commissioned game music. The production procedure below records lessons from
the separate Iko iko session. It does not replace current delivery gates, approve
an existing song for the game, or commission wholesale replacement of the score.

Start with the [master planning entry](../../audit/MASTER_AUDIT_2026-08-09.md#0-planning-entry),
[design language](../06_COMPREHENSIVE_DESIGN_LANGUAGE.md#10-voice-music-and-non-reader-communication),
[music bible](../../MUSIC_AUDIT_2026-08-09.md), and
[cue worksheet](../templates/MUSIC_CUE_WORKSHEET.md).
The [impact record](../audit_impacts/reaper-music-workflow-20260920.json) bounds
this documentation change; `MA-AUDIO-001` is not closed by it.

For exact software versions, paths, plugin onboarding, Melodyne boundaries,
ReaScript/background rendering and MCP calls, use the
[software runbook](REAPER_SOFTWARE_RUNBOOK.md). Each new VST/library role gets a
[verification profile](../templates/VST_INSTRUMENT_PROFILE.json); the palette is
extensible rather than a fixed shopping list.

## Musical direction before software

Write the cue's purpose, scene owner, emotional arc, motif, meter, tonal center,
approximate duration, and room for dialogue. Choose a small instrumental palette
that belongs to the game's shared musical language. References describe specific
qualities to study, not permission to copy a recording or composition.

REAPER/VST production is the preferred authoring approach for new commissioned
music. Existing generated cues remain working assets until individually replaced
and accepted. Do not treat a richer library as a substitute for composition,
articulation, or listening. Recorded ukulele, other instruments, and voice can
supply the performance that MIDI accompanies; voice is not the only input.

Most cues do not need genre interruptions. The owner identifies the Ember
King/Prince as intended grindcore musicians; develop that character-specific
musical direction in the applicable cue brief, with clear child-facing purpose
and controlled playback level. Do not add blast beats to unrelated scenes or
infer a new boss, plot, or runtime commission from this musical direction.

## Establish one authoritative session

Before editing, identify the active project path, saved revision/hash, REAPER
process/resource directory, dirty state, render source, and latest owner-selected
candidate. A visible old session and a newly rendered saved project are different
states. Never say the live session was updated when only an offline copy changed.

- Preserve original media and the owner's unsaved work. Save a new candidate for
  a bounded change. Use relative media paths inside a collected project package
  where licensing and privacy permit; record external dependencies otherwise.
- Prefer REAPER Lua/ReaScript for project operations and Python for inspection,
  MIDI preparation, audio measurements, manifests, and comparisons. Prefer scripts
  while the owner uses the PC. UI-only operations require an available, authorized
  UI route; do not pretend an unsupported API exists.
- Bind a worker to a specific project identity and unique request/result IDs.
  Inspect the project again immediately before mutation. Do not share an unguarded
  task-file queue between multiple REAPER instances.
- Record process IDs for background renders, capture errors and completion, and
  close only task-owned instances after their work finishes. Never kill the
  owner's session, queue stale mutations, or infer success from a file appearing.
- Keep one current-candidate manifest naming the exact RPP and export hashes.
  On rejection, restore both manifest and listening exports from the selected
  revision. Keep the rejected experiment as history, not current authority.

## Prove the instrument chain before arranging

Record the plugin name, format, version, ID, resource path, library/preset,
license requirement, MIDI channel, note range, keyswitches, output pair and FX
chain. Use one known installation and one intended active source per part.

Kontakt is the sampler host; a Kontakt library is not a standalone VST. A library
appearing in Native Access or the browser does not prove the REAPER instance can
play it. Match the actual loaded plugin and its resource paths. Check whether the
library supports Player or needs full Kontakt. Free libraries can still need
registration/activation; copying a NICNT is not proof of entitlement or a repair
for activation. Do not remove shared installations or libraries as a first guess.

Load one instrument, play known in-range notes at representative velocities, and
render a short test. Verify nonzero audio, correct channel, timbre, articulations,
release, and missing-resource/activation state. Test in musical context before
rewriting a complete part. A silent plugin can masquerade as a mixing problem.

Choose articulations and phrasing before adding effects. Sampled guitar/bass may
need an amp and cabinet, but some presets already include them: avoid accidental
double amplification/cabinet processing. Compare clean, edge-of-breakup and heavy
chains at matched loudness. Genre-specific tone changes belong in explicit
section automation, not an undocumented permanent change to every verse.

Use an authorized SFZ or printed-stem fallback when necessary. A safety print must
match the intended MIDI, timing, processing and revision. Mute the live source
when the print is active. Document that the print makes playback reliable but does
not fix an unresponsive instrument or make later MIDI edits audible automatically.

## Recording and rhythm: protect the performance

Preserve raw takes. Record sample rate, source offsets, take versions and gain;
check noise, overload, room sound and instrument tuning before building layers.
Listen to exposed recordings and in context. Request a retake only for a specific
unrepairable problem; do not substitute a stock sound for an irreplaceable family
performance without authorization. Protected game voices retain their original
bytes and their separate `DL-SND-05` / `DL-SND-11` rules.

Do not assume a recording follows the DAW's default BPM. Establish downbeats,
pickups, swing/offbeats, phrase lengths and chord changes from the performance.
Use a tempo map where needed and make accompaniment follow the intended groove.
For vocals, compare consonant pickup and stressed vowel placement; not every
waveform onset belongs on a beat. Compare repeated phrases before moving a line.

For selective timing repair:

1. Identify a timestamped audible mismatch in the full mix and relevant stems.
2. Confirm the reference beat/lyric against neighboring and repeated phrases.
3. Record the proposed local shift and an intentionally generous tolerance.
   A 70–90 ms detector outlier was only a screening candidate in Iko iko, not a
   universal threshold or automatic correction rule.
4. Move only the faulty attack/word with suitable crossfades or bounded stretch
   anchors; preserve surrounding phrase boundaries and natural timing variation.
5. Compare before/after in context. Reject clicks, missing consonants, flutter,
   robotic repetition, unnatural speed changes, or weakened groove.

Raw source slicing must account for looped takes, offsets, rates, stretch markers,
take FX and ARA. When those alter playback, analyze an actual rendered stem.
Onset detection is evidence of energy changes, not a transcription of rhythm.
Never blanket-quantize a performance to satisfy a detector or an uncertain model.

Melodyne can support selective pitched-vocal correction in the REAPER session.
Verify its actual integration and rendered result. This session did not establish
a general note-editing scripting API; do not claim automation of note edits that
was not performed. Keep uncertain or UI-only edits explicit. Unpitched growls
must not be forced into melodic correction by default.

## Arrange in phrases, then mix

Make the entrance purposeful: a short pickup, immediate vocal, or a brief staged
build. Avoid a long waiting period simply because MIDI starts before the recording.
A longer later verse should develop through answers, register changes, omissions,
articulation, dynamics and instrumental exchanges, not constant added density.
Actual call-and-response leaves a response window; doubling over a lead is harmony.

Keep important instruments quieter under words and let them step forward in gaps.
Audition instruments with the ensemble: an impressive solo tone can be wrong in
context. Version small changes and keep the owner's successful choices locked
unless a new specific defect or request justifies reopening them.

Use gain and arrangement first, then targeted EQ/compression. Locate masking in
its actual section before adjusting it. Gentle expansion, automation, editing or
filtering can address floor/room noise; hard gates can cut syllables and tails.
Avoid piling on de-essing or noise reduction after inconsistent reviews. Document
remaining recording limitations instead of claiming that processing restores
missing source quality.

Give parts stable positions: lead/low-frequency/rhythmic anchors near center,
complementary instruments on opposing sides, restrained short room depth and
controlled tails. Match the visual/narrative purpose rather than copying fixed
pan percentages. Check mono and small speakers; no cue identity may depend only
on stereo width. Keep transient-heavy passages clear by reducing ambience when
appropriate. Artistic saturation can belong in a source tone; it does not waive
the game's output-peak and dialogue-intelligibility requirements.

## Bounded review, revision and acceptance

For each iteration, record observation -> hypothesis -> smallest musical edit ->
render -> comparison -> accept/reject. Retain the exact baseline and candidate.
Use the same excerpt boundaries and comparable loudness. Counterbalance A/B order
when a reviewer is sensitive to presentation order. Review transitions with context
on both sides, then the complete cue; isolated stems alone cannot prove a mix.

Google/Gemini music-perception MCP can supplement human audition. Send only audio
within the owner's authorized scope; a permission/budget for Iko iko is not a
blanket permission to upload new game/family recordings. Keep credentials out of
the repo, logs and prompts. No browser cookie export is part of music production.
Record submitted clip/hash, song offset, question, model/backend, response and
call count. This installed listener processes at most the first 20 seconds, so
explicitly crop later sections. Verify current tool limits rather than assuming
that a whole-song filename means whole-song analysis.

Exclude silent, wrong-version, clipped diagnostic or truncated inputs from musical
judgments. Models have hallucinated instruments in silent/muted tracks, contradicted
A/B comparisons and called intentional distortion clipping. Check those claims
against the actual signal. More calls are useful only when they test a new, bounded
question; a large call count or a 4.8/5 rating does not establish acceptance.

Separate three results: musical edits implemented, machine checks passed, and
human/game-context acceptance. When the owner chooses a checkpoint, stop speculative
polishing of it. An explicit later rejection wins over an earlier model endorsement.

## What belongs in the repository

For each commissioned cue, use a stable slug under
`assets_src/audio/music/<cue_slug>/` when the existing source layout permits it.
Keep the worksheet, arrangement/tempo map, MIDI or edit scripts, sanitized RPP,
plugin/library/preset inventory, source provenance, render recipe, review decisions,
and current accepted-candidate manifest together. This is a recommended package
layout, not a claim that a new importer or manifest schema already exists.

Keep these distinctions clear:

| Artifact | Handling |
|---|---|
| RPP, MIDI, Lua/Python edits, notes and manifests | Version-control portable, inspected sources. Record paths/hashes and rendering prerequisites. Inspect opaque plugin state for portability/privacy before publishing; do not dump it into logs. |
| Raw personal performances and protected family audio | Preserve originals in authorized storage. Only publish within the owner's actual scope; credentials and incidental conversation recordings never belong in source packages. |
| Commercial VSTs, installers, licensed sample libraries, activation state | Keep outside Git. Record dependencies and sample-use rights; installation is not redistribution permission. |
| Freeze stems and lossless masters | Retain versioned, hash-addressed production artifacts in an agreed repository/LFS/artifact location. Do not silently add large binary history or assume a remote exists. |
| Runtime OGG and import metadata | Commit only after cue-specific delivery and license gates, with the runtime manifest and all-audio ledger. |
| Rejected renders and model-call scratch data | Preserve decision evidence; archive bulk scratch outside runtime assets. Never promote it by filename alone. |

Sample libraries may randomize round robins, analog noise or modulation. A saved
RPP is a reproducible production source, not a promise of bit-identical rendering
on every host. Preserve approved freeze stems and a lossless master with hashes,
plus enough source/preset/version information to revise them. Distinguish verifying
a frozen artifact from rebuilding it exactly.

## Bridge into the game: a separate delivery step

The current `tools/build_area_music.py --check` rebuilds declarative synthesized
scores; it does not ingest arbitrary REAPER sessions. Its existing catalog and
provenance claims remain valid for that catalog. Do not label VST recordings as
sample-free synthesis, overwrite generated files that the builder will recreate,
or disable rebuild checks to make an external render pass.

Before integrating the first DAW-authored replacement, implement a bounded external
source lane: distinguish source type, bind a lossless approved render/freeze-stem
hash to the RPP/preset inventory, encode/measure the runtime file, and validate the
proper source type without requiring proprietary plugins in game CI. Preserve
legacy deterministic rebuilds and routing tests. This adapter is future work,
not implemented by this documentation or by the Iko iko experiment.

Current new-area-cue requirements still apply: 48 kHz stereo Ogg Vorbis, integer-bar
24–40-second loop, managed 96 kbps within 80–128 kbps, exact-sample loop/BPM/meter/cue
metadata, -18.5 to -17.5 LUFS-I and at most -3.0 dBTP. An intentional exception
needs explicit scoped authority; a standalone song master is not that authority.
Respect `DL-PERF-05`'s general audio minimum and the stronger music-specific profile.

Audition two loop wraps and codec output, check seams/tails/finite samples/peaks,
compare with accepted game cues at game playback gain, then test voice ducking,
objective intelligibility, music-off, scene ownership/restoration and interruption.
Update `ASSET_LICENSES.md`, per-file audio ledger and cue manifest. Finish with mono,
headphones, speaker and Lenovo Tab M11 listening/performance; applicable older-phone
and child/owner acceptance remain separate. REAPER/VST source approval alone never
changes save/routing behavior or grants release acceptance.

## Iko iko checkpoint and lessons

On 2026-09-20 the owner rejected v90 and selected **v89 soundstage, final for tonight**.
The local song master is 91 seconds at approximately -13.5 LUFS-I/-1.3 dBTP: a standalone
listening master, not compliant game-loop delivery. Its source, media and Google
review logs remain in the separate local REAPER workspace; none is imported here.
The song's composition/recording rights would need a separate decision before any
reuse in the game; this task carries forward production practice only.

What worked: real recordings with sampled accompaniment, verified Kontakt chains,
printed drum fallback, phrase-level arrangement, section-specific tone, restrained
masking control, instrument spotlight automation and stable soundstage placement.
What failed: repeated whole-verse retiming, confusing old live sessions with saved
candidates, treating installation as proof of sound, excessive model-led polishing,
and assuming that a busier arrangement is automatically better. The rejection of
v90 is a concrete reminder: musical taste outranks a successful render or favorable
AI review. Grindcore switching remains an optional arrangement technique.

## Next reusable tooling, in order

1. A project-bound preflight/render runner: inspect live versus saved revision,
   verify plugin audio, use a unique job directory, and retain completion/error
   evidence without leaving orphaned instances or deferred mutations.
2. A versioned source/artifact manifest and comparison helper: collect authorized
   media, pin dependencies, validate stems/master, prepare matched excerpts, and
   promote or roll back one explicit selected candidate.
3. The external-render game-ingestion lane described above, preserving existing
   synthesized-source rebuilds and all delivery/routing checks.
4. Small reusable REAPER track/routing templates, built from verified instruments
   and owned effects. Store roles and settings rather than one rigid genre preset.

These are implementation priorities derived from the session, not tools supplied
or tested by this documentation change. Start with one commissioned game cue to
prove the complete path before replacing other score assets.
