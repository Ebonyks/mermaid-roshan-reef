from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,urllib.request,urllib.parse
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=R/'tmp/connected_nursery_checkpoint_o_publish_v386';out.mkdir(exist_ok=False)
verify=R/'tmp/connected_nursery_checkpoint_o_remote_v386';verify.mkdir(exist_ok=False)
F=R/'audit/job_nursery_wash_connected_v1_20261002';branch='codex/job-art-review-v2-20261001'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args):return subprocess.run(['git',*args],cwd=R,capture_output=True,check=True).stdout
def run(label,args,timeout=600):
 p=subprocess.run(args,cwd=R,capture_output=True,timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/(label+'.stdout.log')).write_bytes(p.stdout);(out/(label+'.stderr.log')).write_bytes(p.stderr)
 print(label,p.returncode,flush=True)
 assert p.returncode==0,p.stderr.decode(errors='replace')[-1200:]
 return p.stdout
shutil.copyfile(Path(__file__),out/Path(__file__).name)
seal=read(R/'tmp/connected_nursery_checkpoint_o_sealed_v385.json')
assert seal['status']=='EXACT_SCOPED_O_BLOBS_SEALED'
assert git('rev-parse','HEAD').decode().strip()==seal['base_revision'] and git('branch','--show-current').decode().strip()==branch
mp=seal['map_path'];raw=git('show',':'+mp);assert sha(raw)==seal['map_sha256'];m=json.loads(raw)
expected=dict(m['files']);expected[mp]=[len(raw),sha(raw)]
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==set(expected)
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for path in sorted(expected):
 proc.stdin.write((':'+path+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().split();assert header[1]==b'blob',path
 n=int(header[2]);left=n;digest=hashlib.sha256()
 while left:
  chunk=proc.stdout.read(min(left,65536));assert chunk;left-=len(chunk);digest.update(chunk)
 assert proc.stdout.read(1)==b'\n' and [n,digest.hexdigest()]==expected[path],path
proc.stdin.close();assert proc.wait(timeout=30)==0
ci=read(F/'full_ci_v1/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['overall_process_exit']==0 and len(ci['probe_results'])==82 and all(r['process_exit']==0 for r in ci['probe_results'])
assert len(ci['source_checks'])==783 and all(sha((R/r['path']).read_bytes())==r['before_sha256'] for r in ci['source_checks'])
bridge=read(F/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_V381.json');assert bridge['status']=='PASS_ALL783_PUBLICATION_BOUNDARY_MEMBERS' and bridge['revision_source_members']==543 and bridge['auxiliary_generated_uid_members']==240
assert read(R/'assets_src/imagegen/nursery_palm_attention_v1_20261002/REFERENCE_UPLOAD_BLOCK.json')['reference_uploaded'] is False
run('fetch',['git','fetch','origin',branch])
assert git('rev-parse','origin/'+branch).decode().strip()==seal['base_revision'],'Topic advanced remotely; reconcile before publication.'
msg=out/'COMMIT_MESSAGE.txt';msg.write_text('Restore connected painted Nursery washing, preserve incomplete action review\n\nNursery WASH previously earned hold progress with an empty work oval. Add a presentation-only specialist using complete own-costume Roshan/basin paintings and suppress the Nursery-only generic boxing impact over clean palms. Input, progress, reward, save and sibling phase owners stay unchanged. Preserve seven native attempts and seven whole-canvas 1024 POT derivatives, including rejected clasp 4.4. Six mounted still states reach provisional 4.5–4.6; whole wash 3.9, attention 3.8, room 2.9 and transition 4.0 remain weak.\n\nDirectly review all 1631 current frames on36 ordered boards and36 full native details, across four training/authored catalog fixtures and actual Bubble Bath card/caller partial-career routes at1280/1600. Neither role belongs to the ordinary birthday roster; no full-career reward or birthday claim. Preserve original empty work, first overlap, pause/resume and partial Back-exit evidence.\n\nV34.1 illustrated register1756 entries adds14 source/derivative files and13 separately scored Nursery state/use/action opinions.690 source/cell/region priorities,10 current Nursery use priorities and385 unassigned source reviews remain. Withhold old Geologist mounted evidence after the shared CareerWorld binding changes. Add a complete dated Doctor review of all1023 preserved frames,24 boards,12 native details and12 individual priorities; dated whole2.7 does not approve current Doctor rendering.\n\nOne bounded local ComfyUI study through the unchanged developed GGUF graph is machine-complete but rejected: all41 native frames reviewed, action3.6/contact3.8/attention3.1. Preserve native output, input/prompt/workflow/dispatch and failed overlapping QA boards. No runtime or cinematic integration. The targeted eyes-to-hands edit remains blocked before any imagegen reference upload, awaiting explicit payload/destination approval. Publication does not bypass that rejected transmission.\n\nOfficial Godot4.7.2 unmodified local suite passes82/82, process0, against783 unchanged frozen local files; all53 raw diagnostics retained. Exact publication source bridge verifies543 revision source/import members plus240 preserved generated UID snapshots at non-runtime QA paths. Record only13 required Nursery import settings; unrelated dirty imports and protected originals stay untouched. First failed seal and complete gap inspection preserved. Authority/development/parser/inference/analyzer and review UI checks pass separately.\n\nImmutable V12 map covers exact changed payload and required prior/current references. Publish only this reversible topic checkpoint, then verify every required byte anonymously at its immutable revision. No finding closure, all-job/device/child/owner/integration or release acceptance.\n',encoding='utf-8',newline='\n')
run('commit',['git','commit','--quiet','--file',str(msg)],1800)
revision=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip();assert git('rev-parse','HEAD^').decode().strip()==seal['base_revision']
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
for label,args in [('authority',[py,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[py,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:run(label,args)
run('push',['git','push','origin','HEAD:refs/heads/'+branch],1800)
assert git('rev-parse','origin/'+branch).decode().strip()==revision
pub={'status':'TOPIC_CANDIDATE_PUBLISHED_REMOTE_VERIFICATION_PENDING','revision':revision,'tree':tree,'branch':branch,'map_path':mp,'map_sha256':seal['map_sha256'],'payload_sha256':m['payload_sha256'],'payload_files':m['required_files'],'payload_bytes':m['required_payload_bytes'],'local_ci_members':783,'revision_source_members':543,'auxiliary_generated_uid_members':240,'checked_utc':now(),'qualification':'Durable topic review checkpoint only. Visual/current-action/all-job/device/child/owner/integration/release remain open; blocked imagegen reference upload remains blocked.'};write(out/'RECEIPT.json',pub)
print('PUBLISHED_TOPIC_REVISION',revision,flush=True)
prefix='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'
started=now()
def fetch(path,expected_value,return_raw=False):
 for attempt in range(1,4):
  try:
   request=urllib.request.Request(prefix+urllib.parse.quote(path,safe='/'),headers={'User-Agent':'MermaidReef-Anonymous-Review-QA'})
   digest=hashlib.sha256();size=0;parts=[]
   with urllib.request.urlopen(request,timeout=60) as response:
    assert response.status==200
    while True:
     chunk=response.read(65536)
     if not chunk:break
     digest.update(chunk);size+=len(chunk)
     if return_raw:parts.append(chunk)
   row={'path':path,'bytes':size,'sha256':digest.hexdigest(),'attempt':attempt,'status':'FETCHED_ANONYMOUS_TLS_GET','expected_bytes':expected_value[0],'expected_sha256':expected_value[1],'matches':[size,digest.hexdigest()]==expected_value,'checked_utc':now()}
   return row,b''.join(parts) if return_raw else None
  except Exception as exc:
   if attempt==3:return {'path':path,'status':'FETCH_FAILED','error':str(exc),'expected_bytes':expected_value[0],'expected_sha256':expected_value[1],'matches':False,'checked_utc':now()},None
   time.sleep(attempt)
map_row,map_raw=fetch(mp,expected[mp],True);assert map_row['matches'] and json.loads(map_raw)==m
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(m['files'].items())).encode();assert sha(formula)==m['payload_sha256']
targets=dict(m['files']);targets.update(m.get('unchanged_required_files',{}));rows=[];fail=[]
with (verify/'VERIFICATION_JOURNAL.jsonl').open('w',encoding='utf-8',newline='\n') as journal:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  for future in concurrent.futures.as_completed([pool.submit(fetch,p,v) for p,v in targets.items()]):
   row,_=future.result();journal.write(json.dumps(row)+'\n');journal.flush();rows.append(row)
   if not row['matches']:fail.append(row)
   if len(rows)%250==0:print('REMOTE_BYTES_VERIFIED',len(rows),'FAILURES',len(fail),flush=True)
 journal.write(json.dumps(map_row)+'\n')
result={'status':'PASS_ALL_ANONYMOUS_REMOTE_BYTES' if not fail else 'FAIL_PRESERVED','revision':revision,'tree':tree,'branch':branch,'entry_url':'https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_nursery_wash_connected_v1_20261002/index.html','tree_url':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,'manifest_url':prefix+mp,'map_sha256':pub['map_sha256'],'payload_sha256':m['payload_sha256'],'payload_files':len(m['files']),'required_unchanged_files':len(m.get('unchanged_required_files',{})),'files_including_manifest':len(rows)+1,'payload_bytes':sum(v[0] for v in m['files'].values()),'access_mode':'Anonymous GET, normal TLS certificate verification, no Authorization header','started_utc':started,'finished_utc':now(),'failed_files':fail,'local_ci_members':783,'revision_source_members':543,'auxiliary_generated_uid_members':240,'qualification':'Every required immutable topic payload/reference byte checked. Publication evidence only; local/hosted/visual/action/device/child/owner/all-job/integration/release remain separate. No imagegen reference upload authorization.'}
write(verify/'RESULT.json',result);print(json.dumps(result),flush=True);raise SystemExit(0 if not fail else 1)
