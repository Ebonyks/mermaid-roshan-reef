from pathlib import Path
import datetime,hashlib,html,json,shutil

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
raw=r/'tmp/doctor_sink_contact_v36'
out=r/'audit/day_two_wash_contact_study_v1_20261001/attempt_02'
assert not out.exists()
process=json.loads((raw/'PROCESS_RECEIPT.json').read_text(encoding='utf-8'))
assert process['status']=='PASS_STATIC_CAPTURE_ONLY' and process['source_unchanged']
out.mkdir()
shutil.copytree(raw/'native_views',out/'native_views')
for name in ['PROFILE.json','PROCESS_RECEIPT.json','parser.stdout.log','parser.stderr.log','inference.stdout.log','inference.stderr.log','analyzer.stdout.log','analyzer.stderr.log','native.stdout.log','native.stderr.log']:
 shutil.copyfile(raw/name,out/name)
shutil.copyfile(r/'tmp/capture_doctor_sink_contact_v36.gd',out/'executed_capture_doctor_sink_contact_v36.gd')
shutil.copyfile(r/'tmp/run_layered_sink_contact_v36.py',out/'executed_run_layered_sink_contact_v36.py')
shutil.copyfile(Path(__file__).with_name('prepare_layered_sink_study_v36.py'),out/'executed_prepare_layered_sink_study_v36.py')
shutil.copyfile(__file__,out/'executed_archive_layered_and_clean_reviews_v39.py')
capture=json.loads((out/'native_views/CAPTURE_RECEIPT.json').read_text(encoding='utf-8'))
assert len(capture['views'])==18
items=[]
for n,row in enumerate(capture['views']):
 p=out/'native_views'/row['path'];assert digest(p)==row['sha256']
 if row['variant'].startswith('original'):
  contact=2.3;composition=2.9
  text='The current actor uses a medical-tool pose at the left station. Separate schematic hands and a large flat basin remain on the right. This width retains the measured spatial and style mismatch. This static capture does not audit the complete original sequence.'
 else:
  contact=4.0 if row['sink_offset_x']==35 else 3.7
  composition=4.1 if row['sink_extent']==150 else 4.0
  text='Drawing the same sink behind Roshan and its original front cabinet region in front keeps her face, arms and attached soap cluster visible. The hands remain left of the faucet/basin centre; no stream connects them to water. The cabinet occludes much of the tail and appears suspended in the busy station composition. '
  text+=('The nearer35px offset improves the local work reading but does not establish contact.' if row['sink_offset_x']==35 else 'The55px offset increases the hand-to-faucet gap and weakens the washing reading.')
  text+=' The '+str(row['sink_extent'])+'px sink is a static test using unchanged source pixels; there is no accepted wet/rub/rinse/clean/return sequence.'
 items.append({'id':'DOCTOR-SINK-A02-%02d'%n,'path':row['path'],'sha256':row['sha256'],'native_dimensions':row['viewport'],'direct_full_native_review':True,'static_contact_score':contact,'static_composition_score':composition,'complete_action_score':None,'evaluation':text,'geometry':{k:row.get(k) for k in ['source','sink_extent','sink_offset_x','front_region','draw_order','character_rect','hand_source_landmark','hand_local','sink_rect']}})
