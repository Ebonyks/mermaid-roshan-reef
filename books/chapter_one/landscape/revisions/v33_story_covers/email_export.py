"""Separate email PDF: native image sizes, exact text/geometry and alpha masks."""
from pathlib import Path
from io import BytesIO
import hashlib,json,struct,zlib
import numpy as np
from PIL import Image
import pypdfium2 as pdfium
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject
V=Path(__file__).resolve().parent;C=V/'complete';R=V.parents[4]
source=C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf';raw=source.read_bytes();source_hash=hashlib.sha256(raw).hexdigest()
out=C/'Mermaid_Roshan_Book_V33_Email.pdf';attempts=[];cache={}
for quality in [91,89]:
 reader=PdfReader(BytesIO(raw));writer=PdfWriter();writer.clone_document_from_reader(reader);seen=set();count=0
 for page in writer.pages:
  for value in page['/Resources'].get('/XObject',{}).values():
   obj=value.get_object()
   if id(obj) in seen:continue
   seen.add(id(obj))
   if obj.get('/Subtype')!='/Image' or str(obj.get('/ColorSpace'))!='/DeviceRGB' or obj.get('/BitsPerComponent')!=8:continue
   w,h=int(obj['/Width']),int(obj['/Height']);key=hashlib.sha256(obj._data).hexdigest()
   if key in cache:im=cache[key]
   else:
    dp=obj.get('/DecodeParms',{})
    if str(obj.get('/Filter'))=='/FlateDecode' and dp.get('/Predictor')==15 and dp.get('/Colors')==3 and dp.get('/Columns')==w:
     def chunk(tag,data):return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
     png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',obj._data)+chunk(b'IEND',b'')
     im=Image.open(BytesIO(png)).convert('RGB')
    else:im=Image.frombytes('RGB',(w,h),obj.get_data())
    cache[key]=im
   buf=BytesIO();im.save(buf,format='JPEG',quality=quality,subsampling=0,optimize=True)
   if len(buf.getvalue())>=len(obj._data):continue
   obj._data=buf.getvalue();obj[NameObject('/Filter')]=NameObject('/DCTDecode');obj.decoded_self=None
   if '/DecodeParms' in obj:del obj['/DecodeParms']
   count+=1
 with out.open('wb') as f:writer.write(f)
 attempts.append(dict(quality=quality,bytes=out.stat().st_size,image_streams=count))
 print(json.dumps(attempts[-1]),flush=True)
 if out.stat().st_size<=24_000_000:break
else:raise RuntimeError('Email size budget not met')
original=PdfReader(BytesIO(raw));email=PdfReader(out);a=pdfium.PdfDocument(raw);b=pdfium.PdfDocument(str(out));checks=[];masks=0
assert len(a)==len(b)==34
qa=R/'tmp/pdfs/book_cover_v33/email_qa';qa.mkdir(parents=True,exist_ok=True)
for n,(pa,pb) in enumerate(zip(a,b)):
 x=original.pages[n];y=email.pages[n]
 assert x.get_contents().get_data()==y.get_contents().get_data() and x.extract_text()==y.extract_text()
 assert x.mediabox==y.mediabox
 for key in x['/Resources'].get('/XObject',{}):
  u=x['/Resources']['/XObject'][key].get_object();v=y['/Resources']['/XObject'][key].get_object()
  if u.get('/Subtype')=='/Image':
   assert u['/Width']==v['/Width'] and u['/Height']==v['/Height']
   if u.get('/SMask'):assert u['/SMask'].get_object()._data==v['/SMask'].get_object()._data;masks+=1
 aa=np.asarray(pa.render(scale=1.5).to_pil().convert('RGB')).astype(np.float32)
 bb=np.asarray(pb.render(scale=1.5).to_pil().convert('RGB')).astype(np.float32)
 mse=float(np.mean((aa-bb)**2));psnr=float(10*np.log10(255**2/mse)) if mse else 100
 assert psnr>=40,(n,psnr)
 checks.append(dict(page=n,render_psnr_db=psnr,text_vector_content_trim_and_image_sizes_exact=True))
 if n in [0,33]:pb.render(scale=3).to_pil().convert('RGB').save(qa/f'page_{n:02}.png')
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
record=dict(status='PASS',source_sha256=source_hash,output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),output_bytes=out.stat().st_size,attempts=attempts,pages=checks,alpha_mask_placements_byte_exact=masks,native_pixel_sizes_preserved=True,source_unchanged=True,minimum_render_psnr_db=min(q['render_psnr_db'] for q in checks),method='Separate JPEG4:4:4 email derivative; original vector text, clips, page geometry and lossless alpha retained. Original master remains lossless.',visual_review='PENDING native cover sample inspection')
(C/'email_verification.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:v for k,v in record.items() if k!='pages'},indent=2))
