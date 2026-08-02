"""Build and audit the shared water-FX atlas vocabulary.

The reviewed ImageGen chroma masters and their keyed alpha counterparts are
preserved under ``assets_src``.  This builder performs only deterministic atlas
packing: whole-cell resolution normalization, fixed-pivot alignment for the
splash/ripple families, the reviewed medium-splash frame selection, and the
static foamline strip crop.  It never synthesizes in-between motion.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageStat


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets_src" / "imagegen" / "water_fx_2026-08-02"
OUTPUT_DIR = ROOT / "assets" / "sprites" / "fx_water"
FRAME_COUNT = 8
CELL_MARGIN = 4
RUNTIME_SATURATION = 0.70
SATURATION_LIMIT = 0.428


@dataclass(frozen=True)
class AtlasSpec:
	name: str
	grid: tuple[int, int]
	size: tuple[int, int]
	pivot: str
	selected_cells: tuple[int, ...] = tuple(range(FRAME_COUNT))
	cell_scale: float = 1.0

	@property
	def source_path(self) -> Path:
		return SOURCE_DIR / f"{self.name}_alpha_native.png"

	@property
	def output_path(self) -> Path:
		return OUTPUT_DIR / f"{self.name}_atlas.png"


SPECS: tuple[AtlasSpec, ...] = (
	AtlasSpec("fx_water_splash_small", (4, 2), (1024, 512), "bottom"),
	# The reviewed native candidate supplied nine painted beats.  Cell 7 is a
	# redundant foam hold; cell 8 is the stronger final settling ring.
	AtlasSpec(
		"fx_water_splash_medium",
		(3, 3),
		(1024, 1024),
		"bottom",
		(0, 1, 2, 3, 4, 5, 6, 8),
	),
	AtlasSpec("fx_water_splash_breach", (3, 3), (1024, 1024), "bottom"),
	AtlasSpec(
		"fx_water_ripple_ring", (4, 2), (1024, 512), "center",
		cell_scale=0.94,
	),
	AtlasSpec("fx_water_bubble_burst", (4, 2), (1024, 512), "source"),
)


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _cell_box(
		size: tuple[int, int], grid: tuple[int, int], index: int,
) -> tuple[int, int, int, int]:
	column = index % grid[0]
	row = index // grid[0]
	left = round(column * size[0] / grid[0])
	top = round(row * size[1] / grid[1])
	right = round((column + 1) * size[0] / grid[0])
	bottom = round((row + 1) * size[1] / grid[1])
	return left, top, right, bottom


def _clean_transparent_rgb(image: Image.Image) -> Image.Image:
	image = image.convert("RGBA")
	transparent = Image.eval(image.getchannel("A"), lambda value: 255 if value == 0 else 0)
	black = Image.new("RGBA", image.size)
	image.paste(black, mask=transparent)
	return image


def _runtime_grade(image: Image.Image) -> Image.Image:
	"""Keep effects at or below the strictest declared standee color band."""
	alpha = image.getchannel("A")
	graded = ImageEnhance.Color(image.convert("RGB")).enhance(RUNTIME_SATURATION)
	graded.putalpha(alpha)
	return graded



def _shift_for_pivot(
		frame: Image.Image, pivot: str,
) -> tuple[int, int]:
	bbox = frame.getchannel("A").getbbox()
	if bbox is None:
		raise ValueError("generated frame has no visible pixels")
	width, height = frame.size
	if pivot == "bottom":
		dx = round((width - 1) * 0.5 - (bbox[0] + bbox[2] - 1) * 0.5)
		dy = height - CELL_MARGIN - bbox[3]
	elif pivot == "center":
		dx = round((width - 1) * 0.5 - (bbox[0] + bbox[2] - 1) * 0.5)
		dy = round((height - 1) * 0.5 - (bbox[1] + bbox[3] - 1) * 0.5)
	elif pivot == "source":
		return 0, 0
	else:
		raise ValueError(f"unknown pivot mode: {pivot}")

	# Preserve the requested transparent cell border even after alignment.
	dx = max(CELL_MARGIN - bbox[0], min(dx, width - CELL_MARGIN - bbox[2]))
	dy = max(CELL_MARGIN - bbox[1], min(dy, height - CELL_MARGIN - bbox[3]))
	return dx, dy


def _normalized_frame(
		source_cell: Image.Image,
		destination_size: tuple[int, int],
		pivot: str,
		cell_scale: float,
) -> Image.Image:
	source_cell = _clean_transparent_rgb(source_cell)
	resized_size = (
		max(1, round(destination_size[0] * cell_scale)),
		max(1, round(destination_size[1] * cell_scale)),
	)
	resized_inner = source_cell.resize(resized_size, Image.Resampling.LANCZOS)
	resized = Image.new("RGBA", destination_size)
	resized.alpha_composite(resized_inner, (
		(destination_size[0] - resized_size[0]) // 2,
		(destination_size[1] - resized_size[1]) // 2,
	))
	dx, dy = _shift_for_pivot(resized, pivot)
	frame = Image.new("RGBA", destination_size)
	frame.alpha_composite(resized, (dx, dy))
	return frame


def _build_atlas(spec: AtlasSpec) -> None:
	with Image.open(spec.source_path) as opened:
		source = opened.convert("RGBA")
	atlas = Image.new("RGBA", spec.size)
	for output_index, source_index in enumerate(spec.selected_cells):
		source_box = _cell_box(source.size, spec.grid, source_index)
		destination_box = _cell_box(spec.size, spec.grid, output_index)
		destination_size = (
			destination_box[2] - destination_box[0],
			destination_box[3] - destination_box[1],
		)
		frame = _normalized_frame(
			source.crop(source_box), destination_size, spec.pivot, spec.cell_scale)
		atlas.alpha_composite(frame, destination_box[:2])
	spec.output_path.parent.mkdir(parents=True, exist_ok=True)
	atlas = _runtime_grade(atlas)
	atlas.save(spec.output_path, optimize=True, compress_level=9)


def _build_foamline() -> Path:
	source_path = SOURCE_DIR / "fx_water_foamline_alpha_native.png"
	output_path = OUTPUT_DIR / "fx_water_foamline_strip.png"
	with Image.open(source_path) as opened:
		source = _clean_transparent_rgb(opened)
	scaled_height = round(source.height * 1024 / source.width)
	scaled = source.resize((1024, scaled_height), Image.Resampling.LANCZOS)
	bbox = scaled.getchannel("A").getbbox()
	if bbox is None:
		raise ValueError("foamline source has no visible pixels")
	strip = Image.new("RGBA", (1024, 256))
	strip.alpha_composite(scaled, (0, CELL_MARGIN - bbox[1]))
	output_path.parent.mkdir(parents=True, exist_ok=True)
	strip = _runtime_grade(strip)
	strip.save(output_path, optimize=True, compress_level=9)
	return output_path


def _frame_difference(first: Image.Image, second: Image.Image) -> float:
	first = first.resize((128, 128), Image.Resampling.LANCZOS)
	second = second.resize((128, 128), Image.Resampling.LANCZOS)
	difference = ImageChops.difference(first, second)
	return sum(ImageStat.Stat(difference).mean) / 4.0



def _mean_opaque_saturation(image: Image.Image) -> float:
	mask = image.getchannel("A").point(lambda value: 255 if value > 127 else 0)
	saturation = image.convert("RGB").convert("HSV").getchannel("S")
	return ImageStat.Stat(saturation, mask=mask).mean[0] / 255.0

def _audit_atlas(spec: AtlasSpec) -> None:
	with Image.open(spec.output_path) as opened:
		atlas = opened.convert("RGBA")
	if atlas.size != spec.size:
		raise ValueError(f"{spec.name}: expected {spec.size}, got {atlas.size}")
	if atlas.getpixel((0, 0))[3] != 0:
		raise ValueError(f"{spec.name}: top-left corner is not transparent")
	frames: list[Image.Image] = []
	pivot_samples: list[float] = []
	saturation = _mean_opaque_saturation(atlas)
	if saturation > SATURATION_LIMIT:
		raise ValueError(
			f"{spec.name}: saturation {saturation:.4f} exceeds {SATURATION_LIMIT}")

	for index in range(FRAME_COUNT):
		box = _cell_box(spec.size, spec.grid, index)
		frame = atlas.crop(box)
		bbox = frame.getchannel("A").getbbox()
		if bbox is None:
			raise ValueError(f"{spec.name}: frame {index} is empty")
		if (
			bbox[0] < 2 or bbox[1] < 2
			or bbox[2] > frame.width - 2 or bbox[3] > frame.height - 2
		):
			raise ValueError(
				f"{spec.name}: frame {index} violates the clear cell border: {bbox}")
		if spec.pivot == "bottom":
			pivot_samples.append(bbox[3] / frame.height)
		elif spec.pivot == "center":
			center_x = (bbox[0] + bbox[2] - 1) * 0.5 / frame.width
			center_y = (bbox[1] + bbox[3] - 1) * 0.5 / frame.height
			if abs(center_x - 0.5) > 0.01 or abs(center_y - 0.5) > 0.01:
				raise ValueError(
					f"{spec.name}: frame {index} center drift {(center_x, center_y)}")
		frames.append(frame)
	if pivot_samples and max(pivot_samples) - min(pivot_samples) > 0.005:
		raise ValueError(f"{spec.name}: bottom pivot drift {pivot_samples}")
	for index in range(1, len(frames)):
		if _frame_difference(frames[index - 1], frames[index]) < 0.8:
			raise ValueError(f"{spec.name}: frames {index - 1}/{index} are too similar")
	if spec.grid == (3, 3):
		unused = atlas.crop(_cell_box(spec.size, spec.grid, 8))
		if unused.getchannel("A").getbbox() is not None:
			raise ValueError(f"{spec.name}: trailing cell is not transparent")
	print(
		f"WATER_FX|OK|{spec.output_path.name}|size={atlas.width}x{atlas.height}"
		f"|grid={spec.grid[0]}x{spec.grid[1]}|sat={saturation:.4f}"
		f"|sha256={_sha256(spec.output_path)}")


def _audit_foamline(path: Path) -> None:
	with Image.open(path) as opened:
		strip = opened.convert("RGBA")
	if strip.size != (1024, 256):
		raise ValueError(f"foamline: expected 1024x256, got {strip.size}")
	alpha = strip.getchannel("A")
	bbox = alpha.getbbox()
	if bbox is None:
		raise ValueError("foamline: empty output")
	if bbox[0] < 8 or bbox[2] > strip.width - 8:
		raise ValueError(f"foamline: horizontal tile edges are not clear: {bbox}")
	if bbox[1] != CELL_MARGIN:
		raise ValueError(f"foamline: top-edge pivot drift: {bbox}")
	saturation = _mean_opaque_saturation(strip)
	if saturation > SATURATION_LIMIT:
		raise ValueError(
			f"foamline: saturation {saturation:.4f} exceeds {SATURATION_LIMIT}")
	print(
		f"WATER_FX|OK|{path.name}|size={strip.width}x{strip.height}"
		f"|grid=1x1|sat={saturation:.4f}|sha256={_sha256(path)}")



def main() -> None:
	for spec in SPECS:
		_build_atlas(spec)
	foamline_path = _build_foamline()
	for spec in SPECS:
		_audit_atlas(spec)
	_audit_foamline(foamline_path)
	print("WATER_FX|RESULT=OK|atlases=6|animated_frames=40")


if __name__ == "__main__":
	main()
