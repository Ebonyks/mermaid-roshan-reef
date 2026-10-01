from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time
r=Path(__file__).resolve().parents[1]
out=r/'tmp/wash_foam_native_fit_v1';assert not out.exists();out.mkdir()
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
baseline=json.loads((r/'audit/day_one_pool_live_refinement_v2_20261001/full_ci_current_retry_v3/SOURCE_BEFORE.json').read_text())
paths=[x['path'] for x in baseline['source_files']]
paths+=['scripts/opera_world_hotspot_2d.gd','scripts/opera_hotspot_catalog.gd','scripts/opera_gesture_surface.gd','assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_native.png','assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_whole_canvas_1024x608.png','assets/opera/worlds/widgets/widget_basin_doctor_bubbles.png','assets/opera/worlds/widgets/widget_basin_nursery_bubbles.png','tmp/capture_foam_native_fit_v1.gd']
sha=lambda p:hashlib.sha256((r/p).read_bytes()).hexdigest()
before={p:sha(p) for p in sorted(set(paths))}
profile={'baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'candidate_tree':subprocess.check_output(['git','write-tree'],cwd=r,text=True).strip(),'scope':'Unbound fresh matte foam02 in doctor/nursery actual invitation nodes, at exact original220x131 canvas size; eight original/candidate full native views. Placement and complete actions remain separate priorities. Source/action/complete-route claims remain separate.','rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-03','DL-ASSET-05','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-READ-01','DL-INT-02','DL-MOT-10','DL-MOT-11','DL-MOT-12','DL-MOT-13','DL-QA-03'],'findings':['MA-VIS-006','MA-PLAY-004'],'reuse_candidates':['assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png','assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_native.png','assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_whole_canvas_1024x608.png','assets/opera/worlds/widgets/widget_basin_shared_shine.png'],'source_before':before,'acceptance':'Pending direct visual evaluation of each full native view. Fresh source draft4.6 remains unbound; no runtime source change, native score or complete action, ordinary played route or owner approval.'}
(out/'PROFILE.json').write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8')
env=dict(os.environ)
for key,folder in [('APPDATA','Roaming'),('LOCALAPPDATA','Local')]:
    target=out/folder;target.mkdir();env[key]=str(target)
script='tmp/capture_foam_native_fit_v1.gd'
commands=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',script]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',script]),('analyzer',[godot,'--headless','--path',str(r),'--check-only','--script','res://'+script]),('native',[godot,'--path',str(r),'--windowed','--resolution','1280x720','--script','res://'+script,'--','--touch','--classic-touch-test'])]
rows=[]
for name,command in commands:
    started=time.monotonic()
    with (out/(name+'.stdout.log')).open('wb') as stdout,(out/(name+'.stderr.log')).open('wb') as stderr:
        try:
            result=subprocess.run(command,cwd=r,env=env,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW,timeout=180)
            code=result.returncode;timed_out=False
        except subprocess.TimeoutExpired:
            code=None;timed_out=True
    rows.append({'name':name,'command':command,'process_exit':code,'timed_out_owned_child':timed_out,'seconds':time.monotonic()-started})
    print(name,code,'timeout='+str(timed_out),flush=True)
    if code != 0:break
after={p:sha(p) for p in before}
passed=len(rows)==len(commands) and all(x['process_exit']==0 for x in rows) and before==after
receipt={'status':'PASS_UNBOUND_NATIVE_CAPTURE' if passed else 'FAIL_PRESERVED','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'processes':rows,'source_before':before,'source_after':after,'source_unchanged':before==after,'qualification':'Local unbound fixture/process checks only. No production source edited. Direct visual evaluation, source score and mounted suitability are not inferred from process status. No complete played action/route/device/child/owner acceptance.'}
(out/'PROCESS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if passed else 1)
