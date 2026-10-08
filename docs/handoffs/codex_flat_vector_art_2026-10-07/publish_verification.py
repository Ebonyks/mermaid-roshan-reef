"""Bind packet bytes and verify anonymous immutable GitHub delivery.

REMOTE_VERIFICATION is deliberately excluded from the immutable payload digest;
its subsequent receipt-only commit is fetched separately to avoid self-reference.
This audit does not include runtime source images as generator input assets.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, subprocess, urllib.request, concurrent.futures
P=Path(__file__).resolve().parent;R=P.parents[2]
REL=P.relative_to(R).as_posix();BASE='92c9fe70319ef46bfaa8f61348a6f51512141ec3'
REPO='Ebonyks/mermaid-roshan-reef';REVISION='FV-AUDIT-20261007-R3'
def digest(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
def save(n,d):(P/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8', newline='\n')
def fetch(url):
    request=urllib.request.Request(url,headers={'User-Agent':'Mermaid-Roshan-flat-vector-audit/1','Cache-Control':'no-cache'})
    with urllib.request.urlopen(request,timeout=90) as response:
        if response.status!=200:raise RuntimeError('HTTP '+str(response.status)+' '+url)
        return response.read()
def manifest():
    rows=[]
    for f in sorted(P.rglob('*'),key=lambda item:item.relative_to(P).as_posix()):
        if f.is_file() and f.name not in {'MANIFEST.json','REMOTE_VERIFICATION.json'} and '__pycache__' not in f.parts:
            b=f.read_bytes();rows.append({'path':f.relative_to(P).as_posix(),'bytes':len(b),'sha256':digest(b),'role':'review_reference' if 'review' in f.parts else 'audit_payload'})
    serialized=''.join(row['path']+'\t'+row['sha256']+'\n' for row in rows).encode()
    sources={}
    for row in read('contact_index.json')['images']:
        sources[row['source_path']]={'role':'contact_original','worktree_bytes_sha256':row['source_sha256']}
    for row in read('per_piece.json')['pieces']:
        sources.setdefault(row['source']['path'],{'role':'named_piece_source','worktree_hash':row['source']['sha256'],'worktree_hash_mode':row['source']['hash_mode']})
    external=[]
    for path,metadata in sorted(sources.items()):
        b=subprocess.check_output(['git','show',BASE+':'+path],cwd=R)
        external.append({'path':path,'revision':BASE,'bytes':len(b),'sha256_git_blob_bytes':digest(b),**metadata})
    for live_machine in [P/'live_v2/MACHINE.json',P/'live_v3/MACHINE.json']:
        if not live_machine.is_file():continue
        for row in json.loads(live_machine.read_text(encoding='utf8'))['sources']:
            b=subprocess.check_output(['git','show',row['revision']+':'+row['path']],cwd=R)
            if digest(b)!=row['git_blob_sha256']:raise RuntimeError('bound live source drift '+row['path'])
            external.append({'path':row['path'],'revision':row['revision'],'bytes':len(b),'sha256_git_blob_bytes':digest(b),'role':'current_capture_runtime_source'})
    required_project=['AGENTS.md','SECURITY.md','ASSET_LICENSES.md','ART_STYLE_GUIDE.md','design/02_ART_DIRECTION.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/05_DOC_LEDGER.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/audit_impacts/flat-vector-art-audit-20261007.json','design/audit_impacts/flat-vector-live-review-20261008.json','design/audit_impacts/flat-vector-castle-dayone-review-20261008.json']
    project=[]
    for path in sorted(required_project):
        oid=subprocess.check_output(['git','hash-object','-w','--path='+path,path],cwd=R,text=True).strip()
        b=subprocess.check_output(['git','cat-file','blob',oid],cwd=R)
        project.append({'path':path,'bytes':len(b),'sha256_git_blob_bytes':digest(b),'role':'project_authority_or_source_license_at_immutable_payload_revision'})
    save('MANIFEST.json',{'schema':'reef.flat_vector_manifest/1','revision':REVISION,'source_baseline':BASE,'status':'AUDIT_CANDIDATE; zero-flat-vector goal remains active','destination':{'repository':REPO,'branch':'codex/flat-vector-art-audit-20261007','path':REL,'recipient':'Owner/dot internal audit handoff'},'files':rows,'payload_sha256':digest(serialized),'payload_hash_algorithm':'SHA-256 of sorted UTF-8 path + TAB + lowercase SHA-256 + LF for every listed payload file','excluded_post_publication_record':'REMOTE_VERIFICATION.json; receipt-only revision verified separately','external_bound_sources':external,'required_project_files':project,'project_revision_basis':'Same immutable payload commit; a receipt-only revision verifies these instructions at its named payload commit.','full_source_inventory_scope':'All 10,046 Git-declared source image metadata/hash records are census data, not a requirement to copy or generate with every source. Required visual previews are self-contained and their actual originals, plus all named source paths, are bound above. Runtime imports/export-only artifacts remain coverage gaps.','acceptance':'No generation/runtime replacement or artistic/device/child/owner acceptance is claimed.'})
    print('MANIFEST',len(rows),'payload files',len(external),'supporting source files')
def verify(revision,write_receipt,project_revision=None):
    project_revision=project_revision or revision
    prefix='https://raw.githubusercontent.com/'+REPO+'/'+revision+'/'+REL+'/'
    manifest_bytes=fetch(prefix+'MANIFEST.json');m=json.loads(manifest_bytes)
    if manifest_bytes!=(P/'MANIFEST.json').read_bytes():raise RuntimeError('remote manifest differs from local literal bytes')
    rows=m['files']
    if [r['path'] for r in rows]!=sorted({r['path'] for r in rows}):raise RuntimeError('payload paths must be unique canonical sorted UTF-8 paths')
    if any(Path(r['path']).is_absolute() or '..' in Path(r['path']).parts for r in rows):raise RuntimeError('unsafe payload relative path')
    serialized=''.join(row['path']+'\t'+row['sha256']+'\n' for row in rows).encode()
    if digest(serialized)!=m['payload_sha256']:raise RuntimeError('remote sorted payload digest mismatch')
    def one(row):
        b=fetch(prefix+row['path'])
        if len(b)!=row['bytes'] or digest(b)!=row['sha256']:raise RuntimeError('remote byte/hash mismatch '+row['path'])
        return {**row,'url':prefix+row['path'],'result':'PASS'}
    def source_one(row):
        url='https://raw.githubusercontent.com/'+REPO+'/'+row['revision']+'/'+row['path'];b=fetch(url)
        if len(b)!=row['bytes'] or digest(b)!=row['sha256_git_blob_bytes']:raise RuntimeError('remote source byte/hash mismatch '+row['path'])
        return {**row,'url':url,'result':'PASS'}
    def project_one(row):
        url='https://raw.githubusercontent.com/'+REPO+'/'+project_revision+'/'+row['path'];b=fetch(url)
        if len(b)!=row['bytes'] or digest(b)!=row['sha256_git_blob_bytes']:raise RuntimeError('remote project instruction hash mismatch '+row['path'])
        return {**row,'revision':project_revision,'url':url,'result':'PASS'}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        result=list(pool.map(one,rows));source_result=list(pool.map(source_one,m['external_bound_sources']));project_result=list(pool.map(project_one,m['required_project_files']))
    owner=json.loads(subprocess.check_output(['gh','api','repos/'+REPO],cwd=R));login=subprocess.check_output(['gh','api','user','--jq','.login'],cwd=R,text=True).strip()
    if login!='Ebonyks' or not owner['permissions']['pull']:raise RuntimeError('intended owner account read access not confirmed')
    receipt={'schema':'reef.flat_vector_remote_verification/1','status':'REMOTE_VERIFIED','request_id':REVISION,'repository':REPO,'branch':'codex/flat-vector-art-audit-20261007','path':REL,'payload_commit':revision,'source_baseline':BASE,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'recipient_access_modes':['Anonymous unauthenticated public immutable raw GitHub HTTP 200 for manifest, every payload file, every bound supporting source and all required project instructions/licenses','Connected intended owner Ebonyks GitHub API account with repository pull access'],'access_limit':'This proves public/owner access to this audit handoff. No external animator or Grok generation delivery/acceptance is claimed.','manifest_sha256':digest(manifest_bytes),'payload_sha256':m['payload_sha256'],'entry_url':'https://github.com/'+REPO+'/blob/'+revision+'/'+REL+'/README.md','immutable_tree_url':'https://github.com/'+REPO+'/tree/'+revision+'/'+REL,'direct_manifest_url':prefix+'MANIFEST.json','payload_file_count':len(result),'payload_verified_bytes':sum(r['bytes'] for r in result),'files':result,'supporting_source_file_count':len(source_result),'supporting_sources':source_result,'required_project_file_count':len(project_result),'required_project_files':project_result,'receipt_publication':'This record is published in a subsequent receipt-only revision; that revision is independently fetched and checked before a delivered claim.'}
    if write_receipt:save('REMOTE_VERIFICATION.json',receipt)
    print('REMOTE VERIFIED',revision,len(result),'payload files',len(source_result),'source files',receipt['payload_verified_bytes'],'bytes')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',action='store_true');ap.add_argument('--verify');ap.add_argument('--project-revision');ap.add_argument('--write-receipt',action='store_true');a=ap.parse_args()
    if a.manifest:manifest()
    elif a.verify:verify(a.verify,a.write_receipt,a.project_revision)
    else:ap.error('choose --manifest or --verify COMMIT')
