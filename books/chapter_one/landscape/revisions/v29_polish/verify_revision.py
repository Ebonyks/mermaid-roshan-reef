"""Verify review PDF, source preservation and lossless document encoding."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageChops
from pypdf import PdfReader
import pypdfium2 as pdfium
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
B=json.loads((L/'book.json').read_text(encoding='utf8'));old=json.loads((V/'BOOK_BASELINE.json').read_text(encoding='utf8'))
pdf=C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf';reader=PdfReader(pdf)
assert len(reader.pages)==34
assert all(list(p.mediabox)==[0,0,504,360] for p in reader.pages)
assert pdf.stat().st_size<100*1024*1024,'PDF exceeds repository host file limit'
layout=json.loads((C/'page_provenance.json').read_text(encoding='utf8'))
for p in B['pages']:
 text=''.join(reader.pages[p['page']].extract_text().split())
 for line in [r['text'] for r in layout['text_lines'] if r['page']==p['page']]:
  assert ''.join(line.split()) in text,(p['page'],line,text)
assert all(k not in [a for p in B['pages'] for a in p['art']] for k in ['v25_shell_duel','v25_art_simple','approved_apology_canvas'])
keys=['cover_rendered',B['back_cover']['art'],'R11_land','v27_door','v22_art_sorting']
preserved=[]
for key in keys:
 assert B['sources'][key]['file']==old['sources'][key]['file']
 path=(L/B['sources'][key]['file']).resolve();rp=path.relative_to(R.resolve()).as_posix()
 baseline=subprocess.check_output(['git','show','5da33b22c9b95358d98defe8e340a901d5470991:'+rp],cwd=R)
 assert hashlib.sha256(baseline).hexdigest()==sha(path)
 preserved.append(dict(key=key,path=rp,sha256=sha(path)))
doc=pdfium.PdfDocument(str(pdf));screens=[]
for i,page in enumerate(doc):
 # Compare the final optimized PDF to the proof PNG made before stream optimization.
 render=page.render(scale=3).to_pil().convert('RGB');before=Image.open(C/f'page_{i:02}.png').convert('RGB')
 assert render.size==before.size
 assert ImageChops.difference(render,before).getbbox() is None,('PDF raster changed during lossless encoding',i)
 screens.append(dict(page_index=i,dimensions=list(render.size),png_sha256=sha(C/f'page_{i:02}.png')))
filters={};fonts=[]
for page in reader.pages:
 for value in page.get('/Resources',{}).get('/XObject',{}).values():
  obj=value.get_object()
  if obj.get('/Subtype')=='/Image':
   f=str(obj.get('/Filter'));filters[f]=filters.get(f,0)+1
   assert '/DCTDecode' not in f and '/JPXDecode' not in f,'Lossy document image stream'
 for value in page.get('/Resources',{}).get('/Font',{}).values():
  font=value.get_object()
  if 'Sniglet' in str(font.get('/BaseFont')):
   descriptor=font['/FontDescriptor'].get_object();assert descriptor.get('/FontFile2')
   fonts.append(str(font['/BaseFont']))
assert fonts,'Sniglet font not embedded'
assert min(row['font_size'] for row in layout['text_lines'] if isinstance(row['page'],int))>=18
result=dict(status='MECHANICAL_PASS; OWNER_CHILD_PRINT_SLP_ACCEPTANCE_PENDING',revision='V29',total_pages=34,story_pages=32,trim_points=[504,360],book_json_sha256=sha(L/'book.json'),page_provenance_sha256=sha(C/'page_provenance.json'),pdf_sha256=sha(pdf),pdf_bytes=pdf.stat().st_size,native_text_matches_manuscript=True,lossless_optimized_pdf_raster_matches_all34screenshots=True,pdf_image_filters=filters,embedded_story_fonts=sorted(set(fonts)),preserved_sources=preserved,screenshots=screens,scope='Book only; no game runtime or protected asset change.',remaining=B['limitations'])
save(C/'verification.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['screenshots','preserved_sources','remaining']},indent=2))
