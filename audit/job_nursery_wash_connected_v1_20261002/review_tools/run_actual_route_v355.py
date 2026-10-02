from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time
r=next(p for p in Path(__file__).resolve().parents if (p/'project.godot').is_file())
out=r/'audit/job_nursery_wash_connected_v1_20261002/actual_route_v2'
width=sys.argv[1];assert width in ['1280','1600']
out.mkdir(exist_ok=True);out=out/('process_'+width);assert not out.exists();out.mkdir()
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
baseline=json.loads((r/'audit/job_geode_supported_celebration_v1_20261002/full_ci_v3/SOURCE_BEFORE.json').read_text())
paths=[x['path'] for x in baseline['source_files']]
paths+=['scripts/opera_world_hotspot_2d.gd','scripts/opera_hotspot_catalog.gd','scripts/opera_gesture_surface.gd','assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_native.png','assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_whole_canvas_1024x608.png','assets/opera/worlds/widgets/widget_basin_doctor_bubbles.png','assets/opera/worlds/widgets/widget_basin_nursery_bubbles.png','audit/job_nursery_wash_connected_v1_20261002/review_tools/capture_actual_route_v355.gd']
paths += [p.relative_to(r).as_posix() for p in (r/'assets/opera').rglob('*.png') if any(c in p.name for c in ['doctor','nursery'])]
paths += ['scripts/opera_nursery_surface.gd'] + [p.relative_to(r).as_posix() for p in (r/'assets/opera/worlds/nursery/wash_connected_v1_20261002').glob('*') if p.is_file()]
paths += ['assets/opera/worlds/props/fx_bop_puff.png','assets/opera/worlds/props/fx_dust_puff.png']
paths += [p+'.import' for p in list(paths) if p.endswith('.png') and (r/(p+'.import')).is_file()]
sha=lambda p:hashlib.sha256((r/p).read_bytes()).hexdigest()
before={p:sha(p) for p in sorted(set(paths))}
profile={'baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'index_tree_not_rendered_source':subprocess.check_output(['git','write-tree'],cwd=r,text=True).strip(),'scope':'Actual production Bubble Bath card/caller, wash first-phase and normal partial-career Back at one aspect; connected fixed-layout candidate v2 states, viewport touch, production approach and natural clocks with measured timestamps. Main/menu room arrival remains a fixture; no complete visual/device/child/owner acceptance.','rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-03','DL-ASSET-05','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-READ-01','DL-INT-02','DL-MOT-10','DL-MOT-11','DL-MOT-12','DL-MOT-13','DL-QA-03'],'findings':['MA-VIS-006','MA-PLAY-004'],'original_bound_artwork':['assets/opera/worlds/widgets/widget_basin_doctor_bubbles.png','assets/opera/worlds/widgets/widget_basin_nursery_bubbles.png','assets/opera/worlds/actors/animation/roshan_doctor_sheet_a.png','assets/opera/worlds/actors/animation/roshan_nursery_sheet_a.png'],'source_before':before,'acceptance':'Pending direct visual evaluation of each full native view. Current newly bound candidate v2 artwork relative to HEAD; original and candidate_v1 sequences preserved. Complete native sequences require direct evaluation; no ordinary root route, phone, child or owner approval.'}
(out/'PROFILE.json').write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8')
env=dict(os.environ)
for key,folder in [('APPDATA','Roaming'),('LOCALAPPDATA','Local')]:
    target=out/folder;target.mkdir();env[key]=str(target)
script='audit/job_nursery_wash_connected_v1_20261002/review_tools/capture_actual_route_v355.gd'
commands=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',script]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',script]),('analyzer',[godot,'--headless','--path',str(r),'--check-only','--script','res://'+script]),('native',[godot,'--path',str(r),'--windowed','--resolution','1280x720','--script','res://'+script,'--','--width='+width,'--touch','--classic-touch-test'])]
rows=[]
for name,command in commands:
    started=time.monotonic()
    with (out/(name+'.stdout.log')).open('wb') as stdout,(out/(name+'.stderr.log')).open('wb') as stderr:
        try:
            result=subprocess.run(command,cwd=r,env=env,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW,timeout=900)
            code=result.returncode;timed_out=False
        except subprocess.TimeoutExpired:
            code=None;timed_out=True
    rows.append({'name':name,'command':command,'process_exit':code,'timed_out_owned_child':timed_out,'seconds':time.monotonic()-started})
    print(name,code,'timeout='+str(timed_out),flush=True)
    if code != 0:break
after={p:sha(p) for p in before}
passed=len(rows)==len(commands) and all(x['process_exit']==0 for x in rows) and before==after
receipt={'status':'PASS_ORIGINAL_VIEWPORT_ROUTE_NATIVE_CAPTURE' if passed else 'FAIL_PRESERVED','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'processes':rows,'source_before':before,'source_after':after,'source_unchanged':before==after,'qualification':'Newly bound candidate v2 artwork in a viewport-input/natural-clock catalog fixture; process checks only. Production source was edited before this frozen run, never during it. Direct visual evaluation, source score and mounted suitability are not inferred from process status. No complete visual, full menu/story-route, target-device, child or owner acceptance.'}
(out/'PROCESS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if passed else 1)
