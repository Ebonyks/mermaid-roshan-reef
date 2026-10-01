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
 revised=b.get('revision','').startswith(('V28','V29','V30','V31','V32'))
 polished=b.get('revision','').startswith(('V29','V30','V31','V32'))
 local_identity=b.get('revision','').startswith(('V30','V31','V32'))
 story_clarity=b.get('revision','').startswith(('V31','V32'))
 rainbow_story=b.get('revision','').startswith('V32')
 by_old={row.get('original_page',row['page']):row for row in b['pages']}
 if revised:review=json.loads((ROOT/('revisions/v32_rainbow_story' if rainbow_story else 'revisions/v31_story_clarity' if story_clarity else 'revisions/v30_identity' if local_identity else 'revisions/v29_polish' if polished else 'revisions/v28_kindness')/'visual_review.json').read_text(encoding='utf8'))
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
  old=page.get('original_page',n)
  if page.get('narrative_border_dialogue') and old!=19:issues.append(f'Page {n}: speaking-character margin exception is only commissioned for the Eagle apology.')
  for balloon in page.get('speech_bubbles',[]):
   x,y,w,h=balloon['box'];tx,ty=balloon['tail']
   if x<24 or y<24 or x+w>480 or y+h>336 or not (24<=tx<=480 and 24<=ty<=336):issues.append(f'Page {n}: speech balloon outside safety inset.')
   for layer in p['layers']:
    if layer['page']==n and layer['role']=='story_art' and overlap(balloon['box'],layer['target_box_points']):issues.append(f'Page {n}: speech balloon covers foreground artwork.')
  if page['mode']=='C':
   if not page.get('integrated_background') and not page['border_assets']:issues.append(f'Page {n}: no contextual background assignment.')
   if page.get('integrated_background'):
    if page['border_assets'] or page['border_placements']:issues.append(f'Page {n}: legacy pasted props still enabled.')
    quiet=page.get('border_intent')=='quiet_reveal'
    if quiet and (n!=25 or page['integrated_background']!='landscape_base' or page.get('integrated_motifs') or page.get('integrated_prop_bounds')):issues.append(f'Page {n}: quiet reveal must use unadorned base with no decorative motifs/bounds.')
    if not quiet and not page.get('integrated_motifs'):issues.append(f'Page {n}: missing contextual motifs.')
    if set(page['art'])&set(page.get('integrated_motifs',[])):issues.append(f'Page {n}: foreground prop repeated in integrated border.')
    if not quiet and not page.get('integrated_prop_bounds'):issues.append(f'Page {n}: missing inspected visible prop bounds.')
    actual=[q for q in p['layers'] if q['page']==n and q['role']=='integrated_stationery']
    if len(actual)!=1 or actual[0]['source_key']!=page['integrated_background']:issues.append(f'Page {n}: integrated background source mismatch.')
    for box in page.get('integrated_prop_bounds',[]):
     x,y,w,h=box
     # Owner approved this exact hug-stationery preview, including its small crest.
     approved_hug=revised and old==15 and page['integrated_background']=='approved_hug_stationery_v2' and box==[138/1484,868/1060,140/1484,114/1060]
     min_y=868/1060 if approved_hug else .80 if page.get('narrative_border_dialogue') else .85-2/1060 if old==20 else .85
     max_h=.12 if revised else .18 if page.get('narrative_border_dialogue') else .12
     if w>.12 or h>max_h or y<min_y or y+h>1 or (x<.62 and x+w>.38):issues.append(f'Page {n}: annotated decoration bounds fail limits.')
   if set(page['art'])&set(page['border_assets']):issues.append(f'Page {n}: foreground/background source duplication.')
   for key in page['art']+page['border_assets']:
    im=Image.open(ROOT/b['sources'][key]['file'])
    if im.mode!='RGBA' or im.getextrema()[3][0]!=0:issues.append(f'Page {n}: non-transparent reduced asset {key}.')
  if page['mode']=='F' and 'focal_exclusions' not in page:issues.append(f'Page {n}: missing manual focal review field.')
 for key in {layer['source_key'] for layer in p['layers']}:
  source=b['sources'][key]
  if 'alpha_box' in source:
   im=Image.open(ROOT/source['file']);x0,y0,x1,y1=source['alpha_box']
   if not (0<=x0<x1<=im.width and 0<=y0<y1<=im.height):issues.append(f'Invalid complete-pose atlas bounds: {key}.')
   if im.mode!='RGBA':issues.append(f'Atlas pose is not alpha artwork: {key}.')
 if 'roshan' in {layer['source_key'] for layer in p['layers']}:issues.append('Repeated neutral Roshan cutout has returned.')
 cover_keys={q['source_key'] for q in p['layers'] if q['page']=='front_cover'}
 if not set(b.get('cover',{}).get('art',[]))<=cover_keys:issues.append('Composite cover is missing a declared source.')
 for layer in p['layers']:
  src=ROOT/b['sources'][layer['source_key']]['file']
  if hashlib.sha256(src.read_bytes()).hexdigest()!=layer['sha256']:issues.append(f"Source hash mismatch: {layer['source_key']}")
  if layer['role']=='mound_decoration':
   x,y,w,h=layer['target_box_points']
   if w>504*.12+.01 or h>360*.12+.01 or y+h>54+.01 or (x<314 and x+w>190):issues.append(f"Page {layer['page']}: mound restrictions failed.")
 counts=Counter(key for page in b['pages'] for key in page.get('integrated_motifs',page.get('border_assets',[])))
 if any(count>2 for count in counts.values()):issues.append('Event-border repetition: one decorative prop used more than twice.')
 if {'brush','sponge','bubbles','dust_curl','rainbow_crystal','friend_pennants'} & set(counts):issues.append('Rejected generic border motif has returned.')
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
 if by_old[3]['art']!=['v23_castle_repair'] or 'clean it together' not in by_old[3]['text']:issues.append('Dirty-castle/setup regression.')
 if by_old[9]['art']!=['v26_rumi_trapped']:issues.append('First dirty-pool page must establish the strainer.')
 if [' '.join(q['text'].split()) for q in by_old[19].get('speech_bubbles',[])]!=['Sorry!','We were just playing!']:issues.append('Missing commissioned bunny apology exchange.')
 back=[q for q in p['layers'] if q['page']=='back_cover']
 if not back or back[0]['source_key']!=b['back_cover']['art'] or back[0]['operation']!='page_trim':issues.append('Rear cover must retain its complete accepted full-art base.')
 if not local_identity and len(back)!=1:issues.append('Uncommissioned rear-cover layers.')
 if local_identity:
  expected={'front_cover':{'v30_front_identity':2},'back_cover':{'v30_rear_identity':2},5 if rainbow_story else 4:{'v30_castle_attention':2},11 if rainbow_story else 10:{'v30_rumi_face_crop':1}}
  if story_clarity:expected['back_cover']['v31_rear_lamma']=1
  for page_id,keys in expected.items():
   actual=Counter(q['source_key'] for q in p['layers'] if q['page']==page_id and q['operation']=='bounded_inpaint_polygon_visible_pdf_resource')
   if dict(actual)!=keys:issues.append(f'Page {page_id}: local identity edit sources/count differ from reviewed scope.')
  if any(q['operation']!='bounded_inpaint_polygon_visible_pdf_resource' for q in back[1:]):issues.append('Rear cover added a non-local scene layer.')
  if by_old[4]['text']!='Daddy gave her a brush and some sponges.\n“One little job at a time.”':issues.append('Sponge variety introduction missing.')
 for n,key in [(17,'rescue_trapped'),(18,'rescue_release'),(27,'v27_scrub'),(28,'R09_suds'),(29,'R10_jump'),(30,'R11_land')]:
  if revised and n==18:key='approved_rescue_release'
  if polished and n in [17,18]:key='v29_rescue18' if n==17 else 'v29_rescue19'
  if by_old[n]['art']!=[key]:issues.append(f'Canonical rescue/finale order mismatch: former page {n}.')
 if by_old[24]['art']!=['v27_door'] or by_old[24]['mode']!='F':issues.append('Door page must show complete route-light hall.')
 if revised:
  if 23 in by_old or pages[3]['art']!=['v29_castle03' if polished else 'v28_castle_entry_source']:issues.append('Disconnected craft beat returned or castle entry missing.')
  if by_old[26]['art']!=['v29_sponge25' if polished else 'v28_puff_reassurance'] or by_old[26]['text']!='“Hold on, we’ll make you feel\nclean and better!” said Roshan.':issues.append('Owner reassurance or sponge artwork missing.')
  if [by_old[n]['page'] for n in [24,25,28,29]]!=[23,24,27,28]:issues.append('Reveal page-turn order changed.')
  if any(term in ' '.join(q['text'].lower() for q in b['pages']) for term in ['dizzy','wobbled','beat him','stopped him','sparkles flew','fighting']):issues.append('Retired combat wording returned.')
  if any(q['source_key'] in {'v25_shell_duel','approved_apology_canvas','v25_art_simple'} for q in p['layers']):issues.append('Rejected active art returned.')
  visitor_keys={'v29_lamma09','v31_rear_lamma'} if story_clarity else {'v29_lamma09','v29_bank31_final'} if polished else {'approved_lamba_bath','v28_lamba_toy_peek'}
  visitor_pages={10,'back_cover'} if rainbow_story else {9,'back_cover'} if story_clarity else {9,31}
  if {q['page'] for q in p['layers'] if q['source_key'] in visitor_keys}!=visitor_pages:issues.append('Expected two unprompted hidden appearances.')
  if rainbow_story:
   if any(term in pages[13]['text'].lower()+' '+pages[14]['text'].lower() for term in ['one stream','three streams','other two']):issues.append('Unsupported waterfall-count language returned.')
   if pages[13]['art']!=['v22_scene_11'] or pages[13].get('local_patches') or 'v31_waterfall_progress' in {q['source_key'] for q in p['layers']}:issues.append('Existing rainbow-water progress source must be restored without the aqua patch.')
   if not all(term in pages[14]['text'].lower() for term in ['swimming pool','magic','makes the water rainbow']):issues.append('Owner magical-pool rainbow explanation missing.')
   if pages[4]['mode']!='C' or pages[4]['art']!=['v32_shell_cobweb','v32_dusty_chest']:issues.append('Source-derived dirty castle inspection page missing.')
   if pages[22]['art']!=['v22_art_sorting'] or 'scrubbed the table' not in pages[22]['text']:issues.append('Art-room cleanup must be completed before the final door.')
   if pages[30]['art']!=['v22_scene_22_fit'] or not any(q['source']=='v32_clean_room30' for q in pages[30].get('local_patches',[])):issues.append('Quiet clean-room completion picture missing.')
   if pages[31]['art']!=['roshan_reflect_large','approved_rainbow_puff_cutout'] or not all(term in pages[31]['text'].lower() for term in ['rainbow shine','thank you','rest with us']):issues.append('Combined rainbow reflection, thanks and belonging missing.')
   if [q['source'] for q in pages[31].get('background_patches',[])]!=['v31_rest_bank31','v31_rest_bank31']:issues.append('Combined ending must retain both reviewed sleepy-bank patches and exclude the old third cameo.')
  elif story_clarity:
   if any(term in pages[12]['text'].lower()+' '+pages[13]['text'].lower() for term in ['one stream','three streams','other two']):issues.append('Unsupported waterfall-count language returned.')
   if pages[31]['art']!=['roshan_wave_large','approved_rainbow_puff_cutout'] or 'Grand Puff' not in pages[31]['text'] or 'rest with us' not in pages[31]['text']:issues.append('Puff belonging/rest ending missing.')
   if [q['source'] for q in pages[31].get('background_patches',[])]!=['v31_rest_bank31','v31_rest_bank31']:issues.append('Former toy-bank cameo must be removed by both reviewed local rest patches.')
 else:
  if pages[23]['art']!=['v25_art_simple'] or 'art_crop' in pages[23]:issues.append('Paint page must use owner-requested simplified painted scene without crop.')
  if pages[26]['art']!=['v25_shell_duel']:issues.append('Missing facing-shell-sparkle-dizzy action cutout.')
 results={'mechanical_status':'FAIL' if issues else 'PASS','issues':issues,'story_pages_checked':32,'pdf_pages_checked':34,'text_lines_checked':len(p['text_lines']),'image_operations_checked':len(p['layers']),'contextual_cutout_pages':sum(q['mode']=='C' for q in b['pages']),'unique_border_assignments':len({tuple(q.get('integrated_motifs',q['border_assets'])) for q in b['pages'] if q['mode']=='C'}),'unique_decorative_props':len(counts),'maximum_prop_repetition':max(counts.values(),default=0),'scope':'Geometry, source hashes, selected-source exclusions, contextual assignments, manually annotated visible border bounds, and manual focal-zone intersections. Integrated shadow/occlusion and exact prop pixel preservation are not measured. Not automatic character-identity, contrast or publication acceptance.','visual_verdict':review['revision_verdict'],'open_findings':review['open_findings']}
 (args.proof/'stress_results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf8')
 if revised:
  print(json.dumps(results,indent=2,ensure_ascii=False))
  if issues:raise SystemExit(1)
  return  # V28 has a separate current review; never relabel the historical V7 report.
 cards=[]
 for row in review['pages']:
  n=row['page'];old=(args.baseline/f'page_{n:02}.jpg').resolve().as_uri();new=f'page_{n:02}.jpg';q=pages[n]
  cards.append(f'<article id="page-{n}"><h2>Page {n}</h2><p><b>Baseline:</b> {html.escape(row["baseline_issue"])}</p><div class="pair"><figure><figcaption>Rejected v7</figcaption><img loading="lazy" src="{old}"></figure><figure><figcaption>Revised proof</figcaption><img loading="lazy" src="{new}"></figure></div><p><b>Change:</b> {html.escape(row["revision"])}</p><p><b>Identity review:</b> {html.escape(row["identity_review"])}</p><p><b>Background:</b> {html.escape(q["background_theme"])} · {html.escape(", ".join(q.get("integrated_motifs",q["border_assets"])) or "Full art; no stationery")}</p></article>')
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
