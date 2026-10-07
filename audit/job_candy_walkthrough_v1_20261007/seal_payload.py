"""Seal all review payload files, preserve transport receipt separately, stage only owned work."""
from pathlib import Path
import hashlib,json,subprocess
p=Path(__file__).resolve().parent
r=p.parents[1]
impact=r/'design/audit_impacts/candymaker-visual-walkthrough-20261007.json'
d=json.loads(impact.read_text(encoding='utf-8'))
d['files']=sorted(x.relative_to(r).as_posix() for x in p.rglob('*') if x.is_file() and not x.name.startswith('preview-'))+['ASSET_LICENSES.md','design/05_DOC_LEDGER.md']
impact.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=json.loads((p/'MANIFEST.json').read_text(encoding='utf-8'))
files=[]
for f in sorted(p.rglob('*')):
    if not f.is_file() or f.name in ['MANIFEST.json','REMOTE_VERIFICATION.json'] or f.name.startswith('preview-'):continue
    raw=f.read_bytes()
    files.append(dict(path=f.relative_to(p).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
seal=''.join(f['path']+'\t'+str(f['bytes'])+'\t'+f['sha256']+'\n' for f in files).encode()
m['payload_files']=files
m['payload_sha256']=hashlib.sha256(seal).hexdigest()
(p/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
subprocess.run(['git','add','-f','--']+d['files']+[impact.relative_to(r).as_posix()],cwd=r,check=True)
for f in files:
    raw=subprocess.check_output(['git','show',':'+p.relative_to(r).as_posix()+'/'+f['path']],cwd=r)
    assert hashlib.sha256(raw).hexdigest()==f['sha256'],f['path']
assert sum(f['bytes'] for f in files)<128*1024*1024
print(json.dumps(dict(payload_files=len(files),payload_bytes=sum(f['bytes'] for f in files),payload_sha256=m['payload_sha256'],staged_raw_bytes_match=True)))
