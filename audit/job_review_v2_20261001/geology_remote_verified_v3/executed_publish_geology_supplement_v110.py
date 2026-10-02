from pathlib import Path
import subprocess, json, hashlib, datetime, sys
b = Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out = b / 'tmp/geology_supplement_publish_v110'
out.mkdir(exist_ok=False)
branch = 'codex/job-art-review-v2-20261001'
def run(name, args, timeout=600):
    p = subprocess.run(args, cwd=b, capture_output=True, timeout=timeout)
    (out/(name+'.stdout.log')).write_bytes(p.stdout)
    (out/(name+'.stderr.log')).write_bytes(p.stderr)
    print(name, p.returncode, flush=True)
    assert p.returncode == 0, p.stderr.decode(errors='replace')[-900:]
    return p.stdout
def git(*args):
    p=subprocess.run(['git',*args],cwd=b,capture_output=True,check=True)
    return p.stdout
seal=json.loads((b/'tmp/geology_supplement_v109_sealed.json').read_text())
assert git('rev-parse','HEAD').decode().strip()==seal['base_revision']
assert git('branch','--show-current').decode().strip()==branch
mp=seal['map_path']; mb=git('show',':'+mp)
assert hashlib.sha256(mb).hexdigest()==seal['map_sha256']
m=json.loads(mb); expected=dict(m['files']);expected[mp]=[len(mb),hashlib.sha256(mb).hexdigest()]
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}
assert staged==set(expected)
paths=sorted(expected)
proc=subprocess.run(['git','cat-file','--batch'],cwd=b,input=''.join(':'+p+'\n' for p in paths).encode(),capture_output=True,check=True)
data=proc.stdout;offset=0
for path in paths:
    end=data.index(b'\n',offset);header=data[offset:end].split();size=int(header[2]);offset=end+1;raw=data[offset:offset+size];offset+=size+1
    assert [len(raw),hashlib.sha256(raw).hexdigest()]==expected[path],path
assert offset==len(data)
snapshot=json.loads((b/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text())['source_files']
assert len(snapshot)==325 and all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in snapshot)
msg=out/'COMMIT_MESSAGE.txt'
msg.write_text('Rebuild geology sources with painted art and embedded geode crystals\n\nPreserve 14 ImageGen native originals and all 220 individually reviewed native comparisons. Correct owner-rejected flat-vector and loose-crystal claims without changing runtime bindings. Keep source scores, isolated placement and full action acceptance separate; all-job, device, child and owner report acceptance remain open. Seal a new 539-file supplement while retaining earlier maps and failed attempts.\n',encoding='utf-8')
run('commit',['git','commit','--file',str(msg)])
revision=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert git('rev-parse','HEAD^').decode().strip()==seal['base_revision']
for name,cmd in [('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:run(name,cmd)
run('fetch',['git','fetch','origin'])
run('push',['git','push','origin','HEAD:refs/heads/'+branch],1800)
assert git('rev-parse','origin/'+branch).decode().strip()==revision
receipt=dict(status='TOPIC_REVIEW_CHECKPOINT_PUBLISHED_REMOTE_VERIFICATION_PENDING',revision=revision,tree=tree,branch=branch,map_path=mp,map_sha256=seal['map_sha256'],payload_sha256=m['payload_sha256'],files=m['required_files'],bytes=m['required_payload_bytes'],source_count=325,production_source_unchanged=True,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),qualification='Reversible review publication only. No dev/master integration, runtime replacement or comprehensive owner acceptance.')
(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt),flush=True)
