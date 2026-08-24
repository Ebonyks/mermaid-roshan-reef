# Intro sound-design review package

This is a non-destructive review render for `C:\Users\Peter\Intro for mermaid roshan.mp4`. It does not modify the source MP4, runtime assets, protected voices, or game scenes. Cabin dialogue is intentionally left owner-recording-blocked; no voice is synthesized, generated, or altered.

## Reproduce

From the repository root, with FFmpeg 8.x and Python 3.10+ available:

```powershell
python review/audio/intro_sound_design_2026-08-23/render_intro_sound_design.py --source "C:\Users\Peter\Intro for mermaid roshan.mp4"
```

The script checks dependencies and required asset paths, writes the deterministic nonvoice engine master under `generated/`, creates and removes temporary component WAVs, mixes a standalone `intro_sound_design_mix.ogg`, remuxes `intro_sound_design_review.mp4` with the source video stream copied (`-c:v copy`), and records `source_ffprobe.json`, `output_ffprobe.json`, `sha256sums.txt`, `video_stream_sha256.txt`, and `render_metrics.txt`. It fails if the copied review video stream hash differs from the source video stream hash.

## Reuse/provenance

Existing project-owned audio is reused first: `assets/audio/music/home.ogg`, `assets/audio/ambience_hall.ogg`, `assets/audio/ambience_reef.ogg`, `assets/audio/ambience_lagoon.ogg`, `assets/audio/chime.ogg`, `assets/audio/hop_boing.ogg`, and `assets/audio/castle/bubble_water.ogg`. Their existing provenance is authoritative; no new `ASSET_LICENSES.md` row is needed because no runtime asset is added.

The only new audio is `generated/flight_engine_gap.wav`, a deterministic procedural nonvoice effect for the measured silent plane/travel beats. It uses fixed sine partials, a fixed SHA-256-derived noise seed, and fades only. It is review evidence, not runtime art. The exact algorithm is in the render script.

## Acceptance notes

- Source video pixels remain untouched and are copied into the review MP4.
- Source audio from approximately 17–23 s remains present underneath the mix.
- Target mix is calm and child-safe: approximately `-17 LUFS`, true peak `<= -1 dBTP`.
- Dialogue gaps are explicit and blocked pending owner-recorded family voices.
