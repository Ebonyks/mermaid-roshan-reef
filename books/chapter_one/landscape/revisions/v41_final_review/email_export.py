"""Adaptive email: native sizes, exact vectors/alpha, >=40dB/page, <=25MB."""
from pathlib import Path
from io import BytesIO
import hashlib,json,struct,zlib
import numpy as np
from PIL import Image
import pypdfium2 as pdfium
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject
V=Path(__file__).resolve().parent;C=V/'complete'
source=C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf';raw=source.read_bytes()
sha=lambda data:hashlib.sha256(data).hexdigest()
source_hash=sha(raw);out=C/'Mermaid_Roshan_Book_V41_Email.pdf'
original=PdfReader(BytesIO(raw));doc=pdfium.PdfDocument(raw)
quality_by_hash={};decoded={};attempts=[];masks=0
# Oversampled full-world page retains native dimensions; a lower JPEG quality
# is eligible only if the same actual-page40dB gate passes. Other pages remain85.
for value in original.pages[2]['/Resources'].get('/XObject',{}).values():
 obj=value.get_object()
 if obj.get('/Subtype')=='/Image' and obj.get('/Width')==6144 and obj.get('/Height')==4389:quality_by_hash[sha(obj._data)]=25
def rgb_image(obj):
 return obj.get('/Subtype')=='/Image' and str(obj.get('/ColorSpace'))=='/DeviceRGB' and obj.get('/BitsPerComponent')==8
def decode(obj):
 key=sha(obj._data)
 if key in decoded:return decoded[key]
 w,h=int(obj['/Width']),int(obj['/Height']);dp=obj.get('/DecodeParms',{})
 if str(obj.get('/Filter'))=='/FlateDecode' and dp.get('/Predictor')==15 and dp.get('/Colors')==3 and dp.get('/Columns')==w:
  def chunk(tag,data):return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
  png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',obj._data)+chunk(b'IEND',b'')
  im=Image.open(BytesIO(png)).convert('RGB')
 else:im=Image.frombytes('RGB',(w,h),obj.get_data())
 decoded[key]=im;return im
reference=[np.asarray(doc[n].render(scale=1.5).to_pil().convert('RGB'),np.float32) for n in range(34)]
for iteration in range(8):
 writer=PdfWriter();writer.clone_document_from_reader(PdfReader(BytesIO(raw)));seen=set()
 for page in writer.pages:
  for value in page['/Resources'].get('/XObject',{}).values():
   obj=value.get_object()
   if id(obj) in seen:continue
   seen.add(id(obj))
   if not rgb_image(obj):continue
   key=sha(obj._data);quality=quality_by_hash.get(key,85);buf=BytesIO();decode(obj).save(buf,format='JPEG',quality=quality,subsampling=0,optimize=True)
   if len(buf.getvalue())>=len(obj._data):continue
   obj._data=buf.getvalue();obj[NameObject('/Filter')]=NameObject('/DCTDecode');obj.decoded_self=None
   if '/DecodeParms' in obj:del obj['/DecodeParms']
 with out.open('wb') as f:writer.write(f)
 email=PdfReader(out);edoc=pdfium.PdfDocument(str(out));checks=[];failed=[];masks=0
 assert len(email.pages)==len(original.pages)==34
 for n in range(34):
  x,y=original.pages[n],email.pages[n]
  assert x.get_contents().get_data()==y.get_contents().get_data() and x.extract_text()==y.extract_text() and x.mediabox==y.mediabox
  for key in x['/Resources'].get('/XObject',{}):
   u=x['/Resources']['/XObject'][key].get_object();v=y['/Resources']['/XObject'][key].get_object()
   if u.get('/Subtype')=='/Image':
    assert (u['/Width'],u['/Height'])==(v['/Width'],v['/Height'])
    if u.get('/SMask'):assert u['/SMask'].get_object()._data==v['/SMask'].get_object()._data;masks+=1
  current=np.asarray(edoc[n].render(scale=1.5).to_pil().convert('RGB'),np.float32);mse=float(np.mean((reference[n]-current)**2));psnr=float(10*np.log10(255**2/mse)) if mse else 100
  checks.append(dict(page=n,render_psnr_db=psnr,text_vector_content_trim_and_image_sizes_exact=True))
  if psnr<40:failed.append(n)
 edoc.close()
 attempts.append(dict(iteration=iteration+1,default_quality=85,bytes=out.stat().st_size,failed_pages=failed,minimum_psnr_db=min(q['render_psnr_db'] for q in checks),quality_overrides=dict(quality_by_hash)))
 print(json.dumps({k:v for k,v in attempts[-1].items() if k!='quality_overrides'}),flush=True)
 if not failed:break
 for n in failed:
  for value in original.pages[n]['/Resources'].get('/XObject',{}).values():
   obj=value.get_object()
   if rgb_image(obj):key=sha(obj._data);quality_by_hash[key]=min(95,quality_by_hash.get(key,85)+2)
else:raise RuntimeError('Email fidelity did not converge within8rounds')
assert out.stat().st_size<=25000000,('Email over25MB',out.stat().st_size)
assert sha(source.read_bytes())==source_hash
record=dict(status='PASS',source_sha256=source_hash,output_sha256=sha(out.read_bytes()),output_bytes=out.stat().st_size,attempts=attempts,pages=checks,alpha_mask_placements_byte_exact=masks,native_pixel_sizes_preserved=True,source_unchanged=True,minimum_render_psnr_db=min(q['render_psnr_db'] for q in checks),method='Adaptive JPEG4:4:4;85default,25for the oversampled6144x4389 arrival only, with2-step increases only for images on pages below40dB. No resizing; vector text/clips/geometry and lossless alpha unchanged. Original master lossless.',visual_review='Review candidate; owner/print acceptance open')
(C/'email_verification.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:v for k,v in record.items() if k not in ['pages','attempts']},indent=2))
