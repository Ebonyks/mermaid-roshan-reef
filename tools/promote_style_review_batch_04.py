"""Promote approved Batch 04 review art into runtime-safe texture roles."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src" / "style_review_batch_04" / "final"


def fit_on_canvas(image: Image.Image, size: tuple[int, int], padding: int) -> Image.Image:
	available = (size[0] - padding * 2, size[1] - padding * 2)
	image = image.copy()
	image.thumbnail(available, Image.Resampling.LANCZOS)
	canvas = Image.new("RGBA", size, (0, 0, 0, 0))
	canvas.alpha_composite(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
	return canvas


def main() -> None:
	leaf_sheet = Image.open(SOURCE / "005_leaf_tropical_sheet.png").convert("RGBA")
	# Crossed-card UVs need one readable silhouette, not the four-item concept sheet.
	leaf = leaf_sheet.crop((20, 35, 310, 625))
	fit_on_canvas(leaf, (512, 1024), 22).save(ROOT / "assets" / "terrain" / "leaf.png")

	rainbow = Image.open(SOURCE / "015_rainbow_swatch_fin.png").convert("RGBA")
	fit_on_canvas(rainbow, (512, 512), 12).save(ROOT / "assets" / "mg" / "rainbow_swatch.png")

	# Keep the reviewed layers in full-square registration with the current line.
	# The complete three-layer fish remains replaceable in a future art pass.
	for source_name, runtime_name in (
		("006_fish_body_layer.png", "fish_body.png"),
		("007_fish_fins_layer.png", "fish_fins.png"),
	):
		layer = Image.open(SOURCE / source_name).convert("RGBA")
		layer.resize((512, 512), Image.Resampling.LANCZOS).save(ROOT / "assets" / "mg" / runtime_name)

	kart_sheet = Image.open(SOURCE / "021_kart_motif_sheet.png").convert("RGBA")
	kart_dir = ROOT / "assets" / "kart"
	kart_dir.mkdir(parents=True, exist_ok=True)
	finish = kart_sheet.crop((30, 35, 995, 245))
	fit_on_canvas(finish, (1024, 256), 8).save(kart_dir / "finish_banner.png")
	boost = kart_sheet.crop((35, 245, 995, 430))
	fit_on_canvas(boost, (1024, 256), 8).save(kart_dir / "boost_ribbon.png")


if __name__ == "__main__":
	main()
