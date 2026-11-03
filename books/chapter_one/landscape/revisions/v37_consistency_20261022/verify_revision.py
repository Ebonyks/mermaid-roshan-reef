"""V37 source/geometry/canon/contrast checks; does not grant human or print acceptance."""
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw,ImageChops,ImageFilter
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete';OLD=V.parent/'v36_next_draft';BASE='b5288f2ca2bab1e36d51fd9a00616de0dc30c2c0'
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def overlap(a,b):return min(a[0]+a[2],b[0]+b[2])>max(a[0],b[0]) and min(a[1]+a[3],b[1]+b[3])>max(a[1],b[1])
b=read(L/'book.json');old=read(V/'BOOK_BASELINE.json');prov=read(C/'page_provenance.json');P={p['page']:p for p in b['pages']};pdf=PdfReader(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf');issues=[]
assert len(pdf.pages)==34 and len(P)==32 and [p['page'] for p in b['pages']]==list(range(1,33))
assert all(list(p.mediabox)==[0,0,1008,720] for p in pdf.pages)
assert b['physical_review_scale']==2 and b['font']==old['font']
# Seal every original source/font against the exact V33 Git tree.
tree={}
for row in subprocess.check_output(['git','ls-tree','-r','-z',BASE],cwd=R).split(b'\0'):
 if row:
  head,path=row.split(b'\t',1);tree[path.decode()]=head.split()[2].decode()
sealed=[]
for p in sorted({(L/q['file']).resolve() for q in old['sources'].values()}|{(L/old['font']).resolve()}):
 data=p.read_bytes();rel=p.relative_to(R).as_posix();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==tree[rel],rel
 sealed.append(dict(path=rel,sha256=hashlib.sha256(data).hexdigest()))
for k,v in old['sources'].items():assert b['sources'][k]==v,k
for q in prov['layers']:assert sha(L/b['sources'][q['source_key']]['file'])==q['sha256']
for q in prov['text_lines']:
 x,y,w,h=q['box'];m=18 if isinstance(q['page'],str) else 24;stroke=max(q.get('outline',0),.85 if q.get('halo') else 0)/2
 if x-stroke<m or y-stroke<m or x+w+stroke>504-m or y+h+stroke>360-m:issues.append('Text inset: '+str(q))
 if isinstance(q['page'],int):
  assert q['font_size'] in [18,20]
  for z in P[q['page']].get('focal_exclusions',[]):
   if overlap(q['box'],z):issues.append('Text/focal overlap: '+str(q['page'])+' '+q['text'])
  if P[q['page']]['mode']=='C':
   for z in prov['layers']:
    if z['page']==q['page'] and z['role']=='story_art' and overlap(q['box'],z['target_box_points']):issues.append('Caption/cutout overlap: '+str(q['page']))
for p in P.values():
 assert p['caption']['size']==20
 if p['mode']=='C':
  assert p.get('integrated_background') and p.get('integrated_motifs') and p.get('integrated_prop_bounds')
  assert not p['border_assets'] and not p['border_placements']
  for x,y,w,h in p['integrated_prop_bounds']:
   minimum=.80 if p.get('narrative_border_dialogue') else .85
   if w>.12 or h>.12 or y<minimum or y+h>1 or (x<.62 and x+w>.38):issues.append('Marginal bounds: '+str(p['page'])+' '+str([x,y,w,h]))
  for k in p['art']:
   im=Image.open(L/b['sources'][k]['file']);assert im.mode=='RGBA' and im.getextrema()[3][0]==0,k
  assert p.get('marginal_bunny_count',0)<=3
# Exact owner manuscript and handoff page order.
import re
owner=(R/'books/chapter_one/handoffs/2026-10-18_v34_audit_fixes/OWNER_DECISION_2026-10-19.md').read_text('utf8')
rows={int(n):t.split(' | ')[0].strip().replace(' / ','\n') for n,t in re.findall(r'^\| (\d+) \| (.*?) \|$',owner,re.M) if int(n)<=32}
assert len(rows)==32, len(rows)
for n in P:assert P[n]['text']==rows[n],(n,P[n]['text'],rows[n])
assert [P[n]['v34_page'] for n in P]==[1,2,3,4,23,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32]
assert b['back_cover']['art']=='v37_rear_scene'
assert any(q['source']=='v37_rear_hair' for q in b['back_cover']['local_patches'])
assert b['back_cover']['caption']['text']=='Pearl Castle needs help.\nWhere will Roshan begin?'
assert b['cover']['subtitle']['text']=='A Pearl Castle friendship story'
assert P[5]['art']==old['pages'][4]['art']
assert P[23]['art']==old['pages'][22]['art']
assert P[25]['art']==['v37_sponge_pose']
assert P[24]['art']==old['pages'][23]['art']
assert P[31]['art']==old['pages'][30]['art']

# Baseline controls stay exact except declared repair sources/masks and caption14/23.
for n,p in P.items():
 before=old['pages'][n-1]
 for field in ['page','mode','layout','text','border_assets','border_placements','v34_page']:
  assert p.get(field)==before.get(field),(n,field)
 if n!=25:assert p['art']==before['art'],n
 if n not in [14,23]:assert p['caption']==before['caption'],n
 for q in p.get('local_patches',[]):
  assert q['source'] in b['sources']
  if q['source'].startswith('v37_'):
   assert q.get('source_canvas_box') and q.get('edge_feather_reference_pixels',0)>0
# Scope-specific new rear composition remains a separate source, not a replacement original.
assert b['sources']['v37_rear_scene']['sha256']=='cd1a5a40d51560170713169b3b3187828a07463610fa929275eaa8dbc604b0d7'

# Native repair provenance and final scoped visual-review records are separate evidence.
generation=read(V/'generation_evidence.json');assert generation['calls']==33 and len(generation['records'])==33
for q in generation['records']:
 assert sha(R/q['output'])==q['output_sha256']
 assert q['input_is_exact_declared_crop']
 assert sha(R/q['input_origin'])==q['input_origin_sha256']
 assert sha(R/q.get('source',q['references'][0]))==q['source_sha256']
 for ref in q.get('bound_reference_records',[]):assert sha(R/ref['path'])==ref['sha256']
visual=read(V/'r07_audits.json');assert len(visual['passes'])==5 and all(q['result']=='PASS' and not q['remaining'] for q in visual['passes'])
assert visual['pdf_sha256']==sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')
parts=read(C/'master_parts/parts.json');payload=b''.join((C/'master_parts'/q['file']).read_bytes() for q in parts['parts'])
assert hashlib.sha256(payload).hexdigest()==parts['master_sha256']==sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')

# Every saved proof is the exact final PDF render, including alpha/stroke/geometry.
doc=pdfium.PdfDocument(str(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'))
for n in range(34):
 im=doc[n].render(scale=1.5).to_pil().convert('RGB');saved=Image.open(C/f'page_{n:02}.png').convert('RGB');assert im.size==(1512,1080) and ImageChops.difference(im,saved).getbbox() is None,n
assert len(list(C.glob('page_[0-9][0-9].png')))==34
# Compare all unchanged-stage F pages after removing text. Only declared local polygons may differ.
scratch=R/'tmp/pdfs/v37';scratch.mkdir(parents=True,exist_ok=True)
def no_text(source,dest):
 w=PdfWriter();r=PdfReader(source)
 for p in r.pages:w.add_page(p)
 w.remove_text()
 with dest.open('wb') as f:w.write(f)
no_text(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf',scratch/'current_art.pdf')
no_text(OLD/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf',scratch/'baseline_art.pdf')
cur=pdfium.PdfDocument(str(scratch/'current_art.pdf'));before=pdfium.PdfDocument(str(scratch/'baseline_art.pdf'))
pixels=[]
for n in [0]+list(P):
 if n and P[n]['mode']!='F':continue
 prev=n
 aa=cur[n].render(scale=1.5).to_pil().convert('RGB');bb=before[prev].render(scale=1.5).to_pil().convert('RGB');mask=Image.new('L',aa.size);draw=ImageDraw.Draw(mask)
 for q in prov['layers']:
  if q['page']==('front_cover' if n==0 else n) and q['operation'].startswith('bounded_') and (q['source_key'].startswith('v37_') or n==20):
   rw,rh=q['clip_reference_size'];ox,oy,s=q['clip_canvas_transform_points'];draw.polygon([((ox+x*s)*3,(360-oy-(rh-y)*s)*3) for x,y in q['clip_polygon_source_pixels']],fill=255)
 mask=mask.filter(ImageFilter.MaxFilter(5));diff=np.max(np.abs(np.asarray(aa,dtype=np.int16)-np.asarray(bb,dtype=np.int16)),axis=2);outside=np.asarray(mask)==0
 count=int(np.count_nonzero(diff[outside]>1))
 if count:issues.append('Outside declared local edits: '+str((n,prev,count)))
 pixels.append(dict(page=n,baseline=prev,outside_declared_masks_pixels_over_one_level=count))
# Caption contrast in COMPOSED art, including actual local repairs, balloons and rear transform.
def lum(a):
 a=np.asarray(a,dtype=float)/255;a=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);return a@np.array([.2126,.7152,.0722])
fills={'navy':float(lum([15.3,40.8,73.95])),'white':float(lum([255,255,249.9]))};contrast=[];images={}
for q in prov['text_lines']:
 n=0 if q['page']=='front_cover' else 33 if q['page']=='back_cover' else q['page']
 if n not in images:images[n]=lum(cur[n].render(scale=1.5).to_pil().convert('RGB'))
 x,y,w,h=q['box'];a=images[n][max(0,int((360-y-h)*3)):min(1080,int((360-y)*3)),max(0,int(x*3)):min(1512,int((x+w)*3))];f=fills[q['color']]
 if a.size==0:issues.append('Empty/off-page caption: '+str(q));continue
 ratio=lambda v:(max(f,v)+.05)/(min(f,v)+.05)
 typical=ratio(float(np.median(a)));worst=ratio(float(np.quantile(a,.9 if q['color']=='white' else .1)))
 verdict='FAIL' if worst<3 else 'OUTLINE_REQUIRED' if typical<4.5 else 'PASS'
 row=dict(page=q['page'],text=q['text'],color=q['color'],typical=round(typical,3),worst=round(worst,3),verdict=verdict,outline=q.get('outline',0),halo=q.get('halo',False));contrast.append(row)
 if verdict=='FAIL':issues.append('Composed contrast: '+str(row))
 if verdict=='OUTLINE_REQUIRED' and not (q.get('outline',0)>=1 or q.get('halo')):issues.append('Unresolved outline: '+str(row))
save(V/'composed_caption_contrast.json',dict(method='Same fill/median/worst10percent luminance thresholds as supplied gate, sampled from exact caption-free final PDF composition. Includes real local edits, masks, speech capsules and rear transform; stroke intentionally excluded from ratio.',counts=dict(Counter(q['verdict'] for q in contrast)),lines=contrast))
(V/'composed_caption_contrast.tsv').write_text('page\tcolor\ttypical\tworst\tverdict\ttext\n'+'\n'.join(f"{q['page']}\t{q['color']}\t{q['typical']}\t{q['worst']}\t{q['verdict']}\t{q['text']}" for q in contrast)+'\n',encoding='utf8',newline='\n')
out=dict(status='PASS' if not issues else 'FAIL',baseline=BASE,pages=34,story_pages=32,page_size_points=[1008,720],raster_upsample=False,source_seal=sealed,source_seal_count=len(sealed),exact_pdf_proofs=34,narrative_outside_mask_checks=pixels,contrast_counts=dict(Counter(q['verdict'] for q in contrast)),issues=issues,acceptance='Machine verification only. Five visual-pass results in r07_audits.json. Owner/child/SLP/final-resolution/trim/physical print remain open.')
out.update(pdf_sha256=sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),manuscript_sha256=sha(L/'book.json'),provenance_sha256=sha(C/'page_provenance.json'))
save(C/'verification.json',out);print(json.dumps({k:v for k,v in out.items() if k not in ['source_seal','narrative_outside_mask_checks']},ensure_ascii=False,indent=2))
if issues:raise SystemExit(1)
