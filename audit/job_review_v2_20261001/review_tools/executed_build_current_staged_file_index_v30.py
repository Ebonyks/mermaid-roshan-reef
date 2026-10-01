from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');family=r/'audit/job_review_v2_20261001';index=family/'CURRENT_B_FILES_V1.json'
assert not index.exists()
gates=json.loads((family/'document_gates_v7/RECEIPT.json').read_text(encoding='utf-8'));assert gates['status']=='PASS'
source='8e41deaf34f925869395cd8ab0affefe89f89ab5';manifestpath=family/'MANIFEST_V2.json';m=json.loads(manifestpath.read_text(encoding='utf-8'))
assert m['payload_revision']==source
helper=family/'review_tools/executed_build_current_staged_file_index_v30.py';shutil.copyfile(__file__,helper)
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'))
d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in family.rglob('*') if x.is_file()}|{index.relative_to(r).as_posix()})
d['scope']+=' Seal a separately named currentB file map from canonical staged Git blobs; sourceA payload map and five remote original manifests remain immutable source history, not currentB byte claims.'
impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
paths=sorted(x for x in d['files'] if (r/x).is_file())
assert all(not x.startswith(('.git/','.secrets/','.aws/','.codex/','.claude/','.github/')) and Path(x).name.lower() not in {'agents.md','security.md','claude.md'} for x in paths)
stage=r/'tmp/v2_exact_owned_stage_v30.bin';stage.write_bytes(b'\0'.join(x.encode() for x in paths)+b'\0')
with (r/'tmp/v2_stage_v30.log').open('wb') as log:p=subprocess.run(['git','add','-f','--sparse','--pathspec-from-file='+str(stage),'--pathspec-file-nul'],cwd=r,stdout=log,stderr=subprocess.STDOUT)
assert p.returncode==0
stage_records={}
for record in subprocess.check_output(['git','ls-files','--stage','-z'],cwd=r).split(b'\0'):
 if not record:continue
 meta,path=record.split(b'\t',1);mode,oid,level=meta.split();assert level==b'0';stage_records[path.decode('utf-8')]=oid.decode('ascii')
source_records={}
for record in subprocess.check_output(['git','ls-tree','-r','-z',source],cwd=r).split(b'\0'):
 if not record:continue
 meta,path=record.split(b'\t',1);mode,kind,oid=meta.split()
 if kind==b'blob':source_records[path.decode('utf-8')]=oid.decode('ascii')
oldmap={}
for row in m['files']+m['dependencies']:
 if row['path'] in oldmap:assert oldmap[row['path']]==[row['bytes'],row['sha256']]
 oldmap[row['path']]=[row['bytes'],row['sha256']]
changed=set(x.decode('utf-8') for x in subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMRT','-z'],cwd=r).split(b'\0') if x)
desired=set(oldmap)|changed|{x for x in d['files'] if x in stage_records}
desired.discard(index.relative_to(r).as_posix())
assert desired<=set(stage_records)
assert not any(x.startswith(('.secrets/','.aws/')) or 'keystore' in Path(x).name.lower() for x in desired)
files={};hashcache={};reused=0;hashed=0;total=0
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=r,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
try:
 for path in sorted(desired):
  oid=stage_records[path]
  if path in oldmap and source_records.get(path)==oid:
   value=oldmap[path];reused+=1
  elif oid in hashcache:value=hashcache[oid]
  else:
   proc.stdin.write((oid+'\n').encode('ascii'));proc.stdin.flush();header=proc.stdout.readline().split();assert len(header)==3 and header[0].decode()==oid and header[1]==b'blob'
   size=int(header[2]);left=size;sha=hashlib.sha256()
   while left:
    chunk=proc.stdout.read(min(left,1024*1024));assert chunk;sha.update(chunk);left-=len(chunk)
   assert proc.stdout.read(1)==b'\n';value=[size,sha.hexdigest()];hashcache[oid]=value;hashed+=1
  files[path]=value;total+=value[0]
finally:
 proc.stdin.close();proc.wait(timeout=30);assert proc.returncode==0
digest=hashlib.sha256(''.join(path+'\0'+str(value[0])+'\0'+value[1]+'\n' for path,value in files.items()).encode('utf-8')).hexdigest()
sealed={'schema':'reef.current-job-art-review-files.v1','repository':'https://github.com/Ebonyks/mermaid-roshan-reef','branch':'codex/job-art-review-v2-20261001','baseline':'5b8bfb989ca8012924115d45901252808edb9b62','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'revision_binding':'The enclosing immutable commit after publication; no pre-commit remote delivery claim.','byte_origin':'Canonical stage0 Git blobs. Matching immutable sourceA blob IDs reuse its anonymously verified SHA256/byte records. Changed/new blobs SHA256 streamed from git cat-file --batch, never Windows working-file CRLF substitutions.','entry':'audit/job_review_v2_20261001/index.html','file_value_schema':['bytes','sha256'],'files':files,'file_count':len(files),'payload_bytes':total,'sorted_payload_sha256':digest,'hash_scope':'This separately named file index excludes itself. Its exact blob is separately fetched/hashed against the immutable enclosing commit. Later publication-control receipts need a separate supplemental index and do not silently alter this file map.','source_a':{'revision':source,'map_path':'audit/job_review_v2_20261001/MANIFEST_V2.json','map_sha256':hashlib.sha256(manifestpath.read_bytes()).hexdigest(),'original_manifest_url':m['representation']['source_manifest_url'],'original_manifest_sha256':m['representation']['source_manifest_sha256'],'source_map_sha256':m['representation']['source_map_sha256'],'qualification':'ImmutableA history only; currentB files above may differ. Original five sealed manifests are never rewritten.'},'verification_work':{'source_a_same_blob_sha_records_reused':reused,'new_or_changed_unique_blobs_hashed':hashed},'acceptance':'Reversible partial owner-review draft. Full82 local trusted processes pass with unchanged325 source files; raw diagnostics and prior failures retained. All-job audit/refinement, complete natural actions, target-device/child/owner, strict2D, hosted current commit, integration and release remain separate and open.'}
data=json.dumps(sealed,ensure_ascii=False,separators=(',',':')).encode('utf-8')+b'\n';assert len(data)<4*1024*1024
index.write_bytes(data)
p=subprocess.run(['git','add','-f','--',index.relative_to(r).as_posix()],cwd=r,capture_output=True);assert p.returncode==0,p.stderr.decode('utf-8',errors='replace')
print(json.dumps({'status':'CANONICAL_CURRENT_B_FILE_INDEX_STAGED','file_count':len(files),'payload_bytes':total,'index_bytes':len(data),'index_sha256':hashlib.sha256(data).hexdigest(),'payload_sha256':digest,'source_a_records_reused':reused,'new_unique_blobs_hashed':hashed,'publication':'CurrentB uncommitted/unpublished. No global visual or owner acceptance.'}))
