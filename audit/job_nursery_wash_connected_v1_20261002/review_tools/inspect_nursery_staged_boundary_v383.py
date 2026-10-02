from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_nursery_wash_connected_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
target=F/'review_tools'/Path(__file__).name;out=F/'SEAL_SOURCE_INSPECTION_V383.json'
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip);imp['files']=sorted(set(imp['files'])|{target.relative_to(R).as_posix(),out.relative_to(R).as_posix()});write(ip,imp);shutil.copyfile(Path(__file__),target)
ci=read(F/'full_ci_v1/RECEIPT.json');rows=[]
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for r in ci['source_checks']:
 path=r['path'];proc.stdin.write((':'+path+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().split()
 if len(header)==2 and header[1]==b'missing':rows.append({'path':path,'status':'ABSENT_FROM_GIT_INDEX','local_sha256':r['before_sha256']});continue
 assert header[1]==b'blob';n=int(header[2]);raw=proc.stdout.read(n);assert len(raw)==n and proc.stdout.read(1)==b'\n'
 local=(R/path).read_bytes();text=Path(path).suffix.lower() in {'.gd','.godot','.import','.json','.tres','.tscn','.sh','.py','.uid','.cfg'}
 normalize=lambda d:d.replace(b'\r\n',b'\n') if text else d
 if normalize(raw)!=normalize(local):rows.append({'path':path,'status':'MATERIAL_INDEX_MISMATCH','local_sha256':r['before_sha256'],'index_sha256':hashlib.sha256(raw).hexdigest()})
proc.stdin.close();assert proc.wait(timeout=30)==0
write(out,{'status':'EXACT_SOURCE_SEAL_FAILED_PENDING_RECONCILIATION','failed_helper':'review_tools/seal_connected_nursery_checkpoint_o_v382.py','failure':'git show of a rendered-source Nursery sheet import file absent from the Git index. No commit/push occurred. Full local CI evidence and original 783 hashes remain unchanged.','source_count':783,'source_local_hashes_unchanged':all(hashlib.sha256((R/r['path']).read_bytes()).hexdigest()==r['before_sha256'] for r in ci['source_checks']),'index_gaps':rows,'protected_originals_modified':False,'qualification':'Diagnostic only. Do not omit missing members, stage unrelated changes, or claim the exact source seal passed.'})
print('STAGED_SOURCE_INSPECTION|'+str(len(rows))+' gaps')
for row in rows:print(row['status'],row['path'])
