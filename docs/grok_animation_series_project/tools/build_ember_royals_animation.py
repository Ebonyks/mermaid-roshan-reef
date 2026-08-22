#!/usr/bin/env python3
"""Build the Ember Royals runtime atlases and timed review loops.

The built-in image generator sometimes renders its transparency preview as a
neutral checkerboard. This builder removes only the border-connected bright
neutral field, preserving enclosed pale character details. It then normalizes
the exact 4x2 grid into stable 256x384 cells, writes a 1024x768 RGBA atlas,
exports each cell, and assembles silent 16:9 MP4 and GIF review loops.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


ATLAS_SIZE = (1024, 768)
CELL_SIZE = (256, 384)
REVIEW_SIZE = (1024, 576)
GIF_SIZE = (512, 288)
PRINCE_HEIGHT_RELATIVE_TO_KING = 0.8
PAIR_KING_SCALE = 1.5
PAIR_GROUND_Y = 520
PAIR_SOURCE_BASELINE_Y = 376


@dataclass(frozen=True)
class SequenceSpec:
	name: str
	indices: tuple[int, ...]
	durations_ms: tuple[int, ...]
	fps: float
	loop: bool = True


CHARACTER_SPECS: dict[str, tuple[SequenceSpec, ...]] = {
	"ember_king": (
		SequenceSpec("idle", (0, 1, 0), (900, 450, 850), 1.35),
		SequenceSpec("heavy_walk", (2, 3, 4, 5), (230, 230, 230, 230), 4.35),
		SequenceSpec("cape_fan", (6, 7, 7, 6, 0), (360, 460, 260, 360, 800), 2.20),
	),
	"ember_prince": (
		SequenceSpec("idle_glance", (0, 1, 0), (850, 500, 850), 1.35),
		SequenceSpec("sleek_walk", (2, 3, 4, 5), (160, 160, 160, 160), 6.25),
		SequenceSpec("cinderstep", (6, 7, 7, 0), (180, 260, 180, 720), 3.00),
	),
}


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _bright_neutral(pixel: tuple[int, int, int]) -> bool:
	low = min(pixel)
	high = max(pixel)
	return low >= 216 and high - low <= 14


def remove_connected_checkerboard(image: Image.Image) -> Image.Image:
	"""Remove the border-connected light checker field without global chroma loss."""
	rgb = image.convert("RGB")
	width, height = rgb.size
	pixels = rgb.load()
	visited = bytearray(width * height)
	queue: deque[tuple[int, int]] = deque()

	def enqueue(x: int, y: int) -> None:
		index = y * width + x
		if visited[index] or not _bright_neutral(pixels[x, y]):
			return
		visited[index] = 1
		queue.append((x, y))

	for x in range(width):
		enqueue(x, 0)
		enqueue(x, height - 1)
	for y in range(height):
		enqueue(0, y)
		enqueue(width - 1, y)

	while queue:
		x, y = queue.popleft()
		if x > 0:
			enqueue(x - 1, y)
		if x + 1 < width:
			enqueue(x + 1, y)
		if y > 0:
			enqueue(x, y - 1)
		if y + 1 < height:
			enqueue(x, y + 1)

	background = Image.new("L", (width, height), 0)
	background.putdata([255 if value else 0 for value in visited])
	# One-pixel expansion removes baked checker antialiasing; the soft blur keeps
	# authored contour edges from becoming harsh.
	background = background.filter(ImageFilter.MaxFilter(3))
	background = background.filter(ImageFilter.GaussianBlur(0.55))
	alpha = ImageOps.invert(background)
	alpha = alpha.point(lambda value: 0 if value < 10 else value)
	result = rgb.convert("RGBA")
	result.putalpha(alpha)
	return result


def split_source(source: Path) -> list[Image.Image]:
	image = Image.open(source).convert("RGB")
	width, height = image.size
	if width % 4 or height % 2:
		raise ValueError(f"{source} must be an exact 4x2 grid; received {image.size}")
	cell_width = width // 4
	cell_height = height // 2
	frames: list[Image.Image] = []
	for row in range(2):
		for column in range(4):
			box = (
				column * cell_width,
				row * cell_height,
				(column + 1) * cell_width,
				(row + 1) * cell_height,
			)
			frames.append(remove_connected_checkerboard(image.crop(box)))
	return frames


def normalize_frames(frames: list[Image.Image]) -> list[Image.Image]:
	cropped: list[Image.Image] = []
	widths: list[int] = []
	heights: list[int] = []
	for frame in frames:
		bbox = frame.getchannel("A").getbbox()
		if bbox is None:
			raise ValueError("A source cell became empty after background removal")
		item = frame.crop(bbox)
		cropped.append(item)
		widths.append(item.width)
		heights.append(item.height)

	available_width = CELL_SIZE[0] - 18
	available_height = CELL_SIZE[1] - 20
	scale = min(available_width / max(widths), available_height / max(heights))
	baseline = CELL_SIZE[1] - 8
	output: list[Image.Image] = []
	for item in cropped:
		new_size = (
			max(1, round(item.width * scale)),
			max(1, round(item.height * scale)),
		)
		item = item.resize(new_size, Image.Resampling.LANCZOS)
		cell = Image.new("RGBA", CELL_SIZE, (0, 0, 0, 0))
		x = (CELL_SIZE[0] - item.width) // 2
		y = baseline - item.height
		cell.alpha_composite(item, (x, y))
		output.append(cell)
	return output


def normalize_single_frame(source: Path) -> Image.Image:
	item = remove_connected_checkerboard(Image.open(source).convert("RGB"))
	bbox = item.getchannel("A").getbbox()
	if bbox is None:
		raise ValueError(f"{source} became empty after background removal")
	item = item.crop(bbox)
	available_width = CELL_SIZE[0] - 18
	available_height = CELL_SIZE[1] - 20
	scale = min(available_width / item.width, available_height / item.height)
	item = item.resize(
		(max(1, round(item.width * scale)), max(1, round(item.height * scale))),
		Image.Resampling.LANCZOS,
	)
	cell = Image.new("RGBA", CELL_SIZE, (0, 0, 0, 0))
	cell.alpha_composite(item, ((CELL_SIZE[0] - item.width) // 2, CELL_SIZE[1] - 8 - item.height))
	return cell


def write_atlas(frames: list[Image.Image], directory: Path, prefix: str) -> Path:
	frame_dir = directory / "frames"
	frame_dir.mkdir(parents=True, exist_ok=True)
	atlas = Image.new("RGBA", ATLAS_SIZE, (0, 0, 0, 0))
	for index, frame in enumerate(frames):
		column = index % 4
		row = index // 4
		atlas.alpha_composite(frame, (column * CELL_SIZE[0], row * CELL_SIZE[1]))
		frame.save(frame_dir / f"{prefix}_frame_{index + 1:02d}.png", optimize=True)
	atlas_path = directory / f"{prefix}_RUNTIME_ATLAS.png"
	atlas.save(atlas_path, optimize=True)
	return atlas_path


def make_review_frame(frame: Image.Image, title_color: tuple[int, int, int]) -> Image.Image:
	canvas = Image.new("RGB", REVIEW_SIZE, (249, 246, 252))
	draw = ImageDraw.Draw(canvas)
	draw.ellipse((322, 505, 702, 548), fill=(226, 216, 238))
	# Scale the normalized cell uniformly; the baseline remains fixed.
	figure = frame.resize((320, 480), Image.Resampling.LANCZOS)
	canvas.paste(figure.convert("RGB"), (352, 48), figure.getchannel("A"))
	draw.rectangle((0, 0, REVIEW_SIZE[0], 8), fill=title_color)
	return canvas


def expand_sequence(spec: SequenceSpec, minimum_ms: int = 3600) -> tuple[list[int], list[int]]:
	indices: list[int] = []
	durations: list[int] = []
	total = 0
	while total < minimum_ms:
		for index, duration in zip(spec.indices, spec.durations_ms):
			indices.append(index)
			durations.append(duration)
			total += duration
			if total >= minimum_ms:
				break
	return indices, durations


def write_gif(
	frames: list[Image.Image], spec: SequenceSpec, output: Path, color: tuple[int, int, int]
) -> None:
	indices, durations = expand_sequence(spec)
	images = [
		make_review_frame(frames[index], color).resize(GIF_SIZE, Image.Resampling.LANCZOS)
		for index in indices
	]
	images[0].save(
		output,
		save_all=True,
		append_images=images[1:],
		duration=durations,
		loop=0,
		optimize=False,
		disposal=2,
	)


def write_mp4(
	frames: list[Image.Image], spec: SequenceSpec, output: Path, color: tuple[int, int, int]
) -> None:
	ffmpeg = shutil.which("ffmpeg")
	if ffmpeg is None:
		raise RuntimeError("ffmpeg is required to build MP4 review loops")
	indices, durations = expand_sequence(spec)
	with tempfile.TemporaryDirectory(prefix="ember-animation-") as temp_name:
		temp = Path(temp_name)
		lines: list[str] = []
		last_path: Path | None = None
		for order, (index, duration) in enumerate(zip(indices, durations)):
			frame_path = temp / f"frame_{order:03d}.png"
			make_review_frame(frames[index], color).save(frame_path)
			lines.append(f"file '{frame_path.as_posix()}'")
			lines.append(f"duration {duration / 1000.0:.3f}")
			last_path = frame_path
		if last_path is not None:
			lines.append(f"file '{last_path.as_posix()}'")
		concat_path = temp / "frames.txt"
		concat_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
		subprocess.run(
			[
				ffmpeg,
				"-y",
				"-f",
				"concat",
				"-safe",
				"0",
				"-i",
				str(concat_path),
				"-vf",
				"fps=30,format=yuv420p",
				"-c:v",
				"libx264",
				"-preset",
				"medium",
				"-crf",
				"18",
				"-movflags",
				"+faststart",
				"-an",
				str(output),
			],
			check=True,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)


def build_character(
	character_id: str,
	source: Path,
	output_root: Path,
	frame_eight_source: Path | None = None,
) -> tuple[dict[str, object], list[Image.Image]]:
	prefix = character_id.upper()
	directory = output_root / character_id
	animation_dir = directory / "animations"
	animation_dir.mkdir(parents=True, exist_ok=True)
	frames = normalize_frames(split_source(source))
	if frame_eight_source is not None:
		frames[7] = normalize_single_frame(frame_eight_source)
	atlas = write_atlas(frames, directory, prefix)
	color = (120, 47, 75) if character_id == "ember_king" else (76, 46, 102)
	animations: list[dict[str, object]] = []
	for spec in CHARACTER_SPECS[character_id]:
		gif_path = animation_dir / f"{prefix}_{spec.name}.gif"
		mp4_path = animation_dir / f"{prefix}_{spec.name}.mp4"
		write_gif(frames, spec, gif_path, color)
		write_mp4(frames, spec, mp4_path, color)
		animations.append(
			{
				"name": spec.name,
				"frame_indices_zero_based": list(spec.indices),
				"durations_ms": list(spec.durations_ms),
				"spriteframes_fps": spec.fps,
				"loop": spec.loop,
				"gif": gif_path.name,
				"mp4": mp4_path.name,
				"gif_sha256": sha256(gif_path),
				"mp4_sha256": sha256(mp4_path),
			}
		)
	result: dict[str, object] = {
		"character_id": character_id,
		"source_master_sha256": sha256(source),
		"runtime_atlas": atlas.name,
		"runtime_atlas_sha256": sha256(atlas),
		"atlas_size": list(ATLAS_SIZE),
		"cell_size": list(CELL_SIZE),
		"animations": animations,
	}
	if frame_eight_source is not None:
		result["frame_eight_replacement_sha256"] = sha256(frame_eight_source)
	return result, frames


def make_pair_review_frame(
	king: Image.Image,
	prince: Image.Image,
	prince_scale: float,
) -> Image.Image:
	canvas = Image.new("RGB", REVIEW_SIZE, (249, 246, 252))
	draw = ImageDraw.Draw(canvas)
	draw.rectangle((0, 0, REVIEW_SIZE[0], 8), fill=(112, 45, 82))
	draw.rectangle((0, 520, REVIEW_SIZE[0], REVIEW_SIZE[1]), fill=(233, 222, 241))
	draw.ellipse((160, 495, 520, 538), fill=(215, 199, 229))
	draw.ellipse((600, 505, 790, 533), fill=(221, 207, 234))
	king_size = (
		round(CELL_SIZE[0] * PAIR_KING_SCALE),
		round(CELL_SIZE[1] * PAIR_KING_SCALE),
	)
	prince_size = (
		round(CELL_SIZE[0] * prince_scale),
		round(CELL_SIZE[1] * prince_scale),
	)
	king_figure = king.resize(king_size, Image.Resampling.LANCZOS)
	prince_figure = prince.resize(prince_size, Image.Resampling.LANCZOS)
	king_position = (
		332 - king_size[0] // 2,
		PAIR_GROUND_Y - round(PAIR_SOURCE_BASELINE_Y * PAIR_KING_SCALE),
	)
	prince_position = (
		710 - prince_size[0] // 2,
		PAIR_GROUND_Y - round(PAIR_SOURCE_BASELINE_Y * prince_scale),
	)
	canvas.paste(king_figure.convert("RGB"), king_position, king_figure.getchannel("A"))
	canvas.paste(prince_figure.convert("RGB"), prince_position, prince_figure.getchannel("A"))
	return canvas


def write_image_sequence_mp4(images: list[Image.Image], durations: list[int], output: Path) -> None:
	ffmpeg = shutil.which("ffmpeg")
	if ffmpeg is None:
		raise RuntimeError("ffmpeg is required to build MP4 review loops")
	with tempfile.TemporaryDirectory(prefix="ember-pair-animation-") as temp_name:
		temp = Path(temp_name)
		lines: list[str] = []
		last_path: Path | None = None
		for order, (image, duration) in enumerate(zip(images, durations)):
			frame_path = temp / f"frame_{order:03d}.png"
			image.save(frame_path)
			lines.append(f"file '{frame_path.as_posix()}'")
			lines.append(f"duration {duration / 1000.0:.3f}")
			last_path = frame_path
		if last_path is not None:
			lines.append(f"file '{last_path.as_posix()}'")
		concat_path = temp / "frames.txt"
		concat_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
		subprocess.run(
			[
				ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_path),
				"-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium",
				"-crf", "18", "-movflags", "+faststart", "-an", str(output),
			],
			check=True,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)


def write_pair_preview(
	king_frames: list[Image.Image], prince_frames: list[Image.Image], output_root: Path
) -> dict[str, object]:
	# Eighty-millisecond ticks let the King hold each walk key for three ticks
	# while the Prince holds each for two, making their cadence contrast literal.
	king_bbox = king_frames[0].getchannel("A").getbbox()
	prince_bbox = prince_frames[0].getchannel("A").getbbox()
	if king_bbox is None or prince_bbox is None:
		raise ValueError("paired scale authority frames must not be empty")
	king_height = king_bbox[3] - king_bbox[1]
	prince_height = prince_bbox[3] - prince_bbox[1]
	prince_scale = (
		PRINCE_HEIGHT_RELATIVE_TO_KING * king_height * PAIR_KING_SCALE / prince_height
	)
	durations = [80] * 45
	images = [
		make_pair_review_frame(
			king_frames[2 + (tick // 3) % 4],
			prince_frames[2 + (tick // 2) % 4],
			prince_scale,
		)
		for tick in range(len(durations))
	]
	gif_path = output_root / "EMBER_ROYALS_family_walk.gif"
	mp4_path = output_root / "EMBER_ROYALS_family_walk.mp4"
	gif_images = [image.resize(GIF_SIZE, Image.Resampling.LANCZOS) for image in images]
	gif_images[0].save(
		gif_path,
		save_all=True,
		append_images=gif_images[1:],
		duration=durations,
		loop=0,
		optimize=False,
		disposal=2,
	)
	write_image_sequence_mp4(images, durations, mp4_path)
	return {
		"name": "family_walk",
		"duration_ms": sum(durations),
		"timing_note": "King advances every 3 ticks; Prince advances every 2 ticks",
		"prince_height_relative_to_king": PRINCE_HEIGHT_RELATIVE_TO_KING,
		"gif": gif_path.name,
		"mp4": mp4_path.name,
		"gif_sha256": sha256(gif_path),
		"mp4_sha256": sha256(mp4_path),
	}


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--king-source", type=Path, required=True)
	parser.add_argument("--king-frame-eight", type=Path)
	parser.add_argument("--prince-source", type=Path, required=True)
	parser.add_argument("--output-root", type=Path, required=True)
	args = parser.parse_args()
	args.output_root.mkdir(parents=True, exist_ok=True)
	king_manifest, king_frames = build_character(
		"ember_king",
		args.king_source,
		args.output_root,
		args.king_frame_eight,
	)
	prince_manifest, prince_frames = build_character(
		"ember_prince",
		args.prince_source,
		args.output_root,
	)
	manifest = {
		"schema": "mermaid-roshan-ember-royals-animation-v1",
		"render_target": "2D limited animation; silent review clips",
		"characters": [king_manifest, prince_manifest],
		"paired_previews": [write_pair_preview(king_frames, prince_frames, args.output_root)],
	}
	manifest_path = args.output_root / "EMBER_ROYALS_ANIMATION_MANIFEST.json"
	manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
	main()
