from pathlib import Path
import datetime, hashlib, json, shutil, subprocess

old = Path(__file__).resolve().parents[1]
new = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
base = '5b8bfb989ca8012924115d45901252808edb9b62'
source = '8e41deaf34f925869395cd8ab0affefe89f89ab5'
families = ['audit/day_one_pool_live_refinement_v2_20261001', 'assets_src/imagegen/day1_playroom_sign_v2_20261001', 'audit/day_two_boxing_puff_reuse_v1_20261001', 'assets_src/imagegen/day2_boxing_single_gloves_v1_20261001', 'audit/day_two_boxing_live_refinement_v1_20261001']
excluded = {p + '/MANIFEST.json' for p in families}
assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=new, text=True).strip() == base
assert subprocess.check_output(['git','branch','--show-current'], cwd=new, text=True).strip() == 'codex/job-art-review-v2-20261001'
assert subprocess.check_output(['git','status','--porcelain'], cwd=new) == b''
assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=old, text=True).strip() == source
for p in excluded:
    assert (old/p).read_bytes() == subprocess.check_output(['git','show',source+':'+p],cwd=old)
    assert not (new/p).exists()

def write(path, raw):
    target = new/path
    assert target.resolve().is_relative_to(new.resolve())
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)

out = 'audit/job_review_v2_20261001'
write(out+'/.gdignore', b'')
impact_path = 'design/audit_impacts/job-review-separate-v2-20261001.json'
impact = {'id':'job-review-separate-v2-20261001', 'baseline':base, 'source_revision':source,
 'scope':'Create a distinct topic review from the last clean baseline. Carry forward exact owned artwork/source/evidence blobs from immutable8e41, preserve original five sealed manifests remotely and in the original workspace, and create one separately named compact V2 representation with all original payload/dependency records. No sealed manifest is rewritten. Add unbound washing artwork and honest source-versus-mounted priorities; preserve full-suite/hosted-red evidence and all owner/device/child gaps.',
 'rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-MED-01','DL-MED-03','DL-MED-09','DL-ASSET-01','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-READ-01','DL-INT-02','DL-MOT-10','DL-MOT-11','DL-MOT-12','DL-MOT-13','DL-QA-03','DL-QA-09'],
 'findings':['MA-2D-002','MA-VIS-006','MA-PLAY-004'], 'files':[out+'/.gdignore'],
 'validation':[{'command':'Distinct-workspace carry-forward and immutable original preservation','result':'PENDING','evidence':out+'/CARRY_FORWARD_RECEIPT.json'}, {'command':'Current authority, development, 2D inventory and complete applicable gates','result':'PENDING','evidence':'Not yet run at distinct V2 candidate; priorA local82/82 and hostedA red remain historical evidence.'}, {'command':'All-job visual/device/child/owner acceptance','result':'PENDING','evidence':'Hundreds of individual source/context/action items and comprehensive owner report unfinished.'}],
 'acceptance_gaps':'No global4.5, complete all-jobs audit, ordinary-route, phone, child, owner, finding closure, integration, release or external cinematic acceptance. Metadata correction does not waive2D zero-debt requirements.'}
