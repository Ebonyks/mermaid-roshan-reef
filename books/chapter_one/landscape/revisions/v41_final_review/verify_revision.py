"""V41 strict scope/source/manuscript/geometry/exact-proof and composed-contrast gate."""
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess,sys,re
import numpy as np
from PIL import Image,ImageDraw,ImageChops,ImageFilter,ImageFont
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete';OLD=V.parent/'v40_wide_arrival';BASE='0d1c49d11651e292a13885413a043f8044032836'
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
 allowed=['art','art_crop','background_theme'] if n==2 else ['local_patches'] if n==5 else []
 if n==5:
  assert [q for q in p['local_patches'] if q['source']!='v41_door_dust']==[q for q in before['local_patches'] if q['source']!='v38_door_dust']
  dust=[q for q in p['local_patches'] if q['source']=='v41_door_dust'];assert len(dust)==1 and dust[0]['opacity']==.9
 assert {k:v for k,v in p.items() if k not in allowed}=={k:v for k,v in before.items() if k not in allowed},n
 assert p['text']==before['text'] and p['caption']==before['caption'],n
assert b['back_cover']==old['back_cover'] and b['cover']==old['cover']
assert {k:v for k,v in b.items() if k not in ['pages','sources','revision','status','download_pdf_href']}=={k:v for k,v in old.items() if k not in ['pages','sources','revision','status','download_pdf_href']}
assert set(b['sources'])-set(old['sources'])=={'v41_arrival_full_setting','v41_door_dust'}
assert P[2]['art']==['v41_arrival_full_setting'] and P[2]['art_crop']==[0,0,6144,4389]
assert P[9]==old['pages'][8]
owner=(R/'books/chapter_one/handoffs/2026-10-18_v34_audit_fixes/OWNER_DECISION_2026-10-19.md').read_text('utf8')
rows={int(n):t.split(' | ')[0].strip().replace(' / ','\n') for n,t in re.findall(r'^\| (\d+) \| (.*?) \|$',owner,re.M) if int(n)<=32}
assert len(rows)==32
for n in P:assert words(P[n]['text'])==words(rows[n]),n
ink_font=ImageFont.truetype(str(L/b['font']),2000)
pdfmetrics.registerFont(TTFont('V41Gate',str(L/b['font'])))
focal_ink_checks=[]
for q in prov['text_lines']:
 x,y,w,h=q['box'];m=18 if isinstance(q['page'],str) else 24;stroke=max(q.get('outline',0),.85 if q.get('halo') else 0)/2
 if x-stroke<m or y-stroke<m or x+w+stroke>504-m or y+h+stroke>360-m:issues.append('Text inset: '+str(q))
 if isinstance(q['page'],int):
  assert q['font_size']==20 or (q['font_size']==18 and q['text'] in [a for z in P[q['page']].get('speech_bubbles',[]) for a in z['text'].split('\n')])
  # Global ascent includes unused accents. Use actual glyph ink plus half the
  # full stroke for focal contact, preserving the conservative inset test above.
  il,it,ir,ib=ink_font.getbbox(q['text'],anchor='ls');factor=q['font_size']/2000
  baseline=q['box'][1]-pdfmetrics.getDescent('V41Gate')*q['font_size']/1000
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
recipe=read(V/'world_composition_provenance.json');selection=recipe['selection']
assert recipe['full_panorama_preserved'] and recipe['horizontal_crop'] is None
assert sha(V/selection['output'])==selection['sha256']==b['sources']['v41_arrival_full_setting']['sha256']
for q in recipe['layers']:assert sha(R/q['source'])==q['sha256']
world=np.asarray(Image.open(V/'art/sky_lagoon_full_world.png').convert('RGB'));final=np.asarray(Image.open(V/selection['output']).convert('RGB'))
a,z=selection['protected_native_world_rows'];assert np.array_equal(world[a:z],final[1401+a:1401+z])
assert next(q for q in recipe['layers'] if 'four-tower' in q['role'])['source'].endswith('sky_lagoon_castle_four_tower_v4.png')
assert next(q for q in recipe['layers'] if q['role'].startswith('native demo plane'))['target_box']==[620,1050,960,523]
prior=read(OLD/'composition_provenance.json');q=next(q for q in prior['layers'] if q['role']=='plane isolation')
assert min(x for x,y in q['polygon'])>=358 and q['frame_index_zero_based']==396
plane=Image.open(R/q['output']);src=Image.open(R/q['source']).convert('RGBA').crop(q['crop'])
assert np.array_equal(np.asarray(plane)[:,:,:3],np.asarray(src)[:,:,:3])
generation=read(V/'generation_evidence.json');assert generation['calls']==3
for q in generation['attempts']:
 assert sha(R/q['native_output'])==q['sha256']
 assert hashlib.sha256(q['prompt'].encode()).hexdigest()==q['prompt_sha256']
 for ref in q['references']:assert sha(R/ref['path'])==ref['sha256']
