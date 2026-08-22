#!/usr/bin/env python3
"""Build the Ember Royals runtime atlases and timed review loops.

The built-in image generator sometimes renders its transparency preview as a
neutral checkerboard. This builder removes only the border-connected bright
neutral field, preserving enclosed pale character details. It keeps the
eight-cell utility atlas and builds each walk from two consecutive 4x2 source
sheets into a dedicated 16-cell power-of-two atlas. It exports every cell and
assembles silent 16:9 MP4 and GIF review loops.
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


BASE_ATLAS_SIZE = (1024, 768)
BASE_CELL_SIZE = (256, 384)
WALK_ATLAS_SIZE = (2048, 1024)
WALK_CELL_SIZE = (256, 512)
WALK_COLUMNS = 8
WALK_BASELINE_Y = 440
REVIEW_SIZE = (1024, 576)
GIF_SIZE = (512, 288)
PRINCE_HEIGHT_RELATIVE_TO_KING = 0.8
PAIR_KING_SCALE = 1.5
PAIR_GROUND_Y = 520


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
		SequenceSpec(
			"cape_fan", (6, 7, 7, 6, 0), (360, 460, 260, 360, 800), 2.20, False
		),
	),
	"ember_prince": (
		SequenceSpec("idle_glance", (0, 1, 0), (850, 500, 850), 1.35),
		SequenceSpec("cinderstep", (6, 7, 7, 0), (180, 260, 180, 720), 3.00, False),
	),
}

WALK_SPECS: dict[str, SequenceSpec] = {
	"ember_king": SequenceSpec("heavy_walk", tuple(range(16)), (100,) * 16, 10.0),
	"ember_prince": SequenceSpec("sleek_walk", tuple(range(16)), (70,) * 16, 14.285714),
}


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def alpha_height(image: Image.Image) -> int:
	bbox = image.getchannel("A").getbbox()
	if bbox is None:
		raise ValueError("animation frame must not be empty")
	return bbox[3] - bbox[1]


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


def normalize_frames(
	frames: list[Image.Image],
	cell_size: tuple[int, int] = BASE_CELL_SIZE,
	target_height: int | None = None,
	baseline: int | None = None,
) -> list[Image.Image]:
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

	available_width = cell_size[0] - 18
	available_height = cell_size[1] - 20
	if target_height is not None:
		available_height = min(available_height, target_height)
	scale = min(available_width / max(widths), available_height / max(heights))
	if baseline is None:
		baseline = cell_size[1] - 8
	output: list[Image.Image] = []
	for item in cropped:
		new_size = (
			max(1, round(item.width * scale)),
			max(1, round(item.height * scale)),
		)
		item = item.resize(new_size, Image.Resampling.LANCZOS)
		cell = Image.new("RGBA", cell_size, (0, 0, 0, 0))
		x = (cell_size[0] - item.width) // 2
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
	available_width = BASE_CELL_SIZE[0] - 18
	available_height = BASE_CELL_SIZE[1] - 20
	scale = min(available_width / item.width, available_height / item.height)
	item = item.resize(
		(max(1, round(item.width * scale)), max(1, round(item.height * scale))),
		Image.Resampling.LANCZOS,
	)
	cell = Image.new("RGBA", BASE_CELL_SIZE, (0, 0, 0, 0))
	cell.alpha_composite(
		item,
		((BASE_CELL_SIZE[0] - item.width) // 2, BASE_CELL_SIZE[1] - 8 - item.height),
	)
	return cell


def write_base_atlas(frames: list[Image.Image], directory: Path, prefix: str) -> Path:
	frame_dir = directory / "frames"
	frame_dir.mkdir(parents=True, exist_ok=True)
	atlas = Image.new("RGBA", BASE_ATLAS_SIZE, (0, 0, 0, 0))
	for index, frame in enumerate(frames):
		column = index % 4
		row = index // 4
		atlas.alpha_composite(
			frame,
			(column * BASE_CELL_SIZE[0], row * BASE_CELL_SIZE[1]),
		)
		frame.save(frame_dir / f"{prefix}_frame_{index + 1:02d}.png", optimize=True)
	atlas_path = directory / f"{prefix}_RUNTIME_ATLAS.png"
	atlas.save(atlas_path, optimize=True)
	return atlas_path


def write_walk_atlas(frames: list[Image.Image], directory: Path, prefix: str) -> Path:
	frame_dir = directory / "walk_frames"
	frame_dir.mkdir(parents=True, exist_ok=True)
	atlas = Image.new("RGBA", WALK_ATLAS_SIZE, (0, 0, 0, 0))
	for index, frame in enumerate(frames):
		column = index % WALK_COLUMNS
		row = index // WALK_COLUMNS
		atlas.alpha_composite(
			frame,
			(column * WALK_CELL_SIZE[0], row * WALK_CELL_SIZE[1]),
		)
		frame.save(frame_dir / f"{prefix}_walk_{index + 1:02d}.png", optimize=True)
	atlas_path = directory / f"{prefix}_WALK_ATLAS.png"
	atlas.save(atlas_path, optimize=True)
	return atlas_path


def write_spriteframes_resource(character_id: str, directory: Path, prefix: str) -> Path:
	lines = [
		"[gd_resource type=\"SpriteFrames\" load_steps=27 format=3]",
		"",
		f"[ext_resource type=\"Texture2D\" path=\"res://{(directory / f'{prefix}_RUNTIME_ATLAS.png').as_posix()}\" id=\"1_base\"]",
		f"[ext_resource type=\"Texture2D\" path=\"res://{(directory / f'{prefix}_WALK_ATLAS.png').as_posix()}\" id=\"2_walk\"]",
		"",
	]
	for index in range(8):
		column = index % 4
		row = index // 4
		lines.extend(
			[
				f"[sub_resource type=\"AtlasTexture\" id=\"Base_{index + 1:02d}\"]",
				"atlas = ExtResource(\"1_base\")",
				f"region = Rect2({column * BASE_CELL_SIZE[0]}, {row * BASE_CELL_SIZE[1]}, {BASE_CELL_SIZE[0]}, {BASE_CELL_SIZE[1]})",
				"",
			]
		)
	for index in range(16):
		column = index % WALK_COLUMNS
		row = index // WALK_COLUMNS
		lines.extend(
			[
				f"[sub_resource type=\"AtlasTexture\" id=\"Walk_{index + 1:02d}\"]",
				"atlas = ExtResource(\"2_walk\")",
				f"region = Rect2({column * WALK_CELL_SIZE[0]}, {row * WALK_CELL_SIZE[1]}, {WALK_CELL_SIZE[0]}, {WALK_CELL_SIZE[1]})",
				"",
			]
		)

	def animation_dictionary(spec: SequenceSpec, frame_prefix: str) -> str:
		frame_entries = ", ".join(
			f'{{"duration": 1.0, "texture": SubResource("{frame_prefix}_{index + 1:02d}")}}'
			for index in spec.indices
		)
		loop = "true" if spec.loop else "false"
		return (
			"{\n"
			f'"frames": [{frame_entries}],\n'
			f'"loop": {loop},\n'
			f'"name": &"{spec.name}",\n'
			f'"speed": {spec.fps:.6f}\n'
			"}"
		)

	animation_blocks = [
		animation_dictionary(spec, "Base") for spec in CHARACTER_SPECS[character_id]
	]
	animation_blocks.append(animation_dictionary(WALK_SPECS[character_id], "Walk"))
	resource_name = "".join(part.title() for part in character_id.split("_")) + "SpriteFrames"
	lines.extend(
		[
			"[resource]",
			f'resource_name = "{resource_name}"',
			"animations = [" + ", ".join(animation_blocks) + "]",
		]
	)
	resource_path = directory / f"{prefix}_SPRITE_FRAMES.tres"
	resource_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
	return resource_path


def make_review_frame(frame: Image.Image, title_color: tuple[int, int, int]) -> Image.Image:
	canvas = Image.new("RGB", REVIEW_SIZE, (249, 246, 252))
	draw = ImageDraw.Draw(canvas)
	draw.ellipse((322, 505, 702, 548), fill=(226, 216, 238))
	bbox = frame.getchannel("A").getbbox()
	if bbox is None:
		raise ValueError("review frame must not be empty")
	figure = frame.crop(bbox)
	scale = min(320 / figure.width, 480 / figure.height)
	figure = figure.resize(
		(round(figure.width * scale), round(figure.height * scale)),
		Image.Resampling.LANCZOS,
	)
	position = ((REVIEW_SIZE[0] - figure.width) // 2, 528 - figure.height)
	canvas.paste(figure.convert("RGB"), position, figure.getchannel("A"))
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
	walk_sources: tuple[Path, Path],
	output_root: Path,
	frame_eight_source: Path | None = None,
) -> tuple[dict[str, object], list[Image.Image], list[Image.Image]]:
	prefix = character_id.upper()
	directory = output_root / character_id
	animation_dir = directory / "animations"
	animation_dir.mkdir(parents=True, exist_ok=True)
	frames = normalize_frames(split_source(source))
	if frame_eight_source is not None:
		frames[7] = normalize_single_frame(frame_eight_source)
	neutral_bbox = frames[0].getchannel("A").getbbox()
	if neutral_bbox is None:
		raise ValueError(f"{character_id} neutral frame must not be empty")
	neutral_height = neutral_bbox[3] - neutral_bbox[1]
	walk_source_frames = split_source(walk_sources[0]) + split_source(walk_sources[1])
	walk_frames = normalize_frames(
		walk_source_frames,
		WALK_CELL_SIZE,
		target_height=neutral_height,
		baseline=WALK_BASELINE_Y,
	)
	atlas = write_base_atlas(frames, directory, prefix)
	walk_atlas = write_walk_atlas(walk_frames, directory, prefix)
	write_spriteframes_resource(character_id, directory, prefix)
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
	walk_spec = WALK_SPECS[character_id]
	walk_gif_path = animation_dir / f"{prefix}_{walk_spec.name}.gif"
	walk_mp4_path = animation_dir / f"{prefix}_{walk_spec.name}.mp4"
	write_gif(walk_frames, walk_spec, walk_gif_path, color)
	write_mp4(walk_frames, walk_spec, walk_mp4_path, color)
	animations.append(
		{
			"name": walk_spec.name,
			"frame_indices_zero_based": list(walk_spec.indices),
			"durations_ms": list(walk_spec.durations_ms),
			"spriteframes_fps": walk_spec.fps,
			"loop": walk_spec.loop,
			"gif": walk_gif_path.name,
			"mp4": walk_mp4_path.name,
			"gif_sha256": sha256(walk_gif_path),
			"mp4_sha256": sha256(walk_mp4_path),
		}
	)
	result: dict[str, object] = {
		"character_id": character_id,
		"source_master_sha256": sha256(source),
		"walk_source_master_sha256": [sha256(path) for path in walk_sources],
		"runtime_atlas": atlas.name,
		"runtime_atlas_sha256": sha256(atlas),
		"atlas_size": list(BASE_ATLAS_SIZE),
		"cell_size": list(BASE_CELL_SIZE),
		"walk_runtime_atlas": walk_atlas.name,
		"walk_runtime_atlas_sha256": sha256(walk_atlas),
		"walk_atlas_size": list(WALK_ATLAS_SIZE),
		"walk_cell_size": list(WALK_CELL_SIZE),
		"walk_frame_count": len(walk_frames),
		"animations": animations,
	}
	if frame_eight_source is not None:
		result["frame_eight_replacement_sha256"] = sha256(frame_eight_source)
	return result, frames, walk_frames


def make_pair_review_frame(
	king: Image.Image,
	prince: Image.Image,
	king_scale: float,
	prince_scale: float,
) -> Image.Image:
	canvas = Image.new("RGB", REVIEW_SIZE, (249, 246, 252))
	draw = ImageDraw.Draw(canvas)
	draw.rectangle((0, 0, REVIEW_SIZE[0], 8), fill=(112, 45, 82))
	draw.rectangle((0, 520, REVIEW_SIZE[0], REVIEW_SIZE[1]), fill=(233, 222, 241))
	draw.ellipse((160, 495, 520, 538), fill=(215, 199, 229))
	draw.ellipse((600, 505, 790, 533), fill=(221, 207, 234))
	king_size = (
		round(WALK_CELL_SIZE[0] * king_scale),
		round(WALK_CELL_SIZE[1] * king_scale),
	)
	prince_size = (
		round(WALK_CELL_SIZE[0] * prince_scale),
		round(WALK_CELL_SIZE[1] * prince_scale),
	)
	king_figure = king.resize(king_size, Image.Resampling.LANCZOS)
	prince_figure = prince.resize(prince_size, Image.Resampling.LANCZOS)
	king_position = (
		332 - king_size[0] // 2,
		PAIR_GROUND_Y - round(WALK_BASELINE_Y * king_scale),
	)
	prince_position = (
		710 - prince_size[0] // 2,
		PAIR_GROUND_Y - round(WALK_BASELINE_Y * prince_scale),
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
	king_neutral: Image.Image,
	prince_neutral: Image.Image,
	king_walk_frames: list[Image.Image],
	prince_walk_frames: list[Image.Image],
	output_root: Path,
) -> dict[str, object]:
	# Eighty-millisecond ticks give the Prince one frame per tick. The King
	# advances four frames per five ticks, yielding 12.5 fps versus 10 fps. The
	# 80-tick loop is the least common multiple of their 16/20-tick cycles.
	king_bbox = king_neutral.getchannel("A").getbbox()
	prince_bbox = prince_neutral.getchannel("A").getbbox()
	if king_bbox is None or prince_bbox is None:
		raise ValueError("paired scale authority frames must not be empty")
	king_height = king_bbox[3] - king_bbox[1]
	prince_height = prince_bbox[3] - prince_bbox[1]
	king_walk_height = max(alpha_height(frame) for frame in king_walk_frames)
	prince_walk_height = max(alpha_height(frame) for frame in prince_walk_frames)
	king_target_height = king_height * PAIR_KING_SCALE
	king_scale = king_target_height / king_walk_height
	prince_target_height = king_target_height * PRINCE_HEIGHT_RELATIVE_TO_KING
	prince_scale = prince_target_height / prince_walk_height
	durations = [80] * 80
	images = [
		make_pair_review_frame(
			king_walk_frames[(tick * 4 // 5) % 16],
			prince_walk_frames[tick % 16],
			king_scale,
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
		"timing_note": "16-frame cycles; King 10 fps, Prince 12.5 fps in paired review",
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
	parser.add_argument("--king-walk-a", type=Path, required=True)
	parser.add_argument("--king-walk-b", type=Path, required=True)
	parser.add_argument("--prince-source", type=Path, required=True)
	parser.add_argument("--prince-walk-a", type=Path, required=True)
	parser.add_argument("--prince-walk-b", type=Path, required=True)
	parser.add_argument("--output-root", type=Path, required=True)
	args = parser.parse_args()
	args.output_root.mkdir(parents=True, exist_ok=True)
	king_manifest, king_frames, king_walk_frames = build_character(
		"ember_king",
		args.king_source,
		(args.king_walk_a, args.king_walk_b),
		args.output_root,
		args.king_frame_eight,
	)
	prince_manifest, prince_frames, prince_walk_frames = build_character(
		"ember_prince",
		args.prince_source,
		(args.prince_walk_a, args.prince_walk_b),
		args.output_root,
	)
	manifest = {
		"schema": "mermaid-roshan-ember-royals-animation-v2",
		"render_target": "2D limited animation; silent review clips",
		"characters": [king_manifest, prince_manifest],
		"paired_previews": [
			write_pair_preview(
				king_frames[0],
				prince_frames[0],
				king_walk_frames,
				prince_walk_frames,
				args.output_root,
			)
		],
	}
	manifest_path = args.output_root / "EMBER_ROYALS_ANIMATION_MANIFEST.json"
	manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
	main()
