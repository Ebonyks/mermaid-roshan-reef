# Intro sound-design review cue sheet

Source: `C:\Users\Peter\Intro for mermaid roshan.mp4` (read-only). Video is 42.125 s at 24 fps; source audio is AAC stereo, 48 kHz, 42.133 s. This review mix keeps the source audio underneath from 17.0006–22.99 s and adds only approved project-owned assets plus one deterministic, nonvoice flight-engine gap effect.

| Time | Picture beat | Review audio | Source / treatment | Priority |
|---|---|---|---|---|
| 0.00–2.00 | Plane cruising | Soft flight-engine bed; home motif begins quietly | `generated/flight_engine_gap.wav`; `assets/audio/music/home.ogg` | P0 |
| 2.00–4.50 | Cabin, Roshan and child | Cabin room tone; music remains ducked and calm | `assets/audio/ambience_hall.ogg`; dialogue remains owner-recording-blocked | P0 |
| 4.50 | Island reveal | Short magical chime | `assets/audio/chime.ogg`, delayed 4.50 s | P1 |
| 4.50–7.50 | Plane approaches island/castle | Flight bed and soft music | Generated engine gap effect; `home.ogg` | P1 |
| 7.50 | Castle reveal | Short magical chime | `chime.ogg`, delayed 7.50 s | P1 |
| 7.50–12.50 | Castle, forest, lakeside | Gentle outdoor ambience | `assets/audio/ambience_reef.ogg` | P1 |
| 12.50–14.00 | Playground plane before otter | Flight/park bed | Generated engine gap effect; reef ambience | P1 |
| 14.00–23.00 | Otter arrives and plays around plane | Playful arrival/landing cue; source audio retained from 17 s | `hop_boing.ogg` at 14.0 and 19.5 s; source MP4 audio is included unedited before the final whole-mix loudness pass | P0 |
| 23.04 | Cut back to cabin | Transition chime | `chime.ogg`, delayed 23.04 s | P1 |
| 23.04–28.00 | Cabin conversation/wide shot | Cabin room tone, music ducked | `ambience_hall.ogg`; dialogue remains owner-recording-blocked | P0 |
| 28.04–36.08 | Family, otter and plane outside | Park/flight bed and gentle movement support | Generated engine gap effect; reef ambience | P1 |
| 36.08 | Castle return | Chime plus water tail | `chime.ogg` at 36.08 s; `castle/bubble_water.ogg` at 36.35 s | P1 |
| 36.08–42.13 | Walk toward castle bridge | Warm closing music, lagoon/water ambience | `home.ogg`, `ambience_lagoon.ogg`, `bubble_water.ogg` | P1 |

## Source-audio evidence

`ffmpeg silencedetect=noise=-40dB:d=0.20` reports silence at 0–17.000646 s, 18.605875–19.026042 s, 19.168125–19.641875 s, and 21.228813–42.133333 s. At `-50 dB`, a low-level tail continues to about 22.99 s.

Full-source `ebur128=peak=true`: integrated `-37.1 LUFS`, LRA `20.4 LU`, true peak `-20.4 dBFS`. The low integrated value is dominated by the long silent sections. The review render is normalized to approximately `-17 LUFS`, `<= -1 dBTP` for phone playback.

The active source signal is low-mid-heavy and near-dual-mono (L/R correlation `0.9967`), consistent with an engine/foley-like bed rather than a complete music mix. Exact semantic identification requires owner listening; the render does not discard it.
