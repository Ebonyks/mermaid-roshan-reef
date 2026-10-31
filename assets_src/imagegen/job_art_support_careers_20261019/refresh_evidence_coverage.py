from pathlib import Path
import json,hashlib,re
r=Path(__file__).resolve().parents[3];s=Path(__file__).resolve().parent
p=r/'ASSET_LICENSES.md';t=p.read_text(encoding='utf-8');listed={m[1] for m in re.finditer(r'^\| `([^`]+)` \|',t,re.M)};added=0
for p in sorted(s.rglob('*.png')):
 n=p.relative_to(r).as_posix()
 if n in listed:continue
 t+='\n| `'+n+'` | Exact source-bound project capture/reference or labeled technical sheet; original roles retained in adjacent manifests | Project/reference/OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | Non-runtime evidence; no pixel/owner acceptance. SHA256 '+hashlib.sha256(p.read_bytes()).hexdigest()+'. |';added+=1
(r/'ASSET_LICENSES.md').write_text(t+'\n' if added else t,encoding='utf-8')
p=r/'design/audit_impacts/job-art-support-careers-20261019.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[x.relative_to(r).as_posix() for x in s.rglob('*') if x.is_file()]+[x.relative_to(r).as_posix() for x in (r/'assets/opera/worlds/support_quality_20261019').glob('*') if x.is_file()]));p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print('coverage',len(d['files']),'licensed',added)
