from pathlib import Path
import datetime, hashlib, html, json, shutil

r = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
raw = r / 'tmp/doctor_sink_contact_v58'
out = r / 'audit/day_two_wash_contact_study_v1_20261001/attempt_04'
assert not out.exists()
out.mkdir()
proc = json.loads((raw/'PROCESS_RECEIPT.json').read_text(encoding='utf-8'))
assert proc['status'] == 'PASS_STATIC_CAPTURE_ONLY' and proc['source_unchanged']
shutil.copytree(raw/'native_views', out/'native_views')
for p in raw.glob('*.json'):
    shutil.copyfile(p, out/p.name)
for p in raw.glob('*.log'):
    shutil.copyfile(p, out/p.name)
for name in ['capture_doctor_sink_contact_v58.gd','run_reach_sink_contact_v58.py']:
    shutil.copyfile(r/'tmp'/name, out/('executed_'+name))
shutil.copyfile(Path(__file__).with_name('prepare_reach_sink_contact_v58.py'), out/'executed_prepare_reach_sink_contact_v58.py')
shutil.copyfile(__file__, out/'executed_archive_reach_contact_and_publication_v59.py')
views = json.loads((out/'native_views/CAPTURE_RECEIPT.json').read_text(encoding='utf-8'))['views']
assert len(views) == 18
opinions = {(250,140,0):(4.3,4.3),(250,140,20):(3.9,4.3),(250,160,0):(4.3,4.2),(250,160,20):(4.0,4.2),(300,140,0):(4.4,4.4),(300,140,20):(4.0,4.4),(300,160,0):(4.4,4.3),(300,160,20):(4.1,4.3)}
items=[]
for n,x in enumerate(views):
    assert sha(out/'native_views'/x['path']) == x['sha256']
    original = x['variant'].startswith('original')
    if original:
        contact, composition = 2.3,2.9
        evaluation = 'Current actor has a medical-tool pose at the left station while detached schematic hands and a basin appear on the right. This original spatial/style mismatch remains unchanged.'
    else:
        fit=int(x['character_rect'][3]); extent=int(x['sink_extent']); offset=int(x['sink_offset_x'])
        contact,composition=opinions[(fit,extent,offset)]
        evaluation = 'Connected outward forearms, a visible hand-over-hand lather cluster and the matching painted basin make the work clearer than the chest-clasp studies. '+('The300px fit enlarges the child and preserves more coat/tail visibility. ' if fit==300 else 'The250px fit leaves the hand action small in the busy clinic scene. ')+('The140px cabinet hides less of the body. ' if extent==140 else 'The160px cabinet conceals more of the lower silhouette. ')+('At zero offset the hands hover over the basin but remain left of the tap outlet; no running water connects them. ' if offset==0 else 'The20px rightward sink shift separates the tap and basin centre farther from the hand cluster; the hands sit near the left edge. ')+'The reused front rim provides plausible partial depth, but the cabinet still overlaps the tail and the action lacks wetting/rinsing and a matching clean-reaching result. This is a static fixture, not a completed wash.'
    items.append({'id':'DOCTOR-SINK-A04-%02d'%n,'path':x['path'],'sha256':x['sha256'],'native_dimensions':x['viewport'],'direct_full_native_review':True,'static_contact_score':contact,'static_composition_score':composition,'complete_action_score':None,'evaluation':evaluation,'geometry':{k:x.get(k) for k in ['source','sink_extent','sink_offset_x','front_region','draw_order','character_rect','hand_source_landmark','hand_local','sink_rect']}})