parts=read(C/'master_parts/parts.json');payload=b''.join((C/'master_parts'/q['file']).read_bytes() for q in parts['parts'])
assert hashlib.sha256(payload).hexdigest()==parts['master_sha256']==sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')
doc=pdfium.PdfDocument(str(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'))
for n in range(34):
 im=doc[n].render(scale=1.5).to_pil().convert('RGB');saved=Image.open(C/f'page_{n:02}.png').convert('RGB')
 assert im.size==(1512,1080) and ImageChops.difference(im,saved).getbbox() is None,n
assert len(list(C.glob('page_[0-9][0-9].png')))==34
unchanged=read(V/'revision_scope.json')['unchanged_pdf_pages']
for n in unchanged:assert sha(C/f'page_{n:02}.png')==sha(OLD/'complete'/f'page_{n:02}.png'),('Unchanged exact proof',n)
scratch=R/'tmp/pdfs/v41';scratch.mkdir(parents=True,exist_ok=True)
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
  pixels.append(dict(page=2,method='Owner rejected V40: complete native geography restored; only sky/foreground extensions and bounded edge joins generated. Native protected world rows180:1748 exact.',outside_declared_masks_pixels_over_one_level=None));continue
 aa=cur[n].render(scale=1.5).to_pil().convert('RGB');bb=before[n].render(scale=1.5).to_pil().convert('RGB')
 if n==5:
  delta=np.max(np.abs(np.asarray(aa,dtype=int)-np.asarray(bb,dtype=int)),axis=2);mask=delta>1
  y,x=np.where(mask);bbox=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
  assert bbox[0]>=970 and bbox[1]>=550 and bbox[2]<=1205 and bbox[3]<=650,bbox
  pixels.append(dict(page=5,changed_bbox_proof=bbox,all_outside_bounded_dust_exact=True));continue
 assert ImageChops.difference(aa,bb).getbbox() is None,n
 pixels.append(dict(page=n,unchanged_caption_free_pixels_exact=True))
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
# Handoff B1: >6 maximum channel delta; contrast of mean linear luminances.
baseline5=np.asarray(Image.open(V.parent/'v37_consistency_20261022/complete/page_05.png').convert('RGB'))
current5=np.asarray(Image.open(C/'page_05.png').convert('RGB'));changed=np.max(np.abs(current5.astype(int)-baseline5.astype(int)),axis=2)>6
y,x=np.where(changed);bbox=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
l0=float(lum(baseline5[changed]).mean());l1=float(lum(current5[changed]).mean());ratio=(max(l0,l1)+.05)/(min(l0,l1)+.05)
dust=dict(method='Exact pinned V41 audit comparison: V37 underlying door, changedmask maxRGBdelta>6,216proofpixels/inch,contrast of mean linear luminances (not mean per-pixel contrast)',changed_pixels=int(changed.sum()),bbox=bbox,strip_height_pixels=bbox[3]-bbox[1],strip_height_inches=(bbox[3]-bbox[1])/216,underlying_mean_linear_luminance=l0,current_mean_linear_luminance=l1,contrast_of_mean_luminances=ratio,required_inches=.2,required_contrast=2,result='PASS' if (bbox[3]-bbox[1])>=44 and ratio>=2 else 'FAIL')
save(V/'dust_visibility.json',dust)
if dust['result']!='PASS':issues.append('B1 dust visibility')
if '--preflight' not in sys.argv:
 visual=read(V/'visual_audits.json')
 assert len(visual['passes'])==5 and all(q['result']=='PASS_PART1_REVIEW' and not q['remaining_in_scope_defects'] for q in visual['passes'])
 assert visual['pdf_sha256']==sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')
 assert visual['email_sha256']==sha(C/'Mermaid_Roshan_Book_V41_Email.pdf')
 for q in visual['passes']:
  for path in q['inspected']:assert sha(V/path)==q['inspected_sha256'][path],('Stale reviewed artifact',path)
out=dict(status='FAIL' if issues else 'PREFLIGHT_PASS' if '--preflight' in sys.argv else 'PASS_PART1_REVIEW',baseline=BASE,pages=34,story_pages=32,page_size_points=[1008,720],source_seal=sealed,source_seal_count=len(sealed),exact_pdf_proofs=34,unchanged_byte_exact_proofs=unchanged,all34_outside_mask_checks=pixels,mask_tolerance='Only story2 full context repair and bounded story5 dust;32 unnamed proof and caption-free pixels exact',contrast_counts=counts,issues=issues,held=['P1-P8 Part2 held until owner illustration acceptance; physical print,child reading,qualifiedSLP remain open'],B2='DONE: A9 closed as not needed at selected11in; no third bath drawing or upscale',acceptance='Machine evidence; independent AI and owner creative acceptance separate. No print edition/runtime/release claim.')
out.update(pdf_sha256=sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),book_sha256=sha(L/'book.json'),book_canonical_sha256=hashlib.sha256(json.dumps(b,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),provenance_sha256=sha(C/'page_provenance.json'),actual_glyph_focal_checks=focal_ink_checks,generation_calls=3,source_scene_reuse=True,dust=dust)
save(C/'verification.json',out)
print(json.dumps({k:v for k,v in out.items() if k not in ['source_seal','all34_outside_mask_checks','unchanged_byte_exact_proofs','actual_glyph_focal_checks']},ensure_ascii=False,indent=2))
if issues:raise SystemExit(1)
