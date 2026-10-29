"""Fail closed on changed cover inputs, interior pages, text, alpha or review bindings."""
from pathlib import Path
import json,hashlib,subprocess,sys
import numpy as np
from PIL import Image
from pypdf import PdfReader
import pypdfium2 as pdfium

V=Path(__file__).resolve().parent;R=V.parents[4];L=V.parents[1];C=V/'complete'
sha=lambda data:hashlib.sha256(data).hexdigest()
b=json.loads((V/'BOOK_CURRENT.json').read_text('utf8'));old=json.loads((V/'BOOK_BASELINE.json').read_text('utf8'))
assert b==json.loads((L/'book.json').read_text('utf8'))
assert b['title']=='Mermaid Roshan and the Dust Bunnies'
assert b['pages']==old['pages'] and b['back_cover']==old['back_cover']
for key,value in old['sources'].items():assert b['sources'][key]==value,key
assert set(b['sources'])-set(old['sources'])=={'v43_bunny_pair','v43_lamma_first','v43_floor_repair'}
baseline='5fbdc77157341686d5db5ca70fce597e9ab8e7b3'
original=json.loads(subprocess.check_output(['git','show',baseline+':books/chapter_one/landscape/book.json'],cwd=R))
assert old==original
sealed=[]
paths={(L/q['file']).resolve().relative_to(R).as_posix() for q in old['sources'].values()}
paths.add((L/old['font']).resolve().relative_to(R).as_posix())
for path in sorted(paths):
 data=subprocess.check_output(['git','show',baseline+':'+path],cwd=R)
 assert (R/path).read_bytes()==data,path
 sealed.append(dict(path=path,sha256=sha(data)))
record=json.loads((V/'generation_record.json').read_text())
assert record['native_sha256']==sha((V/record['native_output']).read_bytes())
assert record['prompt_sha256']==sha((V/record['prompt']).read_bytes())
for ref in record['references']:assert ref['sha256']==sha((V/ref['packet_copy']).read_bytes())
im=Image.open(V/record['native_output']);assert im.mode=='RGBA' and im.getextrema()[3][0]==0
old_pdf=L/'revisions/v42_doublewide_arrival/complete/Mermaid_Roshan_Book_V42_Email.pdf'
new_pdf=C/'Mermaid_Roshan_and_the_Dust_Bunnies_V43.pdf';cover_pdf=C/'Mermaid_Roshan_Dust_Bunnies_Cover_V43.pdf'
x,y=PdfReader(old_pdf),PdfReader(new_pdf);dx,dy=pdfium.PdfDocument(str(old_pdf)),pdfium.PdfDocument(str(new_pdf))
assert len(x.pages)==len(y.pages)==34
assert y.metadata.title==b['title']
assert 'Dust Bunnies' in y.pages[0].extract_text() and 'Hidden Rainbow' not in y.pages[0].extract_text()
checks=[]
for i in range(1,34):
 a,c=x.pages[i],y.pages[i]
 assert a.mediabox==c.mediabox and a.extract_text()==c.extract_text(),i
 assert a.get_contents().get_data()==c.get_contents().get_data(),i
 images=0;masks=0
 for name,val in a['/Resources'].get('/XObject',{}).items():
  u=val.get_object();v=c['/Resources']['/XObject'][name].get_object()
  if u.get('/Subtype')!='/Image':continue
  assert u._data==v._data and u['/Width']==v['/Width'] and u['/Height']==v['/Height'],(i,name)
  images+=1
  if u.get('/SMask'):assert u['/SMask'].get_object()._data==v['/SMask'].get_object()._data;masks+=1
 pa=np.asarray(dx[i].render(scale=1.5).to_pil().convert('RGB'));pb=np.asarray(dy[i].render(scale=1.5).to_pil().convert('RGB'))
 assert np.array_equal(pa,pb),i
 checks.append(dict(pdf_entry=i,render_rgb_sha256=sha(pa.tobytes()),dimensions=list(pa.shape[1::-1]),text_vectors_boxes_and_image_streams_exact=True,images=images,masks=masks))
