from pathlib import Path

from PIL import Image, ImageDraw


root = Path(__file__).parents[1] / "assets_src" / "style_review_batch_04" / "final"
out = Path(__file__).parents[1] / "assets_src" / "style_review_batch_04" / "batch04_contact_sheet.png"
files = sorted(root.glob("*.png"))
cell_w, cell_h = 204, 168
cols = 5
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "#d7d7d7")
draw = ImageDraw.Draw(sheet)
for i, path in enumerate(files):

	with Image.open(path).convert("RGBA") as source:
		thumb = source.copy()
		thumb.thumbnail((cell_w - 12, cell_h - 34), Image.Resampling.LANCZOS)
		x = (i % cols) * cell_w + (cell_w - thumb.width) // 2
		y = (i // cols) * cell_h + 4
		checker = Image.new("RGB", thumb.size, "#f2f2f2")
		for yy in range(0, thumb.height, 8):
			for xx in range(0, thumb.width, 8):
				if ((xx // 8) + (yy // 8)) % 2:
					checker.paste("#c7c7c7", (xx, yy, min(xx + 8, thumb.width), min(yy + 8, thumb.height)))
		checker.paste(thumb, mask=thumb.getchannel("A"))
		sheet.paste(checker, (x, y))
		draw.text(((i % cols) * cell_w + 6, (i // cols) * cell_h + cell_h - 24), path.stem[:32], fill="#202020")
sheet.save(out, format="PNG", optimize=True)
print(out)
