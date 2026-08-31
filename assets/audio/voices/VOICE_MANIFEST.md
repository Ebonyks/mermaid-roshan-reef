# Character voices

## Provisional synthetic filler v1 (2026-08-30)

Runtime now prefers `filler_v1/<speaker>_<event>.ogg`, then the corresponding
legacy path. The 285 live cues comprise all 284 authoritative non-Faron filler
keys plus the three-preset `everyone.ogg` mix. The three group source layers
remain provenance-only WAVs and are not separately addressable runtime cues.
This is a reversible machine-screened
layer—not confirmed talent, not human-auditioned, and not
a claimed match to any real person. Faron and the sacred family recordings are
excluded and remain byte-identical. Three newly authored Daddy event fillers
use distinct keys; they do not replace or modify `daddy1..3.ogg`.

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

`FILLER_MANIFEST.json` schema 2 embeds the candidate evidence even though the
working candidate tree is ignored: `generation_run_provenance` embeds every
attempt's available run record, candidate manifest hash, and candidate
generation rows;
`candidate_selection_evidence` embeds every selected and rejected candidate's
ASR/DNSMOS/identity evidence, disposition, rejection reason, and raw-WAV hash.
Each selected entry records the validated attempt/seed/source tuple. Every
delivery row's `delivery_metrics.ogg_determinism` contains a byte-identical
same-input re-encode proof with fixed Ogg serial and page-CRC evidence. The
three `everyone` components must carry the same strict selection evidence
before they may be mixed; duration alone is not an acceptance gate.

Provenance limitation: attempts 1 and 2 predate captured run records. Their
candidate rows preserve text, preset, description, seed, model/tokenizer
revisions and raw hashes, but their run entries are explicitly marked
`RECONSTRUCTED_FROM_CANDIDATE_MANIFEST` with
`generator_sha256: NOT_CAPTURED_AT_GENERATION`. The 120 selected cues from
those attempts are suitable only for provisional device audition; they do not
close DL-SND-17's complete-provenance requirement without an owner-approved
exception or regeneration under captured provenance.

The game first resolves an exact event in `filler_v1`, then uses the protected
or retained legacy path where policy permits. It does not use the retained
`voice_yay.mp3` as a generic fallback.

## Legacy Kokoro source path

`tools/make_voices.py` retains the authoritative line table and the former
Kokoro-82M fallback generator. Kokoro output is not the accepted live filler
cohort. New provisional candidates must use the Parler candidate/selector/master
pipeline above so the stricter semantic, quality, provenance, and deterministic
delivery gates remain enforceable.

To change a line or add a new one: edit the `LINES` table in
`tools/make_voices.py` and re-run it (setup instructions in the script header).
Use repeatable `--line <exact_key>` arguments for a bounded replacement; do not
regenerate the whole voice library to repair one line. The delivery limiter
leaves conservative encode headroom so decoded Vorbis stays at or below the
project-wide −1.5 dBTP ceiling.
New `<speaker>_<event>.ogg` names are picked up by the game automatically —
no code changes needed. Events used by the game: `talk`, `win`, `fail`,
plus bespoke ones (`greet`, `intro`, `thanks`, `bark`, `pearl`, `idle1..3`).

## Live provisional synthetic preset map

| character | Parler preset | feel |
|---|---|---|
| Roshan | Laura | youthful, bright, consistent guide |
| Huluu | Lea | gentle storybook princess |
| Evie | Jenna | bubbly youthful friend |
| Harper | Lauren | warm big-sister voice |
| Wacky | Gary | kindly older comic voice |
| Shop | Jon | welcoming adult voice |
| Sparkle | Tina | tiny bright creature voice |
| Rosalina | Rose | calm fairy-tale voice |
| Imps | Mike | impish cartoon voice |
| Rumi | Emily | warm youthful friend |
| Mewsha | Joy | playful storybook-kitty voice |
| Daddy fillers only | Will | warm adult helper; numbered recordings untouched |
| everyone | Laura + Lea + Jenna | audited, trimmed three-voice mix |

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
