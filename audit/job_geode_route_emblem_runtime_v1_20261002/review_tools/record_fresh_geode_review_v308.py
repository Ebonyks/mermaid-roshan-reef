from pathlib import Path
import hashlib, json, re, shutil, subprocess, sys

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=b/'audit/job_geode_route_emblem_runtime_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
prior=f/'prior_binding_attempt_01'
for n in ['index.html','BOARD_MANIFEST_1280.json','BOARD_MANIFEST_1600.json','STILL_BOARD_MANIFEST.json']:
 if not (prior/n).exists():shutil.copyfile(f/n,prior/n)
assert (prior/'REVIEW.json').is_file()
s=(f/'review_tools/record_geode_route_review_v286.py').read_text(encoding='utf-8')
replacements={
 "assert len(snapshot['source_files'])==372":"assert len(snapshot['source_files'])==373",
 "assert not (f/'REVIEW.json').exists()":"assert (f/'prior_binding_attempt_01/REVIEW.json').is_file()",
 'attempt_01/':'attempt_02/',
 '[(1280,163,111,142),(1600,153,107,132)]':'[(1280,162,110,141),(1600,155,108,134)]',
 'geode_1280_0111.webp':'geode_1280_0110.webp',
 'geode_1600_0107.webp':'geode_1600_0108.webp',
 'runtime_gate/capture{w}v1.receipt.json':'runtime_gate/capture{w}v2.receipt.json',
 'BOARD_MANIFEST_{w}.json':'BOARD_MANIFEST_V2_{w}.json',
 'STILL_BOARD_MANIFEST.json':'STILL_BOARD_MANIFEST_V2.json',
 'consecutive_frames=316':'consecutive_frames=317',
 '316 consecutive':'317 consecutive',
 'stills/316':'stills/317',
 '372 frozen':'373 frozen',
 'on372':'on373',
 'fresh372':'fresh373',
 'pending372':'pending373',
 '372 source hashes':'373 source hashes',
 'full_ci_v1/RECEIPT.json':'full_ci_v2/RECEIPT.json',
 'The broad aqua/lavender support':'The cream top and lavender side planes of the painted support',
 'All 24 Castle route functions':'All 24 Castle route functions',
}
original=s
for old,new in replacements.items():
 assert old in original,old
 s=s.replace(old,new)
# Backups retain attempt 01; only current capture references are attempt 02.
s=s.replace("assert (f/'prior_binding_attempt_02/REVIEW.json').is_file()","assert (f/'prior_binding_attempt_01/REVIEW.json').is_file()")
s=s.replace("s+='\\n| `'+prefix", "s='\\n'.join(x for x in s.split('\\n') if not x.startswith('| `'+prefix+'/index.html`'))\ns+='\\n| `'+prefix")
s=s.replace('No interpolated, duplicated or repaired frames were substituted.', 'These are actual recorded frames, including unchanged held gameplay states. No interpolated, synthesized or repaired frames were substituted.')
s=s.replace('No missing motion is filled by duplicated images.', 'Repeated held states are actual captured game states; no missing motion is filled by synthesized images.')
s=s.replace('<a href="full_ci_v2/RECEIPT.json">Full current suite receipt</a>', '<a href="full_ci_v2/RECEIPT.json">Full current suite receipt</a> · <a href="full_ci_v1/RECEIPT.json">Preserved failed first suite: 81 of 82 probes passed</a>')
target=Path(__file__).with_name('record_geode_route_review_v309.py')
target.write_text(s,encoding='utf-8',newline='\n')
q=subprocess.run([sys.executable,'-X','utf8','-B',str(target)],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
print(q.stdout.decode('utf-8',errors='replace'));print(q.stderr.decode('utf-8',errors='replace'));assert q.returncode==0
# Intrinsic dimensions prevent deferred-image layout jumps. Read-only image inspection.
from PIL import Image
p=f/'index.html';s=p.read_text(encoding='utf-8')
def dims(m):
 with Image.open((f/m.group(1)).resolve()) as im:w,h=im.size
 return m.group(0)+f' width="{w}" height="{h}"'
s=re.sub(r'<img loading="lazy" src="([^"]+)"',dims,s)
p.write_text(s,encoding='utf-8',newline='\n')
plan=read(f/'PLAN.json')
plan['scope']=plan['scope'].replace('one new open AtlasTexture metadata resource','two new open AtlasTexture metadata resources sharing the same cached atlas')
plan['current_capture_attempt']='attempt_02';plan['full_ci_current_attempt']='full_ci_v2/RECEIPT.json'
write(f/'PLAN.json',plan)
d=read(f/'MECHANIC_UNCHANGED.json')
for x in d['records']:x['after_sha256']=sha(b/x['path'])
write(f/'MECHANIC_UNCHANGED.json',d)
d=read(b/'audit/job_artwork_refinement_live/ALL_ITEMS.json')
for x in d['items']:
 if x['id'].startswith('GEO-USE-'):
  if x['id']=='GEO-USE-DEV-MENU':
   x['unchanged_caller']='scripts/opera_job_playtest_menu.gd'
   x['current_binding']='scripts/castle_career_routes.gd'
  x['binding_sha256']=sha(b/x['current_binding'])
  x['current_capture_review']='audit/job_geode_route_emblem_runtime_v1_20261002/REVIEW.json'
write(b/'audit/job_artwork_refinement_live/ALL_ITEMS.json',d)
p=b/'audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v31.py'
s=p.read_text(encoding='utf-8').replace('the372-file geode capture boundary','the recorded geode capture source boundary')
p.write_text(s,encoding='utf-8',newline='\n')
q=subprocess.run([sys.executable,'-X','utf8','-B',str(p)],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
print(q.stdout.decode('utf-8',errors='replace'));assert q.returncode==0
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip)
d['files']=sorted(set(d['files'])|{x.relative_to(b).as_posix() for x in f.rglob('*') if x.is_file()})
write(ip,d)
print('Fresh complete visual review recorded: 317 real frames, 58 stills, 37 boards, 8 native details; 373 source hashes match.')
