# Local cartoon video pipeline

Use **Ogg Theora video (`.ogv`)** as the game master. Godot 4.4 supports it
directly through `VideoStreamPlayer`; `.ogg` is normally used for audio-only Ogg
Vorbis files. MP4/H.264 is smaller and convenient for review, but Godot does not
play it in core without an extension.

The repository encoder accepts either a directory of generated still frames or
an existing video. It never edits the source material.

## One-time Windows setup

From the repository root:

```powershell
tools\setup_video_tools.cmd
```

This installs a repository-local, pinned FFmpeg 8.1.2 essentials build under
`.video-tools/`. The installer verifies its SHA-256 checksum before extraction.
Nothing is added to the system `PATH`, and `.video-tools/` is gitignored. The
small `.cmd` launcher also works when Windows' PowerShell execution policy blocks
direct `.ps1` invocation.

The pinned Windows build comes from gyan.dev, one of the binary providers linked
by FFmpeg's official download page. It includes `libtheora`, `libvorbis`, and
`libx264`, and is GPLv3-licensed. The binary stays local and is not redistributed
with the game. On macOS or Linux with PowerShell, install a current FFmpeg with
those encoders on the `PATH`; the encoder will find it automatically.

## Encode generated frames

Frame files are naturally sorted, so both `frame_1.png` through `frame_270.png`
and names such as `F001_00000ms.png` work. All files in one frame directory must
use the same image format.

Create the game-ready video and an MP4 review copy in one run:

```powershell
tools\encode_cartoon.cmd `
  docs/storyboards/opening_cinematic/frames `
  build/cartoons/opening_cinematic.ogv `
  -Fps 18 `
  -ReviewMp4
```

The opening cinematic's 270 frames become exactly 15 seconds at 18 fps. To add
or replace its soundtrack:

```powershell
tools\encode_cartoon.cmd `
  docs/storyboards/opening_cinematic/frames `
  build/cartoons/opening_cinematic.ogv `
  -Fps 18 `
  -Audio path/to/opening_soundtrack.ogg `
  -ReviewMp4
```

The soundtrack is padded or trimmed to the frame sequence duration. Source
frames and audio are only read.

## Convert an existing animation

Generated MP4, MOV, AVI, and other FFmpeg-readable sources can be converted to a
Godot master:

```powershell
tools\encode_cartoon.cmd draft.mp4 build/cartoons/draft.ogv
```

Source audio is retained unless `-NoAudio` is passed. Use `-Audio FILE` to
replace it. Existing outputs are protected; pass `-Overwrite` deliberately to
replace them.

Run `tools\encode_cartoon.cmd -?` for quality, size, source-resolution, and
dry-run controls.

## Project defaults

- 1280×720 with aspect ratio preserved and letterboxing instead of cropping.
- Theora variable quality 6, GOP 64, and `yuv420p` for `.ogv`.
- H.264 CRF 18, `faststart`, and `yuv420p` for optional `.mp4` review copies.
- 18 fps for frame directories; existing videos keep their source frame rate
  unless `--fps` is supplied.
- Stereo Vorbis quality 6 for `.ogv`; stereo AAC 160 kbps for `.mp4`.
- FFprobe validation after every encode checks codec, dimensions, pixel format,
  and frame-sequence duration.

The 720p ceiling and low frame rate are intentional. Godot decodes Theora on the
CPU, and this project's low-end Android target has a hard performance budget.

## Moving a finished video into the game

Keep drafts and review copies under `build/` (already gitignored). Only move an
accepted `.ogv` into `assets/` when it is ready to ship. In the same commit:

1. Add its source, license, URL or generation provenance, and modifications to
   `ASSET_LICENSES.md`.
2. Run the required Godot import and full probe suite.
3. Test playback on the Lenovo Tab M11 before integrating it into a scene.

Do not commit the MP4 review copy unless it has an explicit project purpose.

## References

- [Godot 4.4: Playing videos](https://docs.godotengine.org/en/4.4/tutorials/animation/playing_videos.html)
- [FFmpeg official downloads](https://ffmpeg.org/download.html)
- [Pinned Windows build provider and license details](https://www.gyan.dev/ffmpeg/builds/)
