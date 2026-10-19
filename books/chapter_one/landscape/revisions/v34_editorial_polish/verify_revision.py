"""V34 source/geometry/canon/contrast checks; does not grant human or print acceptance."""
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw,ImageChops,ImageFilter
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete';OLD=V.parent/'v33_story_covers';BASE='a14a26ee356296c84b7251ce8222f371740ed2cb'
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
for n in [11,21,23,24]:assert P[n]['integrated_background'].startswith('v34_') and not P[n].get('background_patches')
assert P[21]['marginal_bunny_count']==0 and P[23]['marginal_bunny_count']==1 and P[24]['marginal_bunny_count']==2
assert P[25]['art']==['v34_roshan_sponge_only'] and b['sources']['v34_roshan_sponge_only']['alpha_box'][0]==887
assert P[25]['foreground_zone'][0]>=36
assert [q['text'] for q in P[20]['speech_bubbles']]==['Sorry!','We were just\nplaying!']
assert P[20]['integrated_background']==old['pages'][20]['integrated_background']
assert P[24]['art']==['v26_puff_unwell'] and P[28]['art']==['R10_jump'] and P[29]['art']==['R11_land']
assert P[26]['art']==old['pages'][25]['art'] and P[27]['art']==old['pages'][26]['art'] and P[32]['art']==old['pages'][31]['art']
assert P[22]['art']==['v27_door'] and P[23]['beat']=='quiet_plea_before_reveal' and 'Can you help me?' in P[23]['text']
assert P[25]['text']=='“Hold on, we’ll make you feel\nclean and better!” said Roshan.'
assert 'pool’s magic' in P[13]['text'] and 'rainbow water' in P[13]['text']
assert not any(x in ' '.join(q['text'].lower() for q in P.values()) for x in ['beat him','enemy','dizzy','fighting','attacked'])
assert P[3]['art']==old['pages'][2]['art'] and not P[3].get('local_patches')
assert not any('floor' in q['source_key'] or 'entry_dust' in q['source_key'] for q in prov['layers'] if q['source_key'].startswith('v34_'))
# Two hidden cameos remain unprompted: bath9 and rear; original sources preserved.
assert any(q['source']=='v29_lamma09' for q in P[9].get('local_patches',[])+([P[9]['local_patch']] if P[9].get('local_patch') else [])) if 'v29_lamma09' in b['sources'] else True
assert b['back_cover']['local_patches']==old['back_cover']['local_patches']
scene=[{k:v for k,v in q.items() if k!='page'} for q in prov['layers'] if q['page']==26]
rear=[{k:v for k,v in q.items() if k!='page'} for q in prov['layers'] if q['page']=='back_cover' and q['operation']!='bounded_inpaint_polygon_visible_pdf_resource']
assert scene==rear and prov['rear_view_transform']==b['back_cover']['view_transform']
assert not any(x in ' '.join(q['text'].lower() for q in P.values()) for x in ['lamma','lamb-a','find the llama'])
e=read(V/'generation_evidence.json');assert e['count']==25
actual_files={(L/b['sources'][q['source_key']]['file']).resolve() for q in prov['layers']}
for q in e['native_attempts']:
 p=R/q['path'];assert sha(p)==q['sha256'] and list(Image.open(p).size)==q['native_size']
 assert (p.resolve() in actual_files)==(q['selection']=='DELIVERED'),q['path']
