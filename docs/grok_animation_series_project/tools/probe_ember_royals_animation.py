#!/usr/bin/env python3
"""Static validation for the committed Ember Royals animation package."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CHARACTERS = ROOT / "characters"
EXPECTED = {
	"ember_king": ("EMBER_KING", ("idle", "heavy_walk", "cape_fan")),
	"ember_prince": ("EMBER_PRINCE", ("idle_glance", "sleek_walk", "cinderstep")),
}


def fail(message: str) -> None:
	print(f"FAIL: {message}")
	raise SystemExit(1)


def ffprobe(path: Path) -> dict[str, object]:
	binary = shutil.which("ffprobe")
	if binary is None:
		fail("ffprobe is unavailable")
	result = subprocess.run(
		[
			binary,
			"-v",
			"error",
			"-show_entries",
			"format=duration:stream=codec_type,width,height,r_frame_rate",
			"-of",
			"json",
			str(path),
		],
		check=True,
		capture_output=True,
		text=True,
	)
	return json.loads(result.stdout)


def validate_character(character_id: str, prefix: str, animations: tuple[str, ...]) -> None:
	directory = CHARACTERS / character_id
	atlas_path = directory / f"{prefix}_RUNTIME_ATLAS.png"
	atlas = Image.open(atlas_path)
	if atlas.size != (1024, 768) or atlas.mode != "RGBA":
		fail(f"{atlas_path.name} must be 1024x768 RGBA; got {atlas.size} {atlas.mode}")
	if atlas.getchannel("A").getextrema()[0] != 0:
		fail(f"{atlas_path.name} has no transparent background")

	for index in range(8):
		frame_path = directory / "frames" / f"{prefix}_frame_{index + 1:02d}.png"
		frame = Image.open(frame_path)
		if frame.size != (256, 384) or frame.mode != "RGBA":
			fail(f"{frame_path.name} must be 256x384 RGBA")
		bbox = frame.getchannel("A").getbbox()
		if bbox is None:
			fail(f"{frame_path.name} is empty")
		left, top, right, bottom = bbox
		if left < 2 or top < 2 or right > 254 or bottom > 382:
			fail(f"{frame_path.name} touches its cell edge: {bbox}")

	for animation in animations:
		gif_path = directory / "animations" / f"{prefix}_{animation}.gif"
		gif = Image.open(gif_path)
		if gif.size != (512, 288) or getattr(gif, "n_frames", 1) < 3:
			fail(f"{gif_path.name} is not a multi-frame 512x288 GIF")
		video_path = directory / "animations" / f"{prefix}_{animation}.mp4"
		metadata = ffprobe(video_path)
		streams = metadata.get("streams", [])
		video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
		audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
		if len(video_streams) != 1 or audio_streams:
			fail(f"{video_path.name} must contain one video stream and no audio")
		stream = video_streams[0]
		if (stream.get("width"), stream.get("height")) != (1024, 576):
			fail(f"{video_path.name} must be 1024x576")
		duration = float(metadata.get("format", {}).get("duration", 0.0))
		if duration <= 0.0 or duration > 15.0:
			fail(f"{video_path.name} duration is outside 0-15 seconds: {duration}")

	resource = (directory / f"{prefix}_SPRITE_FRAMES.tres").read_text(encoding="utf-8")
	for animation in animations:
		if f'&"{animation}"' not in resource:
			fail(f"SpriteFrames resource omits {animation}")
	print(f"OK: {character_id} atlas, 8 cells, 3 GIF loops, 3 silent MP4 loops, SpriteFrames")


def main() -> None:
	manifest_path = CHARACTERS / "EMBER_ROYALS_ANIMATION_MANIFEST.json"
	manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
	if manifest.get("schema") != "mermaid-roshan-ember-royals-animation-v1":
		fail("animation manifest schema mismatch")
	for character_id, (prefix, animations) in EXPECTED.items():
		validate_character(character_id, prefix, animations)
	paired_entries = manifest.get("paired_previews", [])
	if len(paired_entries) != 1:
		fail("animation manifest must contain exactly one paired preview")
	if paired_entries[0].get("prince_height_relative_to_king") != 0.8:
		fail("paired preview must lock Prince height to 4/5 of King height")

	for suffix in ("gif", "mp4"):
		path = CHARACTERS / f"EMBER_ROYALS_family_walk.{suffix}"
		if not path.is_file():
			fail(f"missing paired preview {path.name}")
	paired_video = ffprobe(CHARACTERS / "EMBER_ROYALS_family_walk.mp4")
	duration = float(paired_video.get("format", {}).get("duration", 0.0))
	if duration <= 0.0 or duration > 15.0:
		fail(f"paired preview duration is outside 0-15 seconds: {duration}")
	print("OK: paired family walk preview")
	print("RESULT: EMBER_ROYALS_ANIMATION_PACKAGE_OK")


if __name__ == "__main__":
	try:
		main()
	except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
		fail(str(error))
