# Intro sound-design review package (second pass)

This package is a non-destructive review render for `C:\Users\Peter\Intro for mermaid roshan.mp4`. The source MP4 is read-only. The renderer includes the source audio stream underneath the mix, accepts only `assets/audio/music/home.ogg` from runtime game audio, and uses only the eight newly authored procedural nonvoice masters under `authored/`. No voices are synthesized or altered; cabin dialogue remains owner-recording-blocked.

## Reproduce

From the repository root with FFmpeg 8.x and Python 3.10+:

```powershell
python review/audio/intro_sound_design_2026-08-23/render_intro_sound_design.py --source "C:\Users\Peter\Intro for mermaid roshan.mp4"
```

The renderer hard-fails if the authored palette or approved `home.ogg` is missing, or if any other runtime audio path is introduced. Component WAVs are written only to a disposable system temp directory and removed on completion. The rejected prior `generated/` directory is not a renderer input and must remain absent.

Outputs include the standalone `intro_sound_design_mix.ogg`, remuxed `intro_sound_design_review.mp4` with `-c:v copy`, `cue_audit.json`, `allowlist_audit.json`, `source_ffprobe.json`, `output_ffprobe.json`, `render_metrics.txt`, `silence_audit.txt`, `video_stream_sha256.txt`, and `sha256sums.txt`.

## Palette and provenance

The eight authored masters and their deterministic provenance are owned by `author_sound_palette.py` and documented in `sound_design_spec.md`:

- `flight_exterior_loop.wav`
- `cabin_room_loop.wav`
- `reveal_island.wav`
- `reveal_castle.wav`
- `forest_lakeside_loop.wav`
- `otter_plane_action_loop.wav`
- `reunion_walk_loop.wav`
- `bridge_water_arrival_loop.wav`

The only reused runtime game audio is the approved project-owned `assets/audio/music/home.ogg`. No ambience, chime, UI, combat, Castle, or other game SFX enters the graph. The source MP4 audio remains present as the immutable existing reference layer.

## Acceptance

- Source video stream hash and review video stream hash must be identical.
- Final mix target is approximately `-18` to `-16 LUFS` and `<= -1 dBTP`.
- Silence audit must show no unintended long silent spans in the final standalone mix.
- Cue audit must show only the source MP4, `home.ogg`, and `authored/*.wav` inputs, with no unauthorized repo audio.
- Review is picture-timed and child-safe in intent: no alarms, combat hits, UI clicks, fabricated speech, or text-dependent cues.
