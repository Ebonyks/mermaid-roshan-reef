from pathlib import Path
import datetime, hashlib, html, json, shutil

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=b/'audit/job_river_join_study_v1_20261001'
s=b/'assets_src/imagegen/geologist_river_junctions_v1_20261001'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
scores={'dry_initial':4.3,'isolated_dry':4.3,'isolated_dry_straight':4.5,'isolated_dry_corner':4.3,'isolated_dry_t':4.1,'isolated_dry_cross':4.3,'connected_straight':4.4,'connected_corner':4.0,'connected_t_branch':4.1,'connected_cross':4.3,'partial_json_restored':4.3,'formerly_isolated_now_wet':4.1,'connected_complete':4.1,'quiet_single_completion':4.1}
notes={
 'dry_initial':'Complete painted endpoints are readable; the broad flat board still reads like a diagram. No newly joined tile is visible.',
 'isolated_dry':'One complete dry pool is readable at mounted scale. Endpoint pools and the new excavation float over a flat diagram-like bed.',
 'isolated_dry_straight':'Two dry endcaps form an open continuous channel. The narrow interior is readable, with a slight bank/value change at the meeting plane. 4.5 is provisional and remains an inclusive priority.',
 'isolated_dry_corner':'Dry corner is continuous and has no rail through its centre. The elbow bank becomes noticeably wider than the endpoint stub.',
 'isolated_dry_t':'T centre is open, but the right join has an abrupt vertical bank step and the central bank is wider than both endpoint stubs.',
 'isolated_dry_cross':'Dry loops and four-way centre connect clearly. Banks retain local width changes; the flat field still resembles a plumbing diagram.',
 'connected_straight':'Wet straight path is continuous. The source, old straight strip and new endcap differ in water highlights/width at join planes.',
 'connected_corner':'Wet elbow removes the internal crossing rail, but its top and left port banks show conspicuous shoulders and water-width steps.',
 'connected_t_branch':'Open wet T is readable, with abrupt port-width/value steps against the endcap and straight-strip components.',
 'connected_cross':'Cross water is uninterrupted and source-connected; minor bank-width joins remain visible against the three attached endpoint stubs.',
 'partial_json_restored':'Actual JSON-restored topology is conserved; its cross/straight bank steps remain visually present. Save success does not confer visual acceptance.',
 'formerly_isolated_now_wet':'Previously dry branches fill only after source connection. Continuous water improves readability, but elbow/straight shoulders and port-width seams remain visible.',
 'connected_complete':'The arbitrary route connects both endpoints and completes once. Clear blue interiors contain rooted ground islands; some elbow and strip join shoulders are still conspicuous.',
 'quiet_single_completion':'Further touch does not award another completion. Same completed network retains the visible port-width seams; a static still does not prove full action quality.'}
views=[]
for width in [1280,1600]:
 manifest=read(f/'attempt_03'/('MANIFEST_%d.json'%width))
 assert len(manifest['views'])==14
 for x in manifest['views']:
  assert hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['sha256']
  state=x['state'];x.update(id='RIVER-JOIN-V3-%d-%s'%(width,state.upper()),direct_review=True,material_score=4.6,mounted_detail_score=4.5,sampled_state_score=scores[state],network_score=None if state in ['dry_initial','isolated_dry'] else scores[state],work_bed_context_score=3.2,sampled_wetting_score=4.6 if state.startswith('connected') or state in ['formerly_isolated_now_wet','quiet_single_completion'] else None,complete_action_score=None,actor_contact_score=None,owner_acceptance=None,priority=True,evaluation=notes[state],reviewed_utc=now)
  views.append(x)
review={'schema':'reef.river-join-study.v3','baseline':'40b1c7bfe025f284507c586fea61b9dd76b61423','reviewed_utc':now,'status':'ALL28_NATIVE_V3_VIEWS_DIRECTLY_REVIEWED_PORT_STEPS_REJECTED4_0_TO4_4','current_native_views':views,'prior_review':'audit/job_river_join_study_v1_20261001/REVIEW.json','inherited_input_flow':'PASS_BOTH14_STATE_CAPTURES_REAL_INPUT_JSON_RESTORE_SINGLE_COMPLETION','production_binding':False,'qualification':'Non-runtime isolated drawing study; direct source/material4.6 does not pass port geometry, flat work bed3.2, absent actor/room/training/story/full timed action/device/child/owner. All28 actual native frames independently inspected, including both widths. V1/V2 source files and opinions preserved.'}
write(f/'REVIEW_V3.json',review)
write(f/'attempt_03'/'DIRECT_REVIEW.json',review)
style='body{font:17px/1.5 system-ui;background:#e9eeef;color:#292542;margin:0 auto;max-width:1180px;padding:26px}img{display:block;max-width:100%;height:auto}article{background:white;padding:18px;margin:24px 0;border-radius:12px}code{overflow-wrap:anywhere}a{color:#45318b}'
cards=''.join('<article id="%s"><h2>%s · %s/5</h2><img src="%s" alt="%s" loading="lazy"><p>%s</p><p>Material4.6; bed3.2; full action, actor contact and owner acceptance unassigned.</p><code>%s</code></article>'%(x['id'],x['id'],x['sampled_state_score'],x['path'].split('job_river_join_study_v1_20261001/')[1],x['id'],html.escape(x['evaluation']),x['sha256']) for x in views)
(f/'index_v3.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>River join study V3</title><style>'+style+'</style><h1>River join study V3: open interiors, visible join steps</h1><p>Every28 native still directly reviewed. Source material4.6 does not pass assembled geometry4.0–4.4. This isolated subclass preserves actual input/flow/save/completion; production is unchanged.</p><p><a href="index.html">Earlier rejected22 views</a> · <a href="REVIEW_V3.json">Individual written scores</a> · <a href="../../assets_src/imagegen/geologist_river_junctions_v1_20261001/index.html">Wet/dry source artwork</a></p>'+cards,encoding='utf-8')
wet=read(s/'wet_attempt_01'/'REVIEW.json');dry=read(s/'dry_attempt_01'/'REVIEW.json');derivs=read(s/'TECHNICAL_DERIVATIVES.json')['derivatives']
native=[]
for x in [wet,dry]:native.append({'native_path':x['native_path'],'sha256':x['native_sha256'],'source_dimensions':x['native_dimensions'],'source_score':x['source_score'],'direct_review':True,'runtime_bound':False})
aggregate={'status':'ALL2_NATIVE2_DERIVATIVE8_COMPONENTS_DIRECTLY_REVIEWED_SOURCE4_6_JOINS_REJECTED','native_originals':native,'technical_derivatives':derivs,'components':wet['components']+dry['components'],'latest_refinement':{'report':'audit/job_river_join_study_v1_20261001/index_v3.html','note':'All28 current native grid states directly reviewed; open interiors are improved, but port-width steps4.0–4.4 fail the visual floor. Earlier ring/rail study3.6–3.9 retained.'},'qualification':'Source opinions only: every2 original,2 complete derivative and8 complete object regions directly reviewed4.6. None is production bound. Actual wet/dry shared joins, bed, contact, full action, training/story/device/child/owner remain open.','reviewed_utc':now}
write(s/'REVIEW.json',aggregate)
cards=[]
for x in native+derivs:
 p=x.get('native_path',x.get('path'));name=p.split('geologist_river_junctions_v1_20261001/')[1]
 cards.append('<article><h2>%s · source4.6/5</h2><img src="%s" alt="%s"><p>Complete preserved original or uniform complete-canvas derivative. Unbound; no joined-network or action acceptance.</p><code>%s</code></article>'%(name,name,name,x['sha256']))
