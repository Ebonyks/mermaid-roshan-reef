"""Re-encode PDF image streams with PNG prediction; identical decoded pixels."""
from pathlib import Path
from io import BytesIO
import argparse, hashlib, json, struct
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject, DictionaryObject, ArrayObject
ap=argparse.ArgumentParser();ap.add_argument('pdf',type=Path);a=ap.parse_args()
raw=a.pdf.read_bytes();r=PdfReader(BytesIO(raw));w=PdfWriter();w.clone_document_from_reader(r)
seen=set();evidence=[]
def image(obj):
 ident=id(obj)
 if ident in seen:return
 seen.add(ident)
 if obj.get('/SMask'):image(obj['/SMask'].get_object())
 cs=str(obj.get('/ColorSpace'));colors={'/DeviceRGB':3,'/DeviceGray':1}.get(cs)
 if not colors or obj.get('/BitsPerComponent')!=8:return
 width,height=int(obj['/Width']),int(obj['/Height']);data=obj.get_data()
 if len(data)!=width*height*colors:return
 out=BytesIO();Image.frombytes('RGB' if colors==3 else 'L',(width,height),data).save(out,format='PNG',compress_level=6)
 png=out.getvalue();pos=8;streams=[]
 while pos<len(png):
  size=struct.unpack('>I',png[pos:pos+4])[0];tag=png[pos+4:pos+8]
  if tag==b'IDAT':streams.append(png[pos+8:pos+8+size])
  pos+=size+12
 encoded=b''.join(streams)
 if len(encoded)>=len(obj._data):return
 before=hashlib.sha256(data).hexdigest();old=len(obj._data)
 obj._data=encoded;obj[NameObject('/Filter')]=NameObject('/FlateDecode')
 obj[NameObject('/DecodeParms')]=DictionaryObject({NameObject('/Predictor'):NumberObject(15),NameObject('/Colors'):NumberObject(colors),NameObject('/BitsPerComponent'):NumberObject(8),NameObject('/Columns'):NumberObject(width)})
 obj.decoded_self=None
 assert hashlib.sha256(obj.get_data()).hexdigest()==before
 evidence.append(dict(width=width,height=height,colors=colors,decoded_sha256=before,before_bytes=old,after_bytes=len(encoded)))
for page in w.pages:
 for value in page.get('/Resources',{}).get('/XObject',{}).values():
  obj=value.get_object()
  if obj.get('/Subtype')=='/Image':image(obj)
temp=a.pdf.with_suffix('.optimized.pdf')
with temp.open('wb') as f:w.write(f)
temp.replace(a.pdf)
record=dict(operation='Lossless PNG-predictor encoding of PDF image streams; no source image files changed.',before_bytes=len(raw),after_bytes=a.pdf.stat().st_size,images_optimized=len(evidence),decoded_pixels_verified=True,streams=evidence)
(a.pdf.parent/'lossless_pdf_encoding.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:v for k,v in record.items() if k!='streams'}))
