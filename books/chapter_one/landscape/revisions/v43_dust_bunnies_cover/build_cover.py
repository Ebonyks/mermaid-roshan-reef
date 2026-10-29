"""Render the editable cover, then carry all 33 V42 email pages unchanged."""
from pathlib import Path
from io import BytesIO
import hashlib,json,sys
import numpy as np
from PIL import Image
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject
import pypdfium2 as pdfium

V=Path(__file__).resolve().parent
L=V.parents[1]
R=V.parents[4]
C=V/'complete'
C.mkdir(exist_ok=True)
sha=lambda data:hashlib.sha256(data).hexdigest()
source=L/'render_book.py'
program=source.read_text(encoding='utf8')
program=program[:program.index("for p in B['pages']:")]+"""c.save()
(O/'cover_provenance.json').write_text(json.dumps(dict(layers=LAYERS,text_lines=TEXT_LINES),indent=2)+'\\n',encoding='utf8',newline='\\n')
"""
sys.argv=['render_book.py','--book',str(V/'BOOK_CURRENT.json'),'--output',str(C)]
exec(compile(program,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
lossless=C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'
cover=C/'Mermaid_Roshan_Dust_Bunnies_Cover_V43.pdf'
lossless.replace(cover)
original=PdfReader(cover)
proof=pdfium.PdfDocument(str(cover))[0].render(scale=1.5).to_pil().convert('RGB')
proof.save(C/'page_00.png')
# Native dimensions, exact alpha and vector drawing operations survive this
# cover-only email compression. The lossless cover above stays the art master.
ref=np.asarray(proof,dtype=np.float32)
attempts=[]
for quality in (82,86,90,94,98):
 writer=PdfWriter()
 writer.clone_document_from_reader(PdfReader(cover))
 for val in writer.pages[0]['/Resources'].get('/XObject',{}).values():
  obj=val.get_object()
  if obj.get('/Subtype')!='/Image' or str(obj.get('/ColorSpace'))!='/DeviceRGB' or obj.get('/BitsPerComponent')!=8:continue
  w,h=int(obj['/Width']),int(obj['/Height'])
  image=Image.frombytes('RGB',(w,h),obj.get_data())
  buf=BytesIO();image.save(buf,format='JPEG',quality=quality,subsampling=0,optimize=True)
  if len(buf.getvalue())>=len(obj._data):continue
  obj._data=buf.getvalue();obj.decoded_self=None
  obj[NameObject('/Filter')]=NameObject('/DCTDecode')
  if '/DecodeParms' in obj:del obj['/DecodeParms']
 compressed=BytesIO();writer.write(compressed)
 data=compressed.getvalue()
 probe=pdfium.PdfDocument(data)
 candidate=np.asarray(probe[0].render(scale=1.5).to_pil().convert('RGB'),dtype=np.float32)
 mse=float(np.mean((candidate-ref)**2));psnr=float(10*np.log10(255**2/mse)) if mse else 100.
 attempts.append(dict(quality=quality,bytes=len(data),psnr_db=psnr))
 probe.close()
 if psnr>=40:break
else:raise RuntimeError('Cover email fidelity below40dB')
old=L/'revisions/v42_doublewide_arrival/complete/Mermaid_Roshan_Book_V42_Email.pdf'
prior=PdfReader(old)
writer=PdfWriter();writer.add_page(PdfReader(BytesIO(data)).pages[0])
for page in prior.pages[1:]:writer.add_page(page)
writer.add_metadata({'/Title':'Mermaid Roshan and the Dust Bunnies','/Author':'Mermaid Roshan picture-book project','/Subject':'V43 cover review; mixed-width illustration review; physical print held'})
reading=C/'Mermaid_Roshan_and_the_Dust_Bunnies_V43.pdf'
with reading.open('wb') as f:writer.write(f)
assert reading.stat().st_size<25000000
doc=pdfium.PdfDocument(str(reading))
doc[0].render(scale=1.5).to_pil().convert('RGB').save(C/'reading_cover.png')
for i in (1,2,3,24,29,33):
 im=doc[i].render(scale=.4).to_pil().convert('RGB')
 im.save(C/f'context_{i:02}.png')
record=dict(cover_master_sha256=sha(cover.read_bytes()),reading_sha256=sha(reading.read_bytes()),reading_bytes=reading.stat().st_size,baseline_v42_pdf=str(old.relative_to(R)).replace('\\','/'),baseline_v42_pdf_sha256=sha(old.read_bytes()),cover_compression_attempts=attempts,body_method='All33 V42 email PDF pages copied with original vectors,raster streams,alpha,page boxes and text; exact rendered checks in verification.json',source_art='Existing layered V42 cover; two newly posed bunnies plus bounded120x170sourcepixel floor continuity repair; exact original Lamma first cel behind original bucket',status='COVER_REVIEW_OWNER_ACCEPTANCE_OPEN')
(C/'export_record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(record,indent=2))