for x in aggregate['components']:
 rx,ry,rw,rh=x['region'];width,height=x['source_dimensions'];scale=360/rw;p=x['path'].split('geologist_river_junctions_v1_20261001/')[1]
 window='<div style="width:360px;max-width:100%%;height:%.5fpx;overflow:hidden;position:relative;background:#e4eff0"><img src="%s" alt="%s" style="position:absolute;max-width:none;width:%.5fpx;height:%.5fpx;left:%.5fpx;top:%.5fpx"></div>'%(rh*scale,p,x['id'],width*scale,height*scale,-rx*scale,-ry*scale)
 cards.append('<article id="%s"><h2>%s · source4.6/5</h2>%s<p>%s</p><p>Actual V3 joins4.0–4.4. Native region window is a review annotation; no extracted or repaired raster.</p></article>'%(x['id'],x['id'],window,html.escape(x['evaluation'])))
(s/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Painted river junction source review</title><style>'+style+'</style><h1>Painted dry/wet river junctions</h1><p>Two preserved ImageGen originals, two uniform1024 derivatives and eight individually reviewed object regions. All source4.6/5; actual port joins remain below the floor.</p><p><a href="../../../audit/job_river_join_study_v1_20261001/index_v3.html">All28 actual grid states and join scores</a> · <a href="REVIEW.json">Source evaluations and hashes</a></p>'+''.join(cards),encoding='utf-8')
# Small source-placement experiment before spending further ImageGen budget.
target=f/'join_surface_v4.gd';assert not target.exists()
target.write_text((f/'join_surface_v3.gd').read_text(encoding='utf-8').replace('var pixel_scale := 0.25','var pixel_scale := 0.18'),encoding='utf-8',newline='\n')
target=f/'capture_join_study_v4.gd';assert not target.exists()
target.write_text((f/'capture_join_study_v3.gd').read_text(encoding='utf-8').replace('/attempt_03/','/attempt_04/').replace('/join_surface_v3.gd','/join_surface_v4.gd'),encoding='utf-8',newline='\n')
target=f/'run_river_join_capture_v200.py';assert not target.exists()
target.write_text((f/'run_river_join_capture_v199.py').read_text(encoding='utf-8').replace("out=f/'attempt_03'","out=f/'attempt_04'").replace('capture%dv3','capture%dv4').replace('river_join_%d_v199','river_join_%d_v200').replace('capture_join_study_v3.gd','capture_join_study_v4.gd'),encoding='utf-8',newline='\n')
d=read(f/'TILE_CALIBRATION_V3.json');d.update(branch_uniform_scale=0.18,status='V4_UNIFORM_SCALE_CALIBRATION_PENDING_NATIVE_REVIEW',prior='TILE_CALIBRATION_V3.json',reason='V3 branches sampled before their banks become parallel; reduce branch uniform scale to match existing endcap width and sample nearer its already-painted open port. No pixels regenerated/stretched/warped/repaired. This experiment must pass every actual native join separately.')
write(f/'TILE_CALIBRATION_V4.json',d)
shutil.copyfile(__file__,f/Path(__file__).name)
for ip,folder in [(b/'design/audit_impacts/job-geology-river-join-study-20261001.json',f),(b/'design/audit_impacts/job-geology-river-junction-source-20261001.json',s)]:
 d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in folder.rglob('*') if p.is_file()});d['acceptance_gaps']='Every current native/source view directly reviewed. V3 joins4.0–4.4 rejected; V4 placement pending. No production/actor/room/training/story/complete-action/device/child/owner/global pass.';write(ip,d)
print('All28 V3 opinions preserved; source gallery12 displays written; V4 uniform-scale experiment prepared without new pixels.')