print('33/33 carried pages: exact renders, captions, boxes, vectors, images and masks',flush=True)
cover=pdfium.PdfDocument(str(cover_pdf));actual=np.asarray(cover[0].render(scale=1.5).to_pil().convert('RGB'))
assert np.array_equal(actual,np.asarray(Image.open(C/'page_00.png').convert('RGB')))
proof=np.asarray(Image.open(V/'references/v42_cover.png').convert('RGB'))
mask=np.zeros(actual.shape[:2],bool)
mask[0:355,400:1340]=True  # Old/new title and removed subtitle.
mask[680:800,80:220]=True  # Tiny new Lamma head above original bucket.
mask[630:1080,1100:1512]=True  # New bunnies and removed old full-body Lamma.
assert not np.any(np.any(actual!=proof,axis=2)&~mask),'Pixels changed outside declared cover-edit windows'
assert np.array_equal(actual[790:1080,:360],proof[790:1080,:360]),'Original bucket/floor changed'
assert np.array_equal(actual[350:680,10:850],proof[350:680,10:850]),'Family changed'
assert np.array_equal(actual[550:900,860:1170],proof[550:900,860:1170]),'Eagle body changed'
assert np.array_equal(actual[900:1000,860:1145],proof[900:1000,860:1145]),'Eagle feet changed'
# Same renderer + V42 controls must still reproduce the previous cover exactly.
scratch=R/'tmp/pdfs/v43/default_regression';scratch.mkdir(parents=True,exist_ok=True)
program=(L/'render_book.py').read_text('utf8');program=program[:program.index("for p in B['pages']:")]+"c.save()\n"
sys.argv=['render_book.py','--book',str(V/'BOOK_BASELINE.json'),'--output',str(scratch)]
exec(compile(program,str(L/'render_book.py'),'exec'),{'__file__':str(L/'render_book.py'),'__name__':'__main__'})
reg=pdfium.PdfDocument(str(scratch/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'))
assert np.array_equal(np.asarray(reg[0].render(scale=1.5).to_pil().convert('RGB')),proof)
assert new_pdf.stat().st_size<25000000
floor=json.loads((V/'floor_repair_record.json').read_text('utf8'))
for path,key in [('source','source_sha256'),('native_output','native_sha256'),('prompt','prompt_sha256')]:assert sha((V/floor[path]).read_bytes())==floor[key]
provenance=json.loads((C/'cover_provenance.json').read_text('utf8'))
for layer in provenance['layers']:assert sha((L/layer['file']).read_bytes())==layer['sha256']
review=json.loads((V/'visual_audits.json').read_text('utf8'))
assert review['cover_sha256']==sha(cover_pdf.read_bytes()) and review['reading_sha256']==sha(new_pdf.read_bytes())
assert len(review['passes'])==5
for row in review['passes']:
 assert row['result']=='PASS_SCOPED_COVER_REVIEW' and not row['remaining_in_scope_defects']
 for path in row['inspected']:assert sha((V/path).read_bytes())==row['inspected_sha256'][path],path
for path,digest in review['artifact_bindings'].items():assert sha((V/path).read_bytes())==digest,path
geometry=json.loads((V/'title_geometry.json').read_text('utf8'))
assert geometry['minimum_top_ink_inset_logical_points']>=18
assert geometry['cover_pdf_sha256']==sha(cover_pdf.read_bytes())
assert geometry['controls_sha256']==sha((V/'BOOK_CURRENT.json').read_bytes())
assert 'Dust Bunnies' in geometry['actual_title']

e=json.loads((C/'export_record.json').read_text());assert e['reading_sha256']==sha(new_pdf.read_bytes()) and e['cover_master_sha256']==sha(cover_pdf.read_bytes()) and e['cover_compression_attempts'][-1]['psnr_db']>=40
result=dict(status='PASS',baseline=baseline,title=b['title'],source_files_sealed=len(sealed),source_seals=sealed,body_entries_exact=checks,cover_master_sha256=sha(cover_pdf.read_bytes()),reading_sha256=sha(new_pdf.read_bytes()),cover_proof_sha256=sha((C/'page_00.png').read_bytes()),default_cover_regression='Exact V42 RGB at1512x1080 using new renderer and old controls',cover_change_windows_only=True,bucket_family_eagle_outside_named_edits_exact=True,cover_email_psnr_db=e['cover_compression_attempts'][-1]['psnr_db'],held=['Owner cover acceptance','Child/qualifiedSLP','Arrival physical pagination/gutter and V41 printP1-P8','Physical print/resolution/bleed'],issues=[])
(C/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
print('V43 source/scope/export/regression checks: ALL OK')
