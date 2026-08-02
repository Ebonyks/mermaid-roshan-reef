from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SOURCE = Path("tmp/pdfs/mermaid_roshan_motif_review")
PAGES = sorted(SOURCE.glob("page-*.jpg"))
CELL_W = 420
CELL_H = 620
LABEL_H = 34

for start in range(0, len(PAGES), 9):
	group = PAGES[start:start + 9]
	sheet = Image.new("RGB", (CELL_W * 3, (CELL_H + LABEL_H) * 3), "#d9eef2")
	draw = ImageDraw.Draw(sheet)
	for offset, path in enumerate(group):
		with Image.open(path) as source:
			page = source.convert("RGB")
			page.thumbnail((CELL_W - 16, CELL_H - 16), Image.Resampling.LANCZOS)
			x = (offset % 3) * CELL_W + (CELL_W - page.width) // 2
			y = (offset // 3) * (CELL_H + LABEL_H) + LABEL_H + (CELL_H - page.height) // 2
			sheet.paste(page, (x, y))
		page_number = start + offset + 1
		draw.text(((offset % 3) * CELL_W + 10, (offset // 3) * (CELL_H + LABEL_H) + 8), f"Page {page_number}", fill="#222e44")
	sheet.save(SOURCE / f"contact_{start + 1:02d}_{start + len(group):02d}.jpg", quality=90, optimize=True)
