from pathlib import Path
import datetime,json,shutil
r=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp');b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_route_emblem_runtime_v1_20261002'
assert f.exists() and not (f/'PLAN.json').exists() and not (b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json').exists()
original=(r/'prepare_geode_route_binding_v275.py').read_text();start=original.index('def funcs(s):');end=original.index('\nproof=[]',start)
fixed='''def funcs(s):
 lines=s.splitlines(keepends=True);out={}
 for i,line in enumerate(lines):
  m=re.match(r'^(?:static )?func (\\w+)',line)
  if not m:continue
  j=i+1
  while j<len(lines) and (not lines[j].strip() or lines[j].startswith(('\\t',' '))):j+=1
  out[m.group(1)]=''.join(lines[i:j]).rstrip()
 return out
'''
prefix='''from pathlib import Path
import datetime,hashlib,json,re,shutil,subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_route_emblem_runtime_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\\n',encoding='utf-8',newline='\\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
remote=read(b/'tmp/geology_checkpoint_k_remote_v259/RESULT.json');assert remote['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES'
baseline=subprocess.check_output(['git','rev-parse','HEAD'],cwd=b,text=True).strip();assert baseline==remote['revision']
names=['scripts/castle_career_routes.gd','scripts/opera_career_world_2d.gd','scripts/opera_hotspot_catalog.gd'];before={rel:dict(path=rel,sha256=sha(f/'prior_source'/Path(rel).name),bytes=(f/'prior_source'/Path(rel).name).stat().st_size) for rel in names}
source='assets/opera/worlds/geology/coherent_geode_v1_20261002/opening_six_states.png';assert sha(b/source)=='e47a731414210ef70c0b5fffce2828922a15611c6093c244811ee0a283534503'
open_region=[1392.270574971815,556.446448703495,617.632468996618,393.668545659527];closed_region=[96.974069898534,68.112739571590,473.325817361894,421.375422773393];height=142*closed_region[3]/closed_region[2]
reuse=b/'assets_src/reuse/geology_geode_emblems_v1_20261002';resource=b/'assets/opera/worlds/geology/coherent_geode_v1_20261002/open_geode.tres';assert resource.read_bytes()==(reuse/'open_geode_unbound.tres').read_bytes()
'''
target=r/'finish_geode_route_binding_v277.py';assert not target.exists();s=prefix+fixed+original[end:];target.write_text(s,encoding='utf-8',newline='\n');compile(s,str(target),'exec')
shutil.copyfile(r/'prepare_geode_route_binding_v275.py',f/'review_tools/prepare_geode_route_binding_v275.py');shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
(f/'PREPARATION_FAILURE_V275.json').write_text(json.dumps(dict(status='PRESERVED_MECHANICAL_PROOF_BOUNDARY_ERROR',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reason='Initial proof grouped each function until the next func, including intervening top-level constants. The requested GOAL_PROPS constant change was misattributed to ballet_voice_hold_seconds. Diff confirms only intended bindings/catalog metadata/allowlist. Resume extracts actual indented function bodies and completes impact/plan before any gates; no shipping function repaired to satisfy the proof.',production_changes_already_applied=['Only three planned bindings/catalog metadata/allowlist and exact open AtlasTexture metadata copy'],gate_or_game_failure=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared resume after proof boundary error; original source snapshots and failed helper retained.',flush=True)
