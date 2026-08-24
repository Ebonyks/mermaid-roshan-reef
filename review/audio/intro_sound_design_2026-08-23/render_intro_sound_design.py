#!/usr/bin/env python3
"""Render a deterministic, non-destructive intro sound-design review package."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path


DURATION = 42.133333
SAMPLE_RATE = 48_000


def run(cmd: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
	return subprocess.run(cmd, check=True, text=True, capture_output=capture)


def require_tool(name: str) -> str:
	path = shutil.which(name)
	if not path:
		raise SystemExit(f"Required executable not found on PATH: {name}")
	return path


def sha256(path: Path) -> str:
	hash_obj = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1 << 20), b""):
			hash_obj.update(block)
	return hash_obj.hexdigest()


def generate_engine(path: Path) -> None:
	"""Make a fixed, gentle engine bed for silent plane/travel pictures only."""
	seed = int.from_bytes(hashlib.sha256(b"intro-flight-engine-gap-v1").digest()[:8], "big")
	state = seed
	frames = int(round(DURATION * SAMPLE_RATE))
	with wave.open(str(path), "wb") as output:
		output.setnchannels(2)
		output.setsampwidth(2)
		output.setframerate(SAMPLE_RATE)
		block: list[bytes] = []
		for index in range(frames):
			time_s = index / SAMPLE_RATE
			# Plane/travel windows are tied to the measured silent picture beats.
			windows = ((0.0, 2.0), (4.5, 7.5), (12.5, 23.0), (28.0, 36.1))
			level = 0.0
			for start, end in windows:
				if start <= time_s < end:
					fade = min((time_s - start) / 0.45, (end - time_s) / 0.55, 1.0)
					level = max(level, max(0.0, fade))
			state = (1664525 * state + 1013904223) & 0xFFFFFFFF
			noise = ((state / 0xFFFFFFFF) * 2.0) - 1.0
			body = (
				0.42 * math.sin(2.0 * math.pi * 78.0 * time_s)
				+ 0.22 * math.sin(2.0 * math.pi * 156.0 * time_s)
				+ 0.10 * math.sin(2.0 * math.pi * 234.0 * time_s)
				+ 0.025 * noise
			)
			sample = max(-1.0, min(1.0, body * level * 0.16))
			value = int(round(sample * 32767.0))
			block.append(int(value).to_bytes(2, "little", signed=True) * 2)
			if len(block) >= 4096:
				output.writeframesraw(b"".join(block))
				block.clear()
		if block:
			output.writeframesraw(b"".join(block))


def write_probe(ffprobe: str, source: Path, destination: Path) -> None:
	result = run([ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(source)], capture=True)
	destination.write_text(result.stdout, encoding="utf-8")


def video_stream_sha256(ffmpeg: str, source: Path) -> str:
	result = run([
		ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(source),
		"-map", "0:v:0", "-c", "copy", "-f", "streamhash", "-hash", "sha256", "-",
	], capture=True)
	for line in result.stdout.splitlines():
		if "SHA256=" in line:
			return line.rsplit("SHA256=", 1)[1].strip().lower()
	raise RuntimeError(f"FFmpeg did not return a video stream hash for {source}")


def make_component(ffmpeg: str, asset: Path, destination: Path, volume: float, start: float = 0.0, end: float = DURATION) -> None:
	adelay_ms = max(0, int(round(start * 1000.0)))
	active_duration = max(0.05, end - start)
	filter_chain = f"volume={volume:.6f},atrim=duration={active_duration:.6f},afade=t=in:st=0:d=0.08,afade=t=out:st={max(0.0, active_duration - 0.35):.3f}:d=0.35,adelay={adelay_ms}:all=1,apad,atrim=duration={DURATION:.6f}"
	run([ffmpeg, "-hide_banner", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(asset), "-af", filter_chain, "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", "-t", f"{DURATION:.6f}", str(destination)])


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--source", type=Path, required=True)
	parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
	parser.add_argument("--ffmpeg", default="ffmpeg")
	parser.add_argument("--ffprobe", default="ffprobe")
	args = parser.parse_args()
	ffmpeg = require_tool(args.ffmpeg)
	ffprobe = require_tool(args.ffprobe)
	source = args.source.resolve()
	repo = args.repo.resolve()
	if not source.is_file():
		raise SystemExit(f"Source video not found: {source}")
	out_dir = Path(__file__).resolve().parent
	generated = out_dir / "generated"
	generated.mkdir(exist_ok=True)
	assets = {
		"home": repo / "assets/audio/music/home.ogg",
		"hall": repo / "assets/audio/ambience_hall.ogg",
		"reef": repo / "assets/audio/ambience_reef.ogg",
		"lagoon": repo / "assets/audio/ambience_lagoon.ogg",
		"chime": repo / "assets/audio/chime.ogg",
		"hop": repo / "assets/audio/hop_boing.ogg",
		"water": repo / "assets/audio/castle/bubble_water.ogg",
	}
	for name, asset in assets.items():
		if not asset.is_file():
			raise SystemExit(f"Required approved asset missing ({name}): {asset}")
	write_probe(ffprobe, source, out_dir / "source_ffprobe.json")
	engine = generated / "flight_engine_gap.wav"
	generate_engine(engine)
	component_dir = Path(tempfile.mkdtemp(prefix="intro_sound_design_components_"))
	try:
		components: list[Path] = [engine]
		for name, volume, start, end in (("home", 0.16, 0.0, DURATION), ("hall", 0.055, 2.0, 4.5), ("hall", 0.055, 23.04, 28.0), ("reef", 0.045, 7.5, 36.1), ("lagoon", 0.05, 36.08, DURATION)):
			destination = component_dir / f"{name}_{int(round(start * 100)):04d}.wav"
			make_component(ffmpeg, assets[name], destination, volume, start, end)
			components.append(destination)
		for name, volume, start in (("chime", 0.23, 4.5), ("chime", 0.23, 7.5), ("chime", 0.19, 23.04), ("chime", 0.23, 36.08), ("hop", 0.16, 14.0), ("hop", 0.12, 19.5), ("water", 0.10, 36.35)):
			destination = component_dir / f"{name}_{int(round(start * 100)):04d}.wav"
			make_component(ffmpeg, assets[name], destination, volume, start, start + 1.5)
			components.append(destination)
		standalone = out_dir / "intro_sound_design_mix.ogg"
		input_args = ["-i", str(source)] + sum((["-i", str(component)] for component in components), [])
		labels = ["[0:a]"] + [f"[{index}:a]" for index in range(1, len(components) + 1)]
		filter_graph = "".join(labels) + f"amix=inputs={len(labels)}:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-17:TP=-1:LRA=7:print_format=summary[mix]"
		run([ffmpeg, "-hide_banner", "-y", *input_args, "-filter_complex", filter_graph, "-map", "[mix]", "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "libvorbis", "-b:a", "96k", "-t", f"{DURATION:.6f}", str(standalone)])
		review_mp4 = out_dir / "intro_sound_design_review.mp4"
		run([ffmpeg, "-hide_banner", "-y", "-i", str(source), "-i", str(standalone), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(review_mp4)])
		write_probe(ffprobe, review_mp4, out_dir / "output_ffprobe.json")
		source_video_hash = video_stream_sha256(ffmpeg, source)
		review_video_hash = video_stream_sha256(ffmpeg, review_mp4)
		if source_video_hash != review_video_hash:
			raise RuntimeError("Review MP4 video stream differs from the read-only source")
		(out_dir / "video_stream_sha256.txt").write_text(
			f"source_video_stream_sha256={source_video_hash}\n"
			f"review_video_stream_sha256={review_video_hash}\n",
			encoding="utf-8",
		)
		metrics = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(standalone), "-af", "ebur128=peak=true", "-f", "null", "NUL"], capture=True)
		metrics_text = "\n".join(line.rstrip() for line in metrics.stderr.splitlines()) + "\n"
		(out_dir / "render_metrics.txt").write_text(metrics_text, encoding="utf-8")
		checksums = [f"{sha256(source)}  {source}", f"{sha256(standalone)}  {standalone}", f"{sha256(review_mp4)}  {review_mp4}", f"{sha256(engine)}  {engine}"]
		(out_dir / "sha256sums.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
	finally:
		shutil.rmtree(component_dir, ignore_errors=True)
		(out_dir / "intro_sound_design_mix.ogg.import").unlink(missing_ok=True)
	print(f"Rendered: {standalone}")
	print(f"Rendered review MP4: {review_mp4}")
	return 0


if __name__ == "__main__":
	sys.exit(main())
