"""V39 strict scope/source/manuscript/geometry/exact-proof and composed-contrast gate."""
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess,sys,re
import numpy as np
from PIL import Image,ImageDraw,ImageChops,ImageFilter,ImageFont
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete';OLD=V.parent/'v38_audit_fixes';BASE='cb3e2995df8fdf82e308352eb850b3e285f2c6c4'
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def overlap(a,b):return min(a[0]+a[2],b[0]+b[2])>max(a[0],b[0]) and min(a[1]+a[3],b[1]+b[3])>max(a[1],b[1])
def words(s):return ' '.join(s.split())
b=read(L/'book.json');old=read(V/'BOOK_BASELINE.json');prov=read(C/'page_provenance.json');P={p['page']:p for p in b['pages']};pdf=PdfReader(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf');issues=[]
assert b==read(V/'BOOK_CURRENT.json')
assert len(pdf.pages)==34 and len(P)==32 and list(P)==list(range(1,33))
assert all(list(p.mediabox)==[0,0,1008,720] for p in pdf.pages)
assert b['physical_review_scale']==2 and b['font']==old['font']
tree={}
for row in subprocess.check_output(['git','ls-tree','-r','-z',BASE],cwd=R).split(b'\0'):
 if row:
  head,path=row.split(b'\t',1);tree[path.decode()]=head.split()[2].decode()
sealed=[]
for p in sorted({(L/q['file']).resolve() for q in old['sources'].values()}|{(L/old['font']).resolve()}):
 data=p.read_bytes();rel=p.relative_to(R).as_posix()
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==tree[rel],rel
 sealed.append(dict(path=rel,sha256=hashlib.sha256(data).hexdigest()))
for k,v in old['sources'].items():assert b['sources'][k]==v,k
for q in prov['layers']:assert sha(L/b['sources'][q['source_key']]['file'])==q['sha256']
# Exact owner-authorized controls. Old layers remain an unchanged prefix.
for n,p in P.items():
 before=old['pages'][n-1]
 allowed={1:['local_patches'],2:['art','art_crop','background_theme'],24:['background_patches','background_theme','integrated_motifs','integrated_prop_bounds'],25:['background_patches','background_theme','integrated_motifs','integrated_prop_bounds']}.get(n,[])
 assert {k:v for k,v in p.items() if k not in allowed}=={k:v for k,v in before.items() if k not in allowed},n
 for key in ['local_patches','background_patches']:
  assert p.get(key,[])[:len(before.get(key,[]))]==before.get(key,[]),(n,key)
 assert p['text']==before['text'] and p['caption']==before['caption'],n
assert b['back_cover']==old['back_cover']
assert {k:v for k,v in b['cover'].items() if k!='local_patches'}=={k:v for k,v in old['cover'].items() if k!='local_patches'}
assert b['cover']['local_patches'][:len(old['cover']['local_patches'])]==old['cover']['local_patches']
assert {k:v for k,v in b.items() if k not in ['pages','cover','sources','revision','status','download_pdf_href']}=={k:v for k,v in old.items() if k not in ['pages','cover','sources','revision','status','download_pdf_href']}
assert set(b['sources'])-set(old['sources'])=={'v39_daddy_tail','v39_rumi_caudal','v39_care24','v39_care25','v39_lamma','v39_lamma_contact','v39_stained_glass','v39_demo_landing','v39_occlusion_floor','v39_foreground_lock'}
assert P[2]['art']==['v39_demo_landing'] and P[2]['art_crop']==[136,0,1144,720]
assert P[9]==old['pages'][8] # A9 remains unchanged, no new resolution claim.
owner=(R/'books/chapter_one/handoffs/2026-10-18_v34_audit_fixes/OWNER_DECISION_2026-10-19.md').read_text('utf8')
rows={int(n):t.split(' | ')[0].strip().replace(' / ','\n') for n,t in re.findall(r'^\| (\d+) \| (.*?) \|$',owner,re.M) if int(n)<=32}
assert len(rows)==32
for n in P:assert words(P[n]['text'])==words(rows[n]),n
ink_font=ImageFont.truetype(str(L/b['font']),2000)
pdfmetrics.registerFont(TTFont('V39Gate',str(L/b['font'])))
focal_ink_checks=[]
for q in prov['text_lines']:
 x,y,w,h=q['box'];m=18 if isinstance(q['page'],str) else 24;stroke=max(q.get('outline',0),.85 if q.get('halo') else 0)/2
 if x-stroke<m or y-stroke<m or x+w+stroke>504-m or y+h+stroke>360-m:issues.append('Text inset: '+str(q))
 if isinstance(q['page'],int):
  assert q['font_size']==20 or (q['font_size']==18 and q['text'] in [a for z in P[q['page']].get('speech_bubbles',[]) for a in z['text'].split('\n')])
  # Global ascent includes unused accents. Use actual glyph ink plus half the
  # full stroke for focal contact, preserving the conservative inset test above.
  il,it,ir,ib=ink_font.getbbox(q['text'],anchor='ls');factor=q['font_size']/2000
  baseline=q['box'][1]-pdfmetrics.getDescent('V39Gate')*q['font_size']/1000
  ink=[x+il*factor-stroke,baseline-ib*factor-stroke,(ir-il)*factor+2*stroke,(ib-it)*factor+2*stroke]
  for z in P[q['page']].get('focal_exclusions',[]):
   collides=overlap(ink,z)
   focal_ink_checks.append(dict(page=q['page'],text=q['text'],ink_and_stroke_box=ink,focal_box=z,overlap=collides))
   if collides:issues.append('Actual glyph/stroke focal overlap: '+str(q['page'])+' '+q['text'])
  if P[q['page']]['mode']=='C':
   for z in prov['layers']:
    if z['page']==q['page'] and z['role']=='story_art' and z['operation']=='source_region' and overlap(q['box'],z['target_box_points']):issues.append('Caption/cutout overlap: '+str(q['page']))
for p in P.values():
 assert p['caption']['size']==20
 if p['mode']=='C':
  assert p.get('integrated_background') and p.get('integrated_motifs') and p.get('integrated_prop_bounds') and not p['border_assets'] and not p['border_placements']
  for x,y,w,h in p['integrated_prop_bounds']:
   minimum=.80 if p.get('narrative_border_dialogue') else .85
   if w>.12 or h>.12 or y<minimum or y+h>1 or (x<.62 and x+w>.38):issues.append('Marginal bounds: '+str((p['page'],x,y,w,h)))
  for k in p['art']:
   im=Image.open(L/b['sources'][k]['file']);assert im.mode=='RGBA' and im.getextrema()[3][0]==0,k
  assert p.get('marginal_bunny_count',0)<=3
generation=read(V/'generation_evidence.json')
assert generation['calls']==len(generation['records'])==8
assert {q['id'] for q in generation['records'] if q['selected']}=={'DADDY_CAUDAL_FOCUSED_T03','RUMI_CAUDAL_FOCUSED_T03','CARE24_T01','CARE25_T01','COVER_OCCLUSION_FLOOR_T02'}
for q in generation['records']:
 assert sha(R/q['output'])==q['output_sha256'] and list(Image.open(R/q['output']).size)==q['native_size']
 for ref in q['bound_reference_records']:assert sha(R/ref['path'])==ref['sha256']
for q in read(V/'input_provenance.json'):
 assert sha(R/q['path'])==q['sha256']
 source=R/q['source']
 if source.is_file():
  assert sha(source)==q['source_sha256'],q['source']
  if 'crop' in q:
   a=Image.open(source).crop(q['crop']);z=Image.open(R/q['path'])
   assert a.mode==z.mode and a.size==z.size and a.tobytes()==z.tobytes(),q['path']
 else:assert q.get('frame_index_zero_based') in [384,396,408]
assert b['sources']['v39_lamma']['file'].endswith('assets/minigames/seek/lamma_animation.png')
assert b['sources']['v39_stained_glass']['file'].endswith('sky_lagoon_castle_stained_glass_v1.png')
for key in ['v39_lamma','v39_lamma_contact','v39_stained_glass']:
 p=(L/b['sources'][key]['file']).resolve();data=p.read_bytes();rel=p.relative_to(R).as_posix()
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==tree[rel],rel
lamma=[q for q in b['cover']['local_patches'] if q['source']=='v39_lamma'];assert len(lamma)==1
assert lamma[0]['source_canvas_box']==[1225,775,2065.0,1195.0] and lamma[0]['polygon']==[[1225,775],[1435,775],[1435,985],[1225,985]]
parts=read(C/'master_parts/parts.json');payload=b''.join((C/'master_parts'/q['file']).read_bytes() for q in parts['parts'])
assert hashlib.sha256(payload).hexdigest()==parts['master_sha256']==sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')
doc=pdfium.PdfDocument(str(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'))
for n in range(34):
 im=doc[n].render(scale=1.5).to_pil().convert('RGB');saved=Image.open(C/f'page_{n:02}.png').convert('RGB')
 assert im.size==(1512,1080) and ImageChops.difference(im,saved).getbbox() is None,n
assert len(list(C.glob('page_[0-9][0-9].png')))==34
guard=[q for q in b['cover']['local_patches'] if q['source']=='v39_foreground_lock'];assert len(guard)==1
a=np.asarray(Image.open(C/'page_00.png').convert('RGB'),dtype=np.int16);z=np.asarray(Image.open(OLD/'complete/page_00.png').convert('RGB'),dtype=np.int16)
m=Image.new('L',(1512,1080));ImageDraw.Draw(m).polygon(guard[0]['polygon'],fill=255);m=m.filter(ImageFilter.MinFilter(3))
assert np.max(np.abs(a-z)[np.asarray(m)>0])==0,'Roshan original foreground-fin pixels changed'

unchanged=read(V/'revision_scope.json')['unchanged_pdf_pages']
for n in unchanged:assert sha(C/f'page_{n:02}.png')==sha(OLD/'complete'/f'page_{n:02}.png'),('Unchanged exact proof',n)
scratch=R/'tmp/pdfs/v39';scratch.mkdir(parents=True,exist_ok=True)
def no_text(source,dest):
 w=PdfWriter();r=PdfReader(source)
 for p in r.pages:w.add_page(p)
 w.remove_text()
 with dest.open('wb') as f:w.write(f)
no_text(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf',scratch/'current_art.pdf')
no_text(OLD/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf',scratch/'baseline_art.pdf')
cur=pdfium.PdfDocument(str(scratch/'current_art.pdf'));before=pdfium.PdfDocument(str(scratch/'baseline_art.pdf'));pixels=[]
for n in range(34):
 if n==2:
  pixels.append(dict(page=2,method='Owner-directed exact native demo source/crop replacement, not a bounded local patch',outside_declared_masks_pixels_over_one_level=None));continue
 aa=cur[n].render(scale=1.5).to_pil().convert('RGB');bb=before[n].render(scale=1.5).to_pil().convert('RGB');mask=Image.new('L',aa.size);draw=ImageDraw.Draw(mask)
 for q in prov['layers']:
  if q['page']==('front_cover' if n==0 else 'back_cover' if n==33 else n) and q['operation'].startswith('bounded_') and q['source_key'].startswith('v39_'):
   rw,rh=q['clip_reference_size'];ox,oy,s=q['clip_canvas_transform_points'];poly=[(ox+x*s,oy+(rh-y)*s) for x,y in q['clip_polygon_source_pixels']]
   if n==33 and b['back_cover'].get('view_transform'):
    t=b['back_cover']['view_transform'];poly=[(x*t['scale']+t['translate'][0],y*t['scale']+t['translate'][1]) for x,y in poly]
   draw.polygon([(x*3,(360-y)*3) for x,y in poly],fill=255)
 mask=mask.filter(ImageFilter.MaxFilter(13));diff=np.max(np.abs(np.asarray(aa,dtype=np.int16)-np.asarray(bb,dtype=np.int16)),axis=2);outside=np.asarray(mask)==0
 count=int(np.count_nonzero(diff[outside]>1))
 if count:issues.append('Outside declared local edits: '+str((n,count)))
 pixels.append(dict(page=n,outside_declared_masks_pixels_over_one_level=count))
# V37 composed method, same fill, median and worst-decile thresholds, stroke excluded.
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
assert len(contrast)==86,len(contrast)
counts={k:sum(q['verdict']==k for q in contrast) for k in ['PASS','OUTLINE_REQUIRED','FAIL']}
save(V/'composed_caption_contrast.json',dict(method='Exact V37 fill/median/worst10percent luminance thresholds, sampled from caption-free final PDF with actual local repairs; stroke excluded.',baseline=dict(lines=86,PASS=79,OUTLINE_REQUIRED=7,FAIL=0),counts=counts,lines=contrast))
(V/'composed_caption_contrast.tsv').write_text('page\tcolor\ttypical\tworst\tverdict\ttext\n'+'\n'.join(f"{q['page']}\t{q['color']}\t{q['typical']}\t{q['worst']}\t{q['verdict']}\t{q['text']}" for q in contrast)+'\n',encoding='utf8',newline='\n')
if '--preflight' not in sys.argv:
 visual=read(V/'visual_audits.json')
 assert len(visual['passes'])==5 and all(q['result']=='PASS_WITH_DECLARED_A9_HOLD' and not q['remaining_in_scope_defects'] for q in visual['passes'])
 assert visual['pdf_sha256']==sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')
 assert visual['email_sha256']==sha(C/'Mermaid_Roshan_Book_V39_Email.pdf')
out=dict(status='FAIL' if issues else 'PREFLIGHT_PASS' if '--preflight' in sys.argv else 'PASS_WITH_DECLARED_A9_HOLD',baseline=BASE,pages=34,story_pages=32,page_size_points=[1008,720],source_seal=sealed,source_seal_count=len(sealed),exact_pdf_proofs=34,unchanged_byte_exact_proofs=unchanged,all34_outside_mask_checks=pixels,mask_tolerance='Six reference pixels dilation for declared 0–2px Gaussian edge feather and raster antialias; differences over one RGB level outside fail',contrast_counts=counts,issues=issues,held=['A9 native-resolution hold retained exactly from V38; native720p demo still is review source, not final-print-resolution approval'],acceptance='Machine evidence; independent AI visual review separately recorded. Owner/child/SLP/trim/PPI/physical print remain open; no print edition or runtime claim.')
out.update(original_roshan_foreground_guard_pixels=int(np.count_nonzero(np.asarray(m)>0)),original_roshan_foreground_max_rgb_difference=0,pdf_sha256=sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),book_sha256=sha(L/'book.json'),book_canonical_sha256=hashlib.sha256(json.dumps(b,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),provenance_sha256=sha(C/'page_provenance.json'),actual_glyph_focal_checks=focal_ink_checks,generation_calls=8,selected_local_candidates=5)
save(C/'verification.json',out)
print(json.dumps({k:v for k,v in out.items() if k not in ['source_seal','all34_outside_mask_checks','unchanged_byte_exact_proofs','actual_glyph_focal_checks']},ensure_ascii=False,indent=2))
if issues:raise SystemExit(1)
