# Character voices

## Provisional synthetic filler v1 (2026-08-30)

Runtime now prefers `filler_v1/<speaker>_<event>.ogg`, then the corresponding
legacy path. The 271 live cues comprise all 270 non-Faron authored lines plus
the three-preset `everyone.ogg` mix. This is a reversible machine-screened
layer—not confirmed talent, not human-auditioned, and not
a claimed match to any real person. Faron and the sacred family recordings are
excluded and remain byte-identical.

Filler candidates use Parler-TTS Mini v1.1 with named synthetic presets and
mood-specific descriptions. Each line is rendered with a recorded seed and is
rejected unless local speech recognition preserves every semantic word. Among
eligible takes, the selector ranks DNSMOS signal quality plus pitch and spectral
fit. Delivery mastering is 48 kHz mono Ogg Vorbis at 96 kbps, -16 LUFS ±1 and
no higher than -1.5 dBTP. Exact model revisions, prompts, seeds, raw/final
SHA-256 hashes and measured results live in `filler_v1/FILLER_MANIFEST.json`.

Rebuild in isolated Python 3.11 environments with:

1. `tools/make_parler_voice_trials.py` (one or more attempts)
2. `tools/select_filler_voices.py` (exact-word and objective-quality gate)
3. `tools/master_filler_voices.py` (delivery encode and blocking format gate)

These files are temporary placeholders to replace when consented talent is
confirmed. Do not train or condition them on family recordings.

The game plays `assets/audio/voices/<name>.ogg` when it exists (per-line override
like `gabby_win.ogg` first, then `gabby.ogg`), else falls back to the recorded
"yay" clip pitched per character.

## How these were made (and how to remake them)

All scripted lines are generated with **Kokoro-82M** — a free, Apache-2.0 neural
TTS that runs on CPU — via `tools/make_voices.py`. Each character has a fixed
voice + pitch so they stay recognisable, and Roshan keeps ONE consistent
little-girl voice across every clip. Output is silence-trimmed and normalised to
the project standard (-16 LUFS, -1.5 dBTP).

To change a line or add a new one: edit the `LINES` table in
`tools/make_voices.py` and re-run it (setup instructions in the script header).
Use repeatable `--line <exact_key>` arguments for a bounded replacement; do not
regenerate the whole voice library to repair one line. The delivery limiter
leaves conservative encode headroom so decoded Vorbis stays at or below the
project-wide −1.5 dBTP ceiling.
New `<speaker>_<event>.ogg` names are picked up by the game automatically —
no code changes needed. Events used by the game: `talk`, `win`, `fail`,
plus bespoke ones (`greet`, `intro`, `thanks`, `bark`, `pearl`, `idle1..3`).

## Character voice map

| character | Kokoro voice | pitch | feel |
|---|---|---|---|
| Roshan  | af_heart  | 1.24 | 4-6yo girl (consistency critical) |
| Huluu   | bf_emma   | 1.10 | gentle British princess |
| Evie    | af_bella  | 1.30 | little kid |
| Harper  | af_sarah  | 1.18 | big-sister cheer |
| Faron   | af_nicole | 1.05 | soft, hushed caregiver |
| Gabby   | af_sky    | 1.22 | bubbly sing-song |
| Wacky   | am_santa  | 0.98 | grandpa chuckle |
| Shop    | bm_george | 1.02 | friendly shopkeeper |
| Sparkle | af_bella  | 1.55 | tiny baby-eagle chirp |
| everyone | 3-voice mix | — | group "Hooray!" |

## SACRED — never regenerate these (real family recordings)

- `daddy1.ogg`, `daddy2.ogg`, `daddy3.ogg`
- `chuck.ogg`, `chuck_bark.ogg`, `chuck_whimper.ogg`

The retained legacy `../voice_yay.mp3` is not protected and is no longer live.
All success-chirp playback uses the machine-screened synthetic
`filler_v1/yay.ogg`. `filler_v1/roshan_talk.ogg` owns “This is so much fun!”
with an exact manifest hash and cannot fall back while the filler cohort is
present.

To improve a real recording instead of replacing it, run it through a free
speech enhancer (Adobe Podcast Enhance web tool, or locally: resemble-enhance /
DeepFilterNet), then loudness-match with the same -16 LUFS pipeline.

## 2026-08-24 all-audio quality pass

The measured ledger is
`audit/audio_quality_ledger_2026-08-24.csv`; its deterministic builder is
`tools/audit_audio_quality.py`. The two previously missing live Racer
objectives now have exact Roshan clips:

- `roshan_op_racer_tune_up.ogg` — “Turn the wrench in big circles. Tighten
  every wheel before the race!”
- `roshan_op_racer_to_the_line.ogg` — “Push the kart all the way out to the
  starting line!”

Three unprotected generated clips with the least true-peak headroom were
re-rendered from the same Kokoro model and speaker identity using the safer
limiter: `roshan_op_candymaker_parade.ogg`,
`roshan_op_magician_rope.ogg`, and
`roshan_op_popstar_mic_chase.ogg`. Protected Daddy/Chuck recordings and
the retained legacy `voice_yay.mp3` remain byte-identical. The latter is no
longer a runtime fallback and cannot satisfy a spoken instruction.

Machine grades cover decode, codec, sample rate, channels, bitrate, duration,
loudness, true peak, protection, provenance class, and routing evidence. Human
voice identity, pronunciation, intelligibility, child-safety, mono, mix, and
target-device grades remain open until the listening matrix in `DL-SND-15` and
`DL-SND-16` is completed.
