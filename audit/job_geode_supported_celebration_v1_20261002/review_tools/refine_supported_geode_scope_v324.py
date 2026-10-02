from pathlib import Path
import datetime,hashlib,json,re,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=r/'audit/job_geode_supported_celebration_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert read(f/'runtime_gate/capture1280v1.receipt.json')['status']=='PASS' and read(f/'runtime_gate/capture1600v1.receipt.json')['status']=='PASS'
shutil.copyfile(r/'scripts/opera_world_backdrop_2d.gd',f/'baseline/ROOM_PROP_TRIAL_REJECTED.gd')
write(f/'ROOM_PROP_TRIAL_REJECTION_V324.json',{'status':'ROOM_PROP_TRIAL_REJECTED_GEODE_SUPPORT_RETAINED','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':{'path':'baseline/ROOM_PROP_TRIAL_REJECTED.gd','sha256':sha(f/'baseline/ROOM_PROP_TRIAL_REJECTED.gd')},'directly_reviewed_views':['attempt_01/native_views/geologist_1280_phase0_invitation.webp','attempt_01/native_views/geologist_1280_phase1_invitation.webp','attempt_01/native_views/geologist_1280_phase2_invitation.webp','attempt_01/native_frames/geode_1280_0125.webp'],'opinions':[{'item':'fossil display relationship','material':4.6,'mounted_relationship':3.2,'evaluation':'The same fossil is displayed twice when its invitation is active; Roshan/tail overlaps the lower painted specimen. Reject this mounted layout.'},{'item':'pan display relationship','material':4.6,'mounted_relationship':3.0,'evaluation':'The same pan appears twice when its invitation is active, and Roshan overlaps the lower dish. Reject this mounted layout.'},{'item':'mineral gallery relationship','material':4.6,'mounted_relationship':3.1,'evaluation':'Rival feet and lower body overlap the upper mineral so it appears the imp stands on a crystal. Reject this mounted layout.'},{'item':'supported celebration geode','material':4.6,'mounted_relationship':4.5,'evaluation':'Opened halves remain seated on the painted slab; no detached loot. Retain, pending every-frame both-width review.'}],'qualification':'Specific four directly inspected views only; the remaining trial views/frames are preserved and have no inherited direct-review claim. Final support-only candidate requires fresh captures and full suite. Original flat room defects remain explicit priorities.'})
receipt=read(f/'full_ci_v1/RECEIPT.json');assert receipt['status']=='PENDING'
receipt.update(status='NOT_RUN_PREPARED_SOURCE_SUPERSEDED_BY_ROOM_TRIAL_REJECTION',qualification='Prepared boundary is preserved; engine suite never launched. Fresh support-only source boundary/full suite2 required. No machine pass exists for this attempt.')
write(f/'full_ci_v1/RECEIPT.json',receipt)
# Scope narrowing happens before implementation: no new defect is fabricated.
scope='Reversible Geologist-only supported celebration. Keep unchanged open-geode painting rooted inside its two halves, seated on the reviewed painted stone slab throughout the earned curtain call, without the generic prop bounce. Reject the painted room-prop trial because it duplicates active invitations and overlaps actors; preserve all trial sources/captures and restore the pre-existing room presentation pending a separate owned-object/painted-room repair. No image generation, PNG edits, input/mechanics/save/reward or other-career changes.'
gaps='Original flat room props/background2.8/failed2048-per-screen native coverage, work contact2.7, clearing3.9, panning3.8, caption4.0, full training/story/physical device/child/owner/final all-job acceptance and strict zero-3D remain open. Rejected room reuse must not be counted as accepted art. No finding lifecycle closure, integration or release.'
p=f/'PLAN.json';d=read(p);d.update(scope=scope,acceptance_gaps=gaps,status='ROOM_TRIAL_REJECTED_FRESH_SUPPORT_ONLY_REVIEW_PENDING',scope_change='ROOM_PROP_TRIAL_REJECTION_V324.json');d['rules']=sorted(set(d['rules'])|{'DL-MOT-01','DL-MOT-03','DL-MOT-04','DL-MOT-05'});write(p,d)
p=r/'design/audit_impacts/job-geode-supported-celebration-20261002.json';d=read(p);d.update(scope=scope,acceptance_gaps=gaps,rules=read(f/'PLAN.json')['rules']);write(p,d)
p=r/'scripts/opera_world_backdrop_2d.gd';s=p.read_text(encoding='utf-8')
start=s.index('func _load_geology_props()');end=s.index('\n\nfunc _draw_geology_prop',start)
s=s[:start]+'''func _load_geology_props() -> void:
\tvar atlas := AtlasTexture.new()
\tatlas.atlas = load(GEOLOGY_WORK_ART + "work_slab.png") as Texture2D
\tatlas.region = Rect2(68, 332, 889, 369)
\tatlas.filter_clip = true
\tgeology_props["slab"] = atlas
'''+s[end:]
start=s.index('func _draw_geologist(');base=(f/'baseline/opera_world_backdrop_2d.gd').read_text(encoding='utf-8');original=base[base.index('func _draw_geologist('):]
needle='\tif bool(get_meta("geology_work_open", false)):\n';assert needle in original
original=original.replace(needle,'\tif stage_mode:\n\t\t# Only the earned specimen is staged here; live room props stay separate.\n\t\t_draw_geology_prop("slab", GEOLOGY_CELEBRATION_SLAB)\n\t\treturn\n'+needle,1)
s=s[:start]+original;p.write_text(s,encoding='utf-8',newline='\n')
p=f/'capture.gd';s=p.read_text();s=s.replace('attempt_01/','attempt_02/');p.write_text(s,encoding='utf-8',newline='\n')
p=f/'resource_contract.gd';s=p.read_text();s=s.replace('size() == 4','size() == 1').replace('4_SHARED_PAINTED_CROPS','ONE_SHARED_PAINTED_SLAB');p.write_text(s,encoding='utf-8',newline='\n')
for name in ['prepare_supported_geode_boards_v323.py','prepare_supported_geode_stills_v323.py']:
 p=f/'review_tools'/name;s=p.read_text();s=s.replace('attempt_01','attempt_02').replace('v1.receipt','v2.receipt').replace('_V1_','_V2_').replace('_V1.json','_V2.json');p.write_text(s,encoding='utf-8',newline='\n')
