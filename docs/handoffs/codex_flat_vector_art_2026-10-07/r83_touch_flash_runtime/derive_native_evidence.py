from pathlib import Path
import json,hashlib,datetime,struct,collections,shutil,os
T=Path.cwd();P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r83_touch_flash_runtime';S=Path(os.environ.get('R83_JOB_ROOT',str(P)));O=Path(os.environ.get('R83_ANALYSIS_OUTPUT',str(P)));O.mkdir(parents=True,exist_ok=True)
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
assert rd(S/'NATIVE_ATTEMPT2_RESULT.json')['status']=='PASS'
rows=[];cases=[];trials=[];checks=0
for width in (1280,1600):
 folder=P/'native'/('attempt2_actual_source_'+str(width));d=rd(folder/'capture_manifest.json');r=rd(folder/'RESULT.json');launch=rd(folder/'LAUNCH.json'); syntax=rd(folder/'SYNTAX.json')
 assert d['observer_status']=='PASS'and not d['errors']and all(x['pass']for x in d['checks'])
 assert d['renderer']=='mobile'and d['engine']['string']=='4.7.2-stable (official)'and d['aspect']==[width,720]
 assert r['exit_code']==0 and not r['timed_out']and r['normal_unchanged']and not r['runtime_source_changes']and not r['script_or_shader_errors']and r['fixture_unchanged']
 assert all(x['exit_code']==0 for x in syntax['checks'])
 for state in d['states']:
  f=folder/state['path'];raw=f.read_bytes(); assert sha(f)==state['sha256']and raw[:8]==b'\x89PNG\r\n\x1a\n';dim=list(struct.unpack('>II',raw[16:24]));assert dim==state['dimensions']==[width,720]
  assert state['classification']in ('EXCLUDED_BOOTSTRAP_CONTROL','EXCLUDED_WORK_BRANCH_RUNTIME_TRIAL')
  rows.append({'case':width,'id':state['id'],'path':f.relative_to(T).as_posix(),'bytes':len(raw),'sha256':sha(f),'dimensions':dim,'classification':state['classification'],'new_origin_dev_coverage_credit':False,'source_revision':launch['baseline'],'trial_touch_ui_sha256':launch['touch_ui_sha256'],'runtime_pin_sha256':launch['runtime_pin_sha256'],'main_instance_id':state['snapshot']['main_id'],'state_mode':state['snapshot']['mode']})
 for x in d['flash_trials']:
  c=x['onset']['candidate'];assert x['actual_input']and not x['visual_override']and x['freed']and x['painted_child_freed']and c['ancestor_rgb_preserved']and c['original_flat_style_retired']and c['parent_is_original_panel']and c['whole_source_bitmap']
  child=x['painted_child_instance_id'];parent=x['instance_id'];events=d['flash_lifecycle']
  assert sum(e['event']=='painted_child_tree_exiting'and e['instance_id']==child and e['parent_instance_id']==parent for e in events)==1
  assert sum(e['event']=='tree_exiting'and e['instance_id']==parent for e in events)==1
  trials.append({'aspect':width,'consumer':x['consumer'],'actual_original_input':True,'visual_or_controller_override':False,'parent_instance_id':parent,'child_instance_id':child,'onset':x['onset'],'decay':x['decay'],'same_parent_and_child_naturally_freed':True,'source_fade_configuration_seconds':0.35,'limits':'Readback and instrumented wall time are not device latency, exact elapsed tween duration or performance acceptance.'})
 checks+=len(d['checks']);cases.append({'aspect':[width,720],'observer_checks':len(d['checks']),'frames':len(d['states']),'flash_lifecycles':len(d['flash_trials']),'normal_unchanged':True,'post_import_pin_exact':True,'renderer':'mobile','status':'PASS','report_path':(folder/'capture_manifest.json').relative_to(T).as_posix(),'report_sha256':sha(folder/'capture_manifest.json')})
summary={'schema':'reef.touch_flash_runtime_summary/1','recorded_at_utc':rd(S/'NATIVE_ATTEMPT2_RESULT.json')['checked_at_utc'],'baseline':'dd799b2d43871b29d1d6e0503646308a194dad1e','stable_role':'FV-7976FC8C2881','scope_id':'FVS-38151AC2830B','candidate_id':'FV-CAND-R82-RING-01','cases':cases,'native_cases':len(cases),'healthy_observer_checks':checks,'native_frames':len(rows),'classifications':dict(collections.Counter(x['classification']for x in rows)),'actual_work_branch_flash_lifecycles':len(trials),'direct_child_lifecycles_verified':len(trials),'origin_dev_coverage_credit':0,'new_role_family_alias_credit':0,'new_reuse_samples':0,'existing_sample_work_branch_implemented':1,'dev_integrated':0,'approved':0,'accepted_removed':0,'replacement_runtime_verified_formal':0,'global_artwork_total':None,'global_distinct_screen_total':None,'global_regressions_total':None,'full_local_ci':'Separate evidence lane; never inferred from these native checks','new_use_QA11_device_child_owner':'PENDING','failed_native_preflight_attempts_retained':1,'failed_native_preflight_game_launches':0,'source_pin_scope':'Original pin retained; 1102 import sidecar exact CRLF-to-LF-only changes bound to baseline Git; these cases use the separate exact post-import pin.'}
wr(O/'NATIVE_SUMMARY.json',summary);wr(O/'CAPTURE_INDEX.json',{'schema':'reef.runtime_trial_frames/1','frames':rows,'scope':'Unmodified raw Godot PNGs from actual work-branch source. Work-branch trial/bootstrap excluded from current origin/dev coverage and acceptance; not distinct art or screen counts.'});wr(O/'FLASH_LIFECYCLE.json',{'trials':trials,'scope':'Actual source Panel/texture child identity, ancestor RGB, natural fade/free; no observer visual/controller overrides. No human/device acceptance.'})
for name in ['NATIVE_ATTEMPT2_LAUNCH.json','NATIVE_ATTEMPT2_RESULT.json','attempt2_native_1280_driver.log','attempt2_native_1600_driver.log','ENV_ISOLATION_PREFLIGHT.json']:
 if name!='ENV_ISOLATION_PREFLIGHT.json' and (S/name).resolve()!=(O/name).resolve():shutil.copyfile(S/name,O/name)
if O.resolve()==P.resolve():
 I=T/'design/audit_impacts/flat-vector-touch-runtime-20261016.json';v=rd(I);v['files']=sorted(set(v['files']+[f.relative_to(T).as_posix()for f in P.rglob('*')if f.is_file()and'__pycache__'not in f.parts]));wr(I,v)
print('R83_NATIVE_DERIVED',json.dumps({k:summary[k]for k in ['native_cases','healthy_observer_checks','native_frames','classifications','actual_work_branch_flash_lifecycles','accepted_removed']}))
