"""Preserve the exact lossless PDF in Git-sized parts; no PDF re-encoding."""
from pathlib import Path
import argparse,hashlib,json
V=Path(__file__).resolve().parent;C=V/'complete';D=C/'master_parts'
ap=argparse.ArgumentParser();ap.add_argument('--pack',action='store_true');ap.add_argument('--output',type=Path,default=C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf');a=ap.parse_args()
sha=lambda data:hashlib.sha256(data).hexdigest()
if a.pack:
 data=a.output.read_bytes();D.mkdir(exist_ok=True);parts=[]
 for n,start in enumerate(range(0,len(data),50*1024*1024),1):
  payload=data[start:start+50*1024*1024];p=D/f'Mermaid_Roshan_V40_Lossless.pdf.part{n:02}';p.write_bytes(payload);parts.append(dict(file=p.name,bytes=len(payload),sha256=sha(payload)))
 record=dict(method='Exact binary split solely for GitHub100MiB-per-file limit. Concatenation reconstructs byte-identical lossless PDF; no image compression, resizing or source edits.',master_bytes=len(data),master_sha256=sha(data),parts=parts)
 (D/'parts.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(record,indent=2))
else:
 record=json.loads((D/'parts.json').read_text('utf8'));chunks=[]
 for q in record['parts']:
  data=(D/q['file']).read_bytes();assert len(data)==q['bytes'] and sha(data)==q['sha256'];chunks.append(data)
 data=b''.join(chunks);assert len(data)==record['master_bytes'] and sha(data)==record['master_sha256']
 if a.output.exists():assert sha(a.output.read_bytes())==record['master_sha256'],'Existing output differs; choose another --output path'
 else:a.output.write_bytes(data)
 print('Byte-identical lossless master verified:',a.output)
