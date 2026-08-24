"""Render a purpose-built sound mix for the 39.125-second Luna recut."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parents[2]
AUDIO_PACKAGE = REPO / "review/audio/intro_sound_design_2026-08-23"
AUTHORED = AUDIO_PACKAGE / "authored"
DURATION = 39.125
SAMPLE_RATE = 48_000


def tool(name: str) -> str:
	value = shutil.which(name)
	if not value:
		raise RuntimeError(f"Missing executable: {name}")
	return value


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
	return subprocess.run(command, check=True, text=True, capture_output=capture)


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1 << 20), b""):
			digest.update(block)
	return digest.hexdigest()


def component(ffmpeg: str, source: Path, destination: Path, gain: float, start: float, end: float) -> None:
	active = end - start
	delay_ms = round(start * 1000)
	filters = (
		f"volume={gain:.6f},atrim=duration={active:.6f},"
		f"afade=t=in:st=0:d=0.08,afade=t=out:st={max(0.0, active - 0.35):.3f}:d=0.35,"
		f"adelay={delay_ms}:all=1,apad,atrim=duration={DURATION:.6f}"
	)
	run([
		ffmpeg, "-hide_banner", "-y", "-loglevel", "error", "-stream_loop", "-1",
		"-i", str(source), "-af", filters, "-ar", str(SAMPLE_RATE), "-ac", "2",
		"-c:a", "pcm_s16le", "-t", f"{DURATION:.6f}", str(destination),
	])


def main() -> None:
	ffmpeg = tool("ffmpeg")
	home = REPO / "assets/audio/music/home.ogg"
	cues = [
		("music_bed", home, 0.14, 0.0, DURATION),
		("flight", AUTHORED / "flight_exterior_loop.wav", 0.22, 0.0, 2.0),
		("cabin", AUTHORED / "cabin_room_loop.wav", 0.26, 2.0, 6.0),
		("island_reveal", AUTHORED / "reveal_island.wav", 0.24, 5.5, 7.6),
		("flight_bridge", AUTHORED / "flight_exterior_loop.wav", 0.16, 5.6, 8.0),
		("castle_reveal", AUTHORED / "reveal_castle.wav", 0.24, 7.1, 10.2),
		("forest_lakeside", AUTHORED / "forest_lakeside_loop.wav", 0.21, 9.3, 14.6),
		("otter_action", AUTHORED / "otter_plane_action_loop.wav", 0.29, 14.4, 24.05),
		("cabin_return", AUTHORED / "cabin_room_loop.wav", 0.26, 24.04, 29.05),
		("reunion_walk", AUTHORED / "reunion_walk_loop.wav", 0.29, 28.54, 34.09),
		("exterior_air", AUTHORED / "flight_exterior_loop.wav", 0.08, 28.54, 34.09),
		("bridge_arrival", AUTHORED / "bridge_water_arrival_loop.wav", 0.31, 33.58, DURATION),
	]
	for _, path, _, _, _ in cues:
		if not path.is_file():
			raise FileNotFoundError(path)
	output = PACKAGE / "luna_recut_audio_mix.ogg"
	stage = PACKAGE / ".luna_recut_audio_mix.stage.ogg"
	with tempfile.TemporaryDirectory(prefix="luna_recut_audio_") as temp_name:
		temp = Path(temp_name)
		components = []
		for index, (_, source, gain, start, end) in enumerate(cues):
			path = temp / f"component_{index:02d}.wav"
			component(ffmpeg, source, path, gain, start, end)
			components.append(path)
		inputs = sum((["-i", str(path)] for path in components), [])
		labels = "".join(f"[{index}:a]" for index in range(len(components)))
		graph = (
			labels + f"amix=inputs={len(components)}:duration=longest:dropout_transition=0:normalize=0,"
			"loudnorm=I=-17:TP=-1:LRA=7[mix]"
		)
		run([
			ffmpeg, "-hide_banner", "-y", "-loglevel", "error", *inputs,
			"-filter_complex", graph, "-map", "[mix]", "-ar", str(SAMPLE_RATE),
			"-ac", "2", "-c:a", "libvorbis", "-b:a", "96k", "-t", f"{DURATION:.6f}",
			str(stage),
		])
	stage.replace(output)
	resolve_wav = PACKAGE / "luna_recut_audio_mix_resolve.wav"
	run([
		ffmpeg, "-hide_banner", "-y", "-loglevel", "error", "-i", str(output),
		"-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s24le", str(resolve_wav),
	])
	metrics = run([
		ffmpeg, "-hide_banner", "-nostats", "-i", str(output), "-af", "ebur128=peak=true",
		"-f", "null", "NUL",
	], capture=True)
	silence = run([
		ffmpeg, "-hide_banner", "-nostats", "-i", str(output),
		"-af", "silencedetect=noise=-45dB:d=0.20", "-f", "null", "NUL",
	], capture=True)
	(PACKAGE / "audio_render_metrics.txt").write_text(metrics.stderr, encoding="utf-8")
	(PACKAGE / "audio_silence_audit.txt").write_text(silence.stderr, encoding="utf-8")
	(PACKAGE / "audio_cue_audit.json").write_text(json.dumps({
		"duration_seconds": DURATION,
		"music": str(home),
		"authored_palette": str(AUTHORED),
		"source_clip_audio_included": False,
		"voices_generated_or_modified": False,
		"cues": [
			{"name": name, "source": str(path), "gain": gain, "start": start, "end": end}
			for name, path, gain, start, end in cues
		],
		"sha256": sha256(output),
		"resolve_wav": str(resolve_wav),
		"resolve_wav_sha256": sha256(resolve_wav),
	}, indent=2) + "\n", encoding="utf-8")
	print(output)
	print(resolve_wav)


if __name__ == "__main__":
	main()
