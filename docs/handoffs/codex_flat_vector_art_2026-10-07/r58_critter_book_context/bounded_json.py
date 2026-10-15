"""Bounded nonruntime audit JSON with exact logical-byte/SHA verification; no model waiver."""
from pathlib import Path
import json,hashlib
INDEX_SCHEMA='reef.bounded_audit_json_index/1';PART_SCHEMA='reef.bounded_audit_json_text_part/1';MAX_PLAIN_BYTES=3750000;FRAGMENT_BYTES=1000000
ALLOWED_LOGICAL_SCHEMAS={'reef.runtime_path_json_inventory/1','reef.current_source_inventory/1','reef.resource_caller_graph/1','reef.flat_vector_delta_receipt/1','reef.flat_vector_delta_manifest/1'}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def unique(pairs):
 result={}
 for key,value in pairs:
  if key in result:raise ValueError('duplicate JSON key: '+key)
  result[key]=value
 return result
def parse(raw):return json.loads(raw.decode('utf-8'),object_pairs_hook=unique)
def logical_bytes(path):
 path=Path(path);raw=path.read_bytes();d=parse(raw)
 if not isinstance(d,dict) or d.get('schema')!=INDEX_SCHEMA:return raw
 if d.get('logical_schema') not in ALLOWED_LOGICAL_SCHEMAS or not 0<d.get('logical_bytes',0)<=128000000:raise ValueError('invalid logical audit schema/size')
 if d['fragment_count']!=len(d['fragments']) or len({x['path'] for x in d['fragments']})!=d['fragment_count']:raise ValueError('invalid fragment count/duplicates')
 chunks=[]
 for number,x in enumerate(d['fragments'],1):
  if Path(x['path']).name!=x['path'] or '/' in x['path'] or '\\' in x['path'] or ':' in x['path']:raise ValueError('fragment path escape')
  fragment=path.parent/x['path']
  if fragment.resolve().parent!=path.resolve().parent:raise ValueError('fragment parent escape')
  b=fragment.read_bytes()
  if len(b)!=x['bytes'] or sha(b)!=x['sha256'] or len(b)>=4*1024*1024:raise ValueError('fragment bytes/hash/scan cap mismatch')
  part=parse(b)
  if part.get('schema')!=PART_SCHEMA or part.get('part')!=number or part.get('logical_sha256')!=d['logical_sha256'] or not isinstance(part.get('utf8_text'),str):raise ValueError('fragment identity mismatch')
  text=part['utf8_text'].encode('utf-8')
  if len(text)!=x['text_bytes'] or sha(text)!=x['text_sha256']:raise ValueError('fragment text mismatch')
  chunks.append(text)
 result=b''.join(chunks)
 if len(result)!=d['logical_bytes'] or sha(result)!=d['logical_sha256']:raise ValueError('logical payload mismatch')
 document=parse(result)
 if not isinstance(document,dict) or document.get('schema')!=d['logical_schema']:raise ValueError('logical schema mismatch')
 return result
def read_document(path):return parse(logical_bytes(path))
def write_exact(path,raw,original_immutable=None):
 path=Path(path);d=parse(raw)
 if len(raw)<=MAX_PLAIN_BYTES:path.write_bytes(raw);return [path]
 if not isinstance(d,dict) or d.get('schema') not in ALLOWED_LOGICAL_SCHEMAS:raise ValueError('only declared nonruntime audit documents can be segmented')
 digest=sha(raw);rows=[];files=[];pos=0
 while pos<len(raw):
  end=min(pos+FRAGMENT_BYTES,len(raw))
  while True:
   try:fragment=raw[pos:end].decode('utf-8');break
   except UnicodeDecodeError:end-=1
  number=len(rows)+1;name=path.stem+'.fragment'+str(number).zfill(4)+'.json';part={'schema':PART_SCHEMA,'logical_schema':d['schema'],'logical_sha256':digest,'part':number,'utf8_text':fragment};b=(json.dumps(part,indent=2,ensure_ascii=False)+'\n').encode();assert len(b)<4*1024*1024
  target=path.parent/name;target.write_bytes(b);files.append(target);text=fragment.encode('utf-8');rows.append({'path':name,'bytes':len(b),'sha256':sha(b),'text_bytes':len(text),'text_sha256':sha(text)});pos=end
 index={'schema':INDEX_SCHEMA,'logical_schema':d['schema'],'logical_bytes':len(raw),'logical_sha256':digest,'fragment_count':len(rows),'fragments':rows,'scope':'Nonruntime source-audit text evidence;everypart scanned/hashed. LogicalJSON bytes preserved;no runtime/model/creative acceptance orauditor waiver.'}
 if original_immutable is not None:index['original_immutable']=original_immutable
 path.write_bytes((json.dumps(index,indent=2)+'\n').encode());files.insert(0,path);assert logical_bytes(path)==raw;return files
def write_document(path,data):return write_exact(path,(json.dumps(data,indent=2)+'\n').encode())
