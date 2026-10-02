from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=b/'tmp/geology_checkpoint_j_resume_v243';out.mkdir(exist_ok=False)
base='40b1c7bfe025f284507c586fea61b9dd76b61423';mp='audit/job_review_v2_20261001/GEOLOGY_RIVER_GEODE_REVIEW_SUPPLEMENT_FILES_V8.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args,input=None):
 q=subprocess.run(['git',*args],cwd=b,input=input,capture_output=True)
 (out/'git.stderr.log').open('ab').write(q.stderr)
 assert q.returncode==0,q.stderr.decode(errors='replace')[-2000:]
 return q.stdout
assert git('rev-parse','HEAD').decode().strip()==base
old=read(b/mp);paths={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p};assert paths==set(old['files'])|{mp}
def blobs(paths):
 ordered=sorted(paths);data=git('cat-file','--batch',input=''.join(':'+p+'\n' for p in ordered).encode());off=0;result={}
 for p in ordered:
  end=data.index(b'\n',off);head=data[off:end].split();assert head[1]==b'blob';n=int(head[2]);off=end+1;raw=data[off:off+n];off+=n+1;result[p]=[len(raw),hashlib.sha256(raw).hexdigest()]
 assert off==len(data);return result
assert blobs(paths-{mp})==old['files'],'Preserve failed-seal payload exactly before explicitly adding repair helper.'
target=b/'audit/job_geology_river_runtime_v1_20261002/review_tools'/Path(__file__).name;shutil.copyfile(__file__,target)
ip=b/'design/audit_impacts/job-geology-river-painted-runtime-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{target.relative_to(b).as_posix()});write(ip,d)
for name,args in [('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:
 q=subprocess.run(args,cwd=b,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);(out/(name+'.stdout.log')).write_bytes(q.stdout);(out/(name+'.stderr.log')).write_bytes(q.stderr);assert q.returncode==0,(name,q.stdout.decode(errors='replace')[-2000:]);print('Final seal '+name+':PASS',flush=True)
git('add','-f','--',target.relative_to(b).as_posix(),ip.relative_to(b).as_posix())
paths={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p};files=blobs(paths-{mp})
old['files']=files;old['required_files']=len(files);old['required_payload_bytes']=sum(v[0] for v in files.values());old['payload_sha256']=hashlib.sha256(''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()).hexdigest();write(b/mp,old)
git('add','-f','--',mp);raw=git('show',':'+mp)
ci=read(b/'audit/job_geology_river_runtime_v1_20261002/full_ci_v1/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['before_sha256'] for x in ci['source_checks'])
seal={'status':'EXACT_CANONICAL_CURRENT_SCOPED_BLOBS_SEALED','base_revision':base,'map_path':mp,'map_sha256':hashlib.sha256(raw).hexdigest(),'payload_sha256':old['payload_sha256'],'payload_files':len(files),'payload_bytes':old['required_payload_bytes'],'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'recovered_failure':'V241 explicit map add was rejected because audit paths are gitignored. Prior payload verified unchanged; force-add only exact authorized map/helper/impact paths. No reset or unrelated staging.','qualification':'Tested reversible topic checkpoint; exact publisher repeats full-suite/362-source checks and anonymous remote hash validation.'}
write(b/'tmp/geology_checkpoint_j_sealed.json',seal);write(out/'RECEIPT.json',seal);print(json.dumps(seal),flush=True)
