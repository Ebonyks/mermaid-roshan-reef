"""Verify review parity, provenance, links and truthful coverage; no engine run."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
import json, hashlib, struct, time, traceback

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((OUT/n).read_text(encoding='utf-8'))

class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='img':self.images.append(a.get('src'))
  for k in ['src','href']:
   if k in a:self.links.append(a[k])

def main():
 started=time.monotonic();checks=[];errors=[]
 def check(label,ok):
  checks.append({'label':label,'pass':bool(ok)})
  if not ok:errors.append(label)
 try:
  m=read('MANIFEST.json');s=read('STEPS.json');plan=read('WALKTHROUGH_PLAN.json');bindings=read('SOURCE_BINDINGS.json')
  check('numbered steps contiguous', [x['number'] for x in s['steps']]==list(range(1,m['steps']+1)))
  check('claim stays diagnostic', m['claim']=='ILLUSTRATED_DIAGNOSTIC_REVIEW_ONLY' and bindings['dirty_candidate'] and 'FAIL' in bindings['capture_failure'])
  payload=''.join(f['path']+'\0'+f['sha256']+'\n' for f in m['files']).encode()
  check('sorted payload hash',hashlib.sha256(payload).hexdigest()==m['sorted_payload_sha256'])
  for f in m['files']:
   p=OUT/f['path'];check('payload '+f['path'],p.is_file() and p.stat().st_size==f['bytes'] and sha(p)==f['sha256'])
  for f in m['frames']:
   p=OUT/f['path'];original=ROOT/f['original_path'];data=p.read_bytes()
   check('literal native '+f['path'],sha(p)==sha(original)==f['sha256'] and f['pixel_modifications'].startswith('NONE'))
   check('native dimensions '+f['path'],data[:8]==b'\x89PNG\r\n\x1a\n' and list(struct.unpack('>II',data[16:24]))==f['dimensions'])
   original_manifest=read(f['original_manifest'])
   row=next((x for x in original_manifest['frames'] if x['path']==f['original_path']),None)
   check('original metadata '+f['path'],row==f['native_state'])
  for p,h in bindings['captured_source_sha256'].items():
   check('exact source remains '+p,sha(ROOT/p)==h)
   snapshot=OUT/'sources'/(Path(p).name+'.txt')
   check('literal source snapshot '+p,sha(snapshot)==h)
  parser=Links();parser.feed((OUT/'index.html').read_text(encoding='utf-8'))
  check('all illustrated image references match step data',parser.images==['frames/1280/'+n for st in s['steps'] for n in st['images']])
  for link in parser.links:
   if link.startswith('#'):check('anchor '+link,link[1:] in parser.ids)
   elif not link.startswith(('https:','http:','data:')):check('local link '+link,(OUT/link).is_file())
  check('all native masters retained',len(m['frames'])==m['native_master_count']==35)
  check('separate overlays and toggle present','class="overlay"' in (OUT/'index.html').read_text(encoding='utf-8') and 'hide-marks' in (OUT/'index.html').read_text(encoding='utf-8'))
  check('gap panels explicit',sum(bool(x['gap']) for x in s['steps'])==7)
  check('publication remains unclaimed',read('PUBLICATION_STATUS.json')['remote_revision'] is None and read('PUBLICATION_STATUS.json')['status'].startswith('NOT_DELIVERED'))
  bytes_total=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())
  check('review output below declared64MiB',bytes_total<=64*1024*1024)
  check('nonruntime import exclusion',(OUT/'.gdignore').is_file())
 except Exception:
  errors.append(traceback.format_exc())
 result='PASS' if not errors else 'FAIL'
 text='\n'.join(('PASS' if c['pass'] else 'FAIL')+' | '+c['label'] for c in checks)+'\n'+ '\n'.join(errors)+'\nRESULT | '+result+'\n'
 log=OUT/'VERIFY_V2_LOG.txt';log.write_text(text,encoding='utf-8')
 receipt={'result':result,'checked_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':round(time.monotonic()-started,3),'checks':len(checks),'failures':len(errors),'errors':errors,'manifest_sha256':sha(OUT/'MANIFEST.json'),'log_sha256':sha(log),'claim':'Artifact byte/provenance/reference verification only; no runtime/motion/audio/visual4.6/device/child/owner or publication acceptance','native_launches':0,'source_changes':0,'pixel_edits':0}
 (OUT/'VERIFY_V2_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(receipt));return 0 if result=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