review={'status':'ALL18_STATIC_NATIVE_VIEWS_REVIEWED_BELOW_CONTACT_FLOOR','reviewed_utc':stamp,'baseline':'fb03e0ac3dda1658e9ea188d33cc6e084871642b','direct_full_native_views':18,'views_unreviewed':0,'source_pixels_modified':False,'source_opinions':'Doctor washing source6/key1 retain earlier source4.5; first painted sink cell retains earlier source4.6. No source score is raised by this contact study.','items':items,'next_refinement':'Bring the faucet/basin closer to the exact hand anchors using the same original sink. Test the clean-hands source at game scale. A larger local activity composition may be needed for literal contact readability. Timed wet/rub/rinse/clean/return and interruption ownership remain open.','qualification':'Static fixture after real viewport approach; world activity stopped and current actor/task overlays hidden only for test. No shipping binding, animation, reward, device/child/owner or cinematic acceptance.'}
write(out/'REVIEW.json',review)
cards=''.join('<article id="'+x['id']+'"><h2>'+x['id']+'</h2><p>'+html.escape(x['path'])+' · '+str(x['native_dimensions'][0])+' × '+str(x['native_dimensions'][1])+'</p><p>Static contact '+str(x['static_contact_score'])+'/5 · composition '+str(x['static_composition_score'])+'/5</p><a href="native_views/'+x['path']+'"><img loading="lazy" src="native_views/'+x['path']+'" alt="'+html.escape(x['path'])+'"></a><p>'+html.escape(x['evaluation'])+'</p></article>' for x in items)
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doctor sink contact: layered attempt2</title><style>body{font:18px/1.55 system-ui;background:#eef4fa;color:#253447;margin:0}main{max-width:1180px;margin:auto;padding:24px}header,article{background:white;border-radius:20px;padding:22px;margin:0 0 22px}h1{line-height:1.15}img{display:block;max-width:100%;height:auto}p,a{overflow-wrap:anywhere}</style><main><header><a href="../attempt_01/index.html">Preserved first26 failed placements</a><h1>Doctor washing: all18 layered placements reviewed</h1><p>Connected hands are visible, but every tested placement remains below the4.5 contact floor. Bringing the basin closer and demonstrating water/soap/clean causality remain necessary. Every exact native view has an individual written evaluation below.</p><p><a href="REVIEW.json">Individual scores and geometry</a> · <a href="PROCESS_RECEIPT.json">Unchanged-source process receipt</a> · <a href="native_views/CAPTURE_RECEIPT.json">Capture hashes</a></p><p>'+html.escape(review['qualification'])+'</p></header>'+cards+'</main></html>'
(out/'index.html').write_text(page,encoding='utf-8',newline='\n')

clean=r/'assets_src/imagegen/day2_doctor_wash_clean_result_v1_20261001'
prompt=json.loads((clean/'ATTEMPT01_PROMPT.json').read_text(encoding='utf-8'))
alpha=json.loads((clean/'ATTEMPT01_ALPHA.json').read_text(encoding='utf-8'))
native=clean/'attempt01_native.png';assert digest(native)=='c7923b95b393b70bfd575a9a0e03959bd6c8b31697f2685ce13f748866b9e88b'
assert digest(Path(prompt['provider_original']))==digest(native)
cleanreview={'id':'WASH-DOCTOR-CLEAN-KEY01','status':'SOURCE_FLOOR_CANDIDATE_UNBOUND','reviewed_utc':stamp,'path':native.relative_to(r).as_posix(),'sha256':digest(native),'dimensions':[1122,1402],'source_score':4.5,'identity_score':4.5,'clean_state_source_score':4.5,'direct_review':['Complete generated native RGBA output','Original-size neutral white and aqua alpha compositing views'],'evaluation':'The child face, brown curls/rainbow lock, flower, coral-trim coat, teal shirt, heart satchel, broad rainbow tail and paired fin remain coherent with the washing draft. Both attached hands gently separate with readable rounded child fingers and no lather. The small smile and gaze make a plausible clean-hands ending. Source-only4.5 is a drafting floor; chest-level palms, hand separation and the transition from rubbing still need exact game-size and complete-action review.','alpha_evaluation':'Neutral white and aqua original-size views show no visible disconnected red flecks. Pure-red samples in the transparency display are alpha1/255, with none at alpha16 or higher; native hidden RGB and alpha remain unchanged. This observation does not establish mounted edge or target-device acceptance.','method':prompt['method'],'input':prompt['input'],'prompt_sha256':prompt['prompt_sha256'],'mounted_score':None,'sink_contact_score':None,'temporal_continuity_score':None,'complete_action_score':None,'runtime_bound':False,'owner_accepted':False,'qualification':'One complete source-only ending candidate. No wetting/rubbing/rinsing timing, clean payoff in-game, interruption/return, device/child/owner or cinematic delivery acceptance.'}
write(clean/'ATTEMPT01_REVIEW.json',cleanreview)
shutil.copyfile(Path(__file__).with_name('prepare_clean_wash_result_v37.py'),clean/'executed_prepare_clean_wash_result_v37.py')
shutil.copyfile(__file__,clean/'executed_archive_layered_and_clean_reviews_v39.py')
cleanhtml='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doctor clean-hands ending source</title><style>body{font:18px/1.55 system-ui;background:#eef4fa;color:#253447;margin:0}main{max-width:1180px;margin:auto;padding:24px}section{background:white;border-radius:20px;padding:22px;margin:0 0 22px}img{max-width:100%;height:auto}p,a{overflow-wrap:anywhere}.source{background:repeating-conic-gradient(#ebedf6 0%25%,#dce0ec 0%50%)0/24px 24px}</style><main><section><a href="../day2_doctor_wash_motion_v1_20261001/index.html">Preceding rubbing-source candidate</a><h1>Doctor washing: clean-hands ending</h1><p>Source4.5/5 · unbound · complete action pending</p><p>'+html.escape(cleanreview['evaluation'])+'</p><p><a href="ATTEMPT01_REVIEW.json">Bounded written evaluation</a> · <a href="ATTEMPT01_PROMPT.json">Exact input/prompt/native provenance</a> · <a href="ATTEMPT01_ALPHA.json">Alpha measurements</a></p><a href="attempt01_native.png"><img class="source" src="attempt01_native.png" alt="Complete unbound doctor character showing clean separated hands"></a><p>'+html.escape(cleanreview['alpha_evaluation'])+'</p><img loading="lazy" src="attempt01_review_white.png" alt="Review-only white alpha composite"><img loading="lazy" src="attempt01_review_aqua.png" alt="Review-only aqua alpha composite"><p>'+html.escape(cleanreview['qualification'])+'</p></section></main></html>'
(clean/'index.html').write_text(cleanhtml,encoding='utf-8',newline='\n')

license=r/'ASSET_LICENSES.md';s=license.read_text(encoding='utf-8')
for x in items:
 p=(out/'native_views'/x['path']).relative_to(r).as_posix();assert p not in s
 s+='\n| '+p+' | Codex official Godot4.7.2 contact study2026-10-01 | Project diagnostic capture; underlying artwork retains provenance | Same-source sink region layered behind/front, unchanged character pixels | Lossless native static screenshot; below contact floor, no shipping or complete-action acceptance. |\n'
for name in ['attempt01_native.png','attempt01_review_white.png','attempt01_review_aqua.png']:
 p=(clean/name).relative_to(r).as_posix();assert p not in s
 s+='\n| '+p+' | OpenAI built-in imagegen2026-10-01; full edit of doctor source6 | Generated project review artwork; source/prompt/native hashes in ATTEMPT01_PROMPT.json | '+('Native complete transparent image, unchanged provider bytes' if name.endswith('native.png') else 'Review-only neutral alpha composite; native original preserved')+' | Source4.5 unbound; contact, continuity, action and owner acceptance pending. |\n'
license.write_text(s,encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-wash-contact-study-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'))
d['rules']=sorted(set(d['rules'])|{'DL-ASSET-02','DL-ASSET-05','DL-ASSET-06','DL-VIS-03','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-VIS-08'})
d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for root in [out.parent,clean] for x in root.rglob('*') if x.is_file()})
d['validation']=[{'command':'Official Godot4.7.2 first26 static placements','result':'PASS','evidence':'audit/day_two_wash_contact_study_v1_20261001/attempt_01/PROCESS_RECEIPT.json; source hashes unchanged.'},{'command':'Individual native visual review, first26 placements','result':'FAIL','evidence':'audit/day_two_wash_contact_study_v1_20261001/attempt_01/REVIEW.json; contact2.0–3.8/composition2.8–4.0. Earlier failure preserved.'},{'command':'Official Godot4.7.2 layered18 static placements','result':'PASS','evidence':'audit/day_two_wash_contact_study_v1_20261001/attempt_02/PROCESS_RECEIPT.json; parser/inference/analyzer/native0 and source hashes unchanged.'},{'command':'Individual native visual review, layered18 placements','result':'FAIL','evidence':'audit/day_two_wash_contact_study_v1_20261001/attempt_02/REVIEW.json; contact3.7–4.0 and composition4.0–4.1, original2.3/2.9. Static floor not reached.'},{'command':'Direct clean-hands full-source and neutral alpha review','result':'PASS','evidence':'assets_src/imagegen/day2_doctor_wash_clean_result_v1_20261001/ATTEMPT01_REVIEW.json; source-only4.5, all mounted/timed scores null.'}]
write(impact,d)
allow=r/'tmp/v2_preview_allowed.json';a=set(json.loads(allow.read_text(encoding='utf-8')));a.update(d['files']);write(allow,sorted(a))
print(json.dumps({'layered_views':18,'contact_floor_reached':False,'clean_source':4.5,'complete_action':None,'source_pixels_preserved':True,'checkpoint_index':'c211 immutable map unchanged; separate new study files.'}))
