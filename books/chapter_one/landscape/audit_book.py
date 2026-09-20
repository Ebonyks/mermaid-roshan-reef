"""Geometry/source stress checks plus a human-readable before/after review."""
from pathlib import Path
import argparse,hashlib,html,json,shutil
from collections import Counter
from PIL import Image
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent

def overlap(a,b):
 return min(a[0]+a[2],b[0]+b[2])>max(a[0],b[0]) and min(a[1]+a[3],b[1]+b[3])>max(a[1],b[1])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--proof',required=True,type=Path);ap.add_argument('--baseline',required=True,type=Path);args=ap.parse_args()
 b=json.loads((ROOT/'book.json').read_text(encoding='utf8'));p=json.loads((args.proof/'page_provenance.json').read_text(encoding='utf8'));review=json.loads((ROOT/'stress_review.json').read_text(encoding='utf8'));issues=[];pages={row['page']:row for row in b['pages']}
 pdf=PdfReader(args.proof/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')
 if len(pdf.pages)!=34:issues.append('Expected 32 story pages plus covers.')
 for i,page in enumerate(pdf.pages):
  if list(page.mediabox)!=[0,0,504,360]:issues.append(f'Wrong trim size: PDF page {i+1}.')
 for line in p['text_lines']:
  x,y,w,h=line['box'];margin=18 if isinstance(line['page'],str) else 24
  if x<margin or y<margin or x+w>504-margin or y+h>360-margin:issues.append(f"Page {line['page']}: text outside safety inset: {line['text']}")
  if not isinstance(line['page'],int):continue
  page=pages[line['page']]
  if line['font_size']<18:issues.append(f"Page {line['page']}: story font below 18 points.")
  for focal in page.get('focal_exclusions',[]):
   if overlap(line['box'],focal):issues.append(f"Page {line['page']}: caption overlaps manually annotated focal region: {line['text']}")
  if page['mode']=='C':
   for layer in p['layers']:
    if layer['page']==page['page'] and layer['role']=='story_art' and overlap(line['box'],layer['target_box_points']):issues.append(f"Page {page['page']}: text intersects foreground bounding box.")
 for page in b['pages']:
  n=page['page']
  if page['mode']=='C':
   if not page['border_assets']:issues.append(f'Page {n}: no contextual background assignment.')
   if set(page['art'])&set(page['border_assets']):issues.append(f'Page {n}: foreground/background source duplication.')
   for key in page['art']+page['border_assets']:
    im=Image.open(ROOT/b['sources'][key]['file'])
    if im.mode!='RGBA' or im.getextrema()[3][0]!=0:issues.append(f'Page {n}: non-transparent reduced asset {key}.')
  if page['mode']=='F' and 'focal_exclusions' not in page:issues.append(f'Page {n}: missing manual focal review field.')
 for layer in p['layers']:
  src=ROOT/b['sources'][layer['source_key']]['file']
  if hashlib.sha256(src.read_bytes()).hexdigest()!=layer['sha256']:issues.append(f"Source hash mismatch: {layer['source_key']}")
  if layer['role']=='mound_decoration':
   x,y,w,h=layer['target_box_points']
   if w>504*.12+.01 or h>360*.12+.01 or y+h>54+.01 or (x<314 and x+w>190):issues.append(f"Page {layer['page']}: mound restrictions failed.")
 counts=Counter(key for page in b['pages'] for key in page.get('border_assets',[]))
 if any(count>2 for count in counts.values()):issues.append('Event-border repetition: one decorative prop used more than twice.')
 if {'brush','sponge','bubbles'} & set(counts):issues.append('Generic brush/sponge/suds border motif has returned.')
 for page in b['pages']:
  if page['mode']!='C':continue
  if [q['source'] for q in page['border_placements']]!=page['border_assets']:issues.append(f"Page {page['page']}: border plan differs from actual placements.")
  for key in page['border_assets']:
   source=b['sources'][key]
   if 'alpha_box' in source:
    im=Image.open(ROOT/source['file']);x0,y0,x1,y1=source['alpha_box']
    if not (0<=x0<x1<=im.width and 0<=y0<y1<=im.height):issues.append(f'Invalid atlas bounds: {key}.')
    if im.getchannel('A').crop((x0,y0,x1,y1)).getextrema()[0]!=0:issues.append(f'Atlas prop lacks transparent silhouette: {key}.')
 forbidden={'hug','eagle','playroom','rescue_isolated','release_cut','window_wide'}
 if forbidden & {layer['source_key'] for layer in p['layers']}:issues.append('Rejected identity/isolation source still used.')
 if pages[3]['art']!=['dirty_hall_entry'] or 'clean it together' not in pages[3]['text']:issues.append('Dirty-castle/setup regression.')
 for n,key in [(17,'pinned'),(18,'loose'),(27,'R09_open'),(28,'R09_suds'),(29,'R10_jump'),(30,'R11_land')]:
  if pages[n]['art']!=[key]:issues.append(f'Canonical rescue/finale order mismatch: page {n}.')
 if pages[23].get('art_crop')!=[420,90,1280,704]:issues.append('Noncanonical paint crown has not been excluded.')
 results={'mechanical_status':'FAIL' if issues else 'PASS','issues':issues,'story_pages_checked':32,'pdf_pages_checked':34,'text_lines_checked':len(p['text_lines']),'image_operations_checked':len(p['layers']),'contextual_cutout_pages':sum(q['mode']=='C' for q in b['pages']),'unique_border_assignments':len({tuple(q['border_assets']) for q in b['pages'] if q['mode']=='C'}),'unique_decorative_props':len(counts),'maximum_prop_repetition':max(counts.values(),default=0),'scope':'Geometry, source hashes, selected-source exclusions, contextual assignments, and manual focal-zone intersections. Not automatic character-identity, contrast or publication acceptance.','visual_verdict':review['revision_verdict'],'open_findings':review['open_findings']}
 (args.proof/'stress_results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf8')
 cards=[]
 for row in review['pages']:
  n=row['page'];old=(args.baseline/f'page_{n:02}.jpg').resolve().as_uri();new=f'page_{n:02}.jpg';q=pages[n]
  cards.append(f'<article id="page-{n}"><h2>Page {n}</h2><p><b>Baseline:</b> {html.escape(row["baseline_issue"])}</p><div class="pair"><figure><figcaption>Rejected v7</figcaption><img loading="lazy" src="{old}"></figure><figure><figcaption>Revised proof</figcaption><img loading="lazy" src="{new}"></figure></div><p><b>Change:</b> {html.escape(row["revision"])}</p><p><b>Identity review:</b> {html.escape(row["identity_review"])}</p><p><b>Background:</b> {html.escape(q["background_theme"])} · {html.escape(", ".join(q["border_assets"]) or "Full art; no stationery")}</p></article>')
 open_rows=''.join('<li><b>'+html.escape(f['id'])+'</b> · '+html.escape(str(f['pages']))+': '+html.escape(f['issue'])+'</li>' for f in review['open_findings'])
 doc='<!doctype html><meta charset="utf-8"><title>Mermaid Roshan · Comprehensive stress review</title><style>body{font:17px/1.5 system-ui;background:#e5f2f8;color:#153047;margin:0}header,article{max-width:1250px;margin:25px auto;padding:24px;background:white;border-radius:10px}h1{font-size:32px}h2{margin-top:0}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}img{width:100%}figcaption{font-weight:bold;padding:8px 0}.status{background:#fff1d2;padding:18px}a{color:#125bb0}@media(max-width:800px){.pair{grid-template-columns:1fr}article,header{margin:15px;padding:16px}}</style><header><h1>Comprehensive picture-book stress review</h1><p class="status"><b>The v7 proof failed the owner’s visual review.</b> This revision addresses confirmed issues; it is not a final visual acceptance.</p><p>32 story pages + covers. Text placement, source selection, identity signatures, background ownership and story progression reviewed. Mechanical checks: '+results['mechanical_status']+'.</p><p><a href="READ_BOOK.html">Read the revised book</a> · <a href="stress_results.json">Machine evidence</a></p><h2>Still open</h2><ul>'+open_rows+'</ul><p>Comparison panels below are audit evidence, not proposed framed illustrations in the book.</p></header>'+''.join(cards)
 original=ROOT.parents[2]/'assets/book/baby_eagle.png'
 if original.exists() and 'eagle' in b['sources']:
  refs=args.proof/'identity_references';refs.mkdir(exist_ok=True);cards=[]
  for i,(label,src) in enumerate([('Original book Eagle',original),('Rejected v7 Eagle',ROOT/b['sources']['eagle']['file']),('Revised isolation',ROOT/b['sources']['eagle_original_isolated']['file'])]):
   shutil.copy2(src,refs/f'eagle_{i}.png');cards.append(f'<figure><figcaption>{label}</figcaption><img style="height:330px;object-fit:contain;background:#dceff6" src="identity_references/eagle_{i}.png"></figure>')
  doc=doc.replace('</header>','<h2>Eagle identity comparison</h2><div class="pair">'+''.join(cards)+'</div><p>Grey feet and pastel character cues restored through bounded extraction. Exact extraction fidelity remains a review candidate.</p></header>',1)
 (args.proof/'STRESS_TEST.html').write_text(doc,encoding='utf8');print(json.dumps(results,indent=2))
 if issues:raise SystemExit(1)

if __name__=='__main__':main()
