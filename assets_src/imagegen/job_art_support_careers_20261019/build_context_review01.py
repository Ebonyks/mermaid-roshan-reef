"""Diagnostic contact sheets only; original capture pixels remain untouched."""
from pathlib import Path
import hashlib, json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[3]
source = Path(__file__).resolve().parent
out = source / 'review_context01'
assert not out.exists()
out.mkdir()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
records = []
for version in ['current04', 'current07']:
    manifest = source / ('review_' + version) / 'capture.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    for row in data['captures']:
        herd = row['id'].startswith('farmer-2-herd-')
        if (version == 'current04' and herd) or (version == 'current07' and not herd):
            continue
        p = root / row['path']
        records.append({**row, 'capture_manifest':manifest.relative_to(root).as_posix(), 'sha256':sha(p)})
pages = []
for start in range(0, len(records), 6):
    page = Image.new('RGB', (1600, 1260), '#e7e1da')
    d = ImageDraw.Draw(page)
    subset = records[start:start+6]
    for slot, row in enumerate(subset):
        x, y = (slot % 2) * 800, (slot // 2) * 420
        d.text((x+8,y+6), row['id'], fill='black')
        im = Image.open(root / row['path']).convert('RGB')
        thumb = im.copy(); thumb.thumbnail((270, 170))
        page.paste(thumb, (x+5,y+40))
        ox,oy = row['canvas_origin']; sx,sy = row['canvas_scale']; w,h=row['surface_size']
        box = (max(0,round(ox-20)),max(0,round(oy-20)),min(im.width,round(ox+w*sx+20)),min(im.height,round(oy+h*sy+20)))
        crop=im.crop(box); crop.thumbnail((510,370))
        page.paste(crop,(x+285,y+35))
        row['diagnostic_crop_box'] = list(box)
        d.text((x+8,y+220), 'Scene + HUD left / activity detail right', fill='black')
        d.text((x+8,y+240), 'Configured Mobile GUI; no canonical/device claim', fill='black')
    path=out/('context_%02d.png' % (len(pages)+1))
    page.save(path)
    pages.append({'path':path.relative_to(root).as_posix(),'sha256':sha(path),'captures':[r['id'] for r in subset]})
(out/'manifest.json').write_text(json.dumps({'role':'diagnostic_only','review_status':'NOT_YET_REVIEWED','limits':'current04 non-HERD functions unchanged; current07 refreshed HERD. Original captures and exact source receipts retained.','captures':records,'pages':pages},indent=2)+'\n',encoding='utf-8')
print(len(records),'frames',len(pages),'pages')
