# Day One voice timelines

This directory contains review-only voice cue plans for editorial videos. The
attached `grok-0e40140f-8759-4188-8e0f-6ba103909db8.mp4` is an untrusted,
read-only reference. It is registered by SHA-256 and is never copied into
runtime assets or muxed by the tooling.

The initial source is the 46.5-second, 1280x720, 24-fps, silent rough covering
D1-C00/C01. The cue sidecar uses exact half-open frame/time spans and stable
event keys. The 33.5–36.5 second otter beat is intentionally omitted because
the reaction is ambiguous. The closed-door beat remains explicit before the
door-opening cue.

Use `tools/build_day_one_voice_timeline.py` to intake future D1-C00 through
D1-C12 uploads using the same ledger schema. `plan` output must remain under
this review directory (or another non-runtime path). Audio is pending until a
real audio file hash is recorded; `--require-audio` is the delivery gate.

No timeline entry permits time-stretching or muxing. Visual acceptance,
human listening, device playback, and final delivery acceptance remain open.
