from pathlib import Path
import json,hashlib,re,subprocess
from datetime import datetime,timezone
from PIL import Image
r=Path.cwd();s=r/'assets_src/imagegen/job_art_nursery_20261019';b=r/'assets_src/imagegen/job_art_boxer_20261019';v=s/'verification';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Every new image is licensed; final runtime rows replace earlier derivative hashes only.
p=r/'ASSET_LICENSES.md';t=p.read_text(encoding='utf-8');lines=t.splitlines();lookup={}
for i,line in enumerate(lines):
 m=re.match(r'^\| `([^`]+)` \|',line)
 if m:lookup.setdefault(m[1],[]).append(i)
records={x['path']:x for folder in [s,b] for x in json.loads((folder/'runtime_provenance.json').read_text())['records']}
for name,row in records.items():
 path=r/name;assert sha(path)==row['sha256'];line=f"| `{name}` | Painted P5 artwork; exact source/hash in adjacent job-art runtime_provenance.json | Source rights/OpenAI output terms retained; no protected-source substitution | https://openai.com/policies/terms-of-use/ | {row['modifications']} Final SHA256 {row['sha256']}; local AI static appearance candidate only, motion/device/child/owner acceptance separate. |"
 if name in lookup:
  assert len(lookup[name])==1,(name,lookup[name]);lines[lookup[name][0]]=line
 else:lookup[name]=[len(lines)];lines.append(line)
added=0
for folder in [s,b]:
 for path in sorted(folder.rglob('*.png')):
  name=path.relative_to(r).as_posix()
  if name in lookup:continue
  if '/review' in name or '/retired_' in name:
   source='Project artwork/current exact4.7.2 Mobile screenshot or labeled QA contact sheet; existing source rights retained';mods='Non-runtime diagnostic/review evidence, not generator appearance input or accepted delivery art. Technical crop/downsample/layout only where sheet; original screenshots retained.'
  elif '/recovered/' in name:
   source='Exact recovered project native; immutable cfcadc966bc2f3d9962243589d8a820c19ac2b0d and original source/license roles in source_inventory.json';mods='Native source bytes preserved; upstream attribution in source_license_rows.txt; owner older-Roshan exception is Nursery-only.'
  else:
   source='Available builtin ImageGen or recovered project native; source_inventory.json/prompts.json preserve exact origin, model revision unexposed';mods='Native/rejected source outside runtime, exact original alpha/RGB retained. Source/context/acceptance scope is explicit in adjacent records.'
  lines.append(f'| `{name}` | {source} | Project/source/OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | {mods} SHA256 {sha(path)}. |');lookup[name]=[len(lines)-1];added+=1
p.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('Licensed',added,'new evidence/native images; refreshed',len(records),'finalruntime rows')
# Complete trusted suite using only the already-controlled native-output transport.
original=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/assets_src/imagegen/artwork_quality_20261018/verification')
for old,new in [('windows_native_capture_05.py','windows_native_capture_01.py'),('run_ci_native_capture_05.sh','run_ci_native_capture_01.sh'),('run_full_ci_native_capture_05.py','run_full_ci_01.py')]:
 target=v/new;assert not target.exists()
 txt=(original/old).read_text(encoding='utf-8').replace('native_capture_05','native_capture_01')
 if old.endswith('.sh'):
  txt=txt.replace("cd '/c/Users/Peter/Documents/mermaid-roshan-reef'","cd '/c/Users/Peter/.codex/worktrees/art-ci-control-20261018/mermaid-roshan-reef'").replace('C:/Users/Peter/Documents/mermaid-roshan-reef/assets_src/imagegen/artwork_quality_20261018/verification/windows_native_capture_01.py',(v/'windows_native_capture_01.py').as_posix())
 if old.startswith('run_full'):
  txt=txt.replace('e31864fb904b0e1192b90a2b577516864497bb10','e90c0daa83cf05644f0e9942e85c1198ed7901f7').replace("'assets/mg/painted_quality_20261018'","'assets/opera/worlds/nursery_quality_20261019','assets/opera/worlds/boxer_quality_20261019','assets/opera/worlds/props','assets/ui'")
  anchor='pins = {p.relative_to(root).as_posix(): sha(p) for p in sources}';assert anchor in txt;txt=txt.replace(anchor,"for impact_name in ['job-art-teacher-20261018','job-art-astronaut-20261018']:\n    impact=json.loads((root/('design/audit_impacts/'+impact_name+'.json')).read_text())\n    sources += [root/p for p in impact['files'] if p.startswith('assets/') and p.endswith('.png') and (root/p).is_file()]\n"+anchor)
 target.write_text(txt,encoding='utf-8')
for n in ['full_ci_native_capture_01.log','native_capture_01_events.jsonl']:
 p=v/n;assert not p.exists();p.touch()
p=v/'full_ci_native_capture_01.json';assert not p.exists();p.write_text(json.dumps({'status':'PENDING','baseline':'e90c0daa83cf05644f0e9942e85c1198ed7901f7','scope':'CoherentP5Nursery/Boxer afterdev583; unchanged complete scripts/ci.sh82probes, original deadlines/classifiers/no retries. Exact4.7.2, freshprivatehomes controlled native output.'},indent=2)+'\n')
commands=[['python','-B','tools/audit_document_authority.py'],['python','-B','tools/audit_development.py','--base','auto']]
for i in range(len(commands)):(v/f'pre_full01_gate_{i}.log').touch()
p=r/'design/audit_impacts/job-art-nursery-20261019.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[x.relative_to(r).as_posix() for folder in [s,b] for x in folder.rglob('*') if x.is_file()]));d['validation'].append({'command':'Complete unchanged scripts/ci.sh local82after currentdev583 reconciliation, nativecapture01','result':'PENDING','evidence':'assets_src/imagegen/job_art_nursery_20261019/verification/full_ci_native_capture_01.json/log; no retry, originaldeadlines/classifiers/sourcepins.'});p.write_text(json.dumps(d,indent=2)+'\n')
for i,c in enumerate(commands):
 q=subprocess.run(c,capture_output=True,text=True,encoding='utf-8');(v/f'pre_full01_gate_{i}.log').write_text(q.stdout+q.stderr,encoding='utf-8');print(i,q.returncode,(q.stdout+q.stderr)[-2600:]);assert q.returncode==0
print('Full01prepared, machine suite must be launched only after latest GUIcapture exits/source freezes.')
