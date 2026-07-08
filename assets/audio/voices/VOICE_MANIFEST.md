# Character voices

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
- `chuck.ogg`, `chuck_bark.ogg`
- `../voice_yay.mp3`

To improve a real recording instead of replacing it, run it through a free
speech enhancer (Adobe Podcast Enhance web tool, or locally: resemble-enhance /
DeepFilterNet), then loudness-match with the same -16 LUFS pipeline.
