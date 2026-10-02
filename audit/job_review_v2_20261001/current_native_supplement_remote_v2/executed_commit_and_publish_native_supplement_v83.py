from pathlib import Path
import datetime, hashlib, json, subprocess, sys
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
def git(*args):return subprocess.run(['git',*args],cwd=r,capture_output=True,check=True).stdout
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
base='56d66f63e375b61cf02936b426a05a2b92c14d3b'
branch='codex/job-art-review-v2-20261001'
assert git('rev-parse','HEAD').decode().strip()==base
assert git('branch','--show-current').decode().strip()==branch
map_path='audit/job_review_v2_20261001/CURRENT_NATIVE_JOB_ART_SUPPLEMENT_FILES_V2.json'
index=git('show',':'+map_path)
assert hashlib.sha256(index).hexdigest()=='402e68d7b75e6d00bd7027b6b767af89ba89616c4043132538d5bb90f13e2d85'
m=json.loads(index);assert m['required_files']==444 and m['required_payload_bytes']==43281662
paths={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}
assert paths==set(m['files'])|{map_path}
assert not git('diff','--name-only').strip()
body=r/'tmp/native_supplement_commit_v83.txt'
body.write_text('Expand individual job art reviews and preserve reversible drafts\n\nAdd eight shared source sheets and94 native regions, seven nursery/teacher/geology source opinions and five separately illustrated cushions. Preserve all eight vector drafts with individual evaluations; five selected sources meet4.5 while current runtime bindings remain unchanged.\n\nKeep every94 doctor sink-contact view and every41 new local ComfyUI reference frame individually reviewed. Source4.5 does not pass contact4.4, water3.7 or motion4.0. Archive exact prior-checkpoint remote verification and its completed green hosted probe run; retain all preparation and prior CI failures.\n\nThe searchable register contains1532 items,571 inclusive source priorities and388 unassigned source opinions. Canonical-byte supplement maps444 payload files. Parser, inference, official4.7.2 import, authority/development, contract tests and2D no-regression pass;325 production source hashes remain unchanged. No mounted-action/device/child/owner, strict2D, integration or release acceptance.\n',encoding='utf-8',newline='\n')
p=subprocess.run(['git','commit','--file',str(body)],cwd=r,capture_output=True)
(r/'tmp/native_supplement_commit_v83.stdout.log').write_bytes(p.stdout)
(r/'tmp/native_supplement_commit_v83.stderr.log').write_bytes(p.stderr)
assert p.returncode==0,p.stderr.decode(errors='replace')[-1000:]
revision=git('rev-parse','HEAD').decode().strip()
assert git('show',revision+':'+map_path)==index
assert {x.decode() for x in git('diff','--name-only',base,revision,'-z').split(b'\0') if x}==paths
receipt=dict(status='COMMITTED_NATIVE_JOB_ART_REVIEW_SUPPLEMENT',revision=revision,tree=git('rev-parse',revision+'^{tree}').decode().strip(),base_revision=base,map_path=map_path,map_sha256=hashlib.sha256(index).hexdigest(),mapped_files=444,payload_bytes=43281662,staged_changes=445,committed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),qualification='Review-only work branch; exact new remote bytes and hosted checks pending; no dev integration or release.')
write(r/'tmp/native_supplement_commit_v83.RECEIPT.json',receipt)
print(json.dumps(receipt),flush=True)
for name,cmd in [('postcommit_authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('postcommit_development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto']),('fetch',['git','fetch','origin']),('push',['git','push','origin','HEAD:refs/heads/'+branch])]:
    with (r/('tmp/native_supplement_v83_'+name+'.stdout.log')).open('wb') as so,(r/('tmp/native_supplement_v83_'+name+'.stderr.log')).open('wb') as se:
        p=subprocess.run(cmd,cwd=r,stdout=so,stderr=se,timeout=900)
    print(name,p.returncode,flush=True)
    assert p.returncode==0,name
assert git('rev-parse','origin/'+branch).decode().strip()==revision
receipt['status']='PUBLISHED_NATIVE_JOB_ART_SUPPLEMENT_REMOTE_BYTES_AND_HOSTED_PENDING'
receipt['published_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
write(r/'tmp/native_supplement_commit_v83.RECEIPT.json',receipt)
print('PUBLISHED',revision,flush=True)
