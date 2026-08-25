"""Build the revised mix with the retained jump clip's original audio in sync."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parents[3]
AUTHORED = REPO / "review/audio/intro_sound_design_2026-08-23/authored"
DOWNLOADS = Path.home() / "Downloads"
DURATION = 807 / 24
SAMPLE_RATE = 48_000


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
	return subprocess.run(command, check=True, text=True, capture_output=capture)


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1 << 20), b""):
			digest.update(block)
	return digest.hexdigest()


def loop_component(ffmpeg: str, source: Path, destination: Path, gain: float, start: float, end: float) -> None:
	active = end - start
	filters = (
		f"volume={gain:.6f},atrim=duration={active:.6f},"
		f"afade=t=in:st=0:d=0.08,afade=t=out:st={max(0.0, active - 0.35):.3f}:d=0.35,"
		f"adelay={round(start * 1000)}:all=1,apad,atrim=duration={DURATION:.6f}"
	)
	run([ffmpeg, "-hide_banner", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(source), "-af", filters, "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", "-t", f"{DURATION:.6f}", str(destination)])


def source_component(ffmpeg: str, source: Path, destination: Path) -> None:
	# Picture uses source frames [12, 133) at 24 fps, placed at record frame 384.
	filters = (
		"atrim=start=0.5:end=5.541666667,asetpts=PTS-STARTPTS,volume=3.8,"
		"afade=t=in:st=0:d=0.04,afade=t=out:st=4.791667:d=0.25,"
		f"adelay=16000:all=1,apad,atrim=duration={DURATION:.6f}"
	)
	run([ffmpeg, "-hide_banner", "-y", "-loglevel", "error", "-i", str(source), "-map", "0:a:0", "-af", filters, "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", "-t", f"{DURATION:.6f}", str(destination)])


def main() -> None:
	ffmpeg = shutil.which("ffmpeg")
	if not ffmpeg:
		raise RuntimeError("ffmpeg is not on PATH")
	home = REPO / "assets/audio/music/home.ogg"
	source_audio = DOWNLOADS / "grok-b313bcb5-6577-46b0-80f6-b383830c786d-720p.mp4"
	cues = [
		("music_bed", home, 0.14, 0.0, DURATION),
		("flight", AUTHORED / "flight_exterior_loop.wav", 0.22, 0.0, 2.0),
		("cabin", AUTHORED / "cabin_room_loop.wav", 0.26, 2.0, 6.0),
		("island_reveal", AUTHORED / "reveal_island.wav", 0.24, 5.5, 7.6),
		("flight_bridge", AUTHORED / "flight_exterior_loop.wav", 0.16, 5.6, 8.0),
		("castle_reveal", AUTHORED / "reveal_castle.wav", 0.24, 7.1, 10.2),
		("forest_lakeside", AUTHORED / "forest_lakeside_loop.wav", 0.21, 9.3, 14.6),
		("otter_action_authored", AUTHORED / "otter_plane_action_loop.wav", 0.23, 14.4, 21.0416667),
		("cabin_return", AUTHORED / "cabin_room_loop.wav", 0.26, 21.0416667, 23.5416667),
		("reunion_walk", AUTHORED / "reunion_walk_loop.wav", 0.29, 23.0416667, 28.5833333),
		("exterior_air", AUTHORED / "flight_exterior_loop.wav", 0.08, 23.0416667, 28.5833333),
		("bridge_arrival", AUTHORED / "bridge_water_arrival_loop.wav", 0.31, 28.0833333, DURATION),
	]
	for _, source, _, _, _ in cues:
		if not source.is_file():
			raise FileNotFoundError(source)
	if not source_audio.is_file():
		raise FileNotFoundError(source_audio)
	output = PACKAGE / "otter_recut_v2_audio_mix.ogg"
	resolve_wav = PACKAGE / "otter_recut_v2_audio_mix_resolve.wav"
	with tempfile.TemporaryDirectory(prefix="otter_recut_v2_audio_") as temp_name:
		temp = Path(temp_name)
		components = []
		for index, (_, source, gain, start, end) in enumerate(cues):
			path = temp / f"component_{index:02d}.wav"
			loop_component(ffmpeg, source, path, gain, start, end)
			components.append(path)
		source_path = temp / "component_original_otter_audio.wav"
		source_component(ffmpeg, source_audio, source_path)
		components.append(source_path)
		inputs = sum((["-i", str(path)] for path in components), [])
		labels = "".join(f"[{index}:a]" for index in range(len(components)))
		graph = labels + f"amix=inputs={len(components)}:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-17:TP=-1:LRA=7[mix]"
		run([ffmpeg, "-hide_banner", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph, "-map", "[mix]", "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "libvorbis", "-b:a", "112k", "-t", f"{DURATION:.6f}", str(output)])
	run([ffmpeg, "-hide_banner", "-y", "-loglevel", "error", "-i", str(output), "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s24le", str(resolve_wav)])
	metrics = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(output), "-af", "ebur128=peak=true", "-f", "null", "NUL"], capture=True)
	(PACKAGE / "audio_metrics_v2.txt").write_text(metrics.stderr, encoding="utf-8")
	(PACKAGE / "audio_cue_audit_v2.json").write_text(json.dumps({
		"duration_seconds": DURATION,
		"source_clip_audio_included": True,
		"source_clip": str(source_audio),
		"source_clip_sha256": sha256(source_audio),
		"source_audio_stream": "0:a:0 AAC-LC stereo 48000 Hz",
		"source_frames": [12, 133],
		"record_frames": [384, 505],
		"sync_offset_seconds": 16.0,
		"source_trim_seconds": [0.5, 5.541666667],
		"source_gain": 3.8,
		"voices_generated_or_modified": False,
		"mix": str(output),
		"mix_sha256": sha256(output),
		"resolve_wav": str(resolve_wav),
		"resolve_wav_sha256": sha256(resolve_wav),
	}, indent=2) + "\n", encoding="utf-8")
	print(output)
	print(resolve_wav)


if __name__ == "__main__":
	main()