review={'status':'ALL18_NATIVE_REACH_VIEWS_REVIEWED_BELOW_CONTACT_FLOOR','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'direct_full_native_views':18,'views_unreviewed':0,'items':items,'best_static_contact_score':4.4,'best_static_composition_score':4.4,'total_contact_native_views_across_four_attempts':76,'source_pixels_modified':False,'next_refinement':'Reuse the same sink. Align its actual spout to the back-of-hand contact rather than the lower fingertips and add a small literal graphic stream/contact splash in a gameplay-only fixture. Generate a matching complete clean-reaching ending only for that named source gap. Audit timed rub/rinse/clean/quiet return independently.','qualification':'Actual viewport approach precedes static test-only composition. Old actor/stations/action panel hidden only for this study; no production asset/code binding, awards, wash progress, complete action, device/child/owner or cinematic acceptance.'}
write(out/'REVIEW.json',review)
cards=''.join('<article><h2>'+x['id']+'</h2><p>'+html.escape(x['path'])+' · contact'+str(x['static_contact_score'])+'/5 · composition'+str(x['static_composition_score'])+'/5</p><a href="native_views/'+x['path']+'"><img loading="lazy" src="native_views/'+x['path']+'" alt="'+html.escape(x['path'])+'"></a><p>'+html.escape(x['evaluation'])+'</p></article>' for x in items)
(out/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doctor reaching hands:18 native views</title><style>body{font:18px/1.55 system-ui;background:#edf4fa;color:#253447;margin:0}main{max-width:1180px;margin:auto;padding:24px}header,article{background:white;padding:22px;border-radius:20px;margin-bottom:22px}img{max-width:100%;height:auto;display:block}p,a{overflow-wrap:anywhere}</style><main><header><a href="../attempt_03/index.html">Previous14 closer-contact views</a><h1>Doctor outward reach:18 native contact views</h1><p>Every18 view directly inspected. Best static contact/composition4.4 remain below4.5. All76 contact views across four attempts remain available.</p><p><a href="REVIEW.json">Every individual evaluation</a> · <a href="PROCESS_RECEIPT.json">Process and unchanged sources</a></p><p>'+html.escape(review['qualification'])+'</p></header>'+cards+'</main></html>',encoding='utf-8')
lic=r/'ASSET_LICENSES.md';s=lic.read_text(encoding='utf-8')
for x in items:
    rel=(out/'native_views'/x['path']).relative_to(r).as_posix();assert rel not in s
    s+='\n| '+rel+' | Codex official Godot4.7.2 outward-reach contact study2026-10-01 | Project diagnostic screenshot; underlying asset provenance retained | Uniform complete-character fit, original sink region and same front rim | Lossless native static view; contact below floor, no runtime/whole-action/owner acceptance. |\n'
lic.write_text(s,encoding='utf-8',newline='\n')
ip=r/'design/audit_impacts/job-wash-contact-study-20261001.json';d=json.loads(ip.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in out.rglob('*') if p.is_file()});d['validation'] += [{'command':'Official Godot4.7.2 outward-reach18 native contact capture','result':'PASS','evidence':(out/'PROCESS_RECEIPT.json').relative_to(r).as_posix()+'; parser/inference/analyzer/native0 and exact source hashes unchanged.'},{'command':'Individual direct native review of all18 reaching contact placements','result':'FAIL','evidence':(out/'REVIEW.json').relative_to(r).as_posix()+'; best static contact/composition4.4, whole action unassigned.'}];write(ip,d)

# New publication receipt, separate from every earlier sealed byte map and receipt.
pub=r/'audit/job_review_v2_20261001/current_supplement_remote_v1';assert not pub.exists();pub.mkdir()
success=r/'tmp/review_supplement_remote_v57';failure=r/'tmp/review_supplement_remote_v55'
for p in success.glob('*'):
    if p.is_file():shutil.copyfile(p,pub/p.name)
result=json.loads((pub/'RESULT.json').read_text(encoding='utf-8'));assert result['status']=='PASS_ALL_IMMUTABLE_REVIEW_SUPPLEMENT_BYTES' and result['verified_files']==239 and not result['failures']
shutil.copytree(failure,pub/'verifier_attempt01_failure')
shutil.copyfile(Path(__file__).with_name('verify_review_supplement_remote_v57.py'),pub/'executed_verify_review_supplement_remote_v57.py')
shutil.copyfile(__file__,pub/'executed_archive_reach_contact_and_publication_v59.py')
post=r/'tmp/postcommit_review_v54'
for name in ['authority.stdout.log','authority.stderr.log','development.stdout.log','development.stderr.log','push.stdout.log','push.stderr.log','hosted_list.stdout.json','hosted_list.stderr.log','hosted_state.stdout.json','hosted_state.stderr.log']:
    shutil.copyfile(post/name,pub/name)
hosted=json.loads((pub/'hosted_state.stdout.json').read_text(encoding='utf-8'));assert hosted['headSha']==result['revision']
write(pub/'PUBLICATION_STATE.json',{'status':'SUPPLEMENT_PUBLISHED_ANONYMOUS_BYTES_PASS_HOSTED_PENDING','revision':result['revision'],'remote_verified_utc':result['checked_utc'],'hosted_snapshot_status':hosted['status'],'hosted_snapshot_conclusion':hosted['conclusion'],'hosted_run':hosted['url'],'qualification':'Historical observation only; this snapshot has no hosted completion. Earlier M failure remains archived. All artwork and sequence/device/child/owner acceptance remain independent.'})
(pub/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Review supplement publication receipt</title><style>body{font:18px/1.55 system-ui;max-width:1100px;margin:auto;padding:24px;background:#edf4fa;color:#253447}a,code{overflow-wrap:anywhere}</style><h1>Review supplement: exact published bytes verified</h1><p>Revision<code>'+result['revision']+'</code>:239/239 changed payload files,34,451,210 bytes and the40,562-byte map all match their immutable Git blobs using anonymous HTTPS with normal TLS. Checked'+result['checked_utc']+'.</p><p><a href="'+result['entry']+'">GitHub entry</a> · <a href="'+result['tree_url']+'">Immutable tree</a> · <a href="'+result['manifest']+'">Direct manifest</a> · <a href="RESULT.json">Remote verification receipt</a> · <a href="FETCH_JOURNAL.jsonl">Every actual path/hash/check time</a> · <a href="'+hosted['url']+'">Exact-revision hosted checks</a></p><p>The first verifier rejected an assumed digest formula before fetching payload files; its script and failure are preserved. The successful verifier uses the exact sealed builder formula. No map or artwork was altered. Hosted checks were still running at the saved observation; this receipt proves publication bytes only. No all-items4.5, full-action, owner approval, integration or release is claimed.</p>',encoding='utf-8')
entry=r/'audit/job_review_v2_20261001/index.html';s=entry.read_text(encoding='utf-8');assert '</nav>' in s;s=s.replace('</nav>','<a href="current_supplement_remote_v1/index.html">239-file corrected review: published bytes verified</a><a href="../day_two_wash_contact_study_v1_20261001/attempt_04/index.html">18 outward-reach native placements</a></nav>',1);entry.write_text(s,encoding='utf-8',newline='\n')
ip=r/'design/audit_impacts/job-review-current-remote-receipt-20261001.json';d=json.loads(ip.read_text(encoding='utf-8'));d['scope']+=' Archive exact C56d66 supplement remote verification, corrected verifier failure history and committed postcommit gates/push logs; do not rebind the older c211 map.';d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in pub.rglob('*') if p.is_file()});d['validation'].append({'command':'Anonymous normal-TLS GET of all239 supplement payload blobs and self-map at56d66','result':'PASS','evidence':(pub/'RESULT.json').relative_to(r).as_posix()+';239/239,34451210 payload bytes, empty failures; map exactGit40562 bytes. Hosted run36944960786 pending separately.'});write(ip,d)
allow=r/'tmp/v2_preview_allowed.json';a=set(json.loads(allow.read_text(encoding='utf-8')));a.update(p.relative_to(r).as_posix() for folder in [out,pub,r/'assets_src/imagegen/day2_doctor_wash_reach_v1_20261001'] for p in folder.rglob('*') if p.is_file());write(allow,sorted(a))
print(json.dumps({'contact_review':review['status'],'total_contact_views':76,'publication':result['status'],'hosted_observation':hosted['status']}))
