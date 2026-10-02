from pathlib import Path
import datetime,hashlib,html,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
raw=r/'tmp/doctor_sink_contact_v44';out=r/'audit/day_two_wash_contact_study_v1_20261001/attempt_03';assert not out.exists();out.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
process=json.loads((raw/'PROCESS_RECEIPT.json').read_text(encoding='utf-8'));assert process['status']=='PASS_STATIC_CAPTURE_ONLY' and process['source_unchanged']
shutil.copytree(raw/'native_views',out/'native_views')
for name in ['PROFILE.json','PROCESS_RECEIPT.json','parser.stdout.log','parser.stderr.log','inference.stdout.log','inference.stderr.log','analyzer.stdout.log','analyzer.stderr.log','native.stdout.log','native.stderr.log']:shutil.copyfile(raw/name,out/name)
shutil.copyfile(r/'tmp/capture_doctor_sink_contact_v44.gd',out/'executed_capture_doctor_sink_contact_v44.gd')
shutil.copyfile(r/'tmp/run_closer_sink_contact_v44.py',out/'executed_run_closer_sink_contact_v44.py')
shutil.copyfile(Path(__file__).with_name('prepare_closer_sink_contact_v44.py'),out/'executed_prepare_closer_sink_contact_v44.py')
shutil.copyfile(__file__,out/'executed_archive_closer_contact_v46.py')
capture=json.loads((out/'native_views/CAPTURE_RECEIPT.json').read_text(encoding='utf-8'));assert len(capture['views'])==14
items=[]
for n,x in enumerate(capture['views']):
 assert sha(out/'native_views'/x['path'])==x['sha256']
 original=x['variant'].startswith('original');clean='clean_result' in x.get('source','')
 contact=2.3 if original else 4.0 if clean else 4.2
 composition=2.9 if original else 4.1
 text=('Current actor holds a medical tool at the left station while separate schematic hands/basin occupy the right. The original spatial and style mismatch persists.' if original else 'The closer basin now sits under the connected hand cluster and the same original front-rim region provides clearer depth. The shell basin and child share the painted palette. At this250px character fit the hands and action remain small; the cabinet hides most of the body and no water/rinsing causality is shown. '+('Clean palms remove the lather, but at native size their chest-level separation is partly lost against the rim. This static finishing view is4.0, below the source-only4.5 opinion.' if clean else 'The lather is attached, but a static soapy pose is not a rubbing/rinsing action; the current visual still needs a literal connected water/result sequence.'))
 items.append({'id':'DOCTOR-SINK-A03-%02d'%n,'path':x['path'],'sha256':x['sha256'],'native_dimensions':x['viewport'],'direct_full_native_review':True,'static_contact_score':contact,'static_composition_score':composition,'clean_result_static_score':4.0 if clean else None,'complete_action_score':None,'evaluation':text,'geometry':{k:x.get(k) for k in ['source','sink_extent','sink_offset_x','front_region','draw_order','character_rect','hand_source_landmark','hand_local','sink_rect']}})
review={'status':'ALL14_NATIVE_STATIC_VIEWS_REVIEWED_BELOW_FLOOR','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'direct_full_native_views':14,'views_unreviewed':0,'source_pixels_modified':False,'items':items,'source_opinions':'Washing/rubbing/clean sources retain unbound source-only4.5, sink first cell4.6. All source opinions are distinct from these below-floor mounted static views.','next_refinement':'A source reach extending the hands away from the chest may let Roshan work beside the basin without losing her body to the front rim. Preserve the reused sink. Audit larger local-action readability, water/contact, rubbing, rinsing, clean consequence and quiet return before runtime binding.','qualification':'Test-only native composition after actual viewport approach. No shipping binding, continuous motion, gameplay progress, ordinary whole-route/device/child/owner or cinematic acceptance.'}
write(out/'REVIEW.json',review)
cards=''.join('<article id="'+x['id']+'"><h2>'+x['id']+'</h2><p>'+html.escape(x['path'])+' · static contact'+str(x['static_contact_score'])+'/5 · composition'+str(x['static_composition_score'])+'/5</p><a href="native_views/'+x['path']+'"><img loading="lazy" src="native_views/'+x['path']+'" alt="'+html.escape(x['path'])+'"></a><p>'+html.escape(x['evaluation'])+'</p></article>' for x in items)
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doctor closer basin and clean ending</title><style>body{font:18px/1.55 system-ui;background:#eef4fa;color:#253447;margin:0}main{max-width:1180px;margin:auto;padding:24px}header,article{background:white;border-radius:20px;padding:22px;margin:0 0 22px}img{display:block;max-width:100%;height:auto}p,a{overflow-wrap:anywhere}</style><main><header><a href="../attempt_02/index.html">Previous18 layered views</a><h1>Doctor washing:14 closer-contact views</h1><p>All14 exact native views are directly reviewed. Local contact4.2 and clean ending4.0 remain below4.5; original views remain2.3. Every source is preserved and the complete action is still open.</p><p><a href="REVIEW.json">Every individual evaluation and anchor</a> · <a href="PROCESS_RECEIPT.json">Process receipt</a></p><p>'+html.escape(review['qualification'])+'</p></header>'+cards+'</main></html>'
(out/'index.html').write_text(page,encoding='utf-8',newline='\n')
license=r/'ASSET_LICENSES.md';s=license.read_text(encoding='utf-8')
for x in items:
 p=(out/'native_views'/x['path']).relative_to(r).as_posix();assert p not in s
 s+='\n| '+p+' | Codex official Godot4.7.2 closer-contact study2026-10-01 | Project diagnostic screenshot; underlying source provenance retained | Uniform full-character fit; same original sink and front-rim region | Lossless native static screenshot, below contact/result floor; no action or owner acceptance. |\n'
license.write_text(s,encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-wash-contact-study-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in out.rglob('*') if x.is_file()});d['validation'] += [{'command':'Official Godot4.7.2 closer-contact14 native capture','result':'PASS','evidence':(out/'PROCESS_RECEIPT.json').relative_to(r).as_posix()+'; parser/inference/analyzer/native0, source hashes unchanged.'},{'command':'Individual direct native visual review of all14 closer-contact views','result':'FAIL','evidence':(out/'REVIEW.json').relative_to(r).as_posix()+'; contact4.2/clean4.0/composition4.1 below floor; original2.3/2.9.'}];write(impact,d)
allow=r/'tmp/v2_preview_allowed.json';a=set(json.loads(allow.read_text(encoding='utf-8')));a.update(d['files']);write(allow,sorted(a))
print(json.dumps({'status':review['status'],'total_contact_native_views_across_three_attempts':58,'complete_action':None}))
