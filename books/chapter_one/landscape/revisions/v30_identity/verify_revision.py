"""Verify complete PDF plus exact outside-region preservation against V29."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageChops,ImageDraw,ImageFilter
from pypdf import PdfReader
import pypdfium2 as pdfium
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete';OLD=V.parent/'v29_polish/complete'
BASE='82a6dc1dba381c0b3ef507a8397512fa09ef624e'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text('utf-8'))
def save(p,q):p.write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
B=read(L/'book.json');old=read(V/'BOOK_BASELINE.json');layout=read(C/'page_provenance.json')
pdf=C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf';reader=PdfReader(pdf)
assert len(reader.pages)==34 and len(B['pages'])==32
assert all(list(p.mediabox)==[0,0,504,360] for p in reader.pages)
assert pdf.stat().st_size<100*1024*1024
assert [p['page'] for p in B['pages']]==[p['page'] for p in old['pages']]
for p,q in zip(B['pages'],old['pages']):
 assert p['text']==q['text'] or (p['page']==5 and p['text']=='Daddy gave her a brush and some sponges.\n“One little job at a time.”')
 assert p['art'][:len(q['art'])]==q['art']
 assert p['caption']==q['caption']
 text=''.join(reader.pages[p['page']].extract_text().split())
 for line in [r['text'] for r in layout['text_lines'] if r['page']==p['page']]:assert ''.join(line.split()) in text
preserved=[]
for key in ['cover_rendered',B['back_cover']['art'],'v23_castle_repair','v26_rumi_trapped','R11_land','v27_door','v22_art_sorting']:
 path=(L/B['sources'][key]['file']).resolve();rp=path.relative_to(R.resolve()).as_posix()
 data=subprocess.check_output(['git','show',BASE+':'+rp],cwd=R)
 assert hashlib.sha256(data).hexdigest()==sha(path)
 preserved.append({'source':key,'path':rp,'sha256':sha(path),'base_pixels_unchanged':True})
for layer in layout['layers']:assert sha(L/layer['file'])==layer['sha256']
doc=pdfium.PdfDocument(str(pdf));screens=[];changed=[];unchanged=[];outside=[]
for n,page in enumerate(doc):
 im=page.render(scale=3).to_pil().convert('RGB');proof=Image.open(C/f'page_{n:02}.png').convert('RGB')
 assert ImageChops.difference(im,proof).getbbox() is None,('Export pixel mismatch',n)
 baseline=Image.open(OLD/f'page_{n:02}.png').convert('RGB')
 diff=ImageChops.difference(proof,baseline)
 if diff.getbbox() is None:unchanged.append(n)
 else:
  changed.append(n);page_id='front_cover' if n==0 else 'back_cover' if n==33 else n
  mask=Image.new('L',proof.size,0);d=ImageDraw.Draw(mask)
  for layer in layout['layers']:
   if layer['page']!=page_id:continue
   if 'clip_polygon_source_pixels' in layer:
    rw,rh=layer['clip_reference_size'];s=max(504/rw,360/rh);ox=(504-rw*s)/2;oy=(360-rh*s)/2
    d.polygon([((ox+x*s)*3,(360-oy-(rh-y)*s)*3) for x,y in layer['clip_polygon_source_pixels']],fill=255)
   if n==5 and layer['source_key']=='v30_yellow_sponge':
    x,y,w,h=layer['target_box_points'];d.rectangle((x*3,(360-y-h)*3,(x+w)*3,(360-y)*3),fill=255)
  if n==5:
   for prov in [layout,read(OLD/'page_provenance.json')]:
    for layer in prov['layers']:
     if layer['page']==5 and layer['role']=='story_art':
      x,y,w,h=layer['target_box_points'];d.rectangle((x*3,(360-y-h)*3,(x+w)*3,(360-y)*3),fill=255)
   for prov in [layout,read(OLD/'page_provenance.json')]:
    for line in prov['text_lines']:
     if line['page']==5:
      x,y,w,h=line['box'];d.rectangle((x*3,(360-y-h)*3,(x+w)*3,(360-y)*3),fill=255)
  mask=mask.filter(ImageFilter.MaxFilter(7)) # Three proof-pixel antialias allowance at exposed boundaries.
  rem=ImageChops.multiply(diff,Image.merge('RGB',[ImageChops.invert(mask)]*3))
  assert rem.getbbox() is None,('Outside declared local scopes changed',n,rem.getbbox())
  outside.append({'page':n,'outside_declared_regions_changed_pixels':0,'boundary_allowance_proof_pixels':3})
 screens.append({'page_index':n,'dimensions':list(im.size),'png_sha256':sha(C/f'page_{n:02}.png')})
assert changed==[0,4,5,10,33] and len(unchanged)==29
filters={};fonts=[]
for page in reader.pages:
 for value in page.get('/Resources',{}).get('/XObject',{}).values():
  obj=value.get_object()
  if obj.get('/Subtype')=='/Image':
   f=str(obj.get('/Filter'));filters[f]=filters.get(f,0)+1;assert '/DCTDecode' not in f and '/JPXDecode' not in f
 for value in page.get('/Resources',{}).get('/Font',{}).values():
  font=value.get_object()
  if 'Sniglet' in str(font.get('/BaseFont')):assert font['/FontDescriptor'].get_object().get('/FontFile2');fonts.append(str(font['/BaseFont']))
assert fonts and min(q['font_size'] for q in layout['text_lines'] if isinstance(q['page'],int))>=18
result={'status':'MECHANICAL_PASS; EXTERNAL_ACCEPTANCE_SEPARATE','revision':'V30','total_pages':34,'story_pages':32,'trim_points':[504,360],'book_json_sha256':sha(L/'book.json'),'page_provenance_sha256':sha(C/'page_provenance.json'),'pdf_sha256':sha(pdf),'pdf_bytes':pdf.stat().st_size,'native_text_matches_manuscript':True,'lossless_optimized_pdf_raster_matches_all34screenshots':True,'pdf_image_filters':filters,'embedded_story_fonts':sorted(set(fonts)),'changed_pages':changed,'unchanged_pages_byte_identical_to_v29':unchanged,'outside_region_preservation':outside,'preserved_sources':preserved,'screenshots':screens,'scope':'Full-book source/text/geometry/export checks and exact scoped delta evidence; visual/clinical/print acceptance not inferred.'}
save(C/'verification.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['screenshots','preserved_sources']},indent=2))