p=f/'review_tools/run_supported_geode_full_ci_v322.py';s=p.read_text();s=s.replace('full_ci_v1','full_ci_v2').replace('supported celebration full suite1','supported celebration full suite2');p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(f/'SOURCE_CURRENT_BEFORE_CAPTURES.json',f/'SOURCE_TRIAL_BEFORE_CAPTURES.json')
d=read(f/'SOURCE_CURRENT_BEFORE_CAPTURES.json');d['source_files']=[{'path':x['path'],'sha256':sha(r/x['path']),'bytes':(r/x['path']).stat().st_size} for x in d['source_files']];d.update(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='CURRENT_SUPPORT_ONLY_LITERAL_SOURCE_SNAPSHOT');write(f/'SOURCE_CURRENT_BEFORE_CAPTURES.json',d)
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
p=r/'ASSET_LICENSES.md';s=p.read_text();old='`OperaWorldBackdrop2D` uses the unchanged licensed `painted_work_v1_20261001` work_slab, fossil, pan and mineral PNGs through the same measured AtlasTexture regions already used by the specialist surface.';assert old in s;s=s.replace(old,'`OperaWorldBackdrop2D` uses the unchanged licensed `painted_work_v1_20261001/work_slab.png` through the same measured AtlasTexture region used by the specialist surface. The broader fossil/pan/mineral room reuse trial is rejected and preserved outside runtime evidence.');p.write_text(s,encoding='utf-8',newline='\n')
p=r/'design/05_DOC_LEDGER.md';s=p.read_text();s=s.replace('reversible painted celebration support and four room-prop reuse at task baseline','reversible painted celebration support; broader room-prop trial rejected for duplicate invitations and actor overlap at task baseline');p.write_text(s,encoding='utf-8',newline='\n')
p=r/'design/audit_impacts/job-geode-supported-celebration-20261002.json';d=read(p);d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()});write(p,d)
print('Rejected room-prop trial preserved; support-only source frozen for fresh captures and full suite2.')