write(impact_path, (json.dumps(impact,indent=2)+'\n').encode())
paths = subprocess.check_output(['git','diff','--name-only','-z',base,source],cwd=old).decode().split('\0')
paths = sorted(p for p in paths if p and p not in excluded)
assert not any(p.startswith(('assets/book/','assets/audio/voices/','assets/characters/friends/','.secrets/','.codex/','.claude/','.github/')) or p in ['AGENTS.md','CLAUDE.md','SECURITY.md'] for p in paths)
cat = subprocess.Popen(['git','cat-file','--batch'],cwd=old,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
count=0; total=0
for p in paths:
    cat.stdin.write((source+':'+p+'\n').encode());cat.stdin.flush()
    header=cat.stdout.readline().decode().strip().split()
    assert len(header)==3 and header[1]=='blob', (p,header)
    size=int(header[2]); raw=cat.stdout.read(size); assert len(raw)==size and cat.stdout.read(1)==b'\n'
    write(p,raw);count+=1;total+=size
    if count%500==0: print('EXACT_BLOB_CARRY',count,'/',len(paths),flush=True)
cat.stdin.close();assert cat.wait()==0

local_dirs = ['assets_src/imagegen/day2_wash_foam_v1_20261001','audit/day_two_wash_bubble_reuse_v1_20261001']
local_files=[]
for prefix in local_dirs:
    for p in sorted((old/prefix).rglob('*')):
        if p.is_file():
            rel=p.relative_to(old).as_posix();write(rel,p.read_bytes());local_files.append(rel)
for name in ['PROFILE.json','PROCESS_RECEIPT.json','analyzer.stderr.log','analyzer.stdout.log','inference.stderr.log','inference.stdout.log','native.stderr.log','native.stdout.log','parser.stderr.log','parser.stdout.log']:
    p=old/'tmp/wash_foam_native_fit_v1'/name
    rel='assets_src/imagegen/day2_wash_foam_v1_20261001/native_fit_v1/'+name
    assert p.is_file();write(rel,p.read_bytes());local_files.append(rel)
for p in sorted((old/'tmp/wash_foam_native_fit_v1/native_views').rglob('*')):
    if p.is_file():
        rel='assets_src/imagegen/day2_wash_foam_v1_20261001/native_fit_v1/native_views/'+p.name
        write(rel,p.read_bytes());local_files.append(rel)
for name in ['capture_foam_native_fit_v1.gd','run_foam_native_fit_v1.py','prepare_foam_native_fit_v1.py']:
    rel='assets_src/imagegen/day2_wash_foam_v1_20261001/native_fit_v1/executed_'+name
    write(rel,(old/'tmp'/name).read_bytes());local_files.append(rel)
for src,rel in [
    ('audit/day_one_pool_live_refinement_v2_20261001/REMOTE_VERIFICATION.json',out+'/SOURCE_A_REMOTE_VERIFICATION.json'),
    ('tmp/current_public_remote_v6/CHECKPOINT_IDENTITY.json',out+'/SOURCE_A_CHECKPOINT_IDENTITY.json'),
    ('tmp/current_public_remote_v6/VERIFIED_FILES.jsonl',out+'/SOURCE_A_FETCH_JOURNAL.jsonl'),
    ('tmp/current_public_remote_v6/attempt_01/RESULT.json',out+'/SOURCE_A_REMOTE_RESULT.json'),
    ('tmp/verify_current_job_art_remote_v6.py',out+'/executed_source_a_remote_verifier_v6.py'),
    ('audit/job_review_publication_20261001/hosted_ci_8e41_failure_v1/STATE.json',out+'/HOSTED_A_FAILURE_STATE.json'),
    ('audit/job_review_publication_20261001/hosted_ci_8e41_failure_v1/failed_steps.log',out+'/HOSTED_A_FAILED_STEPS.log')]:
    write(rel,(old/src).read_bytes());local_files.append(rel)

original_path=families[0]+'/MANIFEST.json'
original=(old/original_path).read_bytes();data=json.loads(original)
source_map_sha=hashlib.sha256(json.dumps({'files':data['files'],'dependencies':data['dependencies']},sort_keys=True).encode()).hexdigest()
data['schema']='reef.joint-job-art-review-compact-representation.v2'
data['source_schema']='reef.joint-job-art-review-packet.v1'
data['payload_revision']=source
data['representation']={'id':'job-review-v2-20261001','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_manifest_path':original_path,'source_manifest_sha256':hashlib.sha256(original).hexdigest(),'source_manifest_url':'https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+source+'/'+original_path,'source_map_sha256':source_map_sha,'method':'Separately named compact JSON representation in a new clean-baseline workspace. Original files/dependencies, order, hashes, dimensions and declared normalizations preserved; original5 sealed manifests unchanged. New V2 review files and later evidence are separately indexed, never silently substituted for sourceA bytes.'}
compact=json.dumps(data,ensure_ascii=False,separators=(',',':')).encode()+b'\n'
assert len(compact)<4*1024*1024
assert json.loads(compact)['files']==json.loads(original)['files'] and json.loads(compact)['dependencies']==json.loads(original)['dependencies']
write(out+'/MANIFEST_V2.json',compact);local_files.append(out+'/MANIFEST_V2.json')
receipt={'schema':'reef.distinct-review-carry-forward.v2','baseline':base,'source_revision':source,'new_branch':'codex/job-art-review-v2-20261001','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'carried_exact_git_blobs':count,'carried_bytes':total,'original_sealed_manifest_paths_preserved_and_not_copied':sorted(excluded),'new_manifest_path':out+'/MANIFEST_V2.json','new_manifest_bytes':len(compact),'new_manifest_sha256':hashlib.sha256(compact).hexdigest(),'complete_source_maps_equal':True,'source_map_sha256':source_map_sha,'qualification':'Distinct review representation, not a modification of originalA handoff. OriginalA all9583 bytes publicly verified; A hostedCIred and outstanding scores preserved. New candidate gates/publication pending.'}
write(out+'/CARRY_FORWARD_RECEIPT.json',(json.dumps(receipt,indent=2)+'\n').encode());local_files.append(out+'/CARRY_FORWARD_RECEIPT.json')
for p in excluded: assert (old/p).read_bytes()==subprocess.check_output(['git','show',source+':'+p],cwd=old) and not(new/p).exists()
impact['files']=sorted(set([out+'/.gdignore']+local_files))
impact['validation'][0]['result']='PASS'
write(impact_path,(json.dumps(impact,indent=2)+'\n').encode())
print(json.dumps(receipt),flush=True)
