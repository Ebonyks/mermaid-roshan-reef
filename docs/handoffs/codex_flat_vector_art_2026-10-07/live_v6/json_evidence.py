"""Byte-exact sections for readable non-runtime JSON metadata; no acceptance claim."""
from pathlib import Path
import hashlib,json
SCHEMA='reef.literal_json_sections/1'
LIMIT=1024*1024

def sha(data):return hashlib.sha256(data).hexdigest()

def unique(data):
 def pairs(items):
  d={}
  for key,value in items:
   if key in d:raise ValueError('duplicate JSON key')
   d[key]=value
  return d
 return json.loads(data.decode('utf-8'),object_pairs_hook=pairs)

def read_json(path):
 path=Path(path);d=unique(path.read_bytes())
 if not isinstance(d,dict) or d.get('schema')!=SCHEMA:return d
 if not d['sections'] or len(d['sections'])>64:raise ValueError('invalid section count')
 chunks=[];names=set()
 for row in d['sections']:
  n=Path(row['path']);q=(path.parent/n).resolve()
  if n.is_absolute() or '..' in n.parts or row['path'] in names or not q.is_relative_to(path.parent.resolve()):raise ValueError('unsafe/duplicate section')
  names.add(row['path']);b=q.read_bytes()
  if not b or len(b)>LIMIT or len(b)!=row['bytes'] or sha(b)!=row['sha256']:raise ValueError('section identity failed')
  b.decode('utf-8');chunks.append(b)
 b=b''.join(chunks)
 if len(b)>64*LIMIT or len(b)!=d['original_bytes'] or sha(b)!=d['original_sha256']:raise ValueError('original identity failed')
 out=unique(b)
 if isinstance(out,dict) and out.get('schema')==SCHEMA:raise ValueError('nested index forbidden')
 return out

def shard_json(path,origin):
 path=Path(path);b=path.read_bytes();before=unique(b);target=path.with_name(path.stem+'.literal');target.mkdir(exist_ok=False)
 chunks=[];current=bytearray()
 for line in b.splitlines(keepends=True):
  if len(line)>LIMIT:raise ValueError('oversized line')
  if current and len(current)+len(line)>LIMIT:chunks.append(bytes(current));current.clear()
  current.extend(line)
 if current:chunks.append(bytes(current))
 rows=[]
 for i,chunk in enumerate(chunks):
  f=target/f'section_{i:03d}.json.txt';f.write_bytes(chunk);rows.append({'path':f.relative_to(path.parent).as_posix(),'bytes':len(chunk),'sha256':sha(chunk),'role':'literal unencoded UTF8 JSON section;join in order to recover every original byte'})
 d={'schema':SCHEMA,'original_reference':origin,'original_bytes':len(b),'original_sha256':sha(b),'sections':rows,'claim':'Storage representation only;unchanged scanner/gates;no artistic/runtime acceptance'}
 path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 if read_json(path)!=before:raise ValueError('metadata facts changed')
 return d
