from pathlib import Path
import datetime,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_coherent_runtime_v1_20261002'
write=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
source=b/'tmp/seal_geology_checkpoint_k_v258.py';target=b/'tmp/seal_geology_checkpoint_k_v274.py';assert not target.exists()
s=source.read_text(encoding='utf-8').replace('geology_checkpoint_k_seal_v258','geology_checkpoint_k_seal_v274')
s=s.replace('rejected mount4.3 and interrupted suite preserved.','rejected mount4.3, interrupted suite1 and failed suite2 passive127 preserved separately. Unbound same-source closed142px/open50px reuse4.5 provisional and larger open sizes4.6, all ten isolated presentations directly reviewed; new grotto1254-square fails required2048-square native coverage and stays reference-only. Shared training has three source and eleven component opinions with literal caller trace.')
target.write_text(s,encoding='utf-8',newline='\n');compile(s,str(target),'exec')
write(f/'CHECKPOINT_SEAL_PREPARATION_FAILURE_V258.json',dict(status='PRESERVED_PREPARATION_TIMING_FAILURE_NO_STAGING',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),action='seal_geology_checkpoint_k_v258.py',reason='Sealer started while prior preparation still ran its 2D gate; 2dv1.receipt.json did not exist yet. It stopped before copy, staging or map construction. Empty staging-output directory preserved; retry uses distinct v274 output only after prep exits0.',production_changed=False,index_changed=False))
shutil.copyfile(source,f/'review_tools'/source.name);shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-coherent-runtime-20261002.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
print('Prepared distinct seal retry; previous preparation timing failure retained, no product changes.',flush=True)
