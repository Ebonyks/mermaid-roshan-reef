from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import datetime, hashlib, json, posixpath, re, subprocess
root=next(p for p in Path(__file__).resolve().parents if (p/'project.godot').is_file())
families=[('day-one-pool-live-refinement-v2-20261001', 'audit/day_one_pool_live_refinement_v2_20261001'), ('day-one-playroom-sign-v2-20261001', 'assets_src/imagegen/day1_playroom_sign_v2_20261001'), ('day-two-boxing-puff-reuse-v1-20261001', 'audit/day_two_boxing_puff_reuse_v1_20261001'), ('day-two-boxing-single-gloves-v1-20261001', 'assets_src/imagegen/day2_boxing_single_gloves_v1_20261001'), ('day-two-boxing-live-refinement-v1-20261001', 'audit/day_two_boxing_live_refinement_v1_20261001')]
manifest_paths={prefix+'/MANIFEST.json' for _,prefix in families}
assert all(not (root/name).exists() for name in manifest_paths),'Already sealed; preserve manifests.'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()=='5b8bfb989ca8012924115d45901252808edb9b62'
assert subprocess.run(['git','rev-parse','--verify','MERGE_HEAD'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode != 0
baseline=json.loads((root/'audit/day_one_pool_live_refinement_v2_20261001/full_ci_current_retry_v3/SOURCE_BEFORE.json').read_text())
for row in baseline['source_files']:assert hashlib.sha256((root/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
retry=json.loads((root/'audit/day_one_pool_live_refinement_v2_20261001/full_ci_current_retry_v3/RECEIPT.json').read_text())
assert retry['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and retry['overall_process_exit']==0
assert retry['source_unchanged'] and len(retry['source_checks'])==325
assert len(retry['probe_results'])==82 and all(r['process_exit']==0 for r in retry['probe_results'])
gates=json.loads((root/'audit/day_two_boxing_live_refinement_v1_20261001/current_document_gates_v5/RECEIPT.json').read_text())
assert gates['status']=='PASS'
http=json.loads((root/'audit/day_one_pool_live_refinement_v2_20261001/delivery_http_v4/RECEIPT.json').read_text())
assert http['status']=='PASS' and not http['failures'] and len(http['video_byte_ranges'])==18
ours=set()
for ident,prefix in families:
    p=root/'design/audit_impacts'/f'{ident}.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files'])|{prefix+'/MANIFEST.json'})
    p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    ours.update(d['files']);ours.add(p.relative_to(root).as_posix())
staging=sorted(ours-manifest_paths)
assert all((root/p).is_file() for p in staging)
for i in range(0,len(staging),70):subprocess.run(['git','add','-f','--sparse','--',*staging[i:i+70]],cwd=root,check=True)
tracked={p.decode() for p in subprocess.check_output(['git','ls-files','-z'],cwd=root).split(b'\0') if p}
deps={'AGENTS.md','SECURITY.md','project.godot','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md'}
deps.update(r['path'] for r in baseline['source_files'])
unresolved=set()
def visit(value):
    if isinstance(value,dict):
        for child in value.values():visit(child)
    elif isinstance(value,list):
        for child in value:visit(child)
    elif isinstance(value,str):
        name=value.removeprefix('res://')
        if name.startswith(('assets/','assets_src/','scripts/','design/','audit/','tools/')) and '\n' not in name and not ' ' in name:
            if name in tracked:deps.add(name)
            elif not any(x in name for x in ['*','{','}']):unresolved.add(name)
for _,prefix in families:
    for p in (root/prefix).rglob('*.json'):visit(json.loads(p.read_text(encoding='utf-8-sig')))
visit(json.loads((root/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text(encoding='utf-8')))
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k not in ['src','href'] or not v:continue
            target=urlsplit(urljoin('https://review.invalid/'+self.path,v))
            name=unquote(target.path).lstrip('/')
            if target.netloc=='review.invalid' and name in tracked:deps.add(name)
for _,prefix in families:
    for p in (root/prefix).rglob('*.html'):
        parser=Links();parser.path=p.relative_to(root).as_posix();parser.feed(p.read_text(encoding='utf-8'))
deps-=ours
batch=subprocess.Popen(['git','cat-file','--batch'],cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def raw(path):
    batch.stdin.write((':'+path+'\n').encode());batch.stdin.flush()
    header=batch.stdout.readline().decode().strip().split()
    assert len(header)==3 and header[1]=='blob',(path,header)
    content=batch.stdout.read(int(header[2]));assert len(content)==int(header[2])
    assert batch.stdout.read(1)==b'\n';return content
def record(path,role):
    content=raw(path);return {'path':path,'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content),'role':role,'byte_origin':'Exact staged Git blob of enclosing review revision'}
payload=[record(p,'Reversible source/native diagnostic/individual drafting opinion/preserved failure/authority and verification evidence') for p in staging]
dependencies=[record(p,'Exact enclosing revision dependency: declared sources, scoped artwork references, controllers, probes and authority') for p in sorted(deps)]
print(f'REVIEW_SEAL_PROGRESS|payload={len(payload)}|deps={len(dependencies)}|checking literal/staged normalization',flush=True)
normalizations=[]
for row in payload+dependencies:
    p=root/row['path']
    if not p.is_file():continue
    literal=p.read_bytes();staged=raw(row['path'])
    if literal!=staged:
        assert literal.replace(b'\r\n',b'\n')==staged.replace(b'\r\n',b'\n'),row['path']
        normalizations.append({'path':row['path'],'checkout_sha256':hashlib.sha256(literal).hexdigest(),'staged_sha256':row['sha256'],'method':'Declared Git CRLF/LF normalization only; no code or asset-content change.'})
digest=hashlib.sha256('\n'.join(r['path']+'\t'+r['sha256'] for r in payload).encode()).hexdigest()
for ident,prefix in families:
    manifest={'schema':'reef.joint-job-art-review-packet.v1','repository':'https://github.com/Ebonyks/mermaid-roshan-reef','branch':'codex/day2-art-replacements-batch1-20260930','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':'5b8bfb989ca8012924115d45901252808edb9b62','incoming_integration':'c5e98477efe4fe3c36d6bffe68818d84c2d08325','payload_revision':'Immutable enclosing commit; named by subsequent anonymous byte-verification receipt','packet_id':ident,'entry':prefix+'/index.html' if (root/prefix/'index.html').exists() else 'audit/job_artwork_refinement_live/index.html','scope':'Joint reversible review: live pool six refined props with complete ordered native action evidence and named body/grip priorities; unbound matte teddy sign; historical clean-puff and separate-glove source/static comparisons; live painted left/right boxing gloves and exact clean puff, all1402 action frames and16 current edge views reviewed. Failed generations, earlier native limits and red full-suite attempts remain inspectable. This does not establish exhaustive all-job acceptance.','acceptance':'OWNER_REVIEW_DRAFT. Selected individual art has scoped4.6 drafting opinions. Pool full actions4.2; guard/imp sequences4.2; belt sequence4.0. Counter4.0, connected imp acting3.8, belt contact/return3.8 and shared marked puff2.5 remain priorities. All-jobs discovery/refinement, ordinary played traversal, phone/child/owner approval and comprehensive final report remain unfinished. No finding closure, integration or release.','files':payload,'dependencies':dependencies,'packet_payload_sha256':digest,'declared_line_ending_normalizations':normalizations,'unresolved_text_only_mentions':sorted(unresolved),'unresolved_qualification':'Unresolved narrative/template/provider-relative strings are preserved data, not published artwork dependencies or proof of every actual job object. Every actual HTML resource link is separately checked.','manifest_hash_scope':'Five joint manifests and later anonymous remote receipts excluded from joint payload self-reference. Exact manifest bytes are remotely fetched and hashed separately.','machine_evidence':{'full_retry':'audit/day_one_pool_live_refinement_v2_20261001/full_ci_current_retry_v3/RECEIPT.json','unchanged_production_sources':325,'trusted_probe_processes':82,'fresh_document_contract':'audit/day_two_boxing_live_refinement_v1_20261001/current_document_gates_v5/RECEIPT.json','http_receipt':'audit/day_one_pool_live_refinement_v2_20261001/delivery_http_v4/RECEIPT.json'},'delivery_instructions':'Read each individual opinion beside its artwork, inspect ordered frames and failed attempts, and keep source, mounted appearance, contact, complete sequence and full played route distinct. Scores are drafting evaluations. Preserve protected originals. Approved-source reuse and complete-source new generations retain provenance. Green tests do not establish device, child, owner or cinematic acceptance.','remote_verification':'REMOTE_VERIFICATION.json added only after anonymous normalTLS immutable remote bytes match every payload/dependency/manifest.'}
    (root/prefix/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
subprocess.run(['git','add','-f','--sparse','--',*sorted(manifest_paths)],cwd=root,check=True)
batch.stdin.close();batch.stdout.close();batch.wait()
print(f'CURRENT_JOB_REVIEW_SEALED|payload={len(payload)}|deps={len(dependencies)}|bytes={sum(r["bytes"] for r in payload+dependencies)}|normalizations={len(normalizations)}|325 tested sources unchanged',flush=True)
