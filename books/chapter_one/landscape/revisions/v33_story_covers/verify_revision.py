"""Verify unchanged interiors/originals and exact cover-only source/mask scope."""
from pathlib import Path
from collections import Counter
import hashlib,json,subprocess
from PIL import Image,ImageChops,ImageDraw,ImageFilter
import pypdfium2 as pdfium
from pypdf import PdfReader
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete';OLD=V.parent/'v32_rainbow_story'/'complete';BASE='2719d2fcf66afe4cb73b8445087e09dd52319849'
def read(p):return json.loads(p.read_text('utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def page(prov,n):return [q for q in prov['layers'] if q['page']==('front_cover' if n==0 else 'back_cover' if n==33 else n)]
b=read(L/'book.json');old=read(V/'BOOK_BASELINE.json');layout=read(C/'page_provenance.json');op=read(OLD/'page_provenance.json')
assert b['pages']==old['pages'] and b['font']==old['font']
assert all(b['sources'][k]==v for k,v in old['sources'].items())
tree={}
for entry in subprocess.check_output(['git','ls-tree','-r','-z',BASE],cwd=R).split(b'\0'):
 if entry:
  head,path=entry.split(b'\t',1);tree[path.decode('utf8')]=head.split()[2].decode()
sealed=[]
for p in sorted({(L/q['file']).resolve() for q in old['sources'].values()}|{(L/old['font']).resolve()}):
 data=p.read_bytes();rel=p.relative_to(R).as_posix()
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==tree[rel],rel
 sealed.append(dict(path=rel,sha256=hashlib.sha256(data).hexdigest()))
assert len(b['pages'])==32
for n in range(1,33):
 assert sha(C/f'page_{n:02}.png')==sha(OLD/f'page_{n:02}.png'),n
 assert page(layout,n)==page(op,n),n
assert [q for q in layout['text_lines']]==op['text_lines']
def polygon_mask(layers,size):
 mask=Image.new('L',size);draw=ImageDraw.Draw(mask)
 for q in layers:
  rw,rh=q['clip_reference_size'];ox,oy,s=q['clip_canvas_transform_points']
  draw.polygon([((ox+x*s)*3,(360-oy-(rh-y)*s)*3) for x,y in q['clip_polygon_source_pixels']],fill=255)
 return mask
checks=[]
for n,previous in [(0,0),(33,26)]:
 after=Image.open(C/f'page_{n:02}.png').convert('RGB');before=Image.open(OLD/f'page_{previous:02}.png').convert('RGB')
 additions=[q for q in page(layout,n) if q['source_key'].startswith('v33_')]
 mask=polygon_mask(additions,after.size)
 if n==33:
  draw=ImageDraw.Draw(mask)
  for q in op['text_lines']:
   if q['page']==26:
    x,y,w,h=q['box'];draw.rectangle((x*3,(360-y-h)*3,(x+w)*3,(360-y)*3),fill=255)
 mask=mask.filter(ImageFilter.MaxFilter(7))
 outside=ImageChops.multiply(ImageChops.difference(before,after),ImageChops.invert(mask).convert('RGB'))
 assert outside.getbbox() is None,(n,outside.getbbox())
 checks.append(dict(page=n,compared_to_v32_page=previous,outside_declared_regions_changed_pixels=0,scope='Two front local edits' if n==0 else 'Exact existing scene26; remove caption; tiny shelf cameo only'))
scene=[{k:v for k,v in q.items() if k!='page'} for q in page(layout,26)]
rear=[{k:v for k,v in q.items() if k!='page'} for q in page(layout,33) if not q['source_key'].startswith('v33_')]
assert scene==rear
pdf=C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf';reader=PdfReader(pdf);baseline=PdfReader(OLD/pdf.name);doc=pdfium.PdfDocument(str(pdf))
assert len(reader.pages)==len(doc)==34
for n,p in enumerate(doc):
 im=p.render(scale=3).to_pil().convert('RGB')
 assert ImageChops.difference(im,Image.open(C/f'page_{n:02}.png').convert('RGB')).getbbox() is None,n
 assert ''.join(reader.pages[n].extract_text().split())==''.join(baseline.pages[n].extract_text().split()),n
 assert list(reader.pages[n].mediabox)==[0,0,504,360]
assert len(pdf.read_bytes())<100*1024*1024
e=read(V/'generation_evidence.json')
for q in e['generated']:
 assert q['native_output']['sha256']==sha(R/q['native_output']['path'])
 assert q['prompt_sha256']==hashlib.sha256(q['prompt'].encode()).hexdigest()
 for ref in q['references']:assert ref['sha256']==sha(R/ref['path'])
record=dict(status='PASS',baseline=BASE,revision='V33',story_pages=32,total_pages=34,changed_pages=[0,33],interior_pages_byte_identical_to_v32=list(range(1,33)),book_json_sha256=sha(L/'book.json'),page_provenance_sha256=sha(C/'page_provenance.json'),pdf_sha256=sha(pdf),pdf_bytes=pdf.stat().st_size,all34_lossless_pdf_renders_match_pngs=True,all_native_text_and_trim_exact=True,all_interior_source_transforms_exact=True,rear_reuses_exact_story26_source_layers=True,outside_region_preservation=checks,source_and_font_files_sealed=len(sealed),sealed_sources=sealed,screen_hashes=[dict(page=n,sha256=sha(C/f'page_{n:02}.png')) for n in range(34)],scope='Mechanical source/layout/text/export evidence only; root native/editorial review and owner/child/print acceptance remain separate.')
save(C/'verification.json',record);print(json.dumps({k:v for k,v in record.items() if k not in ['sealed_sources','screen_hashes']},indent=2))