assert not any('attempt1.png' in b['sources'][k]['file'] for k in ['v34_tidy_art_bank','v34_care_bank24','v34_quiet_bank'])
# Every saved proof is the exact final PDF render, including alpha/stroke/geometry.
doc=pdfium.PdfDocument(str(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'))
for n in range(34):
 im=doc[n].render(scale=1.5).to_pil().convert('RGB');saved=Image.open(C/f'page_{n:02}.png').convert('RGB');assert im.size==(1512,1080) and ImageChops.difference(im,saved).getbbox() is None,n
assert len(list(C.glob('page_[0-9][0-9].png')))==34
# Compare all unchanged-stage F pages after removing text. Only declared local polygons may differ.
scratch=R/'tmp/pdfs/v34';scratch.mkdir(parents=True,exist_ok=True)
def no_text(source,dest):
 w=PdfWriter();r=PdfReader(source)
 for p in r.pages:w.add_page(p)
 w.remove_text()
 with dest.open('wb') as f:w.write(f)
no_text(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf',scratch/'current_art.pdf')
no_text(OLD/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf',scratch/'baseline_art.pdf')
cur=pdfium.PdfDocument(str(scratch/'current_art.pdf'));before=pdfium.PdfDocument(str(scratch/'baseline_art.pdf'));mapping=read(V/'pagination.json');pixels=[]
a1=np.asarray(cur[1].render(scale=1.5).to_pil().convert('RGB'),dtype=np.int16)
b1=np.asarray(before[1].render(scale=3).to_pil().convert('RGB'),dtype=np.int16)
assert np.count_nonzero(np.max(np.abs(a1-b1),axis=2)>1)==0,'Arrival artwork must remain the exact original full frame.'
for mp in mapping:
 n=mp['new'];prev=mp['baseline_v33']
 if prev is None or P[n]['mode']!='F' or n==1:continue
 aa=cur[n].render(scale=1.5).to_pil().convert('RGB');bb=before[prev].render(scale=3).to_pil().convert('RGB');mask=Image.new('L',aa.size);draw=ImageDraw.Draw(mask)
 for q in prov['layers']:
  if q['page']==n and q['source_key'].startswith('v34_') and q['operation'].startswith('bounded_'):
   rw,rh=q['clip_reference_size'];ox,oy,s=q['clip_canvas_transform_points'];draw.polygon([((ox+x*s)*3,(360-oy-(rh-y)*s)*3) for x,y in q['clip_polygon_source_pixels']],fill=255)
 mask=mask.filter(ImageFilter.MaxFilter(5));diff=np.max(np.abs(np.asarray(aa,dtype=np.int16)-np.asarray(bb,dtype=np.int16)),axis=2);outside=np.asarray(mask)==0
 count=int(np.count_nonzero(diff[outside]>1));assert count==0,(n,prev,count)
 pixels.append(dict(page=n,baseline=prev,outside_declared_masks_pixels_over_one_level=count))
# Caption contrast in COMPOSED art, including actual local repairs, balloons and rear transform.
def lum(a):
 a=np.asarray(a,dtype=float)/255;a=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);return a@np.array([.2126,.7152,.0722])
fills={'navy':float(lum([15.3,40.8,73.95])),'white':float(lum([255,255,249.9]))};contrast=[];images={}
for q in prov['text_lines']:
 n=0 if q['page']=='front_cover' else 33 if q['page']=='back_cover' else q['page']
 if n not in images:images[n]=lum(cur[n].render(scale=1.5).to_pil().convert('RGB'))
 x,y,w,h=q['box'];a=images[n][max(0,int((360-y-h)*3)):min(1080,int((360-y)*3)),max(0,int(x*3)):min(1512,int((x+w)*3))];f=fills[q['color']]
 ratio=lambda v:(max(f,v)+.05)/(min(f,v)+.05)
 typical=ratio(float(np.median(a)));worst=ratio(float(np.quantile(a,.9 if q['color']=='white' else .1)))
 verdict='FAIL' if worst<3 else 'OUTLINE_REQUIRED' if typical<4.5 else 'PASS'
 row=dict(page=q['page'],text=q['text'],color=q['color'],typical=round(typical,3),worst=round(worst,3),verdict=verdict,outline=q.get('outline',0),halo=q.get('halo',False));contrast.append(row)
 if verdict=='FAIL':issues.append('Composed contrast: '+str(row))
 if verdict=='OUTLINE_REQUIRED' and not (q.get('outline',0)>=1 or q.get('halo')):issues.append('Unresolved outline: '+str(row))
save(V/'composed_caption_contrast.json',dict(method='Same fill/median/worst10percent luminance thresholds as supplied gate, sampled from exact caption-free final PDF composition. Includes real local edits, masks, speech capsules and rear transform; stroke intentionally excluded from ratio.',counts=dict(Counter(q['verdict'] for q in contrast)),lines=contrast))
(V/'composed_caption_contrast.tsv').write_text('page\tcolor\ttypical\tworst\tverdict\ttext\n'+'\n'.join(f"{q['page']}\t{q['color']}\t{q['typical']}\t{q['worst']}\t{q['verdict']}\t{q['text']}" for q in contrast)+'\n',encoding='utf8',newline='\n')
out=dict(status='PASS' if not issues else 'FAIL',baseline=BASE,pages=34,story_pages=32,page_size_points=[1008,720],raster_upsample=False,source_seal=sealed,source_seal_count=len(sealed),exact_pdf_proofs=34,narrative_outside_mask_checks=pixels,generation_calls=25,selected_native_derivatives=sum(q['selection']=='DELIVERED' for q in e['native_attempts']),contrast_counts=dict(Counter(q['verdict'] for q in contrast)),issues=issues,acceptance='Machine verification only; owner/child, professional SLP, final-resolution/trim and physical-print acceptance remain open.')
out.update(pdf_sha256=sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),manuscript_sha256=sha(L/'book.json'),provenance_sha256=sha(C/'page_provenance.json'))
save(C/'verification.json',out);print(json.dumps({k:v for k,v in out.items() if k not in ['source_seal','narrative_outside_mask_checks']},ensure_ascii=False,indent=2))
if issues:raise SystemExit(1)
