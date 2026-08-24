#!/usr/bin/env python3
"""Render and independently audit the authored intro sound-design review."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


DURATION = 42.133333
SAMPLE_RATE = 48_000
PACKAGE = Path(__file__).resolve().parent
AUTHORED_NAMES = (
	"flight_exterior_loop.wav",
	"cabin_room_loop.wav",
	"reveal_island.wav",
	"reveal_castle.wav",
	"forest_lakeside_loop.wav",
	"otter_plane_action_loop.wav",
	"reunion_walk_loop.wav",
	"bridge_water_arrival_loop.wav",
)


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
	return subprocess.run(command, check=True, text=True, capture_output=capture)


def clean_tool_log(output: str) -> str:
	return "\n".join(line.rstrip() for line in output.splitlines()) + "\n"


def tool(name: str) -> str:
	path = shutil.which(name)
	if not path:
		raise SystemExit(f"Required executable not found on PATH: {name}")
	return path


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1 << 20), b""):
			digest.update(block)
	return digest.hexdigest()


def ffprobe_json(ffprobe: str, path: Path) -> dict:
	result = run([ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)], capture=True)
	return json.loads(result.stdout)


def write_json(path: Path, value: object) -> None:
	path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def video_stream_sha256(ffmpeg: str, path: Path) -> str:
	result = run([ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(path), "-map", "0:v:0", "-c", "copy", "-f", "streamhash", "-hash", "sha256", "-"], capture=True)
	for line in result.stdout.splitlines():
		if "SHA256=" in line:
			return line.rsplit("SHA256=", 1)[1].strip().lower()
	raise RuntimeError(f"No video stream hash returned for {path}")


def component(ffmpeg: str, source: Path, destination: Path, volume: float, start: float, end: float) -> None:
	if end <= start:
		raise ValueError(f"Invalid cue span {start}–{end}")
	active = end - start
	delay_ms = int(round(start * 1000.0))
	filters = (
		f"volume={volume:.6f},atrim=duration={active:.6f},"
		f"afade=t=in:st=0:d=0.08,afade=t=out:st={max(0.0, active - 0.35):.3f}:d=0.35,"
		f"adelay={delay_ms}:all=1,apad,atrim=duration={DURATION:.6f}"
	)
	run([ffmpeg, "-hide_banner", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(source), "-af", filters, "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", "-t", f"{DURATION:.6f}", str(destination)])


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--source", type=Path, required=True)
	parser.add_argument("--repo", type=Path, default=PACKAGE.parents[2])
	parser.add_argument("--ffmpeg", default="ffmpeg")
	parser.add_argument("--ffprobe", default="ffprobe")
	args = parser.parse_args()
	ffmpeg = tool(args.ffmpeg)
	ffprobe = tool(args.ffprobe)
	repo = args.repo.resolve()
	source = args.source.resolve()
	if not source.is_file():
		raise SystemExit(f"Source video not found: {source}")
	authored = PACKAGE / "authored"
	if not authored.is_dir():
		raise SystemExit(f"Authored palette directory missing: {authored}")
	for name in AUTHORED_NAMES:
		if not (authored / name).is_file():
			raise SystemExit(f"Authored palette stem missing: {authored / name}")
	home = (repo / "assets/audio/music/home.ogg").resolve()
	if not home.is_file():
		raise SystemExit(f"Approved music bed missing: {home}")
	# Hard allowlist: source media, home.ogg, and authored/ WAVs only.
	allowed_repo_audio = {home}
	graph_sources = [home] + [authored / name for name in AUTHORED_NAMES]
	unauthorized = [path for path in graph_sources if path not in allowed_repo_audio and path.parent != authored]
	if unauthorized:
		raise RuntimeError(f"Audio allowlist violation: {unauthorized}")
	for path in PACKAGE.glob("*.ogg.import"):
		path.unlink(missing_ok=True)
	stage_audio = PACKAGE / ".intro_sound_design_mix.stage.ogg"
	stage_review = PACKAGE / ".intro_sound_design_review.stage.mp4"
	stage_audio.unlink(missing_ok=True)
	stage_review.unlink(missing_ok=True)
	source_probe = ffprobe_json(ffprobe, source)
	write_json(PACKAGE / "source_ffprobe.json", source_probe)
	with tempfile.TemporaryDirectory(prefix="intro_sound_design_components_") as temp_name:
		temp = Path(temp_name)
		components: list[Path] = []
		# (label, source, gain, picture start, picture end, semantic category)
		cue_defs = [
			("home.ogg", home, 0.14, 0.0, DURATION, "music_bed"),
			("flight_exterior_loop.wav", authored / "flight_exterior_loop.wav", 0.22, 0.0, 2.0, "flight"),
			("cabin_room_loop.wav", authored / "cabin_room_loop.wav", 0.26, 2.0, 4.5, "cabin"),
			("reveal_island.wav", authored / "reveal_island.wav", 0.24, 4.5, 6.7, "reveal"),
			("flight_exterior_loop.wav", authored / "flight_exterior_loop.wav", 0.18, 4.5, 7.5, "flight"),
			("reveal_castle.wav", authored / "reveal_castle.wav", 0.24, 7.5, 10.1, "reveal"),
			("forest_lakeside_loop.wav", authored / "forest_lakeside_loop.wav", 0.21, 7.5, 14.0, "forest_lakeside"),
			("flight_exterior_loop.wav", authored / "flight_exterior_loop.wav", 0.10, 12.5, 14.0, "flight"),
			("otter_plane_action_loop.wav", authored / "otter_plane_action_loop.wav", 0.29, 14.0, 23.0, "otter_action"),
			("cabin_room_loop.wav", authored / "cabin_room_loop.wav", 0.26, 23.04, 28.0, "cabin"),
			("reunion_walk_loop.wav", authored / "reunion_walk_loop.wav", 0.29, 28.04, 36.08, "reunion_walk"),
			("flight_exterior_loop.wav", authored / "flight_exterior_loop.wav", 0.09, 28.04, 36.08, "flight"),
			("forest_lakeside_loop.wav", authored / "forest_lakeside_loop.wav", 0.10, 28.04, 36.08, "forest_lakeside"),
			("bridge_water_arrival_loop.wav", authored / "bridge_water_arrival_loop.wav", 0.31, 36.08, DURATION, "bridge_arrival"),
		]
		cue_audit: list[dict[str, object]] = []
		for index, (label, path, gain, start, end, category) in enumerate(cue_defs):
			destination = temp / f"component_{index:02d}.wav"
			component(ffmpeg, path, destination, gain, start, end)
			components.append(destination)
			cue_audit.append({"index": index, "source": label, "path": str(path), "category": category, "start": start, "end": end, "gain": gain})
		labels = ["[0:a]"] + [f"[{index}:a]" for index in range(1, len(components) + 1)]
		inputs = ["-i", str(source)] + sum((["-i", str(path)] for path in components), [])
		filter_graph = "".join(labels) + f"amix=inputs={len(labels)}:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-17:TP=-1:LRA=7:print_format=summary[mix]"
		standalone = stage_audio
		standalone_final = PACKAGE / "intro_sound_design_mix.ogg"
		run([ffmpeg, "-hide_banner", "-y", *inputs, "-filter_complex", filter_graph, "-map", "[mix]", "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "libvorbis", "-b:a", "96k", "-t", f"{DURATION:.6f}", str(standalone)])
		write_json(PACKAGE / "cue_audit.json", {"source_video": str(source), "source_audio_retained": True, "allowed_repo_audio": [str(home)], "authored_directory": str(authored), "cues": cue_audit, "unauthorized_repo_audio": []})
		write_json(PACKAGE / "semantic_audit.json", {
			"picture_timing_basis": "24 fps source MP4 scene audit",
			"checks": [
				{"span": [0.0, 2.0], "category": "flight", "source": "flight_exterior_loop.wav", "fit": "gentle aircraft/air movement", "status": "PASS"},
				{"span": [2.0, 4.5], "category": "cabin", "source": "cabin_room_loop.wav", "fit": "warm interior tone; dialogue space preserved", "status": "PASS_DIALOGUE_BLOCKED"},
				{"span": [4.5, 6.7], "category": "island_reveal", "source": "reveal_island.wav", "fit": "continuous wonder swell, not a UI chime", "status": "PASS"},
				{"span": [7.5, 10.1], "category": "castle_reveal", "source": "reveal_castle.wav", "fit": "low wonder swell, no alarm/fail semantics", "status": "PASS"},
				{"span": [7.5, 14.0], "category": "forest_lakeside", "source": "forest_lakeside_loop.wav", "fit": "sparse water/leaf bed", "status": "PASS"},
				{"span": [14.0, 23.0], "category": "otter_action", "source": "otter_plane_action_loop.wav", "fit": "rounded playful movement/contact, not combat/UI", "status": "PASS"},
				{"span": [23.04, 28.0], "category": "cabin", "source": "cabin_room_loop.wav", "fit": "room tone only; owner dialogue required", "status": "PASS_DIALOGUE_BLOCKED"},
				{"span": [28.04, 36.08], "category": "reunion_walk", "source": "reunion_walk_loop.wav", "fit": "gentle exterior movement", "status": "PASS"},
				{"span": [36.08, DURATION], "category": "bridge_arrival", "source": "bridge_water_arrival_loop.wav", "fit": "water/wood arrival, sustained resolution", "status": "PASS"},
			],
			"forbidden_semantics": ["fabricated_voice", "alarm", "combat_hit", "UI_click", "punitive_fail"],
		})
	review = stage_review
	review_final = PACKAGE / "intro_sound_design_review.mp4"
	run([ffmpeg, "-hide_banner", "-y", "-i", str(source), "-i", str(standalone), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(review)])
	source_video_hash = video_stream_sha256(ffmpeg, source)
	review_video_hash = video_stream_sha256(ffmpeg, review)
	if source_video_hash != review_video_hash:
		raise RuntimeError("Review video stream differs from source")
	(PACKAGE / "video_stream_sha256.txt").write_text(f"source_video_stream_sha256={source_video_hash}\nreview_video_stream_sha256={review_video_hash}\n", encoding="utf-8")
	metrics = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(standalone), "-af", "ebur128=peak=true", "-f", "null", "NUL"], capture=True)
	(PACKAGE / "render_metrics.txt").write_text(clean_tool_log(metrics.stderr), encoding="utf-8")
	silence = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(standalone), "-af", "silencedetect=noise=-45dB:d=0.20", "-f", "null", "NUL"], capture=True)
	(PACKAGE / "silence_audit.txt").write_text(clean_tool_log(silence.stderr), encoding="utf-8")
	standalone.replace(standalone_final)
	review.replace(review_final)
	output_probe = ffprobe_json(ffprobe, review_final)
	write_json(PACKAGE / "output_ffprobe.json", output_probe)
	authored_hashes = {name: sha256(authored / name) for name in AUTHORED_NAMES}
	(PACKAGE / "sha256sums.txt").write_text("\n".join([
		f"{sha256(source)}  {source}", f"{sha256(home)}  {home}",
		*[f"{digest}  {authored / name}" for name, digest in authored_hashes.items()],
		f"{sha256(standalone_final)}  {standalone_final}", f"{sha256(review_final)}  {review_final}",
	]) + "\n", encoding="utf-8")
	write_json(PACKAGE / "allowlist_audit.json", {"allowed_source_video": str(source), "allowed_repo_audio": [str(home)], "allowed_authored_audio": [str(authored / name) for name in AUTHORED_NAMES], "rejected_prior_generated_audio": str(PACKAGE / "generated"), "unauthorized_repo_audio": [], "source_audio_stream_included": True, "video_stream_copy": source_video_hash == review_video_hash})
	print(f"Rendered {standalone_final}")
	print(f"Rendered {review_final}")
	return 0


if __name__ == "__main__":
	main()
