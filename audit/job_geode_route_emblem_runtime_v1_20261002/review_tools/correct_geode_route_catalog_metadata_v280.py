from pathlib import Path
import datetime,hashlib,json,re,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_route_emblem_runtime_v1_20261002';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
gate=read(f/'runtime_gate/contractv1.receipt.json');assert gate['status']=='FAIL_PRESERVED' and any('unused asset metadata:' in x for x in gate['blocking_diagnostics'])
p=b/'scripts/opera_hotspot_catalog.gd';s=p.read_text();old='\t"res://assets/opera/worlds/geology/painted_geode_v1_20261001/closed.png": {"dimensions": Vector2i(1024, 1024), "role": "object"},\n';assert s.count(old)==1;s=s.replace(old,'');old='\t\tor path == "res://assets/opera/worlds/geology/painted_geode_v1_20261001/closed.png" \\\n';assert s.count(old)==1;s=s.replace(old,'');p.write_text(s,encoding='utf-8',newline='\n')
p=f/'resource_contract.gd';assert not (f/'resource_contract_v1.gd').exists();shutil.copyfile(p,f/'resource_contract_v1.gd');s=p.read_text();old='\tassert(errors.is_empty(), str(errors))';assert old in s;s=s.replace(old,'\tif not errors.is_empty():\n\t\tprinterr("GEODE_RESOURCE_CONTRACT|FAIL|", str(errors))\n\t\tquit(1)\n\t\treturn');p.write_text(s,encoding='utf-8',newline='\n')
write(f/'CONTRACT_FAILURE_V1.json',dict(status='FAIL_PRESERVED_OBSOLETE_METADATA_CORRECTED_RETRY_PENDING',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),failure='Unchanged catalog validator rejects unused metadata for the previous closed source, because GEODE now references the current authored atlas.',repair='Remove only the unused old ASSET_META row and old exact allowlist path; keep original PNG/import/license and all recorded prior opinions. No validator tolerance or rule changed.',process_stop='Stopped only two verified owned Godot processes whose command line named this resource_contract.gd after the synchronous assert left the engine idle. Earlier stdout/stderr/process receipt and original fixture preserved. New review fixture explicitly exits1 for catalog errors.',gates_relaxed=False,creative_score_changed=False))
def funcs(s):
 lines=s.splitlines(keepends=True);out={}
 for i,line in enumerate(lines):
  m=re.match(r'^(?:static )?func (\w+)',line)
  if m:
   j=i+1
   while j<len(lines) and (not lines[j].strip() or lines[j].startswith(('\t',' '))):j+=1
   out[m.group(1)]=''.join(lines[i:j]).rstrip()
 return out
p=f/'MECHANIC_UNCHANGED.json';d=read(p);shutil.copyfile(p,f/'MECHANIC_UNCHANGED_V1.json')
for x in d['records']:
 a=funcs((f/'prior_source'/Path(x['path']).name).read_text());c=funcs((b/x['path']).read_text());changed=[n for n in a if a[n]!=c[n]];assert changed==(['_allowed_runtime_path'] if x['path'].endswith('opera_hotspot_catalog.gd') else []);x['after_sha256']=sha(b/x['path']);x['changed_functions']=changed
d['qualification']+=' Retired now-unused old source metadata and exact allowlist path; all existing resource/aspect/alpha-gutter checks remain literal unchanged.';write(p,d)
p=f/'PLAN.json';d=read(p);d['scope']+=' Remove now-unused old catalog metadata/exact allowlist path while preserving the artwork, as required by the unchanged existing validator.';d['catalog_failure_preserved']='CONTRACT_FAILURE_V1.json';write(p,d)
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name);ip=b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip);d['scope']+=' Same strict catalog found and removed now-unused previous source metadata/allowlist path; original art preserved, failed contractv1 retained, new review fixture exits1 on errors.';d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
print('Retired obsolete catalog metadata only; prior strict failure preserved, retry pending.',flush=True)
