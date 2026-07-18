#!/usr/bin/env python3
"""Build review galleries for model renders and normalized textures."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit" / "full_regen_2026-07-18"
MODEL_DIR = AUDIT / "renders" / "models"
TEXTURE_DIR = ROOT / "assets" / "full_texture_regen_2026-07-18" / "textures"
GALLERY_DIR = AUDIT / "galleries"
MANIFEST = ROOT / "assets" / "full_texture_regen_2026-07-18" / "model_manifest.json"
CELL = 256
LABEL = 42


def checker(size: tuple[int, int], block: int = 16) -> Image.Image:
	image = Image.new("RGB", size, (217, 234, 235))
	draw = ImageDraw.Draw(image)
	for y in range(0, size[1], block):
		for x in range(0, size[0], block):
			if (x // block + y // block) % 2:
				draw.rectangle((x, y, x + block - 1, y + block - 1), fill=(184, 207, 211))
	return image


def fit_image(path: Path, size: tuple[int, int], repeat: int = 1) -> Image.Image:
	with Image.open(path) as source:
		image = source.convert("RGBA")
	if repeat > 1:
		unit = image.resize((max(1, size[0] // repeat), max(1, size[1] // repeat)), Image.Resampling.LANCZOS)
		canvas = checker(size)
		for y in range(repeat):
			for x in range(repeat):
				canvas.paste(unit, (x * unit.width, y * unit.height), unit if "A" in unit.getbands() else None)
		return canvas
	image.thumbnail(size, Image.Resampling.LANCZOS)
	canvas = checker(size)
	position = ((size[0] - image.width) // 2, (size[1] - image.height) // 2)
	canvas.paste(image, position, image)
	return canvas


def make_pages(items: list[tuple[Path, str]], prefix: str, columns: int = 4, rows: int = 4,
		repeat: int = 1, cell_size: int = CELL, label_height: int = LABEL) -> list[str]:
	per_page = columns * rows
	outputs: list[str] = []
	font = ImageFont.load_default(size=13 if cell_size >= 200 else 10)
	for page_index in range(math.ceil(len(items) / per_page)):
		page_items = items[page_index * per_page:(page_index + 1) * per_page]
		page = Image.new("RGB", (columns * cell_size, rows * (cell_size + label_height)), (233, 243, 243))
		draw = ImageDraw.Draw(page)
		for item_index, (path, label) in enumerate(page_items):
			column = item_index % columns
			row = item_index // columns
			x = column * cell_size
			y = row * (cell_size + label_height)
			page.paste(fit_image(path, (cell_size, cell_size), repeat=repeat), (x, y))
			draw.rectangle((x, y + cell_size, x + cell_size, y + cell_size + label_height), fill=(244, 248, 248))
			draw.text((x + 5, y + cell_size + 4), label[:18 if cell_size < 200 else 36], fill=(45, 58, 78), font=font)
		output = GALLERY_DIR / f"{prefix}_{page_index + 1:02d}.png"
		page.save(output, optimize=True)
		outputs.append(output.relative_to(ROOT).as_posix())
	return outputs


def main() -> None:
	GALLERY_DIR.mkdir(parents=True, exist_ok=True)
	manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
	model_items = [(MODEL_DIR / f"{entry['name']}.png", f"{entry['role_id']} | {entry['name']}") for entry in manifest["assets"]]
	texture_paths = sorted(TEXTURE_DIR.glob("*.png"))
	texture_items = [(path, path.stem) for path in texture_paths]
	tile_items = [(path, path.stem) for path in texture_paths if path.stem.startswith(("R007_", "R008_", "R032_", "R033_", "R034_", "R044_", "R050_"))]
	model_pages = make_pages(model_items, "models", columns=4, rows=4)
	texture_pages = make_pages(texture_items, "textures", columns=4, rows=4)
	tile_pages = make_pages(tile_items, "texture_repetition", columns=4, rows=2, repeat=3)
	mobile_pages = make_pages(model_items, "models_phone_scale", columns=8, rows=6, cell_size=112, label_height=26)
	texture_mobile_pages = make_pages(texture_items, "textures_phone_scale", columns=7, rows=5, cell_size=112, label_height=26)
	summary = {
		"model_count": len(model_items),
		"texture_count": len(texture_items),
		"tile_count": len(tile_items),
		"model_pages": model_pages,
		"texture_pages": texture_pages,
		"tile_pages": tile_pages,
		"phone_scale_pages": mobile_pages,
		"texture_phone_scale_pages": texture_mobile_pages,
	}
	(AUDIT / "gallery_manifest.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
	print(json.dumps(summary, indent=2))


if __name__ == "__main__":
	main()
