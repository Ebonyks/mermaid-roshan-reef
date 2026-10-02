from pathlib import Path
import datetime,hashlib,json,re,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_nursery_wash_connected_v1_20261002';A=F/'source_boundary_generated_uids'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ins=read(F/'SEAL_SOURCE_INSPECTION_V383.json');assert len(ins['index_gaps'])==253 and all(r['status']=='ABSENT_FROM_GIT_INDEX' for r in ins['index_gaps'])
uids=[r for r in ins['index_gaps'] if r['path'].endswith('.gd.uid')]
imports=[r for r in ins['index_gaps'] if r['path'].endswith('.png.import')]
assert len(uids)==240 and len(imports)==13 and all(r['path'].startswith('assets/opera/worlds/') and 'nursery' in r['path'] for r in imports)
ignored=subprocess.run(['git','check-ignore','--stdin'],cwd=R,input='\n'.join(r['path'] for r in uids+imports).encode(),capture_output=True,check=True).stdout.decode().splitlines();assert set(ignored)=={r['path'] for r in uids+imports}
assert not A.exists()
target=F/'review_tools'/Path(__file__).name;index=F/'PUBLICATION_AUXILIARY_UID_INDEX_V384.json'
planned=[target,index]+[A/(r['path']+'.txt') for r in uids]
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip)
imp['scope']+=' The exact publication seal found thirteen context-required generated Nursery texture import files and 240 generated script UID sidecars absent from the Git index, with no material mismatch in any indexed source. Record only those thirteen Nursery import files as reproducible rendering dependencies; preserve all 240 ignored script UID bytes at non-runtime QA snapshot paths. Every one of the original 783 local CI members remains covered: 543 exact revision source/import members and 240 auxiliary generated UID snapshots. Never promote generated UID snapshots into runtime scripts, omit frozen members or stage unrelated import changes. Preserve the failed first seal and its complete inspection.'
imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in planned}|{r['path'] for r in imports});write(ip,imp);shutil.copyfile(Path(__file__),target)
rows=[]
for r in uids:
 src=R/r['path'];raw=src.read_bytes();assert sha(raw)==r['local_sha256'] and re.fullmatch(rb'uid://[a-z0-9]+\r?\n?',raw)
 dst=A/(r['path']+'.txt');dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
 rows.append({'original_local_path':r['path'],'published_snapshot_path':dst.relative_to(R).as_posix(),'sha256':sha(raw),'bytes':len(raw),'role':'generated_local_script_uid_metadata_only','runtime_integration':False,'pixels':False})
for r in imports:
 raw=(R/r['path']).read_bytes();assert sha(raw)==r['local_sha256'] and b'importer="texture"' in raw and b'CompressedTexture2D' in raw
write(index,{'status':'ALL240_GENERATED_UID_SIDECARS_PRESERVED','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'failed_seal_inspection':'SEAL_SOURCE_INSPECTION_V383.json','original_local_ci_members':783,'revision_source_members':543,'auxiliary_generated_uid_members':240,'new_named_nursery_import_dependencies':imports,'uids':rows,'qualification':'All 783 frozen local CI files retain literal before/after checks. The 240 ignored generated .gd.uid files are non-runtime metadata evidence stored at separate snapshot paths, not script or art changes. Thirteen exact Nursery texture import settings become named rendering dependencies. Publication bridge must verify 543 source/import files against their exact revision blobs and all 240 UID snapshots against their preserved literal bytes; it must not say every local auxiliary filename exists at its runtime path in Git.'})
sentence=' The publication boundary distinguishes 543 exact revision source/import files from 240 preserved generated local script UID snapshots; all 783 original local CI members remain verified and accounted for.'
p=F/'index.html';t=p.read_text(encoding='utf-8');needle='All 53 raw engine diagnostics are preserved and qualified.';assert t.count(needle)==1;t=t.replace(needle,needle+sentence,1);p.write_text(t,encoding='utf-8',newline='\n')
imp=read(ip);imp['validation'].append({'command':'Exact first publication-source seal v382','result':'FAIL','evidence':(F/'SEAL_SOURCE_INSPECTION_V383.json').relative_to(R).as_posix()});imp['validation'].append({'command':'Preserve all generated UID sidecars and named Nursery import dependencies','result':'PASS','evidence':index.relative_to(R).as_posix()});write(ip,imp)
print('PUBLICATION_BOUNDARY|543 revision members|240 exact generated UID snapshots|13 named Nursery imports|783 frozen local files unchanged')
